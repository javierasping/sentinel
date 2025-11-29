---
title: "11 - Configurar Neutron en el nodo controlador"
date: 2025-11-23T12:00:00+00:00
description: "Guía completa para configurar Neutron, el servicio de redes de OpenStack, en el controlador."
tags: [openstack,instalacion,neutron]
hero: images/openstack/instalacion-manual/instalar-configurar-neutron-controlador.png
weight: 11
---

En esta página instalo y configuro el servicio de red Neutron en el nodo controlador (`controller01`). Neutron gestiona las redes virtuales, routers, subredes y demás componentes de networking para las instancias.

## Requisitos previos

Antes de empezar, asegúrate de tener:

- Keystone instalado y accesible.
- Una base de datos MySQL/MariaDB disponible.
- Credenciales administrativas (`admin-openrc`) para crear usuarios y servicios.

### Crear la base de datos

Me conecto al servidor de base de datos como `root` para crear la base de datos de Neutron:

1. Accedo al cliente SQL:

```bash
vagrant@controller01:~$ sudo mysql           
```

2. Creo la base de datos `neutron`:

```sql
MariaDB [(none)]> CREATE DATABASE neutron;
```

3. Concedo los permisos al usuario `neutron` (sustituye `NEUTRON_DBPASS` por tu contraseña):

```sql
MariaDB [(none)]> GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'localhost' \
  IDENTIFIED BY 'NEUTRON_DBPASS';
MariaDB [(none)]> GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'%' \
  IDENTIFIED BY 'NEUTRON_DBPASS';
```

4. Salgo del cliente cuando termine.

### Crear el usuario y los endpoints del servicio

Cargo mis credenciales de administrador para trabajar con la CLI de OpenStack:

1. Cargo las variables de entorno:

```bash
vagrant@controller01:~$ source admin-openrc 
```

2. Creo el usuario `neutron` en Keystone (usa `NEUTRON_PASSWORD` como contraseña de ejemplo):

```bash
vagrant@controller01:~$ openstack user create --domain default --password NEUTRON_PASSWORD neutron

+---------------------+----------------------------------+
| Field               | Value                            |
+---------------------+----------------------------------+
| default_project_id  | None                             |
| domain_id           | default                          |
| email               | None                             |
| enabled             | True                             |
| id                  | 9d9e34ba52904f8c91ecd20e481aa649 |
| name                | neutron                          |
| description         | None                             |
| password_expires_at | None                             |
+---------------------+----------------------------------+
```

3. Añado el rol `admin` al usuario `neutron` dentro del proyecto `service`:

```bash
vagrant@controller01:~$ openstack role add --project service --user neutron admin
```

4. Registro el servicio Neutron en el catálogo de Keystone:

```bash
vagrant@controller01:~$ openstack service create --name neutron --description "OpenStack Networking" network
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| id          | ff5a9465f4b54499bf503a490babb9cd |
| name        | neutron                          |
| type        | network                          |
| enabled     | True                             |
| description | OpenStack Networking             |
+-------------+----------------------------------+
```

5. Creo los endpoints públicos, internos y admin apuntando al puerto 9696:

```bash
vagrant@controller01:~$ openstack endpoint create --region RegionOne network public http://controller01:9696
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | 0daf60c82a71419cb743be39a74db328 |
| interface    | public                           |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | ff5a9465f4b54499bf503a490babb9cd |
| service_name | neutron                          |
| service_type | network                          |
| url          | http://controller01:9696           |
+--------------+----------------------------------+
vagrant@controller01:~$ openstack endpoint create --region RegionOne network internal http://controller01:9696 
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | 06db6d1bbedc48d0a54f24a8f3657f6b |
| interface    | internal                         |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | ff5a9465f4b54499bf503a490babb9cd |
| service_name | neutron                          |
| service_type | network                          |
| url          | http://controller01:9696           |
+--------------+----------------------------------+
vagrant@controller01:~$ openstack endpoint create --region RegionOne network admin http://controller01:9696
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | 9f2dc6c761014193b99e0662f27b840b |
| interface    | admin                            |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | ff5a9465f4b54499bf503a490babb9cd |
| service_name | neutron                          |
| service_type | network                          |
| url          | http://controller01:9696           |
+--------------+----------------------------------+
```

## Instalar y configurar los componentes de Neutron

Instalo los paquetes de Neutron en el nodo controlador:

```bash
vagrant@controller01:~$ sudo apt install -y neutron-server neutron-plugin-ml2 neutron-linuxbridge-agent neutron-l3-agent neutron-dhcp-agent neutron-metadata-agent

```

### Configurar el archivo principal de Neutron

Edito `/etc/neutron/neutron.conf` y configuro las secciones clave.

En `[database]` establezco la cadena de conexión a MariaDB (sustituye `NEUTRON_DBPASS`):

```bash
[database]
connection = mysql+pymysql://neutron:NEUTRON_DBPASS@controller01/neutron
```

En `[DEFAULT]` activo ML2, el plugin de ruteo y la conexión a RabbitMQ (sustituye `RABBIT_PASS`):

```bash
[DEFAULT]
core_plugin = ml2
service_plugins = router
allow_overlapping_ips = true
transport_url = rabbit://openstack:RABBIT_PASS@controller
notify_nova_on_port_status_changes = true
notify_nova_on_port_data_changes = true
```

En `[api]` y `[keystone_authtoken]` configuro la autenticación con Keystone (reemplaza `NEUTRON_PASS`):

```bash
[api]
auth_strategy = keystone


[keystone_authtoken]
www_authenticate_uri = http://controller01:5000
auth_url = http://controller01:5000
memcached_servers = controller01:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = neutron
password = NEUTRON_PASS
```

En `[nova]` indico cómo Neutron se autentica frente a Nova (sustituye `NOVA_PASS`):

```bash
[nova]
auth_url = http://controller01:5000
auth_type = password
project_domain_name = Default
user_domain_name = Default
region_name = RegionOne
project_name = service
username = nova
password = NOVA_PASS
```

En `[oslo_concurrency]` defino la ruta de bloqueo:

```bash
[oslo_concurrency]
lock_path = /var/lib/neutron/tmp
```

### Configurar el plugin Modular Layer 2 (ML2)

ML2 conecta los tipos de red con el mecanismo (linuxbridge). Edito `/etc/neutron/plugins/ml2/ml2_conf.ini` para habilitar drivers y tipos.

En `[ml2]` activo flat, VLAN y VXLAN:

```bash
[ml2]
type_drivers = flat,vlan,vxlan
tenant_network_types = vxlan
mechanism_drivers = linuxbridge,l2population
extension_drivers = port_security
```

Defino la red flat llamada `provider`:

```bash
[ml2_type_flat]
flat_networks = provider
```

Configuro el rango VNI para VXLAN:

```bash
[ml2_type_vxlan]
vni_ranges = 1:1000

[securitygroup]
enable_security_group = true
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
```

### Configurar Linux Bridge Agent

En `/etc/neutron/plugins/ml2/linuxbridge_agent.ini` indico la interfaz física y la IP local para VXLAN:

```bash
[linux_bridge]
# La interfaz por la que tus máquinas saldrán a la red externa
physical_interface_mappings = provider:eth0

[vxlan]
enable_vxlan = true
local_ip = 10.0.0.2
l2_population = true

[securitygroup]
enable_security_group = true
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
```

### Configurar L3 Agent

En `/etc/neutron/l3_agent.ini` uso el driver de linuxbridge:

```bash
[DEFAULT]
interface_driver = linuxbridge
```

### Configurar DHCP Agent

En `/etc/neutron/dhcp_agent.ini` activo el driver de linuxbridge y Dnsmasq:

```bash
[DEFAULT]
interface_driver = linuxbridge
dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq
enable_isolated_metadata = true
```

### Configurar Metadata Agent

En `/etc/neutron/metadata_agent.ini` indico el host de Nova y la clave compartida:

```bash
[DEFAULT]
nova_metadata_host = controller01
metadata_proxy_shared_secret = openstack
```

### Configurar Nova para usar Neutron

En `/etc/nova/nova.conf` configuro la sección `[neutron]` para que Nova use el servicio de red:

```bash
[neutron]
url = http://controller01:9696
auth_url = http://controller01:5000
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = neutron
password = openstack
service_metadata_proxy = true
metadata_proxy_shared_secret = openstack
```

### Poblar la base de datos de Neutron

Ejecuto las migraciones para crear las tablas necesarias:

```bash
sudo su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron
```

Si todo va bien verás mensajes de alembic aplicando las migraciones y finalmente `OK`:

```bash
INFO  [alembic.runtime.migration] Running upgrade a8b517cff8ab -> 3b935b28e7a0
INFO  [alembic.runtime.migration] Running upgrade 3b935b28e7a0 -> b12a3ef66e62
INFO  [alembic.runtime.migration] Running upgrade b12a3ef66e62 -> 97c25b0d2353
INFO  [alembic.runtime.migration] Running upgrade 97c25b0d2353 -> 2e0d7a8a1586
INFO  [alembic.runtime.migration] Running upgrade 2e0d7a8a1586 -> 5c85685d616d
  OK
```

## Reiniciar servicios y comprobar agentes

Reinicio los servicios para aplicar la configuración:

```bash
sudo service nova-api restart
sudo service neutron-server restart
sudo service neutron-linuxbridge-agent restart
sudo service neutron-dhcp-agent restart
sudo service neutron-metadata-agent restart
sudo service neutron-l3-agent restart
```

Compruebo el estado de los agentes con:

```bash
vagrant@controller01:~$ openstack network agent list
```

Deberías ver los agentes `Linux bridge`, `DHCP`, `L3` y `Metadata` en estado `UP`:

```bash
+--------------------------------------+--------------------+--------------+-------------------+-------+-------+---------------------------+
| ID                                   | Agent Type         | Host         | Availability Zone | Alive | State | Binary                    |
+--------------------------------------+--------------------+--------------+-------------------+-------+-------+---------------------------+
| 94434668-d4b3-4960-8363-54c1be53d0a5 | Linux bridge agent | controller01 | None              | :-)   | UP    | neutron-linuxbridge-agent |
| ca0e8819-add4-4c03-991f-35d2f5bf112d | DHCP agent         | controller01 | nova              | :-)   | UP    | neutron-dhcp-agent        |
| d121bb9a-d44d-4ae0-829e-6623d17e8e13 | L3 agent           | controller01 | nova              | :-)   | UP    | neutron-l3-agent          |
| d6849ebc-86f2-4ed2-80fc-cf3f9fce7d76 | Metadata agent     | controller01 | None              | :-)   | UP    | neutron-metadata-agent    |
+--------------------------------------+--------------------+--------------+-------------------+-------+-------+---------------------------+

```