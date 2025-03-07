---
title: "VPN site to site con OpenVPN y certificados x509"
date: 2024-03-28T10:00:00+00:00
description: VPN site to site con OpenVPN y certificados x509
tags: [VPN,CISCO,LINUX,DEBIAN,OPENVPN]
hero: /images/vpn/sitetosite.png
---



## Montando el escenario 

Para realizar este ejercicio he montado el siguiente escenario en GNS3 :

![](/vpn/site_to_site_openvpn/img/Pastedimage20240114150833.png)

### Configuración del router cisco
Vamos a darle a cada interfaz la configuración de red correspondiente :

```bash
# Interfaz que nos dará internet 
R1#configure terminal 
R1(config)#interface fastEthernet 0/0
R1(config-if)#ip add dhcp
R1(config-if)#no shut
R1(config-if)#exit

# Interfaz red Servidor 1 
R1(config)#interface fastEthernet 1/0
R1(config-if)#ip add 90.0.0.1 255.255.255.0
R1(config-if)#no shut
R1(config-if)#exit

# Interfaz red Servidor 2 
R1(config)#interface fastEthernet 1/1
R1(config-if)#ip add 100.0.0.1 255.255.255.0
R1(config-if)#no shut
R1(config-if)#exit

# Ruta por defecto para internet
R1(config)#ip route 0.0.0.0 0.0.0.0 192.168.122.1

# Guarda la configuración
R1#write

# Configuración de SNAT
R1#conf term

R1(config)#access-list 1 permit 90.0.0.0 0.0.0.255
R1(config)#access-list 1 permit 100.0.0.0 0.0.0.255

R1(config)# ip nat pool NAT-Pool 192.168.122.127 192.168.122.127 prefix-length 24
R1(config)#ip nat inside source list 1 pool NAT-Pool overload

R1(config)#interface FastEthernet0/0
R1(config-if)#ip nat outside

R1(config)#interface FastEthernet1/0
R1(config-if)#ip nat inside

R1(config)#interface FastEthernet1/1
R1(config-if)#ip nat inside
```

#### Configuración del Servidor 1

Configuración de red servidor 1 : 

```bash
debian@servidor1:~$ cat /etc/network/interfaces

auto lo
iface lo inet loopback

auto ens3
iface ens3 inet static
        address 90.0.0.2
        netmask 255.255.255.0
        gateway 90.0.0.1
        dns-nameservers 8.8.8.8

auto ens4
iface ens4 inet static
        address 192.168.0.1
        netmask 255.255.255.0
```

Ademas configuraremos el SNAT :

```bash
#Activa el bit de forwarding 
debian@servidor1:~$ sudo nano /etc/sysctl.conf 
net.ipv4.ip_forward=1 

# Regla SNAT
debian@servidor1:~$ sudo iptables -t nat -A POSTROUTING -o ens3 -s 192.168.0.0/24 -j MASQUERADE

# Te recomiendo que lo hagas permanente , configura iptables-persistent
debian@servidor1:~$ sudo apt install iptables-persistent 
```
#### Configuración del Servidor 2

Configuración de red servidor 2 : 

```bash
debian@servidor2:~$ cat /etc/network/interfaces

auto lo
iface lo inet loopback

auto ens3
iface ens3 inet static
        address 100.0.0.2
        netmask 255.255.255.0
        gateway 100.0.0.1
        dns-nameservers 8.8.8.8

auto ens4
iface ens4 inet static
        address 192.168.1.1
        netmask 255.255.255.0
```

Ademas configuraremos el SNAT :

```bash
#Activa el bit de forwarding 
debian@servidor2:~$ sudo nano /etc/sysctl.conf 
net.ipv4.ip_forward=1 

# Regla SNAT
debian@servidor2:~$ sudo iptables -t nat -A POSTROUTING -o ens3 -s 192.168.1.0/24 -j MASQUERADE

# Te recomiendo que lo hagas permanente , configura iptables-persistent
debian@servidor2:~$ sudo apt install iptables-persistent 
```
#### Comprobación enroutamiento 
Vamos a comprobar que hemos enroutado bien nuestro escenario , para ello desde los servidores haremos un ping al contrario y ha Internet .

Desde servidor 1 :

```bash
debian@servidor1:~$ ping 8.8.8.8  -c 1
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=112 time=37.4 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 37.374/37.374/37.374/0.000 ms
debian@servidor1:~$ 

debian@servidor1:~$ ping 100.0.0.2 -c 1
PING 100.0.0.2 (100.0.0.2) 56(84) bytes of data.
64 bytes from 100.0.0.2: icmp_seq=1 ttl=63 time=18.6 ms

--- 100.0.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 18.567/18.567/18.567/0.000 ms
debian@servidor1:~$ 
```


Desde el servidor 2 :
```bash
debian@servidor2:~$ ping 90.0.0.2 -c 1
PING 90.0.0.2 (90.0.0.2) 56(84) bytes of data.
64 bytes from 90.0.0.2: icmp_seq=1 ttl=63 time=19.1 ms

--- 90.0.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 19.099/19.099/19.099/0.000 ms

debian@servidor2:~$ ping 8.8.8.8 -c 1
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=112 time=160 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 160.147/160.147/160.147/0.000 ms
debian@servidor2:~$ 
```

También comprobaremos desde los clientes ya que hay configurado un snat .

Desde el  cliente 1 :
```bash
debian@cliente1:~$ ping 100.0.0.2 -c 1
PING 100.0.0.2 (100.0.0.2) 56(84) bytes of data.
64 bytes from 100.0.0.2: icmp_seq=1 ttl=62 time=19.0 ms

--- 100.0.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 18.968/18.968/18.968/0.000 ms

debian@cliente1:~$ ping 8.8.8.8 -c 1
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=111 time=61.6 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 61.598/61.598/61.598/0.000 ms
```

Desde el  cliente 3 :
```bash
debian@cliente3:~$ ping 90.0.0.2 -c 1
PING 90.0.0.2 (90.0.0.2) 56(84) bytes of data.
64 bytes from 90.0.0.2: icmp_seq=1 ttl=62 time=15.7 ms

--- 90.0.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 15.656/15.656/15.656/0.000 ms

debian@cliente3:~$ ping 8.8.8.8 -c 1
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=111 time=45.8 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 45.760/45.760/45.760/0.000 ms
```

## Instalación de OpenVPN

Instalaremos en ambos servidores el paquete openvpn
```bash
# Servidor 1 
debian@servidor1:~$ sudo apt install -y openvpn
# Servidor 2
debian@servidor2:~$ sudo apt install -y openvpn 
```

### Generación de claves y certificados 
Podemos generar los certificados manualmente, pero existe una herramienta llamada Easy RSA que automatiza este proceso. Además, Easy RSA facilita la generación de los módulos Diffie-Hellman, que son esenciales para el funcionamiento del servidor OpenVPN. 

No es necesario que nos la descarguemos ya que esta viene con el paquete openvpn .

Para OpenVPN necesitamos crear:

- Una clave privada y un certificado x509 para la autoridad certificante que firma (CA)
- Una clave privada y un certificado x509 firmado para el servidor.
- Una clave privada y un certificado x509 firmado para cada cliente.
- Un grupo Diffie-Hellman para el servidor.

En el servidor 1, copiaremos el archivo de ejemplo de variables para evitar la solicitud repetitiva de información como organización, país, provincia, etc., por parte de EasyRSA.

```bash
debian@servidor1:/usr/share/easy-rsa$ sudo cp vars.example vars
```

Editaremos el mismo y cambiaremos los siguientes valores :

```bash
debian@servidor1:/usr/share/easy-rsa$ sudo nano vars
set_var EASYRSA_REQ_COUNTRY     "ES"
set_var EASYRSA_REQ_PROVINCE    "Sevilla"
set_var EASYRSA_REQ_CITY        "Dos Hermanas"
set_var EASYRSA_REQ_ORG         "iesgn"
set_var EASYRSA_REQ_EMAIL       "contacto@javiercd.es"
set_var EASYRSA_REQ_OU          "Informatica"
```

Una vez cambiado los valores por defecto por los nuestros , vamos a iniciar la infraestructura de clave pública (PKI) utilizando el script EasyRSA. Al ejecutar este comando, se crea un nuevo directorio PKI con la estructura necesaria para gestionar las claves y certificados. 
```bash
debian@servidor1:/usr/share/easy-rsa$ sudo ./easyrsa init-pki
* Notice:

  init-pki complete; you may now create a CA or requests.

  Your newly created PKI dir is:
  * /usr/share/easy-rsa/pki
```

#### Generación de los parámetros Diffie-Hellman

La clave de intercambio de Diffie-Hellman, es un método criptográfico que permite a dos partes acordar de forma segura una clave de sesión compartida sobre un canal no seguro. Así que vamos a generarla haciedo uso del siguiente comando : 

```bash
debian@servidor1:/usr/share/easy-rsa$ sudo  ./easyrsa gen-dh
* Notice:
Using Easy-RSA configuration from: /usr/share/easy-rsa/vars

* WARNING:

  Move your vars file to your PKI folder, where it is safe!

* Notice:
Using SSL: openssl OpenSSL 3.0.11 19 Sep 2023 (Library: OpenSSL 3.0.11 19 Sep 2023)

Generating DH parameters, 2048 bit long safe prime

.........

* Notice:

DH parameters of size 2048 created at /usr/share/easy-rsa/pki/dh.pem
```

Se nos habrá generado la clave en /usr/share/easy-rsa/pki/dh.pem , tal y como indica la salida del comando .

#### Generación del certificado de la CA

Vamos a proceder a generar el certificado de nuestra CA :

```bash
debian@servidor1:/usr/share/easy-rsa$ sudo ./easyrsa build-ca nopass
* Notice:
Using Easy-RSA configuration from: /usr/share/easy-rsa/vars

* WARNING:

  Move your vars file to your PKI folder, where it is safe!

* Notice:
Using SSL: openssl OpenSSL 3.0.11 19 Sep 2023 (Library: OpenSSL 3.0.11 19 Sep 2023)

Using configuration from /usr/share/easy-rsa/pki/52a64968/temp.25a8f31d

You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Common Name (eg: your user, host, or server name) [Easy-RSA CA]:ca.javiercd.es

* Notice:

CA creation complete and you may now import and sign cert requests.
Your new CA certificate file for publishing is at:
/usr/share/easy-rsa/pki/ca.crt
```

Se nos habrá generado en /usr/share/easy-rsa/pki/ca.crt

#### Generación del certificado del servidor 1 
Con el siguiente comando generaremos los certificados para el servidor 1 . Se generaran varios archivos :
- servidor1.req : Este archivo contiene la solicitud de certificado generada para el servidor 
- servidor1.key : Este archivo contiene la clave privada

```bash
debian@servidor1:/usr/share/easy-rsa$ sudo ./easyrsa gen-req servidor1 nopass
* Notice:
Using Easy-RSA configuration from: /usr/share/easy-rsa/vars

* WARNING:

  Move your vars file to your PKI folder, where it is safe!

* Notice:
Using SSL: openssl OpenSSL 3.0.11 19 Sep 2023 (Library: OpenSSL 3.0.11 19 Sep 2023)

....+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*..+........+...+.+......+..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+............+...+....+...+.....+...+...+......+....+.....+......+...+.+..+...+....+..+...............+......+.........+......+.......+.....+......+.+........+.+.....+......+...............+.+.....+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
....+............+..+.+...+...........+....+...........+......+...+.+...+..+.+........+....+...+.....+.......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.........+............+...+.....+....+..+...+.+...............+.....+......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*......+........+..........+...+.................+.+..+....+.....+..........+...+......+.........+.....+.+............+..+..................+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Common Name (eg: your user, host, or server name) [servidor1]:          
* Notice:

Keypair and certificate request completed. Your files are:
req: /usr/share/easy-rsa/pki/reqs/servidor1.req
key: /usr/share/easy-rsa/pki/private/servidor1.key
```

Ahora vamos a firmar  el certificado del servidor1 con la clave privada de la CA .

```bash
debian@servidor1:/usr/share/easy-rsa$ sudo ./easyrsa sign-req server servidor1
* Notice:
Using Easy-RSA configuration from: /usr/share/easy-rsa/vars

* WARNING:

  Move your vars file to your PKI folder, where it is safe!

* Notice:
Using SSL: openssl OpenSSL 3.0.11 19 Sep 2023 (Library: OpenSSL 3.0.11 19 Sep 2023)


You are about to sign the following certificate.
Please check over the details shown below for accuracy. Note that this request
has not been cryptographically verified. Please be sure it came from a trusted
source or that you have verified the request checksum with the sender.

Request subject, to be signed as a server certificate for 825 days:

subject=
    commonName                = servidor1


Type the word 'yes' to continue, or any other input to abort.
  Confirm request details: yes

Using configuration from /usr/share/easy-rsa/pki/e66a9d70/temp.40a6d9dd
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'servidor1'
Certificate is to be certified until Apr 18 16:15:16 2026 GMT (825 days)

Write out database with 1 new entries
Database updated

* Notice:
Certificate created at: /usr/share/easy-rsa/pki/issued/servidor1.crt
```

Como puedes ver tendremos los 3 ficheros referentes a nuestro servidor 1 generados :

```bash
# Certificado firmado
debian@servidor1:/usr/share/easy-rsa$ sudo ls -la pki/issued | grep servidor1
-rw------- 1 root root 4637 Jan 14 16:15 servidor1.crt

# Clave privada
debian@servidor1:/usr/share/easy-rsa$ sudo ls -la pki/private | grep servidor1
-rw------- 1 root root 1704 Jan 14 16:09 servidor1.key

# Solicitud de firma del certificado 
debian@servidor1:/usr/share/easy-rsa$ sudo ls -la pki/reqs | grep servidor1
-rw------- 1 root root  891 Jan 14 16:09 servidor1.req
```

#### Generación del certificado del servidor 2

Repetiremos el mismo proceso que hemos realizado para el servidor 1 , pero ahora para nuestro servidor 2 .

Generaremos la clave y el certificado :

```bash
debian@servidor1:/usr/share/easy-rsa$ sudo ./easyrsa gen-req servidor2 nopass
* Notice:
Using Easy-RSA configuration from: /usr/share/easy-rsa/vars

* WARNING:

  Move your vars file to your PKI folder, where it is safe!

* Notice:
Using SSL: openssl OpenSSL 3.0.11 19 Sep 2023 (Library: OpenSSL 3.0.11 19 Sep 2023)

.+.+.................+...+...+.......+..+.+...........+.+..+.+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*........+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+....+..+..........+....................+.......+.....+.......+...+..+................+..+.......+.........+...........+....+..+...+.+......+..+...+....+.....+.........+....+......+......+.........+..+...+............+...+.+...+..+....+............+...............+..+...+.............+............+.....+.......+.....+.+......+........+.....................+.+......+..+.+......+.....+.........+......+.........+.......+...+...............+.....+...............+.+....................+......+...+................+...+...+............+.....+...............+.......+......+........+......+....+......+........+.+.....+....+..+.+........+.+.....+.+.....+...........................+......+.+...+.....+......+....+..+....+......+........+.............+..+...+.........+....+..+...+....+...+...+...........+......+...................+.....+................+...+..+....+...+..+......+...+..........+..+.......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
..........+............+...+....+...+.....+...+......+.+.....+.......+..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.........+.+......+..+.+..+...+.........+............+..................+.......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+...+...........+.+...+..+....+..............+......+...............+.+......+..............+....+......+..................+...+............+..+....+.....+.......+...+.........+..+......+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Common Name (eg: your user, host, or server name) [servidor2]:
* Notice:

Keypair and certificate request completed. Your files are:
req: /usr/share/easy-rsa/pki/reqs/servidor2.req
key: /usr/share/easy-rsa/pki/private/servidor2.key
```

Fíjate que ahora a este certificado a la hora de firmarlo diremos que es de tipo cliente . Ya que el servidor 2 "actuara como un cliente":

```bash
debian@servidor1:/usr/share/easy-rsa$ sudo ./easyrsa sign-req client servidor2
* Notice:
Using Easy-RSA configuration from: /usr/share/easy-rsa/vars

* WARNING:

  Move your vars file to your PKI folder, where it is safe!

* Notice:
Using SSL: openssl OpenSSL 3.0.11 19 Sep 2023 (Library: OpenSSL 3.0.11 19 Sep 2023)


You are about to sign the following certificate.
Please check over the details shown below for accuracy. Note that this request
has not been cryptographically verified. Please be sure it came from a trusted
source or that you have verified the request checksum with the sender.

Request subject, to be signed as a client certificate for 825 days:

subject=
    commonName                = servidor2


Type the word 'yes' to continue, or any other input to abort.
  Confirm request details: yes

Using configuration from /usr/share/easy-rsa/pki/8e1b2785/temp.504078d9
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'servidor2'
Certificate is to be certified until Apr 18 16:57:49 2026 GMT (825 days)

Write out database with 1 new entries
Database updated

* Notice:
Certificate created at: /usr/share/easy-rsa/pki/issued/servidor2.crt
```

#### Generación de la clave TLS

Este paso es opcional , pero es recomendable generar una clave compartida (también conocida como clave de parámetro adicional o clave ta.key) en el contexto de OpenVPN.)

En el contexto de OpenVPN, esta clave compartida (ta.key) se utiliza para firmar y verificar todos los paquetes de datos transmitidos a través de la conexión VPN. Su propósito principal es proporcionar una capa adicional de seguridad y autenticación, ayudando a prevenir ataques como el de replay.

```bash
debian@servidor1:/usr/share/easy-rsa$ sudo openvpn --genkey --secret ta.key
```

### Distribuir las claves
Ahora tenemos que hacer llegar cada clave a su lugar correspondiente .

En el servidor 1 crearemos el directorio /etc/openvpn/keys y guardaremos los siguientes ficheros :

```bash
# Creamos el directorio donde guardaremos las claves 
debian@servidor1:/usr/share/easy-rsa$ sudo mkdir /etc/openvpn/keys

# Nos la copiamos al directorio creado
debian@servidor1:~$ sudo cp /usr/share/easy-rsa/pki/dh.pem /etc/openvpn/keys
debian@servidor1:~$ sudo cp /usr/share/easy-rsa/pki/ca.crt /etc/openvpn/keys
debian@servidor1:~$ sudo cp /usr/share/easy-rsa/pki/private/servidor1.key /etc/openvpn/keys
debian@servidor1:~$ sudo cp /usr/share/easy-rsa/pki/issued/servidor1.crt /etc/openvpn/keys
debian@servidor1:~$ sudo cp /usr/share/easy-rsa/ta.key /etc/openvpn/keys

# Comprobamos que tenemos todoos los ficheros necesarios
debian@servidor1:~$ sudo ls -l /etc/openvpn/keys
total 24
-rw------- 1 root root 1216 Jan 14 17:08 ca.crt
-rw------- 1 root root  424 Jan 14 17:08 dh.pem
-rw------- 1 root root 4637 Jan 14 17:08 servidor1.crt
-rw------- 1 root root 1704 Jan 14 17:08 servidor1.key
-rw------- 1 root root  636 Jan 14 17:08 ta.key
```

Ahora haremos lo mismo para el servidor2 , pero tendremos que llevarnos las claves haciendo uso de SCP

```bash
# Creamos el directorio donde guardaremos las claves 
debian@servidor2:~$ sudo mkdir /etc/openvpn/keys

# Desde servidor1 pasare a servidor2 las claves 

debian@servidor1:~$ sudo scp /usr/share/easy-rsa/pki/ca.crt debian@100.0.0.2:/home/debian
debian@servidor1:~$ sudo scp /usr/share/easy-rsa/ta.key debian@100.0.0.2:/home/debian
debian@servidor1:~$ sudo scp /usr/share/easy-rsa/pki/private/servidor2.key debian@100.0.0.2:/home/debian
debian@servidor1:~$ sudo scp /usr/share/easy-rsa/pki/issued/servidor2.crt debian@100.0.0.2:/home/debian

# Las movemos a /etc/openvpn/keys
debian@servidor2:~$ sudo mv * /etc/openvpn/keys

# Nos aseguramos de tener los 4 ficheros que hemos enviado :
debian@servidor2:~$ sudo ls -l /etc/openvpn/keys
total 20
-rw------- 1 debian debian 1216 Jan 14 17:12 ca.crt
-rw------- 1 debian debian 4515 Jan 14 17:14 servidor2.crt
-rw------- 1 debian debian 1704 Jan 14 17:13 servidor2.key
-rw------- 1 debian debian  636 Jan 14 17:13 ta.key
```

## Configuración de OpenVPN

### Configuración del servidor 1
> [!NOTE]
> Este apartado lo esta comparando con el post de VPN de acceso remoto.


Como ves los únicos parámetros que hemos cambiado en la configuración es la IP virtual y el parámetro route para generar la ruta hacia la red privada del otro extremo:

```bash
debian@servidor1:~$ sudo nano /etc/openvpn/servidor1.conf 
# Utilizar un dispositivo TUN dinámico
dev tun
# IP virtual
ifconfig 10.99.99.1 10.99.99.2
# Ruta para llegar a la red del otro extremo        
route 192.168.1.0 255.255.255.0
# Habilitar TLS y asumir el rol de servidor
tls-server
# Parámetros de Diffie-Hellman
dh /etc/openvpn/keys/dh.pem
# Certificado de la Autoridad Certificadora
ca /etc/openvpn/keys/ca.crt
# Certificado del servidor
cert /etc/openvpn/keys/servidor1.crt
# Clave privada del servidor
key /etc/openvpn/keys/servidor1.key
# Utilizar compresión LZO rápida
comp-lzo
# Ping al remoto cada 10 segundos y reiniciar después de 60 segundos
keepalive 10 60
# Establecer la verbosidad de salida en un rango de uso normal
verb 3
```

Reinicia el servicio OpenVPN del servidor 1 :

```bash
debian@servidor1:~$ sudo systemctl restart openvpn
```

Comprueba que se te ha generado la interfaz tun0 :

```bash
debian@servidor1:~$ ip a show tun0
9: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UNKNOWN group default qlen 500
    link/none 
    inet 10.99.99.1 peer 10.99.99.2/32 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fe80::a6be:e8ba:17e5:35e3/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
```

Y por ultimo comprueba que la ruta para llegar a la red del otro extremo es correcta , es decir que va a través de la interfaz tun0 :

```bash
debian@servidor1:~$ ip r
default via 90.0.0.1 dev ens3 onlink 
10.99.99.2 dev tun0 proto kernel scope link src 10.99.99.1 
90.0.0.0/24 dev ens3 proto kernel scope link src 90.0.0.2 
192.168.0.0/24 dev ens4 proto kernel scope link src 192.168.0.1 
192.168.1.0/24 via 10.99.99.2 dev tun0 
```


### Configuración del servidor 2

```bash
debian@servidor2:~$ sudo nano /etc/openvpn/servidor2.conf
# Utilizar un dispositivo TUN dinámico
dev tun
# Conectar al servidor
remote 90.0.0.2
# Establecer direcciones IP virtuales punto a punto
ifconfig 10.99.99.2 10.99.99.1
# Ruta para llegar a la red remota (local del servidor 1)
route 192.168.0.0 255.255.255.0
# Habilitar TLS y asumir el rol de cliente durante el handshake de TLS
tls-client
# Certificado de la Autoridad Certificadora
ca /etc/openvpn/keys/ca.crt
# Certificado del cliente
cert /etc/openvpn/keys/servidor2.crt
# Clave privada del cliente
key /etc/openvpn/keys/servidor2.key
# Utilizar compresión LZO rápida
comp-lzo
# Hacer ping al remoto cada 10 segundos y reiniciar después de 60 segundos si no hay señal de vida del >
keepalive 10 60
# Establecer la verbosidad de salida en un rango de uso normal
verb 3
# Registrar mensajes en el archivo openvpn.log
log /var/log/openvpn.log
```

Reinicia el servicio OpenVPN en el servidor 2 para que se aplique la nueva configuración : 

```bash
debian@servidor2:~$ sudo systemctl restart openvpn
```

Comprueba que se te ha generado la interfaz tun0 :

```bash
debian@servidor2:~$ ip a show tun0
10: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UNKNOWN group default qlen 500
    link/none 
    inet 10.99.99.2 peer 10.99.99.1/32 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fe80::ded7:8620:c295:146a/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
```

Y por ultimo comprueba que la ruta para llegar a la red del otro extremo es correcta , es decir que va a través de la interfaz tun0 :

```bash
debian@servidor2:~$ ip r
default via 100.0.0.1 dev ens3 onlink 
10.99.99.1 dev tun0 proto kernel scope link src 10.99.99.2 
100.0.0.0/24 dev ens3 proto kernel scope link src 100.0.0.2 
192.168.0.0/24 via 10.99.99.1 dev tun0 
192.168.1.0/24 dev ens4 proto kernel scope link src 192.168.1.1 
```

### Comprobación de funcionamiento 

Ahora, ambas redes privadas, tanto la 192.168.0.0/24 como la 192.168.1.0/24, contarán con conectividad gracias a los servidores VPN .

Ping desde cliente 1 hacia cliente 2 :

```bash
debian@cliente1:~$ ping 192.168.1.2 -c 1
PING 192.168.1.2 (192.168.1.2) 56(84) bytes of data.
64 bytes from 192.168.1.2: icmp_seq=1 ttl=62 time=15.6 ms

--- 192.168.1.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 15.645/15.645/15.645/0.000 ms
```

Ping desde cliente 2 hacia cliente 1 :

```bash
debian@cliente3:~$ ping 192.168.0.2 -c 1
PING 192.168.0.2 (192.168.0.2) 56(84) bytes of data.
64 bytes from 192.168.0.2: icmp_seq=1 ttl=62 time=17.3 ms

--- 192.168.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 17.345/17.345/17.345/0.000 ms
```

Ping desde servidor 1 hacia servidor 2 :

```bash
debian@servidor1:~$ ping 192.168.1.1 -c 1
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=18.0 ms

--- 192.168.1.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 17.988/17.988/17.988/0.000 ms
```

Ping desde servidor 1 hacia servidor 2 : 

```bash
debian@servidor2:~$ ping 192.168.0.1 -c 1
PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.
64 bytes from 192.168.0.1: icmp_seq=1 ttl=64 time=12.6 ms

--- 192.168.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 12.558/12.558/12.558/0.000 ms
```

Por supuesto también podremos acceder a cualquier servicio en la otra red o conectarnos por SSH desde un extremo del túnel a otro  :

```bash
debian@cliente3:~$ ssh 192.168.0.1
debian@192.168.0.1's password: 
Linux servidor1 6.1.0-15-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.66-1 (2023-12-09) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Jan 16 18:51:53 2024 from 192.168.1.2
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
9: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UNKNOWN group default qlen 500
    inet 10.99.99.1 peer 10.99.99.2/32 scope global tun0
       valid_lft forever preferred_lft forever
```
#### Cliente Android

> [!TIP]
> En los post de redes encontraras una guia para instalar una maquina virtual de android en KVM y GNS3

La configuración de red del mismo se realiza desde el wifi :

![](/vpn/site_to_site_openvpn/img/Pastedimage20240117195853.png)

Comprueba que desde la red local del mismo tienes conectividad con la ip asignada :

```bash
debian@cliente3:~$ ping 192.168.1.4
PING 192.168.1.4 (192.168.1.4) 56(84) bytes of data.
64 bytes from 192.168.1.4: icmp_seq=1 ttl=64 time=0.534 ms
^C
--- 192.168.1.4 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.534/0.534/0.534/0.000 ms
```

Ademas este cuenta en las aplicaciones con un emulador de terminal que nos servirá para comprobar que tiene conectividad :

![](/vpn/site_to_site_openvpn/img/Pastedimage20240117200346.png)
