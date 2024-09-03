---
title: "Túneles IPV6"
date: 2023-09-08T10:00:00+00:00
description: En este post detallado, exploramos el proceso de configuración de túneles IPv6 a IPv4 y viceversa en entornos Linux y Cisco. A medida que la migración hacia IPv6 gana importancia, la capacidad de establecer comunicaciones entre redes IPv4 e IPv6 se vuelve fundamental. Cubriremos los conceptos básicos de la configuración de túneles, incluyendo los tipos de túneles más comunes, como 6to4 y Teredo. Además, proporcionaremos instrucciones paso a paso para la configuración tanto en sistemas Linux como en dispositivos Cisco
tags: [Redes,IPV6,IPV4,Cisco,Linux]
hero: images/redes/tuneles_ipv6/portada.png
---



En este post detallado, exploramos el proceso de configuración de túneles IPv6 a IPv4 y viceversa en entornos Linux y Cisco. A medida que la migración hacia IPv6 gana importancia, la capacidad de establecer comunicaciones entre redes IPv4 e IPv6 se vuelve fundamental. Cubriremos los conceptos básicos de la configuración de túneles, incluyendo los tipos de túneles más comunes, como 6to4 y Teredo. Además, proporcionaremos instrucciones paso a paso para la configuración tanto en sistemas Linux como en dispositivos Cisco

<!-- ![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.001.jpeg) -->


## Túneles 6to4 en cisco

### 1.Configuraron de las interfaces de red de los Routers

**R1**

R1 –> FastEthernet 0/0  
- Llevara el prefijo de red –> 3333:db7::/64
- Enlace :FE80::C801:20FF:FE69:0  Global : 3333:DB7::C801:20FF:FE69:0

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.002.png)

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.003.png)

R1 –> FastEthernet 1/0  

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.004.png)

R1 –> FastEthernet 2/0

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.005.png)

Para los clientes del router 1 configurare SLAAC :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.006.png)


**R2**

R2 –> FastEthernet 0/0  

- Llevara el prefijo de red –> 3333:db7:1::/64
- Enlace :FE80::C802:20FF:FE79:0 Global : 3333:DB7:1:0:C802:20FF:FE79:0

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.007.png)


<!-- ![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.008.png) -->

R2–> FastEthernet 1/0  

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.009.png)

R2–> FastEthernet 2/0

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.010.png)

Para los clientes del router 2 configurare SLAAC :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.011.png)


**R3**

R3 –> FastEthernet 0/0  

- Llevara el prefijo de red –> 3333:db7:2::/64
- Enlace :FE80::C803:20FF:FE89:0 Global : 3333:DB7:2:0:C803:20FF:FE89:0

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.012.png)

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.013.png)

R3–> FastEthernet 1/0  

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.014.png)

R3–> FastEthernet 2/0

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.015.png)

Para los clientes del router 3 configurare SLAAC :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.016.png)

**\*En este escenario no es necesario que configuremos rutas IPV4 manualmente ya que con la configuración dada en las tarjetas de red el escenario estará enrodado en IPV4.**

### 2.Túneles GRE

GRE es un protocolo de tunneling de VPN de sitio a sitio básico no seguro que puede encapsular una amplia variedad de tipos de paquete de protocolo dentro de túneles IP, lo que permite que una organización entregue otros protocolos mediante una WAN basada en IP.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.017.png)

Este podrá sobre nuestro paquete IPV6 una cabecera IPV4 para que este pueda viajar por redes IPV4 . 

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.018.jpeg)

**R1 –> R3**

Crearemos una interfaz de tunnel :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.019.png)

Establecemos el modo del túnel a GRE con IP que encapsulara nuestros paquetes IPV6 dentro de IPV4:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.020.png)

Le damos una IPV4 a nuestro túnel:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.021.png)

Establecemos la dirección WAN de nuestro router , FastEthernet 1/0:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.022.png)

Establecemos la dirección WAN del extremo del túnel (R2) :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.023.png)

Habilitamos OSPF que es  un protocolo de enrutamiento dinámico :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.024.png)

Este comando agrega a la red del túnel a OSPF:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.025.png)

Le daremos una IPV6 a nuestro tunnel , con el prefijo de red 2002 a partir de la IPV4 del router 2002:0A00:0001::1/64 :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.026.png)

Creamos la ruta para llegar a la red  :

![ref1]

Crearemos una interfaz de tunnel 

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.028.png)

Establecemos el modo del túnel a GRE con IP que encapsulara nuestros paquetes IPV6 dentro de IPV4:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.029.png)

Le damos una dirección IPV4 a nuestro túnel :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.030.png)

Establecemos la dirección WAN de nuestro router , FastEthernet 1/0.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.031.png)

Establecemos la dirección WAN del extremo del túnel (R2) :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.032.png)

Habilitamos OSPF que es  un protocolo de enrutamiento dinámico . 

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.033.png)

Este comando agrega a la red del túnel a OSPF

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.034.png)

Le daremos una IPV6 a nuestro tunnel , con el prefijo de red 2002 a partir de la IPV4 del router 2002:0A00:0002::1/64 :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.035.png)

Creamos la ruta para llegar a la red  :

![ref1]

Crearemos una interfaz de tunnel 

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.036.png)

Establecemos el modo del túnel a GRE con IP que encapsulara nuestros paquetes IPV6 dentro de IPV4:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.037.png)

Le damos una direccion IPV4 a nuestro túnel :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.038.png)

Establecemos la direccion WAN de nuestro router , FastEthernet 1/0.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.039.png)

Establecemos la direccion WAN del extremo del túnel (R2) :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.040.png)

Habilitamos OSPF que es  un protocolo de enrutamiento dinámico . 

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.041.png)

Este comando agrega a la red del túnel a OSPF

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.042.png)

Le daremos una IPV6 a nuestro tunnel , con el prefijo de red 2002 a partir de la IPV4 del router 2002:1400:0001 :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.043.png)

Creamos la ruta para llegar a la red  :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.044.png)


**R3 –> R1**

Crearemos una interfaz de tunnel 

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.045.png)

Establecemos el modo del túnel a GRE con IP que encapsulara nuestros paquetes IPV6 dentro de IPV4:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.046.png)

Le damos una dirección IPV4 a nuestro túnel :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.047.png)

Establecemos la dirección WAN de nuestro router , FastEthernet 1/0.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.048.png)

Establecemos la dirección WAN del extremo del túnel (R2) :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.049.png)

Habilitamos OSPF que es  un protocolo de enrutamiento dinámico . 

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.050.png)

Este comando agrega a la red del túnel a OSPF

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.051.png)

Le daremos una IPV6 a nuestro tunnel , con el prefijo de red 2002 a partir de la IPV4 del router 2002:1400:0002::1/64 :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.052.png)

Creamos la ruta para llegar a la red  :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.053.png)


**R3 –> R2**

Crearemos una interfaz de tunnel 

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.054.png)

Establecemos el modo del túnel a GRE con IP que encapsulara nuestros paquetes IPV6 dentro de IPV4:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.055.png)

Le damos una dirección IPV4 a nuestro túnel :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.056.png)

Establecemos la dirección WAN de nuestro router , FastEthernet 1/0.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.057.png)

Establecemos la dirección WAN del extremo del túnel (R2) :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.058.png)

Habilitamos OSPF que es  un protocolo de enrutamiento dinámico . 

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.059.png)

Este comando agrega a la red del túnel a OSPF

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.060.png)

Le daremos una IPV6 a nuestro tunnel , con el prefijo de red 2002 a partir de la IPV4 del router: 

30.0.0.2 –> 2002:1e00:0002::1/64

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.061.png)

Creamos la ruta para llegar a la red  :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.062.png)


**R2–> R3**

Crearemos una interfaz de tunnel 

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.063.png)

Establecemos el modo del túnel a GRE con IP que encapsulara nuestros paquetes IPV6 dentro de IPV4:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.064.png)

Le damos una dirección IPV4 a nuestro túnel :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.065.png)

Establecemos la dirección WAN de nuestro router , FastEthernet 1/0.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.066.png)

Establecemos la dirección WAN del extremo del túnel (R2) :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.067.png)

Habilitamos OSPF que es  un protocolo de enrutamiento dinámico . 

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.068.png)

Este comando agrega a la red del túnel a OSPF

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.069.png)

Le daremos una IPV6 a nuestro tunnel , con el prefijo de red 2002 a partir de la IPV4 del router 30.0.0.1 –> 2002:1e00:0001::1/64 :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.070.png)

Creamos la ruta para llegar a la red  :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.071.png)



### 3.Comprobaciones de funcionamiento

Vamos a comprobar que se ha creado los túneles para ello introduciremos el siguiente comando en los tres routers de nuestro escenario :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.072.png)

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.073.png)

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.074.png)

Esto aparecerá una vez ambos extremos del túnel se han creado si no nos aparecerá nada . En nuestro caso podemos ver que se ha creado exitosamente los túneles .



#### Ping

Comprobaremos el funcionamiento de los túneles haciendo un ping .

- PC1-→3333:db7::e60:ddff:fea6:0 
- PC2-→ 3333:db7:1:0:e2e:3bff:fe83:0 
- PC3 –> 3333:db7:2:0:e62:5dff:fedf:0

PC1 –> PC2

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.075.png)

PC1 –> PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.076.png)

PC2 –> PC1

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.077.png)

PC2-→ PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.078.png)

PC3 –> PC1

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.079.png)

PC3→ PC2

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.080.png)

Vemos que tenemos conectividad entre todas nuestras maquinas del escenario con IPV6 aunque tengamos que atravesar redes IPV4 .

#### Traceroute

Vamos a comprobar la trayectoria que siguen los paquetes . Trayectoria que sigue un paquete PC1 a PC2  :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.081.png)

Trayectoria que sigue un paquete PC1 a PC3  :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.082.png)

Trayectoria que sigue un paquete PC2 a PC1  :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.083.png)

Trayectoria que sigue un paquete PC2 a PC3  :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.084.png)

Trayectoria que sigue un paquete PC3 a PC1  :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.085.png)

Trayectoria que sigue un paquete PC3 a PC2  :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.086.png)

### 4.Estudio de un paquete encapsulado

**Antes de pasar por el túnel** 

Paquete que viaja de PC1 a PC2.

Vemos que al no haber atravesado el túnel aun no tiene las cabeceras IPV4 , solo tiene las IPV6. Podemos ver que el origen es PC1 y el destino es PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.087.jpeg)

Veremos como en el siguiente tramo una vez atraviese el túnel el router le pondrá una cabecera IPV4 para que pueda atravesar ese tramo .

**Después de atravesar el túnel** 

Si nos fijamos en un paquete que tiene que ha atravesado un túnel podemos ver que tiene “2 niveles de red ” :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.088.png)

Si nos fijamos en el nivel de red , vemos que las IPs de origen y destino son las de los extremos del túnel . Además vemos que utiliza el protocolo 47 que significa que ha travesado un túnel GRE .

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.089.jpeg)

Ya por ultimo podemos ver en la cabecera IPV6 , que no se distingue de una que no ha atravesado un túnel . 

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.090.jpeg)

**Una vez llega a la red de destino** 

Vemos que una vez llega al destino es decir , una vez ya ha recorrido el tramo IPV4 y vuelve a entrar a la red IPV6 el router eliminara la cabecera correspondiente a IPV4 y dejara la de IPV6 para que el paquete llegue a su destino .

Vemos que la cabecera IPV6 sigue intacta , es la misma durante todo el trayecto del paquete :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.091.jpeg)

## Túneles 6to4 en Linux

<!-- ![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.092.jpeg) -->

### 1.Configuración de las interfaces de red

Voy a respetar las direcciones IPV4 del escenario con cisco .

**R1**

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.093.jpeg)

Para aplicar la configuración haremos un sudo systemctl restart networking.service  

Voy a configurar SLAAC  para configurar los clientes de nuestra red IPV6 , previamente tendremos que tener instalado el paquete radvd con sudo apt install radvd.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.094.png)

Una  configurado  el  servicio  reiniciaremos  radvd  y  nuestros  clientes  se  configuraran automáticamente con el prefijo indicado .


**R2**

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.095.jpeg)

Para aplicar la configuración haremos un sudo systemctl restart networking.service  

Voy a configurar SLAAC  para configurar los clientes de nuestra red IPV6 , previamente tendremos que tener instalado el paquete radvd con sudo apt install radvd.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.096.png)

Una  configurado  el  servicio  reiniciaremos  radvd  y  nuestros  clientes  se  configuraran automáticamente con el prefijo indicado .


**R3**

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.097.jpeg)

Para aplicar la configuración haremos un sudo systemctl restart networking.service  

Voy a configurar SLAAC  para configurar los clientes de nuestra red IPV6 , previamente tendremos que tener instalado el paquete radvd con sudo apt install radvd.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.098.png)

Una  configurado  el  servicio  reiniciaremos  radvd  y  nuestros  clientes  se  configuraran automáticamente con el prefijo indicado .

**En este escenario no es necesario que configuremos rutas IPV4 manualmente ya que con la configuración dada en las tarjetas de red el escenario estará enrodado en IPV4.**

Sin embargo sera necesario para todos los routers que habilitemos el bit de forwarding tanto para IPV4 como para IPV6.

Para ello editamos el fichero sudo nano /etc/sysctl.conf  y descomentamos las siguientes lineas :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.099.jpeg)

Esto mismo lo repetiremos para los cada uno de nuestros routers y reiniciaremos para que se apliquen los cambios .

### 2.Configuración de los túneles SIT

El funcionamiento es similar a los túneles GRE en cisco este cojera nuestros paquetes  y a través de una interfaz tipo túnel le añadirá una cabecera IPV4 para que pueda atravesar redes IPV4 .

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.100.png)

Una vez el túnel este levantado le diremos al router que para llegar al prefijo de la red X tendrá que utilizar este para que le añada la cabecera a nuestros paquetes .

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.101.png)

Para mayor comodidad he creado un pequeño script en cada router con los comandos necesarios para que el tunnel funcione .

Consta de 4 comandos :

1. Creara la interfaz de tunnel con el destino y a continuación el origen de este .
2. Levantara la tarjeta de red
3. Le asignara la IPV6 al túnel a partir de la dirección IPV4 de origen del mismo .
4. Crearemos la ruta del trafico que utilizara el tunnel .

Podemos ponerle al túnel el nombre que deseemos en mi caso he puesto tunnel seguido de un numero para poder identificarlos 


**Túneles de R2**

Así quedaría el “script” de los túneles de R2

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.102.png)

Una vez creado el script le daremos permiso y lo ejecutaremos :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.103.png)

Comprobaremos que las interfaces se han creado correctamente :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.104.jpeg)

![ref2]

Una vez creado el script le daremos permiso y lo ejecutaremos :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.106.png)

Comprobaremos que las interfaces se han creado correctamente :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.107.jpeg)


**Túneles de R3**

Así quedaría el “script” de los túneles de R3

![ref2]

Una vez creado el script le daremos permiso y lo ejecutaremos :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.108.png)

Comprobaremos que las interfaces se han creado correctamente :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.109.jpeg)



### 3.Comprobación de funcionamiento

PC1 –> 3333:db7::e47:bfff:fe86:0 PC2 –> 2222:db7::ebc:f6ff:fe7d:0 PC3 –> 4444:db7::e43:78ff:fec6:0

#### Ping

PC1 –> PC2

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.110.png)

PC1 –> PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.111.png)

PC2 –> PC1

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.112.png)

PC2 –> PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.113.png)


PC3 –> PC1

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.114.png)

PC3 –> PC2

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.115.png)

#### Traceroute

Una vez que hemos comprobado que tenemos conectividad vamos a ver si los paquetes utilizan los túneles .

PC1 –> PC2

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.116.png)

PC1 –> PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.117.png)


PC2 –> PC1

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.118.png)

PC2 –> PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.119.png)

PC3 –> PC1

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.120.png)

PC3 –> PC2

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.121.png)

### 4.Estudio de un paquete encapsulado

**Antes de pasar por el túnel** 

Paquete que viaja de PC1 a PC2.

Vemos que al no haber atravesado el túnel aun no tiene las cabeceras IPV4 , solo tiene las IPV6. Podemos ver que el origen es PC1 y el destino es PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.122.jpeg)

Veremos como en el siguiente tramo una vez atraviese el túnel el router le pondrá una cabecera IPV4 para que pueda atravesar ese tramo .

**Después de atravesar el túnel** 

Si nos fijamos en un paquete que tiene que ha atravesado un túnel podemos ver que tiene “2 niveles de red ” .

Si nos fijamos en el nivel de red , vemos que las IPs de origen y destino son las de los extremos del túnel . Además vemos que utiliza el protocolo 47 que significa que ha travesado un túnel GRE .

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.123.jpeg)


Ya por ultimo podemos ver en la cabecera IPV6 , que no se distingue de una que no ha atravesado un túnel . 

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.124.jpeg)

**Una vez llega a la red de destino** 

Vemos que una vez llega al destino es decir , una vez ya ha recorrido el tramo IPV4 y vuelve a entrar a la red IPV6 el router eliminara la cabecera correspondiente a IPV4 y dejara la de IPV6 para que el paquete llegue a su destino .

Vemos que la cabecera IPV6 sigue intacta , es la misma durante todo el trayecto del paquete :

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.125.jpeg)

## Bibliografía

- [Túneles automáticos 6to4 ](https://community.cisco.com/t5/blogs-general/t%C3%BAneles-autom%C3%A1ticos-6to4/ba-p/4822594)
- [Túneles Automáticos Para Ipv6 ](https://educacionadistancia.juntadeandalucia.es/centros/sevilla/pluginfile.php/347162/mod_resource/content/1/52470-Tuneles%20Automaticos%20para%20IPv6\(1\).pdf)
- [Túneles GRE](https://ccnadesdecero.es/tuneles-gre-caracteristicas-y-configuracion/)
- [Túneles SIT 6to4 Linux](https://juncotic.com/tunel-ipv6-montando-tunel-ipv6/) 


[ref1]: ../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.027.png
[ref2]: ../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.105.png
