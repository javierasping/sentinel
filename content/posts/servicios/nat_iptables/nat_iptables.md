---
title: "NAT con iptables"
date: 2023-09-08T10:00:00+00:00
description: Instalacion de un escenario basico y configuracion de SNAT
tags: [Servicios,NAT,SMR,IPTABLES,SNAT]
hero: images/servicios/nat_iptables/portada_iptables.jpeg
---


# NAT con iptables
En este artículo aprenderás a configurar un pequeño escenario en el cual podrás configurar una serie de servicios. Crearás el escenario descrito a continuacion , además, harás que a través de una red interna, usando un servidor Linux, tengas acceso a Internet configurando SNAT en el mismo haciendo uso de iptables.
## Instalación del entorno de pruebas
Vamos a instalar el siguiente entorno:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.001.png)

### Configuración de VirtualBox
Servidor debian :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.002.png)

Cliente windows

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.003.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.004.png)

Cliente debian

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.005.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.006.png)




### Configuración de red
Lo primero que haremos sera configurar las tarjetas de red de nuestras maquinas .

#### Servidor debian
Editamos el fichero con nano /ect/network/interfaces como superusuario y añadimos las siguientes lineas .

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.007.png)

Los cuadros rojos corresponden a la configuración de las tarjetas de red enp0s3(tarjeta externa) y enp0s8(red interna). El cuadro azul corresponde a las reglas iptables para permitir las peticiones al exterior y prohibir las interiores .

#### Cliente debian
Editamos el fichero con nano /etc/network/interfaces como superusuario y añadimos las siguientes lineas .La puerta de enlace sera la dirección ip de la tarjeta del servidor interna .

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.008.png)


#### Cliente Windows 10
En windows 10 configuramos manualmente accediendo a conexiones de red > configuracion del adaptador > ipv4 y le asignamos lo siguiente .Al igual que el cliente debian cambiando la dirección ip . He puesto dns de Google porque utilizo mi red movil .

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.009.png)





### Configuración de nat en el servidor
Modificar el fichero /etc/sysctl.conf. Hay que descomentar la línea :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.010.png)

Comprobamos si se ha aplicado

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.011.png)


### Comprobación de internet en los clientes

#### Windows 10

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.012.png)

#### Debian 11

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.013.png)
