---
title: "DHCP bajo debian 10"
date: 2023-09-08T10:00:00+00:00
description: Configuracion del servidor DHCP en nuestro escenario basico bajo debian 10
tags: [Servicios,NAT,SMR,DHCP,SNAT]
hero: images/servicios/dhcp_v4/isc-dhcp.webp
---
# DHCP
En este artículo aprenderás cómo configurar el servidor DHCP isc-dhcp-server. Además, configurarás una reserva y lo configuraras para que funcione en dos ámbitos.
## Instalación del servidor isc-dhcp-server
Para instalar nuestro servidor dhcp ejecutamos:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.015.png)

Nos dará el siguiente error ya que no esta configurado :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.016.png)


## Configuración del servidor isc-dhcp-server

Lo primero que tenemos que hacer es configurar el interfaz de red por el que va a trabajar el servidor dhcp, para ello editamos el siguiente fichero:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.017.png)

Y añadimos nuestra interfaz que repartirá direcciones :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.018.png)

Configura el servidor dhcp con las siguientes características:

- Rango de direcciones a repartir: 192.168.0.100 - 192.168.0.110
- Máscara de red: 255.255.255.0
- Duración de la concesión: 1 hora
- Puerta de enlace: 192.168.0.1
- Servidores DNS: 8.8.8.8

Para ello editamos el siguiente archivo :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.019.png)


Ahora añadimos lo siguiente :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.020.png)

Aquí estamos configurando nuestro ámbito conforme al enunciado .

Ahora deberemos de reiniciar el servicio con el siguiente comando :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.021.png)

## Configuraciòn de los clientes para obtener un direccionamiento dinámico

Editaremos la configuración de red para que use el dhcp :

En el debian editamos el network/interfaces:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.022.png)

Ahora reiniciamos la tarjeta de red :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.023.png)

Ahora comprobaremos si nos a asignado ip con ipconfig:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.024.png)

Vemos que se ha asignado correctamente . Repetiremos lo mismo con nuestro cliente windows .

Configuramos la tarjeta de red para que utilice el protocolo dhcp, reiniciamos la tarjeta  y comprobamos la ip que nos ha asignado :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.025.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.026.png)







Ahora vamos a comprobar las concesiones de direcciones para ello deberemos ver el siguiente archivo . Lo abriremos con cat ya que es importante no editarlo ,  puede causar problemas .

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.027.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.028.png)







## Reserva de una direccion IP
Para ello deberemos editar el archivo de configuración de nuestro servidor dhcp :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.029.png)

Una vez aquí vamos a añadir las siguientes lineas :

- Nombre de la reserva
- hardware Ethernet: Es la dirección MAC de la tarjeta de red del host.
- fixed-address: La dirección IP que le vamos a asignar.

Quedaría nuestra reserva así(la pondremos fuera de la configuración de nuestro ámbito):

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.030.png)

Ahora reiniciaremos el servicio

Vamos a comprobar que se ha realizado la concesión , para ello nos vamos a windows . Es posible que tengamos que renovar la concesión o reiniciar la tarjeta de red .

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.031.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.032.png)



Vamos a comprobar qué ocurre con la configuración de los clientes en determinadas circunstancias, para ello vamos a poner un tiempo de concesión muy bajo . Le pondré 1 min .

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.033.png)

1.Los clientes toman una configuración, y a continuación apagamos el servidor dhcp. ¿Qué ocurre con el cliente windows? ¿Y con el cliente Linux?

En windows nos asignara una dirección de APIPA

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.034.png)

Mientras que en Linux no me asigna ninguna dirección ip , aunque después me asigno una dirección de APIPA

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.035.png)





## ¿Que ocurre cuando modificamos la configuraciòn?
Los clientes toman una configuración, y a continuación cambiamos la configuración del servidor dhcp (por ejemplo, el rango). ¿Qué ocurre con el cliente windows? ¿Y con el cliente Linux?

Modificamos el rango :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.036.png)

Y reiniciamos el servicio

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.037.png)

Con windows mantengo la dirección de la reserva   :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.038.png)

Y con Linux nos asigna la dirección del nuevo rango  :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.039.png)






## Configurar dos ambitos
Realizar las modificaciones necesarias en la configuración actual de nuestro servidor dhcp para que reparta direcciones ip a dos redes diferentes, la 192.168.0.0 y la 192.168.2.0.

Lo primero que haremos sera añadir una cuarta tarjeta de red  y la configuraremos manualmente . Si no sabemos el nombre de la interfaz podemos verlo con ip a :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.040.png)

Ahora la configuraremos estática  , siguiendo el enunciado y la añadimos al /etc/default/isc-dhcp-server.

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.041.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.042.png)

Y configuramos nuestro segundo rango :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.043.png)

Ahora reiniciamos el servicio :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.044.png)


Ahora le añadiré varias tarjetas de red a mi cliente para comprobar las concesiones y configuramos las tarjetas  :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.045.png)

Y nos habría concedido dirección ip en ambos rangos :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.046.png)



