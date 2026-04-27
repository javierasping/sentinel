---
title: "05 - Instalar y configurar Keystone en el nodo controlador"
date: 2025-11-23T12:00:00+00:00
description: "Paso a paso para instalar el servicio de identidad Keystone en el nodo controlador OpenStack."
tags: [openstack,instalacion,keystone]
hero: images/openstack/instalacion-manual/instalar-keystone-nodo-controlador.png
weight: 5
---

OpenStack está compuesto por múltiples servicios; Keystone (Identity) es el encargado de la autenticación, la autorización y la gestión del catálogo de servicios. En este post, instalaremos Keystone en el nodo `controller01`, analizaremos los archivos principales y verificaremos su funcionamiento.

Recuerda que es imprescindible haber completado los pasos detallados en el post anterior.

Todos los comandos de este post se realizan en el nodo `controller01`.

## Creación de la base de datos de Keystone

Conéctate al servidor de base de datos como root:

```bash
vagrant@controller01:~$ sudo mysql
```

Creación de la base de datos `keystone`:

```bash
MariaDB [(none)]> CREATE DATABASE keystone;
Query OK, 1 row affected (0.000 sec)
```

Creación de los usuarios y asignación de permisos para la base de datos `keystone`:

```bash
MariaDB [(none)]> CREATE USER 'keystone'@'localhost' IDENTIFIED BY 'KEYSTONE-DBPASS';
MariaDB [(none)]> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost';
MariaDB [(none)]> CREATE USER 'keystone'@'%' IDENTIFIED BY 'KEYSTONE-DBPASS';
MariaDB [(none)]> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%';
```

Finalmente, salimos del cliente de la base de datos:

```bash
MariaDB [(none)]> exit
Bye
```

## Configuración de Keystone

En este caso, utilizamos Apache con `mod_wsgi` para servir Keystone en el puerto 5000. Generalmente, el paquete crea la configuración necesaria en Apache de forma automática; aun así, es recomendable verificar que la configuración sea correcta.

Instalaremos los paquetes necesarios mediante el siguiente comando:

```bash
vagrant@controller01:~$ sudo apt install keystone apache2 libapache2-mod-wsgi-py3 -y
```

Editaremos el archivo `/etc/keystone/keystone.conf` para configurar la conexión a la base de datos:

```bash
[database]
connection = mysql+pymysql://keystone:KEYSTONE_DBPASS@10.0.0.2/keystone
```

Sustituye `KEYSTONE_DBPASS` por la contraseña que hayas definido para la base de datos.

En la sección `[token]`, indicaremos que utilizaremos Fernet:

```bash
[token]
provider = fernet
```

Actualizaremos la base de datos de Keystone mediante las migraciones del servicio, lo que creará las tablas necesarias:

```bash
vagrant@controller01:~$ sudo su -s /bin/sh -c "keystone-manage db_sync" keystone
```

Nota: las opciones `--keystone-user` y `--keystone-group` permiten ejecutar Keystone con un usuario o grupo distinto al predeterminado; en este caso, utilizamos `keystone`.

Inicializaremos las claves Fernet y las credenciales protegidas:

```bash
vagrant@controller01:~$ sudo keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
vagrant@controller01:~$ sudo keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
```

A continuación, realizaremos el bootstrap del servicio de identidad (proceso que crea el usuario `admin` y el proyecto `admin` iniciales):

```bash
vagrant@controller01:~$ sudo keystone-manage bootstrap --bootstrap-password ADMIN_PASS \
  --bootstrap-admin-url http://controller01:5000/v3/ \
  --bootstrap-internal-url http://controller01:5000/v3/ \
  --bootstrap-public-url http://controller01:5000/v3/ \
  --bootstrap-region-id RegionOne
```

Sustituye `ADMIN_PASS` por la contraseña que desees asignar al usuario administrador.

## Configuración del servidor web Apache

Editaremos el archivo `/etc/apache2/apache2.conf` para añadir la directiva `ServerName` apuntando al nodo controlador:

```bash
ServerName controller01
```

Tras realizar el cambio, reiniciaremos el servicio y verificaremos que se haya iniciado correctamente:

```bash
vagrant@controller01:~$ sudo systemctl restart apache2
vagrant@controller01:~$ sudo systemctl status apache2
```

En este caso, al tratarse de un laboratorio, no utilizaremos TLS/HTTPS, por lo que con esto finalizamos la configuración de Apache.

## Finalizar la instalación

Configuraremos la cuenta administrativa creando el archivo `admin-openrc` con las siguientes variables de entorno:

```bash
vagrant@controller01:~$ nano admin-openrc
export OS_USERNAME=admin
export OS_PASSWORD=keystone_auth_admin_password
export OS_PROJECT_NAME=admin
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_AUTH_URL=http://controller01:5000/v3
export OS_IDENTITY_API_VERSION=3
```

Estos valores son los asignados por defecto mediante el comando `keystone-manage bootstrap`.

Sustituye `ADMIN_PASS` por la contraseña utilizada en el comando `keystone-manage bootstrap`.

Finalmente, verificaremos que el archivo `admin-openrc` se ha creado correctamente cargando las variables de entorno:

```bash
vagrant@controller01:~$ source admin-openrc
```

Verificaremos que es posible generar un token para confirmar que Keystone responde correctamente:

```bash
vagrant@controller01:~$ openstack token issue
+------------+---------------------------------------------------------------------------------------------+
| Field      | Value                                                                                       |
+------------+---------------------------------------------------------------------------------------------+
| expires    | 2025-11-02T16:21:55+0000                                                                    |
| id         | gAAAAABpB3cTqXldQNcWEFfLFMOGJ1Rsl08mmHQna98Hl5Vy3f9q8blFddNvFH9JWATyAjJfcfi_6PfgGIIrnxLxTXx |
|            | 4A0zfn--                                                                                    |
|            | OHbGdxZna1PGYaoKJOP9ueu0j2czMT3DVIvDvsmBTkUMyL1-2s0WAwKYXngCwqiaN1BuWu8LHmDGzIYdKrRI        |
| project_id | 69782314638942ef831e8754cda5e41d                                                            |
| user_id    | f315a5bcf6574dd49846e6c3182989f9                                                            |
+------------+---------------------------------------------------------------------------------------------+
```

Si obtienes una salida similar, la instalación de Keystone en el nodo controlador se ha completado correctamente.