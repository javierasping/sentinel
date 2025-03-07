---
title: "Ejercicios de modificación de parámetros del kernel"
date: 2023-11-29T10:00:00+00:00
description: Ejercicios de modificación de parámetros del kernel
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/ejercicios_de_modificacion_de_parametros_del_kernel/ejercicios_de_modificacion_de_parametros_del_kernel.jpg
---

## 1.Deshabilita apparmor en el arranque.

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.001.png)

## 2.Deshabilita si es posible el Kernel Mode Setting (KSM) de la tarjeta gráfica. Añadimos la siguiente linea en la configuraron del grub :

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.002.png)

Actualizamos el grub para que se apliquen los cambios :

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.003.png)

## 3.Cambia provisionalmente la swappiness para que la swap de tu equipo se active cuando se use más de un 90% de la RAM.

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.004.png)

## 4.Haz que el cambio de la swappiness sea permanente.

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.005.png)

Tienes que ejecutar sudo sysctl -p para que se aplique . 5.Muestra el valor del bit de forward para IPv6.

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.006.png)

## 6.Deshabilita completamente las Magic Sysrq en el arranque y vuelve a habilitarlas después de reiniciar.

Para deshabilitaras :

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.007.png)

Para volver a habilitarlas cambia el valor de 0 a 1 y reinicia el equipo o  ejecuta sudo sysctl -p:

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.008.png)

