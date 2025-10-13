---
title: "Components of a virtual machine in KVM"
date: 2025-10-13T10:00:00+00:00
description: Learn about the fundamental components of a virtual machine in KVM and how to retrieve detailed information from the hypervisor using virsh.
tags: [Virtualization,Linux,KVM,VM,Hypervisor,Ubuntu,Debian]
hero: images/virtualizacion-kvm-linux/introduccion-kvm/componentes-vm.jpg
---

# Components of a virtual machine in KVM

In **KVM (Kernel-based Virtual Machine)**, a virtual machine is composed of several elements that interact to emulate a complete hardware environment. Understanding each component helps you manage, troubleshoot, and optimize your VMs more efficiently.

## 1. Main components

| Component | Description |
|-------------|--------------|
| **Virtual CPU (vCPU)** | Cores assigned from the physical host to the guest. Defined with `--vcpus` when creating the VM. |
| **Memory (RAM)** | Amount of memory assigned. Configured with `--ram` or can be hot-adjusted with `virsh setmem`. |
| **Virtual disk** | Storage file (`.qcow2`, `.raw`, etc.) used as the guest disk. Managed with `virsh vol-*` or `virt-manager`. |
| **Network interface** | Virtual connection (usually `virtio` or `e1000`) attached to a libvirt network (`default`, `br0`, etc.). |
| **Graphics device / console** | VNC, SPICE, or text mode (no graphical console). Controllable with `--graphics` or `virsh vncdisplay`. |
| **Firmware / BIOS / UEFI** | Defines the boot mode (traditional BIOS or UEFI with OVMF). |
| **Additional devices** | CD-ROM, USB controllers, serial channels, sound interfaces, etc. |

## 2. Essential commands to retrieve VM information

Once the VM is created, you can use `virsh` to inspect and manage all its details.

### List virtual machines

```bash
javiercruces@FJCD-PC:~
$ virsh list --all
 Id   Name              State
----------------------------------
 9    debian13          running
 -    ubuntu-24.04-vm   shut off
```

Shows all VMs, both active and inactive.

### View general information about a VM

```bash
javiercruces@FJCD-PC:~
$ virsh dominfo debian13
Id:             9
Name:           debian13
UUID:           196c28a6-4821-43c8-b862-1feea5995683
OS Type:        hvm
State:          running
CPU(s):         2
CPU time:       20,4s
Max memory:     2097152 KiB
Used memory:    2097152 KiB
Persistent:     yes
Autostart:      disable
Managed save:   no
Security model: apparmor
Security DOI:   0
Security label: libvirt-196c28a6-4821-43c8-b862-1feea5995683 (enforcing)
```

### View the VM's full XML configuration

```bash
virsh dumpxml name_vm
```

This command shows the entire internal definition of the VM: disks, networking, CPU, firmware, etc. Ideal for backing up a configuration or replicating a machine.

Save the definition:
```bash
virsh dumpxml name_vm > name_vm.xml
```

### Information about the VM's disks

```bash
$ virsh domblklist debian13
 Target   Source
--------------------------------------------------
 vda      /var/lib/libvirt/images/debian13.qcow2
 sda      -
```

To get details about a disk:
```bash
javiercruces@FJCD-PC:~
$ virsh domblkinfo debian13 vda --human
Capacity:       20,000 GiB
Allocation:     2,110 GiB
Physical:       20,003 GiB
```

### View network interfaces and IP addresses

```bash
javiercruces@FJCD-PC:~
$ virsh domiflist debian13
 Interface   Type      Source    Model    MAC
-------------------------------------------------------------
 vnet8       network   default   virtio   52:54:00:8d:ef:f0
```

To see the IP assigned by DHCP:
```bash
$ virsh domifaddr debian13
 Name       MAC address          Protocol     Address
-------------------------------------------------------------------------------
 vnet8      52:54:00:8d:ef:f0    ipv4         192.168.122.8/24
 -          -                    ipv4         192.168.122.9/24
```

### Real-time statistics

CPU and memory:
```bash
javiercruces@FJCD-PC:~ [p-ie-omni|]
$ virsh domstats debian13
Domain: 'debian13'
  state.state=1
  state.reason=1
  cpu.time=22002276000
  cpu.user=17092323000
  cpu.system=4909952000
  cpu.cache.monitor.count=0
  cpu.haltpoll.success.time=39199780
  cpu.haltpoll.fail.time=77700049
  balloon.current=2097152
  balloon.maximum=2097152
```

Network traffic and disk usage:
```bash
$ virsh domstats --interface --block  debian13
Domain: 'debian13'
  net.count=1
  net.0.name=vnet8
  net.0.rx.bytes=95541
  net.0.rx.pkts=970
  net.0.rx.errs=0
  net.0.rx.drop=0
  net.0.tx.bytes=2792
  net.0.tx.pkts=35
  net.0.tx.errs=0
  net.0.tx.drop=0
  block.count=2
  block.0.name=vda
  block.0.path=/var/lib/libvirt/images/debian13.qcow2
  block.0.backingIndex=2
  block.0.rd.reqs=4303
  block.0.rd.bytes=126719488
  block.0.rd.times=56885760
  block.0.wr.reqs=550
  block.0.wr.bytes=10887680
  block.0.wr.times=53350513
  block.0.fl.reqs=124
  block.0.fl.times=59918268
  block.0.allocation=3265593344
  block.0.capacity=21474836480
  block.0.physical=2265624576
  block.1.name=sda
  block.1.rd.reqs=19
  block.1.rd.bytes=352
  block.1.rd.times=33044
  block.1.wr.reqs=0
  block.1.wr.bytes=0
  block.1.wr.times=0
  block.1.fl.reqs=0
  block.1.fl.times=0
```

### View the VM console or display

Text console (serial):
```bash
virsh console name_vm
```

VNC (if enabled):
```bash
virsh vncdisplay name_vm
```

### Query host and hypervisor capabilities

Node (host) information:
```bash
virsh nodeinfo
```

Capabilities information:
```bash
virsh capabilities
```

VM-specific capabilities:
```bash
virsh domcapabilities
```

### Get storage information

List pools:
```bash
virsh pool-list
```

View details of a pool:
```bash
virsh pool-info default
```

List volumes in the pool:
```bash
virsh vol-list default
```

### Diagnostics and debugging

View events in real time:
```bash
virsh event --domain name_vm
```

Get detailed logs:
```bash
journalctl -u libvirtd -f
```

## 3. Other useful commands

| Command | Description |
|----------|-------------|
| `virsh domstate name_vm` | Current state of the VM (`running`, `paused`, `shut off`, etc.) |
| `virsh start name_vm` / `virsh shutdown name_vm` | Start or shut down the VM |
| `virsh suspend name_vm` / `virsh resume name_vm` | Suspend and resume |
| `virsh autostart name_vm` | Enable autostart when the host boots |
| `virsh snapshot-list name_vm` | List existing snapshots |
| `virsh domrename old new` | Rename a VM |