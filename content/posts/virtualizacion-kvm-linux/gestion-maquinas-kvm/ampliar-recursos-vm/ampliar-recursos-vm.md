---
title: "Cómo ampliar memoria, CPU y discos de una máquina virtual"
date: 2025-10-16T13:00:00+00:00
description: Cómo aumentar vCPU, memoria RAM y disco de una VM en KVM, incluyendo la ampliación del sistema de archivos dentro del invitado.
tags: [KVM,Virtualizacion,Libvirt,Linux,VM,Recursos]
hero: images/virtualizacion-kvm-linux/gestion-vm/ampliar-recursos.png
weight: 5
---

En este artículo veremos tres casos prácticos para ampliar recursos en una VM gestionada con libvirt/KVM:

- Subir número de vCPU (núcleos)
- Aumentar memoria RAM
- Ampliar el disco y el sistema de archivos dentro del invitado

Usaremos comandos `virsh`, herramientas de libguestfs cuando aplique y utilidades estándar dentro del invitado (growpart, resize2fs, xfs_growfs, LVM). Incluyo vías “en caliente” cuando el sistema lo soporta y alternativas seguras en frío.

> Nota: Para ejecutar sin sudo, tu usuario debe pertenecer a los grupos `libvirt` y `kvm`.

Ejemplo de situación inicial:

```bash
virsh list --all
```

Salida de ejemplo:
```
 Id   Name       State
-----------------------------
 -    debian13   shut off
```

---

## 1 Subir vCPU (núcleos)

Hay dos límites: el máximo de vCPU definido en la VM y el número actual asignado. Puedes subir vCPU en caliente si el invitado lo soporta (CPU hotplug), o en frío ajustando la configuración persistente.

### Ver vCPU actuales y máximos

```bash
virsh vcpucount debian13 --live --maximum
virsh vcpucount debian13 --live
virsh vcpucount debian13 --config --maximum
virsh vcpucount debian13 --config
```

### Aumentar vCPU en caliente (si es posible)

```bash
# Subir a 4 vCPU en la VM en ejecución y persistir el cambio
virsh setvcpus debian13 4 --live
virsh setvcpus debian13 4 --config
```

Si aparece error, el invitado o la definición puede no permitir hotplug. Asegúrate de que el máximo lo permita:

```bash
# Subir el máximo permitido a 8 vCPU (persistente), con la VM apagada
virsh setvcpus debian13 8 --maximum --config
```

Luego ajusta el valor actual y arranca:

```bash
virsh setvcpus debian13 4 --config
virsh start debian13
``;

### Verificación dentro del invitado

```bash
nproc
lscpu | grep -i '^CPU(s)\|Model name\|Thread\|Core\|Socket'
```

---

## 2 Aumentar memoria RAM

La memoria también tiene un máximo (maxmem) y un valor actual. El hotplug de memoria depende del invitado (balloon/virtio-mem). Si falla en caliente, aplica en frío.

### Consultar memoria

```bash
virsh dominfo debian13 | grep -i memory
virsh dommemstat debian13
```

### Subir memoria en caliente (si se soporta)

```bash
# Establecer máximo a 8 GiB y subir memoria actual a 6 GiB
virsh setmaxmem debian13 8G --config
virsh setmem    debian13 6G --live
virsh setmem    debian13 6G --config
```

Si da error en `--live`, realiza el cambio con la VM apagada:

```bash
virsh shutdown debian13
virsh setmaxmem debian13 8G --config
virsh setmem    debian13 6G --config
virsh start debian13
```

### Verificación dentro del invitado

```bash
free -h
grep MemTotal /proc/meminfo
```

---

## 3 Ampliar disco y sistema de archivos

El flujo general es:

1. Ampliar el disco virtual en el host (qcow2/raw o volumen del pool)
2. Dentro del invitado, detectar el nuevo tamaño y ampliar partición/LVM según corresponda
3. Redimensionar el sistema de archivos (ext4/xfs)

> Recomendación: Haz snapshot/backup antes de modificar particiones o LVM.

### 3.1 Ampliar el disco en el host

Primero identifica la ruta del disco de la VM:

```bash
virsh domblklist debian13
```

- Si usas volumen de un pool de libvirt:

```bash
virsh vol-list default
virsh vol-resize --pool default debian13.qcow2 +10G
```

- Si usas fichero directo qcow2/raw:

```bash
qemu-img resize /var/lib/libvirt/images/debian13.qcow2 +10G
```

> Nota: Evita redimensionar un disco con snapshots encadenados sin revisar dependencias.

Reinicia la VM (si estaba encendida) para que el invitado detecte el nuevo tamaño del disco si no soporta hotplug de tamaño:

```bash
virsh shutdown debian13 && virsh start debian13
```

### 3.2 Caso A: Partición única (sin LVM)

Asumiendo un disco `vda` con una partición `vda1` usando ext4 o xfs.

1) Ampliar la partición dentro del invitado:

```bash
sudo apt install -y cloud-guest-utils  # para growpart (Debian/Ubuntu)
sudo growpart /dev/vda 1               # amplía la partición 1 para ocupar el nuevo tamaño
lsblk
```

2) Redimensionar el sistema de archivos:

- ext4:

```bash
sudo resize2fs /dev/vda1
```

- xfs (indica el punto de montaje):

```bash
sudo xfs_growfs /
```

Verifica:

```bash
df -h
```

### 3.3 Caso B: LVM (PV + VG + LV)

Asumiendo que el PV está en `/dev/vda2`, el VG es `vg0` y el LV es `lvroot` montado en `/`.

1) Detectar el nuevo tamaño en el PV:

```bash
sudo pvscan
sudo pvdisplay
sudo pvresize /dev/vda2
```

2) Ampliar el LV y el FS de una vez (ext4/xfs):

```bash
sudo lvdisplay
sudo lvextend -r -l +100%FREE /dev/vg0/lvroot
```

`-r` intenta redimensionar el sistema de archivos automáticamente. Alternativa manual:

```bash
sudo lvextend -l +100%FREE /dev/vg0/lvroot
# ext4
sudo resize2fs /dev/vg0/lvroot
# xfs (indicar punto de montaje)
sudo xfs_growfs /
```

Verifica:

```bash
lsblk
df -h
```

---

## Consejos y solución de problemas

- Hotplug de CPU/Memoria: depende del invitado (kernel, drivers, ACPI, virtio). Si falla en `--live`, haz el cambio con `--config` y reinicia.
- Límite máximo: si `setvcpus`/`setmem` fallan por límite, ajusta primero el máximo con `--maximum` (CPU) o `setmaxmem` (memoria).
- growpart no disponible: usa `parted` o `fdisk` con cuidado; asegúrate de alinear correctamente y no sobrescribir datos.
- xfs no reduce tamaño: solo crece. Para reducir xfs hay que recrear; planifica en consecuencia.

---

## Referencias

- [curso_virtualizacion_linux — GitHub](https://github.com/josedom24/curso_virtualizacion_linux)
- [virsh - Documentación oficial de libvirt](https://libvirt.org/manpages/virsh.html) - Comandos: setvcpus, setmem, setmaxmem, dominfo, vcpucount, dommemstat
- [qemu-img - QEMU Documentation](https://www.qemu.org/docs/master/tools/qemu-img.html) - Comando resize para redimensionar imágenes de disco
- [cloud-guest-utils - Launchpad](https://launchpad.net/cloud-utils) - Incluye growpart para ampliar particiones
- [resize2fs - e2fsprogs](https://man7.org/linux/man-pages/man8/resize2fs.8.html) - Redimensionar sistemas de archivos ext2/ext3/ext4
- [xfs_growfs - XFS Documentation](https://man7.org/linux/man-pages/man8/xfs_growfs.8.html) - Expandir sistemas de archivos XFS
- [LVM Administration Guide - Red Hat](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_and_managing_logical_volumes/) - pvresize, lvextend y gestión de volúmenes lógicos
