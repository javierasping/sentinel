---
title: "FTP bajo debian "
date: 2023-09-08T10:00:00+00:00
description: Configuración del servidor FTP 
tags: [Servicios,NAT,SMR,IPTABLES,SNAT,SSH,FORWARDING,APACHE,FTP]
hero: images/servicios/ftp/portada-ftp.png
---
# Servidor FTP bajo debian
##  Instalación y configuración del servidor proFTPd autentificado
1.Primero nos crearemos un grupo que se llame ftpgroup :
![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.160.png)

2.Crea dos usuarios locales que pertenezcan al grupo ftp que hemos creado: Jose y Maria

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.161.png)

3.Nos instalamos el servicio ftp :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.162.png)

4.Configuración básica del fichero proftpd.conf:

Todos los usuarios accedan  solo a su directorio :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.163.png)

Ahora podemos acceder desde el navegador con los usuarios Jose y Maria  :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.164.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.165.png)

Cada uno de estos he creado una carpeta con su nombre dentro de sus directorios personales para poder identificarlos .

Para que cada usuario pueda conectarse realmente al servidor FTP en Debian y le sea posible subir y descargar los datos en su propio directorio, debes introducir su directorio de entrada en proftpd.conf :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.166.png)

Podemos transferir archivos correctamente :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.167.png)

## Configuración de proFTPd para crear ftp anónimo

Lo primero que tenemos que hacer es crear el directorio y darle el propietario adecuado:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.168.png)

Ahora cambiaremos esta regla y permitiremos que todos puedan unirse :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.169.png)

Ademas añadimos  las siguientes lineas e indicaremos la ruta a la que accederán los anónimos :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.170.png)

Por lo que cuando reiniciemos podrán conectarse los usuarios anónimos :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.171.png)

Pero no con los usuarios que hemos creado anteriormente :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.172.png)

Para permitir que nuestros usuarios se puedan conectar  ademas de los anónimos:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.173.png)

Ahora aplicamos estos cambios y probamos a conectarnos . Vemos que con anónimos no podemos copiar nada al servidor pero si podemos descargar.

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.174.png)

Ahora con un usuario del grupo , podremos copiar archivos  :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.175.png)