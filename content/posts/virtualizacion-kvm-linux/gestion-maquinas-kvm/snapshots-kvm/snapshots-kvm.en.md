---
title: "How to create and manage snapshots in KVM"
date: 2025-10-17T10:00:00+00:00
description: Practical, detailed guide to create, list, revert, and delete virtual machine snapshots in KVM/libvirt, including internal/external snapshots, with memory and disk, quiesce with qemu-guest-agent, and cleanup with blockcommit.
tags: [KVM,Virtualization,Libvirt,Linux,VM,Snapshots]
hero: images/virtualizacion-kvm-linux/gestion-vm/snapshots.png
---

# Snapshots in KVM/libvirt: how to create and manage them

Snapshots let you capture a VM's state at a specific moment so you can roll back if something goes wrong (updates, risky changes, tests). In KVM with libvirt there are two main families:

- Internal snapshots: the snapshot content is stored inside the qcow2 file itself. They usually require the VM to be powered off and only work with qcow2 storage (not raw, LVM, etc.).
- External snapshots: they create separate overlay files (qcow2); these are the most used for hot snapshots (running VM). They allow more flexible flows and can be consolidated later (blockcommit).

Additionally, a snapshot can be:

- Disk-only (most common): saves the state of the disk(s).
- With memory: includes RAM content and CPU state to resume exactly as it was (heavier and slower).

General recommendations:

- For hot snapshots, use external snapshots with `--disk-only` and, if possible, `--quiesce` with qemu-guest-agent.
- Limit the overlay chain depth; consolidate early with blockcommit to avoid performance degradation.
- Do not use snapshots as a replacement for full backups.

---

## Requirements and quick checks

```bash
# List the disks attached to the VM
virsh domblklist debian13

# Check the disk format (important for internal snapshots)
qemu-img info /var/lib/libvirt/images/debian13.qcow2

# Check if the guest agent is working (for --quiesce)
virsh domfsinfo debian13            # requires qemu-guest-agent
virsh qemu-agent-command debian13 '{"execute":"guest-info"}' --timeout 5
```

Notes:

- Internal snapshots require qcow2 and typically a powered-off VM.
- `--quiesce` requires qemu-guest-agent installed and configured in the guest.

---

## Create an external snapshot (recommended while running)

This is the most common flow before a production update.

```bash
# Hot disk snapshot with libvirt metadata
virsh snapshot-create-as \
	--domain debian13 \
	--name snap-pre-upgrade \
	--description "Before apt full-upgrade" \
	--disk-only \
	--atomic \
	--quiesce \
	--live

# If you don't have qemu-guest-agent, omit --quiesce
# virsh snapshot-create-as --domain debian13 --name snap-pre-upgrade \
#   --description "Before apt full-upgrade" --disk-only --atomic --live
```

Verify the overlays created and the snapshot metadata:

```bash
virsh snapshot-list debian13
virsh domblklist debian13
```

Typical `domblklist` output after an external snapshot:

```
 Target   Source
----------------------------------------------
 vda      /var/lib/libvirt/images/debian13-snap-pre-upgrade.qcow2
```

That indicates that writes now go to the overlay (the base file remains protected).

---

## Create an internal snapshot (powered-off VM, qcow2)

Useful for simple scenarios with qcow2 storage and no need for hot snapshots.

```bash
# Power off the VM
virsh shutdown debian13 && virsh domstate debian13

# Create an internal snapshot explicitly for disk vda
virsh snapshot-create-as \
	--domain debian13 \
	--name snap-interno \
	--description "Before changing fstab" \
	--diskspec vda,snapshot=internal

# Start again if appropriate
virsh start debian13
```

For internal snapshots, you can also use `qemu-img snapshot` with the VM powered off, but `virsh` is recommended to keep metadata consistent in libvirt.

---

## List, show info, and current snapshot

```bash
# List the VM's snapshots
virsh snapshot-list debian13

# Show information about a specific snapshot
virsh snapshot-info debian13 --snapshotname snap-pre-upgrade

# Current snapshot (to which the present state points)
virsh snapshot-current debian13
```

---

## Revert to a snapshot

With snapshots that include memory you can resume the exact state; with disk-only snapshots it's safer to revert with the VM powered off.

```bash
# Conservative option for disk-only snapshots: power off, revert, and start
virsh shutdown debian13
virsh snapshot-revert debian13 snap-pre-upgrade
virsh start debian13

# If the snapshot includes memory, you can indicate the state after reverting
# virsh snapshot-revert debian13 snap-con-memoria --running   # resume
# virsh snapshot-revert debian13 snap-con-memoria --paused    # paused
```

Tip: after reverting, validate applications and filesystems.

---

## Delete snapshots

```bash
# Delete a specific snapshot (metadata in libvirt)
virsh snapshot-delete debian13 --snapshotname snap-pre-upgrade

# Delete a snapshot and its descendants
# virsh snapshot-delete debian13 --snapshotname snap-pre-upgrade --children
```

Important: For external snapshots, deleting the metadata does NOT automatically consolidate overlays. To return to a simple chain, use blockcommit.

---

## Clean up overlays (consolidate) with blockcommit

After verifying everything is fine, it's advisable to consolidate the overlay into the base disk to avoid long snapshot chains that penalize performance.

```bash
# Identify the target (e.g., vda)
virsh domblklist debian13

# Start blockcommit live and pivot when it finishes
virsh blockcommit debian13 vda --active --verbose --pivot

# Check job status (optional)
virsh blockjob debian13 vda --info
```

After `--pivot`, the VM writes directly to the base file again and the overlay can be deleted if it's no longer referenced.

---

## Quick demo (flow idea)

```bash
# 1) Create external snapshot before making changes
virsh snapshot-create-as --domain debian13 --name snap-demo --description "Before tests" --disk-only --atomic --live

# 2) (Inside the VM) apply changes
# sudo apt update && sudo apt -y full-upgrade

# 3) If something fails, revert
virsh shutdown debian13
virsh snapshot-revert debian13 snap-demo
virsh start debian13

# 4) If everything went fine and you don't need the snapshot, consolidate and clean up
virsh blockcommit debian13 vda --active --verbose --pivot
virsh snapshot-delete debian13 --snapshotname snap-demo
```

---

## Quiesce with qemu-guest-agent (better snapshots)

To reduce the risk of inconsistencies (especially in databases), use `--quiesce` with the guest agent.

Inside the guest:

```bash
# Debian/Ubuntu
sudo apt install -y qemu-guest-agent

# RHEL/CentOS/Rocky/Fedora
sudo dnf install -y qemu-guest-agent

# Ensure the service is active
sudo systemctl enable --now qemu-guest-agent
```

In the VM definition (it usually comes in modern templates), the agent's `virtio` channel must exist. Verify:

```bash
virsh domfsinfo debian13    # if it responds, the agent is working
```

Then create snapshots with `--quiesce`.

---

## Select disks and exclusions

You can limit the snapshot to a specific disk or exclude one:

```bash
# External snapshot of disk vdb only (useful for data)
virsh snapshot-create-as \
	--domain debian13 \
	--name snap-datos \
	--description "Data only" \
	--disk-only --atomic --live \
	--diskspec vdb,snapshot=external

# Exclude an ephemeral disk (e.g., swap)
# --diskspec vdc,snapshot=no
```

---

## Common problems and how to solve them

- `--quiesce` fails: install and enable qemu-guest-agent inside the guest and check `virsh domfsinfo`.
- Unsupported storage: internal snapshots require qcow2; for raw/LVM/ceph use external snapshots.
- Snapshots with memory are heavy: they can take time and consume a lot; assess whether you really need memory.
- Deep overlay chain: I/O impact; consolidate with blockcommit early.
- Reverting a disk-only snapshot hot: may corrupt data; power off before reverting.
- Not a replacement for backups: snapshots do not protect against host failures or long-standing silent corruption.

---

## References

- [curso_virtualizacion_linux — GitHub](https://github.com/josedom24/curso_virtualizacion_linux)
- [Domain snapshots (libvirt) - Overview](https://libvirt.org/formatsnapshot.html)
- [virsh - snapshot commands](https://libvirt.org/manpages/virsh.html#domain-snapshots-commands)
- [Blockcommit (libvirt) - Consolidation of external snapshots](https://libvirt.org/kbase/blockcommit.html)
- [qemu-img snapshot - QEMU Documentation](https://www.qemu.org/docs/master/tools/qemu-img.html#snapshot-commands)
- [QEMU Guest Agent - Wiki](https://wiki.qemu.org/Features/GuestAgent)
