---
title: "LAMP battery installation in debian 12"
date: 2023-10-28T10:00:00+00:00
Description: LAMP battery installation
tags: [WordPress,CMS,IWEB,AW,debian,LAMP]
hero: /images/iweb/lamp/portada_lamp.png
---



♪ LAMP battery installation in Debian 12

If you are using Debian 12, follow the steps below to install a full LAMP web server on Debian GNU / Linux 12 "BookWorm" (Stable). Note that Debian 12 includes PHP 8.2 in your repositories, which may be different from previous Debian versions.

### Web server installation

The first thing on an LAMP server is Apache's "A." To install Apache, run the following commands:

```bash
javiercruces@IWEB:~$ sudo apt install apache2
javiercruces@IWEB:~$ sudo systemctl enable apache2 && sudo systemctl start apache2
```

With these commands, you will have installed and activated the Apache web server. You can check it by writing the server IP in your favorite browser and should show you the default Apache home page.

## PHP installation

You will usually need to install some specific PHP packages, called modules based on the database you use. You can install them with the following command:

```bash
javiercruces@IWEB:~$ sudo apt install php8.2 libapache2-mod-php8.2 php8.2-mysql
```


If you install CMS like WordPress, Moodle or Prestashop on your server, you may be asked for additional packages for proper operation. These applications often clearly indicate which packages you need to install.

For Apache to apply the changes and activate PHP, restart the service with the following command:

```bash
javiercruces@IWEB:~$ sudo systemctl restart apache2
```

## MariaDB installation and configuration

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

After completing these steps, you will have configured MariaDB and you can connect through the terminal:

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

With this you would already have installed the LAMP battery in debian 12 