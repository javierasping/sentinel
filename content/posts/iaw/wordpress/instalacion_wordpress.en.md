---
title: "WordPress installation in Debian 12 with LAMP PHP-8"
date: 2023-10-28T10:00:00+00:00
Description: WordPress installation in Debian 12 with LAMP PHP-8 battery
tags: [WordPress,CMS,IWEB,AW,debian]
hero: /images/iweb/wordpress/wordpress_lamp.png
---


#WordPress installation in Debian 12 with LAMP PHP-8 battery

WordPress is a very popular open source content management system (CMS) that is used to create and manage websites and blogs. It was first released in 2003 and has since won a wide user base and an active community of developers and designers.


### Preparation

Before we start installing WordPress we will make clear in a list what is the ecosystem of our server for everything to work out properly:

- Full LAMP server: Apache + MySQL - or MariaDB- and PHP 8.x.
- Set up a VirtualHost for our domain.
- Development of database with user.

If you don't have the LAMP battery installed, you can do it in [this link.] (https: / / www.javiercd.es / posts / iaw / lamp / lamp /)

## Creation of VirtualHost

We copy Apache's default configuration file and rename it to wordpress.conf

```bash
javiercruces@IWEB:/etc/apache2/sites-available$ sudo cp 000-default.conf wordpress.conf
```

We set the virtual site, remember to change the ServerName and DocumentRoot

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

Enable the virtual site wordpress.conf

```bash
javiercruces@IWEB:/etc/apache2/sites-available$ sudo a2ensite wordpress.conf 
Enabling site wordpress.
To activate the new configuration, you need to run:
  systemctl reload apache2

```

We rearrange Apache to apply the new configuration

```bash
javiercruces@IWEB:/etc/apache2/sites-available$ sudo systemctl reload apache2
```

To access this VirtualHost, in the machine where you go to access the wordpress, by having no dns server remember to put in the host file the ip of your server with the Server:

```bash
javiercruces@HPOMEN15:~$ cat /etc/hosts 
#Añade la IP de tu servidor y el ServerName correspondiente (wordpress.fjcd.es)
#Ponlo al final del fichero y no modifiques las lineas existentes en tu fichero
192.168.125.27 wordpress.fjcd.es
```

### Creating the database with a user.

I recommend that you * * point * * the data entered below as you need them later.
We connect to the database:
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


## * * WordPress installation * *

The first thing we will do is * * [download WordPress] (https: / / wordpress.org / download /? ref = voidnull.es) * *, we can do it using wget or if we have it downloaded to our host pass it by using SCP or FTP.

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

And * * we'll uncompress the file * * and copy the files within the * 'DocumentRoot' * * of our * * 'VirtualHost': * *

```
javiercruces@IWEB:~$ sudo mkdir   /var/www/wordpress/
javiercruces@IWEB:~$ sudo tar -zxf latest.tar.gz -C /var/www/
```

We enter the * * WordPress * * route to make the permit scheme correctly:

```
javiercruces@IWEB:~$ cd /var/www/
```

We change user and groups:

```
javiercruces@IWEB:/var/www$ sudo chown -R www-data:www-data wordpress/
```

<! -- And we put the right permissions to WordPress:

```
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

``` -->

Once we have set all this up, we can now access our browser to our domain to start installing * * WordPress. * *

## Web installation

We access the url we have put in the ServerName of our virtual site and then set up in the hosts file.

The first thing is to select the language:

! [Untitled] (.. / img / Untitled.png)

Below is a brief explanation of what the CMS WordPress is:

[Untitled] (.. / img / Untitled% 201.png)

You will now need to enter the user data and the name of the database you have created before.

[Untitled] (.. / img / Untitled% 202.png)

Once the correct data is entered we will continue with the installation:

[Untitled] (.. / img / Untitled% 203.png)

Now you must enter the data for your wordpress, such as the name of the site as well as the creation of an administrator user so that you can then access wp-admin:

[Untitled] (.. / img / Untitled% 204.png)

Ready! You've already installed wordpress

[Untitled] (.. / img / Untitled% 205.png)

Now to access the wordpress management panel you must enter the following url into your browser and log in with the user you have created:

[Untitled] (.. / img / Untitled% 206.png)

Ready! This is how you see the wardpress management panel:

[Untitled] (.. / img / Untitled% 207.png)