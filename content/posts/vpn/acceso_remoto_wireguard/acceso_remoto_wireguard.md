---
title: "VPN acceso remoto Wireguard"
date: 2024-03-28T10:00:00+00:00
description: VPN acceso remoto Wireguard
tags: [VPN,CISCO,LINUX,DEBIAN,WIREGUARD]
hero: /images/vpn/wireguard_acceso_remoto.png
---



![](../img/Pastedimage20240114150833.png)

En primer lugar configurare la maquina servidor1  como servidor VPN de acceso remoto y servidor2 como cliente VPN . Posteriormente configurare un cliente Windows y Android . 

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

Una vez generado las claves , vamos a proceder a configurar el servidor de acceso remoto Wireguard , en mi caso voy a llamar al fichero de configuración wg0.conf . Voy a añadirte en cada parámetro de la configuración un comentario para que sepas que tienes que poner en cada campo : 

```bash
debian@servidor1:~$ sudo cat /etc/wireguard/wg0.conf
[Interface]
# IP que tendrá el túnel VPN , en concreto la interfaz wg0 que es como has llamado el fichero de conf 
Address = 10.99.99.1
#Clave privada del servidor
PrivateKey = 2Gg3EnKD+rdyMPEjMikZTwq2w0m78KrEcUsAJ/8icFA=
#Puerto de escucha , 51820 es el puerto por defecto de Wireguard
ListenPort = 51820

# Si no tienes activado el bit de forwarding por defecto puedes hacerlo asi :
PreUp = sysctl -w net.ipv4.ip_forward=1

# Este apartado hace referencia a la configuración de los clientes :
[Peer]
#Clave pública del cliente
Publickey = gS2ED2zfzMHBttMpFhH3MvRpr8D4ALEDTumNcib8A2g=
#IP del túnel VPN del cliente
AllowedIPs = 10.99.99.2/32
#Tiempo de espera que tendrá activo el túnel si no hay trafico
PersistentKeepAlive = 25
```

Ahora configuraremos un cliente debian  , le he dado el mismo nombre al fichero de configuración por lo que la interfaz también se llamara wg0 :

```bash
debian@servidor2:~$ sudo cat /etc/wireguard/wg0.conf
  [Interface]
    Address = 10.99.99.2/24
    #Clave privada del cliente
    PrivateKey = 8IdsSwunfU5zJQzS5nZg4D//cFEbRa+27HGOQE1V90k=
    #Puerto de escucha del servidor
    ListenPort = 51820

    [Peer]
    #Clave pública del servidor
    PublicKey = 2/RjGUbiQuaFR7atYaQ8lcczz2wXxO9aIwfzZEMPXCQ=
    AllowedIPs = 0.0.0.0/0
    #Punto de acceso del servidor
    Endpoint = 90.0.0.2:51820
    #Tiempo de espera de la conexión
    PersistentKeepalive = 25
```

Una vez tenemos configurados ambos ficheros levantaremos el túnel , para ello tenemos varias formas de hacerlo , personalmente la mas cómoda que veo es usando el comando wg-quick .

Levantamos el túnel en el servidor :

```bash
debian@servidor1:~$ sudo wg-quick up wg0
[#] sysctl -w net.ipv4.ip_forward=1
net.ipv4.ip_forward = 1
[#] ip link add wg0 type wireguard
[#] wg setconf wg0 /dev/fd/63
[#] ip -4 address add 10.99.99.1 dev wg0
[#] ip link set mtu 1420 up dev wg0
[#] ip -4 route add 10.99.99.2/32 dev wg0
```

Levantamos el otro extremo , en este caso nuestro cliente es servidor2 :

```bash
debian@servidor2:~$ sudo wg-quick up wg0
[#] ip link add wg0 type wireguard
[#] wg setconf wg0 /dev/fd/63
[#] ip -4 address add 10.99.99.2/24 dev wg0
[#] ip link set mtu 1420 up dev wg0
[#] wg set wg0 fwmark 51820
[#] ip -4 route add 0.0.0.0/0 dev wg0 table 51820
[#] ip -4 rule add not fwmark 51820 table 51820
[#] ip -4 rule add table main suppress_prefixlength 0
[#] sysctl -q net.ipv4.conf.all.src_valid_mark=1
[#] iptables-restore -n
```

Una vez hecho esto comprobaremos que en ambos extremos se nos ha creado una nueva interfaz , que se llama igual que nuestro fichero de configuración sin la extensión .conf .

Comprobamos que se haya creado en servidor1 :

```bash
debian@servidor1:~$ ip -4 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    altname enp0s3
    inet 90.0.0.2/24 brd 90.0.0.255 scope global ens3
       valid_lft forever preferred_lft forever
3: ens4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    altname enp0s4
    inet 192.168.0.1/24 brd 192.168.0.255 scope global ens4
       valid_lft forever preferred_lft forever
6: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 10.99.99.1/32 scope global wg0
       valid_lft forever preferred_lft forever
```

Comprobamos que se haya creado en servidor2 :

```bash
debian@servidor2:~$ ip -4 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    altname enp0s3
    inet 100.0.0.2/24 brd 100.0.0.255 scope global ens3
       valid_lft forever preferred_lft forever
3: ens4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    altname enp0s4
    inet 192.168.1.1/24 brd 192.168.1.255 scope global ens4
       valid_lft forever preferred_lft forever
6: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 10.99.99.2/24 scope global wg0
       valid_lft forever preferred_lft forever
```

También comprobaremos las rutas que se nos ha creado en el servidor y en el cliente : 

```bash
debian@servidor1:~$ ip r
default via 90.0.0.1 dev ens3 onlink 
10.99.99.2 dev wg0 scope link 
10.99.99.4 dev wg0 scope link 
90.0.0.0/24 dev ens3 proto kernel scope link src 90.0.0.2 
192.168.0.0/24 dev ens4 proto kernel scope link src 192.168.0.1 

debian@servidor2:~$ ip r
default via 100.0.0.1 dev ens3 onlink 
10.99.99.0/24 dev wg0 proto kernel scope link src 10.99.99.2 
100.0.0.0/24 dev ens3 proto kernel scope link src 100.0.0.2 
192.168.1.0/24 dev ens4 proto kernel scope link src 192.168.1.1 
```


Vamos a comprobar que desde nuestro cliente (servidor2) tenemos acceso a las distintas maquinas de nuestra red :

```bash
## Ping con el túnel del extremo servidor1
debian@servidor2:~$ ping 10.99.99.1 -c 1
PING 10.99.99.1 (10.99.99.1) 56(84) bytes of data.
64 bytes from 10.99.99.1: icmp_seq=1 ttl=64 time=14.9 ms

--- 10.99.99.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 14.862/14.862/14.862/0.000 ms

## Pings con cliente1 :
debian@servidor2:~$ ping 192.168.0.2 -c 1
PING 192.168.0.2 (192.168.0.2) 56(84) bytes of data.
64 bytes from 192.168.0.2: icmp_seq=1 ttl=63 time=17.5 ms

--- 192.168.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 17.503/17.503/17.503/0.000 ms

# Ping con cliente2
debian@servidor2:~$ ping 192.168.0.3 -c 1
PING 192.168.0.3 (192.168.0.3) 56(84) bytes of data.
64 bytes from 192.168.0.3: icmp_seq=1 ttl=63 time=16.5 ms

--- 192.168.0.3 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 16.522/16.522/16.522/0.000 ms

## Ping con la ip privada del servidor1
debian@servidor2:~$ ping 192.168.0.1 -c 1
PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.
64 bytes from 192.168.0.1: icmp_seq=1 ttl=64 time=20.3 ms

--- 192.168.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 20.272/20.272/20.272/0.000 ms
```

Aunque como esta montado mi escenario , las direcciones IP privadas no están erutadas vamos a comprobar que el trafico va por el túnel , haciendo uso de traceroute : 

```bash
debian@servidor2:~$ traceroute 192.168.0.2
traceroute to 192.168.0.2 (192.168.0.2), 30 hops max, 60 byte packets
 1  10.99.99.1 (10.99.99.1)  18.692 ms  28.987 ms  28.951 ms
 2  192.168.0.2 (192.168.0.2)  28.912 ms  28.877 ms  28.859 ms
```


#### Configuración cliente android 

La maquina virtual de android es bastante incomoda de controlar , así que voy a generarle las claves y su fichero de configuración en el servidor1 . Posteriormente se lo haremos llegar descargandonoslo de este con apache .

Nos generamos las claves para android :

```bash
debian@servidor1:~$ wg genkey | tee androidprivate | wg pubkey > androidpublic
debian@servidor1:~$ cat androidprivate 
CBY5o2iko7xXQrNAFcFDIKohOngawB1uvws7aDDgl0g=
debian@servidor1:~$ cat androidpublic 
cBGl5QWOsbZyI2GN1MXDxUsfeMmI5sKnp3VkxW9lO3g=
```

El fichero de configuración seria el siguiente :

```bash
debian@servidor1:~$ sudo cat android.conf 
[Interface]
Address = 10.99.99.4
PrivateKey = CBY5o2iko7xXQrNAFcFDIKohOngawB1uvws7aDDgl0g=
ListenPort = 51820
  
[Peer]
Publickey = 2/RjGUbiQuaFR7atYaQ8lcczz2wXxO9aIwfzZEMPXCQ=
AllowedIPs = 0.0.0.0/0
Endpoint = 90.0.0.2:51820
```

Me he instalado apache y copiare este archivo al document root para hacerlo llegar a la maquina android . Uso este medio ya que es un escenario ficticio . 

```bash
debian@servidor1:~$ sudo cp android.conf /var/www/html/
```

Desde una terminal , ya que el navegador no funciona demasiado bien nos descargamos el fichero :
![](../img/Pastedimage20240127122826.png)

Ahora vamos a añadir en el fichero de configuración del servidor este nuevo cliente :

```bash
debian@servidor1:~$ sudo cat /etc/wireguard/wg0.conf
#Al final del todo :)
[Peer]
Publickey = cBGl5QWOsbZyI2GN1MXDxUsfeMmI5sKnp3VkxW9lO3g=
AllowedIPs = 10.99.99.4/32
PersistentKeepAlive = 25
```

No olvides reiniciar el túnel :

```bash
debian@servidor1:~$ sudo wg-quick down wg0
debian@servidor1:~$ sudo wg-quick up wg0
```

Ahora abre la aplicación de wireguard y dale a importar desde archivo y activa la conexión . Activa el túnel y asegúrate de que se produce el handshake : 

![](../img/Pastedimage20240127123150.png)

Si abrimos una terminal podremos hacerle pings a los clientes :

![](../img/Pastedimage20240127123551.png)

#### Configuración del cliente Windows

Vamos a repetir el proceso pero ahora con nuestro cliente Windows . 

Para poder copiar y pegar voy a realizar la generación de claves de este cliente en la maquina servidor1 . 

Comenzaremos generando el par de claves

```bash
debian@servidor1:~$ wg genkey | tee winprivate | wg pubkey > winpublic

debian@servidor1:~$ cat winprivate 
QKGQEdrB9FBYRZsLNgc3qr9m8/lx+uc9n5vvj67I9m8=

debian@servidor1:~$ cat winpublic 
E8VdupsWJ7vCTO7SF3oXUciUrsRgJ3p6T+F5UbbLngo=
```

Nos creamos el fichero de configuración para este cliente :

```bash
debian@servidor1:~$ cat win.conf 
[Interface]
Address = 10.99.99.5
PrivateKey = QKGQEdrB9FBYRZsLNgc3qr9m8/lx+uc9n5vvj67I9m8=
ListenPort = 51820
  
[Peer]
Publickey = 2/RjGUbiQuaFR7atYaQ8lcczz2wXxO9aIwfzZEMPXCQ=
AllowedIPs = 0.0.0.0/0
Endpoint = 90.0.0.2:51820
```

Lo moveré al document root para poder descargarlo en mi Windows , no hagas esto en un entorno real .

```bash
debian@servidor1:~$ sudo cp win.conf /var/www/html/
```

Recuerda configurar en la maquina servidor1 este nuevo cliente :

```bash
debian@servidor1:~$ sudo nano /etc/wireguard/wg0.conf

[Peer]
Publickey = E8VdupsWJ7vCTO7SF3oXUciUrsRgJ3p6T+F5UbbLngo=
AllowedIPs = 10.99.99.5/32
PersistentKeepAlive = 25
```

Para que se apliquen los cambios reinicia el túnel :

```bash
debian@servidor1:~$ sudo wg-quick down wg0
debian@servidor1:~$ sudo wg-quick up wg0
```

Una vez tenemos todo configurado , accede a la maquina Windows y descargate el fichero de configuración : 

![](../img/Pastedimage20240127124840.png)

Abre la aplicación de wireguard y selecciona importar desde archivo :

![](../img/Pastedimage20240127124507.png)

Una vez añadido activa el túnel y comprueba que se ha producido el handshake :

![](../img/Pastedimage20240127125205.png)


Si volvemos a nuestro Windows , se nos habrá creado una nueva interfaz :

![](../img/Pastedimage20240127125336.png)

Y tendremos conectividad con las maquinas de la red 192.168.0.0/24 :

![](../img/Pastedimage20240127125609.png)

A modo de curiosidad podemos ver en el servidor que clientes están conectados :

```bash
debian@servidor1:~$ sudo wg show
interface: wg0
  public key: 2/RjGUbiQuaFR7atYaQ8lcczz2wXxO9aIwfzZEMPXCQ=
  private key: (hidden)
  listening port: 51820

peer: cBGl5QWOsbZyI2GN1MXDxUsfeMmI5sKnp3VkxW9lO3g=
  endpoint: 100.0.0.2:51820
  allowed ips: 10.99.99.4/32
  latest handshake: 1 minute, 14 seconds ago
  transfer: 6.43 KiB received, 788 B sent
  persistent keepalive: every 25 seconds

peer: E8VdupsWJ7vCTO7SF3oXUciUrsRgJ3p6T+F5UbbLngo=
  endpoint: 100.0.0.2:49981
  allowed ips: 10.99.99.5/32
  latest handshake: 1 minute, 32 seconds ago
  transfer: 46.23 KiB received, 1.64 KiB sent
  persistent keepalive: every 25 seconds

peer: gS2ED2zfzMHBttMpFhH3MvRpr8D4ALEDTumNcib8A2g=
  allowed ips: 10.99.99.2/32
  persistent keepalive: every 25 seconds

```
