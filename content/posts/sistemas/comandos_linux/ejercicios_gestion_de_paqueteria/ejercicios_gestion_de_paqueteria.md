---
title: "Ejercicios gestión de paquetería"
date: 2023-11-29T10:00:00+00:00
description: Ejercicios gestión de paquetería
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/ejercicios_de_manejo_de_modulos/ejercicios_de_manejo_de_modulos.jpg
---

## Trabajo con apt, aptitude, dpkg

### Ejercicio 1 Que acciones consigo al realizar apt update y apt upgrade. Explica detalladamente.

El comando apt update es el primer paso fundamental en la actualización de paquetes. Realiza las siguientes acciones:

- **Recupera Metadatos Remotos:** apt update se comunica con los repositorios de software en línea y recupera los metadatos relacionados con los paquetes disponibles. Estos metadatos incluyen información sobre las últimas versiones de los paquetes, sus dependencias y otra información esencial.
- **Actualiza la Copia Local de Metadatos:** Luego, apt reconstruye y actualiza la copia local de estos metadatos. Esto permite que el sistema acceda rápidamente a información sobre los paquetes sin necesidad de descargarla repetidamente.

Una vez que apt update ha actualizado la información sobre los paquetes disponibles, el siguiente paso es utilizar el comando apt upgrade. Este comando realiza una serie de pasos importantes:

- **Selección de Versiones Candidatas**: apt selecciona las versiones candidatas de los paquetes disponibles. Estas versiones suelen ser las más recientes, aunque hay excepciones.
- **Resolución de Dependencias:** apt verifica y resuelve las dependencias entre los paquetes para garantizar que la actualización se realice de manera coherente y que todas las dependencias estén satisfechas.
- **Descarga de Paquetes:** Si se encuentran nuevas versiones de paquetes, apt descarga estas versiones desde los repositorios en línea a la caché local del sistema.
- **Desempaquetado de Paquetes:** apt desempaqueta los paquetes binarios recuperados.
- **Ejecución de Órdenes Preinst:**  Durante la actualización, se ejecutan los archivos de órdenes preinstalación, que pueden contener configuraciones y ajustes necesarios antes de la instalación.
- **Instalación de Archivos Binarios:** Los archivos binarios de las nuevas versiones de los paquetes se instalan en el sistema.
- **Ejecución  de  Órdenes  Postinst:**  Finalmente,  se  ejecutan  los  archivos  de  órdenes postinstalación, que pueden realizar configuraciones adicionales después de la instalación.


### Ejercicio 2 Lista la relación de paquetes que pueden ser actualizados. ¿Qué información puedes sacar a tenor de lo mostrado en el listado?

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.001.png)

Puedes verificar la lista de paquetes que pueden ser actualizados utilizando el siguiente comando apt list --upgradable. Este comando mostrará una lista de paquetes disponibles para la actualización y proporcionará información sobre cada uno de ellos. Aquí hay una breve descripción de la información que puedes obtener a partir de este listado:

- Nombre del Paquete: El nombre del paquete es la primera columna de la lista. Te muestra el nombre del paquete que se puede actualizar, por ejemplo, nombre-del-paquete.
- Versión Actual: La versión actualmente instalada del paquete se encuentra a la derecha del nombre del paquete, en la segunda columna. Por ejemplo, 1.2.3.
- Versión Disponible: La tercera columna muestra la versión disponible más reciente del paquete en los repositorios. Por ejemplo, 1.2.4.
- Estado de la Actualización: En la última columna, se indica el estado de la actualización. Si hay un asterisco (\*) junto al nombre del paquete, significa que ese paquete está marcado para ser actualizado.
- Descripción del Paquete: Además de esta información básica, el listado también proporciona una breve descripción del paquete, que te brinda una idea general de la función del paquete y su propósito.


### Ejercicio 3 Indica la versión instalada, candidata así como la prioridad del paquete openssh-client

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.002.png)

## Ejercicio 4 ¿Cómo puedes sacar información de un paquete oficial instalado o que no este instalado?** Podemos usar el comando apt show para paquetes instalados como para no instalados .

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.003.jpeg)

También podemos hacerlo con dpkg pero el paquete tiene que estar instalado → dpkg -s :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.004.jpeg)


### Ejercicio 5 Saca toda la información que puedas del paquete openssh-client que tienes actualmente instalado en tu máquina

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.005.jpeg)

### Ejercicio 6 Saca toda la información que puedas del paquete openssh-client candidato a actualizar en tu máquina

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.006.jpeg)


### Ejercicio 7 Lista todo el contenido referente al paquete openssh-client actual de tu máquina. Utiliza para ello tanto dpkg como apt.

Usando dpkg :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.007.jpeg)

Usando apt :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.008.png)


### Ejercicio 8 Listar el contenido de un paquete sin la necesidad de instalarlo o descargarlo. 

Podemos usar apt file  :

- apt-file list [paquete]

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.009.jpeg)

### Ejercicio 9 Simula la instalación del paquete openssh-client

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.010.jpeg)

### Ejercicio 10 ¿Qué comando te informa de los posible bugs que presente un determinado paquete?

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.011.png)

### Ejercicio 11 Después de realizar un apt update && apt upgrade. Si quisieras actualizar únicamente los paquetes que tienen de cadena openssh. ¿Qué procedimiento seguirías?. Realiza esta acción, con las estructuras repetitivas que te ofrece bash, así como con el comando xargs.

Usando la estructura repetitiva de bash , usando un one line :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.012.png)

Usando xargs :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.013.png)

### Ejercicio 12 ¿Cómo encontrarías qué paquetes dependen de un paquete específico?

Con este vemos las dependencias del paquete directas :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.014.png)

Mientras que con este las dependencias indirectas :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.015.png)

### Ejercicio 13 ¿Cómo procederías para encontrar el paquete al que pertenece un determinado fichero? 

Podemos usar dpkg :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.016.png)

Podemos usar apt-file :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.017.png)

### Ejercicio 14 ¿Que procedimientos emplearías para liberar la caché en cuanto a descargas de paquetería? 

Para limpiar la caché de descargas :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.018.png)

Para eliminarlos paquetes descargados que ya no están en uso:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.019.png)

O podemos hacer las dos cosas a la vez con apt clean :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.020.png)

### Ejercicio 15 Realiza la instalación del paquete keyboard-configuration pasando previamente los valores de los parámetros de configuración como variables de entorno.

Nos aseguramos de que tenemos instalado el paquete :

Para ello nos instalamos debconfs-utils:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.021.png)

En un fichero declaramos las variables que queramos configurar en el teclado :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.022.png)

Y se las proporcionamos al debconf:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.023.png)

Y comprobaremos que se han aplicado los cambios :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.024.jpeg)

### Ejercicio 16 Reconfigura el paquete locales de tu equipo, añadiendo una localización que no exista previamente. Comprueba a modificar las variables de entorno correspondientes para que la sesión del usuario utilice otra localización.

Si queremos almacenar nuestra configuración para cada usuario exportaremos nuestras variables y las pondremos en el bashrc :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.025.png)

A continuación ejecutaremos dpkg-reconfigure y observaremos que tendremos seleccionado el valor de la variable :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.026.jpeg)

### Ejercicio 17 Interrumpe la configuración de un paquete y explica los pasos a dar para continuar la instalación

Una vez irrumpamos la instalación de un paquete , para continuar la instalación del mismo podemos usar el comando dpkg:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.027.png)

Podemos usar el parámetro -a para todos los paquetes o especificar el nombre para continuar su instalación :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.028.png)

### Ejercicio 18 Explica la instrucción que utilizarías para hacer una actualización completa de todos los paquetes de tu sistema de manera completamente no interactiva

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.029.png)

### Ejercicio 19 Bloquea la actualización de determinados paquetes

Lo marcamos para evitar las actualizaciones y listamos los marcados para comprobar que no se actualizara :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.030.png)



## Trabajo con ficheros .deb 

### Ejercicio 1 Descarga un paquete sin instalarlo, es decir, descarga el fichero .deb correspondiente. Indica diferentes formas de hacerlo.

Podemos usar el comando apt :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.031.png)

Podemos usar wget y descargarlo desde los repositorios de debían :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.032.jpeg)

## Ejercicio 2 ¿Cómo puedes ver el contenido, que no extraerlo, de lo que se instalará en el sistema de un paquete deb?

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.033.png)


### Ejercicio 3 Sobre el fichero .deb descargado, utiliza el comando ar. ar permite extraer el contenido de una paquete deb. Indica el procedimiento para visualizar con ar el contenido del paquete deb. Con el paquete que has descargado y utilizando el comando ar, descomprime el paquete. ¿Qué información dispones después de la extracción?. Indica la finalidad de lo extraído.

Para visualizar el contenido :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.034.png)

Para descomprimir el directorio :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.035.png)
Hemos extraído 3 archivos del paquete :

1. control.tar.xz : Contiene scripts que dpkg utiliza para instalar el paquete 
2. data.tar.xz : contiene los archivos del paquete 
3. debian-binary : indica la version del paquete 

Indica el procedimiento para descomprimir lo extraído por ar del punto anterior. ¿Qué información contiene?

Para descomprimir ficheros usaremos tar -xJf :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.036.png)

Nos encontraremos los siguientes directorios y ficheros :

- **control**: Este archivo contiene metadatos sobre el paquete, como su nombre, versión, descripción, dependencias y otros detalles importantes.
- **conffiles**: Este archivo enumera los archivos de configuración que son parte del paquete y que deben ser tratados de manera especial durante las actualizaciones para preservar las configuraciones personalizadas del usuario.
- **preinst**: Este es un script de preinstalación que se ejecuta antes de que el paquete sea instalado en el sistema. Puede contener acciones de preconfiguración necesarias.
- **postinst**: Este es un script de postinstalación que se ejecuta después de que el paquete ha sido instalado en el sistema. Puede contener acciones de postconfiguración necesarias.
- **prerm**: Este es un script de preremoción que se ejecuta antes de que el paquete sea desinstalado del sistema. Puede contener acciones de preeliminación necesarias.
- **postrm**: Este es un script de postremoción que se ejecuta después de que el paquete ha sido desinstalado del sistema. Puede contener acciones de posteliminación necesarias.
- **md5sums**: Este archivo contiene las sumas de control MD5 de los archivos que se instalan con el paquete. Se utiliza para verificar la integridad de los archivos durante la instalación.

El archivo data.tar.xz contiene los archivos y directorios que se instalarán en el sistema cuando se instale el paquete.



## Trabajo con repositorios

### Ejercicio 1 Añade a tu fichero sources.list los repositorios de bullseye-backports y sid.

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.037.png)

### Ejercicio 2 Configura el sistema APT para que los paquetes de debian bullseye tengan mayor prioridad y por tanto sean los que se instalen por defecto.

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.038.png)

### Ejercicio 3 Configura el sistema APT para que los paquetes de bullseye-backports tengan mayor prioridad que los de unstable.

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.039.jpeg)

### Ejercicio 4 ¿Cómo añades la posibilidad de descargar paquetería de la arquitectura i386 en tu sistema. ¿Que comando has empleado?. Lista arquitecturas no nativas. ¿Cómo procederías para desechar la posibilidad de descargar paquetería de la arquitectura i386?

Para añadirla :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.040.png)

Para eliminarla :

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.041.png)

### Ejercicio 5 Si quisieras descargar un paquete, ¿cómo puedes saber todas las versiones disponible de dicho paquete?

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.042.png)

### Ejercicio 6 Indica el procedimiento para descargar un paquete del repositorio stable.

Tal y como lo tenemos configurado los paquetes por prioridad se descargaran del repositorio estable . Pero podemos indicárselo : 

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.043.png)

### Ejercicio 7 Indica el procedimiento para descargar un paquete del repositorio de buster-backports

Tienes que tener el repositorio indicado en el sources.list luego puedes indicarlo con el parámetro -t.

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.044.png)

### Ejercicio 8 Indica el procedimiento para descargar un paquete del repositorio de sid

Igual que el ejercicio anterior solo que aquí indicamos sid ya que tenemos indicado el repositorio en el sources.list:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.045.png)

### Ejercicio 9 Indica el procedimiento para descargar un paquete de arquitectura i386.** Indicamos el nombre del paquete seguido de :i386

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.046.jpeg)



## Trabajo con directorios 

Que cometidos tienen

**/var/lib/apt/lists/:**  Este directorio contiene listas de paquetes disponibles en los repositorios configurados en mi sistema. Estas listas son archivos con extensión .list que contienen información sobre los paquetes disponibles, sus versiones y las fuentes de donde se pueden descargar. Cuando ejecuto apt update, actualizo estas listas .

**/var/lib/dpkg/available:** Este archivo contiene información sobre los paquetes instalados y sus versiones. Es utilizado por mi sistema de gestión de paquetes dpkg para mantener un registro de los paquetes  que  tengo instalados y sus  estados.  Proporciona información  sobre  los  paquetes disponibles y sus dependencias.

**/var/lib/dpkg/status:** Este archivo también contiene información sobre los paquetes instalados en mi sistema, pero proporciona una vista más detallada que /var/lib/dpkg/available. Contiene información sobre el estado de los paquetes, como si están instalados, desinstalados o si hay problemas con su configuración. 

**/var/cache/apt/archives/:** Este directorio almacena los archivos de paquetes que descargo antes de que sean instalados en mi sistema. Cuando ejecuto comandos como apt-get install o apt-get upgrade, los paquetes se descargan primero en este directorio y luego se instalan. Mantener una copia de los paquetes descargados en este directorio puede ser útil si deseo reinstalar o desinstalar un paquete sin volver a descargarlo desde los repositorios, lo que ayuda a ahorrar tiempo y ancho de banda.


