---
title: "Gestión de volúmenes con virsh"
date: 2025-10-25T09:00:00+00:00
description: "Operaciones con volúmenes dentro de pools: listar, crear (vol-create-as), borrar (vol-delete), clonar, redimensionar (vol-resize), vol-download, vol-upload. Comportamiento según tipo de pool."
tags: [KVM,Virtualizacion,Libvirt,Almacenamiento,Volumenes]
hero: images/virtualizacion-kvm-linux/almacenamiento-kvm/gestion-volumenes-virsh.jpg
---

Breve: ejemplos de uso de la API de libvirt (`virsh vol-*`) para gestionar volúmenes dentro de pools y las diferencias según el backend.

## Gestión de volúmenes de almacenamiento con virsh

En este apartado vamos a estudiar la gestión de volúmenes de almacenamiento usando la API de libvirt (herramienta `virsh`). Trabajaremos sobre pools de tipo `dir` (ficheros de imagen en disco), aunque muchas de las operaciones son compatibles con otros backends; donde existan diferencias, se indicará.

### Pools y volúmenes: concepto rápido

Un "volumen" en libvirt es la unidad de almacenamiento creada dentro de un pool. En pools de tipo `dir` y `fs` los volúmenes son ficheros (por ejemplo `qcow2`, `raw`), en `logical` son volúmenes LVM, en `disk` pueden mapearse a particiones y en backends de red (Gluster, RBD, iSCSI) la creación y gestión puede requerir herramientas específicas.

### Comprobar espacio disponible en los pools (requisito previo)

Antes de crear volúmenes conviene verificar que existe espacio disponible en el pool:

```bash
javiercruces@FJCD-PC:~$ virsh pool-list --details
 Name      State     Autostart   Persistent   Capacity     Allocation   Available
------------------------------------------------------------------------------------
 default   running   yes         yes          914,78 GiB   100,98 GiB   813,80 GiB
 isos      running   yes         yes          914,78 GiB   100,98 GiB   813,80 GiB
 libvirt   running   yes         yes          914,78 GiB   100,98 GiB   813,80 GiB
```

### Obtener información de los volúmenes de un pool

Para listar los volúmenes de un pool (ej. `default`):

```bash
javiercruces@FJCD-PC:~$ virsh vol-list default
 Name                                   Path
------------------------------------------------------------------------------------------------------
 debian-13.1.0-amd64-netinst.iso        /var/lib/libvirt/images/debian-13.1.0-amd64-netinst.iso
 debian13-base.qcow2                    /var/lib/libvirt/images/debian13-base.qcow2
 debian13-clonacion-completa.qcow2      /var/lib/libvirt/images/debian13-clonacion-completa.qcow2
 debian13-clonacion-enlazada.qcow2      /var/lib/libvirt/images/debian13-clonacion-enlazada.qcow2
 debian13.qcow2                         /var/lib/libvirt/images/debian13.qcow2
 ubuntu-24.04-vm.qcow2                  /var/lib/libvirt/images/ubuntu-24.04-vm.qcow2
 ubuntu-24.04.3-live-server-amd64.iso   /var/lib/libvirt/images/ubuntu-24.04.3-live-server-amd64.iso
 ubuntu-25.04-live-server-amd64.iso     /var/lib/libvirt/images/ubuntu-25.04-live-server-amd64.iso
 ubuntu-25.04-vm.qcow2                  /var/lib/libvirt/images/ubuntu-25.04-vm.qcow2

 ...
```

Si quieres más datos (capacidad, allocation), usa `--details`:

```bash
javiercruces@FJCD-PC:~$ virsh vol-list default --details
 Name                                   Path                                                           Type   Capacity     Allocation
---------------------------------------------------------------------------------------------------------------------------------------
 debian-13.1.0-amd64-netinst.iso        /var/lib/libvirt/images/debian-13.1.0-amd64-netinst.iso        file   783,00 MiB   783,00 MiB
 debian13-base.qcow2                    /var/lib/libvirt/images/debian13-base.qcow2                    file   20,00 GiB    585,61 MiB
 debian13-clonacion-completa.qcow2      /var/lib/libvirt/images/debian13-clonacion-completa.qcow2      file   20,00 GiB    3,04 GiB
 debian13-clonacion-enlazada.qcow2      /var/lib/libvirt/images/debian13-clonacion-enlazada.qcow2      file   20,00 GiB    105,88 MiB
 debian13.qcow2                         /var/lib/libvirt/images/debian13.qcow2                         file   20,00 GiB    2,11 GiB
 ubuntu-24.04-vm.qcow2                  /var/lib/libvirt/images/ubuntu-24.04-vm.qcow2                  file   20,00 GiB    3,32 MiB
 ubuntu-24.04.3-live-server-amd64.iso   /var/lib/libvirt/images/ubuntu-24.04.3-live-server-amd64.iso   file   3,08 GiB     3,08 GiB
 ubuntu-25.04-live-server-amd64.iso     /var/lib/libvirt/images/ubuntu-25.04-live-server-amd64.iso     file   1,88 GiB     1,88 GiB
 ubuntu-25.04-vm.qcow2                  /var/lib/libvirt/images/ubuntu-25.04-vm.qcow2                  file   20,00 GiB    3,32 MiB
 ...
```

Para obtener información de un volumen concreto:

```bash
javiercruces@FJCD-PC:~$ virsh vol-info debian13.qcow2 default
Name:           debian13.qcow2
Type:           file
Capacity:       20,00 GiB
Allocation:     2,11 GiB
```

La definición XML del volumen puede verse con `vol-dumpxml`:

```bash
javiercruces@FJCD-PC:~$ virsh vol-dumpxml debian13.qcow2 default
<volume type='file'>
  <name>debian13.qcow2</name>
  <key>/var/lib/libvirt/images/debian13.qcow2</key>
  <capacity unit='bytes'>21474836480</capacity>
  <allocation unit='bytes'>2265751552</allocation>
  <physical unit='bytes'>21478375424</physical>
  <target>
    <path>/var/lib/libvirt/images/debian13.qcow2</path>
    <format type='qcow2'/>
    <permissions>
      <mode>0600</mode>
      <owner>0</owner>
      <group>0</group>
    </permissions>
    <timestamps>
      <atime>1761395639.089998838</atime>
      <mtime>1760392793.808858769</mtime>
      <ctime>1760392794.101127920</ctime>
      <btime>0</btime>
    </timestamps>
    <compat>1.1</compat>
    <clusterSize unit='B'>65536</clusterSize>
    <features>
      <lazy_refcounts/>
    </features>
  </target>
</volume>
```

### Crear volúmenes con `vol-create-as`

Ejemplo: crear un volumen `raw` de 10G en el pool `default`:

```bash
javiercruces@FJCD-PC:~$ virsh vol-create-as default vdisk-10G.img --format raw 10G
```

Comprobar fichero creado (en pools `dir` el volumen será un fichero en el directorio target del pool, típicamente `/var/lib/libvirt/images` para el pool `default`):

```bash
javiercruces@FJCD-PC:~$ sudo ls -l /var/lib/libvirt/images/
total 10485760
-rw------- 1 root         root 10737418240 oct 26 00:05 vdisk-10G.img
```

Si creas un volumen en `raw`, no tendrás aprovisionamiento ligero (thin provisioning), el fichero ocupará el tamaño completo desde el inicio. Si creas en `qcow2`, la capacidad será lógica y la asignación física crecerá según uso.

Ejemplo de `qcow2`:

```bash
javiercruces@FJCD-PC:~$ virsh vol-create-as --pool default --format qcow2 vdisk-20G.qcow2 20G
```

Asi podemos comprobar que el disco en formato `raw` ocupa todo su tamaño mientras que el `qcow2` solo lo que realmente tiene ocupado.

```bash
javiercruces@FJCD-PC:~$ virsh vol-list default --details
 Name                Path                                        Type   Capacity  Allocation
---------------------------------------------------------------------------------------------
 vdisk-10G.img                          /var/lib/libvirt/images/vdisk-10G.img                          file   10,00 GiB    10,00 GiB
 vdisk-20G.qcow2                        /var/lib/libvirt/images/vdisk-20G.qcow2                        file   20,00 GiB    196,00 KiB

```

### Borrar volúmenes

```bash
javiercruces@FJCD-PC:~$ virsh vol-delete vdisk-10G.img default
```

Esto elimina el volumen del pool. En pools de red o LVM el efecto depende del backend (p. ej. borrado de LUN, eliminación de RBD image, etc.).

### Clonar volúmenes

Para clonar un volumen dentro del mismo pool:

```bash
javiercruces@FJCD-PC:~$ virsh vol-clone --pool default vdisk-20G.qcow2 vdisk-20G-clone.qcow2
```

Al clonar obtendrás una copia que, si es `qcow2`, tendrá aprovisionamiento ligero equivalente.

### Redimensionar volúmenes

Para aumentar o reducir el tamaño de un volumen:

```bash
javiercruces@FJCD-PC:~$ virsh vol-resize --pool default vdisk-20G.qcow2 30G
```

Si el volumen forma parte de una máquina virtual activa, además de redimensionar el volumen desde el host debes redimensionar la partición y el sistema de ficheros dentro del invitado. A continuación se muestran ejemplos para un sistema con una única partición de datos en /dev/vda1 con un sistema de ficheros ext4.

1) Aumentar el volumen (desde el host):

```bash
javiercruces@FJCD-PC:~$ virsh vol-resize --pool default vdisk-20G.qcow2 30G
```

2) Redimensionar dentro del invitado (online, con la VM arrancada)

Si el invitado dispone de cloud-guest-utils (paquete `growpart`) puedes ampliar la partición y el sistema de ficheros en caliente:

```bash
# Conéctate al invitado (por ejemplo: ssh javiercruces@debian13)
javiercruces@debian13:~$ sudo apt update && sudo apt install -y cloud-guest-utils
javiercruces@debian13:~$ sudo growpart /dev/vda 1
javiercruces@debian13:~$ sudo resize2fs /dev/vda1
```

Explicación rápida:
- `growpart /dev/vda 1` extiende la primera partición del disco `/dev/vda` para ocupar el nuevo espacio disponible.
- `resize2fs /dev/vda1` ajusta el tamaño del sistema de ficheros ext4 a la nueva partición.

3) Alternativa si no tienes `growpart` (online, con `parted`)

```bash
javiercruces@debian13:~$ sudo apt install -y parted
javiercruces@debian13:~$ sudo parted /dev/vda --script resizepart 1 100%
javiercruces@debian13:~$ sudo resize2fs /dev/vda1
```



### Sacar y meter datos de un disco

Descargar el contenido de un volumen a un fichero local:

```bash
javiercruces@FJCD-PC:~$ virsh vol-download --pool default vdisk-20G.qcow2 /tmp/vdisk-20G.qcow2
```

Subir el contenido desde un fichero local a un volumen (sobrescribe):

```bash
javiercruces@FJCD-PC:~$ virsh vol-upload --pool default vdisk-20G.qcow2 /tmp/vdisk-20G.qcow2
```

Estas operaciones pueden ser lentas para ficheros grandes; en muchos casos `qemu-img convert` o herramientas del propio backend (rbd, gluster) son más eficientes.


### Asignar un volumen como disco a una VM

Puedes adjuntar un volumen a una VM directamente desde el host sin crear un fichero XML usando `attach-disk`. Ejemplos:

```bash
javiercruces@FJCD-PC:~$ # Adjuntar en caliente (live)
javiercruces@FJCD-PC:~$ virsh attach-disk testguest1 /var/lib/libvirt/images/vdisk-20G.qcow2 vdb --live

javiercruces@FJCD-PC:~$ # Adjuntar persistentemente en la configuración
javiercruces@FJCD-PC:~$ virsh attach-disk --config testguest1 /var/lib/libvirt/images/vdisk-20G.qcow2 vdb

javiercruces@FJCD-PC:~$ # Adjuntar en caliente y persistente a la vez
javiercruces@FJCD-PC:~$ virsh attach-disk --live --config testguest1 /var/lib/libvirt/images/vdisk-20G.qcow2 vdb
```

Explicación y notas:
- `attach-disk` recibe la ruta al fichero de imagen (o al dispositivo del pool) y el nombre del dispositivo objetivo dentro del invitado (p. ej. `vdb`).
- `--live` realiza la operación en caliente en la VM en ejecución; `--config` escribe la entrada en la definición de la VM para que sea persistente al reinicio. Puedes combinar ambas.
- Estos comandos son prácticos cuando conoces la ruta del volumen en el host y el nombre del dispositivo que quieres usar dentro del invitado.

Alternativa: adjuntar mediante un fragmento XML

Si prefieres la vía basada en XML (útil para casos complejos o cuando necesitas especificar atributos avanzados), puedes crear un fragmento XML y usar `attach-device`:

```xml
<disk type='volume' device='disk'>
  <driver name='qemu' type='qcow2'/>
  <source pool='default' volume='vdisk-20G.qcow2'/>
  <target dev='vdb' bus='virtio'/>
</disk>
```

Y adjuntar persistentemente en la configuración:

```bash
javiercruces@FJCD-PC:~$ virsh attach-device --config testguest1 ~/vdisk-20G.xml
```

Dependiendo del tipo de pool, el XML cambia; para operaciones sencillas `attach-disk` suele ser la forma más directa.

Quitar (desasignar) un disco

Si necesitas quitar el disco por su nombre de dispositivo (sin XML), usa `detach-disk`:

```bash
javiercruces@FJCD-PC:~$ virsh detach-disk testguest1 vdb

javiercruces@FJCD-PC:~$ # Eliminar también la entrada persistente:
javiercruces@FJCD-PC:~$ virsh detach-disk --config testguest1 vdb
```

### Referencias

- [Documentación oficial libvirt: Storage pool and volume XML format](https://libvirt.org/storage.html)
- [virsh manpage / vol-* commands](https://libvirt.org/manpages/virsh.html)