---
title: "16 - Instalar y configurar Horizon en el nodo controlador"
date: 2025-11-23T12:00:00+00:00
description: "Instalamos el panel web Horizon para gestionar OpenStack desde la interfaz gráfica."
tags: [openstack,instalacion,horizon]
hero: ""
weight: 16
---

# Instalación del panel Horizon en OpenStack (nodo controlador)

Explicamos de forma sencilla cómo instalar y configurar el panel web Horizon en el nodo controlador (`controller01`). Todos los comandos muestran el prompt `vagrant@controller01:~$` y usan `sudo` cuando procede.

## 1) Instalar los paquetes necesarios

```bash
vagrant@controller01:~$ sudo apt update
vagrant@controller01:~$ sudo apt install -y openstack-dashboard
```

## 2) Editar la configuración principal de Horizon

Editamos el fichero `/etc/openstack-dashboard/local_settings.py` y nos aseguramos de que contiene las siguientes líneas modificadas o añadidas. Si preferimos editar con `vim` o `nano`, usamos `sudo`.

```bash
vagrant@controller01:~$ sudo nano /etc/openstack-dashboard/local_settings.py
```
Modificamos las siguientes entradas en `local_settings.py`:

```bash
OPENSTACK_HOST = "controller01"

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

CACHES = {
    'default': {
         'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
         'LOCATION': 'controller01:11211',
    }
}

OPENSTACK_KEYSTONE_URL = "http://%s:5000/v3" % OPENSTACK_HOST

OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = True

OPENSTACK_API_VERSIONS = {
    "identity": 3,
    "image": 2,
    "volume": 3,
}

OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = "Default"

OPENSTACK_KEYSTONE_DEFAULT_ROLE = "user"
```

Nota: cambiamos `volume: 2` por `volume: 3` porque usamos endpoints v3 para Cinder. Si preferimos usar v2 modificamos `OPENSTACK_API_VERSIONS['volume']` a `2`.

## 3) Ajustar la configuración de Apache

Editamos `/etc/apache2/conf-available/openstack-dashboard.conf` y añadimos la línea `WSGIApplicationGroup %{GLOBAL}` (al final del fichero) para evitar problemas con módulos Python.

```bash
WSGIScriptAlias /horizon /usr/share/openstack-dashboard/openstack_dashboard/wsgi.py process-group=horizon
WSGIDaemonProcess horizon user=horizon group=horizon processes=3 threads=10 display-name=%{GROUP}
WSGIProcessGroup horizon
WSGIApplicationGroup %{GLOBAL}
Alias /static /var/lib/openstack-dashboard/static/
Alias /horizon/static /var/lib/openstack-dashboard/static/
<Directory /usr/share/openstack-dashboard/openstack_dashboard>
  Require all granted
</Directory>
<Directory /var/lib/openstack-dashboard/static>
  Require all granted
</Directory>
```

Este ajuste evita errores con ciertos módulos Python usados por Horizon.

## 4) Recargar la configuración del servidor web

```bash
vagrant@controller01:~$ sudo service apache2 reload
```

Puede que necesitemos ejecutar esto:

> Note
> vagrant@controller01:/usr/share/openstack-dashboard$ sudo python3 manage.py compress

## 5) Acceder a Horizon

Abrimos un navegador y visitamos:

`http://10.0.0.11/horizon`

Iniciamos sesión con un usuario creado en Keystone (por ejemplo `admin` o un usuario de proyecto).

---