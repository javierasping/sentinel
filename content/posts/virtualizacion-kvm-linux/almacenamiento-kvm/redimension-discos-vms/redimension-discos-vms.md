---
title: "Cómo redimensionar discos de máquinas virtuales"
date: 2025-10-25T09:00:00+00:00
description: "Cómo ampliar volúmenes con `virsh vol-resize` o `qemu-img resize` y los pasos necesarios dentro de la VM (redimensionar particiones y sistemas de archivos). Buenas prácticas y riesgos."
tags: [KVM,Virtualizacion,Libvirt,Almacenamiento,Redimension]
hero: images/virtualizacion-kvm-linux/almacenamiento/redimensionar-volumenes.png
weight: 4
---

En este ejemplo usaremos el pool `default` y un volumen llamado `vdisk-10G.img`. Mostraremos cómo crear el volumen desde el host, cómo formatearlo con los sistemas de ficheros más comunes (ext4, FAT32, XFS, btrfs) usando la VM invitada, y finalmente cómo añadir 10 GB al volumen y redimensionar la partición y el sistema de ficheros.

Nota: los comandos que actúan sobre la gestión de volúmenes (crear, redimensionar) se ejecutan en el host y usan tu prompt de ejemplo. Los comandos que se ejecutan dentro del invitado (para particionar y formatear) se muestran con el prompt del invitado `javiercruces@debian13:~$`.

### 1 Crear los volúmenes
 Crear el volumen (host)

Crearemos el volumen en formato qcow2 (aprovisionamiento ligero/thin). Puedes usar `virsh vol-create-as` o `qemu-img` según prefieras.

```bash
javiercruces@FJCD-PC:~$ # Crear con libvirt en el pool `default` (qcow2, thin)
javiercruces@FJCD-PC:~$ virsh vol-create-as --pool default --format qcow2 vdisk-10G.qcow2 10G

javiercruces@FJCD-PC:~$ # Alternativa: crear el fichero manualmente con qemu-img
javiercruces@FJCD-PC:~$ qemu-img create -f qcow2 /var/lib/libvirt/images/vdisk-10G.qcow2 10G
```

Comprobar que existe:

```bash
javiercruces@FJCD-PC:~$ virsh vol-list default
 Name            Path
-------------------------------------------------
 vdisk-10G.qcow2 /var/lib/libvirt/images/vdisk-10G.qcow2
```

Puedes inspeccionar el fichero con `qemu-img info` para ver que es qcow2 y su asignación actual:

```bash
javiercruces@FJCD-PC:~$ qemu-img info /var/lib/libvirt/images/vdisk-10G.qcow2
image: /var/lib/libvirt/images/vdisk-10G.qcow2
file format: qcow2
virtual size: 10G (10737418240 bytes)
disk size: 196K
```

### 2 Adjuntar el volumen a una VM para formatearlo (host)

Adjunta el volumen a una VM (ej. `testguest1`) como `vdb` en caliente y de forma persistente:

```bash
javiercruces@FJCD-PC:~$ virsh attach-disk --live --config testguest1 /var/lib/libvirt/images/vdisk-10G.qcow2 vdb
```

### 3 Crear una sola partición y formatear dentro del invitado

Conéctate al invitado (ejemplo):

```bash
javiercruces@FJCD-PC:~$ ssh javiercruces@debian13
javiercruces@debian13:~$ sudo -i
```

Usaremos `parted` para crear una tabla GPT o MSDOS y una única partición que ocupe todo el disco:

```bash
javiercruces@debian13:~$ sudo parted /dev/vdb --script mklabel gpt mkpart primary 0% 100%
```

Después de crear la partición normalmente el kernel crea `/dev/vdb1`. A continuación ejemplos de formateo para varios sistemas de ficheros comunes:

- ext4

```bash
javiercruces@debian13:~$ sudo mkfs.ext4 -F /dev/vdb1
sudo mkdir -p /mnt/vdb1 && sudo mount /dev/vdb1 /mnt/vdb1
sudo bash -c 'echo "Prueba ext4" > /mnt/vdb1/README.txt'
```

- FAT32 (vfat)

```bash
javiercruces@debian13:~$ sudo apt update && sudo apt install -y dosfstools
javiercruces@debian13:~$ sudo mkfs.vfat -F 32 /dev/vdb1
sudo mkdir -p /mnt/vdb1 && sudo mount -o uid=1000,gid=1000 /dev/vdb1 /mnt/vdb1
sudo bash -c 'echo "Prueba FAT32" > /mnt/vdb1/README.txt'
```

- XFS

```bash
javiercruces@debian13:~$ sudo apt update && sudo apt install -y xfsprogs
javiercruces@debian13:~$ sudo mkfs.xfs -f /dev/vdb1
sudo mkdir -p /mnt/vdb1 && sudo mount /dev/vdb1 /mnt/vdb1
sudo bash -c 'echo "Prueba XFS" > /mnt/vdb1/README.txt'
```

- Btrfs

```bash
javiercruces@debian13:~$ sudo apt update && sudo apt install -y btrfs-progs
javiercruces@debian13:~$ sudo mkfs.btrfs -f /dev/vdb1
sudo mkdir -p /mnt/vdb1 && sudo mount /dev/vdb1 /mnt/vdb1
sudo bash -c 'echo "Prueba BTRFS" > /mnt/vdb1/README.txt'
```

Desmonta cuando termines las pruebas:

```bash
javiercruces@debian13:~$ sudo umount /mnt/vdb1
exit
```

### 4 Ampliar el volumen en 10 GB (host)

En el host aumenta el tamaño del volumen a 20G (virsh vol-resize usa tamaño absoluto):

```bash
javiercruces@FJCD-PC:~$ virsh vol-resize --pool default vdisk-10G.img 20G
```

Si la VM está usando el disco en caliente, las siguientes operaciones dentro del invitado permitirán que la partición y el FS vean el nuevo espacio.

### 5 Redimensionar partición y sistema de ficheros dentro del invitado

Vuelve a conectarte al invitado (si lo tenías abierto reutiliza la sesión). Usaremos `growpart` cuando esté disponible para extender la partición y luego la herramienta de cada FS para ampliar el tamaño del sistema de ficheros.

```bash
javiercruces@FJCD-PC:~$ ssh javiercruces@debian13
javiercruces@debian13:~$ sudo apt update && sudo apt install -y cloud-guest-utils
javiercruces@debian13:~$ sudo growpart /dev/vdb 1
```

- ext4 (online)

```bash
javiercruces@debian13:~$ sudo resize2fs /dev/vdb1
```

- XFS (online, debe estar montado; crece en el punto de montaje)

```bash
javiercruces@debian13:~$ sudo mount /dev/vdb1 /mnt/vdb1    # si no está ya montado
javiercruces@debian13:~$ sudo xfs_growfs /mnt/vdb1
```

- Btrfs (online)

```bash
javiercruces@debian13:~$ sudo mount /dev/vdb1 /mnt/vdb1
javiercruces@debian13:~$ sudo btrfs filesystem resize max /mnt/vdb1
```

- FAT32

FAT32 no es tan flexible: para redimensionarlo en caliente necesitarás herramientas como `fatresize` (no siempre instaladas) o realizar la operación offline desde el host con `guestfish` o desmontando y usando `fatresize` dentro del invitado. Ejemplo si tienes `fatresize`:

```bash
javiercruces@debian13:~$ sudo apt install -y fatresize
javiercruces@debian13:~$ sudo fatresize -s 20G /dev/vdb1
```

Si `fatresize` no está disponible, la alternativa es hacer la operación offline (desmontar y usar `guestfish` o boot desde un ISO de rescate) o recrear la partición y restaurar los datos.