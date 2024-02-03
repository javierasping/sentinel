---
title: "Migración de un sistema de ficheros"
date: 2023-09-08T10:00:00+00:00
description: Aprende cómo migrar de un sistemas de ficheros tu debian a otro mas grande
tags: [Debian 12,sistemas,ISO,ASO]
hero: images/sistemas/migracion_de_sistema_de_ficheros/portada.jpg
---
# Migración de un sistema de ficheros

En ocasiones, es necesario actualizar el almacenamiento de nuestro sistema Debian para satisfacer las crecientes necesidades de espacio y mejorar la organización del disco. En esta guía, exploraremos el proceso de migración desde un disco con una única partición hacia uno con mayor capacidad, además de dividirlo en particiones separadas para una gestión más eficiente.

Este proceso no solo ampliará el espacio de almacenamiento disponible, sino que también brindará una estructura más ordenada al sistema, facilitando tareas como la gestión de respaldos, el rendimiento del sistema y la administración del espacio en disco.

## Características de la maquina

Crea una máquina virtual en virt-manager con las siguientes características:

- Se instalará sistema operativo GNU/Linux Debian11.
- Tamaño de memoria: 1GB.
- CPU:1
- Tamaño de disco duro: 2GB
- Detalles del hipervisor:
- chipset:Q35
- Firmware: UEFIx86

## Esquema de particiones

La instalación de debian la realizarás, con el siguiente esquema de particiones: partición efi: 50MB

partición /: 2GB

swap: el resto de espacio sobrante.

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.001.png)

No se instalará ningún entorno de escritorio.

Una vez instalado el sistema, nos damos cuenta que estaríamos muy justos de espacio. 

## Ampliación del disco

### Particionado

Añade un disco a tu sistema de 10GB.

Particiona este disco, eligiendo el tamaño apropiado para cada una de las particiones, teniendo en cuentas que cada partición será asignada a un directorio de los indicados:

/boot/efi FAT32 partición efi –> 100MB / ext4 –> 8GB

/home ext4 –>1GB

/var ext4 –> 400MB

/usr ext4 –> 400MB

swap swap –> 200MB

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.002.png)

### Dando sistema de ficheros a las particiones

Para darle formato a esta partición /boot/efi FAT32 partición efi –> 100MB

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.003.png)

Para estas particiones le daré formato ext4: / ext4 –> 8GB

/home ext4 –>1GB

/var ext4 –> 400MB

/usr ext4 –> 400MB

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.004.png)

Para dar formato de swap: swap swap –> 200MB

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.005.png)

Para “activar la swap” –> sudo swapon dev/vdb6 y posteriormente para hacerlo permanente lo
añadiremos al /etc/fstab .

Nos quedaría el disco con los siguientes formatos :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.006.png)

## Migración de datos

### Partición EFI
A continuación realizaremos una copia fidedigna de cada una de nuestras particiones para ello , creare un directorio para montar cada disco en un directorio con su nombre :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.007.png)

Y montaremos las particiones en estos directorios :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.008.png)

Comenzaremos a pasar la información de nuestras particiones . Es importante usar el parámetro a (lo mismo que dpR) que permite hacer la copia recursivamente además se conservan intactos los permisos y enlaces que se encuentren en el sistema. Con el parámetro f, forzamos la copia.

Copia de la partición EFI :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.009.jpeg)


### Partición HOME


Lo montaremos en un directorio cualquiera , a continuación lo copiaremos con rsync y con el comando diff comprobaremos si hay archivos diferentes en los directorios para ahorrarnos hacer la comprobación de forma manual .

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.010.png)

Ahora lo añadiremos al fstab :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.011.png)

Lo montamos con un mount -a . Lo desmontamos y borraremos el directorio home del antiguo disco :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.013.png)

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.014.png)

### Partición VAR


Lo montaremos en un directorio cualquiera , a continuación lo copiaremos con rsync y con el comando diff comprobaremos si hay archivos diferentes en los directorios para ahorrarnos hacer la comprobación de forma manual .

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.015.png)

Ahora lo añadiremos al fstab :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.016.png)

Lo montamos con un mount -a . Lo desmontamos y borraremos el directorio var del antiguo disco :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.017.png)


### Partición USR

Lo montaremos en un directorio cualquiera , a continuación lo copiaremos con rsync y con el comando diff comprobaremos si hay archivos diferentes en los directorios para ahorrarnos hacer la comprobación de forma manual .

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.018.png)

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.019.png)

Ahora lo añadiremos al fstab :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.020.png)

Lo montamos con un mount -a :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.021.jpeg)

Lo desmontamos y borraremos el directorio home del antiguo disco :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.022.png)

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.023.png)

Y volveremos a montarlos con un mount -a .

### Partición RAIZ

Lo montaremos en un directorio cualquiera , a continuación lo copiaremos con rsync y con el comando diff comprobaremos si hay archivos diferentes en los directorios para ahorrarnos hacer la comprobación de forma manual .

Excluyendo los directorios que hemos separado anteriormente :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.024.png)

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.025.png)

Ahora lo añadiremos al fstab :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.026.png)

Para montar esta partición deberemos de reiniciar el sistema .


## Generar la nueva EFI

Para esto hay que seguir un procedimiento distinto , lo primero que haremos sera darle formato fat32 a la partición . Después igual que las demás la montaremos y instalaremos un nuevo grub especificando donde queremos instalarlo , en el segundo disco.

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.028.png)

Ahora lo añadiremos al fstab :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.029.png)

Reiniciaremos el equipo y comprobaremos que funciona  :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.030.jpeg)

Ahora actualizaremos el grub :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.031.png)Ahora para construir el nuevo efi tendremos que a través de un cd live o desde el modo rescate construir un nuevo grub :

Montamos nuestra nueva partición del sistema y le damos a reinstalar el cargador de arranque grub :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.032.png)

Una vez hecho esto apagamos la maquina y ponemos el segundo disco primero e el orden de arranque y reiniciamos el equipo :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.033.png)

Cuando reinicie elegimos la primera opción que es el arranque de vdb :

Y habremos conseguido  migrar el sistema a un disco mas grande :![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.034.png)

Mi /etc/fstab ha quedado de la siguiente manera :

![](../img/Aspose.Words.bb81bc7a-b593-45c4-8e4d-c913a16c26ef.035.jpeg)


## Bibliografía

- [Migrar de un disco a otro ](https://www.dragonjar.org/migrar-instalacion-de-linux-a-una-particion-o-disco-diferente.xhtml)
- [Copiar particiones ](https://juncotic.com/particiones-copiando-instalacion-linux/)
- [Recuperar grub](https://lihuen.linti.unlp.edu.ar/index.php/Gu%C3%ADa_de_instalaci%C3%B3n_o_recuperaci%C3%B3n_de_GRUB)

