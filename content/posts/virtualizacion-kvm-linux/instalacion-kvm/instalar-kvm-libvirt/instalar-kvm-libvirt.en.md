---
title: "Installing KVM on Ubuntu/Debian"
date: 2025-10-13T10:00:00+00:00
description: Learn how to install KVM on Ubuntu/Debian systems, configure users, and verify that the installation is correct.
tags: [Virtualization,Linux,KVM,VM,Hypervisor,Ubuntu,Debian]
hero: images/virtualizacion-kvm-linux/introduccion-kvm/instalacion-kvm.jpg
---

# Installing KVM on Ubuntu/Debian

To install **KVM** on Ubuntu or Debian, you need to prepare the system with the required packages, verify hardware virtualization support, and authorize users to run virtual machines. Below are the steps to install KVM on Ubuntu 24.04 (Noble Numbat) or recent Debian releases.

## Step 1: Update the system

Before installing KVM, update your package repository information:

```bash
sudo apt update
```

## Step 2: Check virtualization support

### 2.1 Verify CPU compatibility

Check if your CPU supports hardware virtualization:

```bash
egrep -c '(vmx|svm)' /proc/cpuinfo
```

* `vmx` → Intel CPU with VT-x
* `svm` → AMD CPU with AMD-V
* `lm` → 64-bit support

If the result is 0, your processor does not support KVM. Any other number indicates that you can proceed and will also show the number of CPU cores.

### 2.2 Check KVM acceleration

```bash
sudo kvm-ok
```

If `kvm-ok` is not available, install the **cpu-checker** package:

```bash
sudo apt install cpu-checker -y
```

Then, rerun `sudo kvm-ok` to confirm that the system can use hardware-accelerated KVM.

```bash
javiercruces@FJCD-PC:~$ sudo kvm-ok
INFO: /dev/kvm exists
KVM acceleration can be used
```

## Step 3: Install KVM packages

Install the essential KVM packages:

```bash
sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils libosinfo-bin virt-install virt-manager virt-viewer libguestfs-tools -y
```

Wait for the installation to complete.

## Step 4: Authorize users

Only members of the **libvirt** and **kvm** groups can run virtual machines. To add the current user to these groups, use environment variables:

```bash
sudo adduser $USER libvirt
sudo adduser $USER kvm
```

For the changes to take effect, log out and log back in, or run:

```bash
newgrp libvirt
newgrp kvm
```

## Step 5: Verify the installation

Confirm that KVM was installed correctly with **virsh**:

```bash
sudo virsh list --all
```

This command will list all active and inactive virtual machines. If no VMs have been created yet, it will show an empty list.

You can also check the status of the virtualization service:

```bash
sudo systemctl status libvirtd
```

If the service is not active, enable it with:

```bash
sudo systemctl enable --now libvirtd
```

With this, your Ubuntu/Debian system is ready to run virtual machines using KVM.