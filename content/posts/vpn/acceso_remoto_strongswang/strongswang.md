---
title: "VPN de acceso remoto con Ipsec StrongSwan"
date: 2024-03-28T10:00:00+00:00
description: VPN de acceso remoto con Ipsec StrongSwan
tags: [VPN,LINUX,DEBIAN,STRONGSWAN]
hero: /images/vpn/strongswan.png
---




StrongSwan es una implementación de VPN (Red Privada Virtual) basada en IPsec, de código abierto, multiplataforma, completa y ampliamente utilizada. Funciona en sistemas operativos como Linux, FreeBSD, OS X, Windows, Android e iOS. Principalmente, es un demonio de intercambio de claves que admite los protocolos de Intercambio de Claves de Internet (IKEv1 e IKEv2) para establecer asociaciones de seguridad (SA) entre dos pares.

> [!NOTE]  
> Voy a partir del post de VPN acceso remoto con OpenVPN , asi que es posible que haga referencia a este durante este articulo . Si quieres tener el mismo escenario ve primero a este .

Recuerda que para la configuración que vamos a hacer tienes que activar el bit de forwarding en las maquinas Servidor1 y Servidor2 . 

![](/vpn/acceso_remoto_strongswang/img/Pastedimage20240128105821.png)


## Instalación de StrongSwan

Comenzaremos instalando el paquete StrongSwan en ambas maquinas :

```bash
debian@servidor1:~$ sudo apt install strongswan -y
debian@servidor2:~$ sudo apt install strongswan -y
```

## Configuración de StrongSwan

### Servidor 1 
A continuación configuraremos el servidor 1 , voy a ponerte un comentario para que sepas que significada cada opción :

```bash
debian@servidor1:~$  sudo cat /etc/ipsec.conf
# Configuración global de strongSwan
config setup
       charondebug="ike 2, knl 2, cfg 2, net 2, esp 2, dmn 2,  mgr 2"

# Configuración por defecto para conexiones VPN
conn %default
       ikelifetime=1h            # Tiempo de vida de la negociación de intercambio de claves y SA.
       keylife=1h                # Tiempo de vida de la llave del cifrado.
       rekeymargin=5m            # Margen de tiempo antes de la expiración para la renovación.
       keyingtries=3             # Número máximo de intentos de renegociación.
       keyexchange=ikev2         # Versión del protocolo IKE.
       authby=secret             # Uso de autenticación con clave precompartida (PSK).
       ike=aes256-sha1-modp1024  # Configuración de algoritmos para la fase IKE.
       esp=aes256-sha1           # Configuración de algoritmos para la fase ESP.

conn servidor2a1
       left=90.0.0.2              # Dirección IP publica de la maquina (servidor1).
       leftsubnet=192.168.0.0/24   # Subred privada de la maquina servidor 1.
       right=100.0.0.2             # Dirección IP publica del otro extremo (servidor2).
       rightsubnet=192.168.1.0/24  # Subred privada del otro extremo (servidor 2).
       auto=start                  # Iniciar la conexión automáticamente al arrancar strongSwan.
```

### Servidor 2 

A continuación configuraremos el servidor 2 , voy a ponerte un comentario para que sepas que significada cada opción :

```bash
debian@servidor2:~$ sudo cat /etc/ipsec.conf
# Configuración global de strongSwan
config setup
       charondebug="ike 2, knl 2, cfg 2, net 2, esp 2, dmn 2,  mgr 2"

# Configuración por defecto para conexiones VPN
conn %default
       ikelifetime=1h            # Tiempo de vida de la negociación de intercambio de claves y SA.
       keylife=1h                # Tiempo de vida de la llave del cifrado.
       rekeymargin=5m            # Margen de tiempo antes de la expiración para la renovación.
       keyingtries=3             # Número máximo de intentos de renegociación.
       keyexchange=ikev2         # Versión del protocolo IKE.
       authby=secret             # Uso de autenticación con clave precompartida (PSK).
       ike=aes256-sha1-modp1024  # Configuración de algoritmos para la fase IKE.
       esp=aes256-sha1           # Configuración de algoritmos para la fase ESP.

conn servidor2a1
       left=100.0.0.2            # Dirección IP publica de la maquina.
       leftsubnet=192.168.1.0/24  # Subred privada de la maquina.
       right=90.0.0.2            # Dirección IP publica del servidor1.
       rightsubnet=192.168.0.0/24 # Subred privada del servidor 1.
       auto=start                # Iniciar la conexión automáticamente al arrancar strongSwan.
```

### Generación de la clave compartida

Una vez que hayas configurado ambas máquinas, es necesario acordar el uso de una clave compartida denominada PSK (Pre-Shared Key). Puedes generar una PSK de manera aleatoria para mejorar la seguridad de la conexión. A continuación, te proporciono un ejemplo de cómo generar una clave aleatoria :

```bash
debian@servidor1:~$ head -c 24 /dev/urandom | base64
cXPeOAcKIVszFHp68CcGX6dLXcWcbrIl
```

Ahora en el fichero /etc/ipsec.secrets configuraremos la clave PSK , que en ambos extremos tiene que ser la misma  :

```bash
debian@servidor1:~$ sudo cat /etc/ipsec.secrets 
# Ip publica de la maquina servidor 1
90.0.0.2 : PSK "cXPeOAcKIVszFHp68CcGX6dLXcWcbrIl"

debian@servidor2:~$ sudo cat /etc/ipsec.secrets 
# Ip publica de la maquina servidor 2
100.0.0.2 : PSK "cXPeOAcKIVszFHp68CcGX6dLXcWcbrIl"
```

Una vez configurado , reiniciaremos el servicio en ambos extremos :

```bash
debian@servidor1:~$ sudo ipsec restart 
debian@servidor2:~$ sudo ipsec restart 
```

## Comprobación de funcionamiento

Ahora comprobaremos que se ha levantado el túnel en ambos extremos :

```bash
debian@servidor1:~$ sudo ipsec status
Security Associations (1 up, 0 connecting):
 servidor1a2[1]: ESTABLISHED 62 seconds ago, 90.0.0.2[90.0.0.2]...100.0.0.2[100.0.0.2]
 servidor1a2{1}:  INSTALLED, TUNNEL, reqid 1, ESP SPIs: ccb4e51d_i c186cf93_o
 servidor1a2{1}:   192.168.0.0/24 === 192.168.1.0/24

debian@servidor2:~$ sudo ipsec status
Security Associations (1 up, 0 connecting):
 servidor2a1[2]: ESTABLISHED 45 seconds ago, 100.0.0.2[100.0.0.2]...90.0.0.2[90.0.0.2]
 servidor2a1{2}:  INSTALLED, TUNNEL, reqid 1, ESP SPIs: c186cf93_i ccb4e51d_o
 servidor2a1{2}:   192.168.1.0/24 === 192.168.0.0/24
```

Es cierto que, a diferencia de OpenVPN y WireGuard, StrongSwan no crea automáticamente una interfaz virtual para la conexión VPN. En lugar de ello, utiliza las rutas del sistema operativo para dirigir el tráfico a través del túnel IPSec. 

### Tablas de enrutamiento

Podemos ver estas rutas de la siguiente manera  , estas están guardadas en la tabla 220:

```bash
debian@servidor1:~$ ip r show table 220
192.168.1.0/24 via 90.0.0.1 dev ens3 proto static src 192.168.0.1 

debian@servidor2:~$ ip route list table 220
192.168.0.0/24 via 100.0.0.1 dev ens3 proto static src 192.168.1.1 
```

### Comprobación de conectividad

Una vez hecho esto vamos a comprobar que la maquina servidor2 puede llegar a las maquinas de la red 192.168.0.0/24 :

```bash
debian@servidor2:~$ ping -c 1 192.168.0.1
PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.
64 bytes from 192.168.0.1: icmp_seq=1 ttl=64 time=12.7 ms

--- 192.168.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 12.721/12.721/12.721/0.000 ms

debian@servidor2:~$ ping -c 1 192.168.0.2
PING 192.168.0.2 (192.168.0.2) 56(84) bytes of data.
64 bytes from 192.168.0.2: icmp_seq=1 ttl=63 time=11.5 ms

--- 192.168.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 11.485/11.485/11.485/0.000 ms
```

### Estadísticas de los túneles

Si quieres ver si el trafico ha pasado por el "túnel" , puedes hacer un statusall y ver las estadísticas :  

```bash
debian@servidor1:~$ sudo ipsec statusall 
Status of IKE charon daemon (strongSwan 5.9.8, Linux 6.1.0-17-cloud-amd64, x86_64):
  uptime: 9 minutes, since Jan 28 10:44:01 2024
  malloc: sbrk 2166784, mmap 0, used 1242160, free 924624
  worker threads: 11 of 16 idle, 5/0/0/0 working, job queue: 0/0/0/0, scheduled: 2
  loaded plugins: charon test-vectors ldap pkcs11 aes rc2 sha2 sha1 md5 mgf1 random nonce x509 revocation constraints pubkey pkcs1 pkcs7 pkcs12 pgp dnskey sshkey pem openssl gcrypt pkcs8 af-alg fips-prf gmp curve25519 agent chapoly xcbc cmac hmac kdf ctr ccm gcm drbg curl attr kernel-netlink resolve socket-default connmark forecast farp stroke updown eap-identity eap-aka eap-md5 eap-gtc eap-mschapv2 eap-radius eap-tls eap-ttls eap-tnc xauth-generic xauth-eap xauth-pam tnc-tnccs dhcp lookip error-notify certexpire led addrblock unity counters
Listening IP addresses:
  90.0.0.2
  192.168.0.1
Connections:
 servidor1a2:  90.0.0.2...100.0.0.2  IKEv2
 servidor1a2:   local:  [90.0.0.2] uses pre-shared key authentication
 servidor1a2:   remote: [100.0.0.2] uses pre-shared key authentication
 servidor1a2:   child:  192.168.0.0/24 === 192.168.1.0/24 TUNNEL
Security Associations (1 up, 0 connecting):
 servidor1a2[1]: ESTABLISHED 9 minutes ago, 90.0.0.2[90.0.0.2]...100.0.0.2[100.0.0.2]
 servidor1a2[1]: IKEv2 SPIs: 80b3e1894dc769f5_i* 92c50ec8c2dedde7_r, pre-shared key reauthentication in 
43 minutes
 servidor1a2[1]: IKE proposal: AES_CBC_256/HMAC_SHA1_96/PRF_HMAC_SHA1/MODP_1024
 servidor1a2{1}:  INSTALLED, TUNNEL, reqid 1, ESP SPIs: ccb4e51d_i c186cf93_o
 servidor1a2{1}:  AES_CBC_256/HMAC_SHA1_96, 252 bytes_i (3 pkts, 358s ago), 280 bytes_o (3 pkts, 355s ag
o), rekeying in 41 minutes
 servidor1a2{1}:   192.168.0.0/24 === 192.168.1.0/24
```

### Captura con Wireshark

Ademas puedes hacer una captura del trafico y asegurarte de que los mensajes van cifrados : 

![](/vpn/acceso_remoto_strongswang/img/Pastedimage20240128112552.png)

### Comprobación con traceroute

Ademas es curioso porque si haces un traceroute el primer salto que da es a la interfaz 192.168.0.1 del servidor1 :

```bash
debian@servidor2:~$ traceroute 192.168.0.2
traceroute to 192.168.0.2 (192.168.0.2), 30 hops max, 60 byte packets
 1  192.168.0.1 (192.168.0.1)  13.695 ms  13.658 ms  13.712 ms
 2  192.168.0.2 (192.168.0.2)  13.704 ms  13.695 ms  13.678 ms
```