---
title: "Protocolo ARP"
date: 2023-09-08T10:00:00+00:00
description: Documento en el cual se responden a una serie de preguntas sobre el protocolo ARP
tags: [Redes, ARP]
hero: images/redes/arp/portada.png
---

## ¿Crees que la pregunta ARP es un mensaje de difusión? Realiza una captura en Wireshark de una petición ARP y analízala para justificar tu respuesta.

Si , es un mensaje de difusión ya que en la cabecera podemos ver que el destino tiene una dirección de broadcast . Esta dirección es la que tiene todos sus bits a 1 que en las direcciones mac se traduce en FF:FF:FF:FF:FF:FF .

Cuando esta le llegue , en este caso al que tiene la dirección ip 192.168.1.1 nos devolverá la petición y en el origen obtendremos su dirección MAC.

![](../img/Aspose.Words.239ce20f-0f3b-447a-b584-fd1166c210d0.001.jpeg)

## ¿Crees que la respuesta ARP es un mensaje de difusión? Realiza una captura en Wireshark de una respuesta ARP y analízala para justificar tu respuesta.

Podemos ver en la respuesta que en la dirección de destino viene la del pc que mando la pregunta , por lo que la respuesta no es un mensaje de broadcast sino una comunicación punto a punto .

![](../img/Aspose.Words.239ce20f-0f3b-447a-b584-fd1166c210d0.002.jpeg)


## Los ordenadores de una red almacenan en memoria una caché con las correspondencias IP-MAC que van conociendo. Explica el proceso de actualización de la caché ARP después de observar como se va rellenando en  las máquinas de un pequeño escenario en GNS3 con una red local con cuatro ordenadores conectados a un switch. Ve comprobando como cambia la caché ARP de todos los ordenadores cuando vas haciendo ping entre un ordenador y otro.

Cuando hacemos un ping el emisor y el receptor “se añaden mutuamente a la tabla arp” , si las consultamos en ambas veremos que están incluidos :

![](../img/Aspose.Words.239ce20f-0f3b-447a-b584-fd1166c210d0.003.png)

![](../img/Aspose.Words.239ce20f-0f3b-447a-b584-fd1166c210d0.004.png)

Podemos ver que el tiempo por el que se guardan en cache es de 120 segundos , cuando este tiempo se acaba, se borra la entrada.

Mientras que en los pcs que no han intervenido no almacenaran nada en la cache arp sobre la “transacción realizada”:

![](../img/Aspose.Words.239ce20f-0f3b-447a-b584-fd1166c210d0.005.png)

![](../img/Aspose.Words.239ce20f-0f3b-447a-b584-fd1166c210d0.006.png)

## Analiza el comando ip neigh para ver las posibilidades que ofrece y piensa cual puede ser el uso real de cada una de ellas.

Este comando nos permite interactuar con la tabla arp donde se guardan la relación de direcciones IP-MAC . Por ejemplo podemos visualizarla , añadir entradas o borrarlas así como modificarlas . Además podemos cambiar el tiempo durante el cual se guarda una petición en la tabla .

Por ejemplo , listar el contenido :

![](../img/Aspose.Words.239ce20f-0f3b-447a-b584-fd1166c210d0.007.png)

Podemos resumir sus funciones : 

- Mostrar la tabla ARP completa: ip neighbour show
- Agregar una entrada a la tabla ARP: ip neighbour add (IP) lladdr {MAC} dev {interface}
- Eliminar una entrada de la tabla ARP: ip neighbour del {IP} dev {interface}
- Establecer el tiempo de vida de una entrada en la tabla ARP: ip neighbour change {IP} dev {interface} nud {state}
- Buscar una entrada específica en la tabla ARP: ip neighbour | grep {IP}

Básicamente esto es lo que debemos conocer para poder controlar las tablas ARP con el comando IP en sustitución (o como complemento) a «arp».

## Averigua qué es un ARP gratuito y cuál es el sentido de su existencia.

Es una solicitud emitida por un dispositivo con el objetivo de actualizar la tabla arp del resto de dispositivos de una red . Este simplemente informa a los demás dispositivos de la red de su propia dirección IP y MAC . 

El propósito principal de las ARP gratuitas es asegurar que todos los dispositivos en una red tengan la información más actualizada posible sobre las direcciones IP y MAC de los demás dispositivos en la red. 

Una de sus utilidades es detectar conflictos de IP's,  "esta ip ya está cogida" esto es debido a  que otro equipo ha respondido con estos paquetes. 

Por lo que a partir de esta información se puede resolver esta incidencia.


## Explica con tus palabras en qué se basa un ataque ARP Spoofing y cómo se lleva a cabo. ¿Puede usarse como técnica de ataque desde tu casa a una red ajena? ¿Cómo podríamos defendernos de él?

El ataque viene a modificar el flujo de los datos enviados desde un PC Víctima que pasa a través de un Gateway para hacer un ataque de tipo MITM (Man in the Middle) consiguiendo que el tráfico de la víctima pase por una máquina Atacante de forma inocua para la víctima.

Así el atacante intercepta los mensajes y es capaz de obtener todo el trafico de la red obteniendo contraseñas e información confidencial o sensible .

![](../img/Aspose.Words.239ce20f-0f3b-447a-b584-fd1166c210d0.008.jpeg)

Los pasos que sigue un atacante al realizar este ataque son :

1. Escanear la red , para obtener una relación de los dispositivos conectados .
2. Enviar paquetes arp falsos para asociar en las víctimas su dirección ip a su propia mac.
3. Una vez que el cliente ha sido “engañado” , el atacante comenzara a interceptar todo el trafico.

Estos ataques solo se producen si el atacante consigue acceso a tu red local , así que para protegernos podemos usar :

- Herramientas de detección de ARP Spoofing .
- Utilizar un firewall , ya que ese es capaz de bloquear paquetes ARP sospechosos .
- Utilizar protocolos como Ipsec y SSL/TLS .
- Configurar la tabla arp de manera estática.

## Hay dos tipos de ataques a switches llamados MAC Flooding y MAC Spoofing. ¿En qué consisten y cómo podemos defendernos de ellos?

MAC Flooding consiste en llenar la tabla arp de un dispositivo  de red , por ejemplo un switch  y hacer que este no sea capaz de localizar a que boca va el trafico a si este lo mandara por todas las bocas provocando que en el peor de los casos dejar sin servicio al dispositivo .

Para mitigar este ataque se recomienda configurar un limite en el tamaño de la tabla ARP y la detección y bloqueo de trafico sospechoso . 

Mientras que el MAC Spoofing consiste en falsificar una dirección MAC para interceptar un determinado trafico , pudiendo tener acceso a contenido privado .

Para mitigar este ataque en el caso de que suplante una maquina de mi red y tenga acceso a contenido  podemos  implementar  herramientas  de  segundo  factor  de  autentificaron  o  usar certificados digitales . 

Además podemos implementar en nuestra red las siguientes estrategias : 

**Entradas estáticas en tabla ARP**

La primera solución que existe corresponde a trabajar con rutas estáticas en los equipos de red. Esto permite invalidar los mensajes ARP, debido a que las IP se asocian una dirección MAC y esta no cambia en el tiempo. Es una solución simple y en general se aplica para asegurar que la puerta de enlace predetermina sea realmente la de la red y no un atacante. Sin embargo, es una estrategia difícil de aplicar si se posee una red con una gran cantidad de terminales.

**DHCP snooping**

Es una estrategia que mantiene un registro de las MAC que están conectadas en cada puerto y detecta inmediatamente si existe una suplantación. Varios fabricantes de equipos de red incorpora esta solución en sus equipos, como es el caso de CISCO.

**Dynamic ARP Inspection**

Para evitar la suplantación de ARP (ARP spoofing) y el envenenamiento por ARP (ARP poisoning) resultante, un switch debe garantizar que solo se transmitan ARP Requests y ARP Replies válidas.

La Inspección Dinámica de ARP/ Dynamic ARP Inspection (DAI) requiere de DHCP snooping y ayuda a prevenir ataques ARP así:

- No retransmitiendo respuestas/Replies ARP invalidas o gratuitas/gratuitous a otros puertos en la misma VLAN.
- Intercepta todas las solicitudes/Requests y respuestas/Replies ARP en puertos no confiables.
- Verificando cada paquete interceptado para un enlace válido de IP a MAC.
- Descarte y registro de respuestas no válidas de ARP para evitar el envenenamiento por ARP.
- Error-disabling la interfaz si se excede el número de paquetes ARP DAI configurado.

**RARP**

RARP es Reversal ARP, esto quiere decir que consulta a partir de una dirección MAC la IP correspondiente. En caso de que retorne más de una dirección IP, entonces la MAC ha sido clonada.



## Bibliografía

- [ip neigh](https://rm-rf.es/control-de-tablas-arp-con-el-comando-ip/)
- [arp spoofing](https://www.incibe-cert.es/blog/arp-spoofing)
- [ARP gratuitos ](http://www.tranquilidadtecnologica.com/2006/05/paquetes-arp-gratuitos.html)
- [medidas de mitigación](http://profesores.elo.utfsm.cl/~agv/elo323/2s14/projects/reports/MoraMorales/mitigacion.html#:~:text=Es%20una%20estrategia%20que%20mantiene,es%20el%20caso%20de%20CISCO.)

