---
title: "Instalación WordPress en Debian 12 con pila LEMP PHP-8"
date: 2023-10-28T10:00:00+00:00
description: Instalación WordPress en Debian 12 con pila LEMP PHP-8
tags: [WordPress,CMS,IWEB,AW,debian]
hero: /images/iweb/wordpress/portada_wordpress.png
---
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GVDYVWJLRH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GVDYVWJLRH');
</script>

# Instalación WordPress en Debian 12 con pila LEMP PHP-8

WordPress es un sistema de gestión de contenidos (CMS, por sus siglas en inglés) de código abierto muy popular que se utiliza para crear y administrar sitios web y blogs. Fue lanzado por primera vez en 2003 y desde entonces ha ganado una amplia base de usuarios y una comunidad activa de desarrolladores y diseñadores.


## Requisitos previos

1. **Servidor con Linux:** Debes disponer de un servidor que ejecute Linux , la guía esta pensada para Debian 12 .
2. **Usuario con permisos de superusuario:** Debes tener acceso a un usuario con privilegios sudo en el servidor para poder llevar a cabo las tareas de instalación y configuración.
3. **Nombre de Dominio Completo (FQDN):** Si deseas acceder a tu sitio WordPress a través de un dominio personalizado, asegúrate de tener configurado y apuntando un nombre de dominio completo (FQDN) al servidor.
4. **Acceso a Internet:** Necesitas acceso a Internet para descargar paquetes y realizar actualizaciones durante el proceso de instalación.

Asegúrate de cumplir con todos estos requisitos antes de comenzar con la instalación de WordPress en tu servidor .

Si no tienes instalado la pila LEMP sigue puedes hacerlo en [este enlace.](https://www.javiercd.es/posts/iaw/lemp/lemp/)


## Creación de un VirtualHost en Nginx

La creación de un VirtualHost en Nginx te permite configurar múltiples sitios web en un único servidor. Sigue estos pasos para crear un VirtualHost en Nginx.

Copia el archivo de configuración por defecto de Nginx para usarlo como ejemplo y nómbralo como quieras. En este ejemplo, lo nombraremos "wordpress" , ya que vamos a instalarlo sin embargo el nombre es meramente informativo.

```bash
javiercruces@IWEB:~$ sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/wordpress
```

Vamos a editar el contenido del mismo , para ello  : 

```bash
javiercruces@IWEB:~$ sudo nano /etc/nginx/sites-available/wordpress
```

Aquí te dejo el ejemplo del fichero de configuración de mi sitio , asegúrate de definir el nombre del servidor (tu dominio) y el directorio raíz del sitio.

```bash
server {
    listen 80;
    root /var/www/wordpress;  # Cambia esta linea por la ubicación del directorio root de tu wordpress
    index  index.php index.html index.htm;
    server_name  wordpress.fjcd.es; # Cambia esta linea y pon el FQDN , a traves de este accederás a tu wordpress 

    client_max_body_size 500M;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location = /favicon.ico {
        log_not_found off;
        access_log off;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
        expires max;
        log_not_found off;
    }

    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }

    location ~ \.php$ {
         include snippets/fastcgi-php.conf;
         fastcgi_pass 127.0.0.1:9000;
         fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
         include fastcgi_params;
    }
}

```

Para hacer esta configuración activa vamos a crear un enlace simbólico 

```bash
javiercruces@IWEB:~$ sudo ln -s /etc/nginx/sites-available/wordpress /etc/nginx/sites-enabled/
```
Ahora vamos a reiniciar nginx , para que se apliquen los cambios :

```bash
javiercruces@IWEB:~$ sudo systemctl reload nginx
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

<!-- Y ponemos los permisos correctos a WordPress:

```
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

``` -->

Una vez hemos configurado todo esto, ahora ya podemos acceder con nuestro navegador a nuestro dominio para iniciar la instalación de **WordPress.**

## Instalación Web

Accedemos a la url que hemos puesto en el ServerName de nuestro sitio virtual y posteriormente hemos configurado en el fichero hosts .

Lo primero sera seleccionar el idioma :

![Untitled](../img/Untitled.png)

A continuación nos dará una breve explicación de que es el CMS WordPress :

![Untitled](../img/Untitled%201.png)

Ahora deberás de introducir los datos referente a los usuarios y el nombre de la base de datos que has creado con anterioridad 

![Untitled](../img/Untitled%202.png)

Una vez introducidos los datos correctos continuaremos con la instalación :

![Untitled](../img/Untitled%203.png)

Ahora deberás de introducir los datos para tu wordpress , como el nombre del sitio asi como la creación de un usuario administrador para que posteriormente puedas acceder a wp-admin:

![Untitled](../img/Untitled%204.png)

Listo !! Ya has instalado wordpress

![Untitled](../img/Untitled%205.png)

Ahora para acceder al panel de administración de wordpress deberás de introducir la siguiente url en tu navegador e inicia sesión con el usuario que has creado:

![Untitled](../img/Untitled%206.png)

Listo !! Asi se ve el panel de administración de wordpress:

![Untitled](../img/Untitled%207.png)