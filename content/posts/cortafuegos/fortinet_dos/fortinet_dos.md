---
title: "Implementación de un cortafuegos perimetral con Fortinet II"
date: 2024-03-28T10:00:00+00:00
description: Implementación de un cortafuegos perimetral con Fortinet II
tags: [FIREWALL,LINUX,DEBIAN,FORTINET]
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



Ahora vamos a emular la práctica de cortafuegos II, pero en GNS3. Para ello, he transformado al cliente 1 en Odin, además he añadido a Thor y Loki como máquinas virtuales en lugar de contenedores en la red LAN. También he creado una nueva red llamada DMZ, en la cual estará la máquina Hela.

Dado que he transformado el escenario anterior en este nuevo, contamos con algunas reglas creadas anteriormente. Por lo tanto, eliminaré del enunciado aquellas que ya estén creadas, como la de hacer SSH a Odin desde el puerto 2222, pero con el servicio escuchando en el 22.

Además, ahora vamos a hacer unas reservas DHCP para tener controladas las IP de las nuevas máquinas.

Ademas como no cuento con los servicios montados en el antiguo escenario en Opsentack y para las reglas del enunciado montare lo mínimo para hacer que funcionen las reglas . 

A lo largo de esta practica te explicare que por como esta montado la topologia de la red , todos de la red LAN pueden comunicarse entre sin necesidad de pasar por el cortafuegos . Así que en algunos ejercicios omitiré la parte de hacer que Loki y Thor se comuniquen con Odin.  Ademas no voy  a montar el servidor DNS ni LDAP ya que las reglas de DNAT son bastante sencillas y a lo largo de la practica aparecen varios ejercicios de hacer DNAT entre las distintas redes . En lugar de esto voy a añadir VPN al final de la misma ya que lo veo mas interesante que repetir las mismas reglas cambiando el servicio .   

![](../img/Pastedimage20240329110607.png)

## Preparación del escenario 

Lo primero que haré sera crear una nueva red en el puerto 3 , que corresponde a la red DMZ .

Como veras en la imagen a continuación he seleccionado que el rol sea LAN , para que me permita tener un servidor DHCP en esa red . Como es una red en la que albergara los servicios no quiero que desde esta se pueda acceder a configurar el cortafuegos así que dejare la administración desactivada .

![](../img/Pastedimage20240329160410.png)

Ahora iré accediendo a los nuevos clientes y les cambiare el nombre de maquina y configurándolas por DHCP .

Maquina Odin , esta era anteriormente la maquina cliente 1 , solo hay que cambiarle el FQDN y el hostname :

```bash
osboxes@odin:~$ hostname -f
odin.javiercd.gonzalonazareno.org
osboxes@odin:~$ ip -4 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    altname enp0s3
    inet 192.168.100.2/24 brd 192.168.100.255 scope global dynamic noprefixroute ens3
       valid_lft 604790sec preferred_lft 604790sec
```

Maquina Thor :

```bash
debian@thor:~$ hostname -f
thor.javiercd.gonzalonazareno.org
debian@thor:~$ ip -4 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    altname enp0s3
    inet 192.168.100.4/24 brd 192.168.100.255 scope global dynamic ens3
       valid_lft 604791sec preferred_lft 604791sec
debian@thor:~$ 
```

Maquina Loki :

```bash
debian@loki:~$ hostname -f
loki.javiercd.gonzalonazareno.org
debian@loki:~$ ip -4 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    altname enp0s3
    inet 192.168.100.3/24 brd 192.168.100.255 scope global dynamic ens3
       valid_lft 604724sec preferred_lft 604724sec
```

Maquina Hela : 

```bash
debian@hela:~$ hostname -f
hela.javiercd.gonzalonazareno.org
debian@hela:~$ ip -4 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    altname enp0s3
    inet 192.168.200.2/24 brd 192.168.200.255 scope global dynamic ens3
       valid_lft 604795sec preferred_lft 604795sec
```


Ahora vamos a hacer unas reservas en el servidor DHCP , accederemos a Dashborad > Networks > DHCP , una vez aquí le daremos clic derecho sobre cada cliente de los 4 que tenemos en el escenario y le crearemos una reserva : 

![](../img/Pastedimage20240329162616.png)

Nos saldrá un menú similar a este para enlazar la dirección MAC a la IP :

![](../img/Pastedimage20240329162730.png)

Una vez hagamos esto con nuestro clientes nos indicara que tenemos la reserva hecha :

![](../img/Pastedimage20240329162855.png)


## Reglas del cortafuegos

Vamos a comenzar a crear las reglas , como dije anteriormente partimos del escenario anterior , así que algunas reglas para el funcionamiento mínimo de la red están creadas . 

Te dejo una captura de como se quedaron las reglas , para que veas del estado en el que partimos  :

![](../img/Pastedimage20240329163530.png)

Algunas de las siguiente reglas ya esta configurada del ejercicio anterior , como la siguiente regla --> *La máquina Odin tiene un servidor ssh escuchando por el puerto 22, pero al acceder desde el exterior habrá que conectar al puerto 2222*

```bash
javiercruces@HPOMEN15:~$ ssh osboxes@192.168.122.77 -p 2222
osboxes@192.168.122.77's password: 
Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.0-25-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

560 updates can be applied immediately.
339 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable

Last login: Fri Mar 29 11:23:44 2024 from 192.168.100.1
osboxes@odin:~$ hostname -f
odin.javiercd.gonzalonazareno.org
```

A continuación veras que hay algunas reglas que he eliminado o modificado , ya que en el escenario actual no se pueden hacer , bien o por la topología o porque anteriormente la maquina Odin era el cortafuegos . En cualquier caso alguna he mantenido y he explicado algunas cosas adicionales . 


### Desde Thor y Hela se debe permitir la conexión ssh por el puerto 22 a la máquina Odin. 

Esta regla no la podemos realizar ya que al tener un switch de por medio interconectando los dispositivos , el trafico no pasara por el cortafuegos por lo que no podremos aplicar reglas en el cortafuego para impedir el trafico local . 

![](../img/Pastedimage20240329170454.png)

Veras que aunque cree la regla , en el cortafuegos esta no se inmutara :

![](../img/Pastedimage20240329170554.png)

Ves que por ejemplo si me conecto desde loki o desde thor puedo llegar a odin :

```bash
debian@loki:~$ ssh osboxes@192.168.100.2
osboxes@192.168.100.2's password: 
Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.0-25-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

560 updates can be applied immediately.
339 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable

Last login: Fri Mar 29 11:42:43 2024 from 192.168.100.3
osboxes@odin:~$ 
```

Pero no llego por la regla que he creado si no por la propia topologia de la red , la regla no tiene hits :

![](../img/Pastedimage20240329170725.png)

Todo el trafico se encarga de redirigirlo el swicht .
### A la máquina Odin se le puede hacer ping desde la DMZ, pero desde la LAN se le debe rechazar la conexión (REJECT) y desde el exterior se rechazará de manera silenciosa. 

Para permitir que desde la red DMZ podamos hacer ping hacia Odin crearemos la siguiente regla :

![](../img/Pastedimage20240329171345.png)

Vamos a comprobar que desde la DMZ podemos hacer el ping a Odin :

```bash
debian@hela:~$ ping 192.168.100.2 -c 1
PING 192.168.100.2 (192.168.100.2) 56(84) bytes of data.
64 bytes from 192.168.100.2: icmp_seq=1 ttl=63 time=2.38 ms

--- 192.168.100.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 2.379/2.379/2.379/0.000 ms
```

Como vemos la regla esta funcionando , así que vamos a comprobar los hits :

![](../img/Pastedimage20240329171520.png)

Por el mismo motivo que en el ejercicio anterior , desde la red LAN no podemos limitar el ping hacia Odin ya que no pasa por el cortafuegos si no por el switch .

Algo parecido nos pasara desde la WAN , al ser un ping dirigido a la IP de la interfaz este se desactiva desde la configuración de la misma , siempre se rechaza de manera silenciosa pero no da opción a elegirlo  :

![](../img/Pastedimage20240329172526.png)

Una vez eliminado 

```bash
javiercruces@HPOMEN15:~$ ping 192.168.122.77 -c 1
PING 192.168.122.77 (192.168.122.77) 56(84) bytes of data.

--- 192.168.122.77 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 0ms
```

### La máquina Odin puede hacer ping a la LAN, la DMZ y al exterior. 

La maquina Odin por la propia topologia puede hacerle ping a todas las maquinas de la LAN ya que el trafico hacia esta red pasa por el swicht .

Para que pueda hacer ping hacia la  DMZ y a la WAN vamos a crear dos reglas :

La regla para la WAN :

![](../img/Pastedimage20240329172816.png)

La regla para la DMZ :

![](../img/Pastedimage20240329172903.png)

```bash
# LAN --> WAN
osboxes@odin:~$ ping 8.8.8.8 -c 1
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=114 time=10.1 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 10.088/10.088/10.088/0.000 ms

# LAN --> DMZ
osboxes@odin:~$ ping 192.168.200.2 -c 1
PING 192.168.200.2 (192.168.200.2) 56(84) bytes of data.
64 bytes from 192.168.200.2: icmp_seq=1 ttl=63 time=0.804 ms

--- 192.168.200.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.804/0.804/0.804/0.000 ms

# LAN --> LAN (No interviene el cortafuegos)
osboxes@odin:~$ ping 192.168.100.3 -c 1
PING 192.168.100.3 (192.168.100.3) 56(84) bytes of data.
64 bytes from 192.168.100.3: icmp_seq=1 ttl=64 time=0.503 ms

--- 192.168.100.3 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.503/0.503/0.503/0.000 ms
```

Vamos a comprobar los hits de las dos reglas que acabamos de crear :

![](../img/Pastedimage20240329173231.png)
### Desde la máquina Hela se puede hacer ping y conexión ssh a las máquinas de la LAN. 

Para lograr esto creare la siguiente regla . Podríamos separarla en 2 reglas independientes para tener los contadores por separado , pero en este caso no es importante distinguir el trafico .

![](../img/Pastedimage20240329173630.png)

Vamos a comprobar la regla , haciendo un ping a las distintas maquinas de la red LAN , ya que anteriormente había una regla para permitir todos los pings hacia Odin :

```bash
# HELA --> ODIN
debian@hela:~$ ping 192.168.100.2 -c 1
PING 192.168.100.2 (192.168.100.2) 56(84) bytes of data.
64 bytes from 192.168.100.2: icmp_seq=1 ttl=63 time=1.10 ms

--- 192.168.100.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 1.101/1.101/1.101/0.000 ms

# HELA --> LOKI
debian@hela:~$ ping 192.168.100.3 -c 1
PING 192.168.100.3 (192.168.100.3) 56(84) bytes of data.
64 bytes from 192.168.100.3: icmp_seq=1 ttl=63 time=1.73 ms

--- 192.168.100.3 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 1.730/1.730/1.730/0.000 ms

# HELA --> THOR
debian@hela:~$ ping 192.168.100.4 -c 1
PING 192.168.100.4 (192.168.100.4) 56(84) bytes of data.
64 bytes from 192.168.100.4: icmp_seq=1 ttl=63 time=0.998 ms

--- 192.168.100.4 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.998/0.998/0.998/0.000 ms
```

Ahora vamos a comprobar que podemos conectarnos por ssh desde Hela a la LAN :

```bash
debian@hela:~$ ssh osboxes@192.168.100.2 'hostname -f'
osboxes@192.168.100.2's password: 
odin.javiercd.gonzalonazareno.org

debian@hela:~$ ssh 192.168.100.3 'hostname -f'
debian@192.168.100.3's password: 
loki.javiercd.gonzalonazareno.org

debian@hela:~$ ssh 192.168.100.4 'hostname -f'
debian@192.168.100.4's password: 
thor.javiercd.gonzalonazareno.org
```

La regla funciona correctamente , vamos a comprobar que ha subido los hits :

![](../img/Pastedimage20240329174824.png)

### Desde cualquier máquina de la LAN se puede conectar por ssh a la máquina Hela. 

 Para ello vamos a crear la siguiente regla :

![](../img/Pastedimage20240329175356.png)

Ahora vamos a comprobar la regla que acabamos de crear :

```bash
osboxes@odin:~$ ssh debian@192.168.200.2 'hostname -f'
debian@192.168.200.2's password: 
hela.javiercd.gonzalonazareno.org

debian@loki:~$ ssh 192.168.200.2 'hostname -f'
debian@192.168.200.2's password: 
hela.javiercd.gonzalonazareno.org

debian@thor:~$ ssh 192.168.200.2 'hostname -f'
debian@192.168.200.2's password: 
hela.javiercd.gonzalonazareno.org
```

Vamos a comprobar que los hits de la regla han subido :

![](../img/Pastedimage20240329175844.png)

### Configura la máquina Odin para que las máquinas de LAN y DMZ puedan acceder al exterior. 

El SNAT en este dispositivo podemos elegir activarlo por cada regla y no en general . Si te has fijado a lo largo de la practica en todas las reglas que implica dar un salto de interfaz he marcado la casilla NAT :

![](../img/Pastedimage20240329180159.png)

Por lo que este apartado se va a ir realizando a lo largo de la practica conforme creemos las reglas . 
### Las máquinas de la LAN pueden hacer ping al exterior y navegar. 

Vamos a tener que crear 3 reglas :
- Permitir el trafico HTTP/HTTPS
- Permitir las consultas DNS
- Permitir hacer ping

De estas tres reglas las dos primeras están creadas con anterioridad :

![](../img/Pastedimage20240329184029.png)

Por lo que solo nos queda añadir la regla del ping , que seria la siguiente :

![](../img/Pastedimage20240329184222.png)

Como tengo una versión de prueba puedo tener como máximo 10 entradas , así que voy a eliminar la que solo deja hacer ping al exterior a Odin .

Vamos a comprobar las reglas , desde un cliente de la red LAN:

```bash
osboxes@odin:~$ dig @8.8.8.8 www.javiercd.es

; <<>> DiG 9.18.1-1ubuntu1-Ubuntu <<>> @8.8.8.8 www.javiercd.es
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 25764
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

;; Query time: 60 msec
;; SERVER: 8.8.8.8#53(8.8.8.8) (UDP)
;; WHEN: Fri Mar 29 13:44:50 EDT 2024
;; MSG SIZE  rcvd: 144

osboxes@odin:~$ ping -c 1 www.javiercd.es
PING javierasping.github.io (185.199.108.153) 56(84) bytes of data.
64 bytes from cdn-185-199-108-153.github.com (185.199.108.153): icmp_seq=1 ttl=55 time=11.1 ms

--- javierasping.github.io ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 11.111/11.111/11.111/0.000 ms

osboxes@odin:~$ curl -I  https://www.javiercd.es/
HTTP/2 200 
server: GitHub.com
content-type: text/html; charset=utf-8
last-modified: Mon, 11 Mar 2024 23:21:37 GMT
access-control-allow-origin: *
strict-transport-security: max-age=31556952
etag: "65ef9201-6878"
expires: Fri, 29 Mar 2024 17:56:01 GMT
cache-control: max-age=600
x-proxy-cache: MISS
x-github-request-id: AE88:3308D5:438AA74:448F970:6606FE58
accept-ranges: bytes
date: Fri, 29 Mar 2024 17:46:01 GMT
via: 1.1 varnish
age: 0
x-served-by: cache-mad2200143-MAD
x-cache: MISS
x-cache-hits: 0
x-timer: S1711734362.862201,VS0,VE134
vary: Accept-Encoding
x-fastly-request-id: 16b6048f2b032ef4b4293c52f0ae36d19b0e0da0
content-length: 26744


```

Así quedarían nuestras tres reglas , veremos que tenemos hits en las mismas  :

![](../img/Pastedimage20240329184410.png)

### La máquina Hela puede navegar. Instala un servidor web, un servidor ftp y un servidor de correos si no los tienes aún. 

Para realizar esto es necesario tener permitido el DNS y la navegación . Para ello he creado la siguiente regla :

![](../img/Pastedimage20240329184830.png)

La he creado en una sola regla para ahorrar en el numero de las mismas , he borrado las que permitía el ping desde DMZ a LAN de ejercicios anteriores . 

```bash
debian@hela:~$ sudo apt install proftpd postfix apache2 -y
```

### Configura la máquina Odin para que los servicios web y ftp sean accesibles desde el exterior. 

Para hacer el DNAT deberemos de crear 2 IPs virtuales , como hicimos en cortafuegos I .

Una para cada servicio que queramos hacer un DNAT . Para el servidor web : 

![](../img/Pastedimage20240329190416.png)

Y para el servidor FTP :

![](../img/Pastedimage20240329190509.png)

Ahora vamos a crear la propia regla de DNAT para el servidor web , en la cual como destino indicamos la IP virtual que acabamos de crear :

![](../img/Pastedimage20240329191130.png)

Veremos que si accedemos a la IP del cortafuegos de la WAN accederemos al apache de Hela :

![](../img/Pastedimage20240329191232.png)

También crearemos la regla DNAT para el servidor FTP :

![](../img/Pastedimage20240329191852.png)

Vamos a comprobar el acceso al servidor ftp :

```bash
javiercruces@HPOMEN15:~$ ftp debian@192.168.122.77
Connected to 192.168.122.77.
220 ProFTPD Server (Debian) [::ffff:192.168.200.2]
331 Password required for debian
Password: 
230 User debian logged in
Remote system type is UNIX.
Using binary mode to transfer files.
ftp>
```

Si comprobamos los hits de las reglas veremos que en ambas ha subido :

![](../img/Pastedimage20240329192338.png)


### El servidor web y el servidor ftp deben ser accesibles desde la LAN y desde el exterior. 

Para realizar este ejercicio deberemos de volver a generar las 2 IPs virtuales pero ahora indicaremos la IP de la tarjeta LAN del firewall . 

Para el DNAT del servidor web :

![](../img/Pastedimage20240329192709.png)

Repetiremos lo mismo para el servicio FTP , cambiando el servicio :

![](../img/Pastedimage20240329192818.png)

Ahora crearemos las 2 reglas de DNAT para permitir el acceso desde la LAN .

Para el servidor web :

![](../img/Pastedimage20240329193041.png)

Para el servidor FTP:

![](../img/Pastedimage20240329193132.png)

Vamos a comprobar que podemos acceder a ambos servicios :

```bash
osboxes@odin:~$ curl -I  http://192.168.100.1
HTTP/1.1 200 OK
Date: Fri, 29 Mar 2024 18:31:59 GMT
Server: Apache/2.4.57 (Debian)
Last-Modified: Fri, 29 Mar 2024 17:53:38 GMT
ETag: "29cd-614d051d4d640"
Accept-Ranges: bytes
Content-Length: 10701
Vary: Accept-Encoding
Content-Type: text/html

osboxes@odin:~$ ftp debian@192.168.100.1
Connected to 192.168.100.1.
220 ProFTPD Server (Debian) [::ffff:192.168.200.2]
331 Password required for debian
Password: 
230 User debian logged in
Remote system type is UNIX.
Using binary mode to transfer files.
```

Vamos a comprobar que han subido los hits en las reglas :

![](../img/Pastedimage20240329193324.png)

### El servidor de correos sólo debe ser accesible desde la LAN. 

Volvemos a repetir los mismos pasos , le crearemos una IP virtual para poder hacer la regla de DNAT :

![](../img/Pastedimage20240329193427.png)

Ahora vamos a crear la regla de DNAT :

![](../img/Pastedimage20240329193724.png)

Y comprobaremos que desde un PC de la LAN haciendo un telnet llegamos al servidor de correos :

```bash
osboxes@odin:~$ telnet 192.168.100.1 25
Trying 192.168.100.1...
Connected to 192.168.100.1.
Escape character is '^]'.
220 hela.javiercd.gonzalonazareno.org ESMTP Postfix (Debian/GNU)
quit
221 2.0.0 Bye
Connection closed by foreign host.
```

Veremos que el hit de la regla ha subido :

![](../img/Pastedimage20240329193822.png)

### En la máquina Loki instala un servidor Postgres si no lo tiene aún. A este servidor se puede acceder desde la DMZ, pero no desde el exterior.

Volveremos a repetir el proceso de crear una nueva IP virtual para este servicio . Ademas en este caso he tenido que crear el servicio ya que no existía . 

![](../img/Pastedimage20240329195211.png)

Vamos a crear la regla de DNAT :

![](../img/Pastedimage20240329200331.png)

Vamos a comprobar que tenemos acceso al servidor pgsql desde la red DMZ :

```bash
debian@hela:~$ psql -h 192.168.200.1 -U postgres -W
Password: 
psql (15.6 (Debian 15.6-0+deb12u1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, compression: off)
Type "help" for help.

postgres=# \q
```

Comprobaremos que la regla tiene hits :

![](../img/Pastedimage20240329200721.png)

### Evita ataques DoS por ICMP Flood, limitando a 4 el número de peticiones por segundo desde una misma IP.

Dentro del apartado de políticas y objetos , encontramos un apartado para crear políticas para DoS . En mi caso he creado una con los valores recomendados que da el fabricante . Y he cambiado el limite de ICMP Flood a 4 paquetes por segundo . 

![](../img/Pastedimage20240329203201.png)

![](../img/Pastedimage20240329203221.png)

Vamos a comprobar que nos bloquea el trafico si excedemos ese limite . Con este comando estamos enviando 3 paquetes por segundo que es inferior al limite establecido asi que no cortara ningún paquete :

```bash
debian@loki:~$ sudo hping3 --icmp  -i u333333 -V 192.168.100.1
--- 192.168.100.1 hping statistic ---
124 packets transmitted, 124 packets received, 0% packet loss
round-trip min/avg/max = 0.7/5.3/9.9 ms
```

Si aumentamos los de paquetes por segundos , bloqueara todos los paquetes que superen a 4 por segundo , por eso deja pasar los 4 primeros de cada segundo :

```bash
debian@loki:~$ sudo hping3 --icmp  -i u200000 -V 192.168.100.1
--- 192.168.100.1 hping statistic ---
44 packets transmitted, 10 packets received, 78% packet loss
round-trip min/avg/max = 4.6/5.5/6.5 ms
```

El cortafuegos ha registrado como una anomalía el trafico que ha tirado :

![](../img/Pastedimage20240329224119.png)


### Evita ataques DoS por SYN Flood.

Con el filtro que hemos activado en el ejercicio anterior tenemos limitada las peticiones TCP a 2000 por minuto desde la misma IP para evitar este tipo de ataque . Vemos que el filtro elimina las peticiones maliciosas y no deja que el ataque tenga efecto :

```bash
debian@loki:~$ sudo hping3 --flood --rand-source -V 192.168.100.1
using ens3, addr: 192.168.100.3, MTU: 1500
HPING 192.168.100.1 (ens3 192.168.100.1): NO FLAGS are set, 40 headers + 0 data bytes
hping in flood mode, no replies will be shown
^C
--- 192.168.100.1 hping statistic ---
930716 packets transmitted, 0 packets received, 100% packet loss
round-trip min/avg/max = 0.0/0.0/0.0 ms
```

### Evita que realicen escaneos de puertos a Odin.

En lugar de hacerlo a Odin por la propia topologia vamos a hacerlo para evitar escaneos desde la WAN . 

Para ello nos abrimos una terminal y lo que vamos a hacer es crear una firma de IPS para evitar los paquetes con una determinada bandera que usa un escaneo determinado . En este caso vamos a evitar el escaneo de NMAP XMAS .

```bash
FTG # config ips custom

FTG (custom) # edit "Block_xmas"
new entry 'Block_xmas' added

FTG (Block_xmas) # set signature "F-SBID(--name 'Block_xmas'; --protocol tcp; --flow from_client; --tcp_flags *FUP; )"

FTG (Block_xmas) # set action block

FTG (Block_xmas) #  end
```

Una vez configurado nos aparecera la regla que hemos creado en IPs signatures :

![](../img/Pastedimage20240330185917.png)

Ahora vamos a crear una regla IPS para asociarla con esta politica de firmas :

![](../img/Pastedimage20240330190210.png)

Añadiremos en IPS signatures and filters , el nuevo filtro que hemos creado anteriormente :

![](../img/Pastedimage20240330190138.png)

A continuación en las reglas de DNAT donde queramos controlar que no sepan que puertos tenemos abiertos , asignaremos la nueva política IPS :

![](../img/Pastedimage20240330190438.png)

En mi caso vamos a probarlo para la regla DNAT de ssh :

![](../img/Pastedimage20240330190507.png)

Si lanzo el NMAP desde mi host que esta en la red WAN , vemos que el puerto 2222 que es el que esta regla tiene abierto no lo detecta :

```bash
javiercruces@HPOMEN15:~$ sudo nmap -sX 192.168.122.77
Starting Nmap 7.93 ( https://nmap.org ) at 2024-03-30 19:05 CET
Nmap scan report for 192.168.122.77
Host is up (0.00059s latency).
All 1000 scanned ports on 192.168.122.77 are in ignored states.
Not shown: 1000 open|filtered tcp ports (no-response)
MAC Address: 0C:18:45:93:00:00 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 21.28 seconds
```

Y el propio cortafuegos nos avisara de que ha habido un escaneo de puertos que ha bloqueado , para ver esto dirígete a Log & Report > Intrusion prevention :

![](../img/Pastedimage20240330191024.png)

Podemos seleccionarlo para ver mas detalles del mismo :

![](../img/Pastedimage20240330191131.png)
![](../img/Pastedimage20240330191146.png)