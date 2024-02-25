---
title: "Compartir directorios con NFS en debian"
date: 2023-09-08T10:00:00+00:00
description: Aprende cómo compartir directorios con NFS en debian
tags: [Linux,Sistemas,ISO,ASO]
hero: images/sistemas/nfs/portada.png
---

La tecnología NFS (Network File System) ha sido una pieza fundamental en la compartición de archivos en entornos de red. Desarrollada por Sun Microsystems, NFS permite a sistemas operativos Unix y Linux compartir recursos de archivos de manera transparente, brindando acceso a archivos y directorios remotos como si estuvieran almacenados localmente.

## 1.Instalación  y configuración NFS

Instalamos el paquete nfs-kernel-server.

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.001.png)

Crearemos el directorio que vamos a compartir  y le cambiamos los dueños y los permisos del mismo :

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.002.png)

En el fichero etc/exports indicaremos cual es nuestro directorio y sus respectivos permisos :

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.003.jpeg)

- **ro**: permiso de solo lectura del directorio
- **rw**: permiso de lectura y escritura del directorio
- **subtree_check**: especifica la verificación de subdirectorios
- **no_subtree_check:** previene verificación de subdirectorios
- **sync:** Escribe todos los cambios en el disco antes de aplicarlo
- **Async:** ignora la verificación de sincronización para mejorar la velocidad

Aplicamos los cambios y reiniciamos el servicio :

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.004.png)

## 2.Visualizarlo en un cliente debian

Nos instalaremos el siguiente paquete :

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.005.png)

La montamos en nuestro cliente : 

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.006.png)

También podemos hacerlo de forma permanente en el fstab :

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.007.png)

Podemos visualizar el contenido :

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.008.png)

Vamos a crear un archivo y a comprobar que se ha creado en el servidor :

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.009.png)

## 3.Visualización en Windows

Nos descargamos la característica de cliente NFS:

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.010.jpeg)

Mapeamos la unidad de red :

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.011.jpeg)

Creamos un fichero de forma remota y comprobamos que se ha creado .

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.012.jpeg)

Lo comprobamos también en el servidor :

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.013.png)

