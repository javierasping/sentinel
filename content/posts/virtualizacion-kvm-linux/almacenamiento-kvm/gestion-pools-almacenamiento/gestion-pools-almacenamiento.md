---
title: "Gestión de pools de almacenamiento"
date: 2025-10-25T09:00:00+00:00
description: "Cómo crear, iniciar, configurar (autostart) y destruir pools usando virsh y archivos XML; listar y obtener información. Diferencias entre tipos: dir, disk, logical, iSCSI, ZFS, NFS."
tags: [KVM,Virtualizacion,Libvirt,Almacenamiento,Pools]
hero: images/virtualizacion-kvm-linux/almacenamiento-kvm/gestion-pools-almacenamiento.jpg
---

Tienes que incluir y responder a las siguientes preguntas en este post .

Que es un pool 
Como se crea y que formas utilizan 

El almacenamiento en KVM/libvirt se organiza en "storage pools" y "storage volumes". En este artículo explicaremos qué es un pool, por qué se usan, y cómo gestionarlos con `virsh` o mediante ficheros XML. Incluiremos ejemplos y recomendaciones prácticas, así como notas sobre pools basados en LVM.

## ¿Qué es un storage pool?

Un storage pool es una abstracción que agrupa una fuente de almacenamiento que libvirt puede exponer a las máquinas virtuales. Un pool puede corresponder a un directorio en disco, a un sistema de ficheros montado, a un conjunto de volúmenes lógicos (LVM), a dispositivos iSCSI, o a backends distribuidos como Ceph RBD o Gluster.

El pool simplifica la gestión: desde la configuración de la VM se referencia un volumen dentro del pool en lugar de manejar rutas físicas o dispositivos. Los pools pueden ser temporales (solo en memoria, desaparecen al reiniciar) o persistentes (definidos en disco y restaurados en arranque).

## ¿Cómo ver los pools existentes?

Para listar los pools conocidos por libvirt:

```bash
javiercruces@FJCD-PC:~$ virsh pool-list --all
 Name      State    Autostart
-------------------------------
 default   active   yes
 isos      active   yes
 libvirt   active   yes

```

El pool `default` suele apuntar a `/var/lib/libvirt/images` y se crea automáticamente en muchas distribuciones.

Para ver información detallada de un pool:

```bash
javiercruces@FJCD-PC:~$ virsh pool-info default
Name:           default
UUID:           017a5e21-579b-43e7-99a2-e8915524dc80
State:          running
Persistent:     yes
Autostart:      yes
Capacity:       914,78 GiB
Allocation:     100,98 GiB
Available:      813,80 GiB

```

Y si quieres ver su definición XML:

```bash
javiercruces@FJCD-PC:~$ virsh pool-dumpxml default
<pool type='dir'>
  <name>default</name>
  <uuid>017a5e21-579b-43e7-99a2-e8915524dc80</uuid>
  <capacity unit='bytes'>982240026624</capacity>
  <allocation unit='bytes'>108423954432</allocation>
  <available unit='bytes'>873816072192</available>
  <source>
  </source>
  <target>
    <path>/var/lib/libvirt/images</path>
    <permissions>
      <mode>0711</mode>
      <owner>0</owner>
      <group>0</group>
    </permissions>
  </target>
</pool>
```

## Crear un pool: temporal vs persistente

Hay dos formas principales de crear pools:

- Crear un pool temporal: `virsh pool-create` o `virsh pool-create-as`. Este pool existirá hasta que el servicio libvirt o el host se reinicie.
- Crear un pool persistente: `virsh pool-define` o `virsh pool-define-as` crea la definición en `/etc/libvirt/storage/` y permite arrancarlo y configurarlo para autostart.

### Crear un pool persistente (ejemplo práctico)

Supongamos que hemos montado un disco en `/srv/images` y queremos crear un pool llamado `vm-images` de tipo `dir`:

```bash
javiercruces@FJCD-PC:~$ virsh pool-define-as vm-images dir --target /srv/images
javiercruces@FJCD-PC:~$ virsh pool-build vm-images
javiercruces@FJCD-PC:~$ virsh pool-start vm-images
javiercruces@FJCD-PC:~$ virsh pool-autostart vm-images
```

Comprobaciones útiles:

```bash
javiercruces@FJCD-PC:~$ virsh pool-list --all
javiercruces@FJCD-PC:~$ virsh pool-info vm-images
```

Si quieres crear el pool a partir de un fichero XML (por ejemplo para iSCSI o configuraciones complejas), escribe el XML y usa:

```bash
javiercruces@FJCD-PC:~$ virsh pool-define /ruta/a/pool-definition.xml
javiercruces@FJCD-PC:~$ virsh pool-start nombre_pool
```

Ejemplo mínimo de XML para un pool `dir`:

```xml
<pool type="dir">
	<name>isos</name>
	<target>
		<path>/var/lib/libvirt/isos</path>
	</target>
</pool>
```

Después de ejecutar `virsh pool-define`, libvirt guarda la definición persistente del pool como un fichero XML en `/etc/libvirt/storage/`. Cada XML en ese directorio representa una definición de pool que libvirt puede arrancar y controlar con `virsh`.

Las entradas que deben arrancarse automáticamente se marcan en el subdirectorio `/etc/libvirt/storage/autostart/`. En la práctica este subdirectorio contiene normalmente enlaces simbólicos que apuntan a los XML de definición originales; su presencia indica que el pool se iniciará al arrancar el servicio libvirt o el sistema.

```bash
javiercruces@FJCD-PC:~$ ls -l /etc/libvirt/storage/
total 16
drwxr-xr-x 2 root root 4096 oct 18 16:13 autostart
-rw------- 1 root root  538 oct 13 20:03 default.xml
-rw------- 1 root root  532 oct 13 20:41 isos.xml
-rw------- 1 root root  531 oct 18 16:13 libvirt.xml

javiercruces@FJCD-PC:~$ ls -l /etc/libvirt/storage/autostart/
total 0
lrwxrwxrwx 1 root root 32 oct 13 20:03 default.xml -> /etc/libvirt/storage/default.xml
lrwxrwxrwx 1 root root 29 oct 13 20:41 isos.xml -> /etc/libvirt/storage/isos.xml
lrwxrwxrwx 1 root root 32 oct 18 16:13 libvirt.xml -> /etc/libvirt/storage/libvirt.xml
```

Nota: puedes controlar si un pool se inicia automáticamente con el comando `virsh pool-autostart` (consulta `virsh help pool-autostart` para las opciones exactas en tu versión). Si eliminas el XML del directorio `/etc/libvirt/storage/` o quitas el enlace en `autostart/`, libvirt dejará de conocer o de arrancar ese pool de forma persistente.

## Refrescar y listar volúmenes

Si añades manualmente ficheros al directorio del pool (por ejemplo descargar una ISO), libvirt puede no detectarlos inmediatamente. Usa:

```bash
javiercruces@FJCD-PC:~$ virsh pool-refresh isos
javiercruces@FJCD-PC:~$ virsh vol-list --pool isos
```

## Eliminar y destruir pools

Si quieres borrar un pool:

1. Parar el pool (no lo borra, solo lo detiene):

```bash
javiercruces@FJCD-PC:~$ virsh pool-destroy vm-images
```

2. (Opcional) Borrar el directorio si ya no lo necesitas:

```bash
javiercruces@FJCD-PC:~$ rm -rf /srv/images
```

3. Eliminar la definición persistente:

```bash
javiercruces@FJCD-PC:~$ virsh pool-undefine vm-images
```

Si prefieres eliminar la carpeta a través de `virsh` (pool-delete) ten en cuenta que el directorio debe estar vacío:

```bash
javiercruces@FJCD-PC:~$ virsh pool-delete vm-images
```

## Pools basados en LVM: consideraciones y pasos

Los pools basados en LVM permiten usar volúmenes lógicos como discos para las VMs. Antes de crear uno asegúrate de entender que el procedimiento puede formatear particiones si creas un nuevo PV/VG.

Pasos básicos (concepto):

- Comprueba que libvirt soporta pools `logical`:

```bash
javiercruces@FJCD-PC:~$ virsh pool-capabilities | grep "'logical' supported='yes'"
```

- Definir un pool lógico que use un dispositivo LVM:

```bash
javiercruces@FJCD-PC:~$ virsh pool-define-as guest_images_logical logical --source-dev=/dev/sdc --source-name libvirt_lvm --target /dev/libvirt_lvm
javiercruces@FJCD-PC:~$ virsh pool-start guest_images_logical
javiercruces@FJCD-PC:~$ virsh pool-autostart guest_images_logical
```

Recomendaciones:

- Haz copia de seguridad antes de manipular particiones o dispositivos físicos.
- Si usas un VG existente, no debería borrar datos; si creas uno nuevo basado en una partición se formateará.
- Verifica `virsh pool-info <pool>` para comprobar capacidad, allocation y estado.

## Buenas prácticas y recomendaciones

- Usa nombres claros para pools (ej. `images`, `vms`, `isos`, `backups`) y separa propósitos.
- Prefiere pools persistentes para entornos de producción y activa `autostart` cuando proceda.
- Monitoriza `Capacity`, `Allocation` y `Available` para evitar sobrecommit en entornos thin-provisioned.
- Evita modificar manualmente rutas de pools sin usar `virsh pool-build`/`pool-refresh`, porque libvirt puede perder sincronización con el contenido.
- Para entornos con migraciones frecuentes, elige backends compartidos y probados (Ceph RBD, NFS bien configurado, Gluster) para facilitar live-migration.

## Resumen

Los storage pools son la forma en que libvirt abstrae las distintas fuentes de almacenamiento. Con `virsh` puedes listar, crear (temporal o persistente), iniciar, autostart, refrescar, destruir y eliminar pools. Para configuraciones complejas (iSCSI, LVM, Ceph) es habitual usar definiciones XML que luego se cargan con `virsh pool-define`.

En el próximo artículo cubriremos cómo crear y gestionar volúmenes dentro de un pool y cómo asignarlos a VMs.

## Fuentes

- Documentación oficial libvirt: Storage management; Storage pool and volume XML format — https://libvirt.org/storage.html
- Guía de uso y ejemplos: Xavi Aznar — "Cómo crear un storage pool en KVM" (2019)
- Red Hat / documentación LVM y libvirt: secciones sobre pools LVM y ejemplos de `virsh`
