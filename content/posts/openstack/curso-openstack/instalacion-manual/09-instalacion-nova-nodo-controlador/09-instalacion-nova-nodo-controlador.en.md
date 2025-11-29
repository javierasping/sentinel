---
title: "09 - Install and configure Nova on the controller node"
date: 2025-11-23T12:00:00+00:00
description: "Step‑by‑step to deploy the Nova compute service on the OpenStack controller node."
tags: [openstack,installation,nova]
hero: images/openstack/instalacion-manual/instalar-configurar-nova-controlador.png
weight: 9
---

This document describes how to install and configure the Compute service (Nova) on the controller node (`controller01`).

## Prerequisites

Before starting, make sure you have the basic Keystone credentials and databases created (admin-openrc available).

## Create the databases (on `controller01`)

Connect to the SQL server as `root` to create the necessary databases:

```bash
vagrant@controller01:~$ sudo mysql
```

Create the `nova_api`, `nova`, and `nova_cell0` databases:

```sql
CREATE DATABASE nova_api;
CREATE DATABASE nova;
CREATE DATABASE nova_cell0;
```

Grant permissions to the `nova` account (replace `NOVA_DBPASS` with your password):

```sql
GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost' IDENTIFIED BY 'NOVA_DBPASS';
GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' IDENTIFIED BY 'NOVA_DBPASS';

GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' IDENTIFIED BY 'NOVA_DBPASS';
GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' IDENTIFIED BY 'NOVA_DBPASS';

GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'localhost' IDENTIFIED BY 'NOVA_DBPASS';
GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'%' IDENTIFIED BY 'NOVA_DBPASS';
```

Exit the client when finished:

```sql
exit;
```

## Create service credentials (on `controller01`)

Load the administrator environment variables to run Keystone commands:

```bash
vagrant@controller01:~$ source admin-openrc 
```

Create the `nova` service user (use `NOVA_PASSWORDS` as an example password):

```bash
vagrant@controller01:~$ openstack user create --domain default --password NOVA_PASSWORDS nova
```

Assign the `admin` role to user `nova` within the `service` project:

```bash
vagrant@controller01:~$ openstack role add --project service --user nova admin
```

Register the `nova` service entity in Keystone:

```bash
vagrant@controller01:~$ openstack service create --name nova --description "OpenStack Compute" compute
```

## Create the API endpoints (on `controller01`)

Create the public, internal and admin endpoints for the compute API:

```bash
vagrant@controller01:~$ openstack endpoint create --region RegionOne compute public http://controller01:8774/v2.1
vagrant@controller01:~$ openstack endpoint create --region RegionOne compute internal http://controller01:8774/v2.1
vagrant@controller01:~$ openstack endpoint create --region RegionOne compute admin http://controller01:8774/v2.1
```

## Install and configure Nova components (on `controller01`)

Install the controller packages needed on this node:

```bash
vagrant@controller01:~$ sudo apt install nova-api nova-conductor nova-novncproxy nova-scheduler -y
```

Edit `/etc/nova/nova.conf` and make the following changes:

```ini
[api_database]
connection = mysql+pymysql://nova:NOVA_DBPASS@controller01/nova_api

[database]
connection = mysql+pymysql://nova:NOVA_DBPASS@controller01/nova

[DEFAULT]
transport_url = rabbit://openstack:RABBIT_PASS@controller01:5672/
my_ip = 10.0.0.2

[keystone_authtoken]
www_authenticate_uri = http://controller01:5000/
auth_url = http://controller01:5000/
memcached_servers = controller01:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = nova
password = NOVA_PASS

[service_user]
send_service_user_token = true
auth_url = http://controller01:5000/v3
auth_type = password
project_domain_name = Default
project_name = service
user_domain_name = Default
username = nova
password = NOVA_PASS

[vnc]
enabled = true
server_listen = $my_ip
server_proxyclient_address = $my_ip

[glance]
api_servers = http://controller01:9292

[oslo_concurrency]
lock_path = /var/lib/nova/tmp

[placement]
region_name = RegionOne
project_domain_name = Default
project_name = service
auth_type = password
user_domain_name = Default
auth_url = http://controller01:5000/v3
username = placement
password = PLACEMENT_PASS
```

## Initialize Nova databases (on `controller01`)

Run the `nova-manage` commands to synchronize schemas and create the additional cell:

```bash
vagrant@controller01:~$ sudo su -s /bin/sh -c "nova-manage api_db sync" nova
vagrant@controller01:~$ sudo su -s /bin/sh -c "nova-manage cell_v2 map_cell0" nova
vagrant@controller01:~$ sudo su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --verbose" nova
vagrant@controller01:~$ sudo su -s /bin/sh -c "nova-manage db sync" nova
vagrant@controller01:~$ sudo su -s /bin/sh -c "nova-manage cell_v2 list_cells" nova
```

Verify that the cells are registered correctly (example output):

```bash
vagrant@controller01:~$ sudo su -s /bin/sh -c "nova-manage cell_v2 list_cells" nova
+-------+--------------------------------------+------------------------------------------+-------------------------------------------------+----------+
|  Name |                 UUID                 |              Transport URL               |               Database Connection               | Disabled |
+-------+--------------------------------------+------------------------------------------+-------------------------------------------------+----------+
| cell0 | 00000000-0000-0000-0000-000000000000 |                  none:/                  | mysql+pymysql://nova:****@controller/nova_cell0 |  False   |
| cell1 | 29e1ed74-59fa-43e3-9651-999d592a2cdf | rabbit://openstack:****@controller01:5672/ |    mysql+pymysql://nova:****@controller/nova    |  False   |
+-------+--------------------------------------+------------------------------------------+-------------------------------------------------+----------+
```

## Finalize installation (on `controller01`)

Restart the Nova services to apply the new configuration:

```bash
vagrant@controller01:~$ sudo service nova-api restart
vagrant@controller01:~$ sudo service nova-scheduler restart
vagrant@controller01:~$ sudo service nova-conductor restart
vagrant@controller01:~$ sudo service nova-novncproxy restart
```
