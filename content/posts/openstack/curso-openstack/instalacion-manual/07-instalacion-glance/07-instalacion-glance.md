---
title: "07 - Instalar y configurar Glance"
date: 2025-11-23T12:00:00+00:00
description: "Guía para instalar y configurar Glance, el servicio de imágenes de OpenStack, en tu laboratorio."
tags: [openstack,instalacion,glance]
hero: images/openstack/instalacion-manual/instalar-configurar-glance.png
weight: 7
---

A primera vista, Glance puede parecer un servicio sencillo; su función principal es almacenar, gestionar y servir imágenes al servicio de cómputo (Nova). En este post, instalaremos y configuraremos Glance en el nodo `controller01`, analizaremos sus componentes clave y estableceremos un flujo básico para cargar una imagen de prueba.

## Arquitectura de Glance

Te resumo los componentes que verás durante la instalación:

- Glance API: expone la API REST para almacenar, listar y recuperar imágenes.
- Glance Store: gestiona los backends donde se alojan los ficheros de imagen (file, Swift, Ceph, ...).
- Servicio de metadatos / registry: guarda metadatos de las imágenes (en muchos despliegues esta funcionalidad está integrada en la API y en la DB).

Glance usa una base de datos SQL para su estado, aquí usamos MySQL/MariaDB en el controlador.

En esta guía uso el backend `file` (ficheros en el sistema local) por simplicidad.

Recuerda que es imprescindible haber completado los pasos detallados en los posts anteriores antes de comenzar con la instalación de Glance.

## Creación de la base de datos

Antes de instalar y configurar el servicio de imágenes, debemos crear la base de datos, las credenciales del servicio y los endpoints de la API.

Nos conectamos al servidor de base de datos como usuario root:

```bash
vagrant@controller01:~$ sudo mysql
```

Creo la base de datos `glance`:

```bash
MariaDB [(none)]> CREATE DATABASE glance;
Query OK, 1 row affected (0.000 sec)
```

Asignaremos permisos al usuario `glance` (sustituye `GLANCE_DBPASS` por la contraseña definida):

```bash
GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' IDENTIFIED BY 'GLANCE_DBPASS';
GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' IDENTIFIED BY 'GLANCE_DBPASS';
```

Finalmente, salimos del cliente de la base de datos:

```bash
MariaDB [(none)]> exit
```

## Creación del usuario Glance en Keystone

Cargo las credenciales de administrador para trabajar con la CLI:

```bash
vagrant@controller01:~$ source admin-openrc
```

Crea el usuario de servicio `glance` (usa `GLANCE_ADMIN_PASSWORD` para la contraseña):

```bash
vagrant@controller01:~$ openstack user create --domain default --password GLANCE_ADMIN_PASSWORD glance
+---------------------+----------------------------------+
| Field               | Value                            |
+---------------------+----------------------------------+
| default_project_id  | None                             |
| domain_id           | default                          |
| email               | None                             |
| enabled             | True                             |
| id                  | b1e94e5fb65b401280d1ac816ada0ac4 |
| name                | glance                           |
| description         | None                             |
| password_expires_at | None                             |
++---------------------+----------------------------------+
```

Añade el rol `admin` al usuario `glance` en el proyecto `service`:

```bash
vagrant@controller01:~$ openstack role add --project service --user glance admin
```

Registro el servicio `glance` en Keystone:

```bash
vagrant@controller01:~$ openstack service create --name glance --description "OpenStack Image" image
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| id          | e82241015cf24034a0209b70c812ff1a |
| name        | glance                           |
| type        | image                            |
| enabled     | True                             |
| description | OpenStack Image                  |
+-------------+----------------------------------+
```

## Creación de los Endpoints de Glance

Crea los endpoints (public, internal, admin) apuntando a `http://controller01:9292`:

```bash
vagrant@controller01:~$ openstack endpoint create --region RegionOne image public http://controller01:9292
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | 59ae3c4723674e5491beba4b430e60c7 |
| interface    | public                           |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | e82241015cf24034a0209b70c812ff1a |
| service_name | glance                           |
| service_type | image                            |
| url          | http://controller01:9292           |
+--------------+----------------------------------+
vagrant@controller01:~$ openstack endpoint create --region RegionOne image internal http://controller01:9292
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | 203682a7d7ca46c8941aa12c1dac5332 |
| interface    | internal                         |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | e82241015cf24034a0209b70c812ff1a |
| service_name | glance                           |
| service_type | image                            |
| url          | http://controller01:9292           |
+--------------+----------------------------------+
vagrant@controller01:~$ openstack endpoint create --region RegionOne image admin http://controller01:9292
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | 233aa6af772643f6ba9c3b64719796e2 |
| interface    | admin                            |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | e82241015cf24034a0209b70c812ff1a |
| service_name | glance                           |
| service_type | image                            |
| url          | http://controller:9292           |
+--------------+----------------------------------+
```

Si quieres activar límites de cuota para Glance, debes registrar los recursos en Keystone (opcional). Asegúrate además de activar `use_keystone_limits=True` en `glance-api.conf` si vas a usar este mecanismo.

## Instalación de paquetes y configuración de Glance

Instala el paquete `glance` en el controlador:

```bash
vagrant@controller01:~$ sudo apt install glance -y 
```

Edita el fichero de configuración principal:

```bash
vagrant@controller01:~$ sudo nano /etc/glance/glance-api.conf
```

En `[database]` configuro Glance para que apunte a la base de datos que creé anteriormente:

```bash
[database]
connection = mysql+pymysql://glance:GLANCE_DBPASS@controller01/glance
```

En las secciones `[keystone_authtoken]` y `[paste_deploy]`, configuraremos la conexión con Keystone (sustituye `GLANCE_PASS` por la contraseña del usuario `glance`):

```bash
[keystone_authtoken]
www_authenticate_uri  = http://controller01:5000
auth_url = http://controller01:5000
memcached_servers = controller01:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = glance
password = GLANCE_PASS

[paste_deploy]
flavor = keystone

```

En la sección `[glance_store]`, habilitaremos el backend local y el destino de las imágenes:

```bash
[DEFAULT]
enabled_backends=fs:file

[glance_store]
default_backend = fs

[fs]
filesystem_store_datadir = /var/lib/glance/images/
```

En la sección `[oslo_limit]`, configuraremos el acceso a Keystone (en caso de utilizar el cliente unificado de límites):

```bash
[oslo_limit]
auth_url = http://controller01:5000
auth_type = password
user_domain_id = default
username = glance
system_scope = all
password = GLANCE_PASS
endpoint_id = ENDPOINT_ID
region_name = RegionOne
```

Sustituye `GLANCE_PASS` por la contraseña del usuario `glance` en el servicio Identity.

Sustituye `ENDPOINT_ID` por el ID del endpoint de imagen creado anteriormente, el cual puedes obtener mediante:

```bash
vagrant@controller01:~$ openstack endpoint list --service glance --region RegionOne
+--------------------+-----------+--------------+--------------+---------+-----------+---------------------+
| ID                 | Region    | Service Name | Service Type | Enabled | Interface | URL                 |
+--------------------+-----------+--------------+--------------+---------+-----------+---------------------+
| 203682a7d7ca46c894 | RegionOne | glance       | image        | True    | internal  | http://controller:9 |
| 1aa12c1dac5332     |           |              |              |         |           | 292                 |
| 233aa6af772643f6ba | RegionOne | glance       | image        | True    | admin     | http://controller:9 |
| 9c3b64719796e2     |           |              |              |         |           | 292                 |
| 59ae3c4723674e5491 | RegionOne | glance       | image        | True    | public    | http://controller:9 |
| beba4b430e60c7     |           |              |              |         |           | 292                 |
+--------------------+-----------+--------------+--------------+---------+-----------+---------------------+
```

Asegúrate de que la cuenta `glance` tenga permisos de lectura sobre los recursos con alcance de sistema (system-scope), como los límites:

```bash
vagrant@controller01:~$ openstack role add --user glance --user-domain Default --system all reader
```

Consulta la documentación de `oslo_limit` para más información sobre la configuración del cliente unificado de límites.

En la sección `[DEFAULT]`, puedes habilitar opcionalmente las cuotas por tenant:

```bash
[DEFAULT]
use_keystone_limits = True
```

Ten en cuenta que, si activas esta opción, debes haber creado previamente los límites registrados (registered limits) según se indica arriba.

Una vez finalizada la configuración del servicio, crearemos las tablas en la base de datos:

```bash
vagrant@controller01:~$ sudo su -s /bin/sh -c "glance-manage db_sync" glance
Database is synced successfully.
```

Reiniciaremos el servicio de Glance:

```bash
vagrant@controller01:~$ sudo service glance-api restart
```

## Verificación de la instalación de Glance

Verificaremos el funcionamiento del servicio de imágenes utilizando CirrOS, una imagen Linux ligera ideal para probar despliegues de OpenStack.

Cargaremos las credenciales de administrador para ejecutar los comandos de la CLI con los privilegios necesarios:

```bash
vagrant@controller01:~$ source admin-openrc
```

Descargaremos la imagen de prueba (CirrOS):

```bash
vagrant@controller01:~$ wget http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img
```

Subiremos la imagen al servicio Glance (formato QCOW2, contenedor `bare` y visibilidad pública):

```bash
vagrant@controller01:~$ glance image-create --name "cirros" \
  --file cirros-0.4.0-x86_64-disk.img \
  --disk-format qcow2 --container-format bare \
  --visibility=public
+------------------+----------------------------------------------------------------------------------+
| Property         | Value                                                                            |
+------------------+----------------------------------------------------------------------------------+
| checksum         | 443b7623e27ecf03dc9e01ee93f67afe                                                 |
| container_format | bare                                                                             |
| created_at       | 2025-11-02T18:15:48Z                                                             |
| disk_format      | qcow2                                                                            |
| id               | ecd8e173-2c2a-4c0e-b019-2e7d55393a96                                             |
| min_disk         | 0                                                                                |
| min_ram          | 0                                                                                |
| name             | cirros                                                                           |
| os_hash_algo     | sha512                                                                           |
| os_hash_value    | 6513f21e44aa3da349f248188a44bc304a3653a04122d8fb4535423c8e1d14cd6a153f735bb0982e |
|                  | 2161b5b5186106570c17a9e58b64dd39390617cd5a350f78                                 |
| os_hidden        | False                                                                            |
| owner            | 69782314638942ef831e8754cda5e41d                                                 |
| protected        | False                                                                            |
| size             | 12716032                                                                         |
| status           | active                                                                           |
| stores           | fs                                                                               |
| tags             | []                                                                               |
| updated_at       | 2025-11-02T18:15:49Z                                                             |
| virtual_size     | 46137344                                                                         |
| visibility       | public                                                                           |
+------------------+----------------------------------------------------------------------------------+
```

Verificaremos la lista de imágenes para validar que la subida se ha realizado correctamente:

```bash
vagrant@controller01:~$ glance image-list
+--------------------------------------+--------+
| ID                                   | Name   |
+--------------------------------------+--------+
| ecd8e173-2c2a-4c0e-b019-2e7d55393a96 | cirros |
+--------------------------------------+--------+
```

Con estos pasos, Glance habrá quedado instalado y verificado mediante la carga de una imagen de prueba.