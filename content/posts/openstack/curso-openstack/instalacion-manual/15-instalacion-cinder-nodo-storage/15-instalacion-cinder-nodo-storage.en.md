---
title: "15 - Install and configure Cinder on storage nodes"
date: 2025-11-23T12:00:00+00:00
description: "Install and configure Cinder on storage nodes using LVM in OpenStack."
tags: [openstack,installation,cinder]
hero: images/openstack/instalacion-manual/instalar-configurar-cinder-storage.png
weight: 15
---

This post explains how to install and configure OpenStack's volume service (Cinder) on a storage node using LVM.

Note: run commands on the storage node (`storage01`) and use them as shown.

## Install required packages

```bash
sudo apt install -y lvm2 thin-provisioning-tools
```

## Verify the `/dev/vdb` disk

```bash
fdisk -l
```

Make sure `/dev/vdb` appears and has no partitions before continuing.

## Create the LVM physical volume

```bash
sudo pvcreate /dev/vdb
```

## Create the `cinder-volumes` volume group

```bash
sudo vgcreate cinder-volumes /dev/vdb
```

## Edit `/etc/lvm/lvm.conf`

Under the `devices` section, add or modify the `filter` line to prevent LVM from scanning unwanted disks:

```conf
filter = [ "a/sda/", "a/vdb/", "r/.*/"]
```

## Install the Cinder Volume service

```bash
sudo apt install -y cinder-volume
```

## Configure DB and RabbitMQ

Edit `/etc/cinder/cinder.conf`:

```ini
[database]
connection = mysql+pymysql://cinder:CINDER_DB_PASS@controller01/cinder

[DEFAULT]
transport_url = rabbit://openstack:openstack@controller01
```

## Configure Keystone access

```ini
[keystone_authtoken]
www_authenticate_uri = http://controller01:5000
auth_url = http://controller01:5000
memcached_servers = controller01:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = cinder
password = CINDER_SVC_PASS
```

## Configure the storage node IP

```ini
[DEFAULT]
my_ip = 10.0.0.4
```

## Configure the LVM backend

```ini
[lvm]
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
volume_group = cinder-volumes
iscsi_protocol = iscsi
iscsi_helper = tgtadm

[DEFAULT]
enabled_backends = lvm
```

## Configure Glance and `lock_path`

```ini
[DEFAULT]
glance_api_servers = http://controller01:9292
oslo_concurrency.lock_path = /var/lib/cinder/tmp
```

## Restart services

```bash
sudo service target restart
sudo service cinder-volume restart
```

## Check services

```bash
openstack volume service list
```

Example output:

```bash
vagrant@controller01:~$ openstack volume service list
+------------------+---------------+------+---------+-------+----------------------------+
| Binary           | Host          | Zone | Status  | State | Updated At                 |
+------------------+---------------+------+---------+-------+----------------------------+
| cinder-scheduler | controller01  | nova | enabled | up    | 2025-11-23T14:58:09.000000 |
| cinder-volume    | storage01@lvm | nova | enabled | up    | 2025-11-23T14:58:09.000000 |
+------------------+---------------+------+---------+-------+----------------------------+
```
