---
title: "Network types in KVM (libvirt)"
date: 2025-10-18T09:00:00+00:00
description: "Theoretical overview of the network types available in KVM/libvirt: NAT, isolated, very isolated, external bridge and macvtap; differences, connectivity and use cases."
tags: [KVM,Virtualization,Libvirt,Networking,Linux]
hero: images/virtualizacion-kvm-linux/redes-kvm/tipos-redes-kvm.jpg
---

# Network types in KVM

In KVM, network virtualization is mainly managed through **libvirt**, which lets us create and administer various kinds of virtual networks to which our virtual machines connect. Understanding the available network types is key to properly configuring guest connectivity and the host interaction.

There are two broad categories of networks in KVM:

- **Private virtual networks**: Internal networks isolated from the outside, managed via virtual bridges created by libvirt.
- **Bridged networks**: Networks that connect virtual machines directly to the host's physical network.

---

## Private virtual networks

These networks are created on the host and provide a controlled environment for virtual machines. They fall into three main types:

### 1. NAT (Network Address Translation)

This is the most common private network and is typically used by libvirt's `default` network. Characteristics:

- Virtual machines have private addresses and access the outside through the host using **NAT**.
- A **virtual bridge** is created (by default often `virbr0`) to which VMs and the host connect.
- The host acts as a **router and DHCP server** to assign dynamic addresses.
- The host can also provide **DNS service** to the guests.

Use cases: labs, development and test environments where VMs need Internet access without being directly reachable from the physical network.

### 2. Isolated networks

Private networks where virtual machines have no access to the outside:

- They connect to a virtual bridge, but there is no **NAT** or routing to the outside.
- The host can (optionally) have an IP on that bridge to communicate with the VMs and, if desired, offer internal **DHCP/DNS**.

Use cases: internal service segmentation, test environments with full control over addressing and no egress to the outside.

### 3. Very isolated networks

In this case, virtual machines are completely separated from the host:

- There are no L3 services from the host (no host IP on the bridge) and no **DHCP/DNS** provided by libvirt.
- Network configuration is typically done statically on each VM or via an internal service deployed by the user.

Notes: even if the host has no IP on the bridge (no L3 connectivity), VMs still share the same L2 segment among themselves.

---

## Bridged networks

These networks allow virtual machines to connect directly to the host's physical network. There are two ways to implement them:

### 1. External bridge

A **virtual bridge** is created (for example, `br0`) to which the host's physical interface and the virtual machines attach:

- VMs become part of the same network as the host.
- They can obtain IP addresses from the physical network's **DHCP** (e.g., your router).
- Ideal when VMs must be accessible from other devices on the network.

### 2. Macvtap

Allows VMs to connect directly to the host's physical interface without a bridge:

- VMs receive IP addresses from the physical network.
- There is no direct host↔VM communication by default (a known limitation of macvtap in most modes).
- Useful when direct access to the physical network is needed without additional bridge configuration.

Note: in certain advanced scenarios, host↔VM communication can be enabled by creating an auxiliary interface (macvlan) on the host; however, this is not the default behavior.

---

## Summary table

| Network type    | Host connectivity        | External connectivity     | DHCP available                 |
|-----------------|--------------------------|---------------------------|--------------------------------|
| NAT             | Yes                      | Yes (via host NAT)        | Yes                            |
| Isolated        | Yes (if host has IP)     | No                        | Optional                       |
| Very isolated   | No (no host IP)          | No                        | No                             |
| External bridge | Yes                      | Yes (direct)              | Yes (physical network DHCP)    |
| Macvtap         | Not directly (limited)   | Yes (direct)              | Yes (physical network DHCP)    |

---

## References

- [Libvirt: Virtual networking overview](https://libvirt.org/network.html)
- [Libvirt: Network XML format](https://libvirt.org/formatnetwork.html)
- [Libvirt: Domain XML (interfaces, NIC types)](https://libvirt.org/formatdomain.html)
- [Libvirt Wiki: Guest networking (macvtap, bridge)](https://wiki.libvirt.org/page/Guest_Networking)
