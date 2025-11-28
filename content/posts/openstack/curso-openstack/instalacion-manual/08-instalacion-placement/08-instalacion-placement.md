---
title: "08 - Configurar Placement en OpenStack"
date: 2025-11-23T12:00:00+00:00
description: "Configura el servicio Placement para la planificación y gestión de recursos en OpenStack."
tags: [openstack,instalacion,placement]
hero: ""
weight: 8
---

Placement realiza el seguimiento de los recursos físicos disponibles y ayuda a Nova a planificar asignaciones. En esta guía instalaré y configuraré Placement en `controller01` usando paquetes de Ubuntu y dejaré los pasos mínimos para verificar su funcionamiento.

## Requisitos previos

Antes de empezar, asegúrate de tener:

- Keystone instalado y accesible.
- Una base de datos MySQL/MariaDB disponible.
- Credenciales administrativas (`admin-openrc`) para crear usuarios y servicios.

## Crear la base de datos

Me conecto al servidor de base de datos como `root` para crear la base de datos de Placement:

```bash
vagrant@controller01:~$ sudo mysql
```

Creo la base de datos y doy permisos al usuario `placement` (sustituye `PLACEMENT_DBPASS`):

```sql
CREATE DATABASE placement;
GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'localhost' IDENTIFIED BY 'PLACEMENT_DBPASS';
GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'%' IDENTIFIED BY 'PLACEMENT_DBPASS';
```

Salgo del cliente cuando termine.

## Crear el usuario y los endpoints del servicio

Cargo mis credenciales de administrador para trabajar con la CLI de OpenStack:

```bash
vagrant@controller01:~$ source admin-openrc
```

Creo el usuario `placement` en Keystone (usa `PLACEMENT_PASSWORD` como contraseña de ejemplo):

```bash
vagrant@controller01:~$ openstack user create --domain default --password PLACEMENT_PASSWORD placement
+---------------------+----------------------------------+
| Field               | Value                            |
+---------------------+----------------------------------+
| default_project_id  | None                             |
| domain_id           | default                          |
| email               | None                             |
| enabled             | True                             |
| id                  | 5a18b6b3caa641d2905f6de876e786f3 |
| name                | placement                        |
| description         | None                             |
| password_expires_at | None                             |
+---------------------+----------------------------------+
```

Añado el rol `admin` al usuario dentro del proyecto `service`:

```bash
vagrant@controller01:~$ openstack role add --project service --user placement admin
```

Registro el servicio Placement en el catálogo de Keystone:

```bash
vagrant@controller01:~$ openstack service create --name placement --description "Placement API" placement
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| id          | 845aa6ed076f4adab229902844c50f9b |
| name        | placement                        |
| type        | placement                        |
| enabled     | True                             |
| description | Placement API                    |
+-------------+----------------------------------+
```

Creo los endpoints públicos, internos y admin apuntando al puerto 8778:

```bash
vagrant@controller01:~$ openstack endpoint create --region RegionOne placement public http://controller01:8778 
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | 74fee05c44b7436ab141ab81d2febc5b |
| interface    | public                           |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 845aa6ed076f4adab229902844c50f9b |
| service_name | placement                        |
| service_type | placement                        |
| url          | http://controller01:8778         |
+--------------+----------------------------------+
vagrant@controller01:~$ openstack endpoint create --region RegionOne placement internal http://controller01:8778
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | f7395645747e47298201d6620c7c1102 |
| interface    | internal                         |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 845aa6ed076f4adab229902844c50f9b |
| service_name | placement                        |
| service_type | placement                        |
| url          | http://controller01:8778         |
+--------------+----------------------------------+
vagrant@controller01:~$ openstack endpoint create --region RegionOne placement admin http://controller01:8778
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | 8cf1ef59f4114fa39ecbb011363e4648 |
| interface    | admin                            |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 845aa6ed076f4adab229902844c50f9b |
| service_name | placement                        |
| service_type | placement                        |
| url          | http://controller01:8778         |
+--------------+----------------------------------+
```

Nota: el puerto puede variar en tu entorno (por ejemplo 8780).

## Instalar los componentes

Instalo el paquete del servicio Placement:

```bash
vagrant@controller01:~$ sudo apt install placement-api -y
```

## Configurar Placement

Edito el fichero principal para apuntar a la base de datos y a Keystone:

```bash
vagrant@controller01:~$ sudo nano /etc/placement/placement.conf
```

En la sección de la base de datos configuro la cadena de conexión (sustituye `PLACEMENT_DBPASS`):

```ini
[placement_database]
connection = mysql+pymysql://placement:PLACEMENT_DBPASS@controller01/placement
```

En `[api]` y `[keystone_authtoken]` habilito Keystone y pongo las credenciales del servicio (reemplaza `PLACEMENT_PASS`):

```ini
[api]
auth_strategy = keystone

[keystone_authtoken]
auth_url = http://controller01:5000/v3
memcached_servers = controller:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = placement
password = PLACEMENT_PASS
```

Comenta o elimina opciones conflictivas si las encuentras.

## Sincronizar la base de datos

Ejecuto la creación de tablas con `placement-manage`:

```bash
vagrant@controller01:~$ sudo su -s /bin/sh -c "placement-manage db sync" placement
```

Puedes ignorar advertencias deprecatorias si no afectan al proceso.

## Finalizar la instalación

Reinicio Apache (Placement suele servirse mediante mod_wsgi):

```bash
vagrant@controller01:~$ sudo service apache2 restart
```

## Verificación

Compruebo el estado con `placement-status`:

```bash
vagrant@controller01:~$ sudo -u placement placement-status upgrade check
+-------------------------------------------+
| Upgrade Check Results                     |
+-------------------------------------------+
| Check: Missing Root Provider IDs          |
| Result: Success                           |
| Details: None                             |
+-------------------------------------------+
| Check: Incomplete Consumers               |
| Result: Success                           |
| Details: None                             |
+-------------------------------------------+
| Check: Policy File JSON to YAML Migration |
| Result: Success                           |
| Details: None                             |
+-------------------------------------------+
```

Y pruebo la API de Placement listando las clases de recursos:

```bash
vagrant@controller01:~$ openstack --os-placement-api-version 1.2 resource class list --sort-column name
+----------------------------------------+
| name                                   |
+----------------------------------------+
| DISK_GB                                |
| FPGA                                   |
| IPV4_ADDRESS                           |
| MEMORY_MB                              |
| MEM_ENCRYPTION_CONTEXT                 |
| NET_BW_EGR_KILOBIT_PER_SEC             |
| NET_BW_IGR_KILOBIT_PER_SEC             |
| NET_PACKET_RATE_EGR_KILOPACKET_PER_SEC |
| NET_PACKET_RATE_IGR_KILOPACKET_PER_SEC |
| NET_PACKET_RATE_KILOPACKET_PER_SEC     |
| NUMA_CORE                              |
| NUMA_MEMORY_MB                         |
| NUMA_SOCKET                            |
| NUMA_THREAD                            |
| PCI_DEVICE                             |
| PCPU                                   |
| PGPU                                   |
| SRIOV_NET_VF                           |
| VCPU                                   |
| VGPU                                   |
| VGPU_DISPLAY_HEAD                      |
+----------------------------------------+
```

Si obtienes una lista (aunque vacía) sin errores, Placement está operativo.