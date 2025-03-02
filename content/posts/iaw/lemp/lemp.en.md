---
title: "LMP battery installation in debian 12 with PHP-8"
date: 2023-10-28T10:00:00+00:00
Description: LMP battery installation in debian 12 with PHP-8
tags: [WordPress,CMS,IWEB,AW,debian,LEMP]
hero: /images/iweb/lamp/portada_lemp.png
---



♪ LMP battery installation in debian 12 with PHP-8

In this guide, I will explain the steps needed to install a LEMP battery (Linux, Nginx, MariaDB and PHP) on a Debian 12 server. The configuration will include PHP 8.2 as the main version. The LEMP battery is essential for hosting PHP-based websites and applications, such as WordPress or other dynamic applications. Follow the detailed steps below to configure your LEMP server with PHP 8.2.

### Previous requirements

Before you start, make sure you meet the following requirements:

- A Linux server.
- A non-root user with sudo privileges.
- A full domain name that points to the server.

First, update and update the system packages:

```bash
javiercruces@IWEB:~$ sudo apt update && sudo apt upgrade
```

In addition, make sure that the following packages are installed in your system, as we will use them later:

```bash
javiercruces@IWEB:~$ sudo apt install wget nano unzip tar -y
```

PHP installation

Debian 12 includes PHP 8.2 by default. You can install it by running the following command:

```bash
javiercruces@IWEB:~$ sudo apt install php-fpm php-cli php-mysql php-mbstring php-xml php-gd
```

We have installed the MySQL, CLI, GD, Mbstring and XML extensions of PHP. You can install any additional extension according to your needs. To verify PHP installation, you can run:

```bash
javiercruces@IWEB:~$ php --version
PHP 8.2.7 (cli) (built: Jun  9 2023 19:37:27) (NTS)
Copyright (c) The PHP Group
Zend Engine v4.2.7, Copyright (c) Zend Technologies
with Zend OPcache v8.2.7, Copyright (c), by Zend Technologies
javiercruces@IWEB:~$
```
## MariaDB installation

You can use MariaDB or Mysql indistinctly, in my case use MariaDB:

```bash
javiercruces@IWEB:~$ sudo apt install mariadb-server
javiercruces@IWEB:~$ sudo systemctl enable mysql && sudo systemctl start mysql
```

During installation, you will be asked to set a password for the root user of MySQL. Once the installation is finished, run the following command to ensure your MariaDB installation:

```bash
javiercruces@IWEB:~$ sudo mysql_secure_installation
```

Follow the instructions to secure your MariaDB installation, such as setting up the root user password and removing anonymous users and test databases.

After completing these steps, you will have configured MariaDB and you will be able to connect through the terminal.

If you have skipped the secure installation script, the root user of the database has no password so click space to log in once the command is released.

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

Install Nginx

First, let's make sure Nginx is installed on your server:

```bash
javiercruces@IWEB:~$ sudo apt install nginx
```

Once Nginx is installed, we will proceed to set up a TCP socket to work with PHP-FPM.

Open the PHP-FPM configuration file to make the necessary configuration:

```bash
javiercruces@IWEB:~$ sudo nano /etc/php/8.2/fpm/pool.d/www.conf
```

Within the file, look for the section that defines the direction in which PHP-FPM accepts FastCGI requests.

Commentate the line that starts with a look and replace it with the following line to set up a TCP socket in the direction 127.0.0.1 and port 9000:

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

Save the changes and close the file.

Now let's edit the default virtual site settings to make it work with fpm.

To achieve this, we will modify the content within the 'location' section in the server configuration. Here I provide you with an example of a configuration file that you can use:

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

Now we're going to restart both php and Nginx services to ensure that the configuration is applied, but first we're going to check if you have syntax errors in both files.

To check syntax errors in Nginx:

```bash
javiercruces@IWEB:~$ sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

If the output is correct, continue to check if you have made syntax errors in the PHP-FPM configuration:

```bash
javiercruces@IWEB:~$ sudo php-fpm8.2 -t
[02-Nov-2023 17:33:02] NOTICE: configuration file /etc/php/8.2/fpm/php-fpm.conf test is successful
```

Once the two outputs of these commands do not contain errors, we will restart both services to apply the configuration:

```bash
javiercruces@IWEB:/etc/nginx$ sudo systemctl restart php8.2-fpm nginx.service
```

### Operating check
To make sure that the server is working properly with PHP-FPM, we will create a file called info.php that will show information about PHP settings on the server. Next, I'll show you how to create the file:

```bash
javiercruces@IWEB:~$ sudo nano /var/www/html/info.php
```

Within the info.php file, add the following content:

```bash
<?php
phpinfo();
?>
```

Save and close the file

This PHP file will display detailed information about the PHP settings on your server. You can access it in your browser by visiting http: / / tudominio.com / info.php (replace tudominio.com with your real domain name) or you can also access it by putting your machine's IP in your browser.

![](../img/info-php.png)

Once this is done, you already have the LEMP battery installed for use in your CMS.