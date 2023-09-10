FRANCISCO JAVIER CRUCES DOVAL    PLANIFICACIÓN Y ADMINISTRACIÓN DE REDES

INSTALACIÓN DE WIRESHARK Y GNS3

![](resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.001.jpeg)

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.002.jpeg)

**Índice**

[1.Instalación de wireshark en Debian 11..............................................................................................3](#_page2_x56.70_y56.70)

1. [Introducción...............................................................................................................................3](#_page2_x56.70_y88.80)
1. [Descarga del paquete en debían.................................................................................................3](#_page2_x56.70_y506.75)
1. [Comprobación de funcionamiento.............................................................................................6](#_page5_x56.70_y56.70)
1. [Componentes de wireshark generales........................................................................................7](#_page6_x56.70_y56.70)

[2.Instalación de GNS3 en Debian 11....................................................................................................8](#_page7_x56.70_y68.70)

1. [Introducción...............................................................................................................................8](#_page7_x56.70_y100.80)
1. [Instalación en debian.................................................................................................................9](#_page8_x56.70_y66.70)
1. [Nuestra primera topología en GNS3........................................................................................12](#_page11_x56.70_y56.70)
1. [Acceso a internet a través de NAT en GNS3...........................................................................19](#_page18_x56.70_y66.70)

[3.Problemas comunes en la instalación..............................................................................................20](#_page19_x56.70_y68.70)

1. [Error VPCS executable version must be >=0.6.1 but not 0.8..................................................20](#_page19_x56.70_y100.80)
1. [Xterm no instalado...................................................................................................................22](#_page21_x56.70_y56.70)

[4 Instalar imágenes IOS......................................................................................................................22 ](#_page21_x56.70_y279.65)[5.Instalación en Windows de GNS3...................................................................................................27](#_page26_x56.70_y68.70)

1. [Paquetes necesarios para Windows.....................................................................................27](#_page26_x56.70_y97.80)
1. [Requisitos mínimos.............................................................................................................28](#_page27_x56.70_y63.70)
1. [Instalación GNS3................................................................................................................28](#_page27_x56.70_y262.95)
1. [Prueba de funcionamiento...................................................................................................41](#_page40_x56.70_y56.70)

[6.Instalación Wireshark en Windows.................................................................................................42](#_page41_x56.70_y56.70)

1. [Instalación...........................................................................................................................42](#_page41_x56.70_y85.80)
1. [Prueba de funcionamiento...................................................................................................47](#_page46_x56.70_y374.55)

[7.GNS VM..........................................................................................................................................48 ](#_page47_x56.70_y68.70)[Conclusión..........................................................................................................................................52 ](#_page51_x56.70_y68.70)[Bibliografía.........................................................................................................................................53](#_page52_x56.70_y68.70)

<a name="_page2_x56.70_y56.70"></a>**1.Instalación de wireshark en Debian 11**

1. **Introducción<a name="_page2_x56.70_y88.80"></a>** 

Wireshark es un analizador de protocolos utilizado para realizar análisis y solucionar problemas en redes de comunicaciones, para análisis de datos y protocolos, y como una herramienta didáctica. 

Añade una interfaz gráfica y muchas opciones de organización y filtrado de información. Así, permite ver todo el tráfico que pasa a través de una red estableciendo la configuración en modo promiscuo de nuestra tarjeta de red . También incluye una versión basada en texto llamada tshark.

Permite examinar datos o de un archivo de captura salvado en disco. Se puede analizar la información capturada, a través de los detalles y sumarios por cada paquete. Wireshark incluye un completo lenguaje para filtrar lo que queremos ver y la habilidad de mostrar el flujo reconstruido de una sesión de TCP.

Wireshark es software libre, y se ejecuta sobre la mayoría de sistemas operativos Unix y compatibles.

Los requisitos mínimos para utilizar este software son :

- Cualquier procesador moderno AMD64/x86-64 de 64 bits o x86 de 32 bits.
- 500 MB de RAM disponibles. Los archivos de captura más grandes requieren más RAM.
- 500 MB de espacio disponible en disco. Los archivos de captura requieren espacio en disco adicional.
- Cualquier pantalla moderna. Se recomienda una resolución de 1280 × 1024 o superior. Wireshark utilizará resoluciones HiDPI o Retina si están disponibles. Los usuarios avanzados encontrarán útiles varios monitores.
- Una tarjeta de red compatible para capturar
2. **Descarga<a name="_page2_x56.70_y506.75"></a> del paquete en debían** 

Para descargar el paquete en nuestro equipo deberemos de mirar en la [pagina oficial](https://www.wireshark.org/download.html) de descargas si incluye soporte para nuestro sistema operativo . 

Vemos que no aparece en la lista ningún sistema operativo GNU/Linux , esto es porque Wireshark está disponible a través del sistema de empaquetado predeterminado en la mayoría de estas plataformas . Es decir esta presente en los repositorios de nuestra distribución , en el caso de que no estuviese tenemos el código fuente al ser un software libre y podríamos compilarlo . 

Podemos comprobar si esta disponible en nuestro sistema operativo visitando la [pagina oficial](https://www.wireshark.org/download.html)  :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.003.jpeg)

Vemos que Debian aparece en la lista esto quiere decir que el paquete esta en los repositorios oficiales de debían.

En Debian contamos con el gestor de paquetes apt , así que podemos comprobar la versión del paquete disponible para la instalación y comprobar desde que repositorios se nos descargara con el siguiente comando : 

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.004.png)

Para realizar la instalación de wireshark introduciremos el siguiente comando : 

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.005.jpeg)

A continuación para hacer capturas de red  en el equipo necesitaremos permisos para nuestro usuario para ello  , utilizaremos el siguiente comando  :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.006.png)

3. **Comprobación<a name="_page5_x56.70_y56.70"></a> de funcionamiento** 

Ahora abriremos el programa para comprobar que todo funciona correctamente :

Ahora iniciaremos una captura de paquetes para ello si queremos hacerla sobre un interfaz en concreta pulsamos sobre ella , en mi caso usare la tarjeta de red inalámbrica wlo1  y haré una petición web  a ![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.007.jpeg)![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.008.jpeg)la pagina  jagger.es . 

Aquí te muestro la petición DNS que ha viajado desde  mi portátil hasta el router .

4. **Componentes<a name="_page6_x56.70_y56.70"></a> de wireshark generales** Wireshark hace uso de unos determinados paquetes :
- **Wireshark :** el analizador de protocolos de red que todos conocemos .
- **TShark :** un analizador de protocolo de red de línea de comandos.
- **Complementos y extensiones :** extras para los motores de disección Wireshark y TShark
- **Complementos Dissector :** complementos con algunas disecciones extendidas.
- **Complementos de estadísticas de árbol** -:Estadísticas extendidas.
- **Mate:** motor de seguimiento y meta análisis : extensiones configurables por el usuario del motor de filtro de pantalla; consulte el Capítulo 12, MATE para obtener más detalles.
- **MIB** de **SNMP**: MIB de SNMP para una disección de SNMP más detallada.
- **Herramientas :** herramientas de línea de comandos adicionales para trabajar con archivos de captura
- **Editcap :** lee un archivo de captura y escribe algunos o todos los paquetes en otro archivo de captura.
- **Text2Pcap :** lee un volcado hexadecimal ASCII y escribe los datos en un archivo de captura pcap.
- **Reordercap :** reordena un archivo de captura por marca de tiempo.
- **Mergecap :**  combina varios archivos de captura guardados en un único archivo de salida.
- **Capinfos :** proporciona información sobre los archivos de captura.
- **Rawshark** : filtro de paquetes sin procesar.
- **Guía del usuario :** instalación local de la Guía del usuario. Los botones de Ayuda en la mayoría de los cuadros de diálogo requerirán una conexión a Internet para mostrar las páginas de ayuda si la Guía del usuario no está instalada localmente.

<a name="_page7_x56.70_y68.70"></a>**2.Instalación de GNS3 en Debian 11**

1. **Introducción<a name="_page7_x56.70_y100.80"></a>** 

GNS3 es un simulador gráfico de red lanzado en 2008, que te permite diseñar topologías de red complejas y poner en marcha simulaciones sobre ellos,permitiendo la combinación de dispositivos tanto reales como virtuales.

Para permitir completar simulaciones, GNS3 está estrechamente vinculada con:

- **Dynamips:** un emulador de IOS que permite a los usuarios ejecutar imágenes de IOS .
- **Dynagen:** un front-end basado en texto para Dynamips .
- **Qemu** y **VirtualBox:** para permitir utilizar máquinas virtuales como un firewall PIX o estaciones de trabajo .
- **VPCS:** un emulador de PC con funciones básicas de networking .
- **IOU:** (IOS en Unix), compilaciones especiales de IOS provistas por Cisco para correr directamente en sistemas UNIX y derivados .

Los requisitos mínimos para hacer uso de esta herramienta son :

- **Procesador :** 2 o más núcleos lógicos
- **Virtualización:** Se requieren extensiones de virtualización. Es posible que deba habilitar esto a través del BIOS de su computadora.
- **Memoria  RAM:** 4 GB de RAM
- **Almacenamiento :** 1 GB de espacio disponible (la instalación de Windows es < 200 MB).
- **Notas adicionales :**  Es posible que necesite almacenamiento adicional para su sistema operativo y las imágenes del dispositivo.
2. **Instalación<a name="_page8_x56.70_y66.70"></a> en debian**

Lo primero que haremos antes de instalar sera comprobar que nuestro sistema este actualizado , para ello haremos un apt update y si tenemos paquetes desactualizados haremos un apt upgrade .

![ref1]

A continuación instalaremos todas las dependencias que necesita GNS3 :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.010.png)

Ahora te describiré la función de los paquetes que vamos a instalar :



|**Paquete**|**Descripción**|
| - | - |
|python3-pip|El módulo pip es el instalador de paquetes de Python.|
|python3-pyqt5|El módulo PyQt5 expone la API de Qt5 a Python 3 .|
|python3-pyqt5.qtsvg|El módulo SVG de PyQt5 proporciona clases para mostrar el contenido de los archivos SVG.|
|python3-pyqt5.qtwebsockets|El módulo WebSockets de PyQt5 proporciona enlaces de Python 3 para la especificación WebSockets (tanto cliente como servidor).|
|qemu|Software de Virtualización , actualmente se encuentra dividido en varios paquetes .|
|qemu-kvm|Binarios de emulación de sistema completo QEMU .|
|qemu-utils|Binario de utilidades de emulación de QEMU .|
|libvirt-clients|Libvirt es un conjunto de herramientas en C para interactuar con las capacidades de virtualización de versiones recientes de Linux .|
|libvirt-daemon-system|Este paquete contiene los archivos de configuración para ejecutar el demonio libvirt como un servicio del sistema.|
|Virtinst|Este paquete contiene algunas utilidades de línea de comandos para crear y editar máquinas virtuales .|
|wireshark|Es un analizador de red que captura paquetes para su posterior análisis .|
|xtightvncviewer|` `Sistema de visualización remota que le permite ver un entorno de 'escritorio' no solo en la máquina donde se está ejecutando, sino desde cualquier lugar en Internet .|
|apt-transport-https|Este es un paquete de transición ficticio: la compatibilidad con https .|
|ca-certificates|Contiene los certificados de las autoridades certificadoras que se incluyen en el navegador de Mozilla para permitir que las aplicaciones basadas en SSL .|
|curl|curl es una herramienta de línea de comandos para transferir datos con sintaxis URL .|
|gnupg2|Se puede utilizar para cifrar datos y crear firmas digitales. Incluye una función avanzada de administración de claves y cumple con el estándar de Internet OpenPGP propuesto.|
|software-properties-common|Le permite administrar fácilmente su distribución y las fuentes de software de proveedores de software independientes.|

Una vez instalados estos paquetes , nos descargaremos GNS3 utilizando pip3 :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.011.png)

Además nos fijaremos en la salida del comando para comprobar si hay algún error :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.012.png)

Lo siguiente sera instalar docker , el cual nos permitirá crear contenedores . Para ello importaremos su clave GPG para que nuestro sistema confié en el :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.013.png)

Lo siguiente sera añadir el repositorio a nuestro sistema para ello utilizaremos el siguiente comando:

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.014.png)

Actualizaremos los repositorios que utiliza apt haciendo un apt update :

![ref1]

Y finalmente podremos instalar docker :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.015.png)

Agregue las siguientes líneas a su /etc/apt/sources.list , para que podamos instalar dynamips y  ubridge:

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.016.png)

Para poder instalar los paquetes necesarios de estos repositorios , añadiremos las claves gpg del mismo :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.017.png)

Actualizaremos los repositorios que utiliza apt haciendo un apt update :

![ref1]

Nos instalaremos los paquetes Dynamips y ubridge :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.018.png)

Saldrá un recuadro como este , para indicar si los usuarios que no son superusuarios pueden capturar paquetes , le diremos que si en nuestro caso :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.019.jpeg)

Para evitar la instalación accidental de cualquier otra cosa de ese repositorio (por ahora), elimine o comente esas dos líneas en su archivo /etc/apt/sources.list y haga un apt update:

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.020.png)

![ref1]

También podemos eliminar la clave GPG de estos repositorios si lo deseamos :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.021.png)

Añadiremos a los usuarios que vayan a utilizar la herramienta a los siguientes grupos :

Reinicie su sesión de usuario cerrando sesión y volviendo a iniciarla, o reiniciando el sistema para que se apliquen estos cambios .![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.022.png)

3. **Nuestra<a name="_page11_x56.70_y56.70"></a> primera topología en GNS3**

Una vez reiniciado el sistema iniciaremos la aplicación , y nos saldrá un recuadro como este :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.023.png)

Aquí indicaremos que voy a correr las aplicaciones localmente en mi maquina .A continuación seleccionaremos la ruta del servidor , el nombre de host y el puerto asociado :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.024.png)

Si todo ha sido correcto , nos dirá que se ha realizado correctamente :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.025.png)

Cuando abramos el programa , nos dará opción a crear un proyecto o podemos crear uno nuevo , en mi caso creare uno :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.026.jpeg)Si nos fijamos en la parte izquierda del programa veremos los siguientes símbolos que sirven para lo siguiente :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.027.png)

Añadiremos arrastrando 2 VPCS :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.028.png)

Le añadiremos un  Ethernet swicht :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.029.png)

Haremos clic en el botón Agregar un enlace para dejar de agregar enlaces , nos quedaría así el escenario :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.030.png)

Podemos hacer visible la interfaz a la cual los hemos conectado pulsando en el siguiente botón :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.031.png)El botón verde "Reproducir" en la barra de herramientas GNS3 encenderá todos los dispositivos en la topología, mientras que el botón amarillo "Pausa" los suspenderá y el botón rojo "Detener" apagará todo en la topología:

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.032.png)

Nos saldrá una advertencia , para que confirmemos si queremos añadir todos los dispositivos , le daremos a si :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.033.png)

Veremos que tanto a la izquierda en el resumen de dispositivos como en las conexiones salientes de los dispositivos su “luz” de estado a cambiado de rojo a verde , puestos que estos ahora están encendidos :

` `![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.034.png)![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.035.png)

Ahora abriremos una terminal en todos nuestros VPCS , con el siguiente botón :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.036.png)

A través de estas terminales le asignaremos direcciones ips a nuestros dispositivos con el siguiente comando :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.037.png) ![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.038.png)

Una vez configurada las tarjetas de red , comprobaremos si hay conectividad entre ellos haciendo un ping :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.039.png)

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.040.png)

Añadiremos un tercer VPCS a nuestro esquema :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.041.png)Lo encenderemos y abriremos una terminal para configurarlo al igual que hemos hecho con los anteriores :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.042.png)

Y comprobare que esta nueva maquina tiene conectividad con las anteriores :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.043.png)

Si queremos que se guarden las configuraciones de nuestros equipos introduciremos el comando save :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.044.png)

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.045.png)

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.046.png)

4. **Acceso<a name="_page18_x56.70_y66.70"></a> a internet a través de NAT en GNS3**

La manera mas fácil de conseguir acceso a internet es a través de la nube NAT .

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.047.png)

Esta cuenta con acceso a internet , así como un servicio DHCP corriendo con IPV4 .Para hacer uso de ella , la pondremos en nuestro escenario y la conectaremos en un swicht . 

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.048.png)

A continuación si queremos salir a internet , tendremos que configurar nuestros clientes para que estos obtengan la configuración de red adecuada . Aprovecharemos que tenemos un servidor DHCP .

Para que los clientes se configuren a través de este servicio introduciremos el comando dhcp :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.049.png)

Probaremos a hacer un ping a google.es para comprobar la conectividad :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.050.png)

<a name="_page19_x56.70_y68.70"></a>**3.Problemas comunes en la instalación** 

1. **Error<a name="_page19_x56.70_y100.80"></a> VPCS executable version must be >=0.6.1 but not 0.8**

Este error viene al hacer la instalación de los VPCS , se descarga de los repositorios una versión que no admite actualmente el programa . 

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.051.png)

Por suerte es muy fácil de solucionar , accederemos al [repositorio](https://github.com/GNS3/vpcs/releases) del desarrollador en github y nos descargaremos el siguiente paquete :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.052.jpeg)

Una vez descargado lo descomprimiremos usando el siguiente comando : 

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.053.png)

Donde hagamos este comando nos creara un directorio en el cual accederemos para compilar el programa :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.054.png)

Ejecutaremos el siguiente script :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.055.png)

Nos creara en esta ruta el directorio vpcs , este tendremos que añadirlo en gns3 :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.056.png)

Accederemos a gns3 , pulsaremos *CTRL + SHIFT + P* para acceder al panel de preferencias . Una vez aquí nos desplazamos al apartado de las vpcs y seleccionamos la ruta del directorio que acabamos de generar :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.057.jpeg)

Aplicamos los cambios y ya podríamos utilizar las vpcs .

2. **Xterm<a name="_page21_x56.70_y56.70"></a> no instalado**

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.058.png)

Este error aparece cuando queremos acceder a una consola de un dispositivo de nuestra tipología de red .Para solucionar este problema lo primero es cerrar GNS3 y a continuación dirigirnos a una terminal para descargarlo, utilizaremos el siguiente comando :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.059.png)

Volveremos a abrir el programa y podremos acceder a las consolas de nuestras maquinas .

<a name="_page21_x56.70_y279.65"></a>**4 Instalar imágenes IOS**

Si queremos añadir a nuestro sistema hardware real como puede ser un router cisco por ejemplo deberemos de acceder a la pagina oficial de GNS3 y descargar concretamente el que deseemos añadir en mi caso añadiré un cisco 3725 .![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.060.jpeg)

Si pulsamos sobre el botón de descarga  nos descargara un archivo con extensión , el cual es una plantilla .

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.061.png)

Si nos fijamos en este caso no tenemos la posibilidad de descargar la imagen desde este repositorio , nos dice que no hay link disponible . Para estos casos existe un repositorio de cisco el cual tiene todas las imágenes de sus productos –>  tfr.org/cisco-ios

Para saber cual nos tenemos que traer de aquí , abriremos gns3 y a través del menú superior izquierdo pulsaremos sobre el apartado file > import appilance   , seleccionaremos la plantilla que vamos a importar . Le daremos a instalar en nuestro ordenador local :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.062.jpeg)

Una vez aquí nos , veremos el nombre del  archivo   y lo buscaremos en el repositorio externo , ya que podemos observar que no se encuentra el archivo

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.063.png)

En este caso descargare , esta version que coincide con la plantilla que he descargado :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.064.png)Cuando hayamos hecho esto tendremos el siguiente problema , las firmas de las imágenes no coincidirán para paliar ese paso marcaremos la opción allow custom files en la parte inferior y importaremos el binario que acabamos de descargar :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.065.png)

Nos informara  que para la plantilla seleccionada , el archivo que hemos descargado del repositorio no coinciden los hashes . En nuestro caso es normal ya que la imagen no es la misma que tendría que venir con la plantilla , así que aceptaremos los riesgos .

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.066.png)Veremos que cambiara el estado a listo para instalar , así que le daremos a siguiente en la parte inferior .

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.067.png)

Nos pedirá confirmación para añadir nuestro dispositivo , confirmaremos la acción :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.068.png)

Nos informara de que nuestro  dispositivo se ha añadido en las plantillas de los router , para este caso .

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.069.png)

Además nos informara del nombre que se le ha asignado .

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.070.png)

Como nos indico , lo encontraremos en la sección de routers :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.071.png)

Ahora haremos una pequeña prueba de funcionamiento , lo añadiremos a nuestro escenario y comprobaremos que podemos arrancarlo y conectarnos a la consola :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.072.png)

` `Veremos la conexión a la consola es correcta :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.073.png)

<a name="_page26_x56.70_y68.70"></a>**5.Instalación en Windows  de GNS3**

1. **Paquetes<a name="_page26_x56.70_y97.80"></a> necesarios para Windows**

Aunque tengamos instalado el software de GNS3 este hará uso de paquetes adicionales para realizar algunas  funciones  o  incluso  añadir  nuevas  funcionalidades  como  emular  enrutadores  de determinados fabricantes . 



|**Artículo**|**Requerido**|**Descripción**|
| - | - | - |
|WinPCAP|Requerido|Requerido para conectar GNS3 a su red informática. Utilizado por los nodos Cloud y NAT para permitir que sus proyectos se comuniquen con el mundo exterior.|
|Npcap|Opcional|El reemplazo moderno de WinPCAP sabe solucionar problemas  pero está menos probado que WinPCAP.Instale Npcap con la opción "Modo compatible con la API de WinPcap" seleccionada, si se usa sin WinPcap.Npcap puede coexistir con WinPcap, si esa opción *no* está seleccionada.|
|Wireshark|Recomendado|Le permite capturar y ver el tráfico de red enviado entre nodos.|
|Dynamips|Requerido|Requerido para ejecutar una instalación local de GNS3 con enrutadores Cisco.|
|QEMU 3.1.0 y 0.11.0|Opcional|<p>Un software de virtualización .La versión anterior de Qemu </p><p>0\.11.0 está instalada para admitir dispositivos ASA antiguos. Se recomienda utilizar la vm GNS3 en su lugar.</p>|
|VPCS|Recomendado|Un emulador de PC muy ligero que admite comandos básicos como ping y traceroute|
|Cpulimit|Opcional|Se usa para evitar que QEMU use el 100% de su CPU (cuando se está ejecutando) en algunos casos, como con los dispositivos ASA antiguos|
|GNS3|Requerido|El software principal de GNS3.Esto siempre es obligatorio.|
|Visor TightVNC|Recomendado|Un cliente VNC utilizado para conectarse a las interfaces gráficas de usuario del dispositivo.|
|Solar-Putty|Recomendado|La nueva aplicación de consola predeterminada.|
|Virt-viewer|Recomendado|Visualizador alternativo de máquinas virtuales de escritorio Qemu que tienen qemu-spice preinstalado.|
|Intel Hardware Acceleration Manager (HAXM)|Opcional|Solo disponible en sistemas con CPU Intel (y VT-X habilitado), que *no* usan Hyper-V. Se utiliza para la aceleración de hardware de la emulación de Android, así como para QEMU.|

2. **Requisitos<a name="_page27_x56.70_y63.70"></a>  mínimos** 

Para entornos pequeños en Windows  los desarrolladores exigen  tener como mínimo las siguientes características  :

|**Características** |**Requisitos**|
| - | - |
|Sistema operativo|Windows 7 (64 bits) o posterior|
|Procesador|2 o más núcleos lógicos|
|Virtualización|Se requieren extensiones de virtualización. Es posible que deba habilitar esto a través del BIOS de su ordenador .|
|Memoria|4 GB de RAM|
|Almacenamiento|1 GB de espacio disponible (la instalación de Windows es < 200 MB).|

3. **Instalación<a name="_page27_x56.70_y262.95"></a> GNS3**

Lo primero que tendremos que sera descargarnos el ejecutable oficial de su pagina web , para ello tendremos que estar registrados previamente .

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.074.jpeg)

Lanzaremos el ejecutable y nos pedirá permisos de administrados , se los concedemos :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.075.png)

Saldrá una pantalla informándonos sobre el producto , le damos a next .

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.076.png)

A continuación deberemos de aceptar los términos y licencias de uso :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.077.png)

Nos preguntara donde queremos crear los atajos del programa , lo dejare por defecto ya que asi los añadirá al escritorio :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.078.png)A continuación debemos de prestar atención ya que debemos de seleccionar instalación local y todos los paquetes que vayamos a hacer uso , si hubiésemos instalado antes  alguno de ellos los desmarcamos (Los mencionados en el punto 5.1) :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.079.png)

Seleccionaremos la ruta donde se instalara el programa , yo dejare la predeterminada . También nos informa el espacio que necesitara la instalación  :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.080.png)

Esperaremos a que se realice la instalación :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.081.png)

**Instalación WinCap**

Requerido para conectar GNS3 a su red informática. Utilizado por los nodos Cloud y NAT para permitir que sus proyectos se comuniquen con el mundo exterior.

Mientras se realiza la instalación de GNS3 comenzara la instalación de todos los programas que hemos marcado anteriormente .

Nos mostrara información sobre el programa esta primera ventana así que le damos a siguiente :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.082.png)

Aceptamos la licencia de términos y uso :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.083.png)

Marcamos la opción para que arranque automáticamente el driver y le damos a instalar 

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.084.png)

Nos informa de que la instalación a sido correcta y cerramos la ventana :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.085.png)

**Instalación Ncap** 

El reemplazo moderno de WinPCAP sabe solucionar problemas  pero está menos probado que WinPCAP.Instale Npcap con la opción "Modo compatible con la API de WinPcap" seleccionada, si se usa sin WinPcap.Npcap puede coexistir con WinPcap, si esa opción no está seleccionada.

Otra vez el mismo proceso , aceptamos los términos y licencias de uso .

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.086.png)

Dejamos la opción marcada por defecto y le damos a install 

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.087.png)

Cuando finalice la instalación le damos a siguiente :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.088.png)

Y cerramos el instalador :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.089.png)Volvemos a GNS3 ya que el proceso de instalación ha quedado detenido mientras hemos instalado los componentes que va a hacer uso , esta se reanuda automáticamente  :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.090.png)

Una vez finalice la instalación  , le damos a siguiente 

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.091.png)

GNS3  nos ofrece una licencia gratuita de Solarwinds , le daremos a si :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.092.png)

Habremos finalizado correctamente la instalación de GNS3

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.093.png)

Abriremos el programa y seleccionaremos correr los dispositivos en nuestra maquina local :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.094.png)

Aquí configuraremos nuestro servidor local de GNS3 

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.095.png)Anteriormente lo deje por defecto , si nuestra configuración es correcta nos dirá que la conexión se ha realizado satisfactoriamente :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.096.png)

Nos mostrara un resumen de la configuración dada anteriormente :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.097.png)

4. **Prueba<a name="_page40_x56.70_y56.70"></a> de funcionamiento** 

Montaremos el mismo escenario que en debian para comprobar su funcionamiento , el proceso es el mismo .

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.098.jpeg)

Configuraremos las direcciones ips de las maquinas y comprobamos que tengan conectividad  a través de solarputty .

PC1 :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.099.png)

PC2:

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.100.png)

Podemos observar que ambos equipos tienen conectividad a través del escenario .

<a name="_page41_x56.70_y56.70"></a>**6.Instalación Wireshark en Windows**

1. **Instalación**

<a name="_page41_x56.70_y85.80"></a>La instalación de este producto es muy sencilla , si hemos instalado GNS3 anteriormente y hemos marcado la casilla de este , se nos habrá instalado automáticamente .

Por el contrario si partimos desde cero podemos hacer su instalación , bajandonoslo de su sitio web oficial :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.101.jpeg)

Cuando abramos el instalador nos pedirá permisos de administrador , se lo concedemos :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.102.png)

Si al igual que yo lo has instalado con GNS3 nos detectara que ya existe una instalaron , así que yo la cancelare . 

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.103.png)

Si no lo tuviésemos la instalación es idéntica a cualquier programa que hemos instalado en la practica . Aquí te lo muestro , lo primero que veras sera una pantalla informativa del ejecutable :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.104.png)

Al igual que todos los programas te pedirá que aceptes los términos y condiciones de uso :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.105.png)

Seleccionaremos los productos que deseemos instalar en mi caso todos :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.106.png)

Además nos preguntara que accesos directos y donde los queremos crear 

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.107.png)

Seleccionaremos la ruta donde queremos que se instale :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.108.png)

Seleccionaremos si nos interesa el paquete Ncap .(Lo hemos instalado con GNS3)

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.109.png)A continuación nos preguntara para instalar la extensión que nos permite analizar trafico USB , en mi caso la desmarcare ya que no me interesa .

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.110.png)

Esperaremos a que finalice la instalación y le daremos a siguiente :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.111.png)

Nos informara de que la instalación ha sido realizada correctamente :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.112.png)

2. **Prueba<a name="_page46_x56.70_y374.55"></a> de funcionamiento ![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.113.jpeg)**

He realizado una petición DNS a [www.sevillafc.es](http://www.sevillafc.es/) y aquí podemos ver la consulta DNS :

<a name="_page47_x56.70_y68.70"></a>**7.GNS VM** 

Si queremos desplegar maquinas virtuales en una instancia virtual desplegaremos la maquina virtual que nos da GNS3 para que este lleve la carga de la Virtualización .

Nos descargaremos la OVA desde la pagina web oficial 

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.114.png)

Una vez descargada la importaremos en Vmware y le daremos las características hardware que consideremos oportuno :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.115.png)

Una  vez echo esto abriremos GNS3 y editaremos las preferencias de GNS VM y seleccionaremos la maquina virtual que acabamos de importar :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.116.jpeg)

Se  nos iniciara la maquina virtual y podremos ver los datos de la misma en la pestaña info :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.117.png)

Lanzaremos el set-up wizard desde la pestaña help de GNS3 y seleccionaremos la opción de ejecutar las apilances en una maquina virtual :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.118.png)

Seleccionaremos la configuración de nuestra maquina virtual :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.119.png)

Seleccionaremos de nuevo nuestra maquina virtual y las características hardware que deseemos  :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.120.jpeg)Solo nos quedara importar los dispositivos en la maquina virtual , esto se hace igual que hemos echo anteriormente cambiando el sitio donde lo importamos :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.121.jpeg)

Si queremos ver donde se ejecutara un dispositivo podemos verlo a través de preferencias :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.122.jpeg)

Además podemos ver en apartado servers sumarry el consumo de recursos de nuestras maquinas :

![](/resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.123.png)

<a name="_page51_x56.70_y68.70"></a>**Conclusión** 

Podemos ver que la instalación es infinitamente mas cómoda en Windows  ya que automáticamente te instala las dependencias, siendo la típica instalación de “siguiente a siguiente ” .

Además en Windows al acabar la instalación el producto estaba listo para usarse y  no he sufrido ningún error  al iniciar el programa ni al usar sus características como si me ha pasado en Debian .

<a name="_page52_x56.70_y68.70"></a>**Bibliografía** 

[Documentacion oficial wireshark](https://www.wireshark.org/docs/wsug_html_chunked/ChBuildInstallWinInstall.html)

[Paquete wireshark en debian](https://packages.qa.debian.org/w/wireshark.html)

[Requisitos mínimos wireshark](https://www.wireshark.org/docs/wsug_html_chunked/ChIntroPlatforms.html)

[Error “VPCS executable version must be >=0.6.1 but not 0.8” ](https://gns3.com/vpcs-executable-version-must-be-greater-than-0-6-1-but-not-0-8)[Descarga VPCS](https://github.com/GNS3/vpcs/releases)
53

[ref1]: resources/_gen/images/posts/category/redes/Practica3InstalacionGNS3.009.png
