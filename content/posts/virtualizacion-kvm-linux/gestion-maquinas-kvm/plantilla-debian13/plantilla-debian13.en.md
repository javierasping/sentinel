---
title: "How to create a Debian 13 virtual machine template"
date: 2025-10-18T09:00:00+00:00
description: "Step-by-step guide to create a Debian 13 golden image with KVM/libvirt: preparation, generalization with virt-sysprep, compaction with virt-sparsify, read-only marking and cloning best practices."
tags: [KVM,Virtualization,Libvirt,Linux,VM,Templates,Debian13]
hero: images/virtualizacion-kvm-linux/gestion-vm/plantillas.png
weight: 7
---

# Virtual machine templates

A virtual machine template is a preconfigured OS image that we use to quickly deploy new VMs, avoiding repetitions and errors. Here we'll see how to create a Debian 13 master template ready for cloning.

---

## 1 Create and install the base VM

Create a clean Debian 13 VM, apply all updates and add the common software you want on all clones (guest agent, utilities, etc.). Minimal example:

```bash
# Create the base VM (adjust CPU, RAM, disk, ISO and network to your environment)
virt-install \
  --name debian13-base \
  --memory 4096 \
  --vcpus 2 \
  --disk path=/var/lib/libvirt/images/debian13-base.qcow2,size=20,format=qcow2 \
  --cdrom /var/lib/libvirt/images/debian-13.1.0-amd64-netinst.iso \
  --os-variant debian12 \
  --network network=default,model=virtio \
  --noautoconsole
```

Once the VM is created, install all the components you want this template to have: users, packages, etc.

To do this, I'll check that it's running and start with the installation:

```bash
$ virsh list 
 Id   Name            State
-------------------------------
 1    debian13-base   running
```

I'll connect via SSH to the machine:

I'll connect via SSH to the machine:

```bash
javiercruces@FJCD-PC:~/Documentos/sentinel (feature/kvm) [prd-eu-central|]
$ virsh domifaddr debian13-base
 Name       MAC address          Protocol     Address
-------------------------------------------------------------------------------
 vnet8      52:54:00:62:d5:6a    ipv4         192.168.122.202/24
 -          -                    ipv4         192.168.122.201/24

javiercruces@FJCD-PC:~/Documentos/sentinel (feature/kvm) [prd-eu-central|]
$ ssh 192.168.122.202
The authenticity of host '192.168.122.202 (192.168.122.202)' can't be established.
ED25519 key fingerprint is SHA256:RvOdKE4i1eQNHJ8bdK6RoYl9GckeGN2xY6X/IsPvMHI.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.122.202' (ED25519) to the list of known hosts.
javiercruces@192.168.122.202's password: 
Linux debian13-base 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.


javiercruces@debian13-base:~$ 
```


In my case, I'll update it to the latest version and install qemu-utils. Also, since I'll only use this machine for testing, I'll configure my SSH key so I can connect to it without needing to enter my password.

```bash
# Inside the VM I ran the following commands:
sudo apt update && sudo apt -y full-upgrade
sudo apt install -y qemu-guest-agent cloud-guest-utils

# Inside our user we generate the following files and assign permissions:
javiercruces@debian13-base:~$ mkdir -p ~/.ssh
javiercruces@debian13-base:~$ touch ~/.ssh/authorized_keys
javiercruces@debian13-base:~$ chmod 700 ~/.ssh
javiercruces@debian13-base:~$ chmod 600 ~/.ssh/authorized_keys

# With this command we add the public key we want to use on the VM
javiercruces@FJCD-PC:~$ ssh-copy-id -i ~/.ssh/jcruces.pub javiercruces@192.168.122.202   

# Finally, I verify I can connect using the SSH key. Remember to disable password authentication in the SSH service.
javiercruces@FJCD-PC:~ [prd-eu-central|]
$ ssh javiercruces@192.168.122.202
Linux debian13-base 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Oct 18 16:35:26 2025 from 192.168.122.1
```

Shut down the base VM when done:

```bash
javiercruces@FJCD-PC:~$ virsh shutdown debian13-base
Domain 'debian13-base' is being shutdown
```

---

## 2 Generalize the image with virt-sysprep

Generalization removes and regenerates elements that must be unique in each clone (machine-id, host SSH keys, hostname, logs, caches, etc.). For Linux we'll use `virt-sysprep` (package `libguestfs-tools`).

```bash
# Generalize by specifying the domain (VM must be powered off)
virt-sysprep -d debian13-base \
  --hostname plantilla-debian13 \
  --firstboot-command "dpkg-reconfigure openssh-server"
```

Notes:
- `--hostname` sets the template hostname.
- `--firstboot-command` executes the command on the first boot of the clone to regenerate host SSH keys.
- You can add/remove operations with `--enable/--operations` (see `virt-sysprep --list-operations`).

---

## 3 Compact the image with virt-sparsify

To save space, compact the image (removes empty blocks) and optionally compress it.

With the base installation, in my case the image occupies around 2 GB real space.
Be careful, because if you try to check its size with ls, you'll see the total logical size the image can reach, not the space it's really using:

```bash
# This way you'd see the total logical size the VM disk can occupy
javiercruces@FJCD-PC:~ [prd-eu-central|]
$ sudo ls -lh /var/lib/libvirt/images/ | grep debian13-base
-rw------- 1 root         root  21G oct 18 16:47 debian13-base.qcow2

# This way you'd see the real size the disk occupies
javiercruces@FJCD-PC:~ [prd-eu-central|]
$ sudo du -h --max-depth=1 /var/lib/libvirt/images/debian13-base.qcow2
2,0G	/var/lib/libvirt/images/debian13-base.qcow2

```

Now we'll compress the base image to make it occupy less:

```bash
sudo virt-sparsify --compress \
  /var/lib/libvirt/images/debian13-base.qcow2 \
  /var/lib/libvirt/images/plantilla-debian13-comprimida.qcow2
```

Keep in mind that before replacing the real image with the compressed one, you should test that a machine can boot using this new disk. 
```bash
# Replace the image with the compacted one
sudo mv /var/lib/libvirt/images/plantilla-debian13-comprimida.qcow2 \
  /var/lib/libvirt/images/debian13-base.qcow2
```

Now, if we check the image size again, we'll see it went from occupying 2GB to 586MB:

```bash
javiercruces@FJCD-PC:~$ sudo du -h --max-depth=1 /var/lib/libvirt/images/debian13-base.qcow2
586M	/var/lib/libvirt/images/debian13-base.qcow2
```

---

## 4 Mark the image as read-only (avoid booting the template)

To avoid losing the template, mark the image as read-only. If someone tries to boot it by mistake, it will fail.

```bash
sudo chmod 444 /var/lib/libvirt/images/debian13-base.qcow2
```

Also, if you want, rename the domain to identify it's a template. In my case I won't:

```bash
virsh domrename debian13-base plantilla-debian13
```

---

## 5 Create clones from the template

You have two main ways:

- Full clone: independent image; takes as much space as the original.
- Linked clone: creates an overlay layer on top of the template (read-only); takes less space, depends on the base.

### 5.1 Full clone

This way we'll create a full clone using the template disk that will occupy as much as the original:

```bash
sudo virt-clone --original debian13-base --name debian13-clonacion-completa \
  --file /var/lib/libvirt/images/debian13-clonacion-completa.qcow2
```

With this command we'll have a new virtual machine with the same components as the template.

Before starting the full clone as a non-root user, make sure to set the correct owner and permissions on the newly created disk file. On many distributions the QEMU/libvirt process runs as `libvirt-qemu:libvirt-qemu` or `qemu:qemu`; if permissions are not corrected, starting the VM as a non-root user may fail.

```bash
javiercruces@FJCD-PC:~$ sudo chown libvirt-qemu:libvirt-qemu /var/lib/libvirt/images/debian13-clonacion-completa.qcow2
javiercruces@FJCD-PC:~$ sudo chmod 660 /var/lib/libvirt/images/debian13-clonacion-completa.qcow2

javiercruces@FJCD-PC:~$ sudo virsh start debian13-clonacion-completa
Domain 'debian13-clonacion-completa' started
```

If your distribution uses a different user/group for the qemu process (for example `qemu:qemu`), replace `libvirt-qemu:libvirt-qemu` accordingly. Also check SELinux/AppArmor policies if permission issues persist.


### 5.2 Linked clone

We can do this in two different ways.

The first is to generate the disk as a backing file to the template (read-only) using qemu-img:

```bash
sudo qemu-img create -f qcow2 \
  -F qcow2 \
  -b /var/lib/libvirt/images/debian13-base.qcow2 \
  /var/lib/libvirt/images/debian13-clonacion-enlazada.qcow2
```

After generating the disk, we create the virtual machine using it:

```bash
sudo virt-install \
  --name debian13-clonacion-enlazada \
  --memory 4096 \
  --vcpus 2 \
  --disk path=/var/lib/libvirt/images/debian13-clonacion-enlazada.qcow2,format=qcow2 \
  --os-variant debian12 \
  --network network=default,model=virtio \
  --import \
  --noautoconsole
```

Before starting the cloned VM, make sure to set the correct owner and permissions on the newly created disk file to avoid access errors when the hypervisor process (qemu/libvirt) runs as a non-root user. On many systems the process runs as `libvirt-qemu:libvirt-qemu` or `qemu:qemu`.

```bash
javiercruces@FJCD-PC:~$ sudo chown libvirt-qemu:libvirt-qemu /var/lib/libvirt/images/debian13-clonacion-enlazada.qcow2
javiercruces@FJCD-PC:~$ sudo chmod 660 /var/lib/libvirt/images/debian13-clonacion-enlazada.qcow2

javiercruces@FJCD-PC:~$ sudo virsh start debian13-clonacion-enlazada
Domain 'debian13-clonacion-enlazada' started
```

If your distribution uses a different user/group for qemu (for example `qemu:qemu`), replace `libvirt-qemu:libvirt-qemu` accordingly. Also check SELinux/AppArmor policies if you still encounter permission issues.

---

## References

- [curso_virtualizacion_linux — GitHub](https://github.com/josedom24/curso_virtualizacion_linux)

- [virt-sysprep (libguestfs)](https://libguestfs.org/virt-sysprep.1.html)
- [virt-sparsify (libguestfs)](https://libguestfs.org/virt-sparsify.1.html)
- [virt-clone (libvirt)](https://libvirt.org/manpages/virt-clone.html)
- [virt-customize (libguestfs)](https://libguestfs.org/virt-customize.1.html)
- [qemu-img (resize/create/backing)](https://www.qemu.org/docs/master/tools/qemu-img.html)
