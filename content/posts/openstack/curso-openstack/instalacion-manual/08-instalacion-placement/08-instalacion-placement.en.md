---
title: "08 - Configure Placement in OpenStack"
date: 2025-11-23T12:00:00+00:00
description: "Configure the Placement service for tracking physical resources and scheduling in OpenStack."
tags: [openstack,installation,placement]
hero: images/openstack/instalacion-manual/instalar-configurar-placement.png
weight: 8
---

Placement tracks available physical resources and helps Nova schedule allocations. In this guide I will install and configure Placement on `controller01` using Ubuntu packages and provide the minimal steps to verify it.

## Prerequisites

Before starting, make sure you have:

- Keystone installed and reachable.
- A MySQL/MariaDB database available.
- Administrative credentials (`admin-openrc`) to create users and services.

## Create the database

Connect to the database server as `root` to create the Placement database:

```bash
vagrant@controller01:~$ sudo mysql
```

Create the database and grant permissions to user `placement` (replace `PLACEMENT_DBPASS`):

```sql
CREATE DATABASE placement;
GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'localhost' IDENTIFIED BY 'PLACEMENT_DBPASS';
GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'%' IDENTIFIED BY 'PLACEMENT_DBPASS';
```

Exit the client when finished.

## Create the user and service endpoints

Load your admin credentials to work with the OpenStack CLI:

```bash
vagrant@controller01:~$ source admin-openrc
```

Create the `placement` user in Keystone (use `PLACEMENT_PASSWORD` as an example password):

```bash
vagrant@controller01:~$ openstack user create --domain default --password PLACEMENT_PASSWORD placement
```

Add the `admin` role to the user within the `service` project:

```bash
vagrant@controller01:~$ openstack role add --project service --user placement admin
```

Register the Placement service in Keystone's catalog:

```bash
vagrant@controller01:~$ openstack service create --name placement --description "Placement API" placement
```

Create the public, internal, and admin endpoints pointing to port 8778:

```bash
vagrant@controller01:~$ openstack endpoint create --region RegionOne placement public   http://controller01:8778
vagrant@controller01:~$ openstack endpoint create --region RegionOne placement internal http://controller01:8778
vagrant@controller01:~$ openstack endpoint create --region RegionOne placement admin    http://controller01:8778
```

Note: the port may vary in your environment (for example 8780).

## Install the components

Install the Placement service package:

```bash
vagrant@controller01:~$ sudo apt install placement-api -y
```

## Configure Placement

Edit `/etc/placement/placement.conf` and set database and Keystone parameters:

```ini
[placement_database]
connection = mysql+pymysql://placement:PLACEMENT_DBPASS@controller01/placement

[api]
auth_strategy = keystone

[keystone_authtoken]
auth_url = http://controller01:5000/v3
memcached_servers = controller01:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = placement
password = PLACEMENT_PASS
```

## Sync DB and finalize

Run table creation with `placement-manage`:

```bash
vagrant@controller01:~$ sudo su -s /bin/sh -c "placement-manage db sync" placement
```

You can ignore deprecation warnings if they do not affect the process.

## Finalize the installation

Restart Apache (Placement is commonly served via mod_wsgi):

```bash
vagrant@controller01:~$ sudo service apache2 restart
```

## Verify

Check the status with `placement-status`:

```bash
vagrant@controller01:~$ sudo -u placement placement-status upgrade check
```

And test the Placement API by listing resource classes:

```bash
vagrant@controller01:~$ openstack --os-placement-api-version 1.2 resource class list --sort-column name
```

If you get a list (even if empty) without errors, Placement is operational.
