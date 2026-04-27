---
title: "09 - Instalar y configurar Nova en el nodo controlador"
date: 2025-11-23T12:00:00+00:00
description: "Paso a paso para desplegar el servicio de computación Nova en el nodo controlador OpenStack."
tags: [openstack,instalacion,nova]
hero: images/openstack/instalacion-manual/instalar-configurar-nova-controlador.png
weight: 9
---

Este documento describe el proceso de instalación y configuración del servicio de cómputo, Nova, en el nodo controlador (`controller01`).

## Requisitos previos

Antes de comenzar, asegúrate de que las bases de datos y las credenciales básicas de Keystone hayan sido creadas y que el archivo `admin-openrc` esté disponible.

### Crear las bases de datos (en `controller01`)

Nos conectaremos al servidor SQL como `root` para crear las bases de datos necesarias:

```bash
vagrant@controller01:~$ sudo mysql
```

Creación de las bases de datos `nova_api`, `nova` y `nova_cell0`:

```sql
CREATE DATABASE nova_api;
CREATE DATABASE nova;
CREATE DATABASE nova_cell0;
```

Asignaremos los permisos a la cuenta `nova` (sustituye `NOVA_DBPASS` por la contraseña definida):

```sql
GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost' IDENTIFIED BY 'NOVA_DBPASS';
GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' IDENTIFIED BY 'NOVA_DBPASS';

GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' IDENTIFIED BY 'NOVA_DBPASS';
GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' IDENTIFIED BY 'NOVA_DBPASS';

GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'localhost' IDENTIFIED BY 'NOVA_DBPASS';
GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'%' IDENTIFIED BY 'NOVA_DBPASS';
```

Finalmente, salimos del cliente de la base de datos:

```sql
exit;
```

## Crear credenciales del servicio (en `controller01`)

Cargaremos las variables de entorno del administrador para ejecutar los comandos de Keystone:

```bash
vagrant@controller01:~$ source admin-openrc 
```

Crearemos el usuario de servicio `nova` (utiliza `NOVA_PASSWORDS` como contraseña de ejemplo):

```bash
vagrant@controller01:~$ openstack user create --domain default --password NOVA_PASSWORDS nova
+---------------------+----------------------------------+
| Field               | Value                            |
+---------------------+----------------------------------+
| default_project_id  | None                             |
| domain_id           | default                          |
| email               | None                             |
| enabled             | True                             |
| id                  | 5da398a114604a278117a4e071796e91 |
| name                | nova                             |
| description         | None                             |
| password_expires_at | None                             |
+---------------------+----------------------------------+
```

Añadiremos el rol `admin` al usuario `nova` dentro del proyecto `service`:

```bash
vagrant@controller01:~$ openstack role add --project service --user nova admin
```

Registraremos la entidad de servicio `nova` en Keystone:

```bash
vagrant@controller01:~$ openstack service create --name nova --description "OpenStack Compute" compute
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| id          | 28cdb92573e7483283b156df041352de |
| name        | nova                             |
| type        | compute                          |
| enabled     | True                             |
| description | OpenStack Compute                |
+-------------+----------------------------------+
```

## Crear los endpoints de la API (en `controller01`)

A continuación, crearemos los endpoints públicos, internos y de administración para el servicio de cómputo:

```bash
vagrant@controller01:~$ openstack endpoint create --region RegionOne compute public http://controller01:8774/v2.1
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | ff46aff4339b4ecfa650cbc08cc38816 |
| interface    | public                           |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 28cdb92573e7483283b156df041352de |
| service_name | nova                             |
| service_type | compute                          |
| url          | http://controller01:8774/v2.1      |
+--------------+----------------------------------+
vagrant@controller01:~$ openstack endpoint create --region RegionOne compute internal http://controller01:8774/v2.1
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | e65163fd3ebe48b69d7ec9982be66cf1 |
| interface    | internal                         |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 28cdb92573e7483283b156df041352de |
| service_name | nova                             |
| service_type | compute                          |
| url          | http://controller01:8774/v2.1      |
+--------------+----------------------------------+
vagrant@controller01:~$ openstack endpoint create --region RegionOne compute admin http://controller01:8774/v2.1
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | 6ef7e3b07f1a46b288ec200212c0547e |
| interface    | admin                            |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 28cdb92573e7483283b156df041352de |
| service_name | nova                             |
| service_type | compute                          |
| url          | http://controller01:8774/v2.1      |
+--------------+----------------------------------+
```

## Instalar y configurar los componentes de Nova (en `controller01`)

Instalaremos los paquetes del controlador necesarios en este nodo:

```bash
vagrant@controller01:~$ sudo apt install nova-api nova-conductor nova-novncproxy nova-scheduler -y
```

Editaremos el archivo `/etc/nova/nova.conf` para aplicar los siguientes cambios:

### Sección `[api_database]` y `[database]`

Configuraremos las cadenas de conexión a las bases de datos creadas (sustituye `NOVA_DBPASS` por la contraseña definida):

```bash
[api_database]
connection = mysql+pymysql://nova:NOVA_DBPASS@controller01/nova_api

[database]
connection = mysql+pymysql://nova:NOVA_DBPASS@controller01/nova
```

### Sección `[DEFAULT]`

En la sección `[DEFAULT]`, indicaremos la conexión a RabbitMQ y la IP de gestión del controlador (`my_ip`):

```bash
[DEFAULT]
transport_url = rabbit://openstack:RABBIT_PASS@controller01:5672/
my_ip = 10.0.0.2
```

### Sección `[keystone_authtoken]`

Configuraremos el acceso a Keystone para la validación de tokens:

```bash
[keystone_authtoken]
www_authenticate_uri = http://controller01:5000/
auth_url = http://controller01:5000/
memcached_servers = controller01:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = nova
password = NOVA_PASS
```

### Sección `[service_user]`

Habilitaremos el token de servicio y definiremos el endpoint v3:

```bash
[service_user]
send_service_user_token = true
auth_url = http://controller01:5000/v3
auth_type = password
project_domain_name = Default
project_name = service
user_domain_name = Default
username = nova
password = NOVA_PASS
```

### Sección `[vnc]`

Configuraremos VNC para que utilice la IP de gestión:

```bash
[vnc]
enabled = true
server_listen = $my_ip
server_proxyclient_address = $my_ip
```

### Sección `[glance]`

Definiremos la URL del servicio Glance para que Nova pueda recuperar las imágenes:

```bash
[glance]
api_servers = http://controller01:9292
```

### Sección `[oslo_concurrency]`

Definiremos el directorio para los bloqueos temporales:

```bash
[oslo_concurrency]
lock_path = /var/lib/nova/tmp
```

### Sección `[placement]`

Conectaremos Nova con el servicio Placement (sustituye `PLACEMENT_PASS` por la contraseña definida):

```bash
[placement]
region_name = RegionOne
project_domain_name = Default
project_name = service
auth_type = password
user_domain_name = Default
auth_url = http://controller01:5000/v3
username = placement
password = PLACEMENT_PASS
```

## Inicializar las bases de datos de Nova (en `controller01`)

Ejecutaremos los comandos de `nova-manage` para sincronizar los esquemas y crear la celda adicional:

```bash
vagrant@controller01:~$ sudo su -s /bin/sh -c "nova-manage api_db sync" nova
vagrant@controller01:~$ sudo su -s /bin/sh -c "nova-manage cell_v2 map_cell0" nova
vagrant@controller01:~$ sudo su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --verbose" nova
vagrant@controller01:~$ sudo su -s /bin/sh -c "nova-manage db sync" nova
```

Verificaremos que las celdas se hayan registrado correctamente:

```bash
vagrant@controller01:~$ sudo su -s /bin/sh -c "nova-manage cell_v2 list_cells" nova
+-------+--------------------------------------+------------------------------------------+-------------------------------------------------+----------+
|  Name |                 UUID                 |              Transport URL               |               Database Connection               | Disabled |
+-------+--------------------------------------+------------------------------------------+-------------------------------------------------+----------+
| cell0 | 00000000-0000-0000-0000-000000000000 |                  none:/                  | mysql+pymysql://nova:****@controller/nova_cell0 |  False   |
| cell1 | 29e1ed74-59fa-43e3-9651-999d592a2cdf | rabbit://openstack:****@controller01:5672/ |    mysql+pymysql://nova:****@controller/nova    |  False   |
+-------+--------------------------------------+------------------------------------------+-------------------------------------------------+----------+
```

## Finalizar la instalación (en `controller01`)

Reiniciaremos los servicios de Nova para aplicar la nueva configuración:

```bash
vagrant@controller01:~$  sudo service nova-api restart
vagrant@controller01:~$  sudo service nova-scheduler restart
vagrant@controller01:~$  sudo service nova-conductor restart
vagrant@controller01:~$  sudo service nova-novncproxy restart
```