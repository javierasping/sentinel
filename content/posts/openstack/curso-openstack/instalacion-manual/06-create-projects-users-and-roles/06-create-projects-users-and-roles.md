---
title: "06 - Crear dominios, proyectos, usuarios y roles en OpenStack"
date: 2025-11-23T12:00:00+00:00
description: "Aprende a organizar tu entorno OpenStack creando dominios, proyectos, usuarios y roles correctamente."
tags: [openstack,instalacion,identity]
hero: ""
weight: 6
---

Identity (Keystone) es el servicio de autenticación y autorización de OpenStack. En este paso voy a preparar la configuración mínima de Identity que necesitamos para continuar con la instalación y para poder probar la OpenStack.

Aunque el dominio `default` ya existe tras el `keystone-manage bootstrap`, voy a crear de forma explícita los proyectos y usuarios que usamos en las guías: `service` (para los usuarios de servicio) y `demo` (para pruebas de usuarios no administrativos). También crearé un rol de ejemplo y lo asignaré al usuario `demo`.

Cuando muestro contraseñas en los ejemplos lo hago por claridad; si prefieres, usa `--password-prompt` para introducir la contraseña de forma interactiva y segura.

## Crear el proyecto `service`

Como administrador, creo el proyecto `service` con el siguiente comando:

```bash
vagrant@controller01:~$ openstack project create --domain default   --description "Service Project" service
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | Service Project                  |
| domain_id   | default                          |
| enabled     | True                             |
| id          | bb95b976bb784cd3af2bed62cd86a3e2 |
| is_domain   | False                            |
| name        | service                          |
| options     | {}                               |
| parent_id   | default                          |
| tags        | []                               |
+-------------+----------------------------------+
```

## Crear el proyecto `demo`

Creamos un proyecto `demo` que servirá para pruebas y uso por parte de usuarios no administrativos:

```bash
vagrant@controller01:~$ openstack project create --domain default   --description "Service Project" demo
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | Service Project                  |
| domain_id   | default                          |
| enabled     | True                             |
| id          | 9f8438d7b08d4c508ae42e377a7beb9e |
| is_domain   | False                            |
| name        | demo                             |
| options     | {}                               |
| parent_id   | default                          |
| tags        | []                               |
+-------------+----------------------------------+
```

## Crear el usuario `demo`

Ahora creo el usuario `demo` dentro del dominio `default`. En este ejemplo muestro la contraseña en claro (`demo`) por simplicidad:

```bash
vagrant@controller01:~$ openstack user create --domain default --password demo demo
+---------------------+----------------------------------+
| Field               | Value                            |
+---------------------+----------------------------------+
| default_project_id  | None                             |
| domain_id           | default                          |
| email               | None                             |
| enabled             | True                             |
| id                  | ca874cb3aa4e47459b62faf425c947b0 |
| name                | demo                             |
| description         | None                             |
| password_expires_at | None                             |
+---------------------+----------------------------------+
```

## Crear el rol y asignarlo al usuario `demo` en el proyecto `demo`

Creo un rol llamado `demo` y se lo asigno al usuario `demo` dentro del proyecto `demo`:

```bash
vagrant@controller01:~$ openstack role create demo
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| id          | 27c7cf177060470b8c89c80a1efc7902 |
| name        | demo                             |
| domain_id   | None                             |
| description | None                             |
+-------------+----------------------------------+
```

Asigno el rol al usuario dentro del proyecto:

```bash
vagrant@controller01:~$ openstack role add --project demo --user demo demo
```

Nota: este comando no produce salida en la CLI cuando se ejecuta con éxito.

## Fichero `demo-openrc` de ejemplo y verificación

Creo un fichero `demo-openrc` con las variables de entorno del usuario `demo`. Adáptalo si tu entorno usa otras URLs o dominios:

```bash
vagrant@controller01:~$ cat demo-openrc
export OS_USERNAME=demo
export OS_PASSWORD=demo
export OS_PROJECT_NAME=demo
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_AUTH_URL=http://controller01:5000/v3
export OS_IDENTITY_API_VERSION=3

```

Para verificar que la autenticación funciona con `demo`, cargo las variables y pido un token:

```bash
vagrant@controller01:~$ source demo-openrc
vagrant@controller01:~$ openstack token issue
+------------+---------------------------------------------------------------------------------------------+
| Field      | Value                                                                                       |
+------------+---------------------------------------------------------------------------------------------+
| expires    | 2025-11-02T16:43:14+0000                                                                    |
| id         | gAAAAABpB3wSv6IlsyDStWPZoJ_tPmdoDZkmYaQ7-tP9JMGejt-                                         |
|            | 3obxjuLzFZ33S3oJeHYGOBTI2k76hY7jLgGdj6C245ZYyNJEQMmRlfYi5m2ROKIzjCh4bytTDlRCO0tiOE8FW_0Veqz |
|            | 4PZpzHEXiJ9KSoJFd3D0iKrpMF2NXc8EzBFF1r_So                                                   |
| project_id | 9f8438d7b08d4c508ae42e377a7beb9e                                                            |
| user_id    | ca874cb3aa4e47459b62faf425c947b0                                                            |
+------------+---------------------------------------------------------------------------------------------+
```

Con esto concluyo la configuración básica de proyectos, usuarios y roles necesarios para continuar con la instalación de otros servicios.