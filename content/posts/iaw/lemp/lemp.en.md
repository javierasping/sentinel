---
title: "LEMP Stack Installation in Debian 12 with PHP 8"
date: 2023-10-28T10:00:00+00:00
description: Learn how to install the LEMP stack on Debian 12 with PHP 8.
tags: [WordPress, CMS, IWEB, AW, Debian, LEMP]
hero: /images/iweb/lamp/portada_lemp.png
---

## LEMP Stack Installation in Debian 12 with PHP 8

In this guide, we will go through the steps to install a LEMP stack (Linux, Nginx, MariaDB, and PHP) on a Debian 12 server. The configuration includes PHP 8.2 as the main version. The LEMP stack is essential for hosting PHP-based websites and applications, such as WordPress or other dynamic applications. Follow the detailed steps below to configure your LEMP server with PHP 8.2.

### Prerequisites

Before starting, ensure you meet the following requirements:

- A Linux server.
- A non-root user with sudo privileges.
- A fully qualified domain name (FQDN) that points to the server.

First, update and upgrade the system packages:

```bash
sudo apt update && sudo apt upgrade -y
```

Additionally, install the following essential packages:

```bash
sudo apt install wget nano unzip tar -y
```

## PHP Installation

Debian 12 includes PHP 8.2 by default. Install it using the following command:

```bash
sudo apt install php-fpm php-cli php-mysql php-mbstring php-xml php-gd -y
```

This installs PHP along with MySQL, CLI, GD, Mbstring, and XML extensions. You can install additional extensions based on your requirements. To verify the PHP installation, run:

```bash
php --version
```

## MariaDB Installation

You can use either MariaDB or MySQL. In this case, we will use MariaDB:

```bash
sudo apt install mariadb-server -y
sudo systemctl enable mysql && sudo systemctl start mysql
```

During installation, you will be prompted to set a password for the MySQL root user. Once installation is complete, secure your MariaDB installation with:

```bash
sudo mysql_secure_installation
```

Follow the instructions to enhance security, such as setting the root user password, removing anonymous users, and deleting test databases.

To verify MariaDB, log in via the terminal:

```bash
sudo mysql -u root -p
Enter password: 
```

## Nginx Installation

To install Nginx, run:

```bash
sudo apt install nginx -y
```

Once Nginx is installed, configure PHP-FPM to use a TCP socket.

Open the PHP-FPM configuration file:

```bash
sudo nano /etc/php/8.2/fpm/pool.d/www.conf
```

Find the following line and comment it out:

```bash
;listen = /run/php/php8.2-fpm.sock
```

Then, replace it with:

```bash
listen = 127.0.0.1:9000
```

Save and close the file.

Now, configure Nginx to work with PHP-FPM by editing the default server block:

```bash
sudo nano /etc/nginx/sites-available/default
```

Modify the file as follows:

```bash
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.php index.htm index.nginx-debian.html;

    server_name _;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass 127.0.0.1:9000;
        include fastcgi_params;
    }
}
```

Save the changes and exit.

## Testing Configuration and Restarting Services

Check for syntax errors in Nginx:

```bash
sudo nginx -t
```

Check PHP-FPM configuration:

```bash
sudo php-fpm8.2 -t
```

If no errors are found, restart both services:

```bash
sudo systemctl restart php8.2-fpm nginx
```

## Verifying PHP Processing

Create a test PHP file to confirm PHP processing:

```bash
sudo nano /var/www/html/info.php
```

Add the following content:

```php
<?php
phpinfo();
?>
```

Save and close the file. You can access it in your browser at:

```
http://your_domain_or_IP/info.php
```

If PHP information is displayed, your LEMP stack is correctly installed.

![](/iaw/lemp/img/info-php.png)

With this, you now have a fully installed and configured LEMP stack on Debian 12.
