---
title: "How to validate the KVM host installation"
date: 2025-10-13T10:00:00+00:00
description: Learn how to validate that your Ubuntu/Debian host meets the requirements to run KVM and manage virtual machines efficiently.
tags: [Virtualization,Linux,KVM,VM,Hypervisor,Ubuntu,Debian]
hero: images/virtualizacion-kvm-linux/instalacion/validacion.png
weight: 2
---

Before creating and running virtual machines with **KVM**, it's essential to validate that the host meets the required **hardware and software** capabilities to ensure optimal performance. This guide describes how to verify system capabilities using tools such as `virt-host-validate` and `virsh`.

## 1. Validating CPU virtualization support

KVM requires processors with **hardware virtualization extensions**:

- Intel: VT-x
- AMD: AMD-V

To check if your CPU is compatible, run:

```bash
grep --color -Ew 'svm|vmx|lm' /proc/cpuinfo
```

* `vmx` → Intel CPU with VT-x
* `svm` → AMD CPU with AMD-V
* `lm` → 64-bit support

If your CPU lacks these extensions, only CPU emulation will be available and performance will be significantly reduced.

## 2. Checking kernel modules

The kernel modules required for virtualization should be loaded:

```bash
lsmod | grep kvm
```

* Intel systems: `kvm_intel`
* AMD systems: `kvm_amd`

If they are not present, load them manually:

```bash
sudo modprobe kvm
sudo modprobe kvm_intel  # For Intel
sudo modprobe kvm_amd    # For AMD
```

## 3. Validating the host with virt-host-validate

The `virt-host-validate` tool runs a set of checks to ensure the system is ready for KVM:

```bash
sudo virt-host-validate
```

A successful result will show `PASS` for all tests, including:

- Hardware virtualization
- Presence of devices `/dev/kvm`, `/dev/vhost-net` and `/dev/net/tun`
- Support for CPU and memory controllers

If a test fails it will be marked `FAIL`, which can affect VM performance.

### Example of a successful output

```
QEMU: Checking for hardware virtualization              : PASS
QEMU: Checking if device /dev/vhost-net exists          : PASS
QEMU: Checking if device /dev/net/tun exists            : PASS
QEMU: Checking for cgroup 'memory' controller support   : PASS
QEMU: Checking for cgroup 'cpu' controller support      : PASS
```

### Example of a failure due to CPU without VT-x/AMD-V

```
QEMU: Checking for hardware virtualization              : FAIL (Only emulated CPUs are available, performance will be significantly limited)
```

## 4. Validating host information with virsh

`virsh` allows querying host details and hypervisor capabilities:

```bash
virsh nodeinfo
```

Sample output:

```yaml
CPU model:           x86_64
CPU(s):              24
CPU frequency:       4252 MHz
CPU socket(s):       1
Core(s) per socket:  12
Thread(s) per core:  2
NUMA cell(s):        1
Memory size:         62324512 KiB
```

To see maximum capabilities for guests:

```bash
virsh domcapabilities | grep -i max
```

Example snippet:

```xml
  <vcpu max='255'/>
    <mode name='maximum' supported='yes'>
      <enum name='maximumMigratable'>
      <maxphysaddr mode='passthrough' limit='48'/>
```

You can also list the types of devices supported by the hypervisor:

```bash
virsh domcapabilities | grep diskDevice -A 5
```

```xml
      <enum name='diskDevice'>
        <value>disk</value>
        <value>cdrom</value>
        <value>floppy</value>
        <value>lun</value>
      </enum>
```

`virsh` is the command-line tool to manage virtual machines and the hypervisor. It allows administering VMs, monitoring resources, managing storage, snapshots and virtual networks.

## References

- [curso_virtualizacion_linux — GitHub](https://github.com/josedom24/curso_virtualizacion_linux)
- [KVM-virsh - Ubuntu Help](https://help.ubuntu.com/community/KVM/Virsh)
- [Managing guests using virsh - RedHat Virtualization Guide](https://access.redhat.com/documentation/en-us/red_hat_virtualization)
- [virsh - libvirt guide](https://libvirt.org/virshcmdref.html)

***

