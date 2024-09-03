---
title: "Configuración de switches en GNS3"
date: 2023-09-08T10:00:00+00:00
description: Aprenderás a configurar los switches de GNS3 como los cisco 7200 como uno .
tags: [Redes, Wireshark, GNS3,Cisco,Switches]
hero: /images/redes/switches_gns3/portada.jpg
---



Aprenderás a configurar switches en GNS3, tanto dispositivos genéricos como switches Cisco, utilizando el concepto de VLANs para segmentar la red y explorar las complejidades de la gestión de redes.

## Preparación escenario

Lo primero que haré sera montar el escenario :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.001.jpeg)

### Configuración de red de los clientes

A continuación configurare las tarjetas de red de los clientes , aprovechando que la nube NAT incluye un servidor DHCP.

Para hacer esto escribimos en los VPCS el siguiente comando :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.002.png)

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.003.png)

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.004.png)

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.005.png)

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.006.png)

## Ejercicio A

**1 PC1 y PC3 pertenecen a la VLAN 10, PC2 y PC4 pertenecen a la VLAN 20. Demuestra el funcionamiento correcto de ambas VLAN y que no hay conectividad entre PC2 y PC3. ¿Puedes hacerlo con los switches Ethernet que trae GNS3? ¿Encuentras alguna limitación? ¿Cuáles son las distintos tipos (types) que puede tener un puerto y en qué se diferencian?**

Para configurar las VLANS en los switches , le damos clic derecho y a continuación realizamos la siguiente configuración :

Para el switch 3 (PC1 y PC2)

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.007.png)

Para el switch 2 (PC3 y PC4)

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.008.jpeg)

Para el switch  (PC5 Y NAT1)

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.009.png)

PC1 , solo tendrá conectividad con los PCs que pertenecen a su VLAN :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.010.png)

PC2 , solo tendrá conectividad con los PCs que pertenecen a su VLAN:

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.011.png)

Con sus respectivas parejas del otro switch obtendremos el mismo resultado. PC3 , solo tendrá conectividad con los PCs que pertenecen a su VLAN:

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.012.png)

PC4 , solo tendrá conectividad con los PCs que pertenecen a su VLAN:

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.013.png)

Tenemos que tener en cuenta que los dispositivos que no pertenecen a la VLAN 10 deberemos de configurados manualmente ya que estos no tienen conectividad con el servidor DHCP.

El ejercicio A podemos hacerlo perfectamente con los switches que trae GNS3 , encontraremos una limitación importante , ya que los switches solo permiten que las bocas pertenezcan a una VLAN . 

Al realizar el ejercicio debemos de tener en cuenta los  types que puede tener un puerto , los que hemos utilizado son los dos primeros  :

- Access: Este es el destinado para un equipo final , es decir un cliente ya que se encarga de eliminar el etiquetado que va en el encabezado.
- Dot1q:Este es el encargado de interconectar dispositivos de red entre si , se encarga de añadir el etiquetado en el encabezado para mandar el paquete a otro dispositivo y que este sepa a que VLAN pertenece .
- QinQ : Es similar a dot1q pero este además se encarga de añadir en el etiquetado , el tipo de paquete para identificarlos .

Teniendo esto en cuenta podemos hacer una analogía con la practica de switches físicos : Los puertos untagged –> Access 

Los puertos tagged –> Dot1q 

Al utilizar estos switches el protocolo 802.1Q pero “con menos funciones” no podemos indicar que VLANS queremos que utilice los puertos configurados como Dot1q , sino que este a través de la VLAN por defecto pasara los paquetes etiquetados de todas las VLANS . 

## Ejercicio B

**2 Todos los ordenadores deben poder acceder al servidor de datos, pero solo PC1 y PC3 deben acceder a Internet. Lo harán a través de vuestra máquina física usando el elemento llamado NAT, que deberéis comprender y configurar. ¿Puedes hacerlo con los switches Ethernet que trae GNS3? ¿Qué limitación te encuentras? Para superar dicha limitación, descarga el CISCO 3725 como appliance y úsalo en lugar de los switches Ethernet configurándolos adecuadamente.**

### Switches Ethernet

Aquí encontramos la primera limitación de estos switches , ya que solo podemos tener 1 VLAN por puerto esto quiere decir que solo una VLAN tendrá acceso a estos recursos .

Como queremos que solo la VLAN 10 navegue por internet configuraremos la boca de nuestra nube a una boca con tipo Access y que pertenezca a esta VLAN :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.014.png)

Por lo que para este punto no hay problema , nuestros PC1 y PC3 , ambos serán capaces de navegar por internet :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.015.png)

Como estos 2 PCS pertenecen a la misma VLAN que la nube NAT pueden comunicarse sin problema y utilizar el servidor DHCP que incluye la misma para configurarse . Mientras que los PC2 y PC4 no podrán ni navegar ni configurarse por DHCP al no pertenecer a la misma VLAN que la nube NAT :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.016.png)

Con el servidor de datos nos toparemos con la limitación  ya que únicamente un puerto puede pertenecer a una VLAN , solo una pareja de nuestros PCs podrán comunicarse . Esto podríamos evitarlo configurando el servidor como una “maquina real” con 2 interfaces virtuales y diciéndole al switch que cada una pertenece a una VLAN distinta .  

### CISCO 3725

Para comenzar a utilizar este dispositivo , tendremos que añadirle espacio al disco para que podamos  iniciarlo  ,  además  podemos  añadir  el  modulo  de  16  bocas  Ethernet  de  forma predeterminada así no tendremos que hacerlo a mano mas adelante .

Para realizar esta configuración deberemos de tener importado el router y acceder a Edit > preferences > IOS routers . 

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.017.jpeg)

Una  vez modificada la plantilla colocaremos los 3725 en el escenario y montaremos el mismo escenario :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.018.png)

Debemos de tener en cuenta que las interfaces FastEthernet0/0 y FastEthernet0/1 funcionan como routers , es decir no podemos utilizarlos como switch . Los puertos que se comportan como switch son todos los de  FastEthernet1  así que sera los que utilicemos .

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.019.png)

A continuación le diremos a estos puertos que tienen que funcionar como si fuesen un switch para ello introduciremos los siguientes comandos en cada uno de los 3725.

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.020.png)

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.021.png)

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.022.png)

Ahora crearemos las vlans usando los siguientes comandos , para cada uno de los switches : 

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.023.png)

Podemos listarlas con el siguiente comando :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.024.jpeg)

Ahora le asignaremos  a los puertos su VLAN correspondiente :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.025.png)

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.026.png)

A continuación configuraremos el puerto que une a los dos 3725 , para esto lo ponemos en modo trunk  y permitimos el trafico encapsulado de todas las VLANS por este puerto .

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.027.png)

Por ultimo guardaremos los cambios para que si se apaga el equipo mantenga las modificaciones que hemos realizado :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.028.png)

Con esto habremos configurado el primer 3725 , su homologo a este , es decir el que conecta a PC3 y PC4 , tendríamos que hacer lo mismo adaptado a los puertos en los que estén conectado los dispositivos . 

Continuaremos configurando el 3725 que une ambos “switches” y da salida al servidor de datos y a internet . Para ello crearemos las VLANS 10 y 20 :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.029.png)Y le asignaremos al servidor de datos ambas VLANS mientras que a la salida a internet solo la VLAN 10:

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.030.png)

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.031.png)

Ahora configuraremos las interfaces que interconectan los switches :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.032.png)

A continuación crearemos las dos subintrantes para permitir el trafico entre ellas y le asignaremos direcciones ip .

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.033.png)

Ahora el servidor de datos lo conectaremos al puerto Fe0/0 y en el crearemos dos subintrantes , yo utilizare una maquina debian . Esto lo haremos editando en network interfaces :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.034.png)

Comprobamos que las interfaces estén subidas  :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.035.png)

Ahora crearemos las rutas de enroutamiento:

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.036.png)

Una vez hecho esto podremos hacerle ping al servidor de datos desde las dos interfaces :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.037.png)

Podemos hacerle ping al servidor de datos y tendremos conectividad con el :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.038.png)

Vemos que el trafico es capaz de llegar al servidor de datos sin embargo este no es capaz de “hacer el camino de vuelta ”.

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.039.jpeg)

También he configurado enroutamiento inter vlan , siguiendo los enlaces de la bibliografía sin embargo no me ha funcionado tampoco.


## Ejercicio C

Responde a las siguientes preguntas sobre los apartados anteriores:

**C.1 ¿Qué pasa con el direccionamiento cuando añades la nube de NAT? ¿Cuál es el motivo de este cambio?** 

Cuando ponemos la nube NAT , esta incluye un servidor DHCP el cual tiene la direccion ip 192.168.122.1 y asignas direcciones de la red 192.168.122.1/24 . A través de la configuración que nos proporciona este nos permitirá navegar por internet .

**C.2¿Por qué es necesario asignar un disco duro a cada uno de los dispositivos y qué tamaño mínimo debe tener para que el escenario funcione?**

Para los routers cisco 3725 , para que este inicie y supere el chequeo inicial este debe tener como mínimo un espacio de 1MB , además si queremos guardar las configuraciones esto sera necesario .Por ejemplo para guardar la información de las vlans sera necesario.

**C.3¿Qué diferencia hay entre configurar un puerto del switch en modo **access** y en modo **trunk** y cuándo hay que usar cada uno de ellos?**

El modo access esta pensado para conectar un cliente final es decir , un pc . Es el equivalente a el “ puerto untagged “ , sin embargo este tiene una limitación el cual es que solo puede pertenecer a una vlan , este puerto se encarga además de eliminar el encabezado que añaden los puertos trunk para que los dispositivos finales puedan entender los paquetes .

Por otro lado el modo trunk permite interconectar un dispositivo de red con otro , por ejemplo un switch con otro switch , seria el equivalente a un “puerto tagged” , este además permite el trafico de varios vlans , etiquetando las tramas para que los demás dispositivos puedan interpretar la VLAN a la que pertenece el paquete  .


## Ejercicio D

**Sustituye ahora PC1 y PC3 por dos máquinas **Linux con Firefox** instalado (puedes encontrar las imágenes en el MarketPlace de GNS3) y comprueba que navegan correctamente.**

Lo añadimos al escenario y los conectamos a las mismas bocas que teníamos nuestros VPCS para que mantengan la configuración anterior de las VLANS y tengamos acceso a la nube NAT .

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.040.png)

Una vez hecho esto accederemos a la interfaz de la maquina y configuraremos su tarjeta de red por DHCP , para ello accederemos al panel de control :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.041.png)

En el panel de control accedemos a network para configurar la red :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.042.png)

En el panel de network diremos que use DHCP y guardamos la configuración :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.043.png)

En la terminal podemos cerciorarnos de que la configuración de red se ha realizado correctamente . 

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.044.png)

Y podemos ver que haciendo este procedimiento ya podremos navegar con el tinycore con Firefox  :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.045.png)

Aquí la prueba con el segundo tiny core :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.046.jpeg)

## Ejercicio E

**Monta un Port Bonding entre el switch de cabecera y los otros dos. Demuestra su correcto funcionamiento y explica detalladamente como lo has configurado. Explica los flags que puede tener un portchannel.**

A continuación deberemos de configurar los puertos extra que hemos añadido al escenario para que estén en modo trunk y se respete nuestro escenario con las VLANS , es repetir lo que hemos hecho anteriormente.

Lo primero que deberemos de hacer sera crear las interfaces lógicas ,sin embargo  este paso lo podemos omitir ya que posteriormente si  no existe la interfaz la creara automáticamente .

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.047.png)

Indicaremos que interfaces queremos que  pertenezcan al port-channel 1 para el enlace lógico entre R1-R2 y que pertenezcan al port-channel 2 para el enlace lógico entre R2-R3.

Para R1-R2 :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.048.png)

Para R2-R1 :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.049.png)

Para R2-R3 :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.050.png)

Para R3-R2 :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.051.png)

También  podemos  configurar  el  EtherChannel  como  un  enlace  trunk,  y  así conseguimos multiplexación estadística del tráfico de las VLANs y que ante la caída de un enlace sigue funcionando el otro con ambas VLANs. Esto lo haremos con todos los enlaces lógicos :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.052.png)

Una vez hecho esto podemos comprobar si están funcionando los etherchannels:

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.053.png)

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.054.png)

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.055.png)

La configuración de un EtherChannel se puede hacer utilizando uno de estos protocolos :Port Aggregation Protocol (PAgP) o Link Aggregation Control Protocol (LACP).Ambos extremos se deben de configurar en el mismo modo.

Estos tienen unas serie de  “modos ” en los cuales cambiara el comportamiento del puerto a la hora de crear enlaces :

- on: En este modo, los enlaces miembros del grupo se agregarán manualmente y no se monitorizarán automáticamente. Este modo se utiliza cuando se desea tener un mayor control sobre los enlaces miembros del grupo.
- desirable: En este modo, el switch intentará negociar  con el dispositivo conectado en el otro extremo del enlace. Si el dispositivo del otro extremo también está configurado en modo "desirable", se agregará automáticamente el enlace.
- auto: En este modo, el switch no intentará negociar sino que agregará automáticamente el enlace si el dispositivo conectado en el otro extremo del enlace está configurado en modo "desirable".
- active: En este modo, el switch enviará constantemente LACP PDUs para determinar si el dispositivo conectado en el otro extremo del enlace está disponible y también está configurado para usar LACP. Si el dispositivo del otro extremo está disponible y también está configurado para usar LACP, se agregará automáticamente el enlace.

## Ejercicio F

**Port Mirroring: Conecta un PC5 al Switch1 y monitoriza el tráfico que sale de PC1. Realiza una captura con Wireshark en la boca correspondiente al PC5 y explica el tráfico capturado.**

Lo primero que haremos sera configurar el port mirroring , en mi caso enviara el trafico de la boca 1/5 a la 1/4.

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.056.png)

Hare en el pc5 un ping a google y monitorizare el cable que va desde el router a pc4 , para comprobar que este funcionando el port mirroring :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.057.png)

Vemos que hemos podido “interceptar ” un ping , proveniente de la dirección ip del PC6 .

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.058.png)

Esto hará que el trafico entrante y saliente del puerto que hemos puesto como sniffer nos lo reenvié al puerto que escucha .

Podemos comprobar el estado de la sesión del port mirroring con este comando :

![](../img/Aspose.Words.1880b7c0-3050-4e53-a32a-505911fdf872.059.png)

## Bibliografía

- [Switching and GNS3](https://docs.gns3.com/docs/using-gns3/beginners/switching-and-gns3/)
- [The NAT node](https://docs.gns3.com/docs/using-gns3/advanced/the-nat-node)
- [Simulando switch cisco en GNS3](https://www.josedomingo.org/pledin/2014/02/simulando-switch-cisco-en-gns3/)
- [GNS3, añadiendo hosts a nuestras topologías](https://www.josedomingo.org/pledin/2013/11/gns3-anadiendo-hosts-a-nuestras-topologias/)
- [Trabajando con switch en GNS3: VLAN y Trunk](https://www.josedomingo.org/pledin/2014/02/trabajando-con-switch-en-gns3-vlan-y-trunk/)
- [LACP y  PAGP](https://community.fs.com/es/blog/lacp-vs-pagp-comparison.html)
- [Routing interVLAN ](https://www.cisco.com/c/es_mx/support/docs/lan-switching/inter-vlan-routing/41860-howto-L3-intervlanrouting.html)
- [Enroutamiento VLAN](https://www.sapalomera.cat/moodlecf/RS/2/course/module5/5.1.2.1/5.1.2.1.html)
- [Configurar PortBonding ](https://ccnadesdecero.es/configurar-etherchannel/)[LinkAggregationControlProtocol(LACP)andPortAggregationProtocol(PAgP) ](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-3750-series-switches/69979-cross-stack-etherchannel.html#lacp)[Wikipedia Ether-channel](https://es.wikipedia.org/wiki/EtherChannel)
- [Comunicación Inter VLAN](https://www.vilarrasa.com.ar/nnn7.htm)
