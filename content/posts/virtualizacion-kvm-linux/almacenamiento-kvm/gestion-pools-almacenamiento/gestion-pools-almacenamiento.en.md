---
title: "How to manage storage pools"
date: 2025-10-25T09:00:00+00:00
description: "How to create, start, configure (autostart) and destroy pools using virsh and XML files; list and inspect pools; differences between types: dir, disk, logical, iSCSI, ZFS, NFS."
tags: [KVM,Virtualization,Libvirt,Storage,Pools]
hero: images/virtualizacion-kvm-linux/almacenamiento/pools.png
weight: 2
---

This post answers the following questions and provides practical examples:

- What is a storage pool?
- How is a pool created and what forms can it take?

Storage in KVM/libvirt is organized using "storage pools" and "storage volumes". In this article we explain what a pool is, why pools are used, and how to manage them with `virsh` or XML definitions. We include examples, practical recommendations, and notes about LVM-based pools.

## What is a storage pool?

A storage pool is an abstraction that groups a storage source that libvirt can expose to virtual machines. A pool can correspond to a directory on disk, a mounted filesystem, a set of logical volumes (LVM), iSCSI devices, or distributed backends like Ceph RBD or Gluster.

The pool simplifies management: from a VM configuration you reference a volume inside the pool instead of handling physical paths or devices. Pools can be temporary (only in memory, disappear on reboot) or persistent (defined on disk and restored at boot).

## How to list existing pools

To list pools known to libvirt:

```bash
javiercruces@FJCD-PC:~$ virsh pool-list --all
 Name      State    Autostart
-------------------------------
 default   active   yes
 isos      active   yes
 libvirt   active   yes

```

The `default` pool usually points to `/var/lib/libvirt/images` and is created automatically on many distributions.

To view detailed information about a pool:

```bash
javiercruces@FJCD-PC:~$ virsh pool-info default
Name:           default
UUID:           017a5e21-579b-43e7-99a2-e8915524dc80
State:          running
Persistent:     yes
Autostart:      yes
Capacity:       914.78 GiB
Allocation:     100.98 GiB
Available:      813.80 GiB

```

And to see its XML definition:

```bash
javiercruces@FJCD-PC:~$ virsh pool-dumpxml default
<pool type='dir'>
	<name>default</name>
	<uuid>017a5e21-579b-43e7-99a2-e8915524dc80</uuid>
	<capacity unit='bytes'>982240026624</capacity>
	<allocation unit='bytes'>108423954432</allocation>
	<available unit='bytes'>873816072192</available>
	<source>
	</source>
	<target>
		<path>/var/lib/libvirt/images</path>
		<permissions>
			<mode>0711</mode>
			<owner>0</owner>
			<group>0</group>
		</permissions>
	</target>
</pool>
```

## Creating a pool: temporary vs persistent

There are two main ways to create pools:

- Create a temporary pool: `virsh pool-create` or `virsh pool-create-as`. This pool will exist until the libvirt service or the host is restarted.
- Create a persistent pool: `virsh pool-define` or `virsh pool-define-as` creates the definition under `/etc/libvirt/storage/` and lets you start it and configure autostart.

### Create a persistent pool (practical example)

Assume you mounted a disk at `/srv/images` and want to create a pool named `vm-images` of type `dir`:

```bash
javiercruces@FJCD-PC:~$ virsh pool-define-as vm-images dir --target /srv/images
javiercruces@FJCD-PC:~$ virsh pool-build vm-images
javiercruces@FJCD-PC:~$ virsh pool-start vm-images
javiercruces@FJCD-PC:~$ virsh pool-autostart vm-images
```

Useful checks:

```bash
javiercruces@FJCD-PC:~$ virsh pool-list --all
javiercruces@FJCD-PC:~$ virsh pool-info vm-images
```

If you want to create the pool from an XML file (common for iSCSI or more complex configs), write the XML and use:

```bash
javiercruces@FJCD-PC:~$ virsh pool-define /path/to/pool-definition.xml
javiercruces@FJCD-PC:~$ virsh pool-start pool_name
```

Minimal XML example for a `dir` pool:

```xml
<pool type="dir">
	<name>isos</name>
	<target>
		<path>/var/lib/libvirt/isos</path>
	</target>
</pool>
```

After `virsh pool-define`, libvirt stores the persistent pool definition as an XML file under `/etc/libvirt/storage/`. Each XML in that directory represents a pool definition that libvirt can start and control with `virsh`.

Entries that should start automatically are represented under `/etc/libvirt/storage/autostart/`. That directory normally contains symlinks pointing to the original XML files; their presence indicates the pool will be started when libvirt or the system boots.

```bash
javiercruces@FJCD-PC:~$ ls -l /etc/libvirt/storage/
total 16
drwxr-xr-x 2 root root 4096 Oct 18 16:13 autostart
-rw------- 1 root root  538 Oct 13 20:03 default.xml
-rw------- 1 root root  532 Oct 13 20:41 isos.xml
-rw------- 1 root root  531 Oct 18 16:13 libvirt.xml

javiercruces@FJCD-PC:~$ ls -l /etc/libvirt/storage/autostart/
total 0
lrwxrwxrwx 1 root root 32 Oct 13 20:03 default.xml -> /etc/libvirt/storage/default.xml
lrwxrwxrwx 1 root root 29 Oct 13 20:41 isos.xml -> /etc/libvirt/storage/isos.xml
lrwxrwxrwx 1 root root 32 Oct 18 16:13 libvirt.xml -> /etc/libvirt/storage/libvirt.xml
```

Note: you can control whether a pool is started automatically with `virsh pool-autostart` (see `virsh help pool-autostart` for exact options). If you remove the XML from `/etc/libvirt/storage/` or remove the symlink in `autostart/`, libvirt will no longer know or start that pool persistently.

## Refresh and list volumes

If you add files manually into a pool directory (for example downloading an ISO), libvirt may not detect them immediately. Use:

```bash
javiercruces@FJCD-PC:~$ virsh pool-refresh isos
javiercruces@FJCD-PC:~$ virsh vol-list --pool isos
```

## Deleting and destroying pools

To remove a pool:

1. Stop the pool (this does not delete it, only stops it):

```bash
javiercruces@FJCD-PC:~$ virsh pool-destroy vm-images
```

2. (Optional) Remove the directory if you no longer need it:

```bash
javiercruces@FJCD-PC:~$ rm -rf /srv/images
```

3. Remove the persistent definition:

```bash
javiercruces@FJCD-PC:~$ virsh pool-undefine vm-images
```

If you prefer to delete the directory via `virsh` (pool-delete), note the directory must be empty:

```bash
javiercruces@FJCD-PC:~$ virsh pool-delete vm-images
```

## LVM-based pools: considerations and steps

LVM-based pools let you use logical volumes as disks for VMs. Before creating one, be aware that the procedure may format partitions if you create a new PV/VG.

Basic concept steps:

- Check whether libvirt supports the `logical` pool type:

```bash
javiercruces@FJCD-PC:~$ virsh pool-capabilities | grep "'logical' supported='yes'"
```

- Define a logical pool that uses a block device:

```bash
javiercruces@FJCD-PC:~$ virsh pool-define-as guest_images_logical logical --source-dev=/dev/sdc --source-name libvirt_lvm --target /dev/libvirt_lvm
javiercruces@FJCD-PC:~$ virsh pool-start guest_images_logical
javiercruces@FJCD-PC:~$ virsh pool-autostart guest_images_logical
```

Recommendations:

- Back up before manipulating partitions or physical devices.
- If you use an existing VG, it should not destroy data; creating a new VG based on a partition will format it.
- Check `virsh pool-info <pool>` to verify capacity, allocation and state.

## Best practices and recommendations

- Use clear pool names (e.g. `images`, `vms`, `isos`, `backups`) and separate purposes.
- Prefer persistent pools for production and enable `autostart` when appropriate.
- Monitor `Capacity`, `Allocation` and `Available` to avoid overcommit in thin-provisioned setups.
- Avoid manually modifying pool paths without using `virsh pool-build`/`pool-refresh`, because libvirt can lose synchronization with contents.
- For environments with frequent migrations, choose tested shared backends (Ceph RBD, well-configured NFS, Gluster) to ease live migration.

## Summary

Storage pools are how libvirt abstracts different storage sources. With `virsh` you can list, create (temporary or persistent), start, enable autostart, refresh, destroy and delete pools. For complex configurations (iSCSI, LVM, Ceph) it's common to use XML definitions loaded with `virsh pool-define`.

The next article will cover how to create and manage volumes inside a pool and how to assign them to VMs.

## Sources

- [Official libvirt documentation: Storage management; Storage pool and volume XML format](https://libvirt.org/storage.html)
