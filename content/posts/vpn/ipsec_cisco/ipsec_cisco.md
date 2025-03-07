---
title: "VPN sitio a sitio con IPsec Cisco"
date: 2024-03-28T10:00:00+00:00
description: VPN sitio a sitio con IPsec Cisco
tags: [VPN,LINUX,CISCO]
hero: /images/vpn/ipsec_cisco.png
---



En este post voy a montar una VPN IPSEC usando routers cisco .

![](/vpn/ipsec_cisco/img/Pastedimage20240128120659.png)


> [!NOTE]  
> En este post se detalla la configuración de los routers R2 y R3 , sin embargo R1 esta explicado en el post de "VPN acceso remoto OpenVPN" . Si quieres ver la configuración de este ultimo mírate el apartado preparando el escenario .

### Configuración del escenario  

Como he cambiado de escenario , hay que configurar los 2 nuevos routers en la red R2 y R3 .

Comenzare por R2 :

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

Lo mismo pero con R3 : 

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

## Configuración VPN IPSEC Cisco


Una vez tenemos configurado el escenario como en los ejercicios anteriores pero ahora todos los routers del escenario son cisco vamos a proceder con la configuración de la VPN IPSEC . Lo ideal es que compruebes que el escenario esta bien enrutado , para no hacer mas largo este documento voy a omitirlo . 


### Router 2 

A continuación te describo paso a paso la configuración que hay que realizar en R2 , haciendo uso de comentarios te indicare que estamos haciendo en cada momento : 

```bash
# Entramos en el modo de configuración
R2#conf term

# Creamos una política ISAKMP , en mi caso con un número de secuencia de 10.
R2(config)#crypto isakmp policy 10

# Establecemos el algoritmo de cifrado AES para la política ISAKMP.
R2(config-isakmp)# encryption aes

# Configuramos el algoritmo de hash SHA para la política ISAKMP.
R2(config-isakmp)# hash sha   

# Configuramos la autenticación precompartida (pre-shared key) para la política ISAKMP.
R2(config-isakmp)# authentication pre-share

# Establecemos el grupo de difie-hellman con 2048 bits para la política ISAKMP.
R2(config-isakmp)# group 14

# Configuramos la clave precompartida para autenticación con el par remoto 100.0.0.2.
R2(config-isakmp)#crypto isakmp key TuClavePrecompartida address 100.0.0.2

# Creamos un conjunto de transformación para la fase 2 (IPsec) con cifrado AES y hash SHA.
R2(config)#crypto ipsec transform-set myset esp-aes esp-sha-hmac 

# Creamos una lista de acceso (ACL) para especificar el tráfico a proteger con IPsec.
R2(cfg-crypto-trans)# access-list 100 permit ip 192.168.1.0 0.0.0.255 192.168.0.0 0.0.0.255 

# Creamos un mapa criptográfico asociado a ISAKMP e IPsec con número de secuencia 10.
R2(config)#crypto map mymap 10 ipsec-isakmp

# Especificamos la dirección IP del peer remoto.
R2(config-crypto-map)# set peer 100.0.0.2

# Asociamos el conjunto de transformación al mapa criptográfico.
R2(config-crypto-map)# set transform-set myset

# Asociamos la lista de acceso al mapa criptográfico para identificar el tráfico a proteger.
R2(config-crypto-map)# match address 100

# Entramos a la interfaz FastEthernet1/0 (PUBLICA) y le asignamos el mapa criptografico para que envie por esta el trafico de la VPN . 
R2(config-crypto-map)#interface FastEthernet1/0 
R2(config-if)# crypto map mymap
```

### Router 3

A continuación te describo paso a paso la configuración que hay que realizar en R3 , haciendo uso de comentarios te indicare que estamos haciendo en cada momento : 

```bash
# Entramos en el modo de configuración
R3#conf term

# Creamos una política ISAKMP , en mi caso con un número de secuencia de 10.
R3(config)#crypto isakmp policy 10

# Establecemos el algoritmo de cifrado AES para la política ISAKMP.
R3(config-isakmp)# encryption aes

# Configuramos el algoritmo de hash SHA para la política ISAKMP.
R3(config-isakmp)# hash sha   

# Configuramos la autenticación precompartida (pre-shared key) para la política ISAKMP.
R3(config-isakmp)# authentication pre-share

# Establecemos el grupo de difie-hellman con 2048 bits para la política ISAKMP.
R3(config-isakmp)# group 14

# Configuramos la clave precompartida para autenticación con el par remoto 100.0.0.2.
R3(config-isakmp)#crypto isakmp key TuClavePrecompartida address 90.0.0.2

# Creamos un conjunto de transformación para la fase 2 (IPsec) con cifrado AES y hash SHA.
R3(config)#crypto ipsec transform-set myset esp-aes esp-sha-hmac 

# Creamos una lista de acceso (ACL) para especificar el tráfico a proteger con IPsec.
R3(cfg-crypto-trans)#access-list 100 permit ip 192.168.1.0 0.0.0.255 192.168.0.0 0.0.0.255       

# Creamos un mapa criptográfico asociado a ISAKMP e IPsec con número de secuencia 10.
R3(config)#crypto map mymap 10 ipsec-isakmp

# Especificamos la dirección IP del peer remoto.
R3(config-crypto-map)# set peer 90.0.0.2

# Asociamos el conjunto de transformación al mapa criptográfico.
R3(config-crypto-map)# set transform-set myset

# Asociamos la lista de acceso al mapa criptográfico para identificar el tráfico a proteger.
R3(config-crypto-map)# match address 100

# Entramos a la interfaz FastEthernet1/0 (PUBLICA) y le asignamos el mapa criptografico para que envie por esta el trafico de la VPN . 
R3(config-crypto-map)#interface FastEthernet1/0
R3(config-if)# crypto map mymap
```

## Comprobaciones

Una vez aplicada la configuración vamos a ver que en ambos extremos la configuración sea correcta , viendo que los túneles estén levantados  :

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

Ya viendo esto podemos cerciorarnos de que la VPN esta levantada pero existen mas comandos que nos brindan diferente información :

- **show crypto isakmp sa : ** Para comprobar las asociaciones ISAKMP
- **show crypto ipsec sa : ** **Para comprobar las asociaciones IPsec

### Prueba de conectividad

Vamos a comprobar que los distintos clientes de la red 192.168.0.0 pueden comunicarse con los otros de la red 192.168.1.0 :

```bash
# Cliente 1 --> R3
debian@cliente1:~$ ping -c 1 192.168.1.1
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=254 time=89.2 ms

--- 192.168.1.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 89.167/89.167/89.167/0.000 ms

# Cliente1 --> Cliente 3
debian@cliente1:~$ ping -c 1 192.168.1.2
PING 192.168.1.2 (192.168.1.2) 56(84) bytes of data.
64 bytes from 192.168.1.2: icmp_seq=1 ttl=62 time=46.4 ms

--- 192.168.1.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 46.412/46.412/46.412/0.000 ms
```

Vamos a comprobar que los distintos clientes de la red 192.168.1.0 pueden comunicarse con los otros de la red 192.168.0.0 :

```bash
# Cliente 3 --> R2
debian@cliente3:~$ ping -c 1 192.168.0.1
PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.
64 bytes from 192.168.0.1: icmp_seq=1 ttl=254 time=54.4 ms

--- 192.168.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 54.440/54.440/54.440/0.000 ms

# Cliente 3 --> Cliente 1
debian@cliente3:~$ ping -c 1 192.168.0.2
PING 192.168.0.2 (192.168.0.2) 56(84) bytes of data.
64 bytes from 192.168.0.2: icmp_seq=1 ttl=62 time=33.5 ms

--- 192.168.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 33.498/33.498/33.498/0.000 ms
```

