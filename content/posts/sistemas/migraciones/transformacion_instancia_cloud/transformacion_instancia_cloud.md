---
title: "Transformación instancia cloud"
date: 2023-11-29T10:00:00+00:00
description: Transformación instancia cloud
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/ejercicios_de_manejo_de_modulos/ejercicios_de_manejo_de_modulos.jpg
---


## Creación del esquema LVM

Nos instalamos el paquete LVM2

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.001.png)

Ahora crearemos las particiones en el segundo disco :

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.002.png)

Creamos el grupo de volúmenes :

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.003.png)

Creamos los volúmenes raíz y home :

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.004.png)

La particiones tienes que tener el siguiente formato : 

-vdb2 etx4

-FJCD-vg-home ext4

-FJCD-vg-raiz ext4

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.005.jpeg)

Nos quedara darle formato a la efi :

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.006.png)

Así quedaría nuestro esquema de particiones :

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.007.jpeg)

## Copiar el contenido de las particiones

Ahora vamos a montar las particiones :

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.008.png)

Ahora vamos a copiar las particiones , comenzamos con la boot :

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.009.png)

Continuamos con la efi :

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.010.png)

Seguimos con la raiz :

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.011.png)

Finalizamos con la home :

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.012.png)

## Instalar el grub en el segundo disco

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.013.png)

Podemos aprovechar para cambiar el fichero /etc/fstab del segundo disco :

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.014.jpeg)

Te dejo grabado en vídeo la prueba en directo de que el sistema arranca quitándole el primer disco. https://youtu.be/zAlMqKIaLCQ

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.015.png)


