---
title: "Clonar y renombrar máquinas virtuales en KVM"
date: 2025-10-16T12:00:00+00:00
description: Aprende a clonar y renombrar máquinas virtuales en KVM usando virt-clone, virt-sysprep y virt-customize para crear plantillas reutilizables.
tags: [KVM,Virtualizacion,Libvirt,Linux,VM,Clonacion]
hero: images/virtualizacion-kvm-linux/gestion-vm/hacer-clones.png
weight: 4
---

# Clonar y renombrar máquinas virtuales en KVM

Una de las ventajas de la virtualización es la capacidad de clonar máquinas virtuales para crear entornos homogéneos rápidamente. Sin embargo, cuando clonamos una VM que contiene un sistema operativo, el clon hereda identificadores únicos como el **machine ID**, direcciones **MAC**, claves **SSH** de host, etc., que deberían ser únicos para cada máquina.

En esta guía veremos cómo:

- Clonar máquinas virtuales con `virt-clone`
- Generalizar clones con `virt-sysprep`
- Personalizar nuevas instancias con `virt-customize`
- Renombrar máquinas virtuales con `virsh domrename`
- Solucionar problemas comunes tras la clonación

---

## Requisitos previos

Asegúrate de tener instalados los siguientes paquetes:

```bash
# Debian/Ubuntu
sudo apt install libguestfs-tools virtinst

# RHEL/Fedora/AlmaLinux
sudo dnf install libguestfs-tools virt-install
```

**Paquetes clave:**

- `virt-clone`: Herramienta para clonar máquinas virtuales (incluida en `virtinst`)
- `virt-sysprep`: Herramienta para generalizar VMs (incluida en `libguestfs-tools`)
- `virt-customize`: Herramienta para personalizar VMs sin arrancarlas (incluida en `libguestfs-tools`)

---

## 1. Preparar la máquina virtual base

Antes de clonar, es recomendable preparar una **máquina de referencia** con toda la configuración base que necesites (paquetes instalados, usuarios, configuración de red básica, etc.).

En nuestro ejemplo, usaremos una VM llamada `debian13` como máquina base.

### Apagar la máquina virtual

Antes de clonarla, debemos apagarla:

```bash
virsh shutdown debian13
```

Verifica que esté completamente apagada:

```bash
virsh list --all
```

Salida esperada:
```
 Id   Name              State
----------------------------------
 -    debian13          shut off
```

---

## 2. Clonar la máquina virtual con virt-clone

`virt-clone` crea una copia completa de una máquina virtual, incluyendo su configuración XML y sus discos virtuales.

### Opción 1: Clonación automática (nombre de disco generado)

Puedes usar `--auto-clone` para que `virt-clone` genere automáticamente el nombre del disco añadiendo el sufijo `-clone`:

```bash
virt-clone --original debian13 --name debian13-clone --auto-clone
```

Salida esperada:
```
Allocating 'debian13-clone.qcow2'    | 20 GB  00:00:05

Clone 'debian13-clone' created successfully.
```

### Opción 2: Especificar nombre de disco personalizado

Para tener más control sobre el nombre del disco, usa el parámetro `--file`:

```bash
virt-clone --original debian13 \
	--name debian-template \
	--file /var/lib/libvirt/images/debian-template.qcow2
```

Salida esperada:
```
Allocating 'debian-template.qcow2'   | 20 GB  00:00:05

Clone 'debian-template' created successfully.
```

### Clonar múltiples discos

Si tu VM tiene varios discos, puedes especificar múltiples parámetros `--file`:

```bash
virt-clone --original debian13 \
	--name debian-template \
	--file /var/lib/libvirt/images/debian-template-disk1.qcow2 \
	--file /var/lib/libvirt/images/debian-template-disk2.qcow2
```

---

## 3. Renombrar máquinas virtuales con virsh domrename

Puedes cambiar el nombre de una VM fácilmente con `virsh domrename`:

```bash
virsh domrename debian13-clone debian-base-image
```

Salida esperada:
```
Domain successfully renamed
```

Verifica el cambio:

```bash
virsh list --all
```

Salida:
```
 Id   Name                State
-----------------------------------
 -    debian13            shut off
 -    debian-base-image   shut off
 -    debian-template     shut off
```

> **Nota:** El comando `virsh domrename` solo cambia el nombre de la VM en libvirt, **no renombra el archivo de disco**. Si deseas renombrar también el disco, hazlo manualmente y luego edita la configuración XML con `virsh edit`.

---

## 4. Generalizar la VM con virt-sysprep

`virt-sysprep` elimina configuraciones específicas de la máquina para convertirla en una **plantilla reutilizable**. Esta herramienta está inspirada en la utilidad `sysprep` de Microsoft Windows.

### ¿Qué hace virt-sysprep?

`virt-sysprep` realiza múltiples operaciones de limpieza automáticamente:

- Elimina el **machine-id** y lo regenerará en el próximo arranque
- Borra las **claves SSH de host** (se regeneran automáticamente o manualmente)
- Limpia el **historial de comandos** (bash_history)
- Elimina las **direcciones MAC** fijas
- Borra **logs del sistema**
- Limpia la **caché de paquetes**
- Elimina **archivos temporales**
- Y mucho más...

### Uso básico de virt-sysprep

```bash
sudo virt-sysprep -d debian-template
```

Salida (fragmento):
```
[   0.0] Examining the guest ...
[   5.2] Performing "abrt-data" ...
[   5.2] Performing "backup-files" ...
[   5.3] Performing "bash-history" ...
[   5.3] Performing "machine-id" ...
[   5.3] Performing "net-hwaddr" ...
[   5.3] Performing "ssh-hostkeys" ...
[   5.4] Performing "tmp-files" ...
[   5.4] Performing "utmp" ...
[   5.5] Setting a random seed
[   5.5] Setting the machine ID in /etc/machine-id
```

### virt-sysprep con opciones adicionales

Puedes establecer el **hostname** y la **contraseña de root** durante la generalización:

```bash
sudo virt-sysprep -d debian-template \
	--hostname debian-template \
	--root-password password:MySecurePassword123!
```

### Opciones útiles de virt-sysprep

| Opción | Descripción |
|--------|-------------|
| `--hostname NOMBRE` | Establece el nombre del host |
| `--root-password password:PASS` | Define la contraseña de root |
| `--firstboot SCRIPT` | Ejecuta un script en el primer arranque |
| `--operations LISTA` | Especifica qué operaciones realizar (por defecto, todas) |
| `--enable OPERACIONES` | Habilita operaciones específicas |
| `--disable OPERACIONES` | Deshabilita operaciones específicas |

Ejemplo deshabilitando la eliminación de claves SSH:

```bash
sudo virt-sysprep -d debian-template --operations all,-ssh-hostkeys
```

---

## 5. Crear nuevas VMs a partir de la plantilla

Una vez que tienes una **machine image** generalizada, puedes crear múltiples instancias rápidamente:

```bash
virt-clone --original debian-template \
	--name vm-debian-01 \
	--file /var/lib/libvirt/images/vm-debian-01.qcow2
```

```bash
virt-clone --original debian-template \
	--name vm-debian-02 \
	--file /var/lib/libvirt/images/vm-debian-02.qcow2
```

Verifica las VMs creadas:

```bash
virsh list --all
```

---

## 6. Personalizar VMs con virt-customize

`virt-customize` permite modificar una VM **sin arrancarla**, lo que es ideal para personalizar clones rápidamente.

### Ejemplo básico: Establecer hostname y contraseña

```bash
sudo virt-customize -d vm-debian-01 \
	--hostname vm-debian-01 \
	--password usuario:password:MyPassword123!
```

Salida:
```
[   0.0] Examining the guest ...
[   3.1] Setting a random seed
[   3.1] Setting the hostname: vm-debian-01
[   4.2] Setting passwords
[   5.0] Finishing off
```

### Opciones avanzadas de virt-customize

```bash
sudo virt-customize -d vm-debian-02 \
	--hostname vm-debian-02 \
	--root-password password:RootPass123! \
	--password admin:password:AdminPass123! \
	--ssh-inject admin:file:/home/user/.ssh/id_rsa.pub \
	--run-command 'apt update && apt install -y nginx' \
	--timezone Europe/Madrid \
	--run-command 'systemctl enable nginx'
```

### Tabla de opciones útiles

| Opción | Descripción |
|--------|-------------|
| `--hostname NOMBRE` | Establece el hostname |
| `--password USER:password:PASS` | Define contraseña de usuario |
| `--ssh-inject USER:file:CLAVE.pub` | Inyecta clave SSH pública |
| `--run-command 'COMANDO'` | Ejecuta un comando dentro de la VM |
| `--install PAQUETES` | Instala paquetes (separados por coma) |
| `--timezone ZONA` | Establece la zona horaria |
| `--update` | Actualiza todos los paquetes |
| `--selinux-relabel` | Reestablece etiquetas SELinux |

### Personalización con script

Puedes ejecutar un script completo:

```bash
sudo virt-customize -d vm-debian-01 \
	--upload /path/to/config.sh:/tmp/config.sh \
	--run-command 'bash /tmp/config.sh' \
	--delete /tmp/config.sh
```

---

## 7. Problemas comunes y soluciones

### Problema 1: Error al conectar por SSH - "Connection refused"

**Causa:** Las claves SSH de host fueron eliminadas por `virt-sysprep`.

**Síntomas:** Al revisar el estado del servicio SSH dentro de la VM:

```bash
sudo systemctl status sshd
```

Verás errores como:
```
sshd[387]: error: Could not load host key: /etc/ssh/ssh_host_rsa_key
sshd[387]: error: Could not load host key: /etc/ssh/ssh_host_ecdsa_key
sshd[387]: error: Could not load host key: /etc/ssh/ssh_host_ed25519_key
sshd[387]: fatal: No supported key exchange algorithms [preauth]
```

**Solución 1:** Regenerar todas las claves SSH automáticamente:

```bash
sudo ssh-keygen -A
sudo systemctl restart sshd
```

Salida:
```
ssh-keygen: generating new host keys: RSA DSA ECDSA ED25519
```

**Solución 2:** Regenerar claves manualmente una por una:

```bash
sudo ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa
sudo ssh-keygen -f /etc/ssh/ssh_host_ecdsa_key -N '' -t ecdsa
sudo ssh-keygen -f /etc/ssh/ssh_host_ed25519_key -N '' -t ed25519
sudo systemctl restart sshd
```

**Solución 3:** Evitar que virt-sysprep elimine las claves SSH:

```bash
sudo virt-sysprep -d debian-template --operations all,-ssh-hostkeys
```

> **Advertencia:** Si conservas las claves SSH en la plantilla, todas las VMs clonadas compartirán las mismas claves de host, lo cual es un riesgo de seguridad. Solo hazlo en entornos de laboratorio.

### Problema 2: "WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!"

**Causa:** Las claves SSH del host cambiaron y el cliente tiene la clave antigua en `~/.ssh/known_hosts`.

**Solución:** Eliminar la entrada antigua del archivo `known_hosts`:

```bash
ssh-keygen -f "/home/usuario/.ssh/known_hosts" -R "192.168.122.50"
```

O editar manualmente el archivo `~/.ssh/known_hosts` y eliminar la línea correspondiente.

### Problema 3: Direcciones MAC duplicadas

**Causa:** Al clonar sin `virt-sysprep`, las VMs pueden tener la misma dirección MAC.

**Solución:** `virt-clone` genera automáticamente nuevas direcciones MAC. Si tienes problemas, edita la VM:

```bash
virsh edit vm-debian-01
```

Busca la sección `<interface>` y elimina o modifica la línea `<mac address='...'/>`. Libvirt generará una nueva al arrancar.

### Problema 4: machine-id duplicado

**Causa:** El archivo `/etc/machine-id` es idéntico en todas las VMs clonadas.

**Solución:** `virt-sysprep` ya se encarga de esto. Si lo hiciste manualmente, regenera el machine-id:

```bash
sudo rm /etc/machine-id
sudo systemd-machine-id-setup
```

---

## 8. Workflow completo recomendado

Aquí tienes un flujo de trabajo completo para crear y desplegar múltiples VMs:

### Paso 1: Crear y configurar la VM base

```bash
# Crear VM base (suponiendo que ya la tienes)
virsh list --all
```

### Paso 2: Apagar y clonar

```bash
virsh shutdown debian13
virt-clone --original debian13 \
	--name debian-template \
	--file /var/lib/libvirt/images/debian-template.qcow2
```

### Paso 3: Generalizar la plantilla

```bash
sudo virt-sysprep -d debian-template \
	--hostname debian-template \
	--root-password password:TemplatePass123!
```

### Paso 4: Crear nuevas instancias

```bash
# Crear VM 1
virt-clone --original debian-template \
	--name vm-web-01 \
	--file /var/lib/libvirt/images/vm-web-01.qcow2

# Personalizar VM 1
sudo virt-customize -d vm-web-01 \
	--hostname vm-web-01 \
	--password admin:password:AdminWeb01! \
	--ssh-inject admin:file:/home/user/.ssh/id_rsa.pub \
	--run-command 'apt update && apt install -y nginx'

# Crear VM 2
virt-clone --original debian-template \
	--name vm-db-01 \
	--file /var/lib/libvirt/images/vm-db-01.qcow2

# Personalizar VM 2
sudo virt-customize -d vm-db-01 \
	--hostname vm-db-01 \
	--password admin:password:AdminDB01! \
	--ssh-inject admin:file:/home/user/.ssh/id_rsa.pub \
	--run-command 'apt update && apt install -y postgresql'
```

### Paso 5: Arrancar y verificar

```bash
virsh start vm-web-01
virsh start vm-db-01

# Verificar IPs asignadas
virsh domifaddr vm-web-01
virsh domifaddr vm-db-01

# Conectar por SSH
ssh admin@192.168.122.X
```

---

## 9. Resumen de comandos principales

| Comando | Descripción |
|---------|-------------|
| `virt-clone --original VM --name NUEVA --auto-clone` | Clona una VM con nombre de disco automático |
| `virt-clone --original VM --name NUEVA --file DISCO.qcow2` | Clona especificando el nombre del disco |
| `virsh domrename VIEJO NUEVO` | Renombra una máquina virtual |
| `sudo virt-sysprep -d VM` | Generaliza una VM eliminando identificadores únicos |
| `sudo virt-customize -d VM --hostname NOMBRE` | Personaliza una VM sin arrancarla |
| `sudo ssh-keygen -A` | Regenera todas las claves SSH de host |
| `virsh edit VM` | Edita la configuración XML de una VM |

---

## Referencias

- [curso_virtualizacion_linux — GitHub](https://github.com/josedom24/curso_virtualizacion_linux)
- [Documentación oficial de virt-clone](https://linux.die.net/man/1/virt-clone)
- [Documentación oficial de virt-sysprep](https://libguestfs.org/virt-sysprep.1.html)
- [Documentación oficial de virt-customize](https://libguestfs.org/virt-customize.1.html)
- [libguestfs - Tools for accessing and modifying VM disk images](https://libguestfs.org/)
