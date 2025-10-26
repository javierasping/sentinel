---
title: "Introduction to storage in KVM/libvirt"
date: 2025-10-25T09:00:00+00:00
description: "Fundamental concepts: storage pools, volumes, image formats (raw, qcow2), snapshots and backend types (dir, disk, LVM, iSCSI, ZFS, etc.)."
tags: [KVM,Virtualization,Libvirt,Storage]
hero: images/virtualizacion-kvm-linux/almacenamiento/introduccion-almacenamiento.png
weight: 1
---

Storage is a foundational part of virtualization: it determines how and where virtual machine disks are stored, how snapshots are handled, and what performance and protection options are available.

In the KVM/libvirt ecosystem storage is organized around two basic concepts:

- Storage pools: logical groupings that represent a storage source (for example, a directory, an LVM volume group, an iSCSI target or a Ceph pool). Libvirt exposes and manages these pools to simplify storage usage for VMs.
- Storage volumes: the units inside a pool that act as virtual disks for guests.

## Types of pools

Libvirt supports several pool types. A practical summary:

- File-based: `dir`, `fs`, `netfs` — simple to set up and suitable for small deployments and testing.
- Block-based: `disk`, `logical` (LVM), `zfs` — provide finer control and better I/O characteristics for demanding workloads.
- Network / distributed: `iscsi`, `rbd` (Ceph), `gluster` — provide shared, replicated or distributed storage for multi-host environments.

Each type has trade-offs; choose according to performance, resilience and operational constraints.

### File-based pools

File-based pools store virtual disks as files on a filesystem, local or remote. They are easy to manage and commonly used for labs, development and small deployments.

Common file formats seen in these pools include:

- `raw`: a plain binary image representing the disk contents. It typically occupies its full size on creation and has minimal I/O overhead.
- `qcow2`: QEMU's copy-on-write format. Supports thin provisioning, snapshots and backing files; files grow as data is written.
- `vdi`, `vmdk`, `vhd/vhdx`: vendor-specific formats (VirtualBox, VMware, Hyper-V) sometimes encountered in heterogeneous environments; conversions are often used when migrating between hypervisors.

File-based pools can be mounted (fs) or exposed over the network (netfs) using NFS/CIFS when sharing images between hosts.

### Block-based pools

Block-based pools operate on block devices or logical volumes and suit workloads where I/O performance and predictability matter.

- `disk`: exposes a physical block device or partitions directly to libvirt-managed VMs.
- `logical`: uses LVM (Logical Volume Manager) to create logical volumes as VM disks; offers flexibility for resizing and snapshots at the block level.
- `zfs`: uses ZFS datasets and zvols, providing features such as snapshots, clones, compression and integrity checks.

### Network and distributed pools

Network/distributed backends provide shared storage accessible by multiple hosts, which is useful for migrations and high-availability setups.

- `iscsi` / `iscsi-direct`: expose iSCSI LUNs as block devices; `iscsi-direct` provides more direct device access in some configurations.
- `rbd` (Ceph): RADOS Block Device backed by a Ceph cluster; offers replication and automatic recovery.
- `gluster`: GlusterFS as a distributed filesystem for shared VM images.

## Other storage features

### Snapshots

Snapshots capture the state of a disk or volume at a point in time. They can be:

- Image-level (formats like `qcow2`).
- Volume/device-level (LVM, ZFS, or other backends offering atomic snapshots).

Use cases include testing, quick rollbacks during updates, and rapid cloning. Snapshots add complexity, can impact performance (especially with multiple COW layers), and need lifecycle management (consolidation and cleanup).

### Thin provisioning

Thin provisioning presents virtual disks larger than the physical storage available, consuming space only when data is written. It improves storage utilization but requires active monitoring to avoid out-of-space situations. Preallocation reserves the full size at creation and is more predictable for performance and capacity planning.

### Backing files and clones

Formats that support backing files (for example `qcow2`) let you create immutable base images and multiple lightweight derived images. This speeds deployments but complicates backups and restores when the backing chains are deep; consolidating or flattening images is often advisable before critical operations.

## Operational and security considerations

- Permissions and SELinux/AppArmor: ensure images and directories have correct permissions and security labels so libvirt can access them without weakening system security.
- Credentials and secrets: backends like iSCSI or Ceph require credential management (CHAP, cephx). Rotate and store secrets securely.
- Locking and concurrent access: do not assume a simple file on NFS is safe for concurrent writes by multiple hypervisors; use shared storage designed for concurrent access or proper locking.

## Typical operations (conceptual)

- Defining pools: can be transient (session-only) or persistent (stored in libvirt); persistent pools are recommended for production.
- Creating volumes: specify capacity, initial allocation and format when applicable.
- Cloning, resizing and migrating: common lifecycle operations that require planning (backups, consistent snapshots, maintenance windows where appropriate).

## Best practices (summary)

- Separate pools by purpose (system images, persistent data, backups) and avoid mixing different roles in a single critical pool.
- For production workloads, prefer block backends or proven distributed solutions (Ceph RBD, ZFS) and avoid overcommitting without monitoring.
- Avoid deep backing-file chains in production; consolidate images prior to backups or migrations.
- Test restores regularly; an unverified backup is not a reliable recovery plan.

## Further reading and references


- [Libvirt — Storage management; Storage pool and volume XML format](https://libvirt.org/storage.html)
- [Libvirt — Storage pool and volume XML format (format details)](https://libvirt.org/formatstorage.html)
- [QEMU — Disk images, formats and qemu-img](https://qemu.org/docs/master/system/images.html)
- [Ceph — RBD (using with libvirt)](https://docs.ceph.com/en/latest/rbd/)
- [LVM — documentation and best practices](https://man7.org/linux/man-pages/man8/lvm.8.html)
- [open-iscsi — iSCSI on Linux](https://linux-iscsi.org/wiki/Main_Page)
- [Cockpit — web console for managing machines and storage](https://cockpit-project.org/)
- [NFS — general guide and considerations](https://nfs.sourceforge.net/)