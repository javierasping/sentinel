---
title: "Migration of a file system"
date: 2023-09-08T10:00:00+00:00
description: Learn how to migrate from one file system your debian to another larger
tags: [Debian 12,Sistemas,ISO,ASO]
hero: images/sistemas/migracion_de_sistema_de_ficheros/portada.jpg
---


Sometimes, it is necessary to update the storage of our Debian system to meet the growing space needs and improve the organization of the disk. In this guide, we will explore the migration process from a single disk to one with greater capacity, as well as divide it into separate partitions for more efficient management.

This process will not only expand the available storage space, but also provide a more orderly structure to the system, facilitating tasks such as backup management, system performance and disk space management.

### Characteristics of the machine

Create a virtual machine in virt-manager with the following features:

- GNU / Linux Debian11 operating system will be installed.
- Memory size: 1GB.
- CPU: 1
- Hard drive size: 2GB
- Details of the hypervisor:
- chipset: Q35
- Firmware: UEFIX 86

### Partition outline

The debian installation will be made, with the following partition scheme: efi partition: 50MB

partition /: 2GB

swap: the rest of spare space.

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.001.png)

No desktop environment will be installed.

Once the system is installed, we realize that we would be very just of space.

## Extending the disk

## # Partitioned

Add a disk to your 10GB system.

Partiate this disk, choosing the appropriate size for each of the partitions, keeping in mind that each partition will be assigned to a directory of those indicated:

/ boot / efi FAT32 efi partition - > 100MB / ext4 - > 8GB

/ home ext4 - > 1GB

/ var ext4 - > 400MB

/ usr ext4 - > 400MB

swap swap - > 200MB

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.002.png)

### Giving file system to partitions

To format this partition / boot / efi FAT32 partition efi - > 100MB

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.003.png)

For these partitions I will give you ext4 format: / ext4 - > 8GB

/ home ext4 - > 1GB

/ var ext4 - > 400MB

/ usr ext4 - > 400MB

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.004.png)

To give swap format: swap swap - > 200MB

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.005.png)

To "activate the swap" - > sudo swapon dev / vdb6 and then to make it permanent
add to / etc / fstab.

We would have the disk with the following formats:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.006.png)

## Data migration

## # EFI partition
Below we will make a reliable copy of each of our partitions for it, create a directory to mount each disk in a directory with its name:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.007.png)

And we'll ride the partitions in these directories:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.008.png)

We will begin to pass the information of our partitions. It is important to use the parameter a (same as dpR) that allows to make the copy recursively in addition to the permissions and links found in the system are kept intact. With parameter f, we force the copy.

Copy of the EFI partition:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.009.jpeg)


## # HOME partition


We'll set it up in any directory, then we'll copy it with rsync and with the diff command we'll check if there are different files in the directories to save us from doing the check manually.

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.010.png)

Now we'll add it to the fstab:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.011.png)

We ride it with a mount -a. We dismount it and we delete the home directory of the old disk:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.013.png)

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.014.png)

## # VAR partition


We'll set it up in any directory, then we'll copy it with rsync and with the diff command we'll check if there are different files in the directories to save us from doing the check manually.

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.015.png)

Now we'll add it to the fstab:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.016.png)

We mount it with a mount -a. We dismount it and we will delete the var directory from the old disk:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.017.png)


## USR partition

We'll set it up in any directory, then we'll copy it with rsync and with the diff command we'll check if there are different files in the directories to save us from doing the check manually.

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.018.png)

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.019.png)

Now we'll add it to the fstab:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.020.png)

We ride it with a mount-a:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.021.jpeg)

We disassemble it and delete the home directory from the old disk:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.022.png)

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.023.png)

And we'll ride them back with a mount-a.

## # RAIZ partition

We'll set it up in any directory, then we'll copy it with rsync and with the diff command we'll check if there are different files in the directories to save us from doing the check manually.

Excluding the directories we've separated before:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.024.png)

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.025.png)

Now we'll add it to the fstab:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.026.png)

To mount this partition we must restart the system.


## Generate the new EFI

For this we have to follow a different procedure, the first thing we will do is give fat32 format to the partition. Then just like the others we'll set it up and install a new grub by specifying where we want to install it, on the second disk.

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.028.png)

Now we'll add it to the fstab:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.029.png)

We will restart the equipment and check that it works:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.030.jpeg)

We will now update the grub:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.031.png)Ahora para construir el nuevo efi tendremos que a través de un cd live o desde el modo rescate construir un nuevo grub :

We mount our new system partition and give you to reinstall the grub boot charger:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.032.png)

Once this is done, we turn off the machine and put the second disk first and the boot order and reboot the equipment:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.033.png)

When we restart we choose the first option that is vdb boot:

And we will have managed to migrate the system to a larger disk:! [...] (/ img / Asposer.Words.b81bc7a-b593-45c4-8e4d-c913a16c26ef.034.png)

My / etc / fstab has been as follows:

![](/sistemas/migraciones/migracion_sistema_de_ficheros/img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.035.jpeg)


## Bibliography

- [To migrate from one disc to another] (https: / / www.dragonjar.org / migrar-installation-de -linux-a-a-a-partition-o-disco-diferente.xhtml)
- [Copy partitions] (https: / / juncotic.com / partitions-copying-installation-linux /)
- [Recover grub] (https: / / lihuen.linti.unlp.edu.ar / index.php / Gu% C3% ADa _ of _ installation% C3% B3n _ or _ recovery% C3% B3n _ of _ GRUB)

