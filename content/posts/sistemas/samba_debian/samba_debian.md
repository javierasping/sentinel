---
title: "Instalar y configurar samba en Debian"
date: 2023-09-20T10:00:00+00:00
description: Instalar y configurar samba en Debian
tags: [Debian 12,Sistemas,ISO,ASO]
hero: images/sistemas/samba_debian/portada.png
---


Samba es una implementación libre y de código abierto del protocolo Server Message Block (SMB), que se utiliza para compartir archivos e impresoras en redes de computadoras. El protocolo SMB es un protocolo de red que permite que los sistemas operativos Windows se comuniquen con otros dispositivos de red, como servidores de archivos, impresoras y otros recursos compartidos.

Samba facilita la interoperabilidad entre sistemas Windows y sistemas operativos basados en Unix/Linux al permitir que los sistemas Unix compartan archivos y recursos con sistemas Windows utilizando el protocolo SMB/CIFS. Esto significa que un servidor Samba puede actuar como un servidor de archivos para clientes Windows, permitiéndoles acceder y compartir archivos como si estuvieran en un entorno Windows.

## 1.Instalación

Lo primero sera instalarnos el servidor samba :

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.001.png)

En el fichero  /etc/samba/smb.conf  realizaremos la configuración de nuestra carpeta :

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.002.png)

Nos crearemos un usuario de samba para poder acceder a los recursos :

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.003.png)

Reiniciaremos el servicio para que se aplique la configuración :

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.004.png)

## 2.Acceso desde Windows

Ahora podemos acceder desde un cliente Windows con el usuario que acabamos de crear -–> \\IP\DIRECTORIO\COMPARTIDO

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.005.png)

Nos pedirá que nos autentiquemos  :

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.006.png)

Podremos ver el contenido y crear :

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.007.png)

## 3.Acceso desde Linux

Nos instalamos el paquete smbclient para poder conectarnos a unidades compartidas con samba:

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.008.png)

Listar los directorios compartidos :

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.009.png)

Nos conectamos al recurso compartido

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.010.png)

Creare un directorio y comprobare que existe :

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.011.png)

## Bibliografía

-[Habilitar el acceso de invitado](https://learn.microsoft.com/es-es/troubleshoot/windows-client/networking/cannot-access-shared-folder-file-explorer)

