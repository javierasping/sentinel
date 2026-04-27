---
title: "15 - Instalar y configurar Cinder en nodos de almacenamiento"
date: 2025-11-23T12:00:00+00:00
description: "Instalamos y configuramos Cinder en nodos de almacenamiento usando LVM en OpenStack."
tags: [openstack,instalacion,cinder]
hero: images/openstack/instalacion-manual/instalar-configurar-cinder-storage.png
weight: 15
---

En este post, explicaremos cómo instalar y configurar el servicio de volúmenes de OpenStack (Cinder) en un nodo de almacenamiento utilizando LVM.

Nota: ejecuta los comandos en el nodo de almacenamiento (`storage01`) y utilízalos tal como aparecen.

## Instalaremos los paquetes necesarios:

```bash
vagrant@storage01:~$ sudo apt install -y lvm2 thin-provisioning-tools
```

## Verificación del disco `/dev/vdb`

```bash
vagrant@storage01:~$ fdisk -l
```

Asegúrate de que `/dev/vdb` esté presente y no tenga particiones antes de continuar.

## Creación del volumen físico LVM:

```bash
vagrant@storage01:~$ sudo pvcreate /dev/vdb
```

## Creación del grupo de volúmenes `cinder-volumes`:

```bash
vagrant@storage01:~$ sudo vgcreate cinder-volumes /dev/vdb
```

## Editar `/etc/lvm/lvm.conf`

En la sección `devices`, añade o modifica la línea `filter` para evitar que LVM escanee discos no deseados:

```conf
filter = [ "a/sda/", "a/vdb/", "r/.*/"]
```

Esto evita que LVM escanee dispositivos que no forman parte del backend de volúmenes.

## Instalaremos el servicio Cinder Volume:

```bash
vagrant@storage01:~$ sudo apt install -y cinder-volume
```

## Configuraremos el acceso a la base de datos y RabbitMQ:

Configuraremos todo esto en el archivo `/etc/cinder/cinder.conf`. Añadiremos o modificaremos las siguientes secciones y parámetros:

```ini
[database]
connection = mysql+pymysql://cinder:CINDER_DB_PASS@controller01/cinder

[DEFAULT]
transport_url = rabbit://openstack:openstack@controller01
```

## Configuraremos el acceso a Keystone:

En el archivo `/etc/cinder/cinder.conf`, añadiremos la sección `keystone_authtoken` completa:

```ini
[keystone_authtoken]
www_authenticate_uri = http://controller01:5000
auth_url = http://controller01:5000
memcached_servers = controller01:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = cinder
password = CINDER_SVC_PASS
```

## Configuraremos la IP del nodo de almacenamiento:

En `/etc/cinder/cinder.conf`, bajo la sección `[DEFAULT]`, añadiremos:

```ini
my_ip = 10.0.0.4
```

## Configuraremos el backend LVM:

En el mismo archivo `/etc/cinder/cinder.conf`, añadiremos la sección `[lvm]`:

```ini
[lvm]
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
volume_group = cinder-volumes
iscsi_protocol = iscsi
iscsi_helper = tgtadm
```

Y en `[DEFAULT]`, asegúrate de incluir:

```ini
enabled_backends = lvm
```

## Configuraremos Glance y la ruta de bloqueo (`lock_path`):

En la sección `[DEFAULT]`, añadiremos:

```ini
glance_api_servers = http://controller01:9292
oslo_concurrency.lock_path = /var/lib/cinder/tmp
```

## Reiniciaremos los servicios:

Ejecuta los siguientes comandos para reiniciarlos y verifica que estén activos.

```bash
vagrant@storage01:~$ sudo service target restart
vagrant@storage01:~$ sudo service cinder-volume restart
```

## Verificación de que el servicio está activo

Finalmente, comprobaremos que, utilizando el cliente de OpenStack, los servicios están activos:

```bash
vagrant@controller01:~$ openstack volume service list
+------------------+---------------+------+---------+-------+----------------------------+
| Binary           | Host          | Zone | Status  | State | Updated At                 |
+------------------+---------------+------+---------+-------+----------------------------+
| cinder-scheduler | controller01  | nova | enabled | up    | 2025-11-23T14:58:09.000000 |
| cinder-volume    | storage01@lvm | nova | enabled | up    | 2025-11-23T14:58:09.000000 |
+------------------+---------------+------+---------+-------+----------------------------+
```