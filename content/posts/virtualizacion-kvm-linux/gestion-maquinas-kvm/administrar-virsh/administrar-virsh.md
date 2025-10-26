---
title: "Cómo administrar máquinas virtuales con virsh"
date: 2025-10-16T10:00:00+00:00
description: Guía práctica sobre cómo administrar máquinas virtuales con virsh, la interfaz de línea de comandos de libvirt para KVM.
tags: [KVM,Virtualizacion,Libvirt,Linux,VM,Administracion]
hero: images/virtualizacion-kvm-linux/gestion-vm/gestion-virsh.png
weight: 3
---

# Administración de máquinas virtuales con virsh

`virsh` es una potente herramienta de línea de comandos incluida en **libvirt** que permite gestionar máquinas virtuales y recursos asociados en **KVM**.  
A través de `virsh`, puedes crear, iniciar, detener, modificar y supervisar dominios (máquinas virtuales), así como gestionar redes, volúmenes y pools de almacenamiento.

---

## 1. Gestión de dominios (máquinas virtuales)

| Comando | Descripción |
|----------|-------------|
| `virsh list --all` | Lista todas las máquinas virtuales, activas e inactivas. |
| `virsh start vm_name` | Inicia una máquina virtual previamente definida. |
| `virsh shutdown vm_name` | Apaga una máquina virtual de forma ordenada. |
| `virsh destroy vm_name` | Detiene una máquina virtual de inmediato (similar a apagarla forzosamente). |
| `virsh suspend vm_name` | Suspende la ejecución de la máquina virtual. |
| `virsh resume vm_name` | Reanuda una máquina suspendida. |
| `virsh reboot vm_name` | Reinicia la máquina virtual. |
| `virsh reset vm_name` | Resetea una máquina virtual como si se pulsara el botón de reset físico. |
| `virsh autostart vm_name` | Activa el inicio automático de la VM al arrancar el host. |
| `virsh dominfo vm_name` | Muestra información detallada sobre la VM (estado, UUID, CPU, memoria, etc.). |
| `virsh dumpxml vm_name` | Muestra la definición XML completa de la VM. |
| `virsh edit vm_name` | Abre la definición XML de la VM en un editor para modificarla. |
| `virsh undefine vm_name` | Elimina la definición de una VM sin borrar su disco. |
| `virsh domrename old_name new_name` | Cambia el nombre de una máquina virtual. |

---

## 2. Información y monitorización

| Comando | Descripción |
|----------|-------------|
| `virsh domstate vm_name` | Muestra el estado actual de una VM (`running`, `shut off`, etc.). |
| `virsh domstats vm_name` | Muestra estadísticas de CPU, red y disco en tiempo real. |
| `virsh domblklist vm_name` | Lista los dispositivos de bloque (discos) asociados a una VM. |
| `virsh domblkinfo vm_name vda` | Muestra información detallada sobre un disco virtual. |
| `virsh domiflist vm_name` | Muestra las interfaces de red conectadas a la VM. |
| `virsh domifaddr vm_name` | Muestra las direcciones IP asignadas a las interfaces de red de la VM. |
| `virsh cpu-stats vm_name` | Muestra estadísticas detalladas del uso de CPU por parte de la VM. |
| `virsh dommemstat vm_name` | Muestra estadísticas de uso de memoria de una VM. |
| `virsh console vm_name` | Conecta a la consola de texto de la máquina virtual. |
| `virsh vncdisplay vm_name` | Muestra el puerto VNC asignado a la VM para acceso gráfico. |

---

## 3. Almacenamiento

| Comando | Descripción |
|----------|-------------|
| `virsh pool-list` | Lista todos los pools de almacenamiento. |
| `virsh pool-info pool_name` | Muestra información detallada de un pool. |
| `virsh pool-start pool_name` | Inicia un pool de almacenamiento. |
| `virsh pool-destroy pool_name` | Detiene un pool de almacenamiento. |
| `virsh pool-undefine pool_name` | Elimina la definición del pool. |
| `virsh vol-list pool_name` | Lista los volúmenes (discos) dentro de un pool. |
| `virsh vol-info --pool pool_name vol_name` | Muestra información sobre un volumen. |
| `virsh vol-create-as pool_name vol_name 20G --format qcow2` | Crea un nuevo volumen de 20 GB en formato QCOW2. |
| `virsh vol-delete --pool pool_name vol_name` | Elimina un volumen de un pool. |
| `virsh vol-clone --pool pool_name source_vol new_vol` | Clona un volumen existente. |

---

## 4. Redes virtuales

| Comando | Descripción |
|----------|-------------|
| `virsh net-list --all` | Lista todas las redes virtuales, activas e inactivas. |
| `virsh net-info net_name` | Muestra información detallada de una red. |
| `virsh net-start net_name` | Inicia una red virtual. |
| `virsh net-destroy net_name` | Detiene una red virtual. |
| `virsh net-autostart net_name` | Habilita el inicio automático de una red. |
| `virsh net-edit net_name` | Edita la configuración XML de una red. |
| `virsh net-dumpxml net_name` | Muestra la definición XML de una red. |
| `virsh net-update net_name` | Actualiza parámetros de una red sin necesidad de reiniciarla. |
| `virsh net-dhcp-leases net_name` | Muestra las direcciones IP entregadas por DHCP en una red. |

---

## 5. Snapshots y backups

| Comando | Descripción |
|----------|-------------|
| `virsh snapshot-list vm_name` | Lista los snapshots disponibles de una VM. |
| `virsh snapshot-create-as vm_name snapshot_name "Descripción"` | Crea un snapshot con nombre y descripción. |
| `virsh snapshot-revert vm_name snapshot_name` | Revierte la VM al estado guardado en un snapshot. |
| `virsh snapshot-delete vm_name snapshot_name` | Elimina un snapshot específico. |
| `virsh backup-begin vm_name --target /backup/` | Inicia una copia de seguridad de los discos de la VM. |
| `virsh backup-dumpxml vm_name` | Muestra información XML sobre una tarea de backup en curso. |

---

## 6. Migración y guardado de estado

| Comando | Descripción |
|----------|-------------|
| `virsh save vm_name /ruta/estado.save` | Guarda el estado actual de una VM en un archivo. |
| `virsh restore /ruta/estado.save` | Restaura una VM desde un archivo guardado. |
| `virsh migrate --live vm_name qemu+ssh://host_destino/system` | Migra una VM en ejecución a otro host mediante SSH. |

---

## 7. Información del host e hipervisor

| Comando | Descripción |
|----------|-------------|
| `virsh nodeinfo` | Muestra información sobre la CPU, memoria y arquitectura del host. |
| `virsh capabilities` | Muestra las capacidades del hipervisor (CPU, virtualización, etc.). |
| `virsh domcapabilities` | Muestra las capacidades soportadas por las VMs. |
| `virsh version` | Muestra la versión de libvirt y del hipervisor. |
| `virsh hostname` | Muestra el nombre del host que ejecuta libvirt. |
| `virsh uri` | Muestra la URI de conexión al hipervisor. |

---

## 8. Consejos adicionales

- Para ejecutar comandos sin privilegios, puedes usar `--connect qemu:///session` o añadir tu usuario a los grupos libvirt y kvm.
- Si gestionas VMs del sistema, utiliza `sudo virsh --connect qemu:///system`.
- Usa `virsh help <sección>` para ver todos los comandos disponibles en un grupo (por ejemplo, `virsh help domain`).
- Todos los cambios realizados mediante `virsh edit` se guardan directamente en los XML de configuración en `/etc/libvirt/qemu/`.

---