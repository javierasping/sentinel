---
title: "How to manage virtual machines using virsh"
date: 2025-10-16T10:00:00+00:00
description: Practical guide on how to manage virtual machines with virsh, the libvirt command-line interface for KVM.
tags: [KVM,Virtualization,Libvirt,Linux,VM,Administration]
hero: images/virtualizacion-kvm-linux/gestion-vm/gestion-virsh.png
weight: 3
---

`virsh` is a powerful command-line tool included in **libvirt** that allows you to manage virtual machines and associated resources in **KVM**.  
Through `virsh`, you can create, start, stop, modify, and monitor domains (virtual machines), as well as manage networks, volumes, and storage pools.

---

## 1. Domain (Virtual Machine) Management

| Command | Description |
|----------|-------------|
| `virsh list --all` | Lists all virtual machines, both active and inactive. |
| `virsh start vm_name` | Starts a previously defined virtual machine. |
| `virsh shutdown vm_name` | Shuts down a virtual machine gracefully. |
| `virsh destroy vm_name` | Stops a virtual machine immediately (similar to forcefully powering it off). |
| `virsh suspend vm_name` | Suspends the execution of a virtual machine. |
| `virsh resume vm_name` | Resumes a suspended machine. |
| `virsh reboot vm_name` | Reboots the virtual machine. |
| `virsh reset vm_name` | Resets a virtual machine as if the physical reset button was pressed. |
| `virsh autostart vm_name` | Enables automatic startup of the VM when the host boots. |
| `virsh dominfo vm_name` | Shows detailed information about the VM (state, UUID, CPU, memory, etc.). |
| `virsh dumpxml vm_name` | Shows the complete XML definition of the VM. |
| `virsh edit vm_name` | Opens the VM's XML definition in an editor for modification. |
| `virsh undefine vm_name` | Removes the VM definition without deleting its disk. |
| `virsh domrename old_name new_name` | Changes the name of a virtual machine. |

---

## 2. Information and Monitoring

| Command | Description |
|----------|-------------|
| `virsh domstate vm_name` | Shows the current state of a VM (`running`, `shut off`, etc.). |
| `virsh domstats vm_name` | Shows real-time CPU, network, and disk statistics. |
| `virsh domblklist vm_name` | Lists block devices (disks) associated with a VM. |
| `virsh domblkinfo vm_name vda` | Shows detailed information about a virtual disk. |
| `virsh domiflist vm_name` | Shows network interfaces connected to the VM. |
| `virsh domifaddr vm_name` | Shows IP addresses assigned to the VM's network interfaces. |
| `virsh cpu-stats vm_name` | Shows detailed CPU usage statistics for the VM. |
| `virsh dommemstat vm_name` | Shows memory usage statistics for a VM. |
| `virsh console vm_name` | Connects to the virtual machine's text console. |
| `virsh vncdisplay vm_name` | Shows the VNC port assigned to the VM for graphical access. |

---

## 3. Storage

| Command | Description |
|----------|-------------|
| `virsh pool-list` | Lists all storage pools. |
| `virsh pool-info pool_name` | Shows detailed information about a pool. |
| `virsh pool-start pool_name` | Starts a storage pool. |
| `virsh pool-destroy pool_name` | Stops a storage pool. |
| `virsh pool-undefine pool_name` | Removes the pool definition. |
| `virsh vol-list pool_name` | Lists volumes (disks) within a pool. |
| `virsh vol-info --pool pool_name vol_name` | Shows information about a volume. |
| `virsh vol-create-as pool_name vol_name 20G --format qcow2` | Creates a new 20 GB volume in QCOW2 format. |
| `virsh vol-delete --pool pool_name vol_name` | Deletes a volume from a pool. |
| `virsh vol-clone --pool pool_name source_vol new_vol` | Clones an existing volume. |

---

## 4. Virtual Networks

| Command | Description |
|----------|-------------|
| `virsh net-list --all` | Lists all virtual networks, both active and inactive. |
| `virsh net-info net_name` | Shows detailed information about a network. |
| `virsh net-start net_name` | Starts a virtual network. |
| `virsh net-destroy net_name` | Stops a virtual network. |
| `virsh net-autostart net_name` | Enables automatic startup of a network. |
| `virsh net-edit net_name` | Edits the XML configuration of a network. |
| `virsh net-dumpxml net_name` | Shows the XML definition of a network. |
| `virsh net-update net_name` | Updates network parameters without needing to restart it. |
| `virsh net-dhcp-leases net_name` | Shows IP addresses delivered by DHCP on a network. |

---

## 5. Snapshots and Backups

| Command | Description |
|----------|-------------|
| `virsh snapshot-list vm_name` | Lists available snapshots for a VM. |
| `virsh snapshot-create-as vm_name snapshot_name "Description"` | Creates a snapshot with name and description. |
| `virsh snapshot-revert vm_name snapshot_name` | Reverts the VM to the state saved in a snapshot. |
| `virsh snapshot-delete vm_name snapshot_name` | Deletes a specific snapshot. |
| `virsh backup-begin vm_name --target /backup/` | Initiates a backup of the VM's disks. |
| `virsh backup-dumpxml vm_name` | Shows XML information about an ongoing backup task. |

---

## 6. Migration and State Saving

| Command | Description |
|----------|-------------|
| `virsh save vm_name /ruta/estado.save` | Saves the current state of a VM to a file. |
| `virsh restore /ruta/estado.save` | Restores a VM from a saved file. |
| `virsh migrate --live vm_name qemu+ssh://host_destino/system` | Migrates a running VM to another host via SSH. |

---

## 7. Host and Hypervisor Information

| Command | Description |
|----------|-------------|
| `virsh nodeinfo` | Shows information about the host's CPU, memory, and architecture. |
| `virsh capabilities` | Shows the hypervisor's capabilities (CPU, virtualization, etc.). |
| `virsh domcapabilities` | Shows capabilities supported by VMs. |
| `virsh version` | Shows the version of libvirt and the hypervisor. |
| `virsh hostname` | Shows the hostname running libvirt. |
| `virsh uri` | Shows the connection URI to the hypervisor. |

---

## 8. Additional Tips

- To run commands without privileges, you can use `--connect qemu:///session` or adding your user to the group kvm and libvirt.
- If managing system VMs, use `sudo virsh --connect qemu:///system`.
- Use `virsh help <section>` to see all available commands in a group (for example, `virsh help domain`).
- All changes made via `virsh edit` are saved directly to the configuration XML files in `/etc/libvirt/qemu/`.

---