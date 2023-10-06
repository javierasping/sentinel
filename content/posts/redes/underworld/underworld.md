---
title: "Underworld"
date: 2023-09-08T10:00:00+00:00
description: Escenario de enrutamiento y acls en cisco
tags: [Redes, Wireshark, GNS3,Cisco,Enroutamiento,ACLS]
hero: /images/redes/underworld/portada_underwolrd.webp
---
Practica basica de enroutamiento en cisco y configuracion de ACLS en routers cusco , tenemos 4 reinos en los cuales en primer lugar queremos lograr que se comuniquen , posteriormente iremos poniendo una serie de reglas para restringir esto.


# Introducción
Vives en UNDERWORLD. En tu mundo, se presentan diferentes tipos de especies con un único fin, “cruzarse” entre sí. Estas criaturas son:

- VAMPIROS 
- LICÁNTROPOS: hombres lobo con la capacidad de regresar a su estado humano.
- HOMBRES LOBO: hombres lobo que tras su primera conversión a lobo, no pudieron regresar a su estado humano.

- HUMANOS: unos mierdecillas.
- TÚ: un guerrero informático con superpoderes como darse la vuelta a un juego que todavía no ha salido al mercado o poseer la facultad de volverse invisible cuando sale de fiesta y trata de cortejar a una fémina diciéndole frases del tipo: ¿quieres que te compile el kernel nena? 

El aspecto de UNDERWORLD es el siguiente:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.001.jpeg)

## 1.Enturar el escenario

### Tablas de enroutamiento a “papel”



|ROUTER HUMANO|||
| - | :- | :- |
|192\.168.1.0/24|0\.0.0.0|F0/0|
|192\.168.2.0/24|0\.0.0.0|F1/0|
|192\.168.3.0/24|192\.168.2.2|F1/0|
|192\.168.4.0/24|192\.168.2.2|F1/0|
|192\.168.5.0/24|192\.168.2.2|F1/0|
|192\.168.6.0/24|192\.168.2.2|F1/0|
|192\.168.7.0/24|192\.168.2.2|F1/0|
|0\.0.0.0/0|192\.168.2.2|F1/0|

------------------------------------------------


|ROUTER VAMPIROS|||
| - | :- | :- |
|192\.168.1.0/24|192\.168.2.1|F1/0|
|192\.168.2.0/24|0\.0.0.0|F1/0|
|192\.168.3.0/24|0\.0.0.0|F0/0|
|192\.168.4.0/24|0\.0.0.0|F2/0|
|192\.168.5.0/24|192\.168.4.2|F2/0|
|192\.168.6.0/24|192\.168.4.2|F2/0|
|192\.168.7.0/24|192\.168.4.2|F2/0|
|0\.0.0.0/0|192\.168.4.2|F2/0|

------------------------------------------------

|ROUTER LICÁNTROPOS|||
| - | :- | :- |
|192\.168.1.0/24|192\.168.4.1|F2/0|
|192\.168.2.0/24|192\.168.4.1|F2/0|
|192\.168.3.0/24|192\.168.4.1|F2/0|
|192\.168.4.0/24|0\.0.0.0|F2/0|
|192\.168.5.0/24|0\.0.0.0|F0/0|
|192\.168.6.0/24|0\.0.0.0|F1/0|
|192\.168.7.0/24|192\.168.6.2|F1/0|
|0\.0.0.0/0|192\.168.4.1|F1/0|

------------------------------------------------

|ROUTER HOMBRE LOBO|||
| - | :- | :- |
|192\.168.1.0/24|192\.168.6.1|F1/0|
|192\.168.2.0/24|192\.168.6.1|F1/0|
|192\.168.3.0/24|192\.168.6.1|F1/0|
|192\.168.4.0/24|192\.168.6.1|F1/0|
|192\.168.5.0/24|192\.168.6.1|F1/0|
|192\.168.6.0/24|0\.0.0.0|F1/0|
|192\.168.7.0/24|0\.0.0.0|F0/0|
|0\.0.0.0/0|192\.168.6.1|F1/0|



## 2.Configuración direcciones Ips interfaces 

### Router humanos 

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.002.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.003.png)

Guardamos la configuración :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.004.png)

### Router vampiros 

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.005.jpeg)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.006.png)

Guardamos la configuración :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.007.png)

### Router licántropos 

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.008.jpeg)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.009.png)

Guardamos la configuración :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.010.png)

### Router vampiros 

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.011.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.012.png)

Guardamos la configuración :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.013.png)



## 3. Añadiendo la tabla de enroutamiento a los routers

### Router humanos

Nos creara por defecto las rutas a las redes que estamos conectados solo necesitaremos añadir la ruta por defecto :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.014.png)

Nos quedaría la tabla de enroutamiento :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.015.png)

Guardamos la configuración :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.016.png)

### Router vampiros 

Añadiremos las siguientes rutas :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.018.png)

Así quedaría la tabla de enroutamiento :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.017.png)

Guardamos la configuración :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.019.png)


### Router licántropos

Añadimos las siguientes rutas :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.020.png)

Así quedaría nuestra tabla de enroutamiento :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.021.png)

Guardamos la configuración :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.022.png)

### Router hombres lobo

Añadimos las siguientes rutas :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.023.png)

Así quedaría nuestra tabla de enroutamiento :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.024.png)

Guardamos la configuración :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.025.png)



## 4.Prueba de enroutamiento

Para no hacer muy extenso este apartado comprobare que desde PC1 llego a todos los PCs:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.026.png)



## 5.Configuración ACLs

Todo el mundo utiliza la red para mandarse mensajitos y ligar (por lo que deberás configurar la red para que esto sea posible en un principio, es decir, que todos los equipos tengan conexión entre sí). Tú, que ya estás hasta la \*#%?! de tanto bicho raro como consecuencia de los cruces que se producen cuando un vampiro se cruza por ejemplo con un licántropo y el hijo de éstos con un hombre lobo y así sucesivamente, decides ponerle fin a la historia haciendo lo siguiente, metiéndole unas cuantas ACLs a los routers que los comunican:

1. **Los  VAMPIROS no podrán comunicarse con el resto de especies.** 

Creamos la regla para denegar el trafico de la red 192.168.3.0:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.027.png)

La aplicamos a la interfaz FastEthernet 0/0(192.168.3.1) y la aplicamos a la salida de esta :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.028.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.029.png)

Comprobaremos que los PCs de la red de Vampiros no pueden comunicarse con el resto , nos dice que hay una ACL cortándonos el paso  :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.030.jpeg)

Si desde cualquier otro reino nos comunicamos con ellos los mensajes serán capaces de llegar a ellos sin embargo la respuesta no llegaran ya que la ACL lo impide , la respuesta es cortada ya que sale de la red de los vampiros :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.031.png)

2. **Los  HOMBRES LOBO y los LICÁNTROPOS, dado que no son tan repulsivos cuando se cruzan, podrán comunicarse entre sí. Con el resto de especies no tendrán comunicación.**

Este apartado podemos darle diferentes soluciones , yo he optado por poner una ACL , en la interfaz F2/0 del router de licántropos .

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.032.jpeg)

Creamos la ACL  :

Y la aplicamos de salida de la interfaz F2/0  de salida :![ref1]![ref2]

Comprobaremos que la ACL funciona , haciendo pings entre las maquinas.

Desde PC7 vemos que no nos permite salir del router de licántropos , este nos corta la comunicación pero sin embargo podemos llegar a las demás redes :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.035.jpeg)

Desde PC5 podemos observar el mismo resultado :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.036.jpeg)

Desde PC1 vemos que no obtenemos respuesta ya que solo estamos cortando el trafico de salida impidiendo que las maquinas de “dentro”  se comuniquen con las de fuera .

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.037.png)

**HUMANOS tampoco podrán comunicarse con el resto de especies**

Con el esquema actual de ACLs no seria necesario implementar una nueva regla en ya que con el esquema actual no es posible la comunicación con ellos . Aunque los mensajes que PC1 realice lleguen a su destino este no recibirá ninguna respuesta .  

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.038.png)

Pero si aun así queremos impedir que los humanos puedan enviar mensajes a los demás desde su red implementaremos la siguiente regla en su router :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.039.png)

Ahora estamos cortando los mensajes de los humanos desde el Router 1:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.040.jpeg)

## 6.Servidor DHCP

Al final decides hacer negocio con las especies raras porque no tienen ni pajolera idea de informática y eres contratado por estos entes malignos para que lleves a cabo las siguientes tareas: 

**Hombres lobo**

Los hombres lobo que son bastante burros metiendo direcciones IP a sus máquinas, te piden que les configures el servicio DHCP para que todas sus máquinas reciban automáticamente una IP libre:

Tendremos que hacer los siguientes pasos :

1. El comando ip dhcp excluded-address 192.168.7.1 –> Señalamos las direcciones que no queremos que se repartan por DHCP , es decir las exclusiones .
1. El comando ip dhcp pool HOMBRES\_LOBO nombramos al rango de direcciones que estamos repartiendo
1. Nos meterá a la configuración del rango, ahora le decimos la red que queremos que reparta las direcciones network 192.168.7.0 255.255.255.0 
1. Ahora le indicaremos que puerta de enlace queremos que asigne default-router 192.168.7.1
1. Si quisiéramos configurar un servidor DNS , por ejemplo el de google seria así dns-server 8.8.8.8

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.041.png)

Podemos ver que el servidor DHCP esta funcionando correctamente con los parámetros que le hemos indicado anteriormente :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.042.png)

**Licántropos**

Los licántropos por su parte, te contratan para que les asignes también por DHCP sus IPs, pero te indican que no pueden recibir las primeras 10 direcciones de su rango (sin contar la de red ni la de la puerta de enlace), ya que éstas, están reservadas para los jefes de su clan que están de viaje y volverán en unos días.

Declaramos las ips que vamos a excluir :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.043.png)

Nombramos al rango de direcciones que estamos repartiendo para así poder configurarlo:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.044.png)

Le decimos la red que queremos que reparta las direcciones :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.045.png)

Ahora le indicaremos que puerta de enlace queremos que asigne :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.046.png)

Comprobaremos que el servidor dhcp esta funcionando :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.047.png)

## 7.Modificación ACLs

**Permitir ligar con las vampiros** 

De tanto hacer negocio con los vampiros, te fijas en un par de vampiritas que están de muy buen ver y  te  gustaría  poder  enviarles  mensajitos  desde  el  chalet  que  te  acabas  de  comprar  en HUMANLAND con el pastizal que les estás sacando a las pobres “criaturicas”. Tu IP es la 192.168.1.4 y la de SELENE y SONJA son la 192.168.3.4 y 192.168.3.5 respectivamente. Añade una máquina a HUMANLAND para tu equipo denominado IT KNIGHT y 2 máquinas denominadas SELENE y SONJA con las mencionadas IPs en TRANSILVANIA.

Si queremos realizar esto deberemos de configurar ACLs avanzadas para poder controlar el origen y el destino de los paquetes.

La sintaxis es bastante sencilla en este caso :

permit ip IP\_ORIGEN WILDCARD IP\_DESTINO WILDCARD Crearemos la ACL para los humanos :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.048.png)

También crearemos la ACL para los vampiros :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.049.png)

La aplicaremos a la interfaz de entrada en cada red , ambas son la FastEthernet 0/0 :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.050.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.051.png)

**\***Deberemos de haber quitado anteriormente las lista asignada a la interfaz si no dará un error , para quitarla es el mismo comando que para ponerla poniendo un no delante .

Ahora comprobaremos la efectividad de estas reglas que hemos implementado :

**IT KNIGHT –> SELENE y SONJA**

Vemos que solo nos permite el trafico hacia estos dos host específicos tal y como hemos indicado en nuestras ACLs

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.052.jpeg)

**SELENE –> IT KNIGHT**

Vemos que solo nos permite el trafico hacia estos dos host específicos tal y como hemos indicado en nuestras ACLs , si intentamos comunicarnos con otro host cortara el trafico la ACL:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.053.png)

**SONJA–> IT KNIGHT** 

Vemos que solo nos permite el trafico hacia estos dos host específicos tal y como hemos indicado en nuestras ACLs , si intentamos comunicarnos con otro host cortara el trafico la ACL:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.054.png)

También podemos ver las estadísticas de la ACL en el router fijándonos en los hits de la regla para ver si están funcionando :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.055.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.056.png)

Aunque en ninguna de las listas hemos especificado en deny any , no seria necesario ya que esta implícito , es decir por defecto al no cumplirse ninguna regla desechara el trafico .

## 8. Servidor web

Desde que no se puede ligar en UNDERWORLD, están todos más aburridos que un ajo, así que decides ponerles un servidor WEB interno a UNDERWORLD. Añade al router PUENTE 1, un servidor denominado FICHEROS que tendrá la IP 192.168.8.2/24, creando las ACLs necesarias para que la comunidad entera de UNDERWORLD, pueda entretenerse viendo algunas web chulas. 

Lo primero sera configurar la nueva interfaz del router de los HUMANOS:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.057.png)

Lo siguiente sera configurar para nuestro esquema actual en el router de VAMPIROS la ruta a la nueva red para que se route el escenario correctamente :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.058.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.059.png)

Ya por ultimo configuraremos la ip de nuestro debian de forma estática con la direccion 192.168.8.2:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.060.png)

Además le instalaremos apache (deberemos hacerlo previamente conectado a la nube NAT ) :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.061.png)

Una vez ya tenemos el servidor web preparado y enrutado en nuestro escenario , vamos a modificar las distintas ACLs para que solo puedan llegar al servidor web por el puerto 80 .

En el router de los humanos añadimos la siguiente regla , la cual permite todo el trafico hacia el host 192.168.8.2 que vaya al puerto 80:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.062.png)

Para refrescar la lista y que se apliquen los cambios deberemos de volver a asignársela al router :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.063.png)

Ahora haremos lo mismo con el router de los vampiros ya que tiene configuradas ACLs extendidas al igual que los humanos :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.064.png)

Ahora vamos a configurar una ACL avanzada para los licántropos y los hombres lobo :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.065.png)

Vamos a comprobar que NO podemos hacerle ping al servidor desde los VPCs:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.066.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.067.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.068.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.069.png)

En resumen hemos mantenido las reglas anteriores pero hemos permitido el trafico al servidor web siempre y cuando venga por el puerto 80 , por eso no podemos hacerle ping .

Vamos a comprobar que podemos acceder al servidor web desde las redes : –>HUMANOS :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.070.jpeg)

–>VAMPIROS:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.071.jpeg)


–>LICÁNTROPOS:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.072.jpeg)

–> HOMBRES LOBO :

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.073.jpeg)


[ref1]: Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.033.png
[ref2]: Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.034.png
