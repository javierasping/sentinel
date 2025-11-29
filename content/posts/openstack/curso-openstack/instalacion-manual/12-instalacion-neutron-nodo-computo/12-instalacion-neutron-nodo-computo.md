---
title: "12 - Configurar Neutron en nodos de cómputo"
date: 2025-11-23T12:00:00+00:00
description: "Aprende a conectar tus nodos de cómputo a la red virtual de OpenStack con Neutron."
tags: [openstack,instalacion,neutron]
hero: images/openstack/instalacion-manual/instalar-configurar-neutron-computo.png
weight: 12
---

En esta página configuro Neutron en el nodo de cómputo (`compute01`). El nodo de cómputo gestiona la conectividad de red y los grupos de seguridad para las instancias que se ejecutan en él.

## Requisitos previos

Antes de empezar, asegúrate de haber completado todos los post anteriores.

## Instalar los componentes

Instalo el agente Linux bridge en el nodo de cómputo:

```bash
vagrant@compute01:~$ sudo apt install -y neutron-linuxbridge-agent
```

## Configurar el componente común

Edito `/etc/neutron/neutron.conf` para configurar la autenticación y la cola de mensajes.

En `[DEFAULT]` configuro el acceso a RabbitMQ y la estrategia de autenticación:

```bash
[DEFAULT]
transport_url = rabbit://openstack:RABBIT_PASS@controller01
auth_strategy = keystone
```

En `[keystone_authtoken]` configuro la autenticación con Keystone:

```bash
[keystone_authtoken]
auth_uri = http://controller01:5000
auth_url = http://controller01:5000
memcached_servers = controller01:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = neutron
password = NEUTRON_PASS
```

En `[oslo_concurrency]` defino la ruta de bloqueo:

```bash
[oslo_concurrency]
lock_path = /var/lib/neutron/tmp
```

## Configurar el agente Linux Bridge

El agente Linux bridge construye la infraestructura de red virtual y gestiona los grupos de seguridad para las instancias.

Edito `/etc/neutron/plugins/ml2/linuxbridge_agent.ini` y configuro las opciones.

En `[linux_bridge]` asigno la interfaz física que se mapea a la red proveedora (en este caso `eth0`):

```bash
[linux_bridge]
physical_interface_mappings = provider:eth0
```

En `[vxlan]` habilito VXLAN para redes de autoservicio y configuro la IP local para el tráfico VXLAN (sustituye `10.0.0.3` por la IP de gestión de tu nodo de cómputo):

```bash
[vxlan]
enable_vxlan = true
local_ip = 10.0.0.3
l2_population = true
```

En `[securitygroup]` activo los grupos de seguridad y configuro el firewall de iptables:

```bash
[securitygroup]
enable_security_group = true
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
```

## Configurar Nova para usar Neutron

Edito `/etc/nova/nova.conf` para que Nova use Neutron en este nodo.

En `[neutron]` configuro los parámetros de acceso:

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
password = NEUTRON_PASS
```

## Reiniciar servicios y comprobar agentes

Reinicio los servicios para aplicar la configuración:

```bash
vagrant@compute01:~$ sudo service nova-compute restart
vagrant@compute01:~$ sudo service neutron-linuxbridge-agent restart
```

Desde el controlador compruebo que todos los agentes están activos:

```bash
vagrant@controller01:~$ openstack network agent list
```

Deberías ver el agente `Linux bridge` del nodo de cómputo (`compute01`) en estado `UP`, además de los agentes del controlador:

```bash
vagrant@controller01:~$ openstack network agent list
+------------------+------------------+--------------+-------------------+-------+-------+------------------+
| ID               | Agent Type       | Host         | Availability Zone | Alive | State | Binary           |
+------------------+------------------+--------------+-------------------+-------+-------+------------------+
| 5103a975-977d-   | Linux bridge     | compute01    | None              | :-)   | UP    | neutron-         |
| 4adb-885c-       | agent            |              |                   |       |       | linuxbridge-     |
| d51cb92bf2de     |                  |              |                   |       |       | agent            |
| 52a6a02e-6e7a-   | L3 agent         | controller01 | nova              | :-)   | UP    | neutron-l3-agent |
| 43a6-ac66-       |                  |              |                   |       |       |                  |
| 85d27c779a6f     |                  |              |                   |       |       |                  |
| 58d07bea-0a2e-   | Metadata agent   | controller01 | None              | :-)   | UP    | neutron-         |
| 499d-89d1-       |                  |              |                   |       |       | metadata-agent   |
| fa3705f6c0cb     |                  |              |                   |       |       |                  |
| ce87bffc-ab25-   | Linux bridge     | controller01 | None              | :-)   | UP    | neutron-         |
| 431e-99d1-       | agent            |              |                   |       |       | linuxbridge-     |
| 55d13cc69a04     |                  |              |                   |       |       | agent            |
| d705285c-b40a-   | DHCP agent       | controller01 | nova              | :-)   | UP    | neutron-dhcp-    |
| 4041-bbb6-       |                  |              |                   |       |       | agent            |
| 3e8be304f156     |                  |              |                   |       |       |                  |
+------------------+------------------+--------------+-------------------+-------+-------+------------------+
```