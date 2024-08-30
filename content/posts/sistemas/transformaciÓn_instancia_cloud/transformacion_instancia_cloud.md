---
title: "Transformación instancia cloud"
date: 2023-11-29T10:00:00+00:00
description: Transformación instancia cloud
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/ejercicios_de_manejo_de_modulos/ejercicios_de_manejo_de_modulos.jpg
---
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GVDYVWJLRH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GVDYVWJLRH');
</script>

## Creación del esquema LVM

Nos instalamos el paquete LVM2

![](../img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.001.png)

Ahora crearemos las particiones en el segundo disco :

![](../img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.002.png)

Creamos el grupo de volúmenes :

![](../img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.003.png)

Creamos los volúmenes raíz y home :

![](../img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.004.png)

La particiones tienes que tener el siguiente formato : 

-vdb2 etx4

-FJCD-vg-home ext4

-FJCD-vg-raiz ext4

![](../img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.005.jpeg)

Nos quedara darle formato a la efi :

![](../img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.006.png)

Así quedaría nuestro esquema de particiones :

![](../img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.007.jpeg)

## Copiar el contenido de las particiones

Ahora vamos a montar las particiones :

![](../img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.008.png)

Ahora vamos a copiar las particiones , comenzamos con la boot :

![](../img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.009.png)

Continuamos con la efi :

![](../img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.010.png)

Seguimos con la raiz :

![](../img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.011.png)

Finalizamos con la home :

![](../img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.012.png)

## Instalar el grub en el segundo disco

![](../img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.013.png)

Podemos aprovechar para cambiar el fichero /etc/fstab del segundo disco :

![](../img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.014.jpeg)

Te dejo grabado en vídeo la prueba en directo de que el sistema arranca quitándole el primer disco. https://youtu.be/zAlMqKIaLCQ

![](../img/Aspose.Words.1d1b77d6-c571-465c-8927-e55061548549.015.png)


