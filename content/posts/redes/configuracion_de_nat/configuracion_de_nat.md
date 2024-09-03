---
title: "Configuración de NAT Cisco y Linux"
date: 2023-09-08T10:00:00+00:00
description: Enrutamiento de un escenario con direcciones publicas , configuramos SNAT y DNAT en maquinas Linux y cisco .
tags: [Redes, Enrutamiento,NAT,SNAT,DNAT,Cisco,Linux]
hero: images/redes/configuracion_nat/portada.jpg
---



En este artículo, exploraremos la configuración de SNAT (Source Network Address Translation) y DNAT (Destination Network Address Translation) en escenarios con direcciones públicas, haciendo uso de routers en entornos Linux y dispositivos Cisco.

## Escenario con maquinas debian

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.001.jpeg)


### Preparación del entorno

#### Instalación de paquetes

Una vez colocadas las maquinas deberemos de descargarnos apache para los servidores web , para realizar esto conectaremos ambos servidores a un switch y este a la nube NAT para disponer de acceso a internet .

Ahora actualizaremos los repositorios haciendo un apt update :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.002.png)

A continuación ya podremos descargar los paquetes , para los servidores instalaremos apache :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.003.png)

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.004.png)

Y para el router de casa descargaremos el servidor DHCP :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.005.png)

Al acabar la instalación saltara un código de error similar a este , esto es debido a que no hay una configuración valida en el servicio :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.006.jpeg)

Por ahora ignoraremos esto y posteriormente configuraremos el servidor DHCP .

Con esto habríamos instalado todos los paquetes necesarios para instalar la practica así que podemos montar el escenario .

#### Configuración de las tarjetas de red

Nos encontraremos con un pequeño obstáculo a la hora de hacer el escenario ya que necesitamos que algunos routers tengan mas de una tarjeta de red . 

Para añadir mas de una tarjeta con el dispositivo apagado y sin estar conectado a nadie , hacemos sobre el clic derecho y pulsamos sobre  configure > network  , y seleccionamos el numero de adaptadores que necesitamos tener en cada uno , por ejemplo para el router de casa necesito tener dos adaptadores :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.007.jpeg)

Una vez hecho esto con las maquinas que necesitan mas de una tarjeta , montaremos el escenario y procederemos a configurar sus tarjetas . 

Para  modificar  la  configuración  de  las  tarjetas  de  red  lo  haremos  editando  el  fichero /etc/network/interfaces  .Para que se aplique la configuración de las tarjetas de red que hemos realizado tenemos varias opciones .

Subir y bajar la tarjeta que hemos modificado : 

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.008.png)

También podemos ahorrar tiempo y reiniciar el servicio de networking , esto funcionara para todas las tarjetas simultáneamente así que nos ahorrara tiempo :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.009.png)

Router CASA:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.010.jpeg)


Router R1:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.011.jpeg)

Router ISP:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.012.jpeg)

Router R2:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.013.jpeg)

Así seria la relación de ips que tienen las tarjetas de red de los routers . Para aplicar esta configuración a las tarjetas de red tendremos que reiniciar la misma como indico al principio de este apartado .

Para que el escenario funcione debemos activar el bit de forwarding para estos 4 routers , en este caso lo haré de forma permanente para ello editamos el fichero /etc/sysctl.conf y descomentamos esta linea :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.014.png)



#### Rutas necesarias

Para mi esquema actual las rutas que necesitamos en los routers son :

Router R1:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.015.png)

Router ISP:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.016.png)

Router R2:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.017.png)

Router CASA:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.018.png)



#### Comprobación de conectividad

Vamos a hacer ping desde cada uno de los routers a su extremos “mas lejanos” para asegurarnos de que hemos realizado correctamente el enrutamiento .

Router R1 –> R2 

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.019.png)

Router R1 –> CASA

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.020.png)

Router R2 –> R1

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.021.png)

Router R2 –> CASA

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.022.png)

Router CASA –> R1

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.023.png)

Router CASA –> R2

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.024.png)

Vemos que todos los dispositivos que tiene direcciónes ips publicas tienen conectividad entre si pero que pasa con los que tienen direcciónamiento privado en nuestro escenario , estos no tendrán conectividad ya que no se enrutan direcciónes privadas en los routers de internet .

Es decir si lanzamos un ping hacia una dirección privada que sea de otra red , por ejemplo del servidor1 al servidor2 este no llegara , ya que en las tablas de enrutamiento del router del ISP no existen rutas para direcciónes privadas .

Por lo que sera imposible alcanzar una red privada diferente a la que pertenezcamos .

Por ejemplo desde casa si le hacemos ping a google se lo hacemos a la dirección PUBLICA 8..8.8.8 no a la dirección privada que tiene el servidor , puede ser la 172.22.1.15

### Configuración del servicio DHCP en router CASA

Retomando lo que habíamos hecho anteriormente en el apartado de instalación de paquetes ya hemos descargado el servidor DHCP para debian (isc-dhcp-server). Así que ahora vamos a configurarlo . 

Lo primero que necesitamos hacer es decirle a nuestro servidor a través de que tarjeta de red queremos que este reparta direcciónes ip , en  nuestro caso es la tarjeta ens5 .

Para ello editaremos el fichero /etc/default/isc-dhcp-server y añadiremos el nombre de la tarjeta en la sección de IPV4 :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.025.jpeg)

Ahora vamos a indicarle a nuestro servidor DHCP que configuración queremos que le asigne a nuestros clientes para ello editamos el fichero  /etc/dhcp/dhcpd.conf , podemos aprovechar uno de los ejemplos que vienen comentados y aplicar nuestra configuración :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.026.png)

Este es un ejemplo muy sencillo de un servidor dhcp pero con esto es suficiente para nuestro escenario .

Los campos significan :

- subnet : dirección de red de la cual queremos repartir direcciónes ip con este servicio .
- netmask : Mascara de red de la red  la cual queremos configurar los dispositivos.
- range: Rango de direcciónes de la cual queremos repartir ips siendo la primera la inicial y la ultima la final .
- option routers: Seria la puerta de enlace de nuestra red 
- option broadcast-address : dirección de broadcast de nuestra red .

Una vez configurado con los parámetros de nuestra red reiniciaremos el servicio :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.027.png)

Y comprobaremos que el servicio esta activo :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.028.jpeg)

Ahora para que los clientes puedan recibir una dirección utilizando este servicio deberemos de configurar las tarjetas de red de PC1 y PC2 de la siguiente manera :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.029.png)

Reiniciamos el servicio para que esta se aplique y el servidor nos asigne automáticamente la configuración de red :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.030.png)

Comprobamos que efectivamente nos ha asignado la configuración de la red :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.031.jpeg)

También podemos hacer un seguimiento de a quien le hemos asignado la ip  través del servidor viendo el siguiente archivo /var/lib/dhcp/dhcpd.leases el cual guarda las concesiones que hemos realizado .

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.032.png)

Podemos ver cuando empieza así como a quien se le ha asignado viendo su dirección MAC.

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.033.jpeg)

### Configuración de NAT 

#### Router CASA

Vamos a configurar el SNAT en el router de casa viendo el esquema actual la regla para hacer esto es : 

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.034.png)

Sin embargo así se eliminaría cuando reiniciase la maquina así que en este caso voy a añadirla al /etc/network/interfaces :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.035.png)

Así podemos ver que se han aplicado después de reiniciar el servicio networking :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.036.png)

Vamos a comprobar que funciona la regla viendo si lanzo un ping a otra red (R1) si este cambia mi dirección IP :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.037.png)

Vemos que haciendo la captura este me ha cambiado la dirección privada de la maquina por la publica del router de casa por lo que la regla de SNAT estaría funcionando correctamente .

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.038.jpeg)

#### Router R2

Vamos a configurar  SNAT y  DNAT para ello añadiré las reglas al /etc/network/interfaces :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.039.png)

Reiniciamos el servicio networking y vemos si se ha aplicado :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.040.png)

Comprobaremos que funciona el SNAT haciendo ping del servidor hacia fuera a una dirección publica :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.041.png)

Vemos que esta funcionando correctamente la regla de SNAT :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.042.png)

Ya que nos ha cambiado la dirección ip privada por la publica correspondiente al router . En los apartados posteriores probare el DNAT .


#### Router R1

Para este router vamos a realizar la creación de las reglas de una forma diferente , para ella crearemos un servicio que se encargue de levantar las reglas de DNAT y SNAT cuando la maquina se reinicie para evitar añadirlas al fichero interfaces . 

Las reglas de DNAT y SNAT  para esta maquina son : 

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.043.png)

Lo primero que tendremos que hacer sera crear un script con nuestras reglas , así que las volcare con el comando iptables-save > /etc/iptables/rules.v4 para volcar las reglas existentes .

Ahora crearemos un script en en el cual restauraremos las reglas que hemos volcado y lo crearemos en la siguiente ruta /usr/local/bin/ :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.044.png)

Nos tendremos que asegurar que tiene permisos de ejecución :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.045.png)

Crearemos un archivo de servicio de Systemd , este archivo debe tener permisos de lectura y escritura solo para root, por lo que se debe ejecutar el siguiente comando como root:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.046.png)

Dentro de este añadiremos el siguiente contenido , solo tendrías que añadir la ruta donde se encuentre tu script de iptables que restaura las  reglas  :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.047.png)

Le diremos al servicio que se inicie automáticamente al reiniciar la maquina :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.048.png)

Y lo iniciamos :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.049.png)

Si queremos asegurarnos de que ha realizado su cometido correctamente miraremos el estado del servicio :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.050.png)

Veremos que las reglas se han añadido automáticamente :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.051.png)

Comprobaremos que nos ha realizado el SNAT correctamente lanzando un ping :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.052.png)

Vemos que nos ha cambiado la dirección ip privada por la publica .

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.053.png)


### Comprobación de navegación y DNAT

Ahora vamos a comprobar que desde la red de casa podemos acceder a los servidores web .

#### Cliente Debian

Desde el cliente debian podemos hacer un curl para comprobar el correcto funcionamiento del DNAT en el Router R1:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.054.jpeg)

Desde el cliente debian podemos hacer un curl para comprobar el correcto funcionamiento del DNAT en el Router R2:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.055.jpeg)

Ahora vamos a comprobar que pasa si ponemos la dirección privada de los distintos servidores web :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.056.png)

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.057.png)

Vemos que no podemos llegar a esa red ya que los routers de internet son incapaces de encaminarnos hacia esta red privada ya que puede haber miles de dispositivos con la misma ip  :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.058.png)

Tampoco recibiríamos respuesta si hiciésemos una petición web .

Si interceptamos una petición http vemos que el SNAT se realiza correctamente , cambiando la ip privada del solicitante por la publica de su router :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.059.png)


Ahora voy a interceptar una petición en la que se haga DNAT para comprobar que este se realiza correctamente :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.060.png)

Podemos ver que el origen es una dirección ip publica mientras que el destino es una dirección ip privada podemos ver que el DNAT se ha realizado correctamente .

Ahora voy a pinchar un Firefox y  volveré a comprobar que podemos acceder a los servidores web solo usando su dirección ip publica :

Server 1 :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.061.jpeg)

Server 2:


![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.062.jpeg)

Vemos que usando dirección ip publica podemos conectarnos , sin embargo no podremos usando las direcciónes ips privada de las maquinas :


Server 1 :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.063.jpeg)

Server 2 : 

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.064.jpeg)

Funciona correctamente ya que hemos conseguido que nuestros routers Linux sean capaces de hacer SNAT y DNAT pudiendo hacer que estos “utilicen” internet y puedan acceder a los recursos de otras redes .  Ya que las direcciónes privadas no se enrutan en los mismos así que si comprobamos usando estas no obtendremos ningún resultado  .


#### Depuración NAT

Para ver cuantos hits ha tenido una regla o para ver cuanta información ha “utilizado” cada regla utilizaremos el siguiente comando :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.065.jpeg)

Para borrar los contadores de todas las cadenas y  reglas usaremos iptables -Z :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.066.png)

Si nuestra cadena tiene hits la regla estará funcionando correctamente si por el contrario esta se mantiene en 0 , la regla no se esta aplicando así que tendremos que revisarla .



## Escenario con routers Cisco

Volveremos a repetir el mismo escenario que con los routers Linux pero ahora usando routers cisco 7200.

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.067.jpeg)


### Preparación del entorno

### Configuración de las tarjetas de red

Lo primeros que haremos sera añadirle los slots necesarios a nuestros routers ya que necesitamos 2 tarjetas de red en R1,R2 y CASA . Edemas de 3 para el router ISP . 

Para los primeros le añadiremos el slot PA-FE-TX , que nos añadirá una interfaz FastEthernet:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.068.png)

Mientras que para el router del ISP le añadiremos  PA-2FE-TX que nos añadirá dos interfaces de red FastEthernet.

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.069.png)


Ahora podemos arrancar los routers y comenzar con la configuración de las tarjetas de red . Usare las mismas direcciónes que en el escenario anterior .

#### Router CASA

Configuramos las tarjetas de red :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.070.png)

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.071.png)

Quedando así nuestras interfaces :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.072.png)

#### Router R1

Configuramos las tarjetas de red :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.073.png)

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.074.png)

Quedando así nuestras interfaces :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.075.png)

#### Router R2

Configuramos las tarjetas de red :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.076.png)

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.077.png)

Quedando así nuestras interfaces :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.078.png)

#### Router ISP

Configuramos las tarjetas de red :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.079.png)

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.080.png)

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.081.png)

Quedando así nuestras interfaces :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.082.png)

### Rutas necesarias

#### Rutas ISP: 

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.083.png)

#### Rutas CASA :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.084.png)

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.085.png)

#### Rutas R2:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.086.png)

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.087.png)

#### Rutas R1:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.088.png)

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.089.png)

Seria necesario únicamente que añadamos las rutas por defecto en los Routers R1 , R2 y CASA .

### Prueba de conectividad 

**R1 –> R2**

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.090.png)

**R1 –> CASA**

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.091.png)

**R2-→ R1**

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.092.png)

**R2 –> CASA**

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.093.png)

**CASA –> R1**

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.094.png)

**CASA –> R2**

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.095.png)

Vemos que todos los dispositivos que tiene direcciónes ips publicas tienen conectividad entre si pero que pasa con los que tienen direcciónamiento privado en nuestro escenario , estos no tendrán conectividad ya que no se enrutan direcciónes privadas en los routers de internet .

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.096.png)

### Configuración del servicio DHCP en router CASA

Lo primero que haremos sera establecer el rango de IP´s excluidas del conjunto (pool) de direcciónes que podrá asignar el servicio indicando la ip inicial y final del rango, ambas incluidas:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.097.png)

Ponemos un nombre al rango del servicio DHCP:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.098.png)

Definimos la red a la que dará servicio de DHCP:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.099.png)

Incluimos la puerta de enlace que ofrecerá el servicio :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.100.png)

Con esto ya estaría configurado el servidor DHCP del router de CASA , nos salimos y guardamos los  cambios  .  Ahora  encenderemos  nuestras  maquinas  y  veremos  que  están  recibirán automáticamente su configuración por DHCP , con el siguiente comando podemos ver las estadísticas del servicio :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.101.png)

Además podemos ver las concesiones con el siguiente comando :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.102.png)

Este nos sera útil para realizar un seguimiento de quien tiene asignada cada IP sin tener que ir individualmente a casa maquina .


### Configuración del NAT

#### Router CASA

Lo primero que haremos sera crear una acl para permitir el trafico que queremos hacer SNAT :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.103.png)

Le asignaremos a la interfaz interna de nuestra red esta regla :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.104.png)

Ahora crearemos un pool con las ips publicas , el comando seria este no sale completo en la terminal :

```bash
ip nat pool ip_publica 102.168.0.2 102.168.0.2 netmask 255.255.255.0 
```

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.105.png)

Activamos el NAT :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.106.png)

Indicamos que interfaz es de “dentro” :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.107.png)

Indicamos la interfaz de “fuera”:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.108.png)

El SNAT estaría funcionando , así que vamos a comprobarlo : 

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.109.png)

Vemos que nos cambia correctamente la ip privada de nuestro host por la publica del router de casa .

#### Router R1

Lo primero que haremos sera crear una acl para permitir el trafico que queremos hacer SNAT :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.110.png)

Le asignaremos a la interfaz interna de nuestra red esta regla :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.111.png)

Ahora crearemos un pool con las ips publicas , el comando seria este no sale completo en la terminal :

```bash
ip nat pool ip_publica 101.168.0.2 101.168.0.2 netmask 255.255.255.0 
```

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.112.png)

Activamos el NAT :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.113.png)

Indicamos que interfaz es de “dentro” :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.114.png)

Indicamos la interfaz de “fuera”:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.115.png)

Y comprobaremos que se esta realizando correctamente :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.116.png)

Nos cambia la ip 172.22.1.1 por la 101.168.0.2 que es la publica del router al realizar un ping , por lo que esta funcionando correctamente el SNAT.

Ahora configuraremos la regla de DNAT , la sintaxis es la siguiente : 

```bash
ip nat inside source static tcp ip_privada puerto ip_publica puerto
```

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.117.png)

*Posteriormente comprobaremos que el DNAT funciona correctamente .


#### Router R2

Lo primero que haremos sera crear una acl para permitir el trafico que queremos hacer SNAT :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.118.png)

Le asignaremos a la interfaz interna de nuestra red esta regla :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.119.png)

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.120.png)

Ahora crearemos un pool con las ips publicas , el comando seria este no sale completo en la terminal :

```bash
ip nat pool ip_publica 103.168.0.2 103.168.0.2 netmask 255.255.255.0 
```

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.121.png)

Activamos el NAT :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.122.png)

Indicamos que interfaz es de “dentro” :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.123.png)

Indicamos la interfaz de “fuera”:

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.124.png)

Y comprobaremos que se esta realizando correctamente :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.125.png)

*Nos cambia la ip 10.0.0.1 por la 103.168.0.2 que es la publica del router al realizar un ping , por lo que esta funcionando correctamente el SNAT.

Ahora configuraremos la regla de DNAT , la sintaxis es la siguiente : 

```bash
ip nat inside source static tcp ip_privada puerto ip_publica puerto
```

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.126.png)

*Posteriormente comprobaremos que el DNAT funciona correctamente .


### Comprobación de navegación y DNAT

Ahora vamos a comprobar que desde la red de casa podemos acceder a los servidores web .

Accederé usando curl desde un host de la red de casa . Primero me conectare al servidor 1 :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.127.png)

Vemos que este nos responde correctamente y se aplica el DNAT , ya que ha cambiado la ip publica del router por la privada del servidor web  :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.128.png)

Ahora comprobaremos el servidor 2 :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.129.png)

Vemos que este nos responde correctamente y se aplica el DNAT , ya que ha cambiado la ip publica del router por la privada del servidor web  :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.130.png)

Ahora comprobaremos que puedo acceder desde un Tiny Core con Firefox a ambos servidores : 

Al servidor 1 :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.131.jpeg)

Al servidor 2 :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.132.jpeg)

Vemos  que  también  podemos  conectarnos  ya  que  las  reglas  de  NAT  están  funcionando correctamente . 

Vamos a comprobar que ocurre si solicitamos la web a través de sus direcciónes ip privadas :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.133.png)

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.134.png)

Pues que obviamente no recibimos respuesta ya que en nuestro escenario estamos simulando internet y en este no se pueden enrutar direcciónes ips privadas ya que están pueden estar repetidas en infinidad de redes .

### Depuración de las reglas NAT

Además para asegurarnos de que las reglas de NAT están funcionando . 

El primer comando nos permite ver la tabla de traducciones de direcciónes DNAT :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.135.png)

Con este comando podremos ver cuantos hits tienen nuestras reglas , si no tiene ninguno es que esta no esta funcionando salvo que nosotros hayamos inicializado este :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.136.png)

Si queremos poner los contadores a cero usaremos el comando clear ip nat statistics .

Si queremos ver en tiempo real los paquetes que muestra información sobre cada paquete que traduce el router :

![](../img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.137.png)

Cuando decodifique el resultado de este comando, observe los significados de los siguientes símbolos y valores:

- **\*** : el asterisco junto a NAT indica que la traducción se realiza en la ruta de switching rápido. Al primer paquete en una conversación siempre se aplica el switching de procesos, que es más lento. Si existe una entrada de caché, el resto de los paquetes atraviesan la ruta de switching rápido.
- **S**:  Este símbolo hace referencia a la dirección IPv4 de origen.
- **a.b.c.d→ w.x.y.z**: este valor indica que la dirección de origen a.b.c.d se traduce a w.x.y.z.
- **d**: = Este símbolo hace referencia a la dirección IPv4 de destino.
- **[xxxx]** = El valor entre corchetes es el número de identificación IPv4. Esta información puede ser útil para la depuración, ya que habilita la correlación con otros seguimientos de paquetes realizados por los analizadores de protocolos.

## Bibliografía

- [Depuración NAT](https://ccnadesdecero.es/resolver-problemas-nat-cisco/)

