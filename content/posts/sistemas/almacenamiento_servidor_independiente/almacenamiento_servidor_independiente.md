---
title: "Storage Spaces en Windows Server"
date: 2023-09-08T10:00:00+00:00
description: Aprende cómo usar Storage Spaces en Windows Server
tags: [Linux,Sistemas,ISO,ASO]
hero: images/sistemas/storage_spaces/portada.png
---


Storage Spaces es una característica de almacenamiento definido por software en el sistema operativo Windows Server que permite a los administradores de sistemas combinar varios discos físicos en un único espacio de almacenamiento lógico llamado "pool de almacenamiento". Este pool de almacenamiento se puede utilizar para crear espacios de almacenamiento virtuales llamados "espacios de almacenamiento" que ofrecen diversas funciones de redundancia y capacidades avanzadas de administración de almacenamiento.

## Grupos de almacenamiento

Los siguientes cmdlets de Windows PowerShell realizan la misma función que el procedimiento anterior. Escriba cada cmdlet en una sola línea, aunque aquí pueden aparecer con saltos de línea entre varias líneas aquí debido a restricciones de formato.

El siguiente ejemplo muestra qué discos físicos están disponibles en el grupo primordial. 

```ps
Get-StoragePool -IsPrimordial $true | Get-PhysicalDisk -CanPool $True
```

![](../img/Aspose.Words.2ccae554-4864-4939-8439-3bfaf64ead92.001.png)

El siguiente ejemplo crea un nuevo grupo de almacenamiento denominado StoragePool1 que usa todos los discos disponibles:

```ps
New-StoragePool –FriendlyName StoragePool1 –StorageSubsystemFriendlyName "Windows Storage\*" –PhysicalDisks (Get-PhysicalDisk –CanPool $True) 
```

![](../img/Aspose.Words.2ccae554-4864-4939-8439-3bfaf64ead92.002.png)

Por defecto el tipo de aprovisionamiento es mirror.

Si necesitamos añadir mas discos :

```ps
Add-PhysicalDisk -StoragePoolFriendlyName StoragePool1 -PhysicalDisks (Get-PhysicalDisk  - CanPool $True)
```

## Crear un disco virtual

Vamos a crear un disco virtual :

```ps
New-VirtualDisk –StoragePoolFriendlyName StoragePool1 –FriendlyName VirtualDisk1 –Size (8GB)
```

![](../img/Aspose.Words.2ccae554-4864-4939-8439-3bfaf64ead92.003.jpeg)

Automáticamente nos creara un volumen y nos lo montara en una letra disponible: :

![](../img/Aspose.Words.2ccae554-4864-4939-8439-3bfaf64ead92.004.jpeg)

Podemos interactuar con el y guardar información :

![](../img/Aspose.Words.2ccae554-4864-4939-8439-3bfaf64ead92.005.png)

Vemos que este es el “equivalente” a LVM en Windows . Vemos que hay similitudes no solo en la estructura a la hora de crearlo si no que también podemos observar que hacen referencia en la documentación oficial a RAID 5 y RAID 6:

![](../img/Aspose.Words.2ccae554-4864-4939-8439-3bfaf64ead92.006.png)

A la forma de almacenar los datos en ya sea en stripes o guardando el espacio completo , al igual que sucede en Linux :

![](../img/Aspose.Words.2ccae554-4864-4939-8439-3bfaf64ead92.007.jpeg)

## Bibliografía

- [Documentación oficial](https://learn.microsoft.com/es-es/windows-server/storage/storage-spaces/deploy-standalone-storage-spaces) 

