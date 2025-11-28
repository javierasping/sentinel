---
title: "10 - Instalar y configurar Nova en nodos de cómputo"
date: 2025-11-23T12:00:00+00:00
description: "Aprende a configurar los nodos de cómputo de OpenStack para gestionar instancias virtuales."
tags: [openstack,instalacion,nova]
hero: ""
weight: 10
---

En esta página configuro un nodo de cómputo (por ejemplo `compute01`) para que pueda ejecutar instancias con Nova. Uso QEMU/KVM cuando el hardware lo soporta; si no, dejo configurado QEMU puro.

Antes de empezar, asegúrate de:

- Haber añadido el nombre e IP del controlador en `/etc/hosts` del nodo de cómputo.
- Disponer de las credenciales del servicio (`admin-openrc`) y de acceso al servidor de bases de datos.

## Instalación y configuración de los componentes (en el nodo de cómputo)

Instalo el paquete principal del servicio de cómputo en el nodo:

```bash
vagrant@compute01:~$ sudo apt install nova-compute -y
```

Edito el fichero `/etc/nova/nova.conf` y apunto las cadenas de conexión a las bases de datos del controlador:

```ini
[database]
connection = mysql+pymysql://nova:NOVA_DBPASS@controller01/nova

[api_database]
connection = mysql+pymysql://nova:NOVA_DBPASS@controller01/nova_api
```

Configuro la conexión con RabbitMQ (reemplaza `RABBIT_PASS`) y otras opciones por defecto:

```ini
[DEFAULT]
transport_url = rabbit://openstack:RABBIT_PASS@controller01
```

Configuro las credenciales del servicio (usuario `nova`) para que el nodo pueda autenticarse contra Keystone:

```ini
[service_user]
send_service_user_token = true
auth_url = http://controller01:5000/v3/
auth_type = password
project_domain_name = Default
project_name = service
user_domain_name = Default
username = nova
password = NOVA_PASS
```

Indico la IP de gestión del nodo en `my_ip` (sustituye `IP_GESTION_NODO_COMPUTO`, en mi ejemplo `10.0.0.3`):

```ini
[DEFAULT]
my_ip = IP_GESTION_NODO_COMPUTO
```

Configuro el apartado VNC para que el proxy use la IP del controlador y el servidor escuche en todas las interfaces:

```
[vnc]
enabled = true
server_listen = 0.0.0.0
server_proxyclient_address = $my_ip
novncproxy_base_url = http://controller01:6080/vnc_auto.html
```

Apunto Nova a Glance y configuro el lock_path:

```ini
[glance]
api_servers = http://controller01:9292

[oslo_concurrency]
lock_path = /var/lib/nova/tmp

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

En la sección de autenticación con Keystone configuro el token middleware (reemplaza `<NOVA_PASSWORD>` si procede):

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
password = <NOVA_PASSWORD>
identity_api_version = 3
```

## Finalizar instalación (en el nodo de cómputo)

Compruebo si el nodo soporta virtualización por hardware y, si no, fuerzo QEMU:

```bash
egrep -c '(vmx|svm)' /proc/cpuinfo
```

Si el resultado es 0, establezco `virt_type=qemu` en `/etc/nova/nova-compute.conf`:

```ini
[libvirt]
virt_type = qemu
```

Reinicio el servicio `nova-compute` para aplicar la configuración:

```bash
vagrant@compute01:~$ sudo service nova-compute restart
```

## Añadir el nodo de cómputo a la base de datos de celdas (ejecutar en el controlador)

Cargo las credenciales de administrador en el controlador y busco hosts sin mapear:

```bash
vagrant@controller01:~$ source admin-openrc 
```

Compruebo si nuestro controlador detecta nodos de cómputo pendientes de ser añadidos:

```bash
vagrant@controller01:~$ sudo su -s /bin/sh -c "nova-manage cell_v2 discover_hosts --verbose" nova
Found 2 cell mappings.
Skipping cell0 since it does not contain hosts.
Getting computes from cell 'cell1': 29e1ed74-59fa-43e3-9651-999d592a2cdf
Checking host mapping for compute host 'compute01': d83ec732-f31c-4358-9326-610b9e660974
Creating host mapping for compute host 'compute01': d83ec732-f31c-4358-9326-610b9e660974
Found 1 unmapped computes in cell: 29e1ed74-59fa-43e3-9651-999d592a2cdf
```

Verifico que el nodo aparece como servicio `nova-compute`:

```bash
vagrant@controller01:~$ openstack compute service list --service nova-compute
+--------------------------+--------------+-----------+------+---------+-------+---------------------------+
| ID                       | Binary       | Host      | Zone | Status  | State | Updated At                |
+--------------------------+--------------+-----------+------+---------+-------+---------------------------+
| a6dda039-f310-4b5b-ae5e- | nova-compute | compute01 | nova | enabled | up    | 2025-11-                  |
| 606a4d89592a             |              |           |      |         |       | 02T19:51:01.000000        |
+--------------------------+--------------+-----------+------+---------+-------+---------------------------+
```

Nota: cada vez que añadas un nuevo nodo debes ejecutar `discover_hosts` en el controlador, o habilitar la detección periódica añadiendo en `/etc/nova/nova.conf`:

```ini
[scheduler]
discover_hosts_in_cells_interval = 300
```
