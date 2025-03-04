---
title: "LAMP Stack Installation in Debian 12"
date: 2023-10-28T10:00:00+00:00
description: Learn how to install the LAMP stack on Debian 12.
tags: [WordPress, CMS, IWEB, AW, Debian, LAMP]
hero: /images/iweb/lamp/portada_lamp.png
---

## LAMP Stack Installation in Debian 12

If you are using Debian 12, follow the steps below to install a full LAMP web server on Debian GNU/Linux 12 "Bookworm" (Stable). Note that Debian 12 includes PHP 8.2 in its repositories, which may differ from previous Debian versions.

### Web Server Installation

The first component of a LAMP server is Apache, represented by the "A." To install Apache, run the following commands:

```bash
sudo apt install apache2
sudo systemctl enable apache2 && sudo systemctl start apache2
```

With these commands, you will have installed and activated the Apache web server. You can verify its functionality by entering the server's IP address in your favorite browser; it should display the default Apache home page.

## PHP Installation

You will likely need to install specific PHP packages, called modules, depending on the database you use. Install them with the following command:

```bash
sudo apt install php8.2 libapache2-mod-php8.2 php8.2-mysql
```

If you install a CMS like WordPress, Moodle, or Prestashop, additional packages may be required for proper operation. These applications usually indicate which packages need to be installed.

To apply the changes and activate PHP, restart Apache with the following command:

```bash
sudo systemctl restart apache2
```

## MariaDB Installation and Configuration

You can use either MariaDB or MySQL. In this case, we will use MariaDB:

```bash
sudo apt install mariadb-server
sudo systemctl enable mysql && sudo systemctl start mysql
```

During installation, you will be prompted to set a password for the MySQL root user. Once the installation is complete, run the following command to secure your MariaDB installation:

```bash
sudo mysql_secure_installation
```

Follow the instructions to enhance security, such as setting the root user password, removing anonymous users, and deleting test databases.

After completing these steps, you will have configured MariaDB and can connect through the terminal:

```bash
sudo mysql -u root -p
Enter password: 
Welcome to the MariaDB monitor. Commands end with ; or \g.
Your MariaDB connection id is 32
Server version: 10.11.4-MariaDB-1~deb12u1 Debian 12

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> 
```

With this, you now have a fully installed LAMP stack on Debian 12.
