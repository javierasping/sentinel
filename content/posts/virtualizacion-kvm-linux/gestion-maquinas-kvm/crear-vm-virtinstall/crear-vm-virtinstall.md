---
title: "Cómo crear una máquina virtual con virt-install"
date: 2025-10-13T10:00:00+00:00
description: Aprende a crear máquinas virtuales en KVM usando la herramienta de línea de comandos virt-install en sistemas Ubuntu/Debian.
tags: [Virtualizacion,Linux,KVM,VM,Hypervisor,Ubuntu,Debian]
hero: images/virtualizacion-kvm-linux/gestion-vm/instalacion-virsh.png
weight: 1
---

Después de instalar **KVM** en tu sistema Ubuntu o Debian, el siguiente paso es crear una máquina virtual utilizando la herramienta de línea de comandos **virt-install**.

## Comprobar máquinas virtuales existentes

Antes de crear una nueva VM, verifica que no haya máquinas virtuales activas:

```bash
sudo virsh list --all
```

Si no hay máquinas, la lista estará vacía.

## Crear una máquina virtual con virt-install

El comando `virt-install` permite especificar todas las propiedades de la VM. Por ejemplo:

> [!NOTE]  
> Recuerda descargar la iso del sistema operativo que quieres instalar , te recomiendo que la guardes en /var/lib/libvirt/images/
que es el directorio por defecto donde se guardan discos e imágenes.

```bash
# Ejemplo para usar una iso descargada en local

virt-install --connect qemu:///system \
    --name ubuntu-24.04-vm \
    --virt-type kvm --hvm --os-variant=ubuntu24.04 \
    --ram 4096 --vcpus 2 --network network=default \
    --disk pool=default,size=20,bus=virtio,format=qcow2 \
    --cdrom /var/lib/libvirt/images/ubuntu-24.04.3-live-server-amd64.iso \
    --boot uefi,cdrom,hd \
    --noautoconsole
```

### Explicación de los parámetros

- `--name vm-test`  
  Nombre de la máquina virtual.

- `--virt-type kvm`  
  Define que se utilizará KVM como hypervisor.

- `--hvm`  
  Habilita la funcionalidad completa de hardware-assisted virtualization (HVM).

- `--os-variant=ubuntu25.04`  
  Optimiza la configuración de la VM según la variante del sistema operativo.

> [!NOTE]  
> Se puede obtener la lista completa usando el comando `osinfo-query os`.

- `--ram 2048`  
  Asigna 2048 MB de memoria RAM a la VM.

- `--vcpus 2`  
  Define 2 núcleos virtuales para la VM.

- `--network network=default`  
  Conecta la VM a la red por defecto del host (NAT) usando libvirt.

- `--graphics vnc,password=remotevnc,listen=0.0.0.0`  
  Configura la consola gráfica vía VNC con contraseña y escucha en todas las interfaces de red.

- `--disk pool=default,size=20,bus=virtio,format=qcow2`  
  Crea un disco de 20 GB en el pool de almacenamiento por defecto usando el bus `virtio` y el formato `QCOW2`.

- `--cdrom /home/$USER/isos/ubuntu-25.04-server.iso`  
  Especifica la ISO del sistema operativo que se va a instalar.

- `--noautoconsole`  
  Evita que se abra automáticamente la consola de la VM tras la creación.

- `--boot cdrom,hd`  
  Establece el orden de arranque, primero desde CD-ROM y luego desde disco duro.


## Validar la creación de la VM

Una vez creada la VM, verifica que esté en ejecución:

```bash
javiercruces@FJCD-PC:~$ sudo virsh list
 Id   Name              State
---------------------------------
 1    ubuntu-24.04-vm   running

# Recuerda que si tu usuario forma parte del grupo libvirt y kvm no necesitaras usar sudo .
javiercruces@FJCD-PC:~$ virsh list
 Id   Name              State
---------------------------------
 1    ubuntu-24.04-vm   running

```

La salida mostrará la VM en estado `running` si se ha iniciado correctamente.

## Conexión a la VM

Para conectarte a la VM de manera gráfica, puedes usar **virt-viewer**. Ten en cuenta que si tu maquina no tiene interfaz gráfica no podrás usar este comando .

```bash
sudo virt-viewer ubuntu-24.04-vm &
```

Si configuraste un password para VNC, se te pedirá al conectar.

## Obtener la IP de la VM

Puedes obtener la dirección IP asignada a la VM con:

```bash
$ virsh domifaddr ubuntu-24.04-vm
 Name       MAC address          Protocol     Address
-------------------------------------------------------------------------------
 vnet10     52:54:00:18:7e:6b    ipv4         192.168.122.117/24
```

Esto muestra las interfaces de red y las IPs correspondientes, permitiéndote conectar vía SSH o VNC desde el host , para proceder con la instalación del Sistema operativo .
