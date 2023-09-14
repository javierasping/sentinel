---
title: "Instalacion GNS3 y Wireshark"
date: 2023-09-08T10:00:00+00:00
description: Descripción de tu publicación.
tags: [Redes, Wireshark, GNS3]
hero: images/gato.webp
---

![1](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.001.jpeg)


![2](/assets/images/gato.webp)

![7](../instalacion_wireshark_gns3/images/gato.jpg)










<!-- 
## Índice

[1.Instalación de wireshark en Debian 11](#_page2_x56.70_y56.70)

1. [Introducción](#_page2_x56.70_y88.80)
1. [Descarga del paquete en debían](#_page2_x56.70_y506.75)
1. [Comprobación de funcionamiento](#_page5_x56.70_y56.70)
1. [Componentes de wireshark generales](#_page6_x56.70_y56.70)

[2.Instalación de GNS3 en Debian 11](#_page7_x56.70_y68.70)

1. [Introducción](#_page7_x56.70_y100.80)
1. [Instalación en debian](#_page8_x56.70_y66.70)
1. [Nuestra primera topología en GNS3](#_page11_x56.70_y56.70)
1. [Acceso a internet a través de NAT en GNS3](#_page18_x56.70_y66.70)

[3.Problemas comunes en la instalación](#_page19_x56.70_y68.70)

1. [Error VPCS executable version must be >=0.6.1 but not 0.8](#_page19_x56.70_y100.80)
1. [Xterm no instalado](#_page21_x56.70_y56.70)

[4 Instalar imágenes IOS](#_page21_x56.70_y279.65)

[5.Instalación en Windows de GNS3](#_page26_x56.70_y68.70)

1. [Paquetes necesarios para Windows](#_page26_x56.70_y97.80)
1. [Requisitos mínimos](#_page27_x56.70_y63.70)
1. [Instalación GNS3](#_page27_x56.70_y262.95)
1. [Prueba de funcionamiento](#_page40_x56.70_y56.70)

[6.Instalación Wireshark en Windows](#_page41_x56.70_y56.70)

1. [Instalación](#_page41_x56.70_y85.80)
1. [Prueba de funcionamiento](#_page46_x56.70_y374.55)

[7.GNS VM](#_page47_x56.70_y68.70)

[Conclusión](#_page51_x56.70_y68.70)

[Bibliografía](#_page52_x56.70_y68.70) -->


## 1. **Introducción**

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

### 1.1 **Descarga del paquete en debían** 

Para descargar el paquete en nuestro equipo deberemos de mirar en la [pagina oficial](https://www.wireshark.org/download.html) de descargas si incluye soporte para nuestro sistema operativo . 

Vemos que no aparece en la lista ningún sistema operativo GNU/Linux , esto es porque Wireshark está disponible a través del sistema de empaquetado predeterminado en la mayoría de estas plataformas . Es decir esta presente en los repositorios de nuestra distribución , en el caso de que no estuviese tenemos el código fuente al ser un software libre y podríamos compilarlo . 

Podemos comprobar si esta disponible en nuestro sistema operativo visitando la [pagina oficial](https://www.wireshark.org/download.html)  :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.003.jpeg)

Vemos que Debian aparece en la lista esto quiere decir que el paquete esta en los repositorios oficiales de debían.

En Debian contamos con el gestor de paquetes apt , así que podemos comprobar la versión del paquete disponible para la instalación y comprobar desde que repositorios se nos descargara con el siguiente comando : 

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.004.png)

Para realizar la instalación de wireshark introduciremos el siguiente comando : 

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.005.jpeg)

A continuación para hacer capturas de red  en el equipo necesitaremos permisos para nuestro usuario para ello  , utilizaremos el siguiente comando  :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.006.png)

### 1.2 **Comprobación de funcionamiento** 

Ahora abriremos el programa para comprobar que todo funciona correctamente :

Ahora iniciaremos una captura de paquetes para ello si queremos hacerla sobre un interfaz en concreta pulsamos sobre ella , en mi caso usare la tarjeta de red inalámbrica wlo1  y haré una petición web  a la pagina  jagger.es . 

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.007.jpeg)

Aquí te muestro la petición DNS que ha viajado desde  mi portátil hasta el router .


![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.008.jpeg)




### 1.3 **Componentes de wireshark generales** Wireshark hace uso de unos determinados paquetes :
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

## 2 **Instalación de GNS3 en Debian 11**

### 2.1 **Introducción** 

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

### 2.2 **Instalación**

Lo primero que haremos antes de instalar sera comprobar que nuestro sistema este actualizado , para ello haremos un apt update y si tenemos paquetes desactualizados haremos un apt upgrade .


A continuación instalaremos todas las dependencias que necesita GNS3 :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.010.png)

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

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.011.png)

Además nos fijaremos en la salida del comando para comprobar si hay algún error :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.012.png)

Lo siguiente sera instalar docker , el cual nos permitirá crear contenedores . Para ello importaremos su clave GPG para que nuestro sistema confié en el :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.013.png)

Lo siguiente sera añadir el repositorio a nuestro sistema para ello utilizaremos el siguiente comando:

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.014.png)

Actualizaremos los repositorios que utiliza apt haciendo un apt update :


Y finalmente podremos instalar docker :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.015.png)

Agregue las siguientes líneas a su /etc/apt/sources.list , para que podamos instalar dynamips y  ubridge:

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.016.png)

Para poder instalar los paquetes necesarios de estos repositorios , añadiremos las claves gpg del mismo :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.017.png)

Actualizaremos los repositorios que utiliza apt haciendo un apt update :


Nos instalaremos los paquetes Dynamips y ubridge :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.018.png)

Saldrá un recuadro como este , para indicar si los usuarios que no son superusuarios pueden capturar paquetes , le diremos que si en nuestro caso :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.019.jpeg)

Para evitar la instalación accidental de cualquier otra cosa de ese repositorio (por ahora), elimine o comente esas dos líneas en su archivo /etc/apt/sources.list y haga un apt update:

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.020.png)


También podemos eliminar la clave GPG de estos repositorios si lo deseamos :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.021.png)

Añadiremos a los usuarios que vayan a utilizar la herramienta a los siguientes grupos :

Reinicie su sesión de usuario cerrando sesión y volviendo a iniciarla, o reiniciando el sistema para que se apliquen estos cambios .

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.022.png)

### 2.3 **Nuestra primera topología en GNS3**

Una vez reiniciado el sistema iniciaremos la aplicación , y nos saldrá un recuadro como este :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.023.png)

Aquí indicaremos que voy a correr las aplicaciones localmente en mi maquina .A continuación seleccionaremos la ruta del servidor , el nombre de host y el puerto asociado :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.024.png)

Si todo ha sido correcto , nos dirá que se ha realizado correctamente :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.025.png)

Cuando abramos el programa , nos dará opción a crear un proyecto o podemos crear uno nuevo , en mi caso creare uno :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.026.jpeg)Si nos fijamos en la parte izquierda del programa veremos los siguientes símbolos que sirven para lo siguiente :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.027.png)

Añadiremos arrastrando 2 VPCS :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.028.png)

Le añadiremos un  Ethernet swicht :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.029.png)

Haremos clic en el botón Agregar un enlace para dejar de agregar enlaces , nos quedaría así el escenario :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.030.png)

Podemos hacer visible la interfaz a la cual los hemos conectado pulsando en el siguiente botón :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.031.png)El botón verde "Reproducir" en la barra de herramientas GNS3 encenderá todos los dispositivos en la topología, mientras que el botón amarillo "Pausa" los suspenderá y el botón rojo "Detener" apagará todo en la topología:

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.032.png)

Nos saldrá una advertencia , para que confirmemos si queremos añadir todos los dispositivos , le daremos a si :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.033.png)

Veremos que tanto a la izquierda en el resumen de dispositivos como en las conexiones salientes de los dispositivos su “luz” de estado a cambiado de rojo a verde , puestos que estos ahora están encendidos :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.034.png)

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.035.png)

Ahora abriremos una terminal en todos nuestros VPCS , con el siguiente botón :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.036.png)

A través de estas terminales le asignaremos direcciones ips a nuestros dispositivos con el siguiente comando :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.037.png) 

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.038.png)

Una vez configurada las tarjetas de red , comprobaremos si hay conectividad entre ellos haciendo un ping :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.039.png)

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.040.png)

Añadiremos un tercer VPCS a nuestro esquema :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.041.png)

Lo encenderemos y abriremos una terminal para configurarlo al igual que hemos hecho con los anteriores :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.042.png)

Y comprobare que esta nueva maquina tiene conectividad con las anteriores :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.043.png)

Si queremos que se guarden las configuraciones de nuestros equipos introduciremos el comando save :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.044.png)

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.045.png)

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.046.png)

## 2.4 **Acceso a internet a través de NAT en GNS3**

La manera mas fácil de conseguir acceso a internet es a través de la nube NAT .

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.047.png)

Esta cuenta con acceso a internet , así como un servicio DHCP corriendo con IPV4 .Para hacer uso de ella , la pondremos en nuestro escenario y la conectaremos en un swicht . 

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.048.png)

A continuación si queremos salir a internet , tendremos que configurar nuestros clientes para que estos obtengan la configuración de red adecuada . Aprovecharemos que tenemos un servidor DHCP .

Para que los clientes se configuren a través de este servicio introduciremos el comando dhcp :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.049.png)

Probaremos a hacer un ping a google.es para comprobar la conectividad :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.050.png)

## 3 **Problemas comunes en la instalación** 

### 3.1 **Error VPCS executable version must be >=0.6.1 but not 0.8**

Este error viene al hacer la instalación de los VPCS , se descarga de los repositorios una versión que no admite actualmente el programa . 

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.051.png)

Por suerte es muy fácil de solucionar , accederemos al [repositorio](https://github.com/GNS3/vpcs/releases) del desarrollador en github y nos descargaremos el siguiente paquete :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.052.jpeg)

Una vez descargado lo descomprimiremos usando el siguiente comando : 

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.053.png)

Donde hagamos este comando nos creara un directorio en el cual accederemos para compilar el programa :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.054.png)

Ejecutaremos el siguiente script :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.055.png)

Nos creara en esta ruta el directorio vpcs , este tendremos que añadirlo en gns3 :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.056.png)

Accederemos a gns3 , pulsaremos *CTRL + SHIFT + P* para acceder al panel de preferencias . Una vez aquí nos desplazamos al apartado de las vpcs y seleccionamos la ruta del directorio que acabamos de generar :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.057.jpeg)

Aplicamos los cambios y ya podríamos utilizar las vpcs .

### 3.2 **Xterm no instalado**

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.058.png)

Este error aparece cuando queremos acceder a una consola de un dispositivo de nuestra tipología de red .Para solucionar este problema lo primero es cerrar GNS3 y a continuación dirigirnos a una terminal para descargarlo, utilizaremos el siguiente comando :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.059.png)

Volveremos a abrir el programa y podremos acceder a las consolas de nuestras maquinas .

## 4 **Instalar imágenes IOS**

Si queremos añadir a nuestro sistema hardware real como puede ser un router cisco por ejemplo deberemos de acceder a la pagina oficial de GNS3 y descargar concretamente el que deseemos añadir en mi caso añadiré un cisco 3725 .

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.060.jpeg)

Si pulsamos sobre el botón de descarga  nos descargara un archivo con extensión , el cual es una plantilla .

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.061.png)

Si nos fijamos en este caso no tenemos la posibilidad de descargar la imagen desde este repositorio , nos dice que no hay link disponible . Para estos casos existe un repositorio de cisco el cual tiene todas las imágenes de sus productos –>  tfr.org/cisco-ios

Para saber cual nos tenemos que traer de aquí , abriremos gns3 y a través del menú superior izquierdo pulsaremos sobre el apartado file > import appilance   , seleccionaremos la plantilla que vamos a importar . Le daremos a instalar en nuestro ordenador local :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.062.jpeg)

Una vez aquí nos , veremos el nombre del  archivo   y lo buscaremos en el repositorio externo , ya que podemos observar que no se encuentra el archivo

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.063.png)

En este caso descargare , esta version que coincide con la plantilla que he descargado :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.064.png)

Cuando hayamos hecho esto tendremos el siguiente problema , las firmas de las imágenes no coincidirán para paliar ese paso marcaremos la opción allow custom files en la parte inferior y importaremos el binario que acabamos de descargar :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.065.png)

Nos informara  que para la plantilla seleccionada , el archivo que hemos descargado del repositorio no coinciden los hashes . En nuestro caso es normal ya que la imagen no es la misma que tendría que venir con la plantilla , así que aceptaremos los riesgos .

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.066.png)

Veremos que cambiara el estado a listo para instalar , así que le daremos a siguiente en la parte inferior .

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.067.png)

Nos pedirá confirmación para añadir nuestro dispositivo , confirmaremos la acción :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.068.png)

Nos informara de que nuestro  dispositivo se ha añadido en las plantillas de los router , para este caso .

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.069.png)

Además nos informara del nombre que se le ha asignado .

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.070.png)

Como nos indico , lo encontraremos en la sección de routers :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.071.png)

Ahora haremos una pequeña prueba de funcionamiento , lo añadiremos a nuestro escenario y comprobaremos que podemos arrancarlo y conectarnos a la consola :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.072.png)

` `Veremos la conexión a la consola es correcta :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.073.png)

## 5 **Instalación en Windows  de GNS3**

### 5.1 **Paquetes necesarios para Windows**

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

### 5.2. **Requisitos mínimos** 

Para entornos pequeños en Windows  los desarrolladores exigen  tener como mínimo las siguientes características  :

|**Características** |**Requisitos**|
| - | - |
|Sistema operativo|Windows 7 (64 bits) o posterior|
|Procesador|2 o más núcleos lógicos|
|Virtualización|Se requieren extensiones de virtualización. Es posible que deba habilitar esto a través del BIOS de su ordenador .|
|Memoria|4 GB de RAM|
|Almacenamiento|1 GB de espacio disponible (la instalación de Windows es < 200 MB).|

### 5.3 **Instalación GNS3**

Lo primero que tendremos que sera descargarnos el ejecutable oficial de su pagina web , para ello tendremos que estar registrados previamente .

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.074.jpeg)

Lanzaremos el ejecutable y nos pedirá permisos de administrados , se los concedemos :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.075.png)

Saldrá una pantalla informándonos sobre el producto , le damos a next .

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.076.png)

A continuación deberemos de aceptar los términos y licencias de uso :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.077.png)

Nos preguntara donde queremos crear los atajos del programa , lo dejare por defecto ya que asi los añadirá al escritorio :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.078.png)A continuación debemos de prestar atención ya que debemos de seleccionar instalación local y todos los paquetes que vayamos a hacer uso , si hubiésemos instalado antes  alguno de ellos los desmarcamos (Los mencionados en el punto 5.1) :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.079.png)

Seleccionaremos la ruta donde se instalara el programa , yo dejare la predeterminada . También nos informa el espacio que necesitara la instalación  :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.080.png)

Esperaremos a que se realice la instalación :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.081.png)

**Instalación WinCap**

Requerido para conectar GNS3 a su red informática. Utilizado por los nodos Cloud y NAT para permitir que sus proyectos se comuniquen con el mundo exterior.

Mientras se realiza la instalación de GNS3 comenzara la instalación de todos los programas que hemos marcado anteriormente .

Nos mostrara información sobre el programa esta primera ventana así que le damos a siguiente :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.082.png)

Aceptamos la licencia de términos y uso :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.083.png)

Marcamos la opción para que arranque automáticamente el driver y le damos a instalar 

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.084.png)

Nos informa de que la instalación a sido correcta y cerramos la ventana :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.085.png)

**Instalación Ncap** 

El reemplazo moderno de WinPCAP sabe solucionar problemas  pero está menos probado que WinPCAP.Instale Npcap con la opción "Modo compatible con la API de WinPcap" seleccionada, si se usa sin WinPcap.Npcap puede coexistir con WinPcap, si esa opción no está seleccionada.

Otra vez el mismo proceso , aceptamos los términos y licencias de uso .

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.086.png)

Dejamos la opción marcada por defecto y le damos a install 

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.087.png)

Cuando finalice la instalación le damos a siguiente :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.088.png)

Y cerramos el instalador :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.089.png)Volvemos a GNS3 ya que el proceso de instalación ha quedado detenido mientras hemos instalado los componentes que va a hacer uso , esta se reanuda automáticamente  :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.090.png)

Una vez finalice la instalación  , le damos a siguiente 

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.091.png)

GNS3  nos ofrece una licencia gratuita de Solarwinds , le daremos a si :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.092.png)

Habremos finalizado correctamente la instalación de GNS3

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.093.png)

Abriremos el programa y seleccionaremos correr los dispositivos en nuestra maquina local :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.094.png)

Aquí configuraremos nuestro servidor local de GNS3 

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.095.png)

Anteriormente lo deje por defecto , si nuestra configuración es correcta nos dirá que la conexión se ha realizado satisfactoriamente :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.096.png)

Nos mostrara un resumen de la configuración dada anteriormente :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.097.png)

### 5.4 **Prueba de funcionamiento** 

Montaremos el mismo escenario que en debian para comprobar su funcionamiento , el proceso es el mismo .

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.098.jpeg)

Configuraremos las direcciones ips de las maquinas y comprobamos que tengan conectividad  a través de solarputty .

PC1 :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.099.png)

PC2:

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.100.png)

Podemos observar que ambos equipos tienen conectividad a través del escenario .

## 6 **Instalación Wireshark en Windows**

### 6.1 **Instalación**

La instalación de este producto es muy sencilla , si hemos instalado GNS3 anteriormente y hemos marcado la casilla de este , se nos habrá instalado automáticamente .

Por el contrario si partimos desde cero podemos hacer su instalación , bajandonoslo de su sitio web oficial :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.101.jpeg)

Cuando abramos el instalador nos pedirá permisos de administrador , se lo concedemos :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.102.png)

Si al igual que yo lo has instalado con GNS3 nos detectara que ya existe una instalaron , así que yo la cancelare . 

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.103.png)

Si no lo tuviésemos la instalación es idéntica a cualquier programa que hemos instalado en la practica . Aquí te lo muestro , lo primero que veras sera una pantalla informativa del ejecutable :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.104.png)

Al igual que todos los programas te pedirá que aceptes los términos y condiciones de uso :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.105.png)

Seleccionaremos los productos que deseemos instalar en mi caso todos :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.106.png)

Además nos preguntara que accesos directos y donde los queremos crear 

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.107.png)

Seleccionaremos la ruta donde queremos que se instale :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.108.png)

Seleccionaremos si nos interesa el paquete Ncap .(Lo hemos instalado con GNS3)

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.109.png)

A continuación nos preguntara para instalar la extensión que nos permite analizar trafico USB , en mi caso la desmarcare ya que no me interesa .

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.110.png)

Esperaremos a que finalice la instalación y le daremos a siguiente :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.111.png)

Nos informara de que la instalación ha sido realizada correctamente :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.112.png)

### 6.2 **Prueba de funcionamiento**

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.113.jpeg)

He realizado una petición DNS a [www.sevillafc.es](http://www.sevillafc.es/) y aquí podemos ver la consulta DNS :

## 7 **GNS VM** 

Si queremos desplegar maquinas virtuales en una instancia virtual desplegaremos la maquina virtual que nos da GNS3 para que este lleve la carga de la Virtualización .

Nos descargaremos la OVA desde la pagina web oficial 

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.114.png)

Una vez descargada la importaremos en Vmware y le daremos las características hardware que consideremos oportuno :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.115.png)

Una  vez echo esto abriremos GNS3 y editaremos las preferencias de GNS VM y seleccionaremos la maquina virtual que acabamos de importar :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.116.jpeg)

Se  nos iniciara la maquina virtual y podremos ver los datos de la misma en la pestaña info :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.117.png)

Lanzaremos el set-up wizard desde la pestaña help de GNS3 y seleccionaremos la opción de ejecutar las apilances en una maquina virtual :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.118.png)

Seleccionaremos la configuración de nuestra maquina virtual :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.119.png)

Seleccionaremos de nuevo nuestra maquina virtual y las características hardware que deseemos  :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.120.jpeg)

Solo nos quedara importar los dispositivos en la maquina virtual , esto se hace igual que hemos echo anteriormente cambiando el sitio donde lo importamos :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.121.jpeg)

Si queremos ver donde se ejecutara un dispositivo podemos verlo a través de preferencias :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.122.jpeg)

Además podemos ver en apartado servers sumarry el consumo de recursos de nuestras maquinas :

![](../Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.123.png)

## 8 **Conclusión** 

Podemos ver que la instalación es infinitamente mas cómoda en Windows  ya que automáticamente te instala las dependencias, siendo la típica instalación de “siguiente a siguiente ” .

Además en Windows al acabar la instalación el producto estaba listo para usarse y  no he sufrido ningún error  al iniciar el programa ni al usar sus características como si me ha pasado en Debian .

## 9 **Bibliografía** 

[Documentacion oficial wireshark](https://www.wireshark.org/docs/wsug_html_chunked/ChBuildInstallWinInstall.html)

[Paquete wireshark en debian](https://packages.qa.debian.org/w/wireshark.html)

[Requisitos mínimos wireshark](https://www.wireshark.org/docs/wsug_html_chunked/ChIntroPlatforms.html)

[Error “VPCS executable version must be >=0.6.1 but not 0.8” ](https://gns3.com/vpcs-executable-version-must-be-greater-than-0-6-1-but-not-0-8)

[Descarga VPCS](https://github.com/GNS3/vpcs/releases)


