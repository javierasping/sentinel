---
title: "How to resize virtual machine disks"
date: 2025-10-25T09:00:00+00:00
description: "How to expand volumes with `virsh vol-resize` or `qemu-img resize` and the necessary steps inside the VM (resize partitions and filesystems). Best practices and risks."
tags: [KVM,Virtualization,Libvirt,Storage,Resize]
hero: images/virtualizacion-kvm-linux/almacenamiento/redimensionar-volumenes.png
weight: 4
---

In this example we'll use the `default` pool and a volume named `vdisk-10G.qcow2`. We'll show how to create the volume from the host, how to format it with common filesystems (ext4, FAT32, XFS, btrfs) from inside the guest, and finally how to add 10 GB to the volume and resize the partition and filesystem.

Note: commands that manage volumes (create, resize) run on the host and use your prompt. Commands executed inside the guest (partitioning and formatting) are shown with the guest prompt `javiercruces@debian13:~$`.

### 1 Create the volume (host)

We'll create the volume in qcow2 format (thin-provisioned). You can use `virsh vol-create-as` or `qemu-img` depending on your preference.

```bash
javiercruces@FJCD-PC:~$ # Create with libvirt in the `default` pool (qcow2, thin)
javiercruces@FJCD-PC:~$ virsh vol-create-as --pool default --format qcow2 vdisk-10G.qcow2 10G

javiercruces@FJCD-PC:~$ # Alternative: create the file directly with qemu-img
javiercruces@FJCD-PC:~$ qemu-img create -f qcow2 /var/lib/libvirt/images/vdisk-10G.qcow2 10G
```

Verify it exists:

```bash
javiercruces@FJCD-PC:~$ virsh vol-list default
 Name            Path
-------------------------------------------------
 vdisk-10G.qcow2 /var/lib/libvirt/images/vdisk-10G.qcow2
```

You can inspect the file with `qemu-img info` to confirm it's qcow2 and check allocation:

```bash
javiercruces@FJCD-PC:~$ qemu-img info /var/lib/libvirt/images/vdisk-10G.qcow2
image: /var/lib/libvirt/images/vdisk-10G.qcow2
file format: qcow2
virtual size: 10G (10737418240 bytes)
disk size: 196K
```

### 2 Attach the volume to a VM for formatting (host)

Attach the volume to a VM (e.g. `testguest1`) as `vdb` live and persistently:

```bash
javiercruces@FJCD-PC:~$ virsh attach-disk --live --config testguest1 /var/lib/libvirt/images/vdisk-10G.qcow2 vdb
```

### 3 Create a single partition and format inside the guest

Connect to the guest (example):

```bash
javiercruces@FJCD-PC:~$ ssh javiercruces@debian13
javiercruces@debian13:~$ sudo -i
```

Use `parted` to create a GPT (or msdos) partition table and a single partition that occupies the whole disk:

```bash
javiercruces@debian13:~$ sudo parted /dev/vdb --script mklabel gpt mkpart primary 0% 100%
```

After creating the partition the kernel typically exposes `/dev/vdb1`. Examples to format the partition with common filesystems:

- ext4

```bash
javiercruces@debian13:~$ sudo mkfs.ext4 -F /dev/vdb1
sudo mkdir -p /mnt/vdb1 && sudo mount /dev/vdb1 /mnt/vdb1
sudo bash -c 'echo "ext4 test" > /mnt/vdb1/README.txt'
```

- FAT32 (vfat)

```bash
javiercruces@debian13:~$ sudo apt update && sudo apt install -y dosfstools
javiercruces@debian13:~$ sudo mkfs.vfat -F 32 /dev/vdb1
sudo mkdir -p /mnt/vdb1 && sudo mount -o uid=1000,gid=1000 /dev/vdb1 /mnt/vdb1
sudo bash -c 'echo "FAT32 test" > /mnt/vdb1/README.txt'
```

- XFS

```bash
javiercruces@debian13:~$ sudo apt update && sudo apt install -y xfsprogs
javiercruces@debian13:~$ sudo mkfs.xfs -f /dev/vdb1
sudo mkdir -p /mnt/vdb1 && sudo mount /dev/vdb1 /mnt/vdb1
sudo bash -c 'echo "XFS test" > /mnt/vdb1/README.txt'
```

- Btrfs

```bash
javiercruces@debian13:~$ sudo apt update && sudo apt install -y btrfs-progs
javiercruces@debian13:~$ sudo mkfs.btrfs -f /dev/vdb1
sudo mkdir -p /mnt/vdb1 && sudo mount /dev/vdb1 /mnt/vdb1
sudo bash -c 'echo "BTRFS test" > /mnt/vdb1/README.txt'
```

Unmount when finished with testing:

```bash
javiercruces@debian13:~$ sudo umount /mnt/vdb1
exit
```

### 4 Extend the volume by 10 GB (host)

On the host increase the volume size to 20G (`virsh vol-resize` uses the absolute size):

```bash
javiercruces@FJCD-PC:~$ virsh vol-resize --pool default vdisk-10G.qcow2 20G
```

If the VM is using the disk live, the following in-guest steps will allow the partition and FS to use the new space.

### 5 Resize partition and filesystem inside the guest

Reconnect to the guest (or reuse an existing session). Use `growpart` when available to expand the partition, then use the filesystem-specific tool to grow the filesystem.

```bash
javiercruces@FJCD-PC:~$ ssh javiercruces@debian13
javiercruces@debian13:~$ sudo apt update && sudo apt install -y cloud-guest-utils
javiercruces@debian13:~$ sudo growpart /dev/vdb 1
```

- ext4 (online)

```bash
javiercruces@debian13:~$ sudo resize2fs /dev/vdb1
```

- XFS (online, must be mounted; grow on the mount point)

```bash
javiercruces@debian13:~$ sudo mount /dev/vdb1 /mnt/vdb1    # if not already mounted
javiercruces@debian13:~$ sudo xfs_growfs /mnt/vdb1
```

- Btrfs (online)

```bash
javiercruces@debian13:~$ sudo mount /dev/vdb1 /mnt/vdb1
javiercruces@debian13:~$ sudo btrfs filesystem resize max /mnt/vdb1
```

- FAT32

FAT32 is less flexible: to resize it online you may need tools like `fatresize` (not always available) or perform the operation offline from the host with `guestfish` or by unmounting and running `fatresize` inside the guest. Example if `fatresize` is available:

```bash
javiercruces@debian13:~$ sudo apt install -y fatresize
javiercruces@debian13:~$ sudo fatresize -s 20G /dev/vdb1
```

If `fatresize` is not available, the alternative is to perform the change offline (unmount and use `guestfish` or boot from a rescue ISO) or recreate the partition and restore data from backup.