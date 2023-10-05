---
title: "Comandos de supervisión de redes"
date: 2023-09-08T10:00:00+00:00
description: Descripción de tu publicación.
tags: [Redes, comandos]
hero: images/redes/comando_de_supervision_de_redes/comando_de_supervision_de_redes.webp
---

assets/images/redes/comando_de_supervision_de_redes/Comandos de supervisión de redes.webp

## Comandos en Windows

### Explica el significado de los distintos parámetros a configurar en las Propiedades de TCP/IP en Windows

Tenemos que tener en cuenta que cada configuración que hagamos es independiente para cada uno de nuestros adaptadores de red .

Para acceder a configurar estos parámetros seguiremos la siguiente ruta en nuestro sistema  :

Panel de control >Redes e Internet > Centro de redes y recursos compartidos > Cambiar configuración del adaptador :


![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.001.png)

Una vez aquí le daremos Clic derecho > Propiedades > Protocolo de version 4 (TCP/IP)

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.002.png)

Una vez aquí veremos dos pestañas a la cual podemos dirigirnos para configurar nuestra tarjeta , en la pestaña general  podemos observar los siguiente apartados :

El primer apartado (General) relacionado con nuestra dirección ip :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.003.png)

- **Obtener una dirección ip automáticamente :** Marcaremos esta opción cuando queramos que se use el servicio DHCP para asignar mediante el servicio dirección IP , mascara de subred y la puerta de enlace predeterminada .
- **Usar  la  siguiente  dirección  IP  :** Aquí  introduciremos  nosotros  manualmente  la configuración de red deseada :
- **Dirección IP:**  es una etiqueta numérica que identifica a nuestra maquina de manera única en nuestra red , no puede estar repetida .
- **Mascara de subred :** conjunto numérico  cuya función es indicar a los dispositivos qué parte de la dirección IP es el número de la red  incluyendo la subred, y qué parte es la correspondiente al host.
- **Puerta de enlace predeterminada :** Es la dirección ip predeterminada que se le asigna a un equipo para enviar los paquetes a otras redes .

En el segundo apartado de esta pestaña realizaremos la configuración referente a los servidores DNS los cuales permitirán traducirnos nombres a direcciones IP para poder navegar .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.004.png)

- **Obtener la dirección del servidor DNS automáticamente :**  Esta opción hará que la dirección se obtenga del servidor DHCP que tengamos configurado en nuestra red .
- **Usar la siguientes direcciones del servidor DNS :** Esta opción nos sirve para manualmente seleccionar la dirección ip de nuestros servidores DNS: 
- **Servidor DNS preferido :** La dirección que pongamos aquí sera la primera en consultar en caso de que necesite hacer una resolución 
- **Servidor DNS alternativo :** Si el servidor primario fallase o estuviera caído en ese momento pasaríamos a utilizar el secundario .

En la pestaña configuración alternativa , esta pensado para equipos que necesiten usarse en mas de una red  , suele verse en entornos profesionales :

- **Dirección ip privada automática :** Hará uso del servidor DHCP para configurarse .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.005.png)
- **Configurada  por  el  usuario  :** Nos permitirá  introducirla  manualmente  la configuración  (omitiré  los  campos explicados anteriormente ) :
- **WINS preferido :** es un servidor de nombres de Microsoft para NetBIOS, que  mantiene  una  tabla  con  la correspondencia entre direcciones IP y nombres NetBIOS de ordenadores . 
- **WINS alternativo :**  Si el servidor primario fallase o estuviera caído en ese momento pasaríamos a utilizar el secundario .


### Utilidad del comando ping

Ping es un comando o una herramienta de diagnóstico que permite hacer una verificación del estado de una determinada conexión de un host local con al menos un equipo remoto contemplado en una red de tipo TCP/IP , es la herramienta de diagnostico de redes mas conocida . 

Los usos mas comunes de esta herramienta son : 

- Comprobar la conectividad de una red.
- Medir la latencia que tardan en comunicarse dos puntos .
- Conocer la dirección IP utilizada por un nombre de dominio.
- Scripts que permiten llevar un registro de la disponibilidad de un servidor remoto.
- Scripts que permiten conocer cuando existe conexión en un equipo.

Para hacer uso de este abriremos una cmd , pulsaremos WIN + R y escribiremos cmd . 

#### Uso general de Ping 

La sintaxis mas simple de ping es la siguiente : ping  [Parámetros] [IP/Nombre]

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.006.png)

Si nos fijamos en la salida del comando vemos que nos permite conoces :

- **Dirección IP** que corresponde al nombre de la máquina remota.
- **El número de secuencia ICMP** (“Código que nos devuelve , ej : 0=red inaccesible”).
- **TTL**: Tiempo de vida en segundos; como este valor se decrementa en cada  máquina en la cual  es procesado, debe ser al menos igual o mayor que el número de saltos que dará .Si alguna vez este número es cero, el router interpretará que el paquete está viajando en círculos, por lo tanto, finaliza el proceso.
- **Latencia :**corresponde al lapso de tiempo en milisegundos que se necesita para dar una vuelta entre las máquinas fuente y destino. Como regla general, la demora de un paquete no debe ser mayor a 200 ms.
- **Estadísticas del ping :** Nos reúne toda la información mostrándonos los paquetes perdidos , enviados y recibidos . Además nos muestra el paquete con menor latencia y con mayor así como una media aritmética . 

#### PING -T 

Este parámetro nos permitirá hacer un ping infinito es decir no finalizara hasta que matemos el proceso , si no lo pusiésemos por defecto solo se enviaran 4 trazas . Para finalizar este la ejecución de este comando pulsaremos CTRL + C .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.007.png)

Cuando detengamos la ejecución nos mostrara las estadísticas que ha recopilado , paquetes enviados, paquetes recibidos y paquetes perdidos así como los tiempos medios de ida y vuelta .

#### PING -A

Este parámetro sirve para que nos resuelva una ip en un nombre de host ,imprimiendo  una linea indicando el nombre de host al cual le estamos dirigiendo las trazas , lo que nos permite identificar mas fácilmente las maquinas :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.008.png)


#### PING -N

Este parámetro sirve para especificar el numero de solicitudes echo  que deseemos al enviar paquetes , este lo indicaremos con un numero comprendido entre 1 – 4294967295 .

Por ejemplo si queremos enviar 10 trazas el comando seria el siguiente :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.009.png)

Podemos comprobar en la parte inferior que ha enviado en numero que le hemos indicado . 

#### PING -L

Nos permite modificar el tamaño en bytes de los paquetes enviados , deberemos especificar un numero entre 0 y 65000 . 

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.010.png)


#### PING -F

Este parámetro sirve para evitar que los paquetes se fragmenten , el tamaño máximo de los paquetes sin fragmentar es de 1472 bytes .

Podemos ver que si superamos este numero , nos dará un error informándonos que es necesario fragmentar el paquete :

#### PING -I 
![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.011.png)

Este parámetro nos permite especificar el numero máximo que se pueden dar hasta alcanzar al destino , el valor máximo que podemos introducir 255 .

Cuando especificamos un TTL esto fija el número máximo de saltos, al pasar por un nuevo dispositivo (un router) este descuenta 1 al TTL especificando hasta que llega a 0, en este caso el destino se mostrará como inalcanzable, de esta forma se evita que un paquete viaje por la red indefinidamente buscando un destino que puede que no exista.

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.012.png)

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.013.png)



#### PING -4 -6 

Ping -4 : Fuerza la respuesta del host especificado con una dirección IPv4. Es necesario que tanto el equipo que lanza el ping como el destino tengan una configuración IPv4 correcta.

Ping -6 : Fuerza la respuesta del host especificado con una dirección IPv6. Es necesario que tanto el equipo que lanza el ping como el destino tengan una configuración IPv6 correcta.

#### Comprobar conectividad en una red 

Vamos a efectuar una serie de pruebas para verificar el funcionamiento y encontrar errores . Lo primero sera hacernos ping a nosotros mismos para ello :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.014.png)

Si la salida es correcta esto demuestra que nuestro adaptador de red funciona correctamente .

Vamos a hacerle ping a una maquina de nuestra red local , así demostraremos que las conexiones físicas son correctas :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.015.png)

Vamos a hacerle ping a la puerta de enlace , de tener éxito demuestra que existe conexión con el equipo que suministra internet :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.016.png)

Haremos ping a un sitio de internet  usando ip , para comprobar que tenemos conexión a internet :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.017.png)



Por ultimo hacer ping a un dominio en internet ,de tener éxito demuestra que existe conexión a internet y los servidores DNS configurados en la conexión funcionan correctamente:

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.018.png)


### Uso general  del comando ipconfig

Este comando se usa para ver la configuración actual de los adaptadores de red de nuestro equipo , un ejemplo de uso general del comando es el siguiente :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.019.png)

Este nos muestra la siguiente información :

- **Descripción del adaptador** : Nombre del adaptador o tarjeta de red utilizado en la conexión.
- **Dirección IPV4:** Es la dirección IP asignada al equipo en la red local.
- **Puerta de enlace predeterminada:** Es la dirección IP del equipo proporciona acceso a internet.
- **Servidores DNS:** Dirección ip del encargado de resolver  nombre de dominio a dirección IP de las paginas solicitadas. Generalmente son dos, el principal y el secundario.
- **Estado de DHCP:** Configuración dinámica de host, en el caso del equipo mostrado  se encuentra habilitada, eso significa que siempre se utilizará una dirección IP asignada por este servicio .

A partir de estos parámetros podemos consultar la información del adaptador o identificar una incoherencia en la configuración del mismo .

#### IPCONFIG /ALL

Nos devolverá toda la información disponible de los adaptadores de red , es una salida mas detallada que si omitimos este parámetro , con este podemos consultar los servidores DNS y las direcciones MAC . 

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.020.png)

#### IPCONFIG /RELEASE

Se utiliza para liberar una dirección ip en el servicio DHCP , no se nos volverá a asignar una hasta que ejecutemos ipconfig /renew

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.021.png)

Podemos  especificar  el  adaptador  del  cual  queremos  que  se  libere  la  ip  escribiéndolo  a continuación, si omitimos el nombre los aplicara a todos . 

EJ: ipconfig /release Ethernet0 –> Solo liberara la ip del adaptador Ethernet0 **\***Si queremos liberar una dirección ipv6 utilizaremos el parámetro /release6

#### IPCONFIG /RENEW

Una vez ejecutado el comando anterior deberemos de ejecutar este para solicitar al servidor DHCP una nueva concesión de dirección IP  .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.022.png)

Podemos especificar el adaptador del cual queremos que se renueve la oferta DHCP  escribiéndolo a continuación. 

EJ: ipconfig /renew Ethernet0 –> Solo renovara la concesión del adaptador Ethernet0 **\***Si queremos renovar una dirección ipv6 utilizaremos el parámetro /renew6

#### IPCONFIG /FLUSHDNS

Se utiliza para vaciar la cache de resolución DNS de nuestro equipo local , suele utilizarse cuando queremos comprobar el correcto funcionamiento del servidor DNS . 

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.023.png)

#### IPCONFIG  /REGISTERDNS

Actualiza todas las concesiones DHCP y vuelve a registrar los nombres DNS. Este comando esta orientado al trabajo en entornos de dominio y a la actualización de los registros dinámicos del servidor de DNS del sistema en el que se esta ejecutando, teniendo en cuenta que si esta bloqueada de alguna forma la actualización dinámica no se efectuará.

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.024.png)

#### IPCONFIG /DISPLAYDNS

Este comando simplemente nos muestra las consultas DNS que se están almacenados en la caché de nuestro sistema de la forma que se muestran en la imagen, muestran datos de registros del protocolo IPv4 como de IPv6.

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.025.png)

#### IPCONFIG /SHOWCLASSID

Este comando nos permite comprobar las clases de usuario configuradas en nuestro servidor DHCP y que estarán disponibles para los diferentes clientes.

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.026.png)

\*Si queremos comprobarlo para IPV6 utilizaremos el parámetro /showclassid6 .


### Uso general ARP

El comando arp muestra y modifica las tablas de conversión de direcciones IP en direcciones

MAC que utiliza el protocolo de resolución de direcciones (ARP).

#### ARP -A

Pide los datos de protocolo actuales y muestra las entradas ARP actuales. Si se especifica inet\_addr, solo se muestran las direcciones IP y física del equipo especificado. Si existe más de una interfaz de red que utilice ARP, se muestran las entradas de cada tabla ARP.

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.027.png)

**\*** La opción -g hace la misma función :

Como se muestra en la captura de pantalla  el comando arp –a enumera todos los dispositivos que se encuentran actualmente en la caché ARP del host, lo cual incluye la dirección IPv4, la dirección física y el tipo de direccionamiento (estático/dinámico) para cada dispositivo.

Si queremos borrar la cache arp utilizaremos la opción -d seguida del comodín \* para borrar todas las entradas en esta tabla , si solo quisiéramos eliminar  una consulta pondríamos la dirección IP . 

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.028.png)

Podemos solicitar la MAC de una dirección usando arp + IP del dispositivo y posteriormente verla en nuestra tabla con arp -a .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.029.png)


### Uso general netstat

El comando netstat genera visualizaciones que muestran el estado de la red y estadísticas de protocolo. El estado de los protocolos TCP, SCTP y los puntos finales de UDP puede visualizarse en formato de tabla. También puede visualizarse información sobre la tabla de enrutamiento e información de interfaces.

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.030.png)

#### NETSTAT -A

Muestra las todas conexiones y puertos de escucha de nuestro equipo , así como el estado del puerto y la dirección remota la cual esta usando el mismo :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.031.png)


#### NETSTAT -B

Muestra el archivo ejecutable implicado en la creación de cada conexión o puerto de escucha.

#### NETSTAT -E
![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.032.png)

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.033.png)

Nos muestra estadísticas sobre las interfaces  de red , sirve para ver la actividad que ha tenido esta:

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.034.png)

#### NETSTAT -R

Nos muestra la tabla de enrutamiento , así podemos ver los sitios a los cual nuestro equipo es capaz de llegar a través de la red :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.035.png)


#### NETSTAT -N

Nos muestra las conexiones activas con un formato de tabla , similar al parámetro -a  solo que este nos indica el numero de puerto en lugar del nombre .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.036.png)

#### NETSTAT -O

Similar al parámetro anterior pero este nos añade el PID del proceso :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.037.png)

#### NETSTAT -P

Nos permite filtrar las conexiones según el protocolo (TCP, UDP, tcpv6 o tcpv4…)

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.038.png)


#### NETSTAT -T

Muestra el estado de descarga de la conexión actual :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.039.png)

Netstat es muy interesante para ver datos estadísticos de la conexión, pero también va a ser muy útil para analizar los puertos abiertos en un momento determinado y  así identificar problemas. Es esencial para determinadas aplicaciones y poder lograr un rendimiento óptimo .

### Uso general nslookup

Es una aplicación incluida en todos los sistemas Windows, para consultar, obtener información, probar y solucionar problemas con los servidores DNS .

Al  invocarlo  sin  especificar  ningún  parámetro,  devolverá  el  nombre  del  servidor  DNS predeterminado y su dirección IP :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.040.png)

El comando dispone de dos modos de uso , el tradicional a través de linea de comandos y el interactivo . Podemos usarlo para resolver nombres de direcciones desde la terminal poniendo nslookup seguido del nombre que queramos resolver :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.041.png)



También podemos hacer consultas inversas , es decir que a través de la ip nos diga el nombre :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.042.png)

Por ejemplo podemos seleccionar el tipo de registros DNS para hacer peticiones los cuales son :

- **A:** para buscar registros A que son los relacionados con la dirección IPv4..
- **AAAA:** para buscar registros AAAA que son los relacionados con la dirección IPv6. Si una web utiliza direccionamiento IPv6 y nosotros también, entonces tendremos que indicar este registro DNS.
- **PTR:** para buscar registros reversos.
- **MX** :para buscar los registros Mail Exchange del correo.
- **TXT:**, para buscar registros de texto como SPF o DKIM.
- **CNAME:** para buscar alias del dominio, esto también se conoce como subdominios, por ejemplo, el «www» siempre es un subdominio del principal» o el típico «ftp.» que es también un subdominio.

Para cambiar el tipo de registro utilizamos la orden set type=Nombre del registro , por ejemplo :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.043.png)

También podemos elegir el servidor desde el cual realizamos las consultas de la siguiente manera :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.044.png)



### Uso general tracert

Sirve para trazar la ruta que hace un paquete entrante que viene desde un host o punto de red hasta tu ordenador , así conocemos por donde viaja nuestro viaje .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.045.png)

Diciendo uno a uno todos los nodos y routers por los que pasa el mensaje de prueba que has enviado, sus direcciones IP y la latencia de cada uno de ellos hasta llegar a su destino.

Hay algunos nodos que no son capaces de respondernos por eso las entradas de tiempo de espera agotado .

Tenemos algunos parámetros interesantes como :

- -d : No convierte direcciones en nombres de host

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.046.png)

- -h : Nos permite seleccionar el numero máximos de saltos 

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.047.png)

- -4 o -6 : Fuerza usar IPV4 o IPV6 :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.048.png)

- -w : Nos permite especificar el tiempo de espera en milisegundos :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.049.png)


### Uso general route print

El comando Route se utiliza para visualizar y modificar la tabla de enrutamiento. Route print muestra una lista con las rutas actuales conocidas por IP para el host. Route add se utiliza para añadir rutas a la tabla, y route delete se utiliza para borrar rutas de la tabla.

Así podemos especificar el camino para llegar a una red o dispositivo .

La sintaxis es la siguiente : route [-f] [-p] [comando [destino]] [MASK máscara de red] 

Comando route  print sin parámetros para mostrar todo el contenido de la tabla de enrutamiento :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.050.png)

Si deseamos borrar la tabla de enrutamiento deberemos de utilizar el parámetro -f :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.051.png)

Además podemos añadir , rutas manuales de la siguiente manera :

→ route add IP\_Destino Mascara\_Destino Puerta\_de\_enlace métrica interfaz

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.052.png)

Si queremos cambiar una ruta , la sintaxis es la misma que el comando anterior cambiando la orden add por change :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.053.png)

Cuando solo queramos eliminar una ruta , utilizaremos la orden delete seguida del destino :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.054.png)


### ¿Cómo puedes averiguar la IP pública de tu router?

Hay muchas forma de saber esto desde Windows , podemos utilizar el  comando  curl para pedir la siguiente web y que nos devuelva la ip :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.055.png)

Otra forma desde la linea de comandos es hacer una consulta dns con nslookup al servicio opendns  :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.056.png)

Si tenemos un navegador podemos usar una de las muchas webs que nos dicen la dirección ip publica del router , yo uso  la siguiente <https://ipchicken.com/>  :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.057.jpeg)


## Linux

### Configurar una interfaz de red  

Para configurar una tarjeta de red en Linux podemos hacerlo desde la interfaz gráfica o desde linea de comandos .

Desde interfaz gráfica nos dirigimos a Configuración > Inalámbrica o Red . Una vez aquí encenderemos la tarjeta y le daremos al engranaje .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.058.jpeg)

Una vez aquí podemos configurar manualmente la configuración de red de nuestra tarjeta .

Esto  mismo  podremos  hacerlo  desde  la  linea  de  comandos  editando  el  fichero /etc/network/interfaces con permisos de superusuario .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.059.png)

Dentro de este podemos indicar la configuración de nuestros adaptadores de red , aquí te indico con lineas comentadas los parámetros básicos que podemos indicar en este archivo .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.060.png)

Una vez hayamos configurado nuestras interfaces los cambios no se aplicaran automáticamente , para hacer esto tenemos varias formas , la mas cómodas es reiniciar el servicio :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.061.png)

Otra forma de cambiar los servidores DNS que se utilizan es a través del fichero /etc/resolf.conf

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.062.png)

Aquí seguido de nameserver pondremos la dirección ip o nombre de nuestro servidor DNS

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.063.png)

### Uso general ifconfig

<a name="_page26_x56.70_y84.70"></a>**Explica la utilidad del comando ifconfig a partir de una captura real. ¿Hay alguna información de las que se obtiene con ipconfig /all que no aparezca? Trata de conseguirla de otra forma.**

Es similar a ifconfig y esta enfocado a las mismas funciones , este comando también se utiliza para ver, cambiar y administrar todas las configuraciones actuales de la red informática.

Esta se instala con el paquete net-tools , para instalarlo:

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.064.png)

Para utilizar esta herramienta necesitaremos hacerlo como superusuario , con su uso mas simple nos mostrara la configuración básica TCP/IP de  nuestra tarjeta de red así como unas estadísticas de la misma :

Por ejemplo con ipconfig /all podemos ver los servidores DNS configurados cosa que con ifconfig no podremos ver .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.065.png)

Así que tendremos que ver  el fichero /etc/resolf.conf

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.066.png)

Un uso común de este comando es configurar rápidamente una interfaz de red , por ejemplo :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.067.png)

Esto podemos ponerlo en una sola linea

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.068.png)

Además también podremos levantar y bajar la tarjeta de red 

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.069.png)

### Uso general dhclient

Este utiliza el protocolo de configuración dinámica de host para configurar dinámicamente los parámetros de red de la interfaz de red.

El siguiente comando indicará a dhclient que libere la concesión actual que tiene del servidor DHCP ,es decir que queremos liberar la ip actual . Utilizaremos los parámetros -r y -v 

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.070.png)

Si queremos volver a pedir una configuración de red al comando dhcp utilizaremos solamente el parámetro -v .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.071.png)

Principalmente este comando se usa para esto , para solucionar problemas con la configuración del servicio DHCP .

Algunos parámetros que no he mencionado y pueden resultar útil son :

- -6 : Sirve para indicar que quieres IPV6
- -p: Sirve para indicar otro puerto para hacer la consulta 
- -s : Sirve para indicar la dirección del servidor DHCP

### Diferencias de los comandos netstat y ping respecto a los empleados en Windows

netstat  muestra información sobre el subsistema de red en nuestro equipo al igual que Windows . Si nos fijamos en el manual nos indica que Esta aplicación está parcialmente obsoleta. El reemplazo de  netstat es  ss,  para  netstat  -r tiene ip route, para netstat -i puede usar ip -s link y para netstat -g dispone de ip maddr.

Si lanzamos el parámetro podemos ver a simple vista que nos muestra mas información sin indicar ningún parámetro , por lo demás estos son los mismo que en Windows .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.072.png)

Mientras que el comando ping la diferencia es que es por defecto infinito , a diferencia de Windows este no acabara hasta que lo detengamos nosotros .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.073.png)

En este los parámetros con respecto a Windows cambia su “letra ” , aquí serian :

- -i : Indicar el intervalo para enviar el siguiente paquete en segundos (por defecto es 1 )
- -s : Cambiar el tamaño del paquete en bytes 
- -f : inundación , para probar el rendimiento de la red bajo una carga pesada (envía una gran cantidad de paquetes lo más rápido posible)
- -c : Indicar el numero de trazas enviadas 
- -w: Dejara de imprimir los resultados después de los segundos indicados 
- -q: Elimina la salida del comando , opción silenciosa 
- -a : hace un sonido cuando hay una respuesta 
- -V indica la version del comando 

La utilidad de este sigue siendo la misma  , solucionar problemas de accesibilidad de hosts en una red. Esto nos ayuda a comprender por qué un sitio web no se carga.

### Uso general comando dig

Dig es un comando que permite realizar consultas a servidores DNS para obtener información relacionada con este servicio. Para instalarlo en nuestro sistema , haremos un apt install dnsutils .

Podemos hacer una consulta dns ,  por ejemplo al instituto para comprobar si somos capaces de obtener su dirección ip :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.074.jpeg)

Utilizando la opción +trace realiza consultas iterativas para resolver la búsqueda de nombres. Consultará los nombres de servidores a partir de la raíz y posteriormente atravesará el árbol del espacio de nombres mediante consultas iterativas siguiendo las referencias en el camino:

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.075.png)



También podemos realizar consultas inversas con la opción -x :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.076.png)

### Diferencias del comando traceroute de Linux con el comando tracert de Windows

La herramienta traceroute es exactamente la misma que el tracert, pero se denomina de otra forma, aunque internamente puede hacer uso de diferentes protocolos, ya que en algunos sistemas operativos se hace uso del protocolo ICMP Echo Request/reply, y en otros de hace uso de mensajes UDP directamente para comprobar cuantos saltos hay de un host a otro . 

Estas se usan para detectar donde esta el error a la hora de acceder a un determinado equipo y saber en que nodo se produce el “error” .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.077.jpeg)


Algunos parámetros que pueden interesarnos son :

- -f, :Establece la distancia entre el primer salto y el siguiente salto.
- -g,: nos permite indicar la puerta de enlace.
- -I : Usa ICMP ECHO 
- -m, :Establece el número de saltos; el valor predeterminado es 64.
- -M, :las rutas de seguimiento se realizan con ICMP o UDP; el método predeterminado es UDP.
- -p: Define el puerto de red; el valor predeterminado es 33434.
- -q: Define el  numero de  paquetes por salto.
- –resolve-hostnames: puede usar esta sintaxis para corregir los nombres de host.
- -w, : Define el tiempo de espera en segundos.

### Uso general wget

Wget es una herramienta informática creada por el Proyecto GNU. Puedes usarlo para recuperar contenido y archivos de varios servidores web. El nombre es una combinación de World Wide Web y la palabra get. Admite descargas a través de FTP, SFTP, HTTP y HTTPS.

Para instalarlo usamos el comando apt install wget .

Un ejemplo es para descargar archivos , por ejemplo una iso . Pondríamos el comando seguido de la url :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.078.png)

Este nos descargara el archivo en el directorio actual de trabajo .

Podemos utilizar el comando -o para indicar un nombre diferente al descargar el archivo :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.079.png)

Algunos parámetros interesantes son :

- -P : Indicar el directorio donde queremos guardar el archivos
- --limit-rate : sirve para limitar la velocidad de descarga 
- -tries : nos permite indicar el numero de reintentos de la descarga 
- -b : Realizara la descarga en segundo plano 
- -c para indicar que se reanude una descarga

Si quisiéramos descargar archivos desde un servidor ftp utilizaríamos la siguiente sintaxis : wget –ftp-user=usuario--ftp-password=contraseña

### Uso general de  tcpdump 

Tcpdump es una herramienta para línea de comandos cuya utilidad principal es analizar el tráfico que circula por la red. Permite al usuario capturar y mostrar en tiempo real los paquetes transmitidos y recibidos por la red a la cual el ordenador está conectado 

Los parámetros mas comunes son :

- -i  Permite especificar la interfaz de red en la que vamos a atender el tráfico. 
- -c <numero> Permite limitar la cantidad de paquetes capturados en un número determinado.
- -n Evita la resolución de puertos y direcciones ip a nombres. 
- -e Muestra las cabeceras ethernet además del paquete ip. 
- -t No imprime la estampa de tiempo de captura de cada paquete. 
- -x Muestra el contenido hexadecimal de la trama capturada. 
- -xx Idem a -x, pero además muestra el contenido de la cabecera Ethernet. 
- -X Muestra el contenido hexadecimal y en ASCII de la trama capturada. 
- -A Solo muesta el contenido ASCII del paquete capturado. 
- -s <numero> Muestra solo los primeros <numero> bytes desde el principio del paquete. 
- -vv Muestra información adicional, incluyendo parámetros de las cabeceras de protocolo. 
- -w file Permite guardar la salida en un archivo con formato pcap. 
- -r file Permite leer los paquetes previamente capturados y almacenados en un archivo pcap.

Por ejemplo podemos hacer una captura de nuestra red de un máximo de 50 paquetes :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.080.png)

Como ves la salida es indescifrable , para leerla usaremos el comando ngrep para buscar coincidencias sin tener en cuenta mayúsculas y minúsculas .

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.081.png)


### Uso general del comando arp

El comando arp nos permitirá  interactuar con la cache de resolución arp , modificándola por ejemplo .

También podemos averiguar la dirección MAC de un dispositivo , buscándolo en la tabla :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.082.png)

Los parámetros son los  mismo que podemos encontrar en Windows :

- -a : Encontrar una determinada dirección en la tabla 
- -v : Muestra todas las entradas 
- -n : Muestra todas las entradas de forma numérica 
- -d : elimina una resolución determinada 

También podemos hacer esto mismo con el comando ip :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.083.png)

Para este la sintaxis básica es  de la siguiente forma :

- add : Añadir resolución
- del : Eliminar resolución
- change : Cambiar una resolución 
- replace : Remplazar una resolución 

Por ejemplo para añadir una tabla :

![](../images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.084.png)

### Comando ip

Podremos ver y configurar direcciones IP, ver y configurar tablas de enrutamiento, ver y configurar túneles IP, y también ver y configurar la interfaz física .

Este se le añade un “segundo comando ” para indicar su funcion , son los siguientes :

- link: nos sirve para configurar las interfaces de red físicas o lógicas, por ejemplo, para ver el estado de todas las interfaces de red.
- address: permite ver y configurar las direcciones IPv4 y IPv6 asociadas a las diferentes interfaces de red. Cada interfaz debe tener al menos, una dirección IP configurada.
- addrlabel: permite añadir una etiqueta
- neighbour: permite ver los enlaces de vecindad, es decir, se puede ver la tabla ARP del sistema operativo.
- rule: permite ver y configurar políticas de enrutado y cambiarlas, esto se utiliza sobre todo cuando vas a configurar varias tablas de enrutamiento.
- route: permite ver y configurar las tablas de enrutamiento, tanto de la tabla de enrutamiento principal, como de las «secundarias» que configures.
- tunnel: permite ver los túneles IP y también configurarlos.
- maddr: permite ver y configurar las direcciones multienlace.
- mroute: permite ver y configurar la tabla de enrutamiento multicast.
- mrule: permite ver y configurar políticas de enrutamiento de direcciones multicast.
- monitor: permite monitorizar el estado de las tarjetas de red de manera continua, también direcciones IP y rutas.
- ntable: gestiona el caché de neighbour (ARP)
- tuntap: gestiona las interfaces TUN/TAP, orientado a las VPN como OpenVPN o WireGuard.
- maddress: configuración de las direcciones multicast
- xfrm: gestiona las políticas IPsec.
- netns: administrar espacios de nombres de red
- l2tp: configuración de L2TP
- tcp\_metrics: gestiona métricas TCP.
- token: gestiona los identificadores con token de las interfaces.

## Bibliografía

[Cambiar configuración TCP/IP ](https://support.microsoft.com/es-es/windows/cambiar-la-configuraci%C3%B3n-de-tcp-ip-bd0a07af-15f5-cd6a-363f-ca2b6f391ace#WindowsVersion=Windows_10)[Información general sobre comandos ](https://openwebinars.net/blog/20-comandos-de-red-mas-importantes-en-windows/)[Información protocolo ICMP](http://redesdecomputadores.umh.es/red/icmp/default.html#:~:text=Campos%20ICMP%3A%20Tipo%203%20C%C3%B3digo,en%20la%20ruta%20de%20origen.)

[Comando PING](https://apuntesjulio.com/como-usar-el-comando-ping/)

[Comando NSLOOKUP](https://axarnet.es/blog/que-es-nslookup)

[Descripción parámetros de los comandos ](http://trajano.us.es/~fornes/ARSSP/ComandosRedWindows.pdf)[Configuración red debian ](https://wiki.debian.org/es/NetworkConfiguration)

[Comando ifconfig](http://somebooks.es/comando-ifconfig-ubuntu/)

[Comando ip](https://www.redeszone.net/tutoriales/servidores/configurar-linux-comando-ip-iproute2-suite/)

