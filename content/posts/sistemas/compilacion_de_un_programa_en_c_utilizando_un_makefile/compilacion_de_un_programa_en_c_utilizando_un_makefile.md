---
title: "Compilación de un programa en C utilizando un Makefile"
date: 2023-11-29T10:00:00+00:00
description: Compilación de un programa en C utilizando un Makefile
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/compilacion_de_un_programa_en_c/compilacion_de_un_programa_en_c.jpg
---



## Introducción

La compilación de programas en el lenguaje de programación C es un proceso fundamental en el desarrollo de software. Permite traducir el código fuente escrito por los programadores en instrucciones comprensibles por la computadora. Uno de los desafíos asociados con la compilación es la gestión eficiente de los archivos y dependencias del proyecto, lo cual se vuelve aún más crucial cuando se trabaja en proyectos grandes y complejos.

Este trabajo tiene como objetivo explorar uno de los mecanismos más utilizados para compilar proyectos en C: el uso de un archivo Makefile. Un Makefile es un archivo de configuración que describe cómo se deben compilar los archivos fuente de un proyecto y cómo se deben gestionar las dependencias entre ellos. Además, permite automatizar el proceso de compilación y facilita la tarea de mantener y actualizar el código.

A lo largo de este trabajo, examinaremos en detalle el proceso de compilación de un programa en C utilizando un Makefile. Comenzaremos por entender la estructura de un Makefile y cómo se define el flujo de compilación. Luego, exploraremos las ventajas de su uso, como la detección automática de cambios en los archivos fuente y la recopilación selectiva. También abordaremos las prácticas recomendadas para crear Makefiles efectivos y fáciles de mantener.

Además, analizaremos un ejemplo práctico de compilación de un programa C, detallando los pasos necesarios para crear un Makefile y compilar el proyecto. Asimismo, discutiremos la instalación del programa resultante en un directorio personal, evitando interferencias con el sistema de paquetes.

En última instancia, aprenderemos cómo desinstalar limpiamente el programa y comprenderemos la importancia de una gestión adecuada del software en sistemas Unix/Linux.

A medida que avanzamos en este trabajo, ganaremos una comprensión más profunda de la compilación en C y la utilidad de un Makefile como una herramienta esencial en el desarrollo de software.

## Compilación de un programa en C utilizando un Makefile

Lo primero que vamos a instalar son fundamentales para la compilación de paquetes en C en Debian. 

El paquete build-essential proporciona las herramientas de compilación necesarias, y dpkg-dev facilita la gestión de paquetes y la obtención del código fuente. Puedes instalar otros paquetes de desarrollo específicos según tus necesidades, pero estos dos son los más esenciales para comenzar a compilar software en C en Debian.

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.001.png)

Ahora vamos a descargar los ficheros fuente del paquete que queramos compilar en mi caso lo haré de samba :

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.002.png)

Una vez hecho esto veremos en nuestro directorio que se han creado una serie de ficheros y directorios :

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.003.png)

**samba-4.17.12+dfsg:** Este es el directorio que contiene el código fuente de Samba, que se descargó desde los repositorios de Debian. Es la fuente que se utilizará para compilar e instalar Samba en tu sistema.

**samba\_4.17.12+dfsg-0+deb12u1.debian.tar.xz:**  Este  archivo  comprimido  contiene  las modificaciones específicas de Debian para el paquete Samba. Puede incluir parches, scripts de construcción y otros archivos relacionados con la construcción del paquete.

**samba\_4.17.12+dfsg-0+deb12u1.dsc:** Este archivo es el fichero de control de las fuentes Debian (Debian Source Control). Contiene información sobre la fuente y las versiones del paquete, así como enlaces a otros archivos relacionados con la fuente.

**samba\_4.17.12+dfsg.orig.tar.xz:** Este archivo comprimido es la fuente original de Samba tal como se publicó en el sitio web oficial de Samba. Se utiliza como base para construir el paquete Debian.

Vamos a meternos en el directorio principal y podemos ver el código fuente del paquete :

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.004.png)

Lo primero que haremos sera instalar las dependencias del paquete que queremos compilar en mi caso samba  : 

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.005.png)

Ahora vamos a lanzar el script configure . Este script se utiliza para configurar la compilación de samba en función de tus necesidades y las características del sistema :

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.006.png)

Ahora vamos a compilar el código  fuente utilizando el comando make . Este se encargara de compilar el código y creara las ejecutables y bibliotecas que a creado el script configure :

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.007.png)

Este tardara en función del tamaño del paquete en mi caso me ha tardado 8 min :

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.008.png)

Una vez compilado el código para instalarlo vamos a usar make install : 

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.009.png)

Una vez hecho esto tendremos nuestro paquete instalado en la ruta /usr/local :

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.010.png)

Ahora para iniciar el servicio de samba ejecutaremos el fichero nmbd  y nos aseguraremos de que este esta funcionando :

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.011.png)

Vemos que la versión instalada es la que hemos compilado :

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.012.png)

## Desinstalar el paquete compilado

Para eliminar el paquete que hemos compilado :

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.013.png)

Vemos que solo nos deja los ficheros de configuración del servicio :

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.014.png)

Es posible que queden en nuestro sistema rastros de samba ya que el fichero makefile no esta configurado en este caso para eliminarlo completamente , ejecutamos whereis y eliminamos el contenido de las rutas :

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.015.png)

Una vez hecho esto habremos eliminado el rastro de samba :

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.016.png)

