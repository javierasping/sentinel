---
title: "Componentes de una máquina virtual en KVM"
date: 2025-10-13T10:00:00+00:00
description: Aprende sobre los componentes fundamentales de una máquina virtual en KVM y cómo obtener información detallada del hipervisor usando virsh.
tags: [Virtualizacion,Linux,KVM,VM,Hypervisor,Ubuntu,Debian]
hero: images/virtualizacion-kvm-linux/introduccion-kvm/componentes-vm.jpg
---

# Componentes de una máquina virtual en KVM

En **KVM (Kernel-based Virtual Machine)**, una máquina virtual está compuesta por varios elementos que interactúan entre sí para emular un entorno de hardware completo. Comprender cada componente te ayudará a administrar, depurar y optimizar tus VMs de forma más eficiente.

## 1. Componentes principales

| Componente | Descripción |
|-------------|--------------|
| **CPU virtual (vCPU)** | Núcleos asignados desde el host físico al guest. Se definen con `--vcpus` al crear la VM. |
| **Memoria RAM** | Cantidad de memoria asignada. Se configura con `--ram` o puede ajustarse en caliente con `virsh setmem`. |
| **Disco virtual** | Archivo de almacenamiento (`.qcow2`, `.raw`, etc.) usado como disco del guest. Se gestiona con `virsh vol-*` o `virt-manager`. |
| **Interfaz de red** | Conexión virtual (generalmente `virtio` o `e1000`) unida a una red libvirt (`default`, `br0`, etc.). |
| **Dispositivo gráfico / consola** | VNC, SPICE o modo texto (sin consola gráfica). Controlable con `--graphics` o `virsh vncdisplay`. |
| **Firmware / BIOS / UEFI** | Define el modo de arranque (BIOS tradicional o UEFI con OVMF). |
| **Dispositivos adicionales** | CD-ROM, controladores USB, canales seriales, interfaces de sonido, etc. |

## 2. Comandos esenciales para obtener información de una VM

Una vez creada la VM, puedes usar `virsh` para inspeccionar y administrar todos sus detalles.

### Listar máquinas virtuales

```bash
javiercruces@FJCD-PC:~
$ virsh list --all
 Id   Name              State
----------------------------------
 9    debian13          running
 -    ubuntu-24.04-vm   shut off
```

Muestra todas las VMs, tanto activas como inactivas.

### Ver información general de una VM

```bash
javiercruces@FJCD-PC:~
$ virsh dominfo debian13
Id:             9
Name:           debian13
UUID:           196c28a6-4821-43c8-b862-1feea5995683
OS Type:        hvm
State:          running
CPU(s):         2
CPU time:       20,4s
Max memory:     2097152 KiB
Used memory:    2097152 KiB
Persistent:     yes
Autostart:      disable
Managed save:   no
Security model: apparmor
Security DOI:   0
Security label: libvirt-196c28a6-4821-43c8-b862-1feea5995683 (enforcing)
```

### Ver configuración XML completa de la VM

```bash
virsh dumpxml nombre_vm
```

Este comando muestra toda la definición interna de la VM: discos, red, CPU, firmware, etc.
Ideal para realizar copias de configuración o replicar una máquina.

Guardar la definición:
```bash
virsh dumpxml nombre_vm > nombre_vm.xml
```

### Información sobre los discos de la VM

```bash
$ virsh domblklist debian13
 Target   Source
--------------------------------------------------
 vda      /var/lib/libvirt/images/debian13.qcow2
 sda      -
```

Para obtener detalles de un disco:
```bash
javiercruces@FJCD-PC:~
$ virsh domblkinfo debian13 vda --human
Capacity:       20,000 GiB
Allocation:     2,110 GiB
Physical:       20,003 GiB
```

### Ver interfaces de red y direcciones IP

```bash
javiercruces@FJCD-PC:~
$ virsh domiflist debian13
 Interface   Type      Source    Model    MAC
-------------------------------------------------------------
 vnet8       network   default   virtio   52:54:00:8d:ef:f0
```

Para ver la IP asignada por DHCP:
```bash
$ virsh domifaddr debian13
 Name       MAC address          Protocol     Address
-------------------------------------------------------------------------------
 vnet8      52:54:00:8d:ef:f0    ipv4         192.168.122.8/24
 -          -                    ipv4         192.168.122.9/24
```

### Estadísticas en tiempo real

CPU y memoria:
```bash
javiercruces@FJCD-PC:~ 
$ virsh domstats debian13
Domain: 'debian13'
  state.state=1
  state.reason=1
  cpu.time=22002276000
  cpu.user=17092323000
  cpu.system=4909952000
  cpu.cache.monitor.count=0
  cpu.haltpoll.success.time=39199780
  cpu.haltpoll.fail.time=77700049
  balloon.current=2097152
  balloon.maximum=2097152
```

Tráfico de red y uso de disco:
```bash
$ virsh domstats --interface --block  debian13
Domain: 'debian13'
  net.count=1
  net.0.name=vnet8
  net.0.rx.bytes=95541
  net.0.rx.pkts=970
  net.0.rx.errs=0
  net.0.rx.drop=0
  net.0.tx.bytes=2792
  net.0.tx.pkts=35
  net.0.tx.errs=0
  net.0.tx.drop=0
  block.count=2
  block.0.name=vda
  block.0.path=/var/lib/libvirt/images/debian13.qcow2
  block.0.backingIndex=2
  block.0.rd.reqs=4303
  block.0.rd.bytes=126719488
  block.0.rd.times=56885760
  block.0.wr.reqs=550
  block.0.wr.bytes=10887680
  block.0.wr.times=53350513
  block.0.fl.reqs=124
  block.0.fl.times=59918268
  block.0.allocation=3265593344
  block.0.capacity=21474836480
  block.0.physical=2265624576
  block.1.name=sda
  block.1.rd.reqs=19
  block.1.rd.bytes=352
  block.1.rd.times=33044
  block.1.wr.reqs=0
  block.1.wr.bytes=0
  block.1.wr.times=0
  block.1.fl.reqs=0
  block.1.fl.times=0
```

### Ver consola o pantalla de la VM

Consola de texto (serie):
```bash
virsh console nombre_vm
```

VNC (si está habilitado):
```bash
virsh vncdisplay nombre_vm
```

### Consultar capacidades del host y del hipervisor

Información del nodo (host):
```bash
virsh nodeinfo
```

Información sobre capacidades:
```bash
virsh capabilities
```

Capacidades específicas de VMs:
```bash
virsh domcapabilities
```

### Obtener información sobre almacenamiento

Listar pools:
```bash
virsh pool-list
```

Ver detalles de un pool:
```bash
virsh pool-info default
```

Listar volúmenes del pool:
```bash
virsh vol-list default
```

### Diagnóstico y depuración

Ver eventos en tiempo real:
```bash
virsh event --domain nombre_vm
```

Obtener logs detallados:
```bash
journalctl -u libvirtd -f
```

## 3. Otros comandos útiles

| Comando | Descripción |
|----------|-------------|
| `virsh domstate nombre_vm` | Estado actual de la VM (`running`, `paused`, `shut off`, etc.) |
| `virsh start nombre_vm` / `virsh shutdown nombre_vm` | Iniciar o apagar la VM |
| `virsh suspend nombre_vm` / `virsh resume nombre_vm` | Pausar y reanudar |
| `virsh autostart nombre_vm` | Habilitar inicio automático al arrancar el host |
| `virsh snapshot-list nombre_vm` | Ver snapshots existentes |
| `virsh domrename old new` | Renombrar una VM |