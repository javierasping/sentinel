---
title: "VPN site to site Wireguard"
date: 2024-03-28T10:00:00+00:00
description: VPN site to site Wireguard
tags: [VPN,CISCO,LINUX,DEBIAN,WIREGUARD]
hero: /images/vpn/wireguard.png
---



![](../img/Pastedimage20240114150833.png)

> [!NOTE]  
> Voy a partir del post de VPN acceso remoto con Wireguard , asi que es posible que haga referencia a este durante este articulo .

## Generación de claves

Lo primero que haremos sera instalarnos tanto en ambas maquinas el paquete Wireguard :

```bash
root@servidor1:~# sudo apt update && sudo apt install wireguard
debian@servidor2:~$ sudo apt update && sudo apt install wireguard
```

Vamos a generar los pares de claves que se utilizarán para cifrar la conexión. Necesitaremos una clave para el servidor y un par de  claves adicionales por cada cliente.

Comenzaremos con el par de claves del servidor1:

```bash
debian@servidor1:~$ wg genkey | sudo tee /etc/wireguard/server_private.key | wg pubkey | sudo tee /etc/wireguard/server_public.key
2/RjGUbiQuaFR7atYaQ8lcczz2wXxO9aIwfzZEMPXCQ=

# Puedes visualizar la clave privada posteriormente :
debian@servidor1:~$ sudo cat /etc/wireguard/server_private.key
2Gg3EnKD+rdyMPEjMikZTwq2w0m78KrEcUsAJ/8icFA=

# Puedes visualizar la clave publica posteriormente :
debian@servidor1:~$ sudo cat /etc/wireguard/server_public.key
2/RjGUbiQuaFR7atYaQ8lcczz2wXxO9aIwfzZEMPXCQ=

```

Nos desplazamos al servidor2 y les generamos las suyas  :

```bash
# Generamos el par de claves para el cliente de acceso remoto servidor2
debian@servidor2:~$ wg genkey | sudo tee /etc/wireguard/client_private.key | wg pubkey | sudo tee /etc/wireguard/client_public.key
gS2ED2zfzMHBttMpFhH3MvRpr8D4ALEDTumNcib8A2g=

# Puedes visualizar la clave privada posteriormente :
debian@servidor2:~$ sudo cat /etc/wireguard/client_private.key
8IdsSwunfU5zJQzS5nZg4D//cFEbRa+27HGOQE1V90k=

# Puedes visualizar la clave publica posteriormente :
debian@servidor2:~$ sudo cat /etc/wireguard/client_public.key
gS2ED2zfzMHBttMpFhH3MvRpr8D4ALEDTumNcib8A2g=
```

## Configuración de Wireguard

Vamos a modificar el archivo de configuración en la máquina servidor1. La única modificación necesaria será en el parámetro "AllowedIPs", donde debemos agregar la dirección de red a la que nos conectaremos. Además, incluiremos en el campo "Peer Endpoint" la dirección IP de la otra máquina, ya que ambas actuarán como servidores en esta configuración.

```bash
debian@servidor1:~$ sudo cat /etc/wireguard/wg0.conf
[Interface]
Address = 10.99.99.1
PrivateKey = 2Gg3EnKD+rdyMPEjMikZTwq2w0m78KrEcUsAJ/8icFA=
ListenPort = 51820

[Peer]
Publickey = gS2ED2zfzMHBttMpFhH3MvRpr8D4ALEDTumNcib8A2g=
AllowedIPs = 10.99.99.2/32,192.168.1.0/24
PersistentKeepAlive = 25
Endpoint = 100.0.0.2:51820
```

Lo mismo para la maquina servidor2 , la configuración quedaría así:

```bash
debian@servidor2:~$ sudo cat /etc/wireguard/wg0.conf
[Interface]
Address = 10.99.99.2/24
PrivateKey = 8IdsSwunfU5zJQzS5nZg4D//cFEbRa+27HGOQE1V90k=
ListenPort = 51820

[Peer]
PublicKey = 2/RjGUbiQuaFR7atYaQ8lcczz2wXxO9aIwfzZEMPXCQ=
AllowedIPs = 10.99.99.1/32,192.168.0.0/24
Endpoint = 90.0.0.2:51820
PersistentKeepalive = 25
```

Como yo tengo levantado los túneles del ejercicio anterior los bajaremos y los subiremos para que se aplique la nueva configuración : 

```bash
debian@servidor1:~$ sudo wg-quick down wg0
debian@servidor2:~$ sudo wg-quick down wg0

debian@servidor1:~$ sudo wg-quick up wg0
debian@servidor1:~$ sudo wg-quick up wg0
```

Comprobaremos que en ambos servidores se ha creado la interfaz wg0 , que es la que nos corresponde por el nombre del fichero de configuración : 

```bash
debian@servidor1:~$ sudo ip link show wg0
11: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/none 
    
debian@servidor2:~$ sudo ip link show wg0
11: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/none 
```

A continuación voy a mostrarte las tablas de enroutamiento de los 2 servidores para que veas que se han creado rutas para llegar a ambas redes privadas por la interfaz wg0: 

```bash
debian@servidor1:~$ ip r
default via 90.0.0.1 dev ens3 onlink 
10.99.99.2 dev wg0 scope link 
90.0.0.0/24 dev ens3 proto kernel scope link src 90.0.0.2 
192.168.0.0/24 dev ens4 proto kernel scope link src 192.168.0.1 
192.168.1.0/24 dev wg0 scope link 

debian@servidor2:~$ ip r
default via 100.0.0.1 dev ens3 onlink 
10.99.99.0/24 dev wg0 proto kernel scope link src 10.99.99.2 
100.0.0.0/24 dev ens3 proto kernel scope link src 100.0.0.2 
192.168.0.0/24 dev wg0 scope link 
192.168.1.0/24 dev ens4 proto kernel scope link src 192.168.1.1 
```

### Comprobación de funcionamiento
  
Ahora, ambas redes privadas están completamente conectadas, lo que nos permite acceder desde cualquiera de las dos a la otra. Vamos a llevar a cabo algunas pruebas desde los clientes para asegurarnos de que la conexión esté funcionando correctamente.

Voy a hacer un ping desde la red 192.168.0.0 a la 192.168.1.0 con cliente1 :

```bash
# cliente1 --> servidor2
debian@cliente1:~$ ping 192.168.1.1 -c 1
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=63 time=17.6 ms

--- 192.168.1.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 17.554/17.554/17.554/0.000 ms

# Cliente1 --> Cliente 3
debian@cliente1:~$ ping 192.168.1.2 -c 1
PING 192.168.1.2 (192.168.1.2) 56(84) bytes of data.
64 bytes from 192.168.1.2: icmp_seq=1 ttl=62 time=12.9 ms
debian@cliente1:~$ ping 192.168.1.1 -c 1
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=63 time=17.8 ms

--- 192.168.1.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 17.803/17.803/17.803/0.000 ms

# Cliente1 --> Windows
debian@cliente1:~$ ping 192.168.1.5 -c 1
PING 192.168.1.5 (192.168.1.5) 56(84) bytes of data.
64 bytes from 192.168.1.5: icmp_seq=1 ttl=126 time=19.9 ms

--- 192.168.1.5 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 19.906/19.906/19.906/0.000 ms

# Cliente1 --> Android
debian@cliente1:~$ ping 192.168.1.4 -c 1
PING 192.168.1.4 (192.168.1.4) 56(84) bytes of data.
64 bytes from 192.168.1.4: icmp_seq=1 ttl=62 time=20.8 ms

--- 192.168.1.4 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 20.834/20.834/20.834/0.000 ms
```

Como ves tengo conectividad desde cualquier cliente de la red 192.168.0.0 con la 192.168.1.0 .

Vamos a comprobarlo en la dirección contraria , es decir desde la red 192.168.1.0 hacia la 192.168.0.0 :

```bash
# Cliente3 --> Servidor1
debian@cliente3:~$ ping 192.168.0.1 -c 1
PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.
64 bytes from 192.168.0.1: icmp_seq=1 ttl=63 time=16.6 ms

--- 192.168.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 16.581/16.581/16.581/0.000 ms

# Cliente3 --> Cliente1
debian@cliente3:~$ ping 192.168.0.2 -c 1
PING 192.168.0.2 (192.168.0.2) 56(84) bytes of data.
64 bytes from 192.168.0.2: icmp_seq=1 ttl=62 time=21.0 ms

--- 192.168.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 21.031/21.031/21.031/0.000 ms

# Cliente3 --> Cliente2
debian@cliente3:~$ ping 192.168.0.3 -c 1
PING 192.168.0.3 (192.168.0.3) 56(84) bytes of data.
64 bytes from 192.168.0.3: icmp_seq=1 ttl=62 time=16.1 ms

--- 192.168.0.3 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 16.115/16.115/16.115/0.000 ms
```

Para cerciorarnos de que el trafico esta pasando por el túnel en los 2 extremos vamos a hacer un traceroute desde las 2 redes :

Desde la red 192.168.0.0 a la 192.168.1.0 :

```bash
debian@cliente1:~$ traceroute 192.168.1.2
traceroute to 192.168.1.2 (192.168.1.2), 30 hops max, 60 byte packets
 1  192.168.0.1 (192.168.0.1)  0.629 ms  0.601 ms  0.595 ms
 2  10.99.99.2 (10.99.99.2)  13.677 ms  13.667 ms  13.657 ms
 3  192.168.1.2 (192.168.1.2)  13.649 ms  13.636 ms  13.626 ms
```

Desde la red 192.168.1.0 a la 192.168.0.0 :

```bash
debian@cliente3:~$ traceroute 192.168.0.3 
traceroute to 192.168.0.3 (192.168.0.3), 30 hops max, 60 byte packets
 1  192.168.1.1 (192.168.1.1)  0.430 ms  0.399 ms  0.393 ms
 2  10.99.99.1 (10.99.99.1)  19.343 ms  19.337 ms  19.329 ms
 3  192.168.0.3 (192.168.0.3)  19.324 ms  19.320 ms  19.313 ms
```

