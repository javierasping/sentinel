---
title: "Instalación pila LAMP en debian 12"
date: 2023-10-28T10:00:00+00:00
description: Instalación pila LAMP
tags: [WordPress,CMS,IWEB,AW,debian,LAMP]
hero: /images/iweb/lamp/portada_lamp.png
---

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GVDYVWJLRH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GVDYVWJLRH');
</script>

# Instalación pila LAMP en Debian 12

Si estás utilizando Debian 12, sigue los pasos a continuación para instalar un servidor web LAMP completo en Debian GNU/Linux 12 "Bookworm" (Stable). Ten en cuenta que Debian 12 incluye PHP 8.2 en sus repositorios, lo que puede ser diferente de versiones anteriores de Debian.

## Instalación del servidor web

Lo primero en un servidor LAMP es la "A" de Apache. Para instalar Apache, ejecuta los siguientes comandos:

```bash
javiercruces@IWEB:~$ sudo apt install apache2
javiercruces@IWEB:~$ sudo systemctl enable apache2 && sudo systemctl start apache2
```

Con estos comandos, habrás instalado y activado el servidor web Apache. Puedes verificarlo escribiendo la IP del servidor en tu navegador favorito y debería mostrarte la página de inicio de Apache por defecto.

## Instalación de PHP 

Por lo general, necesitarás instalar algunos paquetes específicos para PHP, llamados modulos en funcion de la base de datos que utilices. Puedes instalarlos con el siguiente comando:

```bash
javiercruces@IWEB:~$ sudo apt install php8.2 libapache2-mod-php8.2 php8.2-mysql
```


Si instalas CMS como WordPress, Moodle o Prestashop en tu servidor, es posible que te pidan paquetes adicionales para su correcto funcionamiento. Estas aplicaciones suelen indicar claramente qué paquetes necesitas instalar.

Para que Apache aplique los cambios y active PHP, reinicia el servicio con el siguiente comando:

```bash
javiercruces@IWEB:~$ sudo systemctl restart apache2
```

## Instalación y configuración de MariaDB

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

Después de completar estos pasos, habrás configurado MariaDB y podrás conectarte a través de la terminal:

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

Con esto ya tendrías instalada la pila LAMP en debian 12 