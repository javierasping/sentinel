---
title: "Ejercicios de manejo de módulos"
date: 2023-11-29T10:00:00+00:00
description: Ejercicios de manejo de módulos
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/ejercicios_de_manejo_de_modulos/ejercicios_de_manejo_de_modulos.jpg
---



## 1.Comprueba los módulos cargados en tu equipo.

![](../img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.001.png)

## 2.Cuenta el número de módulos disponibles en el núcleo que estás usando.

![](../img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.002.png)

## 3.Conecta un lápiz USB y observa la salida de la instrucción sudo dmesg.

Vemos como el kernel detecta el dispositivo usb y se cargan los módulos necesarios para el mismo :

![](../img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.003.jpeg)

Vemos como el numero de módulos cargados han aumentado :

![](../img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.004.png)

## 4.Elimina el módulo correspondiente a algún dispotivo no esencial y comprueba qué ocurre. Vuelve a cargarlo.

Si lo descargamos no podremos hacer uso de sistemas de ficheros exfat :

![](../img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.005.png)

Para volver a cargarlo :

![](../img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.006.png)

## 5.Selecciona un módulo que esté en uso en tu equipo y configura el arranque para que no se cargue automáticamente.

Para ello lo añadimos a la “lista negra ” , luego actualizamos el initframes :

![](../img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.007.png)

Cuando reiniciemos este no estará cargado :

![](../img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.008.png)

## 6.Carga el módulo loop, obtén información de qué es y para qué sirve. Lista el contenido de /sys/modules/loop/parameters y configura el equipo para que se puedan cargar como máximo 12 dispositivos loop la próxima vez que se arranque.

Lo cargamos y comprobamos que este este cargado :

![](../img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.009.png)

Vemos la información del mismo :

![](../img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.010.jpeg)

Listo el contenido del directorio  /sys/module/loop/parameters . Esto mostrará los parámetros disponibles para el módulo loop

![](../img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.011.png)

Si queremos limitar que haya 12 dispositivos loop , creamos el siguiente fichero y añadimos la siguiente configuración  :

![](../img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.012.png)

Tendremos que actualizar el initframes sudo update-initramfs -u , para que se apliquen los cambios , además tendremos que reiniciar . 

Una vez reiniciamos , si vemos el contenido del parámetro max_loops . Veremos que este se ha aplicado : 

![](../img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.013.png)

