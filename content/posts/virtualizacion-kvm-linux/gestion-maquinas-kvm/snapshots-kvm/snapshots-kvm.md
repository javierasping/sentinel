---
title: "Cómo crear y gestionar snapshots en KVM"
date: 2025-10-17T10:00:00+00:00
description: Guía práctica y detallada para crear, listar, revertir y eliminar snapshots de máquinas virtuales en KVM/libvirt, incluyendo snapshots internos/externos, con memoria y disco, quiesce con qemu-guest-agent y limpieza con blockcommit.
tags: [KVM,Virtualizacion,Libvirt,Linux,VM,Snapshots]
hero: images/virtualizacion-kvm-linux/gestion-vm/snapshots.png
weight: 6
---

# Snapshots en KVM/libvirt: cómo crearlos y gestionarlos

Los snapshots (instantáneas) permiten capturar el estado de una máquina virtual en un momento concreto para poder volver atrás si algo sale mal (actualizaciones, cambios arriesgados, pruebas). En KVM con libvirt tenemos dos familias principales:

- Snapshots internos: el contenido del snapshot se almacena dentro del propio fichero qcow2. Suelen requerir la VM apagada y sólo funcionan con almacenamiento qcow2 (no raw, LVM, etc.).
- Snapshots externos: crean ficheros overlay (qcow2) aparte; son los más usados para snapshots en caliente (VM encendida). Permiten flujos más flexibles y se pueden consolidar después (blockcommit).

Además, un snapshot puede ser:

- De disco solamente (lo más común): guarda el estado del/los discos.
- Con memoria: incluye el contenido de RAM y estado de CPU para reanudar exactamente como estaba (más pesado y lento).

Recomendación general:

- Para snapshots en caliente, usa snapshots externos con `--disk-only` y, si es posible, `--quiesce` con qemu-guest-agent.
- Limita la profundidad de la cadena de overlays; consolida pronto con blockcommit para evitar degradación de rendimiento.
- No uses snapshots como sustituto de copias de seguridad completas.

---

## Requisitos y comprobaciones rápidas

```bash
# Ver los discos adjuntos a la VM
virsh domblklist debian13

# Comprobar formato del disco (importante para internos)
qemu-img info /var/lib/libvirt/images/debian13.qcow2

# Comprobar si el agente invitado está operativo (para --quiesce)
virsh domfsinfo debian13            # requiere qemu-guest-agent
virsh qemu-agent-command debian13 '{"execute":"guest-info"}' --timeout 5
```

Notas:

- Snapshots internos requieren qcow2 y habitualmente VM apagada.
- `--quiesce` necesita qemu-guest-agent instalado y configurado en el invitado.

---

## Crear un snapshot externo (recomendado en caliente)

Este es el flujo más habitual antes de una actualización en producción.

```bash
# Snapshot de disco en caliente con metadatos de libvirt
virsh snapshot-create-as \
	--domain debian13 \
	--name snap-pre-upgrade \
	--description "Antes de apt full-upgrade" \
	--disk-only \
	--atomic \
	--quiesce \
	--live

# Si no tienes qemu-guest-agent, omite --quiesce
# virsh snapshot-create-as --domain debian13 --name snap-pre-upgrade \
#   --description "Antes de apt full-upgrade" --disk-only --atomic --live
```

Verifica los overlays creados y la metadata del snapshot:

```bash
virsh snapshot-list debian13
virsh domblklist debian13
```

Salida típica de `domblklist` tras un snapshot externo:

```
 Target   Source
----------------------------------------------
 vda      /var/lib/libvirt/images/debian13-snap-pre-upgrade.qcow2
```

Eso indica que ahora se escribe en el overlay (el fichero base queda protegido).

---

## Crear un snapshot interno (VM apagada, qcow2)

Útil para escenarios simples con almacenamiento qcow2 y sin necesidad de en caliente.

```bash
# Apagar la VM
virsh shutdown debian13 && virsh domstate debian13

# Crear snapshot interno explícito del disco vda
virsh snapshot-create-as \
	--domain debian13 \
	--name snap-interno \
	--description "Antes de cambiar fstab" \
	--diskspec vda,snapshot=internal

# Arrancar de nuevo si procede
virsh start debian13
```

Para internos, también puedes usar `qemu-img snapshot` con la VM apagada, pero se recomienda `virsh` para mantener metadatos coherentes en libvirt.

---

## Listar, ver información y snapshot actual

```bash
# Listar snapshots de la VM
virsh snapshot-list debian13

# Ver información de un snapshot concreto
virsh snapshot-info debian13 --snapshotname snap-pre-upgrade

# Snapshot actual (al que apunta el estado presente)
virsh snapshot-current debian13
```

---

## Revertir a un snapshot

Con snapshots con memoria puedes reanudar exactamente el estado; con snapshots sólo de disco es más seguro revertir con la VM apagada.

```bash
# Opción conservadora para snapshots de disco: apagar, revertir y arrancar
virsh shutdown debian13
virsh snapshot-revert debian13 snap-pre-upgrade
virsh start debian13

# Si el snapshot incluye memoria, puedes indicar el estado tras revertir
# virsh snapshot-revert debian13 snap-con-memoria --running   # reanudar
# virsh snapshot-revert debian13 snap-con-memoria --paused    # pausada
```

Consejo: después de revertir, valida aplicaciones y sistemas de archivos.

---

## Eliminar snapshots

```bash
# Eliminar un snapshot concreto (metadatos en libvirt)
virsh snapshot-delete debian13 --snapshotname snap-pre-upgrade

# Eliminar un snapshot y sus descendientes
# virsh snapshot-delete debian13 --snapshotname snap-pre-upgrade --children
```

Importante: En snapshots externos, borrar la metadata NO consolida automáticamente los overlays. Para volver a una cadena sencilla, hay que usar blockcommit.

---

## Limpiar overlays (consolidar) con blockcommit

Tras probar que todo está bien, conviene consolidar el overlay en el disco base para evitar cadenas largas de snapshots que penalizan rendimiento.

```bash
# Identificar el target (por ejemplo vda)
virsh domblklist debian13

# Iniciar el blockcommit en caliente y pivotar al terminar
virsh blockcommit debian13 vda --active --verbose --pivot

# Ver el estado del job (opcional)
virsh blockjob debian13 vda --info
```

Después del `--pivot`, la VM vuelve a escribir directamente en el fichero base y el overlay puede eliminarse si no queda referenciado.

---

## Demostración rápida (idea de flujo)

```bash
# 1) Crear snapshot externo antes de cambios
virsh snapshot-create-as --domain debian13 --name snap-demo --description "Antes de pruebas" --disk-only --atomic --live

# 2) (Dentro de la VM) aplicar cambios
# sudo apt update && sudo apt -y full-upgrade

# 3) Si algo falla, revertir
virsh shutdown debian13
virsh snapshot-revert debian13 snap-demo
virsh start debian13

# 4) Si todo fue bien y no necesitas el snapshot, consolidar y limpiar
virsh blockcommit debian13 vda --active --verbose --pivot
virsh snapshot-delete debian13 --snapshotname snap-demo
```

---

## Quiesce con qemu-guest-agent (mejores snapshots)

Para reducir riesgo de inconsistencias (especialmente en bases de datos), usa `--quiesce` con el agente invitado.

En el invitado:

```bash
# Debian/Ubuntu
sudo apt install -y qemu-guest-agent

# RHEL/CentOS/Rocky/Fedora
sudo dnf install -y qemu-guest-agent

# Asegúrate de que el servicio está activo
sudo systemctl enable --now qemu-guest-agent
```

En la definición de la VM (ya suele venir en plantillas modernas), debe existir el canal `virtio` del agente. Verifica:

```bash
virsh domfsinfo debian13    # si responde, el agente funciona
```

Luego crea snapshots con `--quiesce`.

---

## Seleccionar discos y exclusiones

Puedes limitar el snapshot a un disco concreto o excluir alguno:

```bash
# Snapshot externo sólo del disco vdb (útil para datos)
virsh snapshot-create-as \
	--domain debian13 \
	--name snap-datos \
	--description "Sólo datos" \
	--disk-only --atomic --live \
	--diskspec vdb,snapshot=external

# Excluir un disco efímero (ej. swap)
# --diskspec vdc,snapshot=no
```

---

## Problemas comunes y cómo resolverlos

- Falla `--quiesce`: instala y habilita qemu-guest-agent dentro del invitado y comprueba `virsh domfsinfo`.
- Almacenamiento no compatible: snapshots internos requieren qcow2; en raw/LVM/ceph usa externos.
- Snapshots con memoria muy pesados: pueden tardar y ocupar mucho; evalúa si realmente necesitas memoria.
- Cadena de overlays profunda: impacto en I/O; consolida con blockcommit pronto.
- Revertir en caliente un snapshot de sólo disco: puede corromper datos; apaga antes de revertir.
- No sustituyen backups: los snapshots no protegen contra fallos del host o corrupción silenciosa prolongada.

---

## Referencias

- [curso_virtualizacion_linux — GitHub](https://github.com/josedom24/curso_virtualizacion_linux)
- [Domain snapshots (libvirt) - Visión general](https://libvirt.org/formatsnapshot.html)
- [virsh - comandos de snapshots](https://libvirt.org/manpages/virsh.html#domain-snapshots-commands)
- [Blockcommit (libvirt) - Consolidación de snapshots externos](https://libvirt.org/kbase/blockcommit.html)
- [qemu-img snapshot - QEMU Documentation](https://www.qemu.org/docs/master/tools/qemu-img.html#snapshot-commands)
- [QEMU Guest Agent - Wiki](https://wiki.qemu.org/Features/GuestAgent)
