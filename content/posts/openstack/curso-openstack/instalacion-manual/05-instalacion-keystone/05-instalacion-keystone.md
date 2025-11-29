---
title: "05 - Instalar y configurar Keystone en el nodo controlador"
date: 2025-11-23T12:00:00+00:00
description: "Paso a paso para instalar el servicio de identidad Keystone en el nodo controlador OpenStack."
tags: [openstack,instalacion,keystone]
hero: images/openstack/instalacion-manual/instalar-keystone-nodo-controlador.png
weight: 5
---

OpenStack está formado por muchos servicios, Keystone (Identity) se encarga de la autenticación, autorización y del catálogo de servicios. En este post instalaré Keystone en el nodo `controller01`, explicaré los ficheros principales y comprobaré que funciona.

Recuerda que es necesario haber completado los pasos del post anterior.

Todos los comandos de este post se realizan en el nodo `controller01`.

## Creación de la base de datos de Keystone

Conéctate al servidor de base de datos como root:

```bash
vagrant@controller01:~$ sudo mysql
```

Crea la base de datos `keystone`:

```bash
MariaDB [(none)]> CREATE DATABASE keystone;
Query OK, 1 row affected (0.000 sec)
```

Crea los usuarios y concédeles permisos para la base de datos `keystone`:

```bash
MariaDB [(none)]> CREATE USER 'keystone'@'localhost' IDENTIFIED BY 'KEYSTONE-DBPASS';
MariaDB [(none)]> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost';
MariaDB [(none)]> CREATE USER 'keystone'@'%' IDENTIFIED BY 'KEYSTONE-DBPASS';
MariaDB [(none)]> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%';
```

Por último, sal del cliente de base de datos:

```bash
MariaDB [(none)]> exit
Bye
```

## Configuración de Keystone

En mi caso uso Apache con mod_wsgi para servir Keystone en el puerto 5000, el paquete suele crear la configuración necesaria en Apache automáticamente. Aún así, comprueba que la configuración es correcta en tu caso.

Instala los paquetes necesarios con el siguiente comando:

```bash
vagrant@controller01:~$ sudo apt install keystone apache2 libapache2-mod-wsgi-py3 -y
```

Edita el fichero `/etc/keystone/keystone.conf` y configura la conexión a la base de datos:

```bash
[database]
connection = mysql+pymysql://keystone:KEYSTONE_DBPASS@10.0.0.2/keystone
```

Sustituye `KEYSTONE_DBPASS` por la contraseña que hayas elegido para la base de datos.

En la sección `[token]` indica que usas Fernet:

```bash
[token]
provider = fernet
```

Actualiza la base de datos de Keystone con las migraciones del servicio, esto creará las tablas dentro de la base de datos:

```bash
vagrant@controller01:~$ sudo su -s /bin/sh -c "keystone-manage db_sync" keystone
```

Nota: las opciones `--keystone-user` y `--keystone-group` permiten ejecutar keystone con un usuario/grupo distinto del por defecto, en mi caso usamos `keystone`.

Inicializa las claves Fernet y las credenciales protegidas:

```bash
vagrant@controller01:~$ sudo keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
vagrant@controller01:~$ sudo keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
```

Ahora realizo el bootstrap del servicio Identity (esto crea el usuario `admin` y el proyecto `admin` iniciales):

```bash
vagrant@controller01:~$ sudo keystone-manage bootstrap --bootstrap-password ADMIN_PASS \
  --bootstrap-admin-url http://controller01:5000/v3/ \
  --bootstrap-internal-url http://controller01:5000/v3/ \
  --bootstrap-public-url http://controller01:5000/v3/ \
  --bootstrap-region-id RegionOne
```

Sustituye `ADMIN_PASS` por la contraseña que quieras usar para el usuario administrador.

## Configuración del servidor web Apache

Edita el fichero `/etc/apache2/apache2.conf` y añade la opción `ServerName` apuntando al nodo controlador:

```bash
ServerName controller01
```

Luego de realizar el cambio, reinicia el servicio y asegúrate de que está levantado:

```bash
vagrant@controller01:~$ sudo systemctl restart apache2
vagrant@controller01:~$ sudo systemctl status apache2
```

En nuestro caso no usaremos TLS/HTTPS ya que es un laboratorio, así que con esto hemos finalizado la configuración de Apache.

## Finalizar la instalación

Configura la cuenta administrativa creando un fichero `admin-openrc` con las siguientes variables de entorno:

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

Estos valores son los que crea `keystone-manage bootstrap` por defecto.

Sustituye `ADMIN_PASS` por la contraseña que usaste en el comando `keystone-manage bootstrap`.

Por ultimo ,comprueba que `admin-openrc` se ha creado correctamente cargando las variables:

```bash
vagrant@controller01:~$ source admin-openrc
```

Comprueba que eres capaz de generar un token para verificar que Keystone responde correctamente:

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

Si has obtenido una salida similar a esta, la instalación de Keystone en el nodo controlador ha finalizado.