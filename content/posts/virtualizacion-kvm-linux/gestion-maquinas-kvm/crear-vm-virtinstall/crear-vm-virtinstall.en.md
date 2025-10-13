---
title: "Create a Virtual Machine with virt-install in KVM"
date: 2025-10-13T21:24:37+00:00
description: Learn how to create virtual machines in KVM using the virt-install command-line tool on Ubuntu/Debian systems.
tags: [Virtualization,Linux,KVM,VM,Hypervisor,Ubuntu,Debian]
hero: images/virtualizacion-kvm-linux/introduccion-kvm/crear-vm-virt-install.jpg
---

# Create a Virtual Machine with virt-install in KVM

After installing **KVM** on your Ubuntu or Debian system, the next step is to create a virtual machine using the **virt-install** command-line tool.

## Check existing virtual machines

Before creating a new VM, check if there are any existing ones:

```bash
sudo virsh list --all
```

If no machines exist, the list will be empty.

## Create a virtual machine with virt-install

The `virt-install` command allows you to specify all the VM’s properties. For example:

> [!NOTE]  
> Remember to download the ISO of the operating system you want to install.  
> It’s recommended to store it in `/var/lib/libvirt/images/`, which is the default directory for disks and images.

```bash
# Example using a local ISO

virt-install --connect qemu:///system     --name ubuntu-24.04-vm     --virt-type kvm --hvm --os-variant=ubuntu24.04     --ram 4096 --vcpus 2 --network network=default     --disk pool=default,size=20,bus=virtio,format=qcow2     --cdrom /var/lib/libvirt/images/ubuntu-24.04.3-live-server-amd64.iso     --boot uefi,cdrom,hd     --noautoconsole     --graphics none
```

### Parameter Explanation

- `--name vm-test`  
  Name of the virtual machine.

- `--virt-type kvm`  
  Defines that KVM will be used as the hypervisor.

- `--hvm`  
  Enables full hardware-assisted virtualization (HVM).

- `--os-variant=ubuntu25.04`  
  Optimizes the VM configuration according to the OS variant.

> [!NOTE]  
> You can get the full list using the command `osinfo-query os`.

- `--ram 2048`  
  Assigns 2048 MB of RAM to the VM.

- `--vcpus 2`  
  Defines 2 virtual CPUs for the VM.

- `--network network=default`  
  Connects the VM to the default network (NAT) managed by libvirt.

- `--graphics vnc,password=remotevnc,listen=0.0.0.0`  
  Configures VNC graphical console access with a password and listens on all interfaces.

- `--disk pool=default,size=20,bus=virtio,format=qcow2`  
  Creates a 20 GB disk in the default storage pool using the `virtio` bus and `QCOW2` format.

- `--cdrom /home/$USER/isos/ubuntu-25.04-server.iso`  
  Specifies the ISO file for the operating system installation.

- `--noautoconsole`  
  Prevents the console from automatically opening after VM creation.

- `--boot cdrom,hd`  
  Sets the boot order — first CD-ROM, then hard disk.

## Validate the VM creation

Once created, verify that the VM is running:

```bash
virsh list
```
Example output:
```
 Id   Name              State
---------------------------------
 1    ubuntu-24.04-vm   running
```

If your user belongs to the `libvirt` and `kvm` groups, you don’t need to use `sudo`.

## Connect to the VM

To connect graphically, you can use **virt-viewer**. Note that this requires a graphical environment on your host machine.

```bash
virt-viewer ubuntu-24.04-vm &
```

If you set a password for VNC, you will be prompted for it when connecting.

## Get the VM’s IP Address

You can retrieve the IP address assigned to the VM with:

```bash
virsh domifaddr ubuntu-24.04-vm
```
Example output:
```
 Name       MAC address          Protocol     Address
-------------------------------------------------------------------------------
 vnet10     52:54:00:18:7e:6b    ipv4         192.168.122.117/24
```

This displays the VM’s network interfaces and IP addresses, allowing you to connect via SSH or VNC from the host to continue the OS installation.