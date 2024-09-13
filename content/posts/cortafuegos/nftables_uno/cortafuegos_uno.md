---
title: "Implementación de un cortafuegos perimetral con Nftables I"
date: 2024-03-28T10:00:00+00:00
description: Implementación de un cortafuegos perimetral con Nftables
tags: [FIREWALL,LINUX,DEBIAN,NFTABLES]
hero: /images/cortafuegos/nftables1.png
---



En este post sobre un escenario con maquinas Debian , aplicaremos reglas con Nftables para conrtrolar el trafico que entra y sale en nuestra red , intentando imitar un escenario. 



> [!NOTE]  
> Para desplegar el escenario para realizar estos ejercicios necesitaras desplegar el fichero .yaml que encontraras en el enlace del párrafo siguiente . Este se encargara de desplegar 2 maquinas una que hará de cortafuegos y otra que simulara un cliente que estará conectado a la primera maquina para simular una red local .

Realiza con NFTABLES el ejercicio de la página https://fp.josedomingo.org/seguridadgs/u03/perimetral_iptables.html documentando las pruebas de funcionamiento realizadas.

## Preparación del escenario

Lo primero que haremos es activar el bit de forwarding. Para ello, editaremos el archivo `/etc/sysctl.conf` utilizando el siguiente comando :

```bash
javiercruces@router-fw:~$ sudo nano /etc/sysctl.conf 
# Descomentamos la linea
net.ipv4.ip_forward=1
```

A continuación, aplicaremos los cambios utilizando el siguiente comando:

```bash
javiercruces@router-fw:~$ sudo sysctl -p
net.ipv4.ip_forward = 1
```

Ahora añadiremos la tabla filter :

```bash
javiercruces@router-fw:~$ sudo nft add table inet filter
```

Podemos ver las tablas creadas :

```bash
javiercruces@router-fw:~$ sudo nft list tables
table inet filter
```

Crear las cadenas para la entrada y salida :

```bash
# Cadena de "entrada"
javiercruces@router-fw:~$ sudo nft add chain inet filter input { type filter hook input priority 0 \; counter \; policy accept \; }

# Cadena de "salida"
javiercruces@router-fw:~$ sudo nft add chain inet filter output { type filter hook output priority 0 \; counter \; policy accept \; }

# Cadena forward , peticiones que atraviesen :
javiercruces@router-fw:~$ sudo nft add chain inet filter forward { type filter hook forward priority 0 \; counter \; policy drop \; }
```

Ahora comprobaremos que se han creado estas tres cadenas :

```bash
javiercruces@router-fw:~$ sudo nft list chains
table inet filter {
	chain input {
		type filter hook input priority filter; policy accept;
	}
	chain output {
		type filter hook output priority filter; policy accept;
	}
	chain forward {
		type filter hook forward priority filter; policy accept;
	}
}
```
## Reglas del cortafuegos

### Permitir ssh hacia el cortafuegos

Ahora vamos a permitir el ssh hacia la maquina router-fw  :

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter input iif ens3 tcp dport 22 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter output oif ens3 tcp sport 22 ct state established counter accept
```

### Política por defecto DROP

Ahora vamos a poner la política por defecto DROP:

```bash
javiercruces@router-fw:~$ sudo nft chain inet filter input { policy drop \; }
javiercruces@router-fw:~$ sudo nft chain inet filter output { policy drop \; }
javiercruces@router-fw:~$ sudo nft chain inet filter forward { policy drop \; }
```

Comprobaremos que con la nueva política podemos conectarnos por ssh y no hemos perdido la conexión , viendo que tenemos hits en las reglas .

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
table inet filter {
	chain input {
		type filter hook input priority filter; policy drop;
		counter packets 174 bytes 11824
		iif "ens3" tcp dport 22 ct state established,new counter packets 129 bytes 8252 accept
	}

	chain output {
		type filter hook output priority filter; policy drop;
		counter packets 169 bytes 31232
		oif "ens3" tcp sport 22 ct state established counter packets 85 bytes 22632 accept
	}
}
```

### SNAT

Hacemos SNAT para que los equipos de la LAN puedan acceder al exterior.

Para ello sera necesario que creemos la tabla NAT y sus cadenas . Como podemos observar hemos indicado menos prioridad en la cadena postrouting (mientras menor sea el número, mayor es su prioridad) para que las reglas de dicha cadena se ejecuten después de las reglas de prerouting.

```bash
# Creamos la tabla NAT
javiercruces@router-fw:~$ sudo nft add table nat

# Cadena para el DNAT
javiercruces@router-fw:~$ sudo nft add chain nat prerouting { type nat hook prerouting priority 0 \; }

# Cadena para el SNAT
javiercruces@router-fw:~$ sudo nft add chain nat postrouting { type nat hook postrouting priority 100 \; }
```

Ahora vamos a permitir hacer SNAT a la red LAN :

```bash
javiercruces@router-fw:~$ sudo nft add rule ip nat postrouting oifname "ens3" ip saddr 192.168.100.0/24 counter masquerade
```
### Permitimos el ssh desde el cortafuego a la LAN

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter output oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter input iifname "ens4" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter accept
```

Ahora que podemos conectarnos por ssh a nuestra maquina LAN , vamos a comprobar las 2 reglas anteriores . Conectarnos por ssh y el SNAT :

```bash
javiercruces@router-fw:~$ ssh debian@192.168.100.10
Linux lan 6.1.0-12-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.52-1 (2023-09-07) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Feb 27 18:31:10 2024 from 192.168.100.2

debian@lan:~$ ping 1.1.1.1
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
^C
--- 1.1.1.1 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1002ms
```

Veremos que podemos conectarnos por ssh , sin embargo el ping no esta permitido pero lo he realizado para que la regla de SNAT tenga hits.

Vamos a ver que las reglas tienen hits :

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
table inet filter {
	chain input {
		type filter hook input priority filter; policy drop;
		counter packets 621 bytes 63636
		iif "ens3" tcp dport 22 ct state established,new counter packets 493 bytes 41948 accept
		iifname "ens4" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 81 bytes 17628 accept
	}

	chain output {
		type filter hook output priority filter; policy drop;
		counter packets 1231 bytes 141120
		oif "ens3" tcp sport 22 ct state established counter packets 349 bytes 68222 accept
		oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 103 bytes 17420 accept
	}
	chain forward {
		type filter hook forward priority filter; policy drop;
		counter packets 4 bytes 336
	}
}

table ip nat {
	chain prerouting {
		type nat hook prerouting priority filter; policy accept;
	}

	chain postrouting {
		type nat hook postrouting priority srcnat; policy accept;
		oifname "ens3" ip saddr 192.168.100.0/24 counter packets 1 bytes 84 masquerade
	}
}
```

Como podemos ver el SNAT tiene hits , así que la regla esta funcionando , pero como no dejamos que atraviese el firewall estas no saldrán . 
### Permitimos tráfico para la interfaz loopback

Añadimos las reglas , para permitir el trafico hacia la interfaz loopback :

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter input iifname "lo" counter accept    
javiercruces@router-fw:~$ sudo nft add rule inet filter output oifname "lo" counter accept
```

Comprobamos que tenemos conectividad :

```bash
javiercruces@router-fw:~$ ping 127.0.0.1
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.205 ms
```

Vamos a ver los hits de la regla :

```bash
javiercruces@router-fw:~$ sudo nft list ruleset | grep lo
		iifname "lo" counter packets 2 bytes 168 accept
		oifname "lo" counter packets 2 bytes 168 accept
```

### Peticiones y respuestas protocolo ICMP

Vamos a permitir a la maquina router-fw aceptar peticiones ICMP y que envié la respuesta :

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter output oifname "ens3" icmp type echo-reply counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter input iifname "ens3" icmp type echo-request counter accept
```

Le hago ping desde mi maquina :

```bash
javiercruces@HPOMEN15:~/Documentos/2ºASIR/SAD/cortafuegos1$ ping 172.22.201.120 -c 1
PING 172.22.201.120 (172.22.201.120) 56(84) bytes of data.
64 bytes from 172.22.201.120: icmp_seq=1 ttl=61 time=85.4 ms

--- 172.22.201.120 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 85.403/85.403/85.403/0.000 ms
```

### Permitir hacer ping desde la LAN

Vamos a permitir que se pueda hacer ping desde la LAN :

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 icmp type echo-request counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 icmp type echo-reply counter accept
```

Vamos a comprobarlo :

```bash
debian@lan:~$ ping 1.1.1.1
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
64 bytes from 1.1.1.1: icmp_seq=1 ttl=50 time=40.8 ms
64 bytes from 1.1.1.1: icmp_seq=2 ttl=50 time=40.8 ms
^C
--- 1.1.1.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 40.821/40.834/40.848/0.013 ms
```

Vamos a ver los hits de la regla , ademas con esta podemos comprobar la regla del SNAT :

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
table inet filter {
	chain input {
		type filter hook input priority filter; policy drop;
		counter packets 2637 bytes 213636
		iif "ens3" tcp dport 22 ct state established,new counter packets 2346 bytes 172928 accept
		iifname "ens4" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 225 bytes 32812 accept
		iifname "lo" counter packets 2 bytes 168 accept
		iifname "ens3" icmp type echo-request counter packets 1 bytes 84 accept
	}

	chain output {
		type filter hook output priority filter; policy drop;
		counter packets 4656 bytes 697080
		oif "ens3" tcp sport 22 ct state established counter packets 1618 bytes 477018 accept
		oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 291 bytes 30252 accept
		oifname "lo" counter packets 2 bytes 168 accept
		oifname "ens3" icmp type echo-reply counter packets 1 bytes 84 accept
	}

	chain forward {
		type filter hook forward priority filter; policy drop;
		counter packets 31 bytes 2604
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 icmp type echo-request counter packets 12 bytes 1008 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 icmp type echo-reply counter packets 2 bytes 168 accept
	}
}
table ip nat {
	chain prerouting {
		type nat hook prerouting priority filter; policy accept;
	}

	chain postrouting {
		type nat hook postrouting priority srcnat; policy accept;
		oifname "ens3" ip saddr 192.168.100.0/24 counter packets 4 bytes 336 masquerade
	}
}
```
### Consultas y respuestas DNS desde la LAN

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 udp dport 53 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 udp sport 53 ct state established counter accept
```

Vamos a hacer una consulta utilizando el comando host , ya que no dispongo otra herramienta instalada para hacer consultas dns  :

```bash
debian@lan:~$ host www.javiercd.es
www.javiercd.es is an alias for javierasping.github.io.
javierasping.github.io has address 185.199.111.153
javierasping.github.io has address 185.199.108.153
javierasping.github.io has address 185.199.109.153
javierasping.github.io has address 185.199.110.153
javierasping.github.io has IPv6 address 2606:50c0:8000::153
javierasping.github.io has IPv6 address 2606:50c0:8001::153
javierasping.github.io has IPv6 address 2606:50c0:8003::153
javierasping.github.io has IPv6 address 2606:50c0:8002::153
```

Vamos a consultar los hits de las reglas :

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 udp dport 53 ct state established,new counter packets 10 bytes 643 accept
iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 udp sport 53 ct state established counter packets 10 bytes 2644 accept
```
### Permitimos la navegación web desde la LAN

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip protocol tcp ip saddr 192.168.100.0/24 tcp dport { 80,443} ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip protocol tcp ip daddr 192.168.100.0/24 tcp sport { 80,443} ct state established counter accept
```

Para verificar este punto, necesitaremos modificar el archivo /etc/nsswitch.conf, el cual determina la prioridad de la resolución DNS. Realizaremos esta modificación para priorizar la consulta DNS al servicio de DNS de systemd, el cual está incluido en Debian y Ubuntu. Esto permitirá que las consultas se realicen primero en la propia máquina y, en caso necesario, serán enviadas al servidor DNS configurado ya que en este escenario las aplicaciones no nos resuelven si no realizamos esta modificación .

```bash
debian@lan:~$ sudo nano /etc/nsswitch.conf 
hosts:          files dns resolve [!UNAVAIL=return]
```

Ademas cambiaremos el servidor dns de la maquina y en lugar de ser nosotros , pondremos el del instituto :

```bash
debian@lan:~$ sudo cat /etc/resolv.conf 
nameserver 172.22.0.1
```

Una vez aplicados los cambios vamos a pedir una web por el nombre de dominio , así comprobaremos el funcionamiento de los dos puntos anteriores . Pediré solo las cabeceras para que la salida sea mas legible , un código 200 seria correcto . En la parte de http nos da una redirección ya que el servidor te redirige a https  :

```bash
debian@lan:~$ curl -I https://www.javiercd.es/
HTTP/2 200 
server: GitHub.com
content-type: text/html; charset=utf-8
last-modified: Sun, 25 Feb 2024 23:03:49 GMT
access-control-allow-origin: *
strict-transport-security: max-age=31556952
etag: "65dbc755-675b"
expires: Wed, 28 Feb 2024 10:10:17 GMT
cache-control: max-age=600
x-proxy-cache: MISS
x-github-request-id: 5CD4:0E10:CBDBE5:CFBAEA:65DF0430
accept-ranges: bytes
date: Wed, 28 Feb 2024 10:00:17 GMT
via: 1.1 varnish
age: 0
x-served-by: cache-mad2200123-MAD
x-cache: MISS
x-cache-hits: 0
x-timer: S1709114417.014922,VS0,VE167
vary: Accept-Encoding
x-fastly-request-id: e15d291bbff90bf9de58991f0f6477e4398c415d
content-length: 26459

debian@lan:~$ curl -I http://www.javiercd.es/
HTTP/1.1 301 Moved Permanently
Content-Length: 162
Server: GitHub.com
Content-Type: text/html
Location: https://www.javiercd.es/
X-GitHub-Request-Id: 9870:0E7F:37400AD:3848DF5:65DF0425
Accept-Ranges: bytes
Date: Wed, 28 Feb 2024 10:00:27 GMT
Age: 21
X-Served-By: cache-mad2200100-MAD
X-Cache: HIT
X-Cache-Hits: 1
X-Timer: S1709114427.468002,VS0,VE1
Vary: Accept-Encoding
X-Fastly-Request-ID: e321e34041a049f6f7c99e0693be994990da6da3
X-Cache: MISS from f0
X-Cache-Lookup: HIT from f0:3128
Via: 1.1 varnish, 1.1 f0 (squid/4.6)
Connection: close
```


### Permitimos el acceso a nuestro servidor web de la LAN desde el exterior 

Como ya tenemos resolución dns y navegación web , podremos actualizar nuestros repositorios y instalar paquetes : 

```bash
debian@lan:~$ sudo apt update -y && sudo apt install apache2 -y 
```

Una vez instalado apache vamos a realizar la regla de DNAT :

```bash
javiercruces@router-fw:~$ sudo nft add rule ip nat prerouting iifname "ens3" tcp dport 80 counter dnat to 192.168.100.10
```

Ahora tenemos que permitir en la cadena forward el trafico para permitir el DNAT . Las peticiones al servidor web y las respuestas 

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 80 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 80 ct state established counter accept
```

Ahora vamos a comprobar que podemos acceder al servidor web :

```bash
javiercruces@HPOMEN15:~/Documentos/2ºASIR/SAD/cortafuegos1$ curl -I 172.22.201.120
HTTP/1.1 200 OK
Date: Wed, 28 Feb 2024 10:24:26 GMT
Server: Apache/2.4.57 (Debian)
Last-Modified: Wed, 28 Feb 2024 10:17:20 GMT
ETag: "29cd-6126e72b03120"
Accept-Ranges: bytes
Content-Length: 10701
Vary: Accept-Encoding
Content-Type: text/html
```

Desde un navegador :

![](../img/Pastedimage20240228112558.png)

Por ultimo vamos a comprobar que las reglas involucradas tienen hits y te dejo el listado completo para que veas las reglas hasta este punto  :

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
table inet filter {
	chain input {
		type filter hook input priority filter; policy drop;
		counter packets 20313 bytes 2212299
		iif "ens3" tcp dport 22 ct state established,new counter packets 11896 bytes 827728 accept
		iifname "ens4" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 8093 bytes 1321072 accept
		iifname "lo" counter packets 92 bytes 17660 accept
		iifname "ens3" icmp type echo-request counter packets 1 bytes 84 accept
	}

	chain output {
		type filter hook output priority filter; policy drop;
		counter packets 69191 bytes 6011531
		oif "ens3" tcp sport 22 ct state established counter packets 8461 bytes 1953220 accept
		oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 9482 bytes 623484 accept
		oifname "lo" counter packets 92 bytes 17660 accept
		oifname "ens3" icmp type echo-reply counter packets 1 bytes 84 accept
	}

	chain forward {
		type filter hook forward priority filter; policy drop;
		counter packets 42155 bytes 145465374
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 icmp type echo-request counter packets 32 bytes 2688 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 icmp type echo-reply counter packets 18 bytes 1512 accept
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 udp dport 53 ct state established,new counter packets 273 bytes 17860 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 udp sport 53 ct state established counter packets 273 bytes 52163 accept
		iifname "ens4" oifname "ens3" ip protocol tcp ip saddr 192.168.100.0/24 tcp dport { 80, 443 } ct state established,new counter packets 33973 bytes 1794576 accept
		iifname "ens3" oifname "ens4" ip protocol tcp ip daddr 192.168.100.0/24 tcp sport { 80, 443 } ct state established counter packets 7119 bytes 143533481 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 80 ct state established,new counter packets 47 bytes 3905 accept
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 80 ct state established counter packets 32 bytes 24161 accept
	}
}
table ip nat {
	chain prerouting {
		type nat hook prerouting priority filter; policy accept;
		iifname "ens3" tcp dport 80 counter packets 4 bytes 240 dnat to 192.168.100.10
	}

	chain postrouting {
		type nat hook postrouting priority srcnat; policy accept;
		oifname "ens3" ip saddr 192.168.100.0/24 counter packets 547 bytes 38852 masquerade
	}
}

```
## Ejercicios adicionales

Debes añadir después las reglas necesarias para que se permitan las siguientes operaciones:

### Permite poder hacer conexiones ssh al exterior desde la máquina cortafuegos.

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter output oifname "ens3" tcp dport 22 ct state new,established  counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter input iifname "ens3" tcp sport 22 ct state established  counter accept
```

Vamos a conectarnos por ssh desde la maquina cortafuegos a otra para comprobar esto :

```bash
javiercruces@router-fw:~$ ssh 172.22.200.47
Linux odin.javiercd.gonzalonazareno.org 6.1.0-18-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.76-1 (2024-02-01) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Feb 28 10:35:56 2024 from 172.22.201.120
javiercruces@odin:~$ 
```

Vamos a comprobar los hits en las reglas :

```bash
javiercruces@router-fw:~$ sudo nft list ruleset 
iifname "ens3" tcp sport 22 ct state established counter packets 66 bytes 18624 accept
oifname "ens3" tcp dport 22 ct state established,new counter packets 89 bytes 16572 accept

```

### Permite hacer consultas DNS desde la máquina cortafuegos sólo al servidor 8.8.8.8. Comprueba que no puedes hacer un dig @1.1.1.1.

Vamos a añadir esta regla :

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter output oifname "ens3" ip daddr 8.8.8.8 udp dport 53 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter input iifname "ens3" ip saddr 8.8.8.8 udp sport 53 ct state established counter accept
```

Ahora vamos a comprobar que a traves de la 1.1.1.1 no podemos resolver nombres pero con la 8.8.8.8 si : 

```bash
javiercruces@router-fw:~$ dig @1.1.1.1 www.javiercd.es
;; communications error to 1.1.1.1#53: timed out
;; communications error to 1.1.1.1#53: timed out
;; communications error to 1.1.1.1#53: timed out

; <<>> DiG 9.18.24-1-Debian <<>> @1.1.1.1 www.javiercd.es
; (1 server found)
;; global options: +cmd
;; no servers could be reached

javiercruces@router-fw:~$ dig @8.8.8.8 www.javiercd.es

; <<>> DiG 9.18.24-1-Debian <<>> @8.8.8.8 www.javiercd.es
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 4046
;; flags: qr rd ra; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;www.javiercd.es.		IN	A

;; ANSWER SECTION:
www.javiercd.es.	3600	IN	CNAME	javierasping.github.io.
javierasping.github.io.	3600	IN	A	185.199.108.153
javierasping.github.io.	3600	IN	A	185.199.109.153
javierasping.github.io.	3600	IN	A	185.199.110.153
javierasping.github.io.	3600	IN	A	185.199.111.153

;; Query time: 68 msec
;; SERVER: 8.8.8.8#53(8.8.8.8) (UDP)
;; WHEN: Wed Feb 28 11:09:05 UTC 2024
;; MSG SIZE  rcvd: 144

```

Vamos a ver los hits de las reglas :

```bash
javiercruces@router-fw:~$ sudo nft list ruleset 
iifname "ens3" ip saddr 8.8.8.8 udp sport 53 ct state established counter packets 314 bytes 36448 accept
oifname "ens3" ip daddr 8.8.8.8 udp dport 53 ct state established,new counter packets 314 bytes 21912 accept
```

### Permite que la máquina cortafuegos pueda navegar por https.

Vamos a añadir la regla :

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter output oifname "ens3" ip protocol tcp tcp dport 443 ct state new,established  counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter input iifname "ens3" ip protocol tcp tcp sport 443  ct state established  counter accept
```

Vamos a comprobar que pidiendo las cabeceras , que es similar a navegar podemos ver un código 200 en https :

```bash
javiercruces@router-fw:~$ curl -I https://www.javiercd.es/
HTTP/2 200 
server: GitHub.com
content-type: text/html; charset=utf-8
last-modified: Sun, 25 Feb 2024 23:03:49 GMT
access-control-allow-origin: *
strict-transport-security: max-age=31556952
etag: "65dbc755-675b"
expires: Wed, 28 Feb 2024 10:10:17 GMT
cache-control: max-age=600
x-proxy-cache: MISS
x-github-request-id: 5CD4:0E10:CBDBE5:CFBAEA:65DF0430
accept-ranges: bytes
date: Wed, 28 Feb 2024 11:10:32 GMT
via: 1.1 varnish
age: 0
x-served-by: cache-mad22033-MAD
x-cache: HIT
x-cache-hits: 1
x-timer: S1709118632.338441,VS0,VE131
vary: Accept-Encoding
x-fastly-request-id: 01056938385ca0e465882fa75fd0b19d0973df62
content-length: 26459
```

### Los equipos de la red local deben poder tener conexión al exterior.

SNAT realizado anteriormente 

### Permitimos el ssh desde el cortafuegos a la LAN

Permitido por regla anterior 

### Permitimos hacer ping desde la LAN a la máquina cortafuegos.

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter output oifname "ens4" icmp type echo-reply counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter input iifname "ens4" icmp type echo-request counter accept
```

Realizamos el ping desde LAN al cortafuegos

```bash
debian@lan:~$ ping 192.168.100.2
PING 192.168.100.2 (192.168.100.2) 56(84) bytes of data.
64 bytes from 192.168.100.2: icmp_seq=1 ttl=64 time=1.09 ms
64 bytes from 192.168.100.2: icmp_seq=2 ttl=64 time=1.75 ms
^C
--- 192.168.100.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 1.091/1.419/1.748/0.328 ms
```

Veremos los hits para esta regla en concreto :

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
iifname "ens4" icmp type echo-request counter packets 2 bytes 168 accept
oifname "ens4" icmp type echo-reply counter packets 2 bytes 168 accept
```

### Permite realizar conexiones ssh desde los equipos de la LAN

Vamos a hacer las reglas :

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip protocol tcp ip saddr 192.168.100.0/24 tcp dport 22 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip protocol tcp ip daddr 192.168.100.0/24 tcp sport 22 ct state established counter accept
```

Vamos a conectarnos por ssh a una maquina fuera de la lan :

```bash
debian@lan:~$ ssh javiercruces@172.22.200.47
Linux odin.javiercd.gonzalonazareno.org 6.1.0-18-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.76-1 (2024-02-01) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Feb 28 10:36:26 2024 from 172.22.201.120
javiercruces@odin:~$ 
```

Vamos a ver los hits de estas reglas :

```bash
javiercruces@router-fw:~$ sudo nft -a list table inet filter
iifname "ens4" oifname "ens3" ip protocol tcp ip saddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 10 bytes 3312 accept # handle 44
iifname "ens3" oifname "ens4" ip protocol tcp ip daddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 7 bytes 3088 accept # handle 45
```

### Instala un servidor de correos en la máquina de la LAN. Permite el acceso desde el exterior y desde el cortafuegos al servidor de correos. Para probarlo puedes ejecutar un telnet al puerto 25 tcp.

Con estas reglas permitimos conectarnos desde fuera de la red al servidor de correos :

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 25 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 25 ct state established counter accept

# Regla DNAT puerto 25 
javiercruces@router-fw:~$ sudo nft add rule ip nat prerouting iifname "ens3" tcp dport 25 counter dnat to 192.168.100.10
```

Vamos a comprobarlo :

```bash
javiercruces@HPOMEN15:~/Documentos/2ºASIR/SAD/cortafuegos1$ telnet 172.22.201.120 25
Trying 172.22.201.120...
Connected to 172.22.201.120.
Escape character is '^]'.
220 lan.openstacklocal ESMTP Postfix (Debian/GNU)
Connection closed by foreign host.
```

Vamos a ver los hits en las reglas :

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
# Reglas para permitir el trafico
iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 25 ct state established,new counter packets 10 bytes 544 accept # handle 46
iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 25 ct state established counter packets 9 bytes 613 accept
# Regla DNAT
iifname "ens3" tcp dport 25 counter packets 1 bytes 60 dnat to 192.168.100.10

```


### Permite hacer conexiones ssh desde exterior a la LAN

Para ello voy a hacer un DNAT al puerto 2222 y a permitir ese trafico

```bash
# Reglas para permitir el trafico del DNAT
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 2222 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 2222 ct state established counter accept

# Regla DNAT puerto 2222 para ssh 
sudo nft add rule ip nat prerouting iifname "ens3" tcp dport 2222 counter dnat to 192.168.100.10
```

He cambiado el puerto del servicio ssh de lan al 2222 , voy a conectarme desde fuera a la LAN por ssh :

```bash
javiercruces@HPOMEN15:~/Documentos/2ºASIR/SAD/cortafuegos1$ ssh -p 2222 debian@172.22.201.120

Linux lan 6.1.0-12-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.52-1 (2023-09-07) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Feb 28 14:12:18 2024 from 192.168.100.2
debian@lan:~$ 
```

Vamos a comprobar los hits de las reglas :

```bash
# Reglas para permitir el ssh 2222 desde fuera hacia la LAN
iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 2222 ct state established,new counter packets 54 bytes 9784 accept
iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 2222 ct state established counter packets 44 bytes 10494 accept

# Regla DNAT
iifname "ens3" tcp dport 2222 counter packets 5 bytes 300 dnat to 192.168.100.10
```

### Modifica la regla anterior, para que al acceder desde el exterior por ssh tengamos que conectar al puerto 2222, aunque el servidor ssh este configurado para acceder por el puerto 22.

Para esto vamos a eliminar las 3 reglas anteriores y añadiremos las siguientes :

```bash
# Permitimos el trafico que ahora "cambiamos" el puerto con la regla DNAT de 2222 a 22
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter accept

# Regla DNAT
javiercruces@router-fw:~$ sudo nft add rule ip nat prerouting iifname "ens3" tcp dport 2222 counter dnat to 192.168.100.10
```

Ahora vamos a comprobar que podemos conectarnos desde el exterior a la LAN aunque ahora hemos cambiado el servidor ssh de LAN para que escuche en el puerto 22 :

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 34 bytes 7868 accept
iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 32 bytes 9066 accept
iifname "ens3" tcp dport 2222 counter packets 7 bytes 420 dnat to 192.168.100.10:22
```


### Permite hacer consultas DNS desde la LAN sólo al servidor 8.8.8.8. Comprueba que no puedes hacer un dig @1.1.1.1.

Vamos a borrar la regla anterior que permite las consultas DNS :

```bash
javiercruces@router-fw:~$ sudo nft -a list table inet filter
iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 udp dport 53 ct state established,new counter packets 285 bytes 17036 accept # handle 35


javiercruces@router-fw:~$ sudo nft delete rule inet filter forward handle 35
```

Añadimos la regla nueva para permitir solo consultas al 8.8.8.8 :

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 udp dport 53 ip daddr 8.8.8.8 counter accept
```

Vamos a comprobarlo :

```bash
debian@lan:~$ dig @1.1.1.1 www.javiercd.es
;; communications error to 1.1.1.1#53: timed out
;; communications error to 1.1.1.1#53: timed out
;; communications error to 1.1.1.1#53: timed out

; <<>> DiG 9.18.24-1-Debian <<>> @1.1.1.1 www.javiercd.es
; (1 server found)
;; global options: +cmd
;; no servers could be reached

debian@lan:~$ dig @8.8.8.8 www.javiercd.es

; <<>> DiG 9.18.24-1-Debian <<>> @8.8.8.8 www.javiercd.es
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 59302
;; flags: qr rd ra; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;www.javiercd.es.		IN	A

;; ANSWER SECTION:
www.javiercd.es.	3600	IN	CNAME	javierasping.github.io.
javierasping.github.io.	3600	IN	A	185.199.108.153
javierasping.github.io.	3600	IN	A	185.199.109.153
javierasping.github.io.	3600	IN	A	185.199.110.153
javierasping.github.io.	3600	IN	A	185.199.111.153

;; Query time: 72 msec
;; SERVER: 8.8.8.8#53(8.8.8.8) (UDP)
;; WHEN: Wed Feb 28 14:44:29 UTC 2024
;; MSG SIZE  rcvd: 144
```

Vamos a ver los hits de las reglas :

```bash
javiercruces@router-fw:~$ sudo nft -a list table inet filter

iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 udp dport 53 ip daddr 8.8.8.8 counter packets 3 bytes 218 accept # handle 53
```



### Permite que los equipos de la LAN puedan navegar por internet, excepto a la página www.realbetisbalompie.es

Tenemos un problema y es que nftables solo filtra hasta el nivel de transporte , es decir por puerto . Así que no podemos leer el dominio ya que este viaja en una cabecera del nivel de aplicación . 

Para prohibirlo , tendremos que bloquear esa IP en su totalidad para un determinado puerto , en mi caso van a ser el 80 y 443. 

Vamos a averiguar las IPS del dominio que queremos bloquear :

```bash
javiercruces@router-fw:~$ dig +short www.realbetisbalompie.es
realbetisbalompie.es.
51.255.76.196
```

La añadiremos al principio de la cadena en lugar de add añadimos la palabra insert : 

```bash
javiercruces@router-fw:~$ sudo nft insert rule inet filter forward ip daddr 51.255.76.196 tcp dport {80, 443} iifname "ens4" oifname "ens3" counter drop 
```

Y ahora no podremos navegar en la pagina del maligno :

```bash
debian@lan:~$ curl -I https://www.realbetisbalompie.es/
curl: (28) Failed to connect to www.realbetisbalompie.es port 443 after 129885 ms: Couldn't connect to server
```

Vamos a ver los hits de la regla que nos protege del mal :

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
ip daddr 51.255.76.196 tcp dport { 80, 443 } iifname "ens4" oifname "ens3" counter packets 7 bytes 420 drop
```


## Hacer las reglas persistentes 

Vamos a guardar las reglas con :

```bash
rott@router-fw:/home/javiercruces# nft list ruleset > /etc/nftables.conf
```

Si las queremos restaurar  : 

```bash
javiercruces@router-fw:~$ sudo nft -f /etc/nftables.conf
```


Para hacer que al reiniciar las reglas se restauren solas :

```bash
# Creamos la unidad de systemd
javiercruces@router-fw:~$ sudo cat /etc/systemd/system/nftables-persistent.service
[Unit]
Description=Cargar reglas de nftables al iniciar el sistema

[Service]
Type=oneshot
ExecStart=/usr/sbin/nft -f /etc/nftables/nftables.rules

[Install]
WantedBy=multi-user.target

# Activa el servicio para que al reiniciar se apliquen los cambios 
javiercruces@router-fw:~$ sudo systemctl enable nftables-persistent.service
```

## Reglas al final del ejercicio

Te dejo la lista de las reglas en el estado del ultimo ejercicio :

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
table inet filter {
	chain input {
		type filter hook input priority filter; policy drop;
		counter packets 34414 bytes 6500685
		iif "ens3" tcp dport 22 ct state established,new counter packets 21235 bytes 1526616 accept
		iifname "ens4" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 11648 bytes 1793088 accept
		iifname "lo" counter packets 92 bytes 17660 accept
		iifname "ens3" icmp type echo-request counter packets 1 bytes 84 accept
		iifname "ens3" tcp sport 22 ct state established counter packets 66 bytes 18624 accept
		iifname "ens3" ip protocol tcp tcp sport 443 ct state established counter packets 519 bytes 3016033 accept
		iifname "ens3" ip saddr 8.8.8.8 udp sport 53 ct state established counter packets 557 bytes 68077 accept
		iifname "ens4" icmp type echo-request counter packets 2 bytes 168 accept
	}

	chain output {
		type filter hook output priority filter; policy drop;
		counter packets 86303 bytes 8331992
		oif "ens3" tcp sport 22 ct state established counter packets 15004 bytes 3534878 accept
		oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 14125 bytes 950568 accept
		oifname "lo" counter packets 92 bytes 17660 accept
		oifname "ens3" icmp type echo-reply counter packets 1 bytes 84 accept
		oifname "ens3" tcp dport 22 ct state established,new counter packets 89 bytes 16572 accept
		oifname "ens3" ip daddr 8.8.8.8 udp dport 53 ct state established,new counter packets 557 bytes 36254 accept
		oifname "ens3" ip protocol tcp tcp dport 443 ct state established,new counter packets 367 bytes 25011 accept
		oifname "ens4" icmp type echo-reply counter packets 2 bytes 168 accept
	}

	chain forward {
		type filter hook forward priority filter; policy drop;
		ip daddr 51.255.76.196 tcp dport { 80, 443 } iifname "ens4" oifname "ens3" counter packets 7 bytes 420 drop
		counter packets 45573 bytes 149083811
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 icmp type echo-request counter packets 32 bytes 2688 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 icmp type echo-reply counter packets 18 bytes 1512 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 udp sport 53 ct state established counter packets 664 bytes 101857 accept
		iifname "ens4" oifname "ens3" ip protocol tcp ip saddr 192.168.100.0/24 tcp dport { 80, 443 } ct state established,new counter packets 34813 bytes 1843071 accept
		iifname "ens3" oifname "ens4" ip protocol tcp ip daddr 192.168.100.0/24 tcp sport { 80, 443 } ct state established counter packets 7583 bytes 146852066 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 80 ct state established,new counter packets 47 bytes 3905 accept
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 80 ct state established counter packets 32 bytes 24161 accept
		iifname "ens4" oifname "ens3" ip protocol tcp ip saddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 72 bytes 18540 accept
		iifname "ens3" oifname "ens4" ip protocol tcp ip daddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 56 bytes 17296 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 25 ct state established,new counter packets 10 bytes 544 accept
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 25 ct state established counter packets 9 bytes 613 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 90 bytes 17200 accept
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 77 bytes 19296 accept
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 udp dport 53 ip daddr 8.8.8.8 counter packets 81 bytes 5250 accept
	}
}
table ip nat {
	chain prerouting {
		type nat hook prerouting priority filter; policy accept;
		iifname "ens3" tcp dport 80 counter packets 4 bytes 240 dnat to 192.168.100.10
		iifname "ens3" tcp dport 25 counter packets 1 bytes 60 dnat to 192.168.100.10
		iifname "ens3" tcp dport 2222 counter packets 8 bytes 480 dnat to 192.168.100.10:22
	}

	chain postrouting {
		type nat hook postrouting priority srcnat; policy accept;
		oifname "ens3" ip saddr 192.168.100.0/24 counter packets 916 bytes 61536 masquerade
	}
}
```