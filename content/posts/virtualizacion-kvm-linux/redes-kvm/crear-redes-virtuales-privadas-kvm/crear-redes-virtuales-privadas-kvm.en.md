---
title: "Create virtual networks in KVM/libvirt (NAT, isolated and very isolated)"
date: 2025-10-18T09:00:00+00:00
description: "Practical guide to create virtual networks in KVM/libvirt: NAT, isolated and very isolated networks. Includes virsh commands, XML examples and verification steps."
tags: [KVM,Virtualization,Libvirt,Networking,Linux]
hero: images/virtualizacion-kvm-linux/redes-kvm/crear-redes-kvm.jpg
---

In this step-by-step guide you'll create three types of virtual networks managed by libvirt and learn simple ways to verify them:

- NAT (Network Address Translation)
- Isolated
- Very isolated (L2 only)

We'll use `virsh` and XML definitions (you can do the same with `virt-manager`, but we'll focus on the CLI). After each creation, there's a quick check to confirm everything looks good.

---

## Before you start: quick requirements

- Packages: `libvirt-daemon` and `libvirt-daemon-system` (or your distro equivalents). Optional: `virt-manager`.
- Run commands as root or with `sudo`.
- Service: `systemctl status libvirtd` should be active.
- See current networks: `virsh net-list --all`
- Persistent config paths: `/etc/libvirt/qemu/networks/`

Tip: avoid subnet conflicts; choose ranges that don't collide with your physical LAN or other libvirt networks.

---

## Step 1: Create a NAT network

A NAT network lets VMs have private IPs and reach the outside through the host.

### 1.1 Create the XML (example)

```xml
<network>
  <name>red_nat_lab</name>
  <forward mode='nat'/>
  <bridge name='virbr101' stp='on' delay='0'/>
  <ip address='192.168.101.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.101.100' end='192.168.101.254'/>
    </dhcp>
  </ip>
</network>
```

- `<forward mode='nat'/>` enables NAT.
- The host will have `192.168.101.1/24` on bridge `virbr101`.
- Libvirt's DHCP will assign IPs in the given range.

### 1.2 Define, start and autostart

```bash
# Save the XML as red_nat_lab.xml and then:
virsh net-define red_nat_lab.xml
virsh net-autostart red_nat_lab
virsh net-start red_nat_lab

# Verification
virsh net-list --all
virsh net-info red_nat_lab
virsh net-dumpxml red_nat_lab
```

### 1.3 Attach a VM to the NAT network

- With `virt-install`:

```bash
virt-install \
  --name vm-nat-example \
  --memory 2048 \
  --vcpus 2 \
  --disk size=10 \
  --os-variant debian12 \
  --network network=red_nat_lab,model=virtio \
  --cdrom /path/to/your.iso \
  --noautoconsole
```

- With `virsh` (existing VM):

```bash
virsh attach-interface --domain EXISTING_VM \
  --type network --source red_nat_lab \
  --model virtio --config --live
```

### 1.4 Verify it works

```bash
# Check the network is active
virsh net-list --all

# See the bridge and its IP
ip addr show virbr101 | grep inet

# Inside a VM attached to red_nat_lab, test connectivity
ping -c 2 1.1.1.1
```

---

## Step 2: Create an isolated network

Private network with no egress to the outside. The host can have an IP on the bridge to talk to VMs and optionally offer DHCP/DNS.

### 2.1 Create the XML (with optional DHCP)

```xml
<network>
  <name>red_aislada_dev</name>
  <bridge name='virbr102' stp='on' delay='0'/>
  <ip address='192.168.102.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.102.100' end='192.168.102.254'/>
    </dhcp>
  </ip>
</network>
```

- No `<forward>`: no NAT or routing to the outside.
- If you prefer everything static, remove the `<dhcp>` block and set IPs manually on each VM.

### 2.2 Define, start and verify

```bash
virsh net-define red_aislada_dev.xml
virsh net-autostart red_aislada_dev
virsh net-start red_aislada_dev

virsh net-list --all
virsh net-info red_aislada_dev
```

Attach VMs the same way as in the NAT case, but pointing to `red_aislada_dev`.

Useful verification:

```bash
# The bridge should exist; if you set IP/DHCP, it will show up
ip addr show virbr102

# Inside two VMs on the isolated network, check they can reach each other (ping by IP)
```

---

## Step 3: Create a very isolated network (L2 only)

Shared L2 segment among VMs, with no host IP on the bridge and no libvirt services (no DHCP/DNS). VMs must be configured with static IPs or run their own internal service.

### 3.1 Create the XML (no IP, no DHCP)

```xml
<network>
  <name>red_muy_aislada</name>
  <bridge name='virbr103' stp='on' delay='0'/>
</network>
```

### 3.2 Define, start and verify

```bash
virsh net-define red_muy_aislada.xml
virsh net-autostart red_muy_aislada
virsh net-start red_muy_aislada

virsh net-list --all
virsh net-dumpxml red_muy_aislada
```

Useful verification:

```bash
# This bridge won't have a host IP (no L3)
ip addr show virbr103 | grep inet || echo "no IP (expected)"

# Inside VMs, assign static IPs in the same subnet and test connectivity between them
```

---

## Management and removal

- List networks: `virsh net-list --all`
- Show XML: `virsh net-dumpxml NAME`
- Stop network: `virsh net-destroy NAME`
- Disable autostart: `virsh net-autostart NAME --disable`
- Remove (must not be active): `virsh net-undefine NAME`

Persistent files live under `/etc/libvirt/qemu/networks/` (and `.../autostart/`).

---

## Common issues and tips

- Subnet conflicts: choose ranges that don't collide with your LAN (e.g., 192.168.101.0/24, 192.168.102.0/24, 192.168.103.0/24).
- Firewall: libvirt manages NAT/iptables/nft by default, but if you have strict rules, review the `libvirt` chains.
- Permissions: add your user to group `libvirt` if you can't use `virsh` without root.
- Persistence: use `net-define` and `net-autostart` so the network survives reboots.

---

## References

- [Libvirt: Virtual networking overview](https://libvirt.org/network.html)
- [Libvirt: Network XML format](https://libvirt.org/formatnetwork.html)
- [Libvirt: Domain XML (interfaces, NIC types)](https://libvirt.org/formatdomain.html)
- [Libvirt Wiki: Guest networking (macvtap, bridge)](https://wiki.libvirt.org/page/Guest_Networking)