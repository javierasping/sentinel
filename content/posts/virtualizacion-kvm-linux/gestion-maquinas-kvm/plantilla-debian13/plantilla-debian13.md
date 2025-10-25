---
title: "Crear una plantilla de una máquina virtual Debian 13 en KVM/libvirt"
date: 2025-10-18T09:00:00+00:00
description: "Guía paso a paso para crear una plantilla (golden image) de Debian 13 con KVM/libvirt: preparación, generalización con virt-sysprep, compactación con virt-sparsify, marcaje de solo lectura y buenas prácticas de clonación."
tags: [KVM,Virtualizacion,Libvirt,Linux,VM,Templates,Debian13]
hero: images/virtualizacion-kvm-linux/gestion-maquinas-kvm/plantilla-debian13.jpg
---

# Plantillas de máquinas virtuales

Una plantilla de máquina virtual (template) es una imagen preconfigurada del sistema operativo que usamos para desplegar rápidamente nuevas VMs, evitando repeticiones y errores. Aquí veremos cómo crear una plantilla maestra de Debian 13 lista para clonar.

---

## 1 Crear e instalar la VM base

Crea una VM limpia de Debian 13, aplica todas las actualizaciones y añade el software común que quieras en todos los clones (agente invitado, utilidades, etc.). Ejemplo mínimo:

```bash
# Crear la VM base (ajusta CPU, RAM, disco, ISO y red a tu entorno)
virt-install \
  --name debian13-base \
  --memory 4096 \
  --vcpus 2 \
  --disk path=/var/lib/libvirt/images/debian13-base.qcow2,size=20,format=qcow2 \
  --cdrom /var/lib/libvirt/images/debian-13.1.0-amd64-netinst.iso \
  --os-variant debian12 \
  --network network=default,model=virtio \
  --noautoconsole
```

Una vez creada la VM, instala todos los componentes que quieres que tenga esta plantilla: usuarios, paquetes, etc.

Para ello comprobaré que está corriendo y comenzaré con la instalación:

```bash
$ virsh list 
 Id   Name            State
-------------------------------
 1    debian13-base   running
```

Me conectaré por SSH a la máquina:

```bash
javiercruces@FJCD-PC:~/Documentos/sentinel (feature/kvm) [prd-eu-central|]
$ virsh domifaddr debian13-base
 Name       MAC address          Protocol     Address
-------------------------------------------------------------------------------
 vnet8      52:54:00:62:d5:6a    ipv4         192.168.122.202/24
 -          -                    ipv4         192.168.122.201/24

javiercruces@FJCD-PC:~/Documentos/sentinel (feature/kvm) [prd-eu-central|]
$ ssh 192.168.122.202
The authenticity of host '192.168.122.202 (192.168.122.202)' can't be established.
ED25519 key fingerprint is SHA256:RvOdKE4i1eQNHJ8bdK6RoYl9GckeGN2xY6X/IsPvMHI.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.122.202' (ED25519) to the list of known hosts.
javiercruces@192.168.122.202's password: 
Linux debian13-base 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.


javiercruces@debian13-base:~$ 
```


En mi caso, voy a actualizarla a la última versión e instalaré las qemu-utils. Además, como esta máquina solo la voy a utilizar para pruebas, configuraré mi clave SSH para poder conectarme a ella sin necesidad de introducir mi contraseña.

```bash
# Dentro de la VM he realizado los siguientes comandos :
sudo apt update && sudo apt -y full-upgrade
sudo apt install -y qemu-guest-agent cloud-guest-utils

# Dentro de nuestro usuario generamos los siguientes ficheros y asignamos los permisos:
javiercruces@debian13-base:~$ mkdir -p ~/.ssh
javiercruces@debian13-base:~$ touch ~/.ssh/authorized_keys
javiercruces@debian13-base:~$ chmod 700 ~/.ssh
javiercruces@debian13-base:~$ chmod 600 ~/.ssh/authorized_keys

# Con este comando añadimos la clave pública que queremos utilizar en la VM
javiercruces@FJCD-PC:~$ ssh-copy-id -i ~/.ssh/jcruces.pub javiercruces@192.168.122.202   

# Por último, compruebo que puedo conectarme usando la clave SSH. Recuerda desactivar en el servicio SSH la autenticación por contraseña.
javiercruces@FJCD-PC:~ [prd-eu-central|]
$ ssh javiercruces@192.168.122.202
Linux debian13-base 6.12.48+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.48-1 (2025-09-20) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Oct 18 16:35:26 2025 from 192.168.122.1
```

Apaga la VM base cuando termines:

```bash
javiercruces@FJCD-PC:~$ virsh shutdown debian13-base
Domain 'debian13-base' is being shutdown
```

---

## 2 Generalizar la imagen con virt-sysprep

La generalización elimina y regenera elementos que deben ser únicos en cada clon (machine-id, claves SSH de host, hostname, logs, caches, etc.). Para Linux usaremos `virt-sysprep` (paquete `libguestfs-tools`).

```bash
# Generalizar indicando el dominio (VM debe estar apagada)
virt-sysprep -d debian13-base \
  --hostname plantilla-debian13 \
  --firstboot-command "dpkg-reconfigure openssh-server"
```

Notas:
- `--hostname` fija el nombre de host de la plantilla.
- `--firstboot-command` ejecuta el comando al primer arranque del clon para regenerar claves de SSH del host.
- Puedes añadir o quitar operaciones con `--enable/--operations` (ver `virt-sysprep --list-operations`).

---

## 3 Compactar la imagen con virt-sparsify

Para ahorrar espacio, compacta la imagen (elimina bloques vacíos) y opcionalmente comprímela.

Con la instalación base, en mi caso la imagen ocupa alrededor de 2 GB reales.
Ten cuidado, porque si intentas comprobar su tamaño con ls, verás el tamaño lógico total que puede alcanzar la imagen, no el espacio que realmente está usando:

```bash
# Así verías el tamaño lógico total que puede ocupar el disco de la VM
javiercruces@FJCD-PC:~ [prd-eu-central|]
$ sudo ls -lh /var/lib/libvirt/images/ | grep debian13-base
-rw------- 1 root         root  21G oct 18 16:47 debian13-base.qcow2

# Así verías el tamaño real que ocupa el disco
javiercruces@FJCD-PC:~ [prd-eu-central|]
$ sudo du -h --max-depth=1 /var/lib/libvirt/images/debian13-base.qcow2
2,0G	/var/lib/libvirt/images/debian13-base.qcow2

```

Ahora vamos a comprimir la imagen base para que ocupe menos:

```bash
sudo virt-sparsify --compress \
  /var/lib/libvirt/images/debian13-base.qcow2 \
  /var/lib/libvirt/images/plantilla-debian13-comprimida.qcow2
```

Ten en cuenta que antes de reemplazar la imagen real por la comprimida, debes probar que una máquina es capaz de arrancar usando este nuevo disco. 
```bash
# Reemplazar la imagen por la compactada
sudo mv /var/lib/libvirt/images/plantilla-debian13-comprimida.qcow2 \
  /var/lib/libvirt/images/debian13-base.qcow2
```

Ahora, si volvemos a comprobar el tamaño de la imagen, veremos que ha pasado de ocupar 2GB a 586MB:

```bash
javiercruces@FJCD-PC:~$ sudo du -h --max-depth=1 /var/lib/libvirt/images/debian13-base.qcow2
586M	/var/lib/libvirt/images/debian13-base.qcow2
```

---

## 4 Marcar la imagen como solo lectura (evitar arrancar la plantilla)

Para no perder la plantilla, marca la imagen como solo lectura. Si alguien intenta arrancarla por error, fallará.

```bash
sudo chmod 444 /var/lib/libvirt/images/debian13-base.qcow2
```

Además, si quieres, renombra el dominio para identificar que es una plantilla. En mi caso no lo haré:

```bash
virsh domrename debian13-base plantilla-debian13
```

---

## 5 Crear clones a partir de la plantilla

Tienes dos formas principales:

- Clonación completa (full): imagen independiente; ocupa tanto como el original.
- Clonación enlazada (linked): crea una capa overlay sobre la plantilla (sólo lectura); ocupa menos, depende de la base.

### 5.1 Clonación completa

Así crearemos un clon completo utilizando el disco de la plantilla que ocupará tanto como el original:

```bash
sudo virt-clone --original debian13-base --name debian13-clonacion-completa \
  --file /var/lib/libvirt/images/debian13-clonacion-completa.qcow2
```

Con este comando tendremos una nueva máquina virtual con los mismos componentes que la plantilla.

Antes de arrancar la clonación como un usuario no-root, asegúrate de ajustar propietario y permisos del fichero de disco recién creado. En muchas distribuciones el proceso QEMU/libvirt necesita que el archivo pertenezca al usuario/grupo que ejecuta el hypervisor (por ejemplo `libvirt-qemu:libvirt-qemu` o `qemu:qemu`). Si no se corrigen estos permisos, al iniciar la VM con un usuario distinto de root puede fallar.

```bash
javiercruces@FJCD-PC:~$ sudo chown libvirt-qemu:libvirt-qemu /var/lib/libvirt/images/debian13-clonacion-completa.qcow2
javiercruces@FJCD-PC:~$ sudo chmod 660 /var/lib/libvirt/images/debian13-clonacion-completa.qcow2

javiercruces@FJCD-PC:~$ sudo virsh start debian13-clonacion-completa
Domain 'debian13-clonacion-completa' started
```

Si tu distribución usa otro usuario/grupo para el proceso qemu (por ejemplo `qemu:qemu`), sustituye `libvirt-qemu:libvirt-qemu` por el par correcto. Además, si usas SELinux o AppArmor revisa las políticas que puedan bloquear el acceso al fichero.

### 5.2 Clonación enlazada

Podemos hacer esto de dos formas distintas.

La primera es generar el disco como backing file a la plantilla (solo lectura) usando qemu-img:

```bash
sudo qemu-img create -f qcow2 \
  -F qcow2 \
  -b /var/lib/libvirt/images/debian13-base.qcow2 \
  /var/lib/libvirt/images/debian13-clonacion-enlazada.qcow2
```

Tras generar el disco, creamos la máquina virtual haciendo uso de este:

```bash
sudo virt-install \
  --name debian13-clonacion-enlazada \
  --memory 4096 \
  --vcpus 2 \
  --disk path=/var/lib/libvirt/images/debian13-clonacion-enlazada.qcow2,format=qcow2 \
  --os-variant debian12 \
  --network network=default,model=virtio \
  --import \
  --noautoconsole
```

Antes de arrancar la máquina clonada, ajusta propietario y permisos del fichero creado para evitar errores de acceso cuando el hipervisor (qemu/libvirt) no corra como root. En muchos sistemas el proceso corre como `libvirt-qemu:libvirt-qemu` o `qemu:qemu`.

```bash
javiercruces@FJCD-PC:~$ sudo chown libvirt-qemu:libvirt-qemu /var/lib/libvirt/images/debian13-clonacion-enlazada.qcow2
javiercruces@FJCD-PC:~$ sudo chmod 660 /var/lib/libvirt/images/debian13-clonacion-enlazada.qcow2

javiercruces@FJCD-PC:~$ sudo virsh start debian13-clonacion-enlazada
Domain 'debian13-clonacion-enlazada' started
```

Si tu distribución usa otro usuario/grupo para qemu (por ejemplo `qemu:qemu`), sustituye `libvirt-qemu:libvirt-qemu` por el par correcto. Revisa también SELinux/AppArmor si persisten errores.


---

## Referencias

- virt-sysprep (libguestfs): https://libguestfs.org/virt-sysprep.1.html
- virt-sparsify (libguestfs): https://libguestfs.org/virt-sparsify.1.html
- virt-clone (libvirt): https://libvirt.org/manpages/virt-clone.html
- virt-customize (libguestfs): https://libguestfs.org/virt-customize.1.html
- qemu-img (resize/create/backing): https://www.qemu.org/docs/master/tools/qemu-img.html
