---
title: "How to create a bridge interface on the KVM host"
date: 2025-10-18T09:00:00+00:00
description: "Step-by-step guide to create a bridge (br0) on Linux and connect it to libvirt, with Netplan and ifupdown examples."
tags: [KVM,Virtualization,Libvirt,Networking,Linux,Bridge]
hero: images/virtualizacion-kvm-linux/redes/redes-puente.png
weight: 3
---

# Create a bridge network interface on the host for KVM/libvirt

A bridge on the host allows your virtual machines to connect directly to the physical network as if they were another machine on the LAN. It's the basis for "bridged networks" covered in the network types section.

Important: if you perform these changes over remote SSH you may lose connectivity. Whenever possible use local/console access or have a recovery plan (KVM/IPMI, a second interface, maintenance window, etc.).

---

## 0. Preparation: identify your physical interface and back up configs

1) Identify the physical interface connected to your LAN/Internet (for example: `enp1s0`, `enp3s0`, `eth0`):

```bash
ip -br link
ip -br addr
```

2) Back up your network configuration files before changing anything — use the command appropriate to your setup:

```bash
sudo cp -a /etc/netplan /etc/netplan.bak.$(date +%F) 2>/dev/null
sudo cp -a /etc/network/interfaces /etc/network/interfaces.bak.$(date +%F) 2>/dev/null
```

3) Important note: the IP must live on the bridge (`br0`), not on the physical interface. The physical interface will be left without an IP and become a slave of the bridge.

---

## Option A: Netplan (modern Ubuntu/Debian)

Applies to systems using Netplan (Ubuntu Server ≥ 18.04, Debian when migrated). The most common renderer is `networkd`, but `NetworkManager` can also be used. Here we configure `br0` and enslave the physical interface to the bridge.

Example — DHCP (networkd renderer):

```yaml
# /etc/netplan/01-br0.yaml
network:
	version: 2
	renderer: networkd
	ethernets:
		enp1s0:
			dhcp4: no
			dhcp6: no
	bridges:
		br0:
			interfaces: [enp1s0]
			dhcp4: yes
			dhcp6: no
			parameters:
				stp: true
				forward-delay: 0
```

Example — static address:

```yaml
# /etc/netplan/01-br0.yaml
network:
	version: 2
	renderer: networkd
	ethernets:
		enp1s0:
			dhcp4: no
			dhcp6: no
	bridges:
		br0:
			interfaces: [enp1s0]
			addresses: [192.168.1.50/24]
			routes:
				- to: default
					via: 192.168.1.1
			nameservers:
				addresses: [1.1.1.1,8.8.8.8]
			parameters:
				stp: true
				forward-delay: 0
```

Apply and verify:

```bash
sudo netplan apply
ip -br addr show br0
```

---

## Option B: /etc/network/interfaces (ifupdown)

For Debian/Ubuntu servers using the classic ifupdown system (no NetworkManager/Netplan). Ensure you have bridge support installed (e.g., the `bridge-utils` package for `brctl` and the `bridge_*` options).

Example 1 — DHCP on `br0`, physical interface without IP:

```ini
auto lo
iface lo inet loopback

auto enp1s0
iface enp1s0 inet manual

auto br0
iface br0 inet dhcp
		bridge_ports enp1s0
		bridge_stp on
		bridge_fd 0
```

Example 2 — static address on `br0`:

```ini
auto lo
iface lo inet loopback

auto enp1s0
iface enp1s0 inet manual

auto br0
iface br0 inet static
		address 192.168.1.50/24
		gateway 192.168.1.1
		dns-nameservers 1.1.1.1 8.8.8.8
		bridge_ports enp1s0
		bridge_stp on
		bridge_fd 0
```

Notes for ifupdown:
- The physical interface (`enp1s0`) is set to `manual` (no IP). The IP is assigned to `br0`.
- `bridge_stp on` enables STP on the bridge; `bridge_fd 0` minimizes forwarding delay (adjust as needed).
- If you use VLANs you can enable `bridge_vlan_aware yes` on distributions that support it or manage VLANs inside the VMs.

Apply changes carefully (you can lose SSH). Options:

```bash
# Restart networking service (may cut SSH):
sudo systemctl restart networking.service

# Or perform granular bring-down/up (safer with local console):
sudo ifdown enp1s0
sudo ifdown br0
sudo ifup br0
```

---

## Connect VMs to the bridge (libvirt)

Once `br0` is up:

- With `virt-install`:

```bash
virt-install \\
	--name vm-bridge-example \\
	--memory 2048 \\
	--vcpus 2 \\
	--disk size=10 \\
	--os-variant debian12 \\
	--network bridge=br0,model=virtio \\
	--cdrom /path/to/your.iso \\
	--noautoconsole
```

- With `virsh` for an existing VM (attach a bridged interface):

```bash
virsh attach-interface --domain EXISTING_VM \\
	--type bridge --source br0 \\
	--model virtio --config --live
```

- Domain XML fragment:

```xml
<interface type='bridge'>
	<source bridge='br0'/>
	<model type='virtio'/>
</interface>
```

After the VM boots it should get an IP from your physical network (DHCP from your router) or whatever static IP you configure inside the guest.

---

## Verification

- On the host:

```bash
ip link show br0
bridge link
ip route
```

Example `ip a` output:

```bash
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br0 state UP group default qlen 1000
	link/ether 52:54:00:22:d7:3f brd ff:ff:ff:ff:ff:ff
3: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
	link/ether 92:d8:69:79:60:69 brd ff:ff:ff:ff:ff:ff
	inet 192.168.121.169/24 brd 192.168.121.255 scope global dynamic br0
		 valid_lft 3595sec preferred_lft 3595sec
```

If you use `brctl` from `bridge-utils`:

```bash
sudo brctl show
# Expected:
# bridge name	bridge id		STP enabled	interfaces
# br0		8000.7eb448933f70	no	enp1s0
```

- Inside the VM connected to the bridge:

```bash
ip -br addr
ping -c 2 8.8.8.8
ping -c 2 <ROUTER_IP>
```

- From another LAN host, ping the bridged VM's IP to confirm connectivity.

---

## Managing bridged networks with libvirt (bridge vs macvtap)

Besides attaching VMs directly to `br0`, you can define libvirt networks that use the host bridge.

### 1) A libvirt network forwarded to `br0` (mode="bridge")

`red-bridge.xml`:

```xml
<network>
	<name>red_bridge</name>
	<forward mode="bridge"/>
	<bridge name="br0"/>
	<!-- No DHCP/DNS here: the physical network provides them -->
</network>
```

Create and start:

```bash
virsh net-define red-bridge.xml
virsh net-start red_bridge
virsh net-list --all
```

Attach VM to that libvirt network or directly to the host bridge:

```bash
virsh detach-interface debian12 network --mac XX:XX:XX:XX:XX:XX --persistent
virsh attach-interface debian12 network red_bridge --model virtio --persistent

# Or attach directly to the host bridge:
virsh attach-interface debian12 bridge br0 --model virtio --persistent
```

### 2) macvtap network (shares host physical interface, no bridge)

`red-macvtap.xml`:

```xml
<network>
	<name>red_macvtap</name>
	<forward mode="bridge">
		<interface dev="enp1s0"/>
	</forward>
</network>
```

Create and start:

```bash
virsh net-define red-macvtap.xml
virsh net-start red_macvtap
```

Attach VM and note limitations:

```bash
virsh detach-interface debian12 network --mac XX:XX:XX:XX:XX:XX --persistent
virsh attach-interface debian12 network red_macvtap --model virtio --persistent

# Note: macvtap commonly prevents direct host↔VM communication.
```

Example of an expected failure (host unreachable from VM):

```bash
ping 192.168.100.127
# From 192.168.100.250 icmp_seq=1 Destination Host Unreachable
```

---

## Common pitfalls and tips

- Losing network when applying changes: happens when moving IP/gateway to the bridge over SSH. Use local console or schedule a maintenance window.
- Double network managers: avoid NetworkManager and netplan/networkd both managing the same interface.
- STP and switches: STP adds a small delay when ports come up; use `forward-delay 0` only if you understand the implications.
- VLANs: if the physical port is a trunk, configure VLANs on the bridge or tag inside the VMs (virtio VLAN tag support).
- Firewall: check rules when applying strict policies — bridged traffic flows at L2.
- Persistence: ensure your chosen method (Netplan/NM/networkd/interfaces) is applied at boot.

---

## References

- [curso_virtualizacion_linux — GitHub](https://github.com/josedom24/curso_virtualizacion_linux)

- [Netplan](https://netplan.io/examples)
- [Libvirt networking overview](https://libvirt.org/network.html)
- [Debian Wiki: BridgeNetworkConnections](https://wiki.debian.org/BridgeNetworkConnections)
- [iproute2 — ip-link, ip-address, ip-route](https://man7.org/linux/man-pages/man8/ip.8.html)
- [TUN/TAP kernel docs](https://www.kernel.org/doc/Documentation/networking/tuntap.txt)
- [ip-netns (network namespaces)](https://man7.org/linux/man-pages/man8/ip-netns.8.html)
- [veth (ip-link)](https://man7.org/linux/man-pages/man8/ip-link.8.html)
- [Bonding kernel docs](https://www.kernel.org/doc/Documentation/networking/bonding.txt)
- [brctl (bridge-utils) manpage](https://manpages.debian.org/bridge-utils)


