---
title: "VPN sitio a sitio con IPsec Fortinet"
date: 2024-03-28T10:00:00+00:00
description: VPN sitio a sitio con IPsec Fortinet
tags: [VPN,LINUX,FORTINET]
hero: /images/cortafuegos/fortinet.png
---

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GVDYVWJLRH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GVDYVWJLRH');
</script>

En este post voy a montar una VPN IPSEC usando cortafuegos Fortinet  , para ello los visualizaré en GNS3 .


![](../img/Pastedimage20240330235321.png)

## Preparación del escenario 

Para crear la VPN añadiré al escenario un nuevo Fortigate . 

Así que vamos a proceder a configurarlo , lo primero sera conocer la IP que le ha dado el DHCP :

```bash
FortiGate-VM64-KVM login: admin
Password: 
You are forced to change your password. Please input a new password.
New Password: 
Confirm Password: 
Welcome!

FortiGate-VM64-KVM # get system interface physical port1
== [onboard]
	==[port1]
		mode: dhcp
		ip: 192.168.122.22 255.255.255.0
		ipv6: ::/0
		status: up
		speed: 1000Mbps (Duplex: full)
		FEC: none
		FEC_cap: none

```

Esta IP que me ha dado por DHCP se la configurare como estática .

En cuanto a la red local del nuevo FortiNet , va a tener la red 192.168.30.0 :

![](../img/Pastedimage20240330231700.png)

Por ultimo configurare en este la ruta por defecto hacia la dirección IP de de la nube NAT la 192.168.122.1/24 :

![](../img/Pastedimage20240330235554.png)

Una vez hecho esto vamos a ver que tenemos conectividad entre ambos cortafuegos , desde FGT --> FTG2 :

![](../img/Pastedimage20240330235822.png)

Y al revés desde FTG2 --> FTG :

![](../img/Pastedimage20240330235850.png)


## VPN site to site

Nos dirigimos primero al FortiGate FTG que es el que contiene los clientes de Odin,Loki,Thor y Hela . Y iremos a IPsec Wizard , le pondré un nombre significativo con el nombre de los hosts :

![](../img/Pastedimage20240331000231.png)

En el siguiente paso vamos a indicar la IP del FortiGate FTG2 , la interfaz por donde saldrá el trafico y por ultimo una "llave" compartida entre los dos extremos , esta ultima parte puede sustituirse por certificados :

![](../img/Pastedimage20240331000351.png)

A continuación indicaremos las redes locales de ambos extremos donde queremos tener conectividad :

![](../img/Pastedimage20240331000638.png)

Nos saldrá un panel con los distintos objetos que se van a crear y le daremos a crear :

![](../img/Pastedimage20240331000725.png)

Repetiremos el mismo proceso en el otro Fortigate , crearemos un túnel site to site : 

![](../img/Pastedimage20240331000751.png)

Le diremos la IP publica del otro extremo y pondremos la misma clave compartida :

![](../img/Pastedimage20240331000810.png)

Ahora le diremos cual es nuestra red local y la red remota :

![](../img/Pastedimage20240331000833.png)

Por ultimo nos dirá los objetos que se van a crear y le damos a crear :

![](../img/Pastedimage20240331000845.png)

Ahora si accedemos a los paneles de IPsec Tunnels veremos que en unos segundos ambos túneles se levantaran :

![](../img/Pastedimage20240331012140.png)

![](../img/Pastedimage20240331012156.png)

### Comprobación de funcionamiento

Una vez llegado a este punto veremos que la VPN esta funcionando .  Podemos hacer un ping en ambas direcciones :

```bash
debian@cliente1:~$ ping 192.168.100.4 -c 1
PING 192.168.100.4 (192.168.100.4) 56(84) bytes of data.
64 bytes from 192.168.100.4: icmp_seq=1 ttl=62 time=1.22 ms

--- 192.168.100.4 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 1.220/1.220/1.220/0.000 ms

debian@thor:~$ ping 192.168.30.2 -c 1
PING 192.168.30.2 (192.168.30.2) 56(84) bytes of data.
64 bytes from 192.168.30.2: icmp_seq=1 ttl=62 time=1.52 ms

--- 192.168.30.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 1.516/1.516/1.516/0.000 ms
```

Como vemos tenemos conectividad entre las 2 redes privadas a través de la VPN . 

Si nos paramos a ver los objetos que nos ha creado cada túnel , este nos ha creado un total de 4 , los cuales tendremos que borrar si deseamos eliminar el túnel :


![](../img/Pastedimage20240331012446.png)

Por defecto la política que nos ha creado permite TODO el trafico en ambas direcciones , estas 2 políticas la tenemos creada en cada cortafuegos y modificando estas o añadiendo nuevas podemos limitar el trafico que pasa por la VPN en función de nuestras necesidades .

![](../img/Pastedimage20240331012606.png)

Ademas nos habrá creado una ruta para encaminar el trafico hacia la red privada del otro extremo :

![](../img/Pastedimage20240331012805.png)
