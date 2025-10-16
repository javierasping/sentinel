---
title: "Clone and rename virtual machines in KVM"
date: 2025-10-16T12:00:00+00:00
description: Learn how to clone and rename virtual machines in KVM using virt-clone, virt-sysprep, and virt-customize to create reusable templates.
tags: [KVM,Virtualization,Libvirt,Linux,VM,Cloning]
hero: images/virtualizacion-kvm-linux/clonar-renombrar-vm.jpg
---

# Clone and rename virtual machines in KVM

One of the advantages of virtualization is the ability to clone virtual machines to quickly create homogeneous environments. However, when we clone a VM that contains an operating system, the clone inherits unique identifiers such as the **machine ID**, **MAC** addresses, host **SSH** keys, etc., which should be unique for each machine.

In this guide we will cover how to:

- Clone virtual machines with `virt-clone`
- Generalize clones with `virt-sysprep`
- Customize new instances with `virt-customize`
- Rename virtual machines with `virsh domrename`
- Troubleshoot common issues after cloning

---

## Prerequisites

Make sure the following packages are installed:

```bash
# Debian/Ubuntu
sudo apt install libguestfs-tools virtinst

# RHEL/Fedora/AlmaLinux
sudo dnf install libguestfs-tools virt-install
```

**Key packages:**

- `virt-clone`: Tool for cloning virtual machines (included in `virtinst`)
- `virt-sysprep`: Tool for generalizing VMs (included in `libguestfs-tools`)
- `virt-customize`: Tool for customizing VMs without booting them (included in `libguestfs-tools`)

---

## 1. Prepare the base virtual machine

Before cloning, it’s advisable to prepare a **reference machine** with all the baseline configuration you need (installed packages, users, basic network configuration, etc.).

In our example, we’ll use a VM called `debian13` as the base machine.

### Shut down the virtual machine

Before cloning, we must shut it down:

```bash
virsh shutdown debian13
```

Verify that it is completely powered off:

```bash
virsh list --all
```

Expected output:
```
 Id   Name              State
----------------------------------
 -    debian13          shut off
```

---

## 2. Clone the virtual machine with virt-clone

`virt-clone` creates a full copy of a virtual machine, including its XML configuration and virtual disks.

### Option 1: Automatic cloning (auto-generated disk name)

You can use `--auto-clone` so that `virt-clone` automatically generates the disk name by adding the `-clone` suffix:

```bash
virt-clone --original debian13 --name debian13-clone --auto-clone
```

Expected output:
```
Allocating 'debian13-clone.qcow2'    | 20 GB  00:00:05

Clone 'debian13-clone' created successfully.
```

### Option 2: Specify a custom disk name

For more control over the disk name, use the `--file` parameter:

```bash
virt-clone --original debian13 \
	--name debian-template \
	--file /var/lib/libvirt/images/debian-template.qcow2
```

Expected output:
```
Allocating 'debian-template.qcow2'   | 20 GB  00:00:05

Clone 'debian-template' created successfully.
```

### Clone multiple disks

If your VM has multiple disks, you can specify multiple `--file` parameters:

```bash
virt-clone --original debian13 \
	--name debian-template \
	--file /var/lib/libvirt/images/debian-template-disk1.qcow2 \
	--file /var/lib/libvirt/images/debian-template-disk2.qcow2
```

---

## 3. Rename virtual machines with virsh domrename

You can change a VM’s name easily with `virsh domrename`:

```bash
virsh domrename debian13-clone debian-base-image
```

Expected output:
```
Domain successfully renamed
```

Verify the change:

```bash
virsh list --all
```

Output:
```
 Id   Name                State
-----------------------------------
 -    debian13            shut off
 -    debian-base-image   shut off
 -    debian-template     shut off
```

> **Note:** The `virsh domrename` command only changes the VM name in libvirt; it does **not** rename the disk file. If you also want to rename the disk, do it manually and then edit the XML configuration with `virsh edit`.

---

## 4. Generalize the VM with virt-sysprep

`virt-sysprep` removes machine-specific configurations to turn it into a **reusable template**. This tool is inspired by Microsoft Windows’ `sysprep` utility.

### What does virt-sysprep do?

`virt-sysprep` performs multiple cleanup operations automatically:

- Removes the **machine-id** and it will be regenerated on next boot
- Deletes **host SSH keys** (they can be regenerated automatically or manually)
- Clears the **command history** (bash_history)
- Removes fixed **MAC addresses**
- Deletes **system logs**
- Cleans the **package cache**
- Deletes **temporary files**
- And much more...

### Basic usage of virt-sysprep

```bash
sudo virt-sysprep -d debian-template
```

Output (excerpt):
```
[   0.0] Examining the guest ...
[   5.2] Performing "abrt-data" ...
[   5.2] Performing "backup-files" ...
[   5.3] Performing "bash-history" ...
[   5.3] Performing "machine-id" ...
[   5.3] Performing "net-hwaddr" ...
[   5.3] Performing "ssh-hostkeys" ...
[   5.4] Performing "tmp-files" ...
[   5.4] Performing "utmp" ...
[   5.5] Setting a random seed
[   5.5] Setting the machine ID in /etc/machine-id
```

### virt-sysprep with additional options

You can set the **hostname** and the **root password** during generalization:

```bash
sudo virt-sysprep -d debian-template \
	--hostname debian-template \
	--root-password password:MySecurePassword123!
```

### Useful virt-sysprep options

| Option | Description |
|--------|-------------|
| `--hostname NAME` | Sets the host name |
| `--root-password password:PASS` | Sets the root password |
| `--firstboot SCRIPT` | Runs a script on first boot |
| `--operations LIST` | Specifies which operations to perform (all by default) |
| `--enable OPERATIONS` | Enables specific operations |
| `--disable OPERATIONS` | Disables specific operations |

Example disabling SSH host key removal:

```bash
sudo virt-sysprep -d debian-template --operations all,-ssh-hostkeys
```

---

## 5. Create new VMs from the template

Once you have a generalized **machine image**, you can quickly create multiple instances:

```bash
virt-clone --original debian-template \
	--name vm-debian-01 \
	--file /var/lib/libvirt/images/vm-debian-01.qcow2
```

```bash
virt-clone --original debian-template \
	--name vm-debian-02 \
	--file /var/lib/libvirt/images/vm-debian-02.qcow2
```

Verify the created VMs:

```bash
virsh list --all
```

---

## 6. Customize VMs with virt-customize

`virt-customize` lets you modify a VM **without booting it**, which is ideal for quickly customizing clones.

### Basic example: Set hostname and password

```bash
sudo virt-customize -d vm-debian-01 \
	--hostname vm-debian-01 \
	--password usuario:password:MyPassword123!
```

Output:
```
[   0.0] Examining the guest ...
[   3.1] Setting a random seed
[   3.1] Setting the hostname: vm-debian-01
[   4.2] Setting passwords
[   5.0] Finishing off
```

### Advanced options for virt-customize

```bash
sudo virt-customize -d vm-debian-02 \
	--hostname vm-debian-02 \
	--root-password password:RootPass123! \
	--password admin:password:AdminPass123! \
	--ssh-inject admin:file:/home/user/.ssh/id_rsa.pub \
	--run-command 'apt update && apt install -y nginx' \
	--timezone Europe/Madrid \
	--run-command 'systemctl enable nginx'
```

### Useful options table

| Option | Description |
|--------|-------------|
| `--hostname NAME` | Sets the hostname |
| `--password USER:password:PASS` | Sets a user’s password |
| `--ssh-inject USER:file:KEY.pub` | Injects a public SSH key |
| `--run-command 'COMMAND'` | Runs a command inside the VM |
| `--install PACKAGES` | Installs packages (comma-separated) |
| `--timezone ZONE` | Sets the time zone |
| `--update` | Updates all packages |
| `--selinux-relabel` | Restores SELinux labels |

### Customization with a script

You can run a complete script:

```bash
sudo virt-customize -d vm-debian-01 \
	--upload /path/to/config.sh:/tmp/config.sh \
	--run-command 'bash /tmp/config.sh' \
	--delete /tmp/config.sh
```

---

## 7. Common problems and solutions

### Problem 1: Error connecting via SSH - "Connection refused"

**Cause:** The host SSH keys were removed by `virt-sysprep`.

**Symptoms:** When checking the SSH service status inside the VM:

```bash
sudo systemctl status sshd
```

You will see errors such as:
```
sshd[387]: error: Could not load host key: /etc/ssh/ssh_host_rsa_key
sshd[387]: error: Could not load host key: /etc/ssh/ssh_host_ecdsa_key
sshd[387]: error: Could not load host key: /etc/ssh/ssh_host_ed25519_key
sshd[387]: fatal: No supported key exchange algorithms [preauth]
```

**Solution 1:** Regenerate all SSH keys automatically:

```bash
sudo ssh-keygen -A
sudo systemctl restart sshd
```

Output:
```
ssh-keygen: generating new host keys: RSA DSA ECDSA ED25519
```

**Solution 2:** Regenerate keys manually one by one:

```bash
sudo ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa
sudo ssh-keygen -f /etc/ssh/ssh_host_ecdsa_key -N '' -t ecdsa
sudo ssh-keygen -f /etc/ssh/ssh_host_ed25519_key -N '' -t ed25519
sudo systemctl restart sshd
```

**Solution 3:** Prevent virt-sysprep from deleting SSH keys:

```bash
sudo virt-sysprep -d debian-template --operations all,-ssh-hostkeys
```

> **Warning:** If you keep the SSH keys in the template, all cloned VMs will share the same host keys, which is a security risk. Only do this in lab environments.

### Problem 2: "WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!"

**Cause:** The host’s SSH keys changed and the client still has the old key in `~/.ssh/known_hosts`.

**Solution:** Remove the old entry from the `known_hosts` file:

```bash
ssh-keygen -f "/home/usuario/.ssh/known_hosts" -R "192.168.122.50"
```

Or manually edit the `~/.ssh/known_hosts` file and remove the corresponding line.

### Problem 3: Duplicate MAC addresses

**Cause:** When cloning without `virt-sysprep`, VMs may have the same MAC address.

**Solution:** `virt-clone` automatically generates new MAC addresses. If you encounter issues, edit the VM:

```bash
virsh edit vm-debian-01
```

Find the `<interface>` section and remove or modify the `<mac address='...'/>` line. Libvirt will generate a new one on boot.

### Problem 4: Duplicate machine-id

**Cause:** The `/etc/machine-id` file is identical across all cloned VMs.

**Solution:** `virt-sysprep` already takes care of this. If you did it manually, regenerate the machine-id:

```bash
sudo rm /etc/machine-id
sudo systemd-machine-id-setup
```

---

## 8. Recommended complete workflow

Here’s a complete workflow to create and deploy multiple VMs:

### Step 1: Create and configure the base VM

```bash
# Create base VM (assuming you already have it)
virsh list --all
```

### Step 2: Shut down and clone

```bash
virsh shutdown debian13
virt-clone --original debian13 \
	--name debian-template \
	--file /var/lib/libvirt/images/debian-template.qcow2
```

### Step 3: Generalize the template

```bash
sudo virt-sysprep -d debian-template \
	--hostname debian-template \
	--root-password password:TemplatePass123!
```

### Step 4: Create new instances

```bash
# Create VM 1
virt-clone --original debian-template \
	--name vm-web-01 \
	--file /var/lib/libvirt/images/vm-web-01.qcow2

# Customize VM 1
sudo virt-customize -d vm-web-01 \
	--hostname vm-web-01 \
	--password admin:password:AdminWeb01! \
	--ssh-inject admin:file:/home/user/.ssh/id_rsa.pub \
	--run-command 'apt update && apt install -y nginx'

# Create VM 2
virt-clone --original debian-template \
	--name vm-db-01 \
	--file /var/lib/libvirt/images/vm-db-01.qcow2

# Customize VM 2
sudo virt-customize -d vm-db-01 \
	--hostname vm-db-01 \
	--password admin:password:AdminDB01! \
	--ssh-inject admin:file:/home/user/.ssh/id_rsa.pub \
	--run-command 'apt update && apt install -y postgresql'
```

### Step 5: Start and verify

```bash
virsh start vm-web-01
virsh start vm-db-01

# Check assigned IPs
virsh domifaddr vm-web-01
virsh domifaddr vm-db-01

# Connect via SSH
ssh admin@192.168.122.X
```

---

## 9. Summary of main commands

| Command | Description |
|---------|-------------|
| `virt-clone --original VM --name NEW --auto-clone` | Clone a VM with an automatic disk name |
| `virt-clone --original VM --name NEW --file DISK.qcow2` | Clone specifying the disk name |
| `virsh domrename OLD NEW` | Rename a virtual machine |
| `sudo virt-sysprep -d VM` | Generalize a VM by removing unique identifiers |
| `sudo virt-customize -d VM --hostname NAME` | Customize a VM without booting it |
| `sudo ssh-keygen -A` | Regenerate all SSH host keys |
| `virsh edit VM` | Edit a VM’s XML configuration |

---

## References

- [virt-clone official documentation](https://linux.die.net/man/1/virt-clone)
- [virt-sysprep official documentation](https://libguestfs.org/virt-sysprep.1.html)
- [virt-customize official documentation](https://libguestfs.org/virt-customize.1.html)
- [libguestfs - Tools for accessing and modifying VM disk images](https://libguestfs.org/)