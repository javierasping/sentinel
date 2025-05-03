---
title: "Instalación y configuración de un servidor DHCP en Linux"
date: 2023-09-08T10:00:00+00:00
description: Configuración del servidor DHCP en nuestro escenario básico bajo Debian 10
tags: [Servicios, NAT, SMR, DHCP, SNAT]
hero: images/servicios/dhcp_v4/isc-dhcp.webp
---

# Configuración del servidor DHCP bajo Debian

En este artículo aprenderás cómo configurar el servidor DHCP `isc-dhcp-server`. Además, configuraremos una reserva de IP y lo configuraremos para que funcione en dos ámbitos diferentes.

En mi caso esta es la configuración de red de mi servidor DHCP .

```bash
# Red externa del router
auto ens4
iface ens4 inet dhcp

# Red interna 1
auto ens5 
iface ens5 inet static 
        address 192.168.10.1
        netmask 255.255.255.0

# Red interna 2
auto ens6 
iface ens6 inet static 
        address 192.168.20.1
        netmask 255.255.255.0

```

## Instalación del servidor isc-dhcp-server

Para instalar el servidor DHCP en Debian, ejecutamos el siguiente comando:

```bash
sudo apt update && sudo apt install isc-dhcp-server
```

Cuando APT acabe , te devolverá un error indicando que el servicio esta mal configurado , puedes ignorarlo ya que a continuación vamos a realizar la configuración del mismo.

## Configuración del servicio isc-dhcp-server

Lo primero que debemos hacer es configurar la interfaz de red por la que va a operar el servidor DHCP. Para ello, editamos el archivo de configuración de la interfaz:

```bash
sudo nano /etc/default/isc-dhcp-server
```

Añadimos la interfaz que distribuirá las direcciones IP, por ejemplo para la red1 seria:

```bash
INTERFACESv4="ens5"
```

Luego configuramos el servidor DHCP con las siguientes características:

- Rango de direcciones a repartir: `192.168.10.100 - 192.168.0.110`
- Máscara de red: `255.255.255.0`
- Duración de la concesión: 1 hora
- Puerta de enlace: `192.168.10.1`
- Servidores DNS: `8.8.8.8`

Editamos el archivo de configuración de `isc-dhcp-server`:

```bash
sudo nano /etc/dhcp/dhcpd.conf
```

Dentro de este , los parámetros mas importantes son :

- max-lease-time: Tiempo de la concesión de la dirección IP
- default-lease-time: Tiempo de renovación de la concesión
- option routers: Indicamos la dirección red de la puerta de enlace que se utiliza para salir a internet.
- option domain-name-server: Se pone las direcciones IP de los servidores DNS que va a utilizar el cliente.
- option domain­-name: Nombre del dominio que se manda al cliente.
- option subnet­mask: Subred enviada a los clientes.
- option broadcast-­address: Dirección de difusión de la red.

En mi caso , dentro del fichero añadiré el siguiente código para configurar la red1:

```plaintext
subnet 192.168.10.0 netmask 255.255.255.0 {
  range 192.168.10.100 192.168.10.110;
  option routers 192.168.10.1;
  option domain-name-servers 8.8.8.8;
  default-lease-time 3600;
  max-lease-time 3600;
}
```

Con esta configuración, el servidor DHCP proporcionará direcciones dentro del rango indicado y asignará la puerta de enlace y el servidor DNS especificados.

Para aplicar los cambios, reiniciamos el servicio de DHCP:

```bash
sudo systemctl restart isc-dhcp-server
```

## Configuración de los clientes para obtener un direccionamiento dinámico

Para que los clientes obtengan direcciones IP de manera dinámica, debemos asegurarnos de que sus configuraciones de red estén configuradas para usar DHCP.

### En un cliente Debian

Editamos la configuración de red para usar DHCP. Primero, abrimos el archivo `/etc/network/interfaces`:

```bash
sudo nano /etc/network/interfaces
```

Asegúrate de que la configuración de la interfaz se vea de esta manera:

```bash
auto ens4 
iface ens4 inet dhcp 
```

Reiniciamos la interfaz de red para aplicar los cambios:

```bash
debian@cliente1:~$ sudo ifdown ens4 && sudo ifup ens4
```

Veremos que al hacer esto , nos mostrara la salida del cliente DHCP del proceso que ha seguido para configurarse :

```bash
ifdown: interface ens4 not configured
Internet Systems Consortium DHCP Client 4.4.3-P1
Copyright 2004-2022 Internet Systems Consortium.
All rights reserved.
For info, please visit https://www.isc.org/software/dhcp/

Listening on LPF/ens4/0c:07:6b:9a:00:00
Sending on   LPF/ens4/0c:07:6b:9a:00:00
Sending on   Socket/fallback
Created duid "\000\001\000\001/\251\\\227\014\007k\232\000\000".
DHCPDISCOVER on ens4 to 255.255.255.255 port 67 interval 8
DHCPOFFER of 192.168.10.100 from 192.168.10.1
DHCPREQUEST for 192.168.10.100 on ens4 to 255.255.255.255 port 67
DHCPACK of 192.168.10.100 from 192.168.10.1
bound to 192.168.10.100 -- renewal in 1479 seconds.
```

Viendo la salida anterior , podemos ver que configuración nos ha dado el servidor DHCP , pero también podemos comprobarla con varios comandos . Como por ejemplo :

```bash
debian@cliente1:~$ ip -4 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: ens4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    altname enp0s4
    inet 192.168.10.100/24 brd 192.168.10.255 scope global dynamic ens4
       valid_lft 3508sec preferred_lft 3508sec
```


> 💡 **Tip:**  
> En el caso de que quieras modificar la configuración del DHCP o simplemente volver a solicitar la configuración al servidor DHCP estos comandos te serán de utilidad.
> En sistemas Windows, el comando `ipconfig /release` libera la concesión DHCP actual, mientras que `ipconfig /renew` solicita una nueva.  
> En sistemas Linux, la liberación se realiza con `dhclient -r` y la renovación con `dhclient`.

## Comprobación de las concesiones de direcciones

Para ver las concesiones de direcciones en el servidor, abrimos el archivo de registros de DHCP, que normalmente se encuentra en:

```bash
debian@router:~$ sudo cat /var/lib/dhcp/dhcpd.leases
# The format of this file is documented in the dhcpd.leases(5) manual page.
# This lease file was written by isc-dhcp-4.4.3-P1

# authoring-byte-order entry is generated, DO NOT DELETE
authoring-byte-order little-endian;

server-duid "\000\001\000\001/\251[u\014\306\312)\000\001";

lease 192.168.10.100 {
  starts 6 2025/05/03 23:00:40;
  ends 0 2025/05/04 00:00:40;
  cltt 6 2025/05/03 23:00:40;
  binding state active;
  next binding state free;
  rewind binding state free;
  hardware ethernet 0c:07:6b:9a:00:00;
  uid "\377k\232\000\000\000\001\000\001/\251\\\227\014\007k\232\000\000";
  client-hostname "cliente1";
}
```

Es importante no editar este archivo manualmente, ya que cualquier modificación puede causar problemas en el servidor DHCP.

## Reserva de una dirección IP

Para reservar una dirección IP para un cliente específico, editamos el archivo de configuración del servidor DHCP:

```bash
sudo nano /etc/dhcp/dhcpd.conf
```

Añadimos la siguiente configuración para reservar una dirección IP basada en la dirección MAC del cliente:

```bash
host nombre_cliente {
  hardware ethernet 00:11:22:33:44:55;
  fixed-address 192.168.10.120;
}
```

Una vez añadida la reserva, reiniciamos el servicio DHCP:

```bash
sudo systemctl restart isc-dhcp-server
```

Comprobamos en el cliente (Windows o Linux) si la IP reservada ha sido asignada correctamente utilizando el comando `ipconfig` o `ip a`.


## Configurar dos ámbitos

Si queremos que el servidor DHCP administre direcciones para dos redes diferentes, como `192.168.10.0` y `192.168.20.0`, debemos agregar una nueva interfaz de red.

Añadimos la nueva interfaz de red al archivo `/etc/default/isc-dhcp-server`:

```bash
INTERFACESv4="ens5 ens6"
```

Luego configuramos un segundo rango de direcciones en el archivo de configuración de `isc-dhcp-server`:

```bash
sudo nano /etc/dhcp/dhcpd.conf
```

Añadimos lo siguiente:

```plaintext
subnet 192.168.20.0 netmask 255.255.255.0 {
  range 192.168.20.100 192.168.2.110;
  option routers 192.168.20.1;
  option domain-name-servers 8.8.8.8;
  default-lease-time 3600;
  max-lease-time 3600;
}
```

Finalmente, reiniciamos el servicio DHCP:

```bash
sudo systemctl restart isc-dhcp-server
```

Ahora veras en los clientes de esta segunda red que el servicio DHCP les ha asignado la configuración de red configurada .