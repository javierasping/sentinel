---
title: "14 - Configurar Cinder en el nodo controlador"
date: 2025-11-23T12:00:00+00:00
description: "Instala y configura Cinder, el servicio de almacenamiento en bloque, en el nodo controlador OpenStack."
tags: [openstack,instalacion,cinder]
hero: ""
weight: 14
---

# Instalación y configuración de Cinder en el nodo controlador

Este post detalla los pasos que seguimos para instalar y configurar **Cinder**, el servicio de almacenamiento en bloque de OpenStack, en el nodo controlador (`controller01`). Incluimos los comandos para crear la base de datos, configurar los servicios, endpoints y la integración con Nova.

## 1) Crear la base de datos de Cinder

Accedemos a MySQL y creamos la base de datos y el usuario:

```bash
vagrant@controller01:~$ sudo mysql

CREATE DATABASE cinder;
GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'localhost' IDENTIFIED BY 'CINDER_DB_PASS';
GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'%' IDENTIFIED BY 'CINDER_DB_PASS';
EXIT;
```

## 2) Crear el usuario de Cinder y asignar el rol admin

Cargamos las credenciales de administrador y creamos el usuario `cinder` en el proyecto `service`:

```bash
. admin-openrc
openstack user create --domain default --password CINDER_SVC_PASS cinder
openstack role add --project service --user cinder admin

+---------------------+----------------------------------+
| Field               | Value                            |
+---------------------+----------------------------------+
| domain_id           | default                          |
| enabled             | True                             |
| id                  | 97735ce5873c42ac850e63f536a0eec9 |
| name                | cinder                           |
| options             | {}                               |
| password_expires_at | None                             |
+---------------------+----------------------------------+
```

## 3) Crear los servicios y endpoints de Cinder

Creamos los servicios `cinderv2` y `cinderv3` y sus endpoints para la región `RegionOne`:

```bash
openstack service create --name cinderv2 --description "OpenStack Block Storage" volumev2
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | OpenStack Block Storage          |
| enabled     | True                             |
| id          | c5c0d788373e4d88ae8526a95269f4c4 |
| name        | cinderv2                         |
| type        | volumev2                         |
+-------------+----------------------------------+

openstack service create --name cinderv3 --description "OpenStack Block Storage" volumev3

+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | OpenStack Block Storage          |
| enabled     | True                             |
| id          | 27fbad310c2d4f2e823898751c3cd4f5 |
| name        | cinderv3                         |
| type        | volumev3                         |
+-------------+----------------------------------+

# Cinder v2
openstack endpoint create --region RegionOne volumev2 public  http://controller01:8776/v2/%\(project_id\)s
openstack endpoint create --region RegionOne volumev2 internal http://controller01:8776/v2/%\(project_id\)s
openstack endpoint create --region RegionOne volumev2 admin    http://controller01:8776/v2/%\(project_id\)s

# Cinder v3
openstack endpoint create --region RegionOne volumev3 public  http://controller01:8776/v3/%\(project_id\)s
openstack endpoint create --region RegionOne volumev3 internal http://controller01:8776/v3/%\(project_id\)s
openstack endpoint create --region RegionOne volumev3 admin    http://controller01:8776/v3/%\(project_id\)s


```

## 4) Instalar los paquetes de Cinder

```bash
sudo apt install -y cinder-api cinder-scheduler
```

## 5) Configurar la base de datos y RabbitMQ manualmente

Editamos el fichero `/etc/cinder/cinder.conf` para incluir los siguientes parámetros:

```ini
[database]
connection = mysql+pymysql://cinder:CINDER_DB_PASS@controller01/cinder

[DEFAULT]
transport_url = rabbit://openstack:RABBIT_PASS@controller01
```

## 6) Configurar acceso al servicio de identidad (Keystone)

Añadimos los parámetros para Keystone en el mismo fichero:

```ini
[DEFAULT]
auth_strategy = keystone

[keystone_authtoken]
auth_uri = http://controller01:5000
auth_url = http://controller01:5000
memcached_servers = controller01:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = cinder
password = KEYSTONE_SVC_PASS
```

## 7) Configurar IP del nodo y lock_path

```ini
[DEFAULT]
my_ip = 10.0.0.11
oslo_concurrency.lock_path = /var/lib/cinder/tmp
```

## 8) Sincronizar la base de datos de Cinder

```bash
vagrant@controller01:~$ sudo su -s /bin/sh -c "cinder-manage db sync" cinder
```

## 9) Configurar Nova para usar Cinder

Añadimos la región de Cinder en el fichero de configuración de Nova `/etc/nova/nova.conf`:

```ini
[cinder]
os_region_name = RegionOne
```

## 10) Reiniciar los servicios

```bash
sudo service nova-api restart
sudo service cinder-scheduler restart
sudo service apache2 restart
```

## 11) Verificar el funcionamiento de Cinder

```bash
. admin-openrc
vagrant@controller01:~$ openstack volume service list
+------------------+--------------+------+---------+-------+----------------------------+
| Binary           | Host         | Zone | Status  | State | Updated At                 |
+------------------+--------------+------+---------+-------+----------------------------+
| cinder-scheduler | controller01 | nova | enabled | up    | 2025-11-23T02:21:13.000000 |
+------------------+--------------+------+---------+-------+----------------------------+
```

> Nota: Si algún servicio aparece con `State` distinto de `up` o `enabled`, revisamos los logs en `/var/log/cinder/`.

---