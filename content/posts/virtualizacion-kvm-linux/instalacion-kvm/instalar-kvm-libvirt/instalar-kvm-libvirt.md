---
title: "Instalación de KVM en Ubuntu/Debian"
date: 2025-10-13T10:00:00+00:00
description: Aprende a instalar KVM en sistemas Ubuntu/Debian, configurar usuarios y verificar que la instalación sea correcta.
tags: [Virtualizacion,Linux,KVM,VM,Hypervisor,Ubuntu,Debian]
hero: images/virtualizacion-kvm-linux/introduccion-kvm/instalacion-kvm.jpg
---

# Instalación de KVM en Ubuntu/Debian

Para instalar **KVM** en Ubuntu o Debian, se requiere preparar el sistema con los paquetes necesarios, verificar el soporte de virtualización por hardware y autorizar a los usuarios para ejecutar máquinas virtuales. A continuación se detallan los pasos para instalar KVM en Ubuntu 24.04 (Noble Numbat) o Debian recientes.

## Paso 1: Actualizar el sistema

Antes de instalar KVM, actualiza la información de los repositorios de paquetes:

```bash
sudo apt update
```

## Paso 2: Comprobar soporte de virtualización

### 2.1 Verificar compatibilidad del CPU

Comprueba si tu CPU soporta virtualización por hardware:

```bash
egrep -c '(vmx|svm)' /proc/cpuinfo
```

* `vmx` → CPU Intel con VT-x
* `svm` → CPU AMD con AMD-V
* `lm` → soporte de 64 bits

Si el resultado es 0, tu procesador no soporta KVM. Cualquier otro número indica que puedes continuar , ademas indicara el numero de nucleos que tiene tu CPU.

### 2.2 Comprobar aceleración KVM

```bash
sudo kvm-ok
```

Si `kvm-ok` no está disponible, instala el paquete **cpu-checker**:

```bash
sudo apt install cpu-checker -y
```

Luego, vuelve a ejecutar `sudo kvm-ok` para confirmar que el sistema puede usar KVM acelerado por hardware.

```bash
javiercruces@FJCD-PC:~$ sudo kvm-ok
INFO: /dev/kvm exists
KVM acceleration can be used
```

## Paso 3: Instalar paquetes de KVM

Instala los paquetes esenciales para KVM:

```bash
sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils libosinfo-bin virt-install virt-manager virt-viewer libguestfs-tools -y
```

Espera a que se complete la instalación de todos los paquetes.

## Paso 4: Autorizar usuarios

Solo los miembros de los grupos **libvirt** y **kvm** pueden ejecutar máquinas virtuales. Para añadir al usuario actual a estos grupos, usa variables de entorno:

```bash
sudo adduser $USER libvirt
sudo adduser $USER kvm
```

Para que los cambios tengan efecto, cierra sesión y vuelve a iniciar sesión, o ejecuta:

```bash
newgrp libvirt
newgrp kvm
```

## Paso 5: Verificar la instalación

Confirma que KVM se instaló correctamente con **virsh**:

```bash
sudo virsh list --all
```

El comando listará todas las máquinas virtuales activas e inactivas. Si no se han creado VMs todavía, mostrará una lista vacía.

También puedes verificar el estado del servicio de virtualización:

```bash
sudo systemctl status libvirtd
```

Si el servicio no está activo, actívalo con:

```bash
sudo systemctl enable --now libvirtd
```

Con esto, tu sistema Ubuntu/Debian estará listo para ejecutar máquinas virtuales mediante KVM.