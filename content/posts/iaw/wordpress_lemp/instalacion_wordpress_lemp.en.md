---
title: "WordPress installation in Debian 12 with PHP-8 LEMP battery"
date: 2023-10-28T10:00:00+00:00
description: Step-by-step guide for installing WordPress on Debian 12 using the LEMP stack with PHP 8.
tags: [WordPress,CMS,IWEB,AW,debian]
hero: /images/iweb/wordpress/wordpress_lemp.png
---


# WordPress Installation on Debian 12 with the LEMP Stack and PHP 8

WordPress is a highly popular open-source content management system (CMS) used to create and manage websites and blogs. Since its release in 2003, it has built a massive user base and a vibrant community of developers and designers.


### Previous requirements

1. **Linux server:** You must have a server running Linux; this guide is specifically designed for Debian 12.
2. **User with superuser permissions:** You must have access to a user with sudo privileges on the server in order to perform the installation and configuration tasks.
3. **Full Domain Name (FQDN):** If you want to access your WordPress site through a custom domain, make sure you have a full domain name (FQDN) set up and pointed to the server.
4. **Internet access:** You need Internet access to download packages and make updates during the installation process.

Ensure you meet all these requirements before starting the WordPress installation on your server.

If the LEMP stack is not installed, you can do so via [this link](https://www.javiercd.es/posts/iaw/lemp/lemp/).


## Creating a VirtualHost in Nginx

The creation of a VirtualHost in Nginx allows you to configure multiple websites on a single server. Follow these steps to create a VirtualHost in Nginx.

Copy the default Nginx configuration file to use as a template and name it as you prefer. In this example, we will name it `wordpress`; please note that this name is purely informative.

```bash
javiercruces@IWEB:~$ sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/wordpress
```

We will edit the contents of the file using the following command:

```bash
javiercruces@IWEB:~$ sudo nano /etc/nginx/sites-available/wordpress
```

Here I leave the example of my site configuration file, make sure you define the server name (your domain) and the site root directory.

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

To activate this configuration, we will create a symbolic link:

```bash
javiercruces@IWEB:~$ sudo ln -s /etc/nginx/sites-available/wordpress /etc/nginx/sites-enabled/
```
Now, restart Nginx to apply the changes:

```bash
javiercruces@IWEB:~$ sudo systemctl reload nginx
```



To access this VirtualHost from the client machine, since there is no DNS server, remember to add the server's IP and the `ServerName` to the `/etc/hosts` file:

```bash
javiercruces@HPOMEN15:~$ cat /etc/hosts 
#Añade la IP de tu servidor y el ServerName correspondiente (wordpress.fjcd.es)
#Ponlo al final del fichero y no modifiques las lineas existentes en tu fichero
192.168.125.27 wordpress.fjcd.es
```

### Creating the database with a user.

I recommend **noting down** the data entered below, as you will need them later.
We will connect to the database:
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


## WordPress installation

The first step is to **[download WordPress](https://wordpress.org/download/?ref=voidnull.es)**. This can be done using `wget` or, if it's already downloaded on the host machine, by transferring it via SCP or FTP.

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

Next, we will **uncompress the file** and copy its contents into the `DocumentRoot` of our `VirtualHost`:

```
javiercruces@IWEB:~$ sudo mkdir   /var/www/wordpress/
javiercruces@IWEB:~$ sudo tar -zxf latest.tar.gz -C /var/www/
```

We will access the **WordPress** directory to configure the correct permissions:

```
javiercruces@IWEB:~$ cd /var/www/
```

We change user and groups:

```
javiercruces@IWEB:/var/www$ sudo chown -R www-data:www-data wordpress/
```

And we put the right permissions to WordPress:

```
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

``` 

Once all this is configured, we can access our domain via a browser to start the **WordPress** installation.

## Web installation

We will access the URL defined in the `ServerName` of our virtual site and configured in the `/etc/hosts` file.

The first step is to select the language:

!! [Untitled](/iaw/wordpress_lemp/img/Untitled.png)

Below, a brief explanation of the WordPress CMS will be displayed:

![Untitled](/iaw/wordpress_lemp/img/Untitled%201.png)

You will now need to enter the user details and the name of the database created earlier:

![Untitled](/iaw/wordpress_lemp/img/Untitled%202.png)

Once the correct data is entered, we will proceed with the installation:

![Untitled](/iaw/wordpress_lemp/img/Untitled%203.png)

Now you must enter the information for your WordPress site, such as the site name and the creation of an administrator user to later access the `wp-admin` panel:

![Untitled](/iaw/wordpress_lemp/img/Untitled%204.png)

Ready! WordPress has been successfully installed.

![Untitled](/iaw/wordpress_lemp/img/Untitled%205.png)

To access the WordPress management panel, enter the following URL in your browser and log in with the created user:

![Untitled](/iaw/wordpress_lemp/img/Untitled%206.png)

Ready! This is how the WordPress management panel looks:

![Untitled](/iaw/wordpress_lemp/img/Untitled%207.png)