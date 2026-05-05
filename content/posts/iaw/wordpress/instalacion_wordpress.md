---
title: "Instalación WordPress en Debian 12 con pila LAMP PHP-8"
date: 2023-10-28T10:00:00+00:00
description: Guía paso a paso para la instalación de WordPress en Debian 12 utilizando la pila LAMP con PHP 8.
tags: [WordPress,CMS,IWEB,AW,debian]
hero: /images/iweb/wordpress/wordpress_lamp.png
---


# Instalación de WordPress en Debian 12 con la pila LAMP y PHP 8

WordPress es un sistema de gestión de contenidos (CMS, por sus siglas en inglés) de código abierto muy popular que se utiliza para crear y administrar sitios web y blogs. Fue lanzado por primera vez en 2003 y desde entonces ha ganado una amplia base de usuarios y una comunidad activa de desarrolladores y diseñadores.


## Preparación

Antes de comenzar con la instalación de WordPress, definiremos la configuración necesaria del servidor para asegurar que todo funcione correctamente:

- Servidor LAMP completo: Apache + MySQL -o MariaDB- y PHP 8.x.
- Configurado un VirtualHost para nuestro dominio.
- Creación de base de datos con usuario.

Si no tienes instalada la pila LAMP, puedes hacerlo a través de [este enlace](https://www.javiercd.es/posts/iaw/lamp/lamp/).

## Creación del VirtualHost

Copiaremos el archivo de configuración predeterminado de Apache y lo renombraremos como `wordpress.conf`

```bash
javiercruces@IWEB:/etc/apache2/sites-available$ sudo cp 000-default.conf wordpress.conf
```

Configuraremos el sitio virtual; recuerda modificar el `ServerName` y el `DocumentRoot`

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

Habilitaremos el sitio virtual `wordpress.conf`

```bash
javiercruces@IWEB:/etc/apache2/sites-available$ sudo a2ensite wordpress.conf 
Enabling site wordpress.
To activate the new configuration, you need to run:
  systemctl reload apache2

```

Reiniciaremos Apache para aplicar la nueva configuración

```bash
javiercruces@IWEB:/etc/apache2/sites-available$ sudo systemctl reload apache2
```

Para acceder a este VirtualHost desde la máquina cliente, dado que no disponemos de un servidor DNS, recuerda añadir la IP del servidor y el `ServerName` correspondiente al archivo `/etc/hosts` :

```bash
javiercruces@HPOMEN15:~$ cat /etc/hosts 
#Añade la IP de tu servidor y el ServerName correspondiente (wordpress.fjcd.es)
#Ponlo al final del fichero y no modifiques las lineas existentes en tu fichero
192.168.125.27 wordpress.fjcd.es
```

## Creación de la base de datos con un usuario.

Te recomiendo **anotar** los datos introducidos a continuación, ya que los necesitarás más adelante.
Nos conectaremos a la base de datos:
```bash
javiercruces@IWEB:~$ sudo mysql -u root -p
Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 31
Server version: 10.11.4-MariaDB-1~deb12u1 Debian 12

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
# Creación de la base de datos:
MariaDB [(none)]> CREATE DATABASE fjcd_wordpress;
Query OK, 1 row affected (0,001 sec)

# Creación del usuario para la base de datos:
MariaDB [(none)]> CREATE USER 'fjcd-wordpress'@'localhost' IDENTIFIED BY 'tu_contraseña';
Query OK, 0 rows affected (0,013 sec)

# Asignación de permisos sobre la base de datos creada:
MariaDB [(none)]> GRANT ALL PRIVILEGES ON fjcd_wordpress.* TO 'fjcd-wordpress'@'localhost';
Query OK, 0 rows affected (0,010 sec)

# Actualización de los permisos:
MariaDB [(none)]> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0,000 sec)

# Salida de la CLI de MySQL
MariaDB [(none)]> EXIT;
Bye
```


## **Instalación de WordPress**

Lo primero que haremos será **[descargar WordPress](https://wordpress.org/download/?ref=voidnull.es)**. Podemos hacerlo utilizando `wget` o, si ya lo hemos descargado en el equipo anfitrión, transferirlo mediante SCP o FTP.

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

A continuación, **descomprimiremos el archivo** y copiaremos los archivos dentro del `DocumentRoot` de nuestro `VirtualHost`:

```
javiercruces@IWEB:~$ sudo mkdir   /var/www/wordpress/
javiercruces@IWEB:~$ sudo tar -zxf latest.tar.gz -C /var/www/
```

Accederemos al directorio de **WordPress** para configurar correctamente el esquema de permisos:

```
javiercruces@IWEB:~$ cd /var/www/
```

Cambiaremos el propietario y el grupo:

```
javiercruces@IWEB:/var/www$ sudo chown -R www-data:www-data wordpress/
```

Asignaremos los permisos correctos a WordPress:

```
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

```

Una vez configurado todo esto, ya podemos acceder a través del navegador a nuestro dominio para iniciar la instalación de **WordPress**.

## Instalación Web

Accedemos a la URL definida en el `ServerName` de nuestro sitio virtual y configurada previamente en el archivo `/etc/hosts`.

Lo primero será seleccionar el idioma:

![Untitled](/iaw/wordpress/img/Untitled.png)

A continuación, se mostrará una breve explicación sobre el CMS WordPress:

![Untitled](/iaw/wordpress/img/Untitled%201.png)

Ahora deberás introducir los datos del usuario y el nombre de la base de datos creada anteriormente: 

![Untitled](/iaw/wordpress/img/Untitled%202.png)

Una vez introducidos los datos correctos, continuaremos con la instalación:

![Untitled](/iaw/wordpress/img/Untitled%203.png)

Ahora deberás introducir la información de tu sitio de WordPress, como el nombre del sitio y la creación de un usuario administrador para acceder posteriormente al panel `wp-admin`:

![Untitled](/iaw/wordpress/img/Untitled%204.png)

¡Listo! Ya has instalado WordPress.

![Untitled](/iaw/wordpress/img/Untitled%205.png)

Para acceder al panel de administración de WordPress, introduce la siguiente URL en tu navegador e inicia sesión con el usuario creado:

![Untitled](/iaw/wordpress/img/Untitled%206.png)

¡Listo! Así es como se ve el panel de administración de WordPress:

![Untitled](/iaw/wordpress/img/Untitled%207.png)