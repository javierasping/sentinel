---
title: "VPN site to site with IPsec Cisco"
date: 2024-03-28T10:00:00+00:00
Description: VPN site to site with IPsec Cisco
tags: [VPN,LINUX,CISCO]
hero: /images/vpn/ipsec_cisco.png
---



In this post I'm going to mount an IPSEC VPN using swan routers.

![](/vpn/ipsec_cisco/img/Pastedimage20240128120659.png)


> [!NOTE]
> This post details the configuration of R2 and R3 routers, however R1 is explained in the post of "VPN OpenVPN remote access." If you want to see the configuration of the latter, look at the section preparing the stage.

## # Stage configuration

As I have changed stage, the 2 new routers have to be set up on the R2 and R3 network.

I'll start with R2:

```bash
R2(config)#interface FastEthernet0/0
R2(config-if)# ip address 192.168.0.1 255.255.255.0
R2(config-if)#no shut

R2(config)#interface FastEthernet1/0
R2(config-if)# ip address 90.0.0.2 255.255.255.0
R2(config-if)# no shutdown

R2(config)#ip route 0.0.0.0 0.0.0.0 90.0.0.1     

#SNAT
R2(config)#$ ip nat pool NAT-Pool 90.0.0.2 90.0.0.2 prefix-length 24                   
R2(config)#ip nat inside source list 1 pool NAT-Pool overload

R2(config)#interface FastEthernet0/0
R2(config-if)#ip nat inside

R2(config-if)#interface FastEthernet1/0
R2(config-if)#ip nat outside
```

The same thing but with R3:

```bash
R3(config)#Interface FastEthernet0/0
R3(config-if)#ip address 192.168.1.1 255.255.255.0
R3(config-if)#no shut
R3(config-if)#exit

R3(config)#Interface FastEthernet1/0           
R3(config-if)#ip address 100.0.0.2 255.255.255.0  
R3(config-if)#no shut                           
R3(config-if)#exit       

R3(config)#ip route 0.0.0.0 0.0.0.0 100.0.0.1

R3(config)#ip nat pool NAT-Pool 100.0.0.2 100.0.0.2 prefix-length 24      
R3(config)#ip nat inside source list 1 pool NAT-Pool overload

R3(config)#interface FastEthernet0/0
R3(config-if)#ip nat inside

R3(config-if)#interface FastEthernet1/0
R3(config-if)#ip nat outside
```

## VPN IPSEC Cisco configuration


Once we have the stage configured as in previous exercises but now all the routers of the stage are cisco we will proceed with the configuration of the IPSEC VPN. The ideal thing is for you to check that the stage is well routed, so as not to make this document longer I will omit it.


Router 2

Below I describe step by step the configuration to be done in R2, making use of comments I will indicate that we are doing at every moment:

```bash
#Entramos en el modo de configuración
R2#conf term

#Creamos una política ISAKMP , en mi caso con un número de secuencia de 10.
R2(config)#crypto isakmp policy 10

#Establecemos el algoritmo de cifrado AES para la política ISAKMP.
R2(config-isakmp)# encryption aes

#Configuramos el algoritmo de hash SHA para la política ISAKMP.
R2(config-isakmp)# hash sha   

#Configuramos la autenticación precompartida (pre-shared key) para la política ISAKMP.
R2(config-isakmp)# authentication pre-share

#Establecemos el grupo de difie-hellman con 2048 bits para la política ISAKMP.
R2(config-isakmp)# group 14

#Configuramos la clave precompartida para autenticación con el par remoto 100.0.0.2.
R2(config-isakmp)#crypto isakmp key TuClavePrecompartida address 100.0.0.2

#Creamos un conjunto de transformación para la fase 2 (IPsec) con cifrado AES y hash SHA.
R2(config)#crypto ipsec transform-set myset esp-aes esp-sha-hmac 

#Creamos una lista de acceso (ACL) para especificar el tráfico a proteger con IPsec.
R2(cfg-crypto-trans)# access-list 100 permit ip 192.168.1.0 0.0.0.255 192.168.0.0 0.0.0.255 

#Creamos un mapa criptográfico asociado a ISAKMP e IPsec con número de secuencia 10.
R2(config)#crypto map mymap 10 ipsec-isakmp

#Especificamos la dirección IP del peer remoto.
R2(config-crypto-map)# set peer 100.0.0.2

#Asociamos el conjunto de transformación al mapa criptográfico.
R2(config-crypto-map)# set transform-set myset

#Asociamos la lista de acceso al mapa criptográfico para identificar el tráfico a proteger.
R2(config-crypto-map)# match address 100

#Entramos a la interfaz FastEthernet1/0 (PUBLICA) y le asignamos el mapa criptografico para que envie por esta el trafico de la VPN .
R2(config-crypto-map)#interface FastEthernet1/0 
R2(config-if)# crypto map mymap
```

Router 3

Below I describe step by step the configuration to be done in R3, making use of comments I will indicate that we are doing at every moment:

```bash
#Entramos en el modo de configuración
R3#conf term

#Creamos una política ISAKMP , en mi caso con un número de secuencia de 10.
R3(config)#crypto isakmp policy 10

#Establecemos el algoritmo de cifrado AES para la política ISAKMP.
R3(config-isakmp)# encryption aes

#Configuramos el algoritmo de hash SHA para la política ISAKMP.
R3(config-isakmp)# hash sha   

#Configuramos la autenticación precompartida (pre-shared key) para la política ISAKMP.
R3(config-isakmp)# authentication pre-share

#Establecemos el grupo de difie-hellman con 2048 bits para la política ISAKMP.
R3(config-isakmp)# group 14

#Configuramos la clave precompartida para autenticación con el par remoto 100.0.0.2.
R3(config-isakmp)#crypto isakmp key TuClavePrecompartida address 90.0.0.2

#Creamos un conjunto de transformación para la fase 2 (IPsec) con cifrado AES y hash SHA.
R3(config)#crypto ipsec transform-set myset esp-aes esp-sha-hmac 

#Creamos una lista de acceso (ACL) para especificar el tráfico a proteger con IPsec.
R3(cfg-crypto-trans)#access-list 100 permit ip 192.168.1.0 0.0.0.255 192.168.0.0 0.0.0.255       

#Creamos un mapa criptográfico asociado a ISAKMP e IPsec con número de secuencia 10.
R3(config)#crypto map mymap 10 ipsec-isakmp

#Especificamos la dirección IP del peer remoto.
R3(config-crypto-map)# set peer 90.0.0.2

#Asociamos el conjunto de transformación al mapa criptográfico.
R3(config-crypto-map)# set transform-set myset

#Asociamos la lista de acceso al mapa criptográfico para identificar el tráfico a proteger.
R3(config-crypto-map)# match address 100

#Entramos a la interfaz FastEthernet1/0 (PUBLICA) y le asignamos el mapa criptografico para que envie por esta el trafico de la VPN .
R3(config-crypto-map)#interface FastEthernet1/0
R3(config-if)# crypto map mymap
```

## Checks

Once the configuration is applied we will see that at both ends the configuration is correct, seeing that the tunnels are up:

```bash
R3#show crypto session
Crypto session current status

Interface: FastEthernet1/0
Session status: UP-ACTIVE     
Peer: 90.0.0.2 port 500 
  IKE SA: local 100.0.0.2/500 remote 90.0.0.2/500 Active 
  IPSEC FLOW: permit ip 192.168.1.0/255.255.255.0 192.168.0.0/255.255.255.0 
        Active SAs: 2, origin: crypto map

R2#show crypto session
Crypto session current status

Interface: FastEthernet1/0
Session status: UP-ACTIVE     
Peer: 100.0.0.2 port 500 
  IKE SA: local 90.0.0.2/500 remote 100.0.0.2/500 Active 
  IPSEC FLOW: permit ip 192.168.0.0/255.255.255.0 192.168.1.0/255.255.255.0 
        Active SAs: 2, origin: crypto map
```

By seeing this we can make sure that the VPN is up but there are more commands that provide us with different information:

- * * show crypto isakmp sa: * * To check the ISAKMP associations
- * * show crypto ipsec sa: * * * * To check IPsec associations

### Connectivity test

Let's check that the different customers of the network 192.168.0.0 can communicate with the others of the network 192.168.1.0:

```bash
#Cliente 1 --> R3
debian@cliente1:~$ ping -c 1 192.168.1.1
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=254 time=89.2 ms

--- 192.168.1.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 89.167/89.167/89.167/0.000 ms

#Cliente1 --> Cliente 3
debian@cliente1:~$ ping -c 1 192.168.1.2
PING 192.168.1.2 (192.168.1.2) 56(84) bytes of data.
64 bytes from 192.168.1.2: icmp_seq=1 ttl=62 time=46.4 ms

--- 192.168.1.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 46.412/46.412/46.412/0.000 ms
```

Let's check that the different customers of the network 192.168.1.0 can communicate with the others of the network 192.168.0.0:

```bash
#Cliente 3 --> R2
debian@cliente3:~$ ping -c 1 192.168.0.1
PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.
64 bytes from 192.168.0.1: icmp_seq=1 ttl=254 time=54.4 ms

--- 192.168.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 54.440/54.440/54.440/0.000 ms

#Cliente 3 --> Cliente 1
debian@cliente3:~$ ping -c 1 192.168.0.2
PING 192.168.0.2 (192.168.0.2) 56(84) bytes of data.
64 bytes from 192.168.0.2: icmp_seq=1 ttl=62 time=33.5 ms

--- 192.168.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 33.498/33.498/33.498/0.000 ms
```

