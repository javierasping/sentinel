---
title: "15 - Instalar y configurar Cinder en nodos de almacenamiento"
date: 2025-11-23T12:00:00+00:00
description: "Instalamos y configuramos Cinder en nodos de almacenamiento usando LVM en OpenStack."
tags: [openstack,instalacion,cinder]
hero: ""
weight: 15
---

# Instalación y configuración de Cinder en el nodo de storage (LVM)

Explicamos cómo instalar y configurar el servicio de volúmenes de OpenStack (Cinder) en un nodo de almacenamiento usando LVM. Los pasos están escritos de forma sencilla .

Nota: ejecutamos los comandos en el nodo de almacenamiento (por ejemplo `storage01`) y los usamos tal como aparecen.

## 1) Instalar los paquetes necesarios

```bash
vagrant@storage01:~$ sudo apt install -y lvm2 thin-provisioning-tools
```

## 2) Verificar el disco `/dev/vdb`

```bash
vagrant@storage01:~$ fdisk -l
```

Nos aseguramos de que `/dev/vdb` aparece y no tiene particiones antes de continuar.

## 3) Crear el volumen físico LVM

```bash
vagrant@storage01:~$ sudo pvcreate /dev/vdb
```

## 4) Crear el grupo de volúmenes `cinder-volumes`

```bash
vagrant@storage01:~$ sudo vgcreate cinder-volumes /dev/vdb
```

## 5) Editar `/etc/lvm/lvm.conf`

Dentro de la sección `devices`, añadimos o modificamos la línea `filter` para evitar que LVM escanee discos no deseados:

```conf
filter = [ "a/sda/", "a/vdb/", "r/.*/"]
```

Esto evita que LVM escanee dispositivos que no forman parte del backend de volúmenes.

## 6) Instalar el servicio Cinder Volume

```bash
vagrant@storage01:~$ sudo apt install -y cinder-volume
```

## 7) Configurar acceso a la base de datos y RabbitMQ

Todo esto lo configuramos en el fichero `/etc/cinder/cinder.conf`. Añadimos o modificamos las siguientes secciones y parámetros:

```ini
[database]
connection = mysql+pymysql://cinder:CINDER_DB_PASS@controller01/cinder

[DEFAULT]
transport_url = rabbit://openstack:openstack@controller01
```

## 8) Configurar acceso a Keystone

En el fichero `/etc/cinder/cinder.conf`, añadimos la sección `keystone_authtoken` completa:

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

## 9) Configurar la IP del nodo de almacenamiento

En `/etc/cinder/cinder.conf`, bajo la sección `[DEFAULT]` añadimos:

```ini
my_ip = 10.0.0.4
```

## 10) Configurar el backend LVM

En el mismo fichero `/etc/cinder/cinder.conf`, añadimos la sección `[lvm]`:

```ini
[lvm]
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
volume_group = cinder-volumes
iscsi_protocol = iscsi
iscsi_helper = tgtadm
```

Y en `[DEFAULT]` nos aseguramos de incluir:

```ini
enabled_backends = lvm
```

## 11) Configurar Glance y `lock_path`

En la sección `[DEFAULT]` añadimos:

```ini
glance_api_servers = http://controller01:9292
oslo_concurrency.lock_path = /var/lib/cinder/tmp
```

## 12) Reiniciar servicios

```bash
vagrant@storage01:~$ sudo service target restart
vagrant@storage01:~$ sudo service cinder-volume restart
```

## 13) Comprobar que el servicio está corriendo

```bash
vagrant@controller01:~$ openstack volume service list
+------------------+---------------+------+---------+-------+----------------------------+
| Binary           | Host          | Zone | Status  | State | Updated At                 |
+------------------+---------------+------+---------+-------+----------------------------+
| cinder-scheduler | controller01  | nova | enabled | up    | 2025-11-23T14:58:09.000000 |
| cinder-volume    | storage01@lvm | nova | enabled | up    | 2025-11-23T14:58:09.000000 |
+------------------+---------------+------+---------+-------+----------------------------+
```