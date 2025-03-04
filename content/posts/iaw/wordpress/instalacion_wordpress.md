---
title: "Instalación WordPress en Debian 12 con pila LAMP PHP-8"
date: 2023-10-28T10:00:00+00:00
description: Instalación WordPress en Debian 12 con pila LAMP PHP-8
tags: [WordPress,CMS,IWEB,AW,debian]
hero: /images/iweb/wordpress/wordpress_lamp.png
---


# Instalación WordPress en Debian 12 con pila LAMP PHP-8

WordPress es un sistema de gestión de contenidos (CMS, por sus siglas en inglés) de código abierto muy popular que se utiliza para crear y administrar sitios web y blogs. Fue lanzado por primera vez en 2003 y desde entonces ha ganado una amplia base de usuarios y una comunidad activa de desarrolladores y diseñadores.


## Preparación

Antes de empezar con la instalación de WordPress vamos a dejar claro en una lista cual es el ecosistema de nuestro servidor para que todo funcione correctamente:

- Servidor LAMP completo: Apache + MySQL -o MariaDB- y PHP 8.x.
- Configurado un VirtualHost para nuestro dominio.
- Creación de base de datos con usuario.

Si no tienes instalado la pila LAMP sigue puedes hacerlo en [este enlace.](https://www.javiercd.es/posts/iaw/lamp/lamp/)

## Creación del VirtualHost

Copiamos el archivo de configuración predeterminado de Apache y lo renombramos a wordpress.conf

```bash
javiercruces@IWEB:/etc/apache2/sites-available$ sudo cp 000-default.conf wordpress.conf
```

Configuramos el sitio virtual , recuerda cambiar el ServerName y DocumentRoot

```bash
<VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        ServerName wordpress.fjcd.es

        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/wordpress

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf
</VirtualHost>
```

Habilitamos el sitio virtual wordpress.conf

```bash
javiercruces@IWEB:/etc/apache2/sites-available$ sudo a2ensite wordpress.conf 
Enabling site wordpress.
To activate the new configuration, you need to run:
  systemctl reload apache2

```

Recargamos Apache para aplicar la nueva configuración

```bash
javiercruces@IWEB:/etc/apache2/sites-available$ sudo systemctl reload apache2
```

Para acceder a este VirtualHost , en la maquina donde vayas a acceder al wordpress , al no tener servidor dns recuerda poner en el fichero host la ip de tu servidor con el ServerName :

```bash
javiercruces@HPOMEN15:~$ cat /etc/hosts 
#Añade la IP de tu servidor y el ServerName correspondiente (wordpress.fjcd.es)
#Ponlo al final del fichero y no modifiques las lineas existentes en tu fichero
192.168.125.27 wordpress.fjcd.es
```

## Creación de la base de datos con un usuario.

Te recomiendo que **apuntes** los datos introducidos a continuación ya que los necesitaras mas adelante .
Nos conectamos a la base de datos :
```bash
javiercruces@IWEB:~$ sudo mysql -u root -p
Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 31
Server version: 10.11.4-MariaDB-1~deb12u1 Debian 12

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
#Creamos una base de datos :
MariaDB [(none)]> CREATE DATABASE fjcd_wordpress;
Query OK, 1 row affected (0,001 sec)

#Nos creamos el usuario para nuestra base de datos
MariaDB [(none)]> CREATE USER 'fjcd-wordpress'@'localhost' IDENTIFIED BY 'tu_contraseña';
Query OK, 0 rows affected (0,013 sec)

#Le damos permisos sobre la base de datos que hemos creado:
MariaDB [(none)]> GRANT ALL PRIVILEGES ON fjcd_wordpress.* TO 'fjcd-wordpress'@'localhost';
Query OK, 0 rows affected (0,010 sec)

#Actualizamos los permisos:
MariaDB [(none)]> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0,000 sec)

#Nos salimos de la CLI de mysql
MariaDB [(none)]> EXIT;
Bye
```


## **Instalación de WordPress**

Lo primero que haremos será **[descargarnos WordPress](https://wordpress.org/download/?ref=voidnull.es)**, podemos hacerlo usando wget o si lo tenemos descargado en nuestro anfitrión pasarlo haciendo uso de SCP o FTP .

```bash
javiercruces@IWEB:~$ wget https://wordpress.org/latest.tar.gz
--2023-10-27 12:33:17--  https://wordpress.org/latest.tar.gz
Resolviendo wordpress.org (wordpress.org)... 198.143.164.252
Conectando con wordpress.org (wordpress.org)[198.143.164.252]:443... conectado.
Petición HTTP enviada, esperando respuesta... 200 OK
Longitud: 23465047 (22M) [application/octet-stream]
Grabando a: «latest.tar.gz»

latest.tar.gz             100%[=====================================>]  22,38M  14,8MB/s    en 1,5s    

2023-10-27 12:33:19 (14,8 MB/s) - «latest.tar.gz» guardado [23465047/23465047]
```

Y **descomprimiremos el fichero** y copiaremos los ficheros dentro del **`DocumentRoot`** de nuestro **`VirtualHost`:**

```
javiercruces@IWEB:~$ sudo mkdir   /var/www/wordpress/
javiercruces@IWEB:~$ sudo tar -zxf latest.tar.gz -C /var/www/
```

Entramos a la ruta del **WordPress** para realizar poner correctamente el esquema de permisos :

```
javiercruces@IWEB:~$ cd /var/www/
```

Cambiamos usuario y grupos:

```
javiercruces@IWEB:/var/www$ sudo chown -R www-data:www-data wordpress/
```

Y ponemos los permisos correctos a WordPress:

```
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

```

Una vez hemos configurado todo esto, ahora ya podemos acceder con nuestro navegador a nuestro dominio para iniciar la instalación de **WordPress.**

## Instalación Web

Accedemos a la url que hemos puesto en el ServerName de nuestro sitio virtual y posteriormente hemos configurado en el fichero hosts .

Lo primero sera seleccionar el idioma :

![Untitled](/iaw/wordpress/img/Untitled.png)

A continuación nos dará una breve explicación de que es el CMS WordPress :

![Untitled](/iaw/wordpress/img/Untitled%201.png)

Ahora deberás de introducir los datos referente a los usuarios y el nombre de la base de datos que has creado con anterioridad 

![Untitled](/iaw/wordpress/img/Untitled%202.png)

Una vez introducidos los datos correctos continuaremos con la instalación :

![Untitled](/iaw/wordpress/img/Untitled%203.png)

Ahora deberás de introducir los datos para tu wordpress , como el nombre del sitio asi como la creación de un usuario administrador para que posteriormente puedas acceder a wp-admin:

![Untitled](/iaw/wordpress/img/Untitled%204.png)

Listo !! Ya has instalado wordpress

![Untitled](/iaw/wordpress/img/Untitled%205.png)

Ahora para acceder al panel de administración de wordpress deberás de introducir la siguiente url en tu navegador e inicia sesión con el usuario que has creado:

![Untitled](/iaw/wordpress/img/Untitled%206.png)

Listo !! Asi se ve el panel de administración de wordpress:

![Untitled](/iaw/wordpress/img/Untitled%207.png)