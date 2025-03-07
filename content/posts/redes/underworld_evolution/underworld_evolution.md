---
title: "Underworld evolution"
date: 2023-09-08T10:00:00+00:00
description: Escenario en el cual configuraremos el enrutamiento , SNAT , DNAT y cortafuegos con dispositivos Linux y Windows .
tags: [Redes, SNAT ,DNAT , Cisco , Linux]
hero: images/redes/underworld_evolution/portada.jpeg
---

El mundo de UNDERWORLD ha evolucionado mucho en los últimos meses, así que debes realizar tareas de administración de la red para afrontar la nueva situación.

Por un lado, se ha descubierto Internet en el Inframundo, de forma que cada uno de los submundos (recuerda: vampiros, licántropos, hombres lobo y humanos) se conecta a un router que, a su vez, les conecta a uno de los dos grandes routers que forman la Internet de Underworld, llamados Marcus (para humanos y vampiros) y Alexander (para hombres lobo y licántropos). Marcus y Alexander están conectados entre sí.

El esquema sería el siguiente:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.001.jpeg)

Por otro lado, los seres del inframundo han descubierto una vulnerabilidad en los routers CISCO que les permite saltarse las listas de control de acceso, volviendo al caos que lograste impedir en su día con las ACL.

Tu tarea consistirá entonces en:

1. Sustituir en la infraestructura de red los routers CISCO por máquinas Linux siguiendo el esquema de la figura.
2. Configurar adecuadamente las máquinas Linux para que funcionen como routers.
3. Crear las tablas de enrutamiento necesarias para que todas las máquinas se comuniquen con todas en principio, teniendo en cuenta que las redes internas tendrán direcciones privadas y en Internet tendremos direcciones públicas.
4. Configurar los cortafuegos necesarios en los routers para que:
- Los VAMPIROS no puedan comunicarse con el resto de especies. 
- Los HOMBRES LOBO y los LICÁNTROPOS, dado que no son tan repulsivos cuando se cruzan, podrán comunicarse entre sí. Con el resto de especies no tendrán comunicación.
- HUMANOS tampoco podrán comunicarse con el resto de especies. 
5. Configurar el servicio DHCP que tenían los hombres lobo y los licántropos en las mismas condiciones que tenían cuando se usaban routers CISCO.
6. Configurar en los cortafuegos las reglas necesarias para que, desde HUMANLAND, IT KNIGHT siga comunicándose con sus dos vampiras favoritas (SONJA Y SELENE).
7. Realiza las configuraciones necesarias para montar en HUMANLAND un servidor web accesible desde cualquier parte de UNDERWORLD.

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.002.jpeg)

## Preparación del escenario en Linux

### Configuración de las tarjetas de red

Lo primero que haremos sera añadir las tarjetas de red necesarias a cada router , para ello con la maquina apagada hacemos sobre la misma clic derecho > configuración > network y añadimos los slots que sean necesarios para cada maquina :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.003.png)

Necesitaremos el siguiente numero de tarjetas de red por cada dispositivo :

- Router 1 , 2 ,3 y 4 : Necesitaran 2 tarjetas de red 
- MARCUS y ALEXANDER  : Necesitaran 3 tarjetas de red
- PCs : Necesitaran 1 tarjeta de red 

Una vez hecho esto editaremos el fichero /etc/network/interfaces para realizar nuestra configuración de red .

Posteriormente reiniciaremos el servicio networking con systemctl restart networking.service para que se aplique la configuración de red que hemos indicado .

Configuración de la tarjeta de red Router 1 :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.004.png)

Configuración de la tarjeta de red Router 2 :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.005.png)

Configuración de la tarjeta de red Router 3 :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.006.png)

Configuración de la tarjeta de red Router 4 :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.007.png)

Configuración de la tarjeta de red Router MARCUS :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.008.png)

Configuración de la tarjeta de red Router ALEXANDER :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.009.png)

#### Activar el bit de forwarding

Si queremos hacer que una maquina Linux actué como router , es decir que enroute los paquetes que no tienen como destino esta deberemos de activar el bit de forwarding .

Además aprovecharemos para activar el bit de forwarding permanentemente en los routers del escenario para  ello editamos el fichero /etc/sysctl.conf y descomentamos esta linea :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.010.png)

Esto mismo repetiremos para los 6 routers que tenemos en el escenario : 

**Router 1:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.011.png)

**Router 2:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.012.png)

**Router 3:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.013.png)

**Router 4:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.014.png)

**Router MARCUS:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.015.png)

**Router ALEXANDER:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.016.png)

Ahora todas nuestras maquinas están configuradas para actuar como routers y encaminaran los paquetes que le lleguen y no sean para esta .

#### Configuración de rutas

Aquí te mostrare si he añadido alguna ruta manualmente y las tablas de enrutamiento de los dispositivos .

**Router MARCUS:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.017.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.018.png)

**Router ALEXANDER:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.019.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.020.png)

**Router 1:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.021.png)

**Router 2:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.022.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.023.png)

**Router 4:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.024.png)

Teniendo la configuración de red que tengo en las tarjetas solo he añadido 2 rutas manuales , en los routers de MARCUS y ALEXANDER en el resto no ha sido necesario ya que esta se genera automáticamente con la puerta de enlace que hayamos colocado al configurar las interfaces de red .

Podría haberme ahorrado escribirlas si les hubiese colocado en las interfaz que esta configurada en la red 100.X.X.X la dirección ip del otro como puerta de enlace .

#### Prueba de conectividad

Vamos a comprobar que hemos realizado el enrutamiento correctamente así que voy a lanzar un ping desde cada router a cada uno de los extremos del escenario . 

**Router 1 :**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.025.png)

**Router 2 :**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.026.png)

**Router 3:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.027.png)

**Router 4:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.028.png)

Queda comprobado que tenemos conectividad entre todos los routers , los PCS no podrán tener “conectividad” hasta que configuremos el SNAT .

### Configuración DHCP 

#### Licántropos

Los licántropos por su parte, te contratan para que les asignes también por DHCP sus IPs, pero te indican que no pueden recibir las primeras 10 direcciónes de su rango (sin contar la de red ni la de la puerta de enlace), ya que éstas, están reservadas para los jefes de su clan que están de viaje y volverán en unos días.

Con la maquina conectada a la nube NAT y la tarjeta que este conectada configurada por DHCP nos descargaremos el servidor DHCP , para esto primero deberemos de hacer un apt update ya que la maquina no trae cargados los repositorios en memoria :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.029.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.030.png)

Cuando acabe de instalarse nos dará un error , este es debido a que no esta configurado el servicio y no sabe  por que interfaz tiene que repartir direcciónes el servidor :

![ref1]

Para ello editaremos el fichero /etc/default/isc-dhcp-server y añadiremos el nombre de la tarjeta en la sección de IPV4 :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.032.png)

Ahora configuraremos el ámbito con los requisitos que nos solicitan los licántropos para ello editaremos el fichero /etc/dhcp/dhcpd.conf :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.033.png)

Tendremos que tener en cuenta que la configuración que pongamos aquí sea coherente con la configuración de red que tenemos , tenemos que tener en cuenta que tenemos una /28 así que en este caso solo podremos tener 14 direcciónes asignables . 

Pero si seguimos el enunciado las 10 primeras no las quieren por lo que solo podremos asignar 3 a nuestros clientes .

Una vez hecho esto reiniciaremos el servicio :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.034.png)

Y veremos si esta funcionando , viendo el estado :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.035.jpeg)

Le asignaremos ip a un PC para comprobar que funciona :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.036.png)

#### Hombres lobo

Los hombres lobo que son bastante burros metiendo direcciónes IP a sus máquinas, te piden que les configures el servicio DHCP para que todas sus máquinas reciban automáticamente una IP libre.

Con la maquina conectada a la nube NAT y la tarjeta que este conectada configurada por DHCP nos descargaremos el servidor DHCP , para esto primero deberemos de hacer un apt update ya que la maquina no trae cargados los repositorios en memoria :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.037.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.038.png)

Cuando acabe de instalarse nos dará un error , este es debido a que no esta configurado el servicio y no sabe  por que interfaz tiene que repartir direcciónes el servidor :

![ref1]

Para ello editaremos el fichero /etc/default/isc-dhcp-server y añadiremos el nombre de la tarjeta en la sección de IPV4 :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.039.png)


Por suerte los hombres lobo son menos exigentes y ellos quieres que se reparta su rango de direcciónes completo así que para ello editaremos el fichero /etc/dhcp/dhcpd.conf :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.040.png)

Ahora reiniciaremos el servicio :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.041.png)

Comprobaremos el estado del mismo para comprobar que este funcionando correctamente : 

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.042.jpeg)

Le asignaremos una dirección a un cliente para asegurarnos que todo funciona correctamente :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.043.png)

### Configuración  SNAT

Para acabar la fase de preparación necesitaremos de configurar SNAT para que las distintas razas puedan comunicarse entre si .

**Router 1 :**

Me he creado un archivo llamado iptables para guardar todas las reglas de la practica :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.044.png)

Para demostrar que funciona la regla , aquí vemos una captura entre el Router 1 y el PC1 :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.045.png)

Vemos que una vez fuera de la red entre R1 y MARCUS se ha aplicado SNAT :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.046.png)


**Router 2 :**

Me he creado un archivo llamado iptables para guardar todas las reglas de la practica :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.047.png)

Para demostrar que funciona la regla , aquí vemos una captura entre el Router 2 y el PC3. Vemos que el origen es una dirección ip privada :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.048.png)

Vemos que una vez fuera de la red entre R2 y MARCUS se ha aplicado SNAT , ya que el origen ahora es una dirección ip publica :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.049.png)

**Router 3 :**

Me he creado un archivo llamado iptables para guardar todas las reglas de la practica :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.050.png)

Para demostrar que funciona la regla , aquí vemos una captura entre el Router 3 y el PC5. Vemos que el origen es una dirección ip privada :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.051.png)

Vemos que una vez fuera de la red entre R3 y ALEXANDER se ha aplicado SNAT , ya que el origen ahora es una dirección ip publica :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.052.png)

**Router 4 :**

Me he creado un archivo llamado iptables para guardar todas las reglas de la practica :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.053.png)

Para demostrar que funciona la regla , aquí vemos una captura entre el Router 4 y el PC7. Vemos que el origen es una dirección ip privada :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.054.png)

Vemos que una vez fuera de la red entre R4 y ALEXANDER se ha aplicado SNAT , ya que el origen ahora es una dirección ip publica :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.055.png)

Con el escenario actual cualquier PC es capaz de llegar  a todas las direcciónes publicas de nuestra red :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.056.png)

### Configuración DNAT

Para que las maquinas puedan comunicarse entre si se les ha instalado ssh , así que tendremos que configurar el DNAT . 

**R1**

Para esta red como tenemos dos clientes le he cambiado el puerto que usa el ssh :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.057.png)

Comprobamos que puedo conectarme a ambos host desde otra red , así vemos que funciona el DNAT.

Sonja:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.058.png)

Selene:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.059.png)

**R2**

En esta red solo tenemos un cliente que queremos que se pueda acceder desde el exterior así que solo tendremos una regla de DNAT :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.060.png)

Para comprobar la regla me meteré desde los vampiros a los humanos :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.061.png)

**R3**

En esta red al haber un servicio DHCP corriendo para que la regla de DNAT funcione correctamente deberemos de hacerle una reserva a nuestro host o configurarle la tarjeta de manera estática.

Yo haré lo primero por comodidad , para ello nos dirigimos al fichero /etc/dhcp/dhcpd.conf y escribimos lo siguiente:

```BASH
host NombreDeLaReserva { hardware ethernet DIR_MAC_HOST; fixed-address IP_RESERVA;}
```

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.062.png)

Una vez hecho esto reiniciamos el servicio :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.063.png)

Y pondré la siguiente regla:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.064.png)


Ahora vamos a comprobar que me puedo conectar a este host:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.065.jpeg)

**R4**

En esta red también le configuraremos una reserva en el servidor para que nuestras reglas se mantengan activas , en este caso le asignare la dirección 192.168.4.5.

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.066.png)

Reiniciaremos el servicio y comprobamos que nuestro host tenga asignada la ip de la reserva , en caso contrario solicitaremos otra con dhclient :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.067.png)

Ahora añadiremos la regla de DNAT para que se pueda llegar al servidor ssh :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.068.png)

Comprobamos que la regla esta funcionando y podemos conectarnos desde otra red :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.069.jpeg)


### Configuración cortafuegos

#### Los Vampiros no puedan comunicarse con el resto de especies

Pondré una política por defecto DROP en la tabla FORWARD para que tire todo el trafico proveniente de la red de los vampiros :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.070.png)

Comprobaremos que los vampiros son incapaces de llegar a las demás redes :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.071.png)

Podemos ver los hits que ha realizado para ver que esta funcionando la regla :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.072.png)


#### Permitir comunicación entre Hombres Lobo y Licántropos

Los HOMBRES LOBO y los LICÁNTROPOS, dado que no son tan repulsivos cuando se cruzan, podrán comunicarse entre sí. Con el resto de especies no tendrán comunicación.

Pondré una política por defecto DROP en la tabla FORWARD y a continuación permitiré el trafico que entre por la interfaz ens4 y salga por la ens5 , y la inversa para permitir el trafico entre esta dos redes :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.073.png)

Vemos que entre ellos pueden comunicarse sin embargo no pueden acceder a los Humanos ni a los Vampiros :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.074.jpeg)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.075.jpeg)

Comprobaremos que las reglas tienen hits :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.076.png)

#### HUMANOS tampoco podrán comunicarse con el resto de especies

Con las reglas que tenemos actualmente la comunicación con otras especies por parte de los humanos no es posible, podemos ver que en R2 sin ninguna regla adicional no podemos conectarnos :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.077.png)

Vemos que no podemos comunicarnos :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.078.png)

Si queremos prohibir el trafico en nuestro router y no depender de las reglas externas en caso de que estas cambien añadiremos una política por defecto DROP :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.079.png)

Veremos los hits en la política por defecto :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.080.png)


#### Configurar  en  los  cortafuegos  las  reglas  necesarias  para  que,  desde HUMANLAND,  IT  KNIGHT  siga  comunicándose  con  sus  dos  vampiros favoritas (SONJA Y SELENE).

Las ips de estas maquinas son :

- IT KNIGHT (SSH)–>  192.168.2.3:22
- SONJA   (SSH)      –>  192.168.1.4:22    
- SELENE (SSH)     –>  192.168.1.5:2222 

En el router 1 las reglas necesarias para poder permitir esta comunicación son : 

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.081.jpeg)

En el router 2 las reglas necesarias para poder permitir esta comunicación son :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.082.jpeg)


Vamos a ir comprobando acción a acción para asegurarnos de que estas reglas realizan su cometido. 

**SELENE –> ITKNIGHT**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.083.png)

En el router 1 :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.084.jpeg)

En el router 2:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.085.jpeg)


**SONJA –> ITKNIGHT** 

Hacemos ssh :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.086.png)

Vemos los hits del router 1:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.087.jpeg)

Vemos los hits del router 2(Misma regla que el apartado anterior) :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.088.jpeg)

**ITKNIGHT –> SONJA** 

Hacemos ssh :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.089.png)

Vemos los hits del router 1 :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.090.jpeg)

Vemos los hits del router 2 :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.091.jpeg)


**ITKNIGHT –> SELENE**
 
Lanzamos el ssh :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.092.png)

Vemos los hits del router 1 :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.093.jpeg)

Vemos los hits del router 2:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.094.jpeg)

### Servidor web HUMANLAND

Realiza las configuraciones necesarias para montar en HUMANLAND un servidor web accesible desde cualquier parte de UNDERWORLD.

Le he dado a este la ip 192.168.2.10 .

Lo primero que debemos de configurar es el DNAT en el router R2(HUMALAND):

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.095.png)

Ahora en el router 2 permitiremos que se reciban peticiones al servidor y sus respuestas :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.096.png)

En el router 1 permitimos que puedan hacer peticiones y sus respuestas :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.097.png)

Para terminar en ALEXANDER permitimos que puedan atravesar peticiones web :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.098.png)

Vamos a comprobar que se pueden acceder desde todas las redes . 

**VAMPIROS :**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.099.png)

Comprobamos los hits en router 1 :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.100.png)

**HOMBRES LOBO Y LICÁNTROPOS** 

Hacemos la petición web desde ambas redes  :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.101.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.102.png)

Comprobamos los hits en router ALEXANDER :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.103.jpeg)

Por ultimo vemos los hits en el Router 2 (HUMANOS) de la regla DNAT 

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.104.png)

## Escenario con routers Cisco

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.105.jpeg)

### Configuración de las interfaces 

**R1**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.106.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.107.png)

**R2**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.108.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.109.png)

**R3**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.110.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.111.png)

**R4**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.112.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.113.png)

**MARCUS**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.114.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.115.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.116.png)

**ALEXANDER** 

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.117.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.118.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.119.png)

#### Tablas de enrutamiento

**R1**

Añadimos la ruta por defecto :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.120.png)

Así quedaría la tabla de enrutamiento de R1:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.121.png)

**R2**

Añadimos la ruta por defecto :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.122.png)

Así quedaría la tabla de enrutamiento de R2:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.123.png)

**R3**

Añadimos la ruta por defecto :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.124.png)

Así quedaría la tabla de enrutamiento de R3:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.125.png)

**R4**

Añadimos la ruta por defecto :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.126.png)

Así quedaría la tabla de enrutamiento de R4:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.127.png)

**MARCUS**

Añadimos la ruta por defecto :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.128.png)

Así quedaría la tabla de enrutamiento de MARCUS:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.129.png)

**ALEXANDER**

Añadimos la ruta por defecto :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.130.png)

Así quedaría la tabla de enrutamiento de ALEXANDER:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.131.png)



#### Prueba de conectividad

Vamos a comprobar que hemos realizado el enrutamiento correctamente así que voy a lanzar un ping desde cada router a cada uno de los extremos del escenario . 

R1 → A los extremos :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.132.png)

R2 → A los extremos :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.133.png)

R3 –> a los extremos:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.134.jpeg)

R4 –> a los extremos 

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.135.png)


### Configuración DHCP Licántropos

Los licántropos por su parte, te contratan para que les asignes también por DHCP sus IPs, pero te indican que no pueden recibir las primeras 10 direcciónes de su rango (sin contar la de red ni la de la puerta de enlace), ya que éstas, están reservadas para los jefes de su clan que están de viaje y volverán en unos días.

Lo primero que haremos sera establecer el rango de IP´s excluidas del conjunto (pool) direcciónes que podrá asignar el servicio indicando la ip inicial y final del rango, ambas incluidas:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.136.png)

Ponemos un nombre al rango del servicio DHCP:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.137.png)

Definimos la red a la que dará servicio de DHCP:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.138.png)

Incluimos la puerta de enlace que ofrecerá el servicio :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.139.png)

Con esto ya tendríamos montado el servidor DHCP , con el siguiente comando podemos ver las estadísticas del servicio para ver si este esta funcionando :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.140.png)

Comprobaremos a demás que se ha realizado la concesión a nuestro host :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.141.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.142.jpeg)

### DHCP Hombres lobo

Los hombres lobo que son bastante burros metiendo direcciónes IP a sus máquinas, te piden que les configures el servicio DHCP para que todas sus máquinas reciban automáticamente una IP libre.

En el apartado anterior detallo cada apartado de la configuración de un servidor DHCP en cisco , aquí te muestro la configuración para la red de los Hombre Lobo :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.143.png)

Comprobaremos que esta funcionando :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.144.png)

### Configuración SNAT

**Router 1:**

Lo primero que haremos sera crear una acl para permitir el trafico que queremos hacer SNAT :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.145.png)

Le asignaremos a la interfaz interna de nuestra red esta regla :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.146.png)

Ahora crearemos un pool con las ips publicas , el comando seria este no sale completo en la terminal :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.147.png)

Activamos el NAT :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.148.png)

Indicamos que interfaz es de “dentro” :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.149.png)

Indicamos la interfaz de “fuera”:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.150.png)

El SNAT estaría funcionando , así que vamos a comprobarlo : 

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.151.png)

Vemos que la regla tiene HITS:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.152.png)


**Router 2:**

Lo primero que haremos sera crear una acl para permitir el trafico que queremos hacer SNAT :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.153.png)

Le asignaremos a la interfaz interna de nuestra red esta regla :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.154.png)

Ahora crearemos un pool con las ips publicas , el comando seria este no sale completo en la terminal :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.155.png)

Activamos el NAT :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.156.png)

Indicamos que interfaz es de “dentro” :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.157.png)

Indicamos la interfaz de “fuera”:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.158.png)

El SNAT estaría funcionando , así que vamos a comprobarlo viendo si la regla tiene HITS:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.159.png)


**Router 3:**

Lo primero que haremos sera crear una acl para permitir el trafico que queremos hacer SNAT :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.160.png)

Le asignaremos a la interfaz interna de nuestra red esta regla :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.161.png)

Ahora crearemos un pool con las ips publicas , el comando seria este no sale completo en la terminal :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.162.png)

Activamos el NAT :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.163.png)

Indicamos que interfaz es de “dentro” :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.164.png)

Indicamos la interfaz de “fuera”:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.165.png)

El SNAT estaría funcionando , así que vamos a comprobarlo viendo si la regla tiene HITS:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.166.png)


**Router 4:**

Lo primero que haremos sera crear una acl para permitir el trafico que queremos hacer SNAT :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.167.png)

Le asignaremos a la interfaz interna de nuestra red esta regla :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.168.png)

Ahora crearemos un pool con las ips publicas , el comando seria este no sale completo en la terminal :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.169.png)

Activamos el NAT :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.170.png)

Indicamos que interfaz es de “dentro” :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.171.png)

Indicamos la interfaz de “fuera”:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.172.png)

El SNAT estaría funcionando , así que vamos a comprobarlo viendo si la regla tiene HITS:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.173.png)



### Configuración de DNAT 

**R1**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.174.png)

Comprobación :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.175.png)

**R2**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.176.png)

Comprobación :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.177.png)

**R3**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.178.png)

Comprobación :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.179.png)

**R4**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.180.png)

Comprobación :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.181.png)



### Configuración cortafuegos

#### Los Vampiros no puedan comunicarse con el resto de especies

Para ello vamos a borrar la regla existente que hay en la lista :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.182.png)

Ahora denegaremos el trafico saliente de la red de los vampiros :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.183.png)

Comprobamos que no pueden comunicarse :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.184.png)

Miramos los hits de las reglas :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.185.png)


#### Permitir comunicación entre Hombres Lobo y Licántropos

Los HOMBRES LOBO y los LICÁNTROPOS, dado que no son tan repulsivos cuando se cruzan, podrán comunicarse entre sí. Con el resto de especies no tendrán comunicación.

Con estas dos reglas permitimos a cualquier host de nuestra redes locales salir cuando el destino es los hombres lobos o los licántropos :

- R3-→ 180.0.0.1   
- R4 –> 190.0.0.1

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.186.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.187.png)

Vemos que nos tira los paquetes que no van desde HL a LC o de LC a HL :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.188.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.189.png)

#### HUMANOS tampoco podrán comunicarse con el resto de especies

Con las reglas que tenemos actualmente la comunicación con otras especies por parte de los humanos no es posible, podemos ver que en R2 sin ninguna regla adicional no podemos conectarnos ya que nuestros paquetes llegaran a las redes .

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.190.png)

Para que verdaderamente los humanos no puedan comunicarse sin depender de las reglas de los demos reinos  , vamos a impedir que estos salgan del reino :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.191.png)

Si lo comprobamos ahora ellos no podrán salir del reino :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.192.png)

Miramos los hits :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.193.png)

#### Configurar  en  los  cortafuegos  las  reglas  necesarias  para  que,  desde HUMANLAND,  IT  KNIGHT  siga  comunicándose  con  sus  dos  vampiros favoritas (SONJA Y SELENE).

Las ips de estas maquinas son :

- IT KNIGHT (SSH)  -–>  192.168.2.3:22
- SONJA     (SSH)  -–>  192.168.1.4:22    
- SELENE    (SSH)  -–>  192.168.1.5:2222 

Para permitir que los vampiros puedan salir a comunicarse con los humanos  :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.194.png)

Permitimos los mensajes de salida a la publica de los vampiros cuando el puerto sea el 22 y 2222:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.195.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.196.png)

Ahora  vamos a permitir que los vampiros puedan conectarse a los humanos usando el puerto 22 :

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.197.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.198.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.199.jpeg)

No se porque no funciona .. solo va si no coloco ninguna regla incluso permitiendo TODO el trafico ssh tampoco … También he permitido todo el ICMP pero nada sigue ocurriendo lo mismo . 

El nat y el SNAT están funcionando bien pero a la hora de hacer las reglas ssh pasa lo siguiente en la red local al ser mandados de vuelta el router los corta a pesar de que el trafico esta permitido 

[ref1]: /redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.031.jpeg
