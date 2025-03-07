---
title: "Escenario IPv6 Básico"
date: 2023-10-08T10:00:00+00:00
description: Escenario básico en el cual aprenderemos lo básico sobre el protocolo IPV6
tags: [Redes, Enrutamiento, IPV6]
hero: images/redes/escenario_ipv6_basico/portada.png
---


A lo largo de esta guía, exploraremos la configuración de un escenario básico utilizando redes IPv6 tanto en sistemas Linux como en dispositivos Cisco. Además, abordaremos la configuración de un servidor Apache aprovechando las capacidades de IPv6.

## Linux Autoconfiguración IPV6

Conecta dos máquinas Linux al mismo switch y comprueba que tienen conectividad con IPv6 usando la dirección de enlace local.

Comprobaremos las IPV6 que tienen los distintos pcs . El PC1 tiene –> fe80::ef7:42ff:fe92:0/64

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.001.png)

Mientras que el PC2 tiene –> fe80::e5f:61ff:feee:0/64

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.002.png)

Estas dos direcciones se denominan de enlace local y se asignan automáticamente a cada interfaz de red . Este tipo solo nos permitirá comunicarnos con los dispositivos de nuestra red local y tienen el prefijo –> FE80::/10 

Si hacemos un ping desde uno de estos a otros con la dirección de enlace local podremos comunicarnos :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.003.png)

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.004.png)

### SLAAC

Añade a la misma red una tercera máquina Linux y configúrala como router de forma que dé direcciones IPv6 globales a las otras dos usando SLAAC. No olvides instalar RADVD. Comprueba que tienen conectividad.

Lo primero que haremos sera configurar la interfaz de red por ipv6 de nuestro router en este caso le asignare el prefijo 3333:db7::

Calculamos la parte fija de nuestra dirección :

R1  –>  0c:01:30:a0:00:00  –> 0c:01:30:ff:fe:a0:00:00 –>  0E:01:30:FF:FE:A0:00:00

Editamos el interfaces y aplicamos la configuración de nuestra tarjeta de red :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.005.png)

Reiniciamos al servicio y tendríamos una direccion global :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.006.png)

SLAAC(Stateless Address Autoconfiuration) es un mecanismo de configuración único para IPV6 no existe un equivalente en IPV4. El cual nos permite  que  los nodos de nuestra red se configuren automáticamente .

A partir de la dirección de enlace local que tienen todos los host , mediante el protocolo neighbour discovery solicita si hay algún router dentro de la red local le facilite los parámetros de configuración de la red  

Lo primero que haremos para configurar SLAAC sera instalar el paquete radvd :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.007.png)

Si miramos el estado del demonio este nos dirá que no encuentra su fichero de configuración :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.008.png)

Así que le generaremos uno indicándole la interfaz que va a repartir direcciones y además le diremos el comportamiento que tendrá en nuestra red  :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.009.png)

- **MinRtrAdvInterval :** Indica el tiempo mínimo en segundos por el cual el router mandara un mensaje en segundos .
- **MaxRtrAdvInterval:** Indica el tiempo máximo en segundo por el cual el router mandara un mensaje .

- **AdvSendAdvert:** Indica si por la interfaz se mandaran avisos o no .
- **AdvManagedFlag:** Indica si queremos que el servicio utilice  DHCPv6(on) o no (off) .
- **Prefix:** Indica el prefijo de red que usara SLAAC para asignar direcciones .
- **AdvValidLifetime:** Indica el tiempo en segundos que una dirección IPV6 sera valida.
- **AdvPreferredLifetime:** Indica el tiempo en segundos que una dirección generada a partir del prefijo sera preferida en lugar de otras direcciones .



Una vez hecho esto reiniciamos el servicio y el demonio comenzara a configurar a nuestros clientes :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.010.jpeg)

Además deberemos de configurar el bit de forwarding para ipv6 en nuestro router , al igual que con ipv4 editamos el archivo /etc/sysctl.conf :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.011.png)

#### Mensajes de SLAAC

Podemos ver como se ha configurado el PC1 usando SLAAC :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.012.jpeg)

También el PC2 se ha configurado :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.013.jpeg)

Vamos a estudiar los mensajes que han intervenido en esta configuración de SLAAC , si los numeramos como en esta captura de Wireshark :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.014.png)

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.015.png)

- **Router solicitation** (RS) (No aparece en la captura) : El PC le envía un mensaje de RS a todos los routers para indicar que necesita un RA , este mensaje se envía si no recibe ningún RA pasado un tiempo.
- **Router Advertisement** (RA): Una vez el router recibe el RS o periódicamente envía un RA en el cual se incluye el prefijo de la red y su longitud . El mensaje RA se envía a la dirección IPv6 de multidifusión de todos los nodos, FF02::1, con la dirección link-local del router como la dirección IPv6 de origen. (N0 6 y 12).
- **Multicast Listener Report Message v2**:Indica que el dispositivo x ha iniciado una sesión de escucha para trafico multicast (No 7 y 9).
- **Neighbor Solicitation** (NS): Se utiliza para conocer la dirección MAC de un dispositivo de tu red , es similar al protocolo ARP .(No 10,11,613).
- **Neighbor Advertisement** (NA) : Es el mensaje de respuesta de un NS (No 614).

Una vez que el cliente a recibido un RA , este procede a configurar su dirección IPV6 , con un prefijo de red de 64 bits pero necesita una IID(Interface Identifier) .

Hay dos maneras en las que los clientes pueden crear su propia IID única:

- **EUI-64:** mediante el proceso EUI-64, la PC1 crea una IID utilizando su dirección MAC de 48 bits.
- **De generación aleatoria:** la IID de 64 bits puede ser un número aleatorio generado por el sistema operativo cliente.

Dado que SLAAC es un proceso sin estado, para que los clientes pueda utilizar esta dirección IPv6 creada recientemente, debe verificar que sea única. El cliente  enviara un NS  con su propia dirección como la dirección IPv6 de destino. Si ningún otro dispositivo responde con un mensaje de anuncio de vecino, la dirección es única y puede ser utilizada por el cliente. Si este recibe un NA, la dirección no es única, y el sistema operativo debe determinar una nueva ID de interfaz para utilizar.

Este proceso forma parte de la detección de vecinos ICMPv6 y se conoce como “detección de direcciones duplicadas (DAD)”.

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.016.png)

Esta imagen explica la configuración de una interfaz por SLAAC. Ahora vamos a comprobar que los distintos clientes tienen conectividad entre si : 

PC1  –> 3333:db7::ef7:42ff:fe92:0
PC2 –> 3333:db7::e5f:61ff:feee:0   
R1  –> 3333:db7::e01:30ff:fea0:0

Router 1 :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.017.png)

PC2:

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.018.png)

Tenemos que tener en cuenta que estas “concesiones” de direcciones no se almacenan en ningún sitio , es decir en el servidor no almacenamos las configuraciones que ha realizado el servicio .

#### DHCPv6 con SLAAC

Cambia la configuración para que utilice DHCPv6 en vez de SLAAC enviando también los servidores DNS. Comprueba que las máquinas tienen conectividad.

Para ello nos instalamos el servidor DHCPv6 , el paquete es el mismo para ipv4 :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.019.png)

Editamos el fichero de configuración para IPV6 –> sudo nano /etc/dhcp/dhcpd6.conf:

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.020.png)

En el fichero /etc/default/isc-dhcp-server  indicaremos no solo la interfaz que queremos repartir direcciones si no también especificaremos que el servidor funcionara por IPV6 :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.021.jpeg)

Reiniciamos el servicio y comprobamos que esta funcionando con los parámetros que le hemos asignado en la configuraron :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.022.jpeg)

Vamos a comprobar que los clientes se configuraran usando ipv6 , para ello la configuración en el network interfaces es bastante similar a IPV4 :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.023.png)

Reiniciamos el servicio networking.service y obtendremos la configuración por DHCP en la tarjeta :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.024.png)

Además también podemos ver las concesiones el fichero de concesiones , en el servidor en la siguiente ruta /var/lib/dhcp/dhcpd6.leases :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.025.jpeg)

No lo he mencionado anteriormente pero para que al producirse la configuración el cliente obtenga los parámetros que hemos configurado por DHCPv6 tendremos que poner este parámetro a ON en el fichero de configuración de SLAAC :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.026.png)

Como podemos ver el único parámetro que hemos especificado en el servidor DHCP a sido el DNS de google  ha sido correctamente configurado en nuestro cliente :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.027.png)

##### Mensajes DHCPv6 con SLAAC

Acabamos de configurar SLAAC y DHCPv6 sin estado , esto significa que :

- Usa SLAAC para obtener una dirección IPV6 de tipo global unicast , además de la puerta de enlace .
- Usa el servidor DHCPv6 sin estado, para el resto de parámetros de configuración de nuestra red . 

Es decir hemos configurado la segunda opción  de la siguiente imagen :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.028.jpeg)

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.029.jpeg)


{{< alert type="info" >}}
Las capturas que verás a continuación NO están recortadas debido a que se ven pixeladas. Los mensajes de la comunicación están en orden.
{{< /alert >}}

Si observamos la captura de Wireshark y la comparamos con la configuración única de SLAAC :


**Operaciones de SLAAC:**

1. Podemos ver que el PC1 a solicitado un RS , a todos los routers de la red (Multicast)

![ref1]

2. R1 le responde a PC1 con un RA(Indica si necesitara comunicarse con un DHCPv6 con estado o sin estado)

![ref2]

3. NS , para comprobar que la dirección asignada no esta duplicada

![ref3]

**Operaciones de DHCPv6:**

4. Solicit a todos los servidores DHCPv6 de la red (Multicast a ff02::1:2) incluye un identificador de cliente CID.![ref1]
5. Advertise : Es la respuesta del servidor DHCPv6 a un solicit , este incluye las opciones de configuración oportunos , incluido una IPv6 . También incluye un CID y un XID(Id transacción).![ref4]
6. Request: El cliente envía este mensaje a todos los servidores DHCPv6 para indicar que desea los parámetros ofertados en el Adverstise . También incluyen CID y XID.![ref5]
7. Reply: El servidor DHCPv6 responde y confirma que la dirección ha sido asignada así como todos los parámetros adicionales de configuración .También incluyen CID y XID.![ref1]

Aquí te dejo una imagen en la que se observa el orden de los mensajes que hemos recibido y una breve descripción del mismo , además nos indica si los mensajes son unicast o multicast :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.035.jpeg)

## Apache en IPV6

Para las versiones de Apache superiores a 2.X tienen soporte para IPV6 habilitado por defecto así que al instalar el servicio ya estaremos escuchando por este protocolo sin necesidad de realizar ninguna configuración adicional en el servicio .

Podemos comprobar si al instalarlo nuestro servidor esta escuchando por ese puerto :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.036.png)

En el caso de que creemos un virtualhost podemos especificar como queremos que trabajen si usando ambos protocolos IPV6 y IPV4 o solo uno de ellos . Vemos que ssh también utiliza ipv6 por defecto .

### Acceso al servidor web desde dentro de la red

Vamos a acceder desde las maquinas de nuestra red en mi caso lo he montado en el router ya que es el único que tiene acceso a internet en este escenario .

Me conectare a el utilizando la direccion global pero podríamos usar la local sin problema ya que pertenecemos a la misma red local  . 

Acceso desde PC2:

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.037.png)

### Acceso al servidor web desde fuera de la red

Para esto deberemos de configurar R1 y ‘PC3’ en la misma red usando IPV6 :

PC3:

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.038.png)

R1:

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.039.png)

Le haremos la petición a PC1 desde PC3 que esta fuera de esa red local , como vemos no es necesario hacer NAT .

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.040.jpeg)

Incluso puedo hacerle ping a un host desde otra red  :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.041.png)Si analizamos estas peticiones con Wireshark podemos ver que en ningún momento se produce NAT:

Fuera de la red :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.042.png)

Dentro de la red:

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.043.png)

Por supuesto un host de nuestra red local puede acceder al servidor web :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.044.png)

## CISCO

### Configuración de un router cisco en IPV6

Lo primero que haremos sera calcular la direccion IPV6 que le corresponden a las MACS :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.045.png)

F 0/0 –> CA:01:6C:FA:00:00 –>  CA:01:6C:FF:FE:FA:00:00 –> C801:6CFF:FEFA:0

F 1/0 –> CA:01:6C:FA:00:1C-→  CA:01:6C:FF:FE:FA:00:1C –> C801:6CFF:FEFA:001C

Para que nuestro router se configure usando SLACC y no tengamos que hacer esto manualmente introduciremos los siguientes comandos para cada una de las interfaces que queramos que se configuren por SLAAC :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.046.png)

También deberemos de indicarle no shut para que se levante la interfaz .

Con el siguiente comando comprobaremos que nuestro router se ha configurado correctamente automáticamente usando SLAAC :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.047.png)

Ya con las direcciones de enlace local tendremos conectividad con el router :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.048.png)

#### SLAAC

Ahora vamos a hacer que el router configure a los clientes usando SLAAC .

Vamos a configurar una dirección global a nuestro router en la interfaz que da a la red que queremos darle este servicio , con el prefijo de red : 3333:db7::

Vamos a utilizar EUI-64 para configurar nuestras interfaces :

FastEthernet 0/0 –> 3333::C801:6CFF:FEFA:0/64

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.049.png)

FastEthernet 1/0 –> 2222::C801:6CFF:FEFA:1C/64

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.050.png)

Comprobamos las direcciones IPV6 se han “generado” correctamente :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.051.png)

Para que el router nos configure a los clientes deberemos de introducir el siguiente comando este , hará que nuestro router mande RA y conteste a las peticiones de RS:

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.052.png)

Una vez hecho esto nuestros clientes se habrán configurado correctamente : 

PC1:

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.053.png)

PC2:

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.054.png)

Los mensajes que se han producido al configurar los clientes :

**Router solicitation** (RS): El PC le envía un mensaje de RS a todos los routers para indicar que necesita un RA , este mensaje se envía si no recibe ningún RA pasado un tiempo.

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.055.png)

**Router Advertisement** (RA): Una vez el router recibe el RS o periódicamente envía un RA en el cual se incluye el prefijo de la red y su longitud . En el caso de que el router responda a un RS este le envía un RA especifico al host que lo ha solicitado . En el caso de que sea un  mensaje RA periódico  se envía a la dirección IPv6 de multidifusión de todos los nodos, FF02::1, con la dirección link-local del router como la dirección IPv6 de origen.

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.056.png)

**Neighbor Solicitation** (NS): Se utiliza para conocer la direccion MAC de un dispositivo de tu red , es similar al protocolo ARP .

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.057.png)

**Neighbor Advertisement** (NA) : Es el mensaje de respuesta de un NS .

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.058.png)

##### DHCPv6 con SLAAC

Configurar un servidor de DHCPv6 con estado es similar a configurar un servidor sin estado. La diferencia más importante es que un servidor con estado también incluye información de direccionamiento IPv6 de manera similar a un servidor DHCPv4.

Lo primero que tendremos que hacer sera  para habilitar el routing IPv6. Este comando no es necesario para que el router sea un servidor de DHCPv6 con estado, pero se requiere para que el router origine los mensajes RA ICMPv6.

–> ipv6 unicast-routing

Lo tenemos configurado en el apartado anterior así que no lo volveremos a hacer . Configuraremos un pool DHCPV6 :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.059.png)

Con DHCPv6 con estado, todos los parámetros de direccionamiento y otros parámetros de configuración deben ser asignados por el servidor de DHCPv6. El comando address prefix se utiliza para indicar el conjunto de direcciones que debe asignar el servidor. La opción lifetime indica el tiempo de arrendamiento válido y preferido en segundos. Al igual que con DHCPv6 sin estado, el cliente utiliza la dirección IPv6 de origen del paquete que contenía el mensaje RA.

Le indicamos el prefijo de red y el tiempo de vida de cada dirección :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.060.png)

Ahora le indicamos los servidores DNS :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.061.png)

Aun podemos configurar mas parámetros como el nombre del dominio pero en mi caso solo me interesa esto , así que procederemos a indicarle en que interfaz tiene que funcionar el servicio :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.062.png)

Ahora comprobaremos que el servidor DHCP , esta funcionado en nuestra interfaz :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.063.png)

Veremos como en el cliente se ha asignado el servido DNS:

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.064.png)

Y la concesión en el servidor DHCP :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.065.png)

**Operaciones de SLAAC:**

1. Podemos ver que el PC2 a solicitado un RS , a todos los routers de la red (Multicast)

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.066.png)

2. R1 le responde a PC1 con un RA(Indica si necesitara comunicarse con un DHCPv6 con estado o sin estado)

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.067.png)

**Operaciones de DHCPv6:**

3. Solicit a todos los servidores DHCPv6 de la red (Multicast a ff02::1:2) incluye un identificador de cliente CID.

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.068.png)

4. Advertise : Es la respuesta del servidor DHCPv6 a un solicit , este incluye las opciones de configuración oportunos , incluido una IPv6 . También incluye un CID y un XID(Id transacción).

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.069.png)

5. Request: El cliente envía este mensaje a todos los servidores DHCPv6 para indicar que desea los parámetros ofertados en el Adverstise . También incluyen CID y XID.

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.070.png)

6. Reply: El servidor DHCPv6 responde y confirma que la dirección ha sido asignada así como todos los parámetros adicionales de configuración .También incluyen CID y XID.

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.071.png)

###### Acceso al servidor web desde dentro de la red

Desde nuestra red local podremos hacer la petición al servidor web usando tanto la dirección local de enlace como la dirección global :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.072.png)

###### Acceso al servidor web desde fuera de la red

SWEB –> 3333:db7::ef7:42ff:fe92:0

Vemos que con la configuración anterior que teníamos en apache podemos acceder sin problema al servidor web desde una maquina de fuera de nuestra red :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.073.png)

## Configuración básica de apache para IPV6

Como comentaba antes no es necesario a partir de la version 2.X en adelante de configurar nada adicionalmente en apache para que nuestro servidor funcione usando el protocolo IPV6 ya por defecto este escucha en IPV4 y IPV6 .

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.074.png)

Sin embargo podemos configurar para que este solo escuche por IPV6 , para ello deberemos de realizar una simple configuración en el servicio . Accederemos al fichero –> /etc/apache2/ports.conf

Comentaremos la linea Listen 80 ya que hace referencia a IPV4 y le añadiremos la referente a ipv6.

Con esta configuración escucharemos todas las peticiones de cualquier dirección IPV6 , en los corchetes podemos especificar una dirección para responderle peticiones solo a esta .

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.075.png)

Ahora accederemos a nuestro host virtual y cambiaremos la declaración de este , al igual que hemos hecho arriba modificando la etiqueta que hace referencia a todas las direcciones IPV4 y la cambiaremos por esta para hacer referencia a todas las direcciones IPV6 por el puerto 80 :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.076.png)

Ahora reiniciaremos el servicio apache y comprobaremos que el estado del mismo es exitoso :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.077.jpeg)

Con esto ya nuestro servidor apache funcionaria solo en IPV6 :

![](/redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.078.png)

## Bibliografía

- [¿Que es SLAAC?-Alberto Molina ](https://youtu.be/MndaZaCo6xk)
- [Mensajes de SLAAC](https://www.sapalomera.cat/moodlecf/RS/2/course/module10/10.2.1.2/10.2.1.2.html)
- [Montar un servidor DHCPv6 Debian ](https://franciscojesusgu.files.wordpress.com/2020/07/ut01-sri-ipv6_7_dhcp.pdf)
- [Mensajes DHCPv6 con SLAAC ](https://youtu.be/tP9QOLZrAss)
- [Apache IPV6](http://www.ipv6tf.org/pdf/ipv6paratodos.pdf)


[ref1]: /redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.030.png
[ref2]: /redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.031.png
[ref3]: /redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.032.png
[ref4]: /redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.033.png
[ref5]: /redes/escenario_ipv6_basico/img/Aspose.Words.e7f0d3c3-3d56-4aa1-a556-ca7031f37ba4.034.png
