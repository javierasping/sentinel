---
title: "Configuración Apache bajo debian"
date: 2023-09-08T10:00:00+00:00
description: Configuración del servicio Apache 
tags: [Servicios,NAT,SMR,IPTABLES,SNAT,SSH,FORWARDING,APACHE]
hero: images/servicios/apache/portada-apache.jpg
---
## Instalar un servidor web Apache para el uso en una Intranet

Para instalar el servidor debemos ejecutar como root el siguiente comando:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.125.png)

Crea dentro del directorio /var/www/html un fichero llamado entrada.html en el que pongáis un mensaje de bienvenida

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.126.png)

Ahora  lo meteré dentro de la ruta :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.127.png)

A continuación vamos a publicar una página más completa en nuestro servidor, para ello

utiliza tu sitio web de aplicaciones web.


Ademas debemos de darle permisos de lectura a otros para que podamos visualizarla :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.128.png)

Accede desde los clientes, poniendo en un navegador la siguiente URL:

Desde debian cliente :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.129.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.130.png)

A continuación vamos a publicar una página más completa en nuestro servidor, para ello utiliza tu sitio web de aplicaciones web:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.131.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.132.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.133.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.134.png)



Resolución local de nombres : modifica los ficheros necesarios en el servicio BIND y accede usando el nombre que has indicado :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.135.png)

Como ya tenia echo el dns anteriormente he utilizado este nombre :

## Configuración de sitios web virtuales usando Apache
La primera web tendrá el directorio base será /var/www/iesgn y contendrá una página llamada index.html, donde sólo se verá una bienvenida a la página del instituto Gonzalo Nazareno .

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.136.png)

La segunda web tendrá el directorio base será /var/www/departamentos. En este sitio sólo tendremos una página inicial index.html, dando la bienvenida a la página de los departamentos del instituto.

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.137.png)

Necesitamos tener dos ficheros para realizar la configuración de los dos sitios virtuales, para ello vamos a copiar el fichero 000-default.conf

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.138.png)

Una vez hayamos creado los ficheros añadiremos dentro de cada uno el siguiente contenido :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.139.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.140.png)

Ahora deberemos crear un enlace simbólico en el directorio /etc/apache2/sites-enabled.

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.141.png)

Para que se apliquen estos cambios debemos reiniciar el servicio :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.142.png)

Ahora deberemos de actualizar el dns :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.143.png)

Una vez reiniciado el dns podremos acceder a ambos sitios desde el navegador :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.144.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.145.png)




## Acceso autentificado al servidor web Apache

Para activar la autentificación básica debemos de añadir las siguientes lineas a nuestro archivo de configuración del sitio :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.146.png)

Ahora creamos el archivo de las contraseñas , con el usuario previamente creado  :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.147.png)

Reiniciamos el servicio y nos conectamos :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.148.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.149.png)

Ahora vamos ha hacer que a la pagina departamentos solo acceda el director y el profesor , ademas  que a dirección solo acceda el director , para eso añadimos en departamentos:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.150.png)

Ahora vamos a añadir los usuarios de las zonas para eso , utilizamos este comando :

- Usuario profesor a departamentos :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.151.png)

- Usuario director a departamentos :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.152.png)

- Usuario director a zona dirección :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.153.png)

Ahora reiniciaremos el servicio y comprobaremos que podemos acceder :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.154.png)

Accederemos a departamentos :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.155.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.156.png)

Ahora a la zona equipo directivo :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.157.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.158.png)

