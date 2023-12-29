---
title: "Gestión de redes"
date: 2023-09-08T10:00:00+00:00
description: Gestión de redes en OpenStack
tags: [OpenStack, CloudComputing, Instancias, OpenStackCLI, ServiciosEnLaNube, NAT, redes]
hero: images/openstack/taller1/taller1_2.png
---

<!-- https://fp.josedomingo.org/sri/5_iaas/taller3.html -->

En este post, vamos a explorar cómo manejar las redes privadas en OpenStack. Aprenderemos sobre la administración de routers, cómo conectar instancias en diferentes redes y cómo gestionar los puertos de red .

Puedes encontrar apuntes de este post en la pagina web de mi profesor Jose Domingo https://github.com/josedom24/curso_openstack_ies .


##  Taller 3: Gestión de redes en OpenStack

1.Los comandos OSC para crear la red red-externa.

```bash

(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$  openstack network create red-externa
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack subnet create --network red-externa --subnet-range 192.168.0.0/24 --dns-nameserver 172.22.0.1 red-externa_subred
```

2.Los comandos OSC y sus salidas, para visualizar las redes que tienes en tu proyecto y los routers.

```bash
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack router list
+--------------------------------------+-------------------------+--------+-------+----------------------------------+
| ID                                   | Name                    | Status | State | Project                          |
+--------------------------------------+-------------------------+--------+-------+----------------------------------+
| 46260c60-83fb-42f2-805c-3c42469a7531 | router de javier.cruces | ACTIVE | UP    | 83eb5116df714c9b86735f43b85146e9 |
| f06ea14d-a359-426d-b318-6f8ed8385bac | router-red-externa      | ACTIVE | UP    | 83eb5116df714c9b86735f43b85146e9 |
+--------------------------------------+-------------------------+--------+-------+----------------------------------+
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack network list
+--------------------------------------+----------------------+--------------------------------------+
| ID                                   | Name                 | Subnets                              |
+--------------------------------------+----------------------+--------------------------------------+
| 13049974-7a0f-4f82-b363-459e5149041c | red de javier.cruces | 00fc9fae-65a3-4e5b-8190-3ecb34b04496 |
| 2ebd4d15-00e3-44c6-a9a7-aeebef5f6540 | ext-net              | fedce2ca-083e-4df8-bf1c-abbf4ab19cd1 |
| f545c38d-ce09-4795-af2d-a922f4d640f1 | red-externa          | 0ae8c97e-d2b4-491f-85ed-2b0c5bc84c21 |
+--------------------------------------+----------------------+--------------------------------------+

```

3.Cuando crees la instancia maquina-router, accede a ella y comprueba la IP fija que ha tomando. Responde: ¿Has podido añadir una IP flotante a esta nueva instancia? Razona la respuesta.

```bash
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack floating ip create ext-net
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack server add floating ip maquina-router 172.22.200.47

(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ ssh debian@172.22.200.47

debian@maquina-router:~$ ip -4 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc fq_codel state UP group default qlen 1000
    altname enp0s3
    inet 192.168.0.187/24 metric 100 brd 192.168.0.255 scope global dynamic ens3
       valid_lft 86245sec preferred_lft 86245sec

```

4.Comandos OSC para conectar la maquina-router a la red-interna y que tenga la dirección 10.0.100.1.

```bash

(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack network create red-interna
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack subnet create --network red-interna --subnet-range 10.0.100.0/24 --dhcp --dns-nameserver 172.22.0.1 --gateway 10.0.100.1 subnet-red-interna
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$  openstack port create --network red-interna --fixed-ip ip-address=10.0.100.1 puerto1_red_interna
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack server add port maquina-router puerto1_red_interna

debian@maquina-router:~$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc fq_codel state UP group default qlen 1000
    link/ether fa:16:3e:fe:91:b6 brd ff:ff:ff:ff:ff:ff
    altname enp0s3
    inet 192.168.0.183/24 metric 100 brd 192.168.0.255 scope global dynamic ens3
       valid_lft 86393sec preferred_lft 86393sec
    inet6 fe80::f816:3eff:fefe:91b6/64 scope link 
       valid_lft forever preferred_lft forever
3: ens7: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc fq_codel state UP group default qlen 1000
    link/ether fa:16:3e:34:33:2e brd ff:ff:ff:ff:ff:ff
    altname enp0s7
    inet 10.0.100.1/24 metric 100 brd 10.0.100.255 scope global dynamic ens7
       valid_lft 86393sec preferred_lft 86393sec
    inet6 fe80::f816:3eff:fe34:332e/64 scope link 
       valid_lft forever preferred_lft forever

```

5.Comandos OSC para crear la maquina-cliente con la dirección 10.0.100.200. Responde: ¿Has podido añadir una IP flotante a esta nueva instancia? Razona la respuesta.

No se puede añadir un ip externa ya que en esta red no hay ningun router de openstack para hacerle DNAT

```bash
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack port create --network red-interna --fixed-ip ip-address=10.0.100.200 puerto-maquina-cliente

(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack server create --flavor m1.normal --image 017ae8f0-114e-4770-9df9-7e8b8f24199d --key-name jcruces --nic port-id=04158916-1620-4c8f-8963-80e3ceb904f6 maquina-cliente


debian@maquina-cliente:~$ ip r 
default via 10.0.100.1 dev ens3 proto dhcp src 10.0.100.200 metric 100 
10.0.100.0/24 dev ens3 proto kernel scope link src 10.0.100.200 metric 100 
10.0.100.1 dev ens3 proto dhcp scope link src 10.0.100.200 metric 100 
10.0.100.2 dev ens3 proto dhcp scope link src 10.0.100.200 metric 100 
169.254.169.254 via 10.0.100.2 dev ens3 proto dhcp src 10.0.100.200 metric 100 
172.22.0.1 via 10.0.100.1 dev ens3 proto dhcp src 10.0.100.200 metric 100 

```

6.Comandos OSC para deshabilitar la seguridad de los puertos de la red-interna.

```bash
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack server remove security group maquina-router default
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack server remove security group maquina-cliente default
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack port set --disable-port-security puerto-maquina-cliente
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack port set --disable-port-security puerto1_red_interna
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack port set --disable-port-security 69e2d6c0-f3e2-4169-89b8-f7dbcc27edf8
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack router set --route destination=10.0.100.0/24,gateway=192.168.0.217 router-red-externa
```

7.Comprobación de que la maquina-cliente tiene conexión al exterior.

```bash
debian@maquina-cliente:~$ ping 1.1.1.1
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
64 bytes from 1.1.1.1: icmp_seq=1 ttl=51 time=47.2 ms
64 bytes from 1.1.1.1: icmp_seq=2 ttl=51 time=47.4 ms
^C
--- 1.1.1.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 47.229/47.312/47.396/0.083 ms
debian@maquina-cliente:~$ 

```

8.Comprobación del acceso al servidor web de la maquina-cliente desde el exterior.


[](../img/acceso_web_cliente_dnat.png)