---
title: "14 - Install Cinder (controller node)"
date: 2025-11-23T12:00:00+00:00
description: "Install and configure Cinder, the block storage service, on the OpenStack controller node."
tags: [openstack,installation,cinder]
hero: images/openstack/instalacion-manual/instalar-configurar-cinder-controlador.png
weight: 14
---

This post details the steps we follow to install and configure **Cinder**, the OpenStack block storage service, on the controller node (`controller01`). We include the commands to create the database, configure services, endpoints and the Nova integration.

## Create the Cinder database

Access MySQL and create the database and user:

```bash
vagrant@controller01:~$ sudo mysql

CREATE DATABASE cinder;
GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'localhost' IDENTIFIED BY 'CINDER_DB_PASS';
GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'%' IDENTIFIED BY 'CINDER_DB_PASS';
EXIT;
```

## Create the Cinder user and assign the admin role

Load the admin credentials and create the `cinder` user in the `service` project:

```bash
. admin-openrc
openstack user create --domain default --password CINDER_SVC_PASS cinder
openstack role add --project service --user cinder admin

+---------------------+----------------------------------+
| Field               | Value                            |
+---------------------+----------------------------------+
| domain_id           | default                          |
| enabled             | True                             |
| id                  | 97735ce5873c42ac850e63f536a0eec9 |
| name                | cinder                           |
| options             | {}                               |
| password_expires_at | None                             |
---------------------+----------------------------------+
```

## Create Cinder services and endpoints

Create `cinderv2` and `cinderv3` services and endpoints for region `RegionOne`:

```bash
openstack service create --name cinderv2 --description "OpenStack Block Storage" volumev2
```

Example response:

```
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | OpenStack Block Storage          |
| enabled     | True                             |
| id          | c5c0d788373e4d88ae8526a95269f4c4 |
| name        | cinderv2                         |
| type        | volumev2                         |
+-------------+----------------------------------+
```

```bash
openstack service create --name cinderv3 --description "OpenStack Block Storage" volumev3
```

For Cinder v2 endpoints:

```bash
openstack endpoint create --region RegionOne volumev2 public  http://controller01:8776/v2/%\(project_id\)s
openstack endpoint create --region RegionOne volumev2 internal http://controller01:8776/v2/%\(project_id\)s
openstack endpoint create --region RegionOne volumev2 admin    http://controller01:8776/v2/%\(project_id\)s
```

For Cinder v3 endpoints:

```bash
openstack endpoint create --region RegionOne volumev3 public  http://controller01:8776/v3/%\(project_id\)s
openstack endpoint create --region RegionOne volumev3 internal http://controller01:8776/v3/%\(project_id\)s
openstack endpoint create --region RegionOne volumev3 admin    http://controller01:8776/v3/%\(project_id\)s
```

## Install Cinder packages

```bash
sudo apt install -y cinder-api cinder-scheduler
```

## Configure the database and RabbitMQ

Edit `/etc/cinder/cinder.conf` and include the following parameters:

```ini
[database]
connection = mysql+pymysql://cinder:CINDER_DB_PASS@controller01/cinder

[DEFAULT]
transport_url = rabbit://openstack:RABBIT_PASS@controller01
```

## Configure Keystone access

Add Keystone parameters in the same file:

```ini
[DEFAULT]
auth_strategy = keystone

[keystone_authtoken]
auth_uri = http://controller01:5000
auth_url = http://controller01:5000
memcached_servers = controller01:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = cinder
password = KEYSTONE_SVC_PASS
```

## Configure node IP and lock_path

```ini
[DEFAULT]
my_ip = 10.0.0.11
oslo_concurrency.lock_path = /var/lib/cinder/tmp
```

## Sync the Cinder database

```bash
vagrant@controller01:~$ sudo su -s /bin/sh -c "cinder-manage db sync" cinder
```

## Configure Nova to use Cinder

Add the Cinder region to Nova configuration `/etc/nova/nova.conf`:

```ini
[cinder]
os_region_name = RegionOne
```

## Restart services

```bash
sudo service nova-api restart
sudo service cinder-scheduler restart
sudo service apache2 restart
```

## Verify Cinder is working

```bash
. admin-openrc
vagrant@controller01:~$ openstack volume service list
```

Example output:

```
+------------------+--------------+------+---------+-------+----------------------------+
| Binary           | Host         | Zone | Status  | State | Updated At                 |
+------------------+--------------+------+---------+-------+----------------------------+
| cinder-scheduler | controller01 | nova | enabled | up    | 2025-11-23T02:21:13.000000 |
+------------------+--------------+------+---------+-------+----------------------------+
```

Note: if any service shows `State` other than `up` or `enabled`, check the logs under `/var/log/cinder/`.
