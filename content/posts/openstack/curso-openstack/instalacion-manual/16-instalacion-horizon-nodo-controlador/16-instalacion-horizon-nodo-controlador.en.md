---
title: "16 - Install and configure Horizon on the controller node"
date: 2025-11-23T12:00:00+00:00
description: "Install the Horizon web dashboard to manage OpenStack from the GUI."
tags: [openstack,installation,horizon]
hero: images/openstack/instalacion-manual/instalar-configurar-horizon-controlador.png
weight: 16
---

This post explains how to install and configure the Horizon web dashboard on the controller node (`controller01`).

## Install required packages

```bash
sudo apt update
sudo apt install -y openstack-dashboard
```

## Edit Horizon main configuration

Edit `/etc/openstack-dashboard/local_settings.py` and ensure the following lines are set. Use `sudo` with `vim` or `nano` if preferred.

```bash
sudo nano /etc/openstack-dashboard/local_settings.py
```

Key entries:

```python
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

Note: change `volume: 2` to `volume: 3` because we use Cinder v3 endpoints. If you prefer v2, set `OPENSTACK_API_VERSIONS['volume'] = 2`.

## Adjust Apache configuration

Edit `/etc/apache2/conf-available/openstack-dashboard.conf` and add `WSGIApplicationGroup %{GLOBAL}` at the end to avoid Python module issues.

```apache
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

## Reload web server configuration

```bash
sudo service apache2 reload
```

You may need to run:

```bash
cd /usr/share/openstack-dashboard
sudo python3 manage.py compress
```

## Access Horizon

Open a browser and visit:

`http://controller01/horizon` or `http://<CONTROLLER_NODE_IP>/horizon`

Log in with a user created in Keystone (e.g., `admin` or a project user). The default domain is `Default`.

![](/images/openstack/instalacion-manual/iniciar-sesion-horizon.png)

![](/images/openstack/instalacion-manual/vista-general.png)

![](/images/openstack/instalacion-manual/instancias.png)

![](/images/openstack/instalacion-manual/instancia-consola.png)
