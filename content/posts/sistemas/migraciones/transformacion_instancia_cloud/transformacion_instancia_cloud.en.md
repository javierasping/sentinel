---
title: "Transformation instance cloud"
date: 2023-11-29T10:00:00+00:00
description: Transformation instance cloud
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/ejercicios_de_manejo_de_modulos/ejercicios_de_manejo_de_modulos.jpg
---


## Creation of the LVM scheme

We installed the LVM2 package

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.001.png)

Now we'll create the partitions on the second disk:

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.002.png)

We create the group of volumes:

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.003.png)

We create the root and home volumes:

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.004.png)

The partitions must have the following format:

-vdb2 etx4

- FJCD-vg-home ext4

-FJCD-vg-raiz ext4

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.005.jpeg)

We would have to format the efi:

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.006.png)

So would our partition scheme:

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.007.jpeg)

## Copy the partition content

Now let's ride the partitions:

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.008.png)

Now let's copy the partitions, start with the boot:

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.009.png)

We continue with the efi:

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.010.png)

We continue with the root:

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.011.png)

We end with home:

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.012.png)

### Install the grub on the second disk

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.013.png)

We can use it to change the / etc / fstab file of the second disk:

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.014.jpeg)

I leave you on video the live proof that the system starts by removing the first disco. https: / / youtu.be / zAlMqKIaLCQ

![](/sistemas/migraciones/transformacion_instancia_cloud/img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.015.png)


