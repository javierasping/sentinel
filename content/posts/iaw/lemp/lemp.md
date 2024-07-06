---
title: "Instalación pila LEMP en debian 12 con PHP-8"
date: 2023-10-28T10:00:00+00:00
description: Instalación pila LEMP en debian 12 con PHP-8
tags: [WordPress,CMS,IWEB,AW,debian,LEMP]
hero: /images/iweb/lamp/portada_lemp.png
---

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GVDYVWJLRH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GVDYVWJLRH');
</script>

# Instalación pila LEMP en debian 12 con PHP-8

En esta guía, te explicare los pasos necesarios para instalar una pila LEMP (Linux, Nginx, MariaDB y PHP) en un servidor con Debian 12. La configuración incluirá PHP 8.2 como versión principal. La pila LEMP es esencial para alojar sitios web y aplicaciones web basadas en PHP, como WordPress u otras aplicaciones dinámicas. Sigue los pasos detallados a continuación para configurar tu servidor LEMP con PHP 8.2.

## Requisitos previos

Antes de comenzar, asegúrate de que cumples con los siguientes requisitos:

- Un servidor Linux.
- Un usuario no root con privilegios sudo.
- Un nombre de dominio completo que apunte al servidor.

Primero, actualiza y actualiza los paquetes del sistema:

```bash
javiercruces@IWEB:~$ sudo apt update && sudo apt upgrade
```

Además, asegúrate de que los siguientes paquetes estén instalados en tu sistema , ya que los utilizaremos mas adelante :

```bash
javiercruces@IWEB:~$ sudo apt install wget nano unzip tar -y
```

## Instalación PHP  

Debian 12 incluye PHP 8.2 por defecto. Puedes instalarlo ejecutando el siguiente comando:

```bash
javiercruces@IWEB:~$ sudo apt install php-fpm php-cli php-mysql php-mbstring php-xml php-gd
```

Hemos instalado las extensiones MySQL, CLI, GD, Mbstring y XML de PHP. Puedes instalar cualquier extensión adicional según tus necesidades. Para verificar la instalación de PHP, puedes ejecutar:

```bash
javiercruces@IWEB:~$ php --version
PHP 8.2.7 (cli) (built: Jun  9 2023 19:37:27) (NTS)
Copyright (c) The PHP Group
Zend Engine v4.2.7, Copyright (c) Zend Technologies
with Zend OPcache v8.2.7, Copyright (c), by Zend Technologies
javiercruces@IWEB:~$
```
## Instalación MariaDB

Puedes usar indistintamente MariaDB o Mysql , en mi caso usare MariaDB :

```bash
javiercruces@IWEB:~$ sudo apt install mariadb-server
javiercruces@IWEB:~$ sudo systemctl enable mysql && sudo systemctl start mysql
```

Durante la instalación, se te pedirá establecer una contraseña para el usuario root de MySQL. Una vez que haya finalizado la instalación, ejecuta el siguiente comando para asegurar tu instalación de MariaDB:

```bash
javiercruces@IWEB:~$ sudo mysql_secure_installation
```

Sigue las instrucciones para asegurar tu instalación de MariaDB, como configurar la contraseña del usuario root y eliminar usuarios anónimos y bases de datos de prueba.

Después de completar estos pasos, habrás configurado MariaDB y podrás conectarte a través de la terminal .

Si te has saltado lanzar el script de la instalación segura , el usuario root de la base de datos no tiene contraseña asi que pulsa espacio para iniciar sesión una vez lanzado el comando .

```bash
javiercruces@IWEB:~$ sudo mysql -u root -p
Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 32
Server version: 10.11.4-MariaDB-1~deb12u1 Debian 12

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> 
```

## Instalar Nginx

Primero, asegurémonos de que Nginx esté instalado en tu servidor:

```bash
javiercruces@IWEB:~$ sudo apt install nginx
```

Una vez que Nginx esté instalado, procederemos a configurar un socket TCP para trabajar con PHP-FPM.

Abre el archivo de configuración de PHP-FPM para realizar la configuración necesaria:

```bash
javiercruces@IWEB:~$ sudo nano /etc/php/8.2/fpm/pool.d/www.conf
```

Dentro del archivo, busca la sección que define la dirección en la que PHP-FPM acepta solicitudes FastCGI.

Comenta la línea que comienza con listen y reemplázala por la siguiente línea para configurar un socket TCP en la dirección 127.0.0.1 y el puerto 9000:

```bash
; The address on which to accept FastCGI requests.
; Valid syntaxes are:
;   'ip.add.re.ss:port'    - to listen on a TCP socket to a specific IPv4 address on
;                            a specific port;
;   '[ip:6:addr:ess]:port' - to listen on a TCP socket to a specific IPv6 address on
;                            a specific port;
;   'port'                 - to listen on a TCP socket to all addresses
;                            (IPv6 and IPv4-mapped) on a specific port;
;   '/path/to/unix/socket' - to listen on a Unix socket.
; Note: This value is mandatory.
;listen = /run/php/php8.2-fpm.sock --> Comenta esta linea

listen = 127.0.0.1:9000
```

Guarda los cambios y cierra el archivo.

Ahora vamos a editar la configuración del sitio virtual por defecto para hacerlo funcionar con fpm . 

Para lograrlo, vamos a modificar el contenido dentro de la sección `location` en la configuración del servidor. Aquí te proporciono un ejemplo de archivo de configuración que puedes utilizar:

```bash
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;

        index index.html index.php index.htm index.nginx-debian.html ;

        server_name _;

        location / {
                try_files $uri $uri/ =404;
        }

        location ~ \.php$ {
            include snippets/fastcgi-php.conf;
            fastcgi_pass 127.0.0.1:9000; 
            #fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
            # fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include fastcgi_params;
        }
}
```

Ahora vamos a reiniciar los servicios tanto de php como de Nginx para asegurar de que sea aplicado la configuración , pero primero vamos a comprobar si tienes errores de sintais en ambos ficheros .

Para comprobar errores de sintaxis en Nginx :

```bash
javiercruces@IWEB:~$ sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

Si la salida es correcta continua comprobando si has cometido errores de sintaxis en la configuración de PHP-FPM :

```bash
javiercruces@IWEB:~$ sudo php-fpm8.2 -t
[02-Nov-2023 17:33:02] NOTICE: configuration file /etc/php/8.2/fpm/php-fpm.conf test is successful
```

Una vez las dos salidas de estos comandos no contienen errores , vamos a reiniciar ambos servicios para que se aplique la configuración :

```bash
javiercruces@IWEB:/etc/nginx$ sudo systemctl restart php8.2-fpm nginx.service
```

## Comprobación de funcionamiento  
Para asegurarnos de que el servidor está funcionando correctamente con PHP-FPM, vamos a crear un archivo llamado info.php que mostrará información sobre la configuración de PHP en el servidor. A continuación, te mostraré cómo crear el archivo:

```bash
javiercruces@IWEB:~$ sudo nano /var/www/html/info.php
```

Dentro del archivo info.php, agrega el siguiente contenido:

```bash
<?php
phpinfo();
?>
```

Guarda y cierra el archivo

Este archivo PHP mostrará información detallada sobre la configuración de PHP en tu servidor. Puedes acceder a él en tu navegador visitando http://tudominio.com/info.php (reemplaza tudominio.com con tu nombre de dominio real) o también puedes acceder al mismo poniendo en el navegador la IP de tu maquina.

![](../img/info-php.png)

Una vez hecho esto , ya tienes instalado la pila LEMP para que la utilices en tus CMS.