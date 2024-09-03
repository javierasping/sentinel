---
title: "Paso de CentOS stream 8 a CentOS stream 9"
date: 2023-11-29T10:00:00+00:00
description: Paso de CentOS stream 8 a CentOS stream 9
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/paso_de_centos_stream_8_a_centos_stream_9/paso_de_centos_stream_8_a_centos_stream_9.png
---



## Actualizar los paquetes

Antes de migrar, asegúrate de que tu sistema CentOS Stream 8 tenga todos los paquetes y actualizaciones más recientes. 

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.001.jpeg)

Elimina los paquetes innecesarios que nos aparezcan al utilizar el siguiente comando ya que son paquetes huérfanos 

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.002.png)

## Actualización a CentOS9

Instala los repositorios de CentOS 9 : 

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.003.jpeg)

Ahora vamos a actualizar los paquetes a CentOS 9:

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.004.png)

Cuando finalice la instalación nos lo indicara , es posible que se eliminen algunos paquetes  :

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.005.png)

Actualizamos la base de datos de los paquetes locales :

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.006.png)

Eliminamos los paquetes de la cache dnf :

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.007.png)

Actualizamos los paquetes instalados :

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.008.png)

Instalamos los paquetes para la instalación mínima de un server core (sin entorno gráfico):

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.009.png)

Ahora reiniciaremos el sistema y arrancamos con CentOS 9 :

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.010.jpeg)

Al iniciar podemos comprobar que ya oficialmente tenemos CentOS 9 :

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.011.jpeg)

## Limpieza adicional

Si quieres puedes eliminar el kernel antiguo :

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.012.png)

Además si no tienes subscripción puedes eliminar el mánager de suscripciones :

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.013.png)

## Generar entrada de rescate en el grub

Moveremos los kerneles antiguos de rescate a una carpeta temporal como copia de seguridad :

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.014.png)

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.015.png)

Ahora vamos  a regenerar las entradas del kernel , el comando no nos devolverá nada así que podemos comprobarlo mirando en la partición boot :

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.016.png)

Una vez hecho podremos reiniciar y comprobar  que tenemos la entrada de recuperación de CentOS 9:

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.017.png)

## Bibliografía

Guía para migrar de CentOS 8 stream a CenOS 9 stream 

