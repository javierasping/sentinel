---
title: "13 - Verificar la instalación mínima de OpenStack"
date: 2025-11-23T12:00:00+00:00
description: "Comprobación end-to-end: agentes, redes, router, imagen, instancia, IP flotante y conectividad."
tags: [openstack,instalacion,verificacion]
hero: images/openstack/instalacion-manual/verificar-intalacion-minima.png
weight: 13
---

En este post realizamos una comprobación de extremo a extremo desde el nodo controlador (`controller01`). Primero verificamos los agentes de red, luego creamos la red y la subred internas, configuramos un router, preparamos la red externa, revisamos imagen y flavor, generamos un par de claves, lanzamos una instancia y validamos la conectividad (ICMP/SSH) mediante IP flotante. Mantenemos salidas reales para comparar.

Antes de comenzar cargamos nuestras credenciales (si no están ya en el entorno):

```bash
source ~/admin-openrc
```

## Paso 1: Verificar agentes de red

Comprobamos que los agentes Neutron (linuxbridge, DHCP, L3, metadata) estén vivos y en estado UP:

```bash
vagrant@controller01:~$ openstack network agent list
```

Salida de ejemplo:

```
+------------------+------------------+--------------+-------------------+-------+-------+------------------+
| ID               | Agent Type       | Host         | Availability Zone | Alive | State | Binary           |
+------------------+------------------+--------------+-------------------+-------+-------+------------------+
| 94434668-d4b3-   | Linux bridge     | controller01 | None              | :-)   | UP    | neutron-         |
| 4960-8363-       | agent            |              |                   |       |       | linuxbridge-     |
| 54c1be53d0a5     |                  |              |                   |       |       | agent            |
| a2717b0e-fd22-   | Linux bridge     | compute01    | None              | :-)   | UP    | neutron-         |
| 4e52-910c-       | agent            |              |                   |       |       | linuxbridge-     |
| 556f3ad29a67     |                  |              |                   |       |       | agent            |
| ca0e8819-add4-   | DHCP agent       | controller01 | nova              | :-)   | UP    | neutron-dhcp-    |
| 4c03-991f-       |                  |              |                   |       |       | agent            |
| 35d2f5bf112d     |                  |              |                   |       |       |                  |
| d121bb9a-d44d-   | L3 agent         | controller01 | nova              | :-)   | UP    | neutron-l3-agent |
| 4ae0-829e-       |                  |              |                   |       |       |                  |
| 6623d17e8e13     |                  |              |                   |       |       |                  |
| d6849ebc-86f2-   | Metadata agent   | controller01 | None              | :-)   | UP    | neutron-         |
| 4ed2-80fc-       |                  |              |                   |       |       | metadata-agent   |
| cf3f9fce7d76     |                  |              |                   |       |       |                  |
+------------------+------------------+--------------+-------------------+-------+-------+------------------+
```

Nota: si algún agente aparece como DOWN, revisa sus logs en `/var/log/neutron/`.

## Paso 2: Crear red interna y subred

Creamos la red de proyecto `test-net` que usará la instancia:

```bash
vagrant@controller01:~$ openstack network create test-net
```

Salida de ejemplo (puede variar el `id` y `provider:segmentation_id`):

```
+---------------------------+--------------------------------------+
| Field                     | Value                                |
+---------------------------+--------------------------------------+
| admin_state_up            | UP                                   |
| availability_zone_hints   |                                      |
| availability_zones        |                                      |
| created_at                | 2025-11-02T23:19:16Z                 |
| description               |                                      |
| dns_domain                | None                                 |
| id                        | f3b76e27-fe00-4ad1-88a1-fd3528c4e412 |
| mtu                       | 1450                                 |
| name                      | test-net                             |
| port_security_enabled     | True                                 |
| project_id                | 69782314638942ef831e8754cda5e41d     |
| provider:network_type     | vxlan                                |
| provider:physical_network | None                                 |
| provider:segmentation_id  | 612                                  |
| router:external           | Internal                             |
| shared                    | False                                |
| status                    | ACTIVE                               |
+---------------------------+--------------------------------------+
```

Creamos la subred `test-subnet` dentro de la red (definimos rango y gateway):

```bash
vagrant@controller01:~$ openstack subnet create --network test-net --subnet-range 192.168.50.0/24 test-subnet
```

Salida de ejemplo:

```
+----------------------+--------------------------------------+
| Field                | Value                                |
+----------------------+--------------------------------------+
| allocation_pools     | 192.168.50.2-192.168.50.254          |
| cidr                 | 192.168.50.0/24                      |
| created_at           | 2025-11-02T23:19:21Z                 |
| enable_dhcp          | True                                 |
| gateway_ip           | 192.168.50.1                         |
| id                   | 6f9e499d-6b04-4f92-b4fa-3f4c4df225f5 |
| ip_version           | 4                                    |
| name                 | test-subnet                          |
| network_id           | f3b76e27-fe00-4ad1-88a1-fd3528c4e412 |
| router:external      | False                                |
| status               | ACTIVE                               |
+----------------------+--------------------------------------+
```

## Paso 3: Crear router y asociar la subred

Creamos el router `test-router` que conectará la red interna con la externa:

```bash
vagrant@controller01:~$ openstack router create test-router
```

Salida de ejemplo inicial (sin gateway externo todavía):

```
+-------------------------+--------------------------------------+
| Field                   | Value                                |
+-------------------------+--------------------------------------+
| admin_state_up          | UP                                   |
| created_at              | 2025-11-02T23:19:25Z                 |
| distributed             | False                                |
| external_gateway_info   | null                                 |
| ha                      | False                                |
| id                      | 954c7398-6e05-42d9-bd81-2a780835b832 |
| name                    | test-router                          |
| status                  | ACTIVE                               |
+-------------------------+--------------------------------------+
```

Le añadimos la subred interna como interfaz para que gestione `192.168.50.0/24`:

```bash
vagrant@controller01:~$ openstack router add subnet test-router test-subnet
```

## Paso 4: Crear red externa y establecer puerta de enlace

Creamos la red externa `ext-net` (tipo flat) que representará la salida al exterior:

```bash
vagrant@controller01:~$ openstack network create --external \
    --provider-physical-network provider \
    --provider-network-type flat ext-net
```

Creamos la subred externa `ext-subnet` con su pool de IP flotantes:

```bash
vagrant@controller01:~$ openstack subnet create --network ext-net \
    --subnet-range 192.168.121.0/24 \
    --gateway 192.168.121.1 \
    --allocation-pool start=192.168.121.200,end=192.168.121.254 \
    --dns-nameserver 8.8.8.8 ext-subnet
```

Asociamos la red externa al router para habilitar SNAT y tráfico saliente:

```bash
vagrant@controller01:~$ openstack router set test-router --external-gateway ext-net
```

Verificamos los datos del router (debe mostrar `external_fixed_ips` y `enable_snat: true`):

```bash
vagrant@controller01:~$ openstack router show test-router
```

## Paso 5: Notas rápidas de diagnóstico

* Agente DOWN: revisar `/var/log/neutron/*` y comprobar servicio systemd.
* Error creando red externa: validar `bridge_mappings` y existencia del dispositivo físico / bridge.
* `No Network found for provider`: nombre mal escrito o falta definición en ML2.
* MTU baja / conectividad errática: comparar `mtu` de la red con la interfaz física y ajustar si procede.

## Paso 6: Imagen, flavor y par de claves

Verificamos que exista la imagen base (por ejemplo `cirros`):

```bash
vagrant@controller01:~$ openstack image list
```

Creamos un par de claves `testkey` y protegemos el fichero privado:

```bash
vagrant@controller01:~$ openstack keypair create testkey > testkey.pem
vagrant@controller01:~$ chmod 600 testkey.pem
```

Si no existe el flavor `m1.tiny`, lo creamos (RAM 512 MiB, disco 1 GiB, 1 vCPU):

```bash
openstack flavor create --id m1.tiny --ram 512 --disk 1 --vcpus 1 m1.tiny
```


Lanzamos la instancia `test-vm` en la red interna (el `net-id` corresponde a la red `test-net`; puede diferir en tu entorno):

```bash
vagrant@controller01:~$ openstack server create --flavor m1.tiny --image cirros --nic net-id=9d446c54-f58c-4301-a515-428598f460ca --security-group default --key-name testkey test-vm
```

Comprobamos que su estado pase de BUILD a ACTIVE:

```bash
openstack server list
openstack server show test-vm | grep -E "status|addresses|flavor|image"
```

Si se queda en BUILD/ERROR revisamos `openstack console log show test-vm` y los logs de Nova.

Si necesitamos acceso SSH/ICMP desde fuera, añadimos reglas al security group `default` (solo para laboratorio; en producción usar reglas mínimas necesarias):

```bash
openstack security group rule create --proto tcp --dst-port 22 default
openstack security group rule create --proto icmp default
```

Creamos una IP flotante y la asociamos (sustituye `<FLOATING_IP>` por la dirección asignada):

```bash
openstack floating ip create ext-net
openstack server add floating ip test-vm <FLOATING_IP>
```

## Paso 7: Acceder a la instancia y validar red

Accedemos por SSH usando la IP flotante (si la clave fallara, la contraseña por defecto de CirrOS es `gocubsgo`):

```bash
vagrant@controller01:~$ ssh -i .ssh/testkey.pem cirros@192.168.121.212
```

Verificamos la interfaz y el hostname dentro de la instancia:

```bash
$ ip -4 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc pfifo_fast qlen 1000
    inet 192.168.50.225/24 brd 192.168.50.255 scope global eth0
       valid_lft forever preferred_lft forever
$ hostname
test-vm
```

Comprobamos la conectividad con la puerta de enlace interna del router y con Internet:

```bash
$ ping 192.168.50.1 -c 1
PING 192.168.50.1 (192.168.50.1): 56 data bytes
64 bytes from 192.168.50.1: seq=0 ttl=64 time=0.650 ms

--- 192.168.50.1 ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max = 0.650/0.650/0.650 ms
$ ping 1.1.1.1 -c 1
PING 1.1.1.1 (1.1.1.1): 56 data bytes
64 bytes from 1.1.1.1: seq=0 ttl=54 time=9.840 ms

--- 1.1.1.1 ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max = 9.840/9.840/9.840 ms
```

## Paso 8: Validar conectividad desde el host

Desde el host físico validamos el ping a la IP flotante y confirmamos que la IP interna no es accesible (red aislada):

```bash
javiercruces@FJCD-PC:~/openstack-vagrant-ansible/manual-install (main) [prd-eu-west|]
$ ping -c 1 192.168.121.212
PING 192.168.121.212 (192.168.121.212) 56(84) bytes of data.
64 bytes from 192.168.121.212: icmp_seq=1 ttl=63 time=0.824 ms

--- 192.168.121.212 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.824/0.824/0.824/0.000 ms

javiercruces@FJCD-PC:~/openstack-vagrant-ansible/manual-install (main) [prd-eu-west|]
$ ping -c 1 192.168.50.225
PING 192.168.50.225 (192.168.50.225) 56(84) bytes of data.
^C
--- 192.168.50.225 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 0ms
```

Nota: la IP interna (192.168.50.x) está aislada por Neutron; solo la IP flotante es alcanzable desde fuera.

Con esto hemos comprobado que todos los componentes que hemos instalado funcionan perfectamente.