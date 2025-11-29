---
title: "07 - Install and configure Glance"
date: 2025-11-23T12:00:00+00:00
description: "Guide to install and configure Glance, OpenStack's image service, in your lab."
tags: [openstack,installation,glance]
hero: images/openstack/instalacion-manual/instalar-configurar-glance.png
weight: 7
---

At first glance, Glance may seem simple: it stores, manages, and serves images to the compute service (Nova). In this post I install and configure Glance on the `controller01` node, explain key components, and leave a minimal flow to upload a test image.

## Glance architecture

Components you'll see during installation:

- Glance API: exposes the REST API to store, list, and retrieve images.
- Glance Store: manages backends where image files are stored (file, Swift, Ceph, ...).
- Metadata / registry service: stores image metadata (in many deployments this functionality is integrated into the API and DB).

Glance uses an SQL database for state; here we use MySQL/MariaDB on the controller. In this guide we use the `file` backend for simplicity.

## Create the database

Connect to the database server as root and create the `glance` DB and grants:

```bash
sudo mysql <<'SQL'
CREATE DATABASE glance;
GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' IDENTIFIED BY 'GLANCE_DBPASS';
GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' IDENTIFIED BY 'GLANCE_DBPASS';
SQL
```

## Create the Glance user in Keystone

Load admin credentials:

```bash
source admin-openrc
```

Create the service user `glance` and grant `admin` in `service` project:

```bash
openstack user create --domain default --password GLANCE_ADMIN_PASSWORD glance
openstack role add --project service --user glance admin
```

Register the `glance` service and endpoints:

```bash
openstack service create --name glance --description "OpenStack Image" image
openstack endpoint create --region RegionOne image public   http://controller01:9292
openstack endpoint create --region RegionOne image internal http://controller01:9292
openstack endpoint create --region RegionOne image admin    http://controller01:9292
```

## Install packages and configure Glance

Install the package:

```bash
sudo apt install glance -y
```

Edit `/etc/glance/glance-api.conf`:

```ini
[database]
connection = mysql+pymysql://glance:GLANCE_DBPASS@controller01/glance

[keystone_authtoken]
www_authenticate_uri = http://controller01:5000
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

[DEFAULT]
enabled_backends = fs:file

[glance_store]
default_backend = fs

[fs]
filesystem_store_datadir = /var/lib/glance/images/

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

Sync the DB and restart:

```bash
sudo su -s /bin/sh -c "glance-manage db_sync" glance
sudo service glance-api restart
```

## Verify Glance

Download CirrOS and upload it:

```bash
source admin-openrc
wget http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img

glance image-create --name "cirros" \
  --file cirros-0.4.0-x86_64-disk.img \
  --disk-format qcow2 --container-format bare \
  --visibility=public

glance image-list
```

Glance is installed and verified with a test image.
