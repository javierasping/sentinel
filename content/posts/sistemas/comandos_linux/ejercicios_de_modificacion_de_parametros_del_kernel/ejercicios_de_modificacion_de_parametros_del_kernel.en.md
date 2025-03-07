---
title: "Kernel parameter modification exercises"
date: 2023-11-29T10:00:00+00:00
Description: Kernel parameter modification exercises
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/ejercicios_de_modificacion_de_parametros_del_kernel/ejercicios_de_modificacion_de_parametros_del_kernel.jpg
---

## 1.Disable apparmor in boot.

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.001.png)

## 2.Disable if possible the Kernel Mode Setting (KSM) of the graphics card. We add the following line in the group configuration:

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.002.png)

We update the grub to apply the changes:

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.003.png)

## 3 Change the swappiness provisionally so that your equipment swap is activated when more than 90% of the RAM is used.

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.004.png)

## 4 Make swappiness change permanent.

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.005.png)

You have to run sysctl -p sudo to be applied. 5.Show the value of the forward bit for IPv6.

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.006.png)

## 6.Fully disable the Magic Sysrq in the boot and reactivate them after reboot.

To disable:

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.007.png)

To reenable them change the value from 0 to 1 and restart the computer or run sudo sysctl -p:

![](/sistemas/comandos_linux/ejercicios_de_modificacion_de_parametros_del_kernel/img/Aspose.Words.901d0dd4-f71a-4e77-902f-980456adb847.008.png)