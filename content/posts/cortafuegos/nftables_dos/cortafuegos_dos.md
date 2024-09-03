---
title: "Implementación de un cortafuegos perimetral con Nftables II"
date: 2024-03-28T10:00:00+00:00
description: Implementación de un cortafuegos perimetral con Nftables II
tags: [FIREWALL,LINUX,DEBIAN,NFTABLES]
hero: /images/cortafuegos/nftables.png
---




Sobre el escenario creado en el módulo de servicios con las máquinas Odin (Router), Hela (DMZ), Loki y Thor (LAN) y empleando nftables, configura un cortafuegos perimetral en la máquina Odin de forma que el escenario siga funcionando completamente teniendo en cuenta los siguientes puntos:

    • Se valorará la creación de cadenas diferentes para cada flujo de tráfico (de LAN al exterior, de LAN a DMZ, etc…).
    • Política por defecto DROP para todas las cadenas.
    • Se pueden usar las extensiones que creamos adecuadas, pero al menos debe implementarse seguimiento de la conexión cuando sea necesario.
    • Debemos implementar que el cortafuegos funcione después de un reinicio de la máquina.
    • Debes mostrar pruebas de funcionamiento de todas las reglas.

Para no hacer demasiado larga la practica , voy a mostrarte los hits de las reglas al final , así como el script completo de las reglas . Ya que solo te pondré en cada ejercicio las reglas que intervienen y una comprobación del mismo .

## Montar el escenario con Nftables

Voy a eliminar iptables y vamos a pasar a Nftables para que no perdamos ninguna funcionalidad del escenario .

Lo primero sera crear las tablas y cadenas :

```bash
javiercruces@odin:~$ sudo nft add table inet filter

javiercruces@odin:~$ sudo nft add chain inet filter input { type filter hook input priority 0 \; counter \; policy accept \; }
javiercruces@odin:~$ sudo nft add chain inet filter output { type filter hook output priority 0 \; counter \; policy accept \; }
javiercruces@odin:~$ sudo nft add chain inet filter WAN_LAN { type filter hook forward priority 0\; counter \; policy accept \;}
javiercruces@odin:~$ sudo nft add chain inet filter WAN_DMZ { type filter hook forward priority 0\; counter \; policy accept \;}
javiercruces@odin:~$ sudo nft add chain inet filter LAN_WAN { type filter hook forward priority 0\; counter \; policy accept \;}
javiercruces@odin:~$ sudo nft add chain inet filter LAN_DMZ { type filter hook forward priority 0\; counter \; policy accept \;}
javiercruces@odin:~$ sudo nft add chain inet filter DMZ_LAN { type filter hook forward priority 0\; counter \; policy accept \;}
javiercruces@odin:~$ sudo nft add chain inet filter DMZ_WAN { type filter hook forward priority 0\; counter \; policy accept \;}
```

Así quedarían nuestras cadenas creadas :

```bash
javiercruces@odin:~$ sudo nft list chains
table inet filter {
	chain input {
		type filter hook input priority filter; policy accept;
	}
	chain output {
		type filter hook output priority filter; policy accept;
	}
	chain WAN_LAN {
		type filter hook forward priority filter; policy accept;
	}
	chain WAN_DMZ {
		type filter hook forward priority filter; policy accept;
	}
	chain LAN_WAN {
		type filter hook forward priority filter; policy accept;
	}
	chain DMZ_LAN {
		type filter hook forward priority filter; policy accept;
	}
	chain LAN_DMZ {
		type filter hook forward priority filter; policy accept;
	}
	chain DMZ_WAN {
		type filter hook forward priority filter; policy accept;
	}
}
```

La red LAN corresponde a la red de los contenedores 192.168.0.0/24 .
La red DMZ corresponde a la red de hela 172.16.0.0/16 .


Continuamos creando la tabla de NAT para poder configurar el SNAT y el DNAT  , estas ya que suelen ser un numero reducido de reglas no voy a crear distintas cadenas :

```bash
# Creamos la tabla NAT
javiercruces@odin:~$ sudo nft add table nat

# Cadena para el DNAT
javiercruces@odin:~$ sudo nft add chain nat prerouting { type nat hook prerouting priority 0 \; }

# Cadena para el SNAT
javiercruces@odin:~$ sudo nft add chain nat postrouting { type nat hook postrouting priority 100 \; }
```

### Reglas SNAT

Una vez hecho esto voy a crear las reglas de SNAT para que nuestros clientes puedan salir a Internet en la red LAN y DMZ :

Mi tarjeta de red que esta de cara al exterior es la ens4 .

```bash
# Regla SNAT para LAN
sudo nft add rule ip nat postrouting oifname "ens4" ip saddr 192.168.0.0/24 counter masquerade
# Regla SNAT para DMZ
sudo nft add rule ip nat postrouting oifname "ens4" iffname "ens3" ip saddr 172.16.0.0/16 counter masquerade

sudo nft add rule ip nat postrouting oifname "ens4" ip saddr 192.168.0.0/24 counter snat to 172.22.200.47
sudo nft add rule ip nat postrouting oifname "ens4" ip saddr 172.16.0.0/16 counter snat to 172.22.200.47

```

Vamos a comprobar que en los clientes ya pueden acceder a Internet , actualmente la política por defecto es ACCEPT.


Comprobación de SNAT en Hela :

```bash
[javiercruces@hela ~]$ ping www.javiercd.es -c 1
PING javierasping.github.io (185.199.109.153) 56(84) bytes of data.
64 bytes from cdn-185-199-109-153.github.com (185.199.109.153): icmp_seq=1 ttl=51 time=39.4 ms

--- javierasping.github.io ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 39.439/39.439/39.439/0.000 ms
```

Comprobación de SNAT en Thor :

```bash
javiercruces@thor:~$ ping www.javiercd.es -c 1
PING javierasping.github.io (185.199.108.153) 56(84) bytes of data.
64 bytes from cdn-185-199-108-153.github.com (185.199.108.153): icmp_seq=1 ttl=51 time=38.1 ms

--- javierasping.github.io ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 38.138/38.138/38.138/0.000 ms

```

Comprobación de SNAT en Loki :

```bash
javiercruces@loki:~$ ping www.javiercd.es -c 1
PING javierasping.github.io (185.199.111.153) 56(84) bytes of data.
64 bytes from cdn-185-199-111-153.github.com (185.199.111.153): icmp_seq=1 ttl=51 time=37.7 ms

--- javierasping.github.io ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 37.667/37.667/37.667/0.000 ms
```

Por ultimo nos aseguraremos de que la regla recibe hits :

```bash
javiercruces@odin:~$ sudo nft list ruleset
# Salida del comando recortada
	chain postrouting {
		type nat hook postrouting priority srcnat; policy accept;
		oifname "ens4" ip saddr 172.16.0.0/16 counter packets 11 bytes 868 masquerade
		oifname "ens4" ip saddr 192.168.0.0/24 counter packets 122 bytes 10594 masquerade
	}
}
```

### Reglas de DNAT

Las reglas anteriores que teníamos eran las siguientes :

```bash
javiercruces@odin:~$ sudo iptables -L -t nat
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination         
DNAT       tcp  --  anywhere             anywhere             tcp dpt:http to:172.16.0.200
DNAT       udp  --  anywhere             anywhere             udp dpt:domain to:192.168.0.2
DNAT       tcp  --  anywhere             anywhere             tcp dpt:smtp to:192.168.0.3
DNAT       tcp  --  anywhere             anywhere             tcp dpt:mysql to:192.168.0.3
```

Así que vamos a pasarlas a nftables :

```bash
# Para un wordpress que hay en hela
sudo nft add rule ip nat prerouting tcp dport 80 counter dnat to 172.16.0.200

# Para hacer consultas DNS a thor
sudo nft add rule ip nat prerouting udp dport 53 counter dnat to 192.168.0.2

# Para poder recibir correos en loki
sudo nft add rule ip nat prerouting tcp dport 25 counter dnat to 192.168.0.3

# Para acceder desde fuera a un mysql que hay en loki
sudo nft add rule ip nat prerouting tcp dport 3306 counter dnat to 192.168.0.3
```

Ahora vamos a añadir una series de reglas para permitir el trafico anterior y el resto de la preparacion del escenario :

```bash
# PERMITIR USO DE ODIN

## Permitir consultas DNS de odin a thor (DNSSERVER)
sudo nft add rule inet filter output oifname "br-intra2" udp dport 53 counter accept
sudo nft add rule inet filter input iifname "br-intra2" udp sport 53 counter accept

## Permitir tráfico HTTP y HTTPS en odin
sudo nft add rule inet filter output oifname "ens4" ip protocol tcp tcp dport { 80,443 } ct state new,established counter accept
sudo nft add rule inet filter input iifname "ens4" ip protocol tcp tcp sport { 80,443 } ct state established counter accept

# Permitir conexiones SSH por el puerto 2222
sudo nft add rule ip nat prerouting iifname "ens4" tcp dport 2222 counter dnat to 192.168.0.1:22
sudo nft add rule inet filter output oifname "ens4" tcp sport 22 ct state established counter accept
sudo nft add rule inet filter input iifname "ens4" tcp dport 22 ct state new,established counter accept

# Permitir conexiones SSH de odin a hela
sudo nft add rule inet filter output oifname "ens3" ip daddr 172.16.0.0/16 tcp dport 22 counter accept
sudo nft add rule inet filter input iifname "ens3" ip saddr 172.16.0.0/16 tcp sport 22 ct state established,related counter accept

# Permitir conexiones ssh de odin a thor y loki
sudo nft add rule inet filter output oifname "br-intra2" ip daddr 192.168.0.0/24 tcp dport 22 counter accept
sudo nft add rule inet filter input iifname "br-intra2" ip saddr 192.168.0.0/24 tcp sport 22 ct state established,related counter accept

# Reglas perimetrales

## Permitir consultas DNS desde br-intra hacia ens4 , necesario para el forward del dns (ESTA REGLA SOLO ME FUNCIONA SI ESTA EN LA MISMA CADENA)
#sudo nft add rule inet filter DMZ_WAN iifname "br-intra2" oifname "ens4" udp dport 53 counter accept
#sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "br-intra2" udp sport 53 counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens4" udp dport 53 counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "br-intra2" udp sport 53 counter accept


## Permitir consultas dns desde LAN a DMZ (hela --> thor) (ESTA REGLA SOLO ME FUNCIONA SI ESTA EN LA MISMA CADENA)
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" udp dport 53 counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" udp sport 53 counter accept

sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" udp dport 53 counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" udp sport 53 counter accept


## Reglas para permitir trafico a wordpress en hela
sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { new, established } counter accept
sudo nft add rule inet filter DMZ_WAN iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter accept

# Regla para hacer consultas DNS a thor (Permitir DNAT)
sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "br-intra2" ip daddr 192.168.0.2 udp dport 53 ct state new,established counter accept
sudo nft add rule inet filter DMZ_WAN iifname "br-intra2" oifname "ens4" ip saddr 192.168.0.2 udp sport 53 ct state established,related counter accept

# Regla para recibir e enviar correos en loki
sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state new,established counter accept
sudo nft add rule inet filter DMZ_WAN iifname "br-intra2" oifname "ens4" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter accept

# Permitir a hela usar el servidor LDAP
sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" tcp dport 389 counter accept
sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" tcp sport 389 counter accept


```



## Ejercicios

El cortafuegos debe cumplir al menos estas reglas: 

### La máquina Odin tiene un servidor ssh escuchando por el puerto 22, pero al acceder desde el exterior habrá que conectar al puerto 2222. 

Para realizar este ejercicio voy a hacer un DNAT a la interfaz de DMZ de odin que es la 192.168.0.1 , asi me conectare a esa interfaz por ssh . Posteriomente hay que permitir este trafico que va desde la ens4 a la ens3 .

```bash
# Permitimos el trafico que ahora "cambiamos" el puerto con la regla DNAT de 2222 a 22 hacia odin
sudo nft add rule inet filter output oifname "ens4" tcp sport 22 ct state established counter accept
sudo nft add rule inet filter input iifname "ens4" tcp dport 22 ct state new,established counter accept
# Regla DNAT
sudo nft add rule ip nat prerouting iifname "ens4" tcp dport 2222 counter dnat to 192.168.0.1:22
```


Pondré la política por defecto DROP una vez llegado a este punto :

```bash
sudo nft chain inet filter input { policy drop \; }
sudo nft chain inet filter output { policy drop \; }
sudo nft chain inet filter WAN_LAN { policy drop \; }
sudo nft chain inet filter WAN_DMZ { policy drop \; }
sudo nft chain inet filter LAN_WAN { policy drop \; }
sudo nft chain inet filter DMZ_LAN { policy drop \; }
sudo nft chain inet filter LAN_DMZ { policy drop \; }
sudo nft chain inet filter DMZ_WAN { policy drop \; }
```

Y vamos a comprobar que la conexión funciona por el puerto 2222 :

```bash
javiercruces@HPOMEN15:~$ ssh 172.22.200.47 -p 2222
Linux odin.javiercd.gonzalonazareno.org 6.1.0-18-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.76-1 (2024-02-01) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Mar  9 13:49:09 2024 from 172.29.0.58
javiercruces@odin:~$ 
```

Comprobamos los hits en las reglas :

```bash
javiercruces@odin:~$ sudo nft list ruleset
# IMPUT
iifname "ens4" tcp dport 22 ct state established,new counter packets 241918 bytes 13788652 accept
#OUTPUT
oifname "ens4" tcp sport 22 ct state established counter packets 355383 bytes 210012030 accept
#DNAT
iifname "ens4" tcp dport 2222 counter packets 5 bytes 300 dnat to 192.168.0.1:22
```

### Desde Thor y Hela se debe permitir la conexión ssh por el puerto 22 a la máquina Odin. 

Para poder comprobar estas reglas voy a permitir las conexiones ssh desde Odin a ambas redes DMZ y LAN

```bash
# Permitir conexiones ssh de odin a hela
sudo nft add rule inet filter output oifname "ens3" ip daddr 172.16.0.0/16 tcp dport 22 counter accept
sudo nft add rule inet filter input iifname "ens3" ip saddr 172.16.0.0/16 tcp sport 22 ct state established,related counter accept

# Permitir conexiones ssh de odin a thor y loki
sudo nft add rule inet filter output oifname "br-intra2" ip daddr 192.168.0.0/24 tcp dport 22 counter accept
sudo nft add rule inet filter input iifname "br-intra2" ip saddr 192.168.0.0/24 tcp sport 22 ct state established,related counter accept

# Permitir conexion ssh desde hela a odin
sudo nft add rule inet filter input iifname "ens3" ip saddr 172.16.0.200 tcp dport 22 ct state new,established counter accept
sudo nft add rule inet filter output oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 ct state established counter accept

# Permitir conexion ssh desde thor a odin
sudo nft add rule inet filter input iifname "br-intra2" ip saddr 192.168.0.2 tcp dport 22 ct state new,established counter accept
sudo nft add rule inet filter output oifname "br-intra2" ip daddr 192.168.0.2 tcp sport 22 ct state established counter accept
```

Vamos a comprobar las 2 reglas anteriores conectándonos a Odin por ssh desde estos dos clientes :

```bash
#Hela --> Odin
javiercruces@odin:~$ ssh 172.16.0.200 -A
Last login: Sat Mar  9 19:02:49 2024 from 172.16.0.1
[javiercruces@hela ~]$ ssh 172.16.0.1
Linux odin.javiercd.gonzalonazareno.org 6.1.0-18-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.76-1 (2024-02-01) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Mar  9 19:49:28 2024 from 192.168.0.2
javiercruces@odin:~$ 

# Thor --> Odin
javiercruces@thor:~$ ssh 192.168.0.1
Linux odin.javiercd.gonzalonazareno.org 6.1.0-18-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.76-1 (2024-02-01) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Mar  9 19:46:12 2024 from 192.168.0.2
javiercruces@odin:~$ 

```

Te dejare los hits de las reglas al final de la practica .

### La máquina Odin debe tener permitido el tráfico para la interfaz loopback. 

```bash
sudo nft add rule inet filter input iifname "lo" counter accept    
sudo nft add rule inet filter output oifname "lo" counter accept
```

Comprobación :

```bash
javiercruces@odin:~$ ping 127.0.0.1 -c 1
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.100 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.100/0.100/0.100/0.000 ms

```

### A la máquina Odin se le puede hacer ping desde la DMZ, pero desde la LAN se le debe rechazar la conexión (REJECT) y desde el exterior se rechazará de manera silenciosa. 

```bash
# DMZ
sudo nft add rule inet filter input iifname "ens4" ip protocol icmp icmp type echo-request counter accept
sudo nft add rule inet filter output oifname "ens4" ip protocol icmp icmp type echo-reply counter accept
# Las siguientes 2 reglas , no funcionaran como esperamos ya que hacen lo mismo que la politica por defecto , ademas no se permite este trafico .
# LAN 
sudo nft add rule inet filter input iifname "br-intra2" ip protocol icmp counter reject
# Exterior
sudo nft add rule inet filter input iifname "ens3" ip protocol icmp counter drop
```

Vamos a comprobar estas reglas :

```bash
# LAN Thor a odin
javiercruces@thor:~$ ping 192.168.0.1
PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.
From 192.168.0.1 icmp_seq=1 Destination Port Unreachable

# DMZ , Hela --> Odin
[javiercruces@hela ~]$ ping 172.16.0.1 -c 1
PING 172.16.0.1 (172.16.0.1) 56(84) bytes of data.
64 bytes from 172.16.0.1: icmp_seq=1 ttl=64 time=0.471 ms

--- 172.16.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.471/0.471/0.471/0.000 ms

# Exterior a odin
javiercruces@HPOMEN15:~$ ping 172.22.200.47
PING 172.22.200.47 (172.22.200.47) 56(84) bytes of data.
^C
--- 172.22.200.47 ping statistics ---
419 packets transmitted, 0 received, 100% packet loss, time 428036ms
```

Al final de la practica te dejare todos los hits de las reglas .

### La máquina Odin puede hacer ping a la LAN, la DMZ y al exterior. 

```bash
# PERMITIR PING A DMZ
sudo nft insert rule inet filter output oifname "ens3" icmp type echo-request counter accept
sudo nft insert rule inet filter input iifname "ens3" icmp type echo-reply counter accept

# PERMITIR PING A EXTERIOR
sudo nft insert rule inet filter output oifname "ens4" icmp type echo-request counter accept
sudo nft insert rule inet filter input iifname "ens4" icmp type echo-reply counter accept

# PERMITIR PING A LAN
sudo nft insert rule inet filter output oifname "br-intra2" icmp type echo-request counter accept
sudo nft insert rule inet filter input iifname "br-intra2" icmp type echo-reply counter accept
```

Comprobación :

```bash
javiercruces@odin:~$ ping 8.8.8.8 -c 1
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=116 time=8.70 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 8.701/8.701/8.701/0.000 ms

javiercruces@odin:~$ ping 192.168.0.2 -c 1
PING 192.168.0.2 (192.168.0.2) 56(84) bytes of data.
64 bytes from 192.168.0.2: icmp_seq=1 ttl=64 time=6.030 ms

--- 192.168.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.030/0.030/0.030/0.000 ms

javiercruces@odin:~$ ping 172.16.0.200 -c 1
PING 172.16.0.200 (172.16.0.200) 56(84) bytes of data.
64 bytes from 172.16.0.200: icmp_seq=1 ttl=63 time=59.1 ms

--- 172.16.0.200 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 59.052/59.052/59.052/0.000 ms
```

### Desde la máquina Hela se puede hacer ping y conexión ssh a las máquinas de la LAN. 

```bash
## Si no estan en la cadena forward no funciona
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 ip protocol icmp icmp type echo-request counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 ip protocol icmp icmp type echo-reply counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp dport 22 counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 counter accept

sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 ip protocol icmp icmp type echo-request counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 ip protocol icmp icmp type echo-reply counter accept

sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp dport 22 counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 counter accept

```

Comprobación :

```bash
[javiercruces@hela ~]$ ping 192.168.0.2
PING 192.168.0.2 (192.168.0.2) 56(84) bytes of data.
64 bytes from 192.168.0.2: icmp_seq=1 ttl=63 time=0.596 ms
^C
--- 192.168.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.596/0.596/0.596/0.000 ms
[javiercruces@hela ~]$ ssh  192.168.0.2
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 6.1.0-18-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
Last login: Sun Mar 10 14:52:57 2024 from 192.168.0.1
javiercruces@thor:~$ 

```

### Desde cualquier máquina de la LAN se puede conectar por ssh a la máquina Hela. 

```bash
## Si no esta en la cadena forward no funciona
#sudo nft add rule inet filter LAN_DMZ iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 22 counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 22 counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 22 counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 22 counter accept
```

Comprobación :

```bash
javiercruces@thor:~$ ssh 172.16.0.200
Last login: Sun Mar 10 14:53:12 2024 from 192.168.0.2
[javiercruces@hela ~]$ 
```

### Configura la máquina Odin para que las máquinas de LAN y DMZ puedan acceder al exterior. 

Estas reglas ya estaban indicadas previamente .

```bash
sudo nft add rule ip nat postrouting oifname "ens4" ip saddr 192.168.0.0/24 counter masquerade
sudo nft add rule ip nat postrouting oifname "ens4" ip saddr 172.16.0.0/16 counter masquerade
```

### Las máquinas de la LAN pueden hacer ping al exterior y navegar. 

```bash
# Las máquinas de la LAN pueden hacer ping al exterior y navegar. 
## Si no estan en la cadena forward no funciona
#sudo nft add rule inet filter LAN_WAN iifname "br-intra2" oifname "ens4" ip protocol icmp icmp type echo-request counter accept
#sudo nft add rule inet filter WAN_LAN iifname "ens4" oifname "br-intra2" ip protocol icmp icmp type echo-reply counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens4" ip protocol icmp icmp type echo-request counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "br-intra2" ip protocol icmp icmp type echo-reply counter accept
```

Comprobación :

```bash
javiercruces@thor:~$ curl -I https://www.javiercd.es
HTTP/2 200 
server: GitHub.com
content-type: text/html; charset=utf-8
last-modified: Sat, 02 Mar 2024 10:17:01 GMT
access-control-allow-origin: *
strict-transport-security: max-age=31556952
etag: "65e2fc9d-675b"
expires: Sun, 10 Mar 2024 15:35:43 GMT
cache-control: max-age=600
x-proxy-cache: MISS
x-github-request-id: E24C:3800B1:1881E48:18E9A93:65EDD0F7
accept-ranges: bytes
date: Sun, 10 Mar 2024 19:14:10 GMT
via: 1.1 varnish
age: 60
x-served-by: cache-mad22083-MAD
x-cache: HIT
x-cache-hits: 1
x-timer: S1710098050.166466,VS0,VE2
vary: Accept-Encoding
x-fastly-request-id: 0c6c80bbef19370976aadfc6988441c5a36beccc
content-length: 26459

javiercruces@thor:~$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=110 time=38.5 ms
^C
--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 38.451/38.451/38.451/0.000 ms
```


### La máquina Hela puede navegar. Instala un servidor web, un servidor ftp y un servidor de correos si no los tienes aún. 

```bash
# La máquina Hela puede navegar. Instala un servidor web, un servidor ftp y un servidor de correos si no los tienes aún. 
# Hela ya tiene permitido hacer consultas dns a thor
sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" tcp dport {80, 443} counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" tcp sport {80, 443} counter accept
```

Compruebo que puedo navegar :

```bash
[root@hela javiercruces]# curl -I https://www.javiercd.es/
HTTP/2 200 
server: GitHub.com
content-type: text/html; charset=utf-8
last-modified: Sat, 02 Mar 2024 10:17:01 GMT
access-control-allow-origin: *
strict-transport-security: max-age=31556952
etag: "65e2fc9d-675b"
expires: Sun, 10 Mar 2024 15:35:43 GMT
cache-control: max-age=600
x-proxy-cache: MISS
x-github-request-id: E24C:3800B1:1881E48:18E9A93:65EDD0F7
accept-ranges: bytes
date: Sun, 10 Mar 2024 19:13:17 GMT
via: 1.1 varnish
age: 7
x-served-by: cache-mad22067-MAD
x-cache: HIT
x-cache-hits: 1
x-timer: S1710097997.474757,VS0,VE2
vary: Accept-Encoding
x-fastly-request-id: 2d2811893898abf05bebd96c6bd5a09ed7abfe5b
content-length: 26459
```

Entiendo que quieres que instale estos 3 servicios en hela . En nuestro escenario son las otras maquinas quien alberga estos servicios . 

### Configura la máquina Odin para que los servicios web y ftp sean accesibles desde el exterior. 

El servidor web ya esta configurado previamente en la migración del escenario .

```bash
sudo nft add rule ip nat prerouting tcp dport 21 counter dnat to 172.16.0.200
# No funcionan en cadenas separadas 
#sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
#sudo nft add rule inet filter DMZ_WAN iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept

sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept
```

### El servidor web y el servidor ftp deben ser accesibles desde la LAN y desde el exterior. 

El servidor FTP esta en la LAN así que ya es accesible , voy a hacer que sea accesible desde la DMZ . Desde el exterior ambos , ya son accesibles.

```bash
## No funcionan las reglass en cadenas separadas
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { new, established } counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter accept

```

Acceso desde la DMZ a LAN :

```bash
javiercruces@thor:~$ curl 172.16.0.200
<!DOCTYPE html>

javiercruces@thor:~$ ftp 172.16.0.200
Connected to 172.16.0.200.
220 (vsFTPd 3.0.5)
```

### El servidor de correos sólo debe ser accesible desde la LAN. 

Comentamos las lineas de la preparación del escenario que permito el acceso a este y añadimos :

```bash
# No funciona en cadenas separadas
#sudo nft add rule inet filter DMZ_LAN iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state { new, established } counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter accept

sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter accept

```

Accedemos a el :

```bash
[root@hela javiercruces]# telnet 192.168.0.3 25
Trying 192.168.0.3...
Connected to 192.168.0.3.
Escape character is '^]'.
220 loki.javiercd.gonzalonazareno.org ESMTP Postfix (Ubuntu)
```

### En la máquina Loki instala un servidor Postgres si no lo tiene aún. A este servidor se puede acceder desde la DMZ, pero no desde el exterior.


```bash
# no funciona en cadenas distintas
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 5432 ct state { new, established } counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 5432 ct state established,related counter accept


sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 5432 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 5432 ct state established,related counter accept
```

Accedemos al servidor postgree desde hela :

```bash
[root@hela javiercruces]# psql -h 192.168.0.3 -U postgres
Password for user postgres: 
psql (13.14, server 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1))
WARNING: psql major version 13, server major version 14.
         Some psql features might not work.
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
Type "help" for help.

postgres=# 
```

### Evita ataques DoS por ICMP Flood, limitando a 4 el número de peticiones por segundo desde una misma IP.


```bash
sudo nft insert rule inet filter input icmp type echo-request limit rate 1/second burst 4 packets counter drop
```

Si le hacemos un ataque de flood , este cortara el trafico :

```bash
[root@hela javiercruces]# hping3 --icmp --flood --rand-source 172.16.0.1 
HPING 172.16.0.1 (eth0 172.16.0.1): icmp mode set, 28 headers + 0 data bytes
hping in flood mode, no replies will be shown

icmp type echo-request limit rate 1/second burst 4 packets counter packets 46 bytes 2128 drop

```

### Evita ataques DoS por SYN Flood.

```bash
# Evita ataques DoS por SYN Flood.
sudo nft add rule inet filter input tcp flags \& '(fin|syn|rst|ack) == syn' counter limit rate over 25/second drop
```

Si probamos el ataque :

```bash
[root@hela javiercruces]# hping3  --flood --rand-source 172.16.0.1 
HPING 172.16.0.1 (eth0 172.16.0.1): NO FLAGS are set, 40 headers + 0 data bytes
hping in flood mode, no replies will be shown
^C
--- 172.16.0.1 hping statistic ---
1267916 packets transmitted, 0 packets received, 100% packet loss
round-trip min/avg/max = 0.0/0.0/0.0 ms

icmp type echo-request limit rate 1/second burst 4 packets counter packets 31 bytes 2492 drop
```


## Script con todas las reglas

Te dejo aquí el script que he utilizado durante la practica .

```bash
# Crear estructura de tablas
sudo nft delete table inet filter
sudo nft delete table ip nat

## Añadir tabla filter y sus cadenas
sudo nft add table inet filter
sudo nft add chain inet filter forward { type filter hook forward priority 10\; counter \; policy drop\; }
sudo nft add chain inet filter input { type filter hook input priority 0 \; counter \; policy drop \; }
sudo nft add chain inet filter output { type filter hook output priority 0 \; counter \; policy drop \; }

sudo nft add chain inet filter WAN_LAN { type filter hook forward priority 1\; counter \; policy accept \;}
sudo nft add chain inet filter WAN_DMZ { type filter hook forward priority 2\; counter \; policy accept \;}
sudo nft add chain inet filter LAN_WAN { type filter hook forward priority 3\; counter \; policy accept \;}
sudo nft add chain inet filter LAN_DMZ { type filter hook forward priority 4\; counter \; policy accept \;}
sudo nft add chain inet filter DMZ_LAN { type filter hook forward priority 5\; counter \; policy accept \;}
sudo nft add chain inet filter DMZ_WAN { type filter hook forward priority 6\; counter \; policy accept \;}


##  Añadir Tabla NAT y sus cadenas :
sudo nft add table ip nat
sudo nft add chain ip nat prerouting { type nat hook prerouting priority 0 \; }
sudo nft add chain ip nat postrouting { type nat hook postrouting priority 100 \; }


# Reglas para mantener el escenario de clase anterior con IPTABLES

## Reglas SNAT
### Regla SNAT para LAN
sudo nft add rule ip nat postrouting oifname "ens4" ip saddr 192.168.0.0/24 counter masquerade
### Regla SNAT para DMZ
sudo nft add rule ip nat postrouting oifname "ens4" ip saddr 172.16.0.0/16 counter masquerade

## Reglas DNAT
# Para un wordpress que hay en hela
sudo nft add rule ip nat prerouting tcp dport 80 counter dnat to 172.16.0.200

# Para hacer consultas DNS a thor
#sudo nft add rule ip nat prerouting udp dport 53 counter dnat to 192.168.0.2
sudo nft add rule ip nat prerouting iifname "ens3" ip saddr { 172.22.0.0/16, 172.19.0.0/16 } udp dport 53 counter dnat to 192.168.0.2

# Para poder recibir correos en loki
sudo nft add rule ip nat prerouting tcp dport 25 counter dnat to 192.168.0.3
# Para acceder desde fuera a un mysql que hay en loki
sudo nft add rule ip nat prerouting tcp dport 3306 counter dnat to 192.168.0.3


# PERMITIR USO DE ODIN

## Permitir consultas DNS de odin a thor (DNSSERVER)
sudo nft add rule inet filter output oifname "br-intra2" udp dport 53 counter accept
sudo nft add rule inet filter input iifname "br-intra2" udp sport 53 counter accept

## Permitir tráfico HTTP y HTTPS en odin
sudo nft add rule inet filter output oifname "ens4" ip protocol tcp tcp dport { 80,443 } ct state new,established counter accept
sudo nft add rule inet filter input iifname "ens4" ip protocol tcp tcp sport { 80,443 } ct state established counter accept

# Permitir conexiones SSH por el puerto 2222
sudo nft add rule ip nat prerouting iifname "ens4" tcp dport 2222 counter dnat to 192.168.0.1:22
sudo nft add rule inet filter output oifname "ens4" tcp sport 22 ct state established counter accept
sudo nft add rule inet filter input iifname "ens4" tcp dport 22 ct state new,established counter accept

# Permitir conexiones SSH de odin a hela
sudo nft add rule inet filter output oifname "ens3" ip daddr 172.16.0.0/16 tcp dport 22 counter accept
sudo nft add rule inet filter input iifname "ens3" ip saddr 172.16.0.0/16 tcp sport 22 ct state established,related counter accept

# Permitir conexiones ssh de odin a thor y loki
sudo nft add rule inet filter output oifname "br-intra2" ip daddr 192.168.0.0/24 tcp dport 22 counter accept
sudo nft add rule inet filter input iifname "br-intra2" ip saddr 192.168.0.0/24 tcp sport 22 ct state established,related counter accept

# Reglas perimetrales

## Permitir consultas DNS desde br-intra hacia ens4 , necesario para el forward del dns (ESTA REGLA SOLO ME FUNCIONA SI ESTA EN LA MISMA CADENA)
sudo nft add rule inet filter DMZ_WAN iifname "br-intra2" oifname "ens4" udp dport 53 counter accept
sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "br-intra2" udp sport 53 counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens4" udp dport 53 counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "br-intra2" udp sport 53 counter accept


## Permitir consultas dns desde LAN a DMZ (hela --> thor) (ESTA REGLA SOLO ME FUNCIONA SI ESTA EN LA MISMA CADENA)
sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" udp dport 53 counter accept
sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" udp sport 53 counter accept

sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" udp dport 53 counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" udp sport 53 counter accept


## Reglas para permitir trafico a wordpress en hela
sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { new, established } counter accept
sudo nft add rule inet filter DMZ_WAN iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter accept

# Regla para hacer consultas DNS a thor (Permitir DNAT)
sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "br-intra2" ip daddr 192.168.0.2 udp dport 53 ct state new,established counter accept
sudo nft add rule inet filter DMZ_WAN iifname "br-intra2" oifname "ens4" ip saddr 192.168.0.2 udp sport 53 ct state established,related counter accept

# Regla para recibir e enviar correos en loki
# No funcionan en cadenas separadas
#sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state new,established counter accept
#sudo nft add rule inet filter DMZ_WAN iifname "br-intra2" oifname "ens4" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state new,established counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens4" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter accept


# Permitir a hela usar el servidor LDAP
sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" tcp dport 389 counter accept
sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" tcp sport 389 counter accept

# Ejercicios practica
## Permitir conexiones SSH por el puerto 2222
#sudo nft add rule ip nat prerouting iifname "ens4" tcp dport 2222 counter dnat to 192.168.0.1:22
#sudo nft add rule inet filter output oifname "ens4" tcp sport 22 ct state established counter accept
#sudo nft add rule inet filter input iifname "ens4" tcp dport 22 ct state new,established counter accept

# Desde Thor y Hela se debe permitir la conexión ssh por el puerto 22 a la máquina Odin.
## Permitir conexion ssh desde hela a odin
sudo nft add rule inet filter input iifname "ens3" ip saddr 172.16.0.200 tcp dport 22 ct state new,established counter accept
sudo nft add rule inet filter output oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 ct state established counter accept
## Permitir conexion ssh desde thor a odin
sudo nft add rule inet filter input iifname "br-intra2" ip saddr 192.168.0.2 tcp dport 22 ct state new,established counter accept
sudo nft add rule inet filter output oifname "br-intra2" ip daddr 192.168.0.2 tcp sport 22 ct state established counter accept

#La máquina Odin debe tener permitido el tráfico para la interfaz loopback.
sudo nft add rule inet filter input iifname "lo" counter accept
sudo nft add rule inet filter output oifname "lo" counter accept

# A la máquina Odin se le puede hacer ping desde la DMZ, pero desde la LAN se le debe rechazar la conexión (REJECT) y desde el exterior se rechazará de manera silenciosa. 
sudo nft add rule inet filter input iifname "ens3" ip protocol icmp icmp type echo-request counter accept
sudo nft add rule inet filter output oifname "ens3" ip protocol icmp icmp type echo-reply counter accept
## Denegar la conexion desde LAN REJECT
sudo nft add rule inet filter input iifname "br-intra2" ip protocol icmp counter reject
## Denegar de manera silenciosa desde EXTERIOR
sudo nft add rule inet filter input iifname "ens3" ip protocol icmp counter drop

# La máquina Odin puede hacer ping a la LAN, la DMZ y al exterior.
## LAN
sudo nft add rule inet filter output oifname "ens3" icmp type echo-request counter accept
sudo nft add rule inet filter input iifname "ens3" icmp type echo-reply counter accept
## EXTERIOR
sudo nft add rule inet filter output oifname "ens4" icmp type echo-request counter accept
sudo nft add rule inet filter input iifname "ens4" icmp type echo-reply counter accept
## DMZ
sudo nft add rule inet filter output oifname "br-intra2" icmp type echo-request counter accept
sudo nft add rule inet filter input iifname "br-intra2" icmp type echo-reply counter accept


#### Desde la máquina Hela se puede hacer ping y conexión ssh a las máquinas de la LAN.
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 ip protocol icmp icmp type echo-request counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 ip protocol icmp icmp type echo-reply counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp dport 22 counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 counter accept

## Si no estan en la cadena forward no funciona
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 ip protocol icmp icmp type echo-request counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 ip protocol icmp icmp type echo-reply counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp dport 22 counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 counter accept

# Desde cualquier máquina de la LAN se puede conectar por ssh a la máquina Hela. 

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 22 counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 22 counter accept

## Si no esta en la cadena forward no funciona
#sudo nft add rule inet filter LAN_DMZ iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 22 counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 22 counter accept


# Configura la máquina Odin para que las máquinas de LAN y DMZ puedan acceder al exterior.
## SNAT hecho anteriormente

# Las máquinas de la LAN pueden hacer ping al exterior y navegar. 
## Si no estan en la cadena forward no funciona
#sudo nft add rule inet filter LAN_WAN iifname "br-intra2" oifname "ens4" ip protocol icmp icmp type echo-request counter accept
#sudo nft add rule inet filter WAN_LAN iifname "ens4" oifname "br-intra2" ip protocol icmp icmp type echo-reply counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens4" ip protocol icmp icmp type echo-request counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "br-intra2" ip protocol icmp icmp type echo-reply counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens4" tcp dport {80, 443} counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "br-intra2" tcp sport {80, 443} counter accept


# La máquina Hela puede navegar. Instala un servidor web, un servidor ftp y un servidor de correos si no los tienes aún. 
# Hela ya tiene permitido hacer consultas dns a thor
sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" tcp dport {80, 443} counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" tcp sport {80, 443} counter accept



# ### Configura la máquina Odin para que los servicios web y ftp sean accesibles desde el exterior. 
sudo nft add rule ip nat prerouting tcp dport 21 counter dnat to 172.16.0.200

# No funcionan en cadenas separadas 
#sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
#sudo nft add rule inet filter DMZ_WAN iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept

sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept


# ### El servidor web y el servidor ftp deben ser accesibles desde la LAN y desde el exterior. 
## No funcionan las reglass en cadenas separadas
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { new, established } counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter accept


# ### El servidor de correos sólo debe ser accesible desde la LAN. 
# no funciona en cadenas separadas
#sudo nft add rule inet filter DMZ_LAN iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state { new, established } counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter accept



# ### En la máquina Loki instala un servidor Postgres si no lo tiene aún. A este servidor se puede acceder desde la DMZ, pero no desde el exterior.
# no funciona en cadenas distintas
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 5432 ct state { new, established } counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 5432 ct state established,related counter accept


sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 5432 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 5432 ct state established,related counter accept


# ### Evita ataques DoS por ICMP Flood, limitando a 4 el número de peticiones por segundo desde una misma IP.
sudo nft insert rule inet filter input icmp type echo-request limit rate 1/second burst 4 packets counter drop

# ### Evita ataques DoS por SYN Flood.
#sudo nft insert rule inet filter input tcp flags \& '(fin|syn|rst|ack) == syn' counter limit rate over 25/second drop

#### Evita que realicen escaneos de puertos a Odin.
#sudo nft insert rule inet filter input tcp flags & (fin|syn|rst|ack) == (syn) counter drop

#sudo nft add rule inet filter output udp dport 53 counter accept
#sudo nft add rule inet filter input udp sport 53 counter accept

```

## Hits de las reglas

Cada vez que he ejecutado el script las reglas pierden los contadores pero así seria el esquema con todas las reglas al finalizar la practica :

```bash
javiercruces@odin:~$ sudo nft list ruleset  
table inet filter {
	chain forward {
		type filter hook forward priority filter + 10; policy drop;
		counter packets 711 bytes 171730
		iifname "br-intra2" oifname "ens4" udp dport 53 counter packets 107 bytes 8505 accept
		iifname "ens4" oifname "br-intra2" udp sport 53 counter packets 107 bytes 93423 accept
		iifname "ens3" oifname "br-intra2" udp dport 53 counter packets 11 bytes 758 accept
		iifname "br-intra2" oifname "ens3" udp sport 53 counter packets 11 bytes 1818 accept
		iifname "ens4" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state established,new counter packets 0 bytes 0 accept
		iifname "br-intra2" oifname "ens4" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter packets 0 bytes 0 accept
		iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 ip protocol icmp icmp type echo-request counter packets 2 bytes 168 accept
		iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 ip protocol icmp icmp type echo-reply counter packets 2 bytes 168 accept
		iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp dport 22 counter packets 160 bytes 16502 accept
		iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 counter packets 100 bytes 15086 accept
		iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 22 counter packets 30 bytes 6041 accept
		iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 22 counter packets 23 bytes 5213 accept
		iifname "br-intra2" oifname "ens4" ip protocol icmp icmp type echo-request counter packets 1 bytes 84 accept
		iifname "ens4" oifname "br-intra2" ip protocol icmp icmp type echo-reply counter packets 1 bytes 84 accept
		iifname "br-intra2" oifname "ens4" tcp dport { 80, 443 } counter packets 16 bytes 1666 accept
		iifname "ens4" oifname "br-intra2" tcp sport { 80, 443 } counter packets 17 bytes 4947 accept
		iifname "ens3" oifname "ens4" tcp dport { 80, 443 } counter packets 32 bytes 3332 accept
		iifname "ens4" oifname "ens3" tcp sport { 80, 443 } counter packets 34 bytes 9903 accept
		iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { established, new } counter packets 0 bytes 0 accept
		iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter packets 0 bytes 0 accept
		iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { established, new } counter packets 0 bytes 0 accept
		iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter packets 0 bytes 0 accept
		iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { established, new } counter packets 18 bytes 1064 accept
		iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter packets 14 bytes 1348 accept
		iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state { established, new } counter packets 0 bytes 0 accept
		iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter packets 0 bytes 0 accept
		iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 5432 ct state { established, new } counter packets 0 bytes 0 accept
		iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 5432 ct state established,related counter packets 0 bytes 0 accept
	}

	chain input {
		type filter hook input priority filter; policy drop;
		icmp type echo-request limit rate 1/second burst 4 packets counter packets 13 bytes 1092 drop
		counter packets 1490 bytes 141906
		iifname "br-intra2" udp sport 53 counter packets 18 bytes 2352 accept
		iifname "ens4" ip protocol tcp tcp sport { 80, 443 } ct state established counter packets 17 bytes 13286 accept
		iifname "ens4" tcp dport 22 ct state established,new counter packets 965 bytes 70084 accept
		iifname "ens3" ip saddr 172.16.0.0/16 tcp sport 22 ct state established,related counter packets 356 bytes 39980 accept
		iifname "br-intra2" ip saddr 192.168.0.0/24 tcp sport 22 ct state established,related counter packets 131 bytes 15952 accept
		iifname "ens3" ip saddr 172.16.0.200 tcp dport 22 ct state established,new counter packets 0 bytes 0 accept
		iifname "br-intra2" ip saddr 192.168.0.2 tcp dport 22 ct state established,new counter packets 0 bytes 0 accept
		iifname "lo" counter packets 0 bytes 0 accept
		iifname "ens3" ip protocol icmp icmp type echo-request counter packets 0 bytes 0 accept
		iifname "br-intra2" ip protocol icmp counter packets 1 bytes 84 reject with icmp port-unreachable
		iifname "ens3" ip protocol icmp counter packets 1 bytes 84 drop
		iifname "ens3" icmp type echo-reply counter packets 0 bytes 0 accept
		iifname "ens4" icmp type echo-reply counter packets 1 bytes 84 accept
		iifname "br-intra2" icmp type echo-reply counter packets 0 bytes 0 accept
		iifname "lo" counter packets 0 bytes 0 accept
	}

	chain output {
		type filter hook output priority filter; policy drop;
		counter packets 1404 bytes 207511
		oifname "br-intra2" udp dport 53 counter packets 18 bytes 1304 accept
		oifname "ens4" ip protocol tcp tcp dport { 80, 443 } ct state established,new counter packets 19 bytes 7331 accept
		oifname "ens4" tcp sport 22 ct state established counter packets 577 bytes 142596 accept
		oifname "ens3" ip daddr 172.16.0.0/16 tcp dport 22 counter packets 547 bytes 38208 accept
		oifname "br-intra2" ip daddr 192.168.0.0/24 tcp dport 22 counter packets 194 bytes 14400 accept
		oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 ct state established counter packets 0 bytes 0 accept
		oifname "br-intra2" ip daddr 192.168.0.2 tcp sport 22 ct state established counter packets 0 bytes 0 accept
		oifname "lo" counter packets 12 bytes 1008 accept
		oifname "ens3" ip protocol icmp icmp type echo-reply counter packets 0 bytes 0 accept
		oifname "ens3" icmp type echo-request counter packets 1 bytes 84 accept
		oifname "ens4" icmp type echo-request counter packets 1 bytes 84 accept
		oifname "br-intra2" icmp type echo-request counter packets 1 bytes 84 accept
		oifname "lo" counter packets 0 bytes 0 accept
	}

	chain WAN_LAN {
		type filter hook forward priority filter + 1; policy accept;
		counter packets 711 bytes 171730
	}

	chain WAN_DMZ {
		type filter hook forward priority filter + 2; policy accept;
		counter packets 711 bytes 171730
		iifname "ens4" oifname "br-intra2" udp sport 53 counter packets 107 bytes 93423 accept
		iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { established, new } counter packets 0 bytes 0 accept
		iifname "ens4" oifname "br-intra2" ip daddr 192.168.0.2 udp dport 53 ct state established,new counter packets 0 bytes 0 accept
	}

	chain LAN_WAN {
		type filter hook forward priority filter + 3; policy accept;
		counter packets 711 bytes 171730
	}

	chain LAN_DMZ {
		type filter hook forward priority filter + 4; policy accept;
		counter packets 711 bytes 171730
		iifname "ens3" oifname "br-intra2" udp dport 53 counter packets 11 bytes 758 accept
		iifname "ens3" oifname "br-intra2" tcp dport 389 counter packets 0 bytes 0 accept
	}

	chain DMZ_LAN {
		type filter hook forward priority filter + 5; policy accept;
		counter packets 711 bytes 171730
		iifname "br-intra2" oifname "ens3" udp sport 53 counter packets 11 bytes 1818 accept
		iifname "br-intra2" oifname "ens3" tcp sport 389 counter packets 0 bytes 0 accept
	}

	chain DMZ_WAN {
		type filter hook forward priority filter + 6; policy accept;
		counter packets 711 bytes 171730
		iifname "br-intra2" oifname "ens4" udp dport 53 counter packets 107 bytes 8505 accept
		iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter packets 0 bytes 0 accept
		iifname "br-intra2" oifname "ens4" ip saddr 192.168.0.2 udp sport 53 ct state established,related counter packets 0 bytes 0 accept
	}
}
table ip nat {
	chain prerouting {
		type nat hook prerouting priority filter; policy accept;
		tcp dport 80 counter packets 8 bytes 480 dnat to 172.16.0.200
		iifname "ens3" ip saddr { 172.19.0.0/16, 172.22.0.0/16 } udp dport 53 counter packets 0 bytes 0 dnat to 192.168.0.2
		tcp dport 25 counter packets 0 bytes 0 dnat to 192.168.0.3
		tcp dport 3306 counter packets 12 bytes 720 dnat to 192.168.0.3
		iifname "ens4" tcp dport 2222 counter packets 0 bytes 0 dnat to 192.168.0.1:22
		tcp dport 21 counter packets 0 bytes 0 dnat to 172.16.0.200
	}

	chain postrouting {
		type nat hook postrouting priority srcnat; policy accept;
		oifname "ens4" ip saddr 192.168.0.0/24 counter packets 109 bytes 8649 masquerade
		oifname "ens4" ip saddr 172.16.0.0/16 counter packets 2 bytes 120 masquerade
	}
}

```

## Hacer las reglas persistentes 

Vamos a guardar las reglas con :

```bash
root@odin:/home/javiercruces# nft list ruleset > /etc/nftables.conf
```

Si las queremos restaurar  : 

```bash
javiercruces@odin:~$ sudo nft -f /etc/nftables.conf
```


Para hacer que al reiniciar las reglas se restauren solas :

```bash
# Creamos la unidad de systemd
javiercruces@odin:~$ sudo cat /etc/systemd/system/nftables-persistent.service
[Unit]
Description=Cargar reglas de nftables al iniciar el sistema

[Service]
Type=oneshot
ExecStart=/usr/sbin/nft -f /etc/nftables/nftables.rules

[Install]
WantedBy=multi-user.target

# Activa el servicio para que al reiniciar se apliquen los cambios 
javiercruces@odin:~$ sudo systemctl enable nftables-persistent.service
```

