---
title: "How to manage storage volumes with virsh"
date: 2025-10-25T09:00:00+00:00
description: "Operations on volumes inside pools: list, create (vol-create-as), delete (vol-delete), clone, resize (vol-resize), vol-download, vol-upload. Behavior depends on pool type."
tags: [KVM,Virtualization,Libvirt,Storage,Volumes]
hero: images/virtualizacion-kvm-linux/almacenamiento/volumenes.png
weight: 3
---

Short: examples of using the libvirt API (`virsh vol-*`) to manage volumes inside storage pools and notes about backend-specific behavior.

## Managing storage volumes with virsh

In this section we'll look at storage volume management using libvirt's API (the `virsh` tool). We will use pools of type `dir` (image files on disk), although many operations are applicable to other backends; differences are noted where relevant.

### Pools and volumes: quick concept

A "volume" in libvirt is the storage unit created inside a pool. In `dir` and `fs` pools volumes are files (for example `qcow2`, `raw`); in `logical` pools they are LVM logical volumes; in `disk` pools they can map to partitions; and in networked backends (Gluster, RBD, iSCSI) creation and management may require backend-specific tools.

### Check available space in pools (pre-requisite)

Before creating volumes it's a good idea to verify that the pool has free space:

```bash
javiercruces@FJCD-PC:~$ virsh pool-list --details
 Name      State     Autostart   Persistent   Capacity     Allocation   Available
------------------------------------------------------------------------------------
 default   running   yes         yes          914.78 GiB   100.98 GiB   813.80 GiB
 isos      running   yes         yes          914.78 GiB   100.98 GiB   813.80 GiB
 libvirt   running   yes         yes          914.78 GiB   100.98 GiB   813.80 GiB
```

### Get information about pool volumes

To list the volumes in a pool (e.g., `default`):

```bash
javiercruces@FJCD-PC:~$ virsh vol-list default
 Name                                   Path
------------------------------------------------------------------------------------------------------
 debian-13.1.0-amd64-netinst.iso        /var/lib/libvirt/images/debian-13.1.0-amd64-netinst.iso
 debian13-base.qcow2                    /var/lib/libvirt/images/debian13-base.qcow2
 debian13-clonacion-completa.qcow2      /var/lib/libvirt/images/debian13-clonacion-completa.qcow2
 debian13-clonacion-enlazada.qcow2      /var/lib/libvirt/images/debian13-clonacion-enlazada.qcow2
 debian13.qcow2                         /var/lib/libvirt/images/debian13.qcow2
 ubuntu-24.04-vm.qcow2                  /var/lib/libvirt/images/ubuntu-24.04-vm.qcow2
 ...
```

If you need more details (capacity, allocation), use `--details`:

```bash
javiercruces@FJCD-PC:~$ virsh vol-list default --details
 Name                                   Path                                                           Type   Capacity     Allocation
---------------------------------------------------------------------------------------------------------------------------------------
 debian-13.1.0-amd64-netinst.iso        /var/lib/libvirt/images/debian-13.1.0-amd64-netinst.iso        file   783.00 MiB   783.00 MiB
 debian13-base.qcow2                    /var/lib/libvirt/images/debian13-base.qcow2                    file   20.00 GiB    585.61 MiB
 debian13-clonacion-completa.qcow2      /var/lib/libvirt/images/debian13-clonacion-completa.qcow2      file   20.00 GiB    3.04 GiB
 ...
```

To get information about a specific volume:

```bash
javiercruces@FJCD-PC:~$ virsh vol-info debian13.qcow2 default
Name:           debian13.qcow2
Type:           file
Capacity:       20.00 GiB
Allocation:     2.11 GiB
```

The volume's XML definition can be viewed with `vol-dumpxml`:

```bash
javiercruces@FJCD-PC:~$ virsh vol-dumpxml debian13.qcow2 default
<volume type='file'>
  <name>debian13.qcow2</name>
  <key>/var/lib/libvirt/images/debian13.qcow2</key>
  <capacity unit='bytes'>21474836480</capacity>
  <allocation unit='bytes'>2265751552</allocation>
  <target>
    <path>/var/lib/libvirt/images/debian13.qcow2</path>
    <format type='qcow2'/>
    <permissions>
      <mode>0600</mode>
      <owner>0</owner>
      <group>0</group>
    </permissions>
  </target>
</volume>
```

> Note: there is no `virsh vol-define` because volumes are not defined temporarily — they are created with `vol-create-as` or by `vol-create` from XML.

### Create volumes with `vol-create-as`

Example: create a `raw` 10G volume in the `default` pool (name: `vdisk-10G.img`):

```bash
javiercruces@FJCD-PC:~$ virsh vol-create-as default vdisk-10G.img --format raw 10G
```

Check the created file (for `dir` pools the volume is a file in the pool's target directory, typically `/var/lib/libvirt/images` for `default`):

```bash
javiercruces@FJCD-PC:~$ sudo ls -l /var/lib/libvirt/images/
total 10485760
-rw------- 1 root root 10737418240 Oct 26 00:05 vdisk-10G.img
```

If you create a `raw` volume, it will not be thin-provisioned: the file occupies the full size from creation. If you create `qcow2`, capacity is logical and physical allocation grows with use.

Example of `qcow2`:

```bash
javiercruces@FJCD-PC:~$ virsh vol-create-as --pool default --format qcow2 vdisk-20G.qcow2 20G
```

You can verify the difference:

```bash
javiercruces@FJCD-PC:~$ virsh vol-list default --details
 Name                Path                                        Type   Capacity  Allocation
---------------------------------------------------------------------------------------------
 vdisk-10G.img       /var/lib/libvirt/images/vdisk-10G.img       file   10.00 GiB  10.00 GiB
 vdisk-20G.qcow2     /var/lib/libvirt/images/vdisk-20G.qcow2     file   20.00 GiB  196.00 KiB
```

### Delete volumes

```bash
javiercruces@FJCD-PC:~$ virsh vol-delete vdisk-10G.img default
```

This removes the volume from the pool. For networked or LVM backends the exact effect depends on the backend (e.g., deleting an iSCSI LUN, removing an RBD image, etc.).

### Clone volumes

To clone a volume within the same pool:

```bash
javiercruces@FJCD-PC:~$ virsh vol-clone --pool default vdisk-20G.qcow2 vdisk-20G-clone.qcow2
Vol vdisk-20G-clone.qcow2 cloned from vdisk-20G.qcow2
```

If the source is `qcow2` the clone will also benefit from thin provisioning.

### Resize volumes

To increase (or, if the backend allows, decrease) the size of a volume:

```bash
javiercruces@FJCD-PC:~$ virsh vol-resize --pool default vdisk-20G.qcow2 30G
```

If the volume is in use by a running VM, after resizing the volume on the host you often need to resize the partition and filesystem inside the guest. Below are examples for a simple layout where the guest has a single data partition at /dev/vda1 and uses ext4.

1) Increase the volume (host):

```bash
javiercruces@FJCD-PC:~$ virsh vol-resize --pool default vdisk-20G.qcow2 30G
```

2) Resize inside the guest (online)

If the guest has `growpart` (from cloud-guest-utils) you can extend the partition and filesystem while the VM is running:

```bash
# Connect to the guest (e.g. ssh javiercruces@debian13)
javiercruces@debian13:~$ sudo apt update && sudo apt install -y cloud-guest-utils
javiercruces@debian13:~$ sudo growpart /dev/vda 1
javiercruces@debian13:~$ sudo resize2fs /dev/vda1
```

Quick notes:
- `growpart /dev/vda 1` grows the first partition of `/dev/vda` to use the added space.
- `resize2fs /dev/vda1` expands the ext4 filesystem to fill the partition.

3) Alternative using `parted` (online)

```bash
javiercruces@debian13:~$ sudo apt install -y parted
javiercruces@debian13:~$ sudo parted /dev/vda --script resizepart 1 100%
javiercruces@debian13:~$ sudo resize2fs /dev/vda1
```


### Download and upload volume content (vol-download / vol-upload)

Download the content of a volume to a local file:

```bash
javiercruces@FJCD-PC:~$ virsh vol-download --pool default vdisk-20G.qcow2 /tmp/vdisk-20G.qcow2
```

Upload content from a local file to a volume (overwrite):

```bash
javiercruces@FJCD-PC:~$ virsh vol-upload --pool default vdisk-20G.qcow2 /tmp/vdisk-20G.qcow2
```

These operations can be slow for large files; often `qemu-img convert` or backend-specific tools (rbd, gluster) are more efficient.

### Limitations by pool type

- `dir`/`fs` (files): `vol-create-as`, `vol-clone`, `vol-delete`, `vol-resize`, `vol-download` and `vol-upload` work naturally.
- `logical` (LVM): `vol-create-as` can create LVM volumes if libvirt/config allows; alternatively create LVs with `lvcreate` and then define the volume.
- `disk` (partitions): `vol-create-as` may create partitions on a physical device — be careful and backup.
- `iscsi`/`multipath`/`vHBA`: typically managed externally (iSCSI server, multipathd, SAN admin). Not all `virsh vol-*` commands apply.
- `gluster`/`rbd`: sometimes you must use `qemu-img` or backend tools to create/manage images.

### Assign a volume as a disk to a VM (XML example)

You can attach a volume to a VM directly from the host without creating an XML file by using `attach-disk`. Examples:

```bash
javiercruces@FJCD-PC:~$ # Attach live
javiercruces@FJCD-PC:~$ virsh attach-disk testguest1 /var/lib/libvirt/images/vdisk-20G.qcow2 vdb --live

javiercruces@FJCD-PC:~$ # Attach persistently to the VM configuration
javiercruces@FJCD-PC:~$ virsh attach-disk --config testguest1 /var/lib/libvirt/images/vdisk-20G.qcow2 vdb

javiercruces@FJCD-PC:~$ # Attach live and persistent
javiercruces@FJCD-PC:~$ virsh attach-disk --live --config testguest1 /var/lib/libvirt/images/vdisk-20G.qcow2 vdb
```

Notes and explanation:
- `attach-disk` takes the host-side image path (or pool device) and the target device name inside the guest (e.g., `vdb`).
- `--live` makes the change on a running VM; `--config` writes the entry into the VM config so it survives reboots. Combine them when you want both.
- Use this approach when you know the image path and the guest device name; it's the most direct for simple cases.

Alternative: attach using an XML fragment

If you need more control (advanced attributes), create a small XML fragment and use `attach-device`:

```xml
<disk type='volume' device='disk'>
  <driver name='qemu' type='qcow2'/>
  <source pool='default' volume='vdisk-20G.qcow2'/>
  <target dev='vdb' bus='virtio'/>
</disk>
```

Then attach persistently:

```bash
javiercruces@FJCD-PC:~$ virsh attach-device --config testguest1 ~/vdisk-20G.xml
```

The XML varies by pool type; for simple attach operations `attach-disk` is usually easier.

Detach a disk by device name

To remove a disk by its target name (no XML):

```bash
javiercruces@FJCD-PC:~$ virsh detach-disk testguest1 vdb

javiercruces@FJCD-PC:~$ # To also remove the persistent entry:
javiercruces@FJCD-PC:~$ virsh detach-disk --config testguest1 vdb
```

### Best practices and recommendations

- Always check `virsh pool-list --details` before creating volumes to ensure there is available space.
- Take snapshots or backups before resizing or cloning volumes that contain critical data.
- For bulk or automated operations prefer `qemu-img` or native backend tools when the pool does not fully support `vol-create-as`.
- Manage permissions and ownership of files in `dir` pools to avoid startup errors when VMs try to access the files (see `chown`/`chmod` guidance in other posts).

### References

- [curso_virtualizacion_linux — GitHub](https://github.com/josedom24/curso_virtualizacion_linux)
- [Official libvirt documentation: Storage pool and volume XML format](https://libvirt.org/storage.html)
- [virsh manpage / vol-* commands](https://libvirt.org/manpages/virsh.html)