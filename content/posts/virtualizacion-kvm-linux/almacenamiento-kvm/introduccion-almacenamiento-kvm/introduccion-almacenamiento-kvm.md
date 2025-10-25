---
title: "Introducción al almacenamiento en KVM/libvirt"
date: 2025-10-25T09:00:00+00:00
description: "Conceptos fundamentales: pools de almacenamiento, volúmenes, formatos (raw, qcow2), snapshots y tipos de backend (dir, disk, LVM, iSCSI, ZFS, etc.)."
tags: [KVM,Virtualizacion,Libvirt,Almacenamiento]
hero: images/virtualizacion-kvm-linux/almacenamiento-kvm/introduccion-almacenamiento-kvm.jpg
---

El almacenamiento es un pilar en la virtualización: define cómo y dónde se guardan los discos de las máquinas virtuales, cómo se gestionan instantáneas (snapshots), y qué opciones de rendimiento y protección están disponibles.

En el ecosistema KVM/libvirt el almacenamiento se organiza en dos conceptos básicos:

- Pools de almacenamiento (storage pools): agrupaciones lógicas que representan una fuente de almacenamiento (por ejemplo, un directorio, un conjunto LVM, un target iSCSI o un pool Ceph). Libvirt expone y gestiona estos pools para simplificar el uso del almacenamiento por parte de las VMs.
- Volúmenes de almacenamiento (storage volumes): las unidades dentro de un pool que sirven como discos virtuales para las máquinas.

## Tipos de pools

Libvirt soporta múltiples tipos de pool. A modo de resumen práctico:

- Basados en ficheros: `dir`, `fs`, `netfs` (útiles por su sencillez y adecuados en entornos pequeños o de pruebas).
- Basados en bloque: `disk`, `logical` (LVM), `zfs` (ofrecen mayor control y rendimiento para I/O intensivo).
- Red y distribuidos: `iscsi`, `rbd` (Ceph), `gluster` (ofrecen escalabilidad y tolerancia a fallos, pero requieren más operación).

Cada tipo tiene ventajas y limitaciones; elegir uno u otro depende de requisitos de rendimiento, resiliencia y operativa.

### Pools basados en ficheros

Los **pools basados en ficheros** (`dir`, `fs`, `netfs`) almacenan los discos virtuales como **ficheros dentro de un sistema de archivos**, ya sea local o remoto.  
Son los más sencillos de configurar y los más utilizados en entornos de laboratorio, desarrollo o despliegues de pequeña escala.

- **`dir`**: almacena las imágenes de disco como ficheros en un directorio local, normalmente en rutas como `/var/lib/libvirt/images`. Es el tipo de pool más sencillo y el más común en entornos de laboratorio o desarrollo.

  - **`raw`**: formato binario directo que representa el contenido exacto del disco. Ocupa el tamaño total asignado y ofrece acceso directo sin metadatos adicionales.

  - **`qcow2`**: formato nativo de QEMU con soporte para aprovisionamiento ligero, snapshots e imágenes base. El tamaño crece dinámicamente conforme se escriben datos.

  - **`vdi`**: formato de disco de VirtualBox. Permite aprovisionamiento dinámico y snapshots, aunque está pensado para su uso con el hipervisor de Oracle.

  - **`vmdk`**: formato de VMware, ampliamente utilizado en entornos vSphere y Workstation. Soporta discos divididos y snapshots, y puede convertirse fácilmente para uso con QEMU/KVM.

  - **`vhd`** y **`vhdx`**: formatos de Microsoft Hyper-V. `vhdx` es la evolución del formato original, con soporte para discos de mayor tamaño, protección frente a corrupción y mejor alineación para discos modernos.
- **`fs`**: similar a `dir`, pero el pool se basa en un punto de montaje de un sistema de archivos local ya existente (por ejemplo, una partición montada en `/mnt/storage`).
- **`netfs`**: permite montar un sistema de archivos remoto (por ejemplo, **NFS** o **CIFS**) y usarlo como backend de almacenamiento compartido. Ideal cuando varios hosts KVM deben acceder a las mismas imágenes.

---

### Pools basados en bloques

Los **pools basados en bloques** (`disk`, `logical`, `zfs`) operan directamente sobre **dispositivos de bloque físicos o virtuales**, ofreciendo una gestión más cercana al hardware.  
Son apropiados para entornos donde se priorizan el rendimiento, la consistencia y el control fino sobre el almacenamiento.

- **`disk`**: representa un dispositivo de bloque o disco físico completo. Los volúmenes se corresponden con particiones creadas dentro del dispositivo.  
  Este tipo de pool es útil cuando se desea exponer discos dedicados a las máquinas virtuales sin intermediarios, o gestionar particiones específicas desde libvirt.

- **`logical`**: usa **LVM (Logical Volume Manager)** como backend. Los volúmenes se crean dentro de un grupo de volúmenes (VG) y se administran como volúmenes lógicos (LV).  
  Es uno de los métodos más flexibles: permite redimensionar, tomar snapshots, y gestionar espacio de manera granular sin depender de sistemas de archivos intermedios.

- **`zfs`**: se basa en **ZFS**, creando datasets y volúmenes (zvols) que pueden exportarse como bloques o como sistemas de archivos.  
  Ofrece funciones avanzadas como snapshots, clonación instantánea, compresión y verificación de integridad integrada.

---

### Pools basados en red y distribuidos

Los **pools basados en red y distribuidos** proporcionan acceso a almacenamiento remoto o replicado a través de la red.  
Se emplean cuando varios hosts KVM deben compartir los mismos volúmenes, como en entornos de alta disponibilidad o clusters de virtualización.

- **`iscsi`** y **`iscsi-direct`**: conectan a destinos iSCSI que exponen LUNs.  
  El tipo `iscsi` monta los dispositivos como bloques locales, mientras que `iscsi-direct` permite un acceso más directo sin necesidad de un dispositivo persistente.  

- **`rbd` (Ceph)**: usa el backend de **Ceph RADOS Block Device**, que ofrece almacenamiento distribuido y redundante.  
  Los volúmenes se almacenan como objetos en el clúster Ceph, con replicación y recuperación automática.  

- **`gluster`**: integra **GlusterFS** como sistema de archivos distribuido.  
  Permite que varios hosts accedan simultáneamente a un mismo conjunto de imágenes, ideal para infraestructuras de virtualización compartidas.


## Otras características que ofrecen los tipos de almacenamiento

### Snapshots

Los snapshots son copias puntuales del estado del disco o del volumen. Pueden existir a distintos niveles:

- Snapshot a nivel de imagen (formatos COW como `qcow2`).
- Snapshot a nivel de volumen/dispositivo (LVM, ZFS, backends que ofrecen snapshots atomizados).

Normalmente su utilizan para realizar pruebas, actualizaciones con posibilidad de revertir, y creación rápida de clones. Los snapshots incrementan la complejidad de las cadenas de almacenamiento, pueden penalizar el rendimiento (especialmente con varias capas COW) y requieren un plan de gestión (consolidación y limpieza periódica).

### Aprovisionamiento ligero (thin provisioning)

Thin provisioning permite presentar discos de tamaño mayor del que físicamente existe, consumiendo espacio sólo cuando se escriben datos. Esto mejora la densidad de uso del almacenamiento pero exige monitorización activa para evitar quedarse sin capacidad física.

En contraste, la preallocación reserva el espacio completo en el momento de la creación: es más predecible en rendimiento y uso de espacio, pero menos eficiente en términos de almacenamiento.

### Backing files y clones

Los formatos que soportan backing files (por ejemplo `qcow2`) permiten crear imágenes base inmutables y múltiples imágenes derivadas ligeras. Esto acelera despliegues, pero complica backups y restauraciones cuando las cadenas son largas; a menudo es recomendable consolidar o convertir a imágenes planas antes de operaciones críticas.

## Fuentes y lectura recomendada

 
- [Libvirt — Storage management; Storage pool and volume XML format](https://libvirt.org/storage.html)
- [Libvirt — Storage pool and volume XML format (detalles de formato)](https://libvirt.org/formatstorage.html)
- [QEMU — Disk images, formats y qemu-img](https://qemu.org/docs/master/system/images.html)
- [Ceph — RBD (uso con libvirt)](https://docs.ceph.com/en/latest/rbd/)
- [LVM — documentación y buenas prácticas](https://man7.org/linux/man-pages/man8/lvm.8.html)
- [open-iscsi — documentación sobre iSCSI en Linux](https://linux-iscsi.org/wiki/Main_Page)
- [Cockpit — interfaz web para gestión de máquinas y almacenamiento](https://cockpit-project.org/)
- [NFS — guía general y consideraciones](https://nfs.sourceforge.net/)