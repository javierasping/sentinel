---
title: "How to expand VM memory, CPU and disks"
date: 2025-10-16T13:00:00+00:00
description: How to increase vCPU, RAM, and disk space of a VM in KVM, including expanding the filesystem inside the guest.
tags: [KVM,Virtualization,Libvirt,Linux,VM,Resources]
hero: images/virtualizacion-kvm-linux/gestion-vm/ampliar-recursos.png
weight: 5
---

# Expand virtual machine resources in KVM

In this article we'll cover three practical cases for expanding resources in a VM managed with libvirt/KVM:

- Increase the number of vCPUs (cores)
- Increase RAM memory
- Expand disk and filesystem inside the guest

We'll use `virsh` commands, libguestfs tools where applicable, and standard utilities inside the guest (growpart, resize2fs, xfs_growfs, LVM). I'll include "hot" methods when the system supports them and safe cold alternatives.

> Note: To run without sudo, your user must belong to the `libvirt` and `kvm` groups.

Example of initial situation:

```bash
virsh list --all
```

Example output:
```
 Id   Name       State
-----------------------------
 -    debian13   shut off
```

---

## 1 Increase vCPU (cores)

There are two limits: the maximum vCPU defined in the VM and the currently assigned number. You can increase vCPU hot if the guest supports it (CPU hotplug), or cold by adjusting the persistent configuration.

### View current and maximum vCPU

```bash
virsh vcpucount debian13 --live --maximum
virsh vcpucount debian13 --live
virsh vcpucount debian13 --config --maximum
virsh vcpucount debian13 --config
```

### Increase vCPU hot (if possible)

```bash
# Increase to 4 vCPU on the running VM and persist the change
virsh setvcpus debian13 4 --live
virsh setvcpus debian13 4 --config
```

If an error appears, the guest or the definition may not allow hotplug. Make sure the maximum allows it:

```bash
# Increase maximum allowed to 8 vCPU (persistent), with VM powered off
virsh setvcpus debian13 8 --maximum --config
```

Then adjust the current value and start:

```bash
virsh setvcpus debian13 4 --config
virsh start debian13
```

### Verification inside the guest

```bash
nproc
lscpu | grep -i '^CPU(s)\|Model name\|Thread\|Core\|Socket'
```

---

## 2 Increase RAM memory

Memory also has a maximum (maxmem) and a current value. Memory hotplug depends on the guest (balloon/virtio-mem). If it fails hot, apply cold.

### Check memory

```bash
virsh dominfo debian13 | grep -i memory
virsh dommemstat debian13
```

### Increase memory hot (if supported)

```bash
# Set maximum to 8 GiB and increase current memory to 6 GiB
virsh setmaxmem debian13 8G --config
virsh setmem    debian13 6G --live
virsh setmem    debian13 6G --config
```

If it errors on `--live`, make the change with the VM powered off:

```bash
virsh shutdown debian13
virsh setmaxmem debian13 8G --config
virsh setmem    debian13 6G --config
virsh start debian13
```

### Verification inside the guest

```bash
free -h
cat /proc/meminfo | grep MemTotal
```

---

## 3 Expand disk and filesystem

The general flow is:

1. Expand the virtual disk on the host (qcow2/raw or pool volume)
2. Inside the guest, detect the new size and expand partition/LVM as appropriate
3. Resize the filesystem (ext4/xfs)

> Recommendation: Make a snapshot/backup before modifying partitions or LVM.

### 3.1 Expand the disk on the host

First identify the VM's disk path:

```bash
virsh domblklist debian13
```

- If using a libvirt pool volume:

```bash
virsh vol-list default
virsh vol-resize --pool default debian13.qcow2 +10G
```

- If using a direct qcow2/raw file:

```bash
qemu-img resize /var/lib/libvirt/images/debian13.qcow2 +10G
```

> Note: Avoid resizing a disk with chained snapshots without checking dependencies.

Restart the VM (if it was running) so the guest detects the new disk size if it doesn't support size hotplug:

```bash
virsh shutdown debian13 && virsh start debian13
```

### 3.2 Case A: Single partition (no LVM)

Assuming a `vda` disk with a `vda1` partition using ext4 or xfs.

1) Expand the partition inside the guest:

```bash
sudo apt install -y cloud-guest-utils  # for growpart (Debian/Ubuntu)
sudo growpart /dev/vda 1               # expands partition 1 to occupy the new size
lsblk
```

2) Resize the filesystem:

- ext4:

```bash
sudo resize2fs /dev/vda1
```

- xfs (specify the mount point):

```bash
sudo xfs_growfs /
```

Verify:

```bash
df -h
```

### 3.3 Case B: LVM (PV + VG + LV)

Assuming the PV is on `/dev/vda2`, the VG is `vg0` and the LV is `lvroot` mounted at `/`.

1) Detect the new size on the PV:

```bash
sudo pvscan
sudo pvdisplay
sudo pvresize /dev/vda2
```

2) Expand the LV and the FS at once (ext4/xfs):

```bash
sudo lvdisplay
sudo lvextend -r -l +100%FREE /dev/vg0/lvroot
```

`-r` attempts to automatically resize the filesystem. Manual alternative:

```bash
sudo lvextend -l +100%FREE /dev/vg0/lvroot
# ext4
sudo resize2fs /dev/vg0/lvroot
# xfs (specify mount point)
sudo xfs_growfs /
```

Verify:

```bash
lsblk
df -h
```

---

## Tips and troubleshooting

- CPU/Memory hotplug: depends on the guest (kernel, drivers, ACPI, virtio). If it fails on `--live`, make the change with `--config` and restart.
- Maximum limit: if `setvcpus`/`setmem` fail due to limit, first adjust the maximum with `--maximum` (CPU) or `setmaxmem` (memory).
- growpart not available: use `parted` or `fdisk` carefully; make sure to align correctly and not overwrite data.
- xfs doesn't shrink: it only grows. To shrink xfs you have to recreate; plan accordingly.

---

## References

- [curso_virtualizacion_linux — GitHub](https://github.com/josedom24/curso_virtualizacion_linux)
- [virsh - Official libvirt documentation](https://libvirt.org/manpages/virsh.html) - Commands: setvcpus, setmem, setmaxmem, dominfo, vcpucount, dommemstat
- [qemu-img - QEMU Documentation](https://www.qemu.org/docs/master/tools/qemu-img.html) - Resize command to resize disk images
- [cloud-guest-utils - Launchpad](https://launchpad.net/cloud-utils) - Includes growpart to expand partitions
- [resize2fs - e2fsprogs](https://man7.org/linux/man-pages/man8/resize2fs.8.html) - Resize ext2/ext3/ext4 filesystems
- [xfs_growfs - XFS Documentation](https://man7.org/linux/man-pages/man8/xfs_growfs.8.html) - Expand XFS filesystems
- [LVM Administration Guide - Red Hat](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_and_managing_logical_volumes/) - pvresize, lvextend and logical volume management
