---
title: "15 - Instalar y configurar Cinder en nodos de almacenamiento"
date: 2025-11-23T12:00:00+00:00
description: "Instalamos y configuramos Cinder en nodos de almacenamiento usando LVM en OpenStack."
tags: [openstack,instalacion,cinder]
hero: ""
weight: 15
---

En este post explico cómo instalar y configurar el servicio de volúmenes de OpenStack (Cinder) en un nodo de almacenamiento usando LVM.

Nota: ejecuta los comandos en el nodo de almacenamiento (`storage01`) y úsalos tal como aparecen.

## Instalar los paquetes necesarios

```bash
vagrant@storage01:~$ sudo apt install -y lvm2 thin-provisioning-tools
```

## Verificar el disco `/dev/vdb`

```bash
vagrant@storage01:~$ fdisk -l
```

Asegúrate de que `/dev/vdb` aparece y no tiene particiones antes de continuar.

## Crear el volumen físico LVM

```bash
vagrant@storage01:~$ sudo pvcreate /dev/vdb
```

## Crear el grupo de volúmenes `cinder-volumes`

```bash
vagrant@storage01:~$ sudo vgcreate cinder-volumes /dev/vdb
```

## Editar `/etc/lvm/lvm.conf`

Dentro de la sección `devices`, añade o modifica la línea `filter` para evitar que LVM escanee discos no deseados:

```conf
filter = [ "a/sda/", "a/vdb/", "r/.*/"]
```

Esto evita que LVM escanee dispositivos que no forman parte del backend de volúmenes.

## Instalar el servicio Cinder Volume

```bash
vagrant@storage01:~$ sudo apt install -y cinder-volume
```

## Configurar acceso a la base de datos y RabbitMQ

Configura todo esto en el fichero `/etc/cinder/cinder.conf`. Añade o modifica las siguientes secciones y parámetros:

```ini
[database]
connection = mysql+pymysql://cinder:CINDER_DB_PASS@controller01/cinder

[DEFAULT]
transport_url = rabbit://openstack:openstack@controller01
```

## Configurar acceso a Keystone

En el fichero `/etc/cinder/cinder.conf`, añade la sección `keystone_authtoken` completa:

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

## Configurar la IP del nodo de almacenamiento

En `/etc/cinder/cinder.conf`, bajo la sección `[DEFAULT]`, añade:

```ini
my_ip = 10.0.0.4
```

## Configurar el backend LVM

En el mismo fichero `/etc/cinder/cinder.conf`, añade la sección `[lvm]`:

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

## Configurar Glance y `lock_path`

En la sección `[DEFAULT]`, añade:

```ini
glance_api_servers = http://controller01:9292
oslo_concurrency.lock_path = /var/lib/cinder/tmp
```

## Reiniciar servicios

Lanza los siguientes comandos para reiniciarlos y asegúrate de que estén levantados.

```bash
vagrant@storage01:~$ sudo service target restart
vagrant@storage01:~$ sudo service cinder-volume restart
```

## Comprobar que el servicio está corriendo

Pod ultimo comprueba que usando el cliente de OpenStack los servicios están levantados :

```bash
vagrant@controller01:~$ openstack volume service list
+------------------+---------------+------+---------+-------+----------------------------+
| Binary           | Host          | Zone | Status  | State | Updated At                 |
+------------------+---------------+------+---------+-------+----------------------------+
| cinder-scheduler | controller01  | nova | enabled | up    | 2025-11-23T14:58:09.000000 |
| cinder-volume    | storage01@lvm | nova | enabled | up    | 2025-11-23T14:58:09.000000 |
+------------------+---------------+------+---------+-------+----------------------------+
```