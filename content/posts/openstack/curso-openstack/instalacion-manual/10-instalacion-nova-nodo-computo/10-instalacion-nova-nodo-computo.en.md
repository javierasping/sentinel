---
title: "10 - Install and configure Nova on compute nodes"
date: 2025-11-23T12:00:00+00:00
description: "Configure OpenStack compute nodes to manage virtual instances."
tags: [openstack,installation,nova]
hero: images/openstack/instalacion-manual/instalar-configurar-nova-computo.png
weight: 10
---

On this page I configure a compute node (for example `compute01`) so it can run instances with Nova. I use QEMU/KVM when the hardware supports it; if not, I configure pure QEMU.

Before starting, make sure you have:

- Added the controller name and IP in `/etc/hosts` on the compute node.
- Service credentials (`admin-openrc`) and access to the database server.

## Install and configure the components (on the compute node)

```bash
vagrant@compute01:~$ sudo apt install nova-compute -y
```

Edit `/etc/nova/nova.conf` and point the connection strings to the controller databases:

```ini
[database]
connection = mysql+pymysql://nova:NOVA_DBPASS@controller01/nova

[api_database]
connection = mysql+pymysql://nova:NOVA_DBPASS@controller01/nova_api

[DEFAULT]
transport_url = rabbit://openstack:RABBIT_PASS@controller01

[service_user]
send_service_user_token = true
auth_url = http://controller01:5000/v3/
auth_type = password
project_domain_name = Default
project_name = service
user_domain_name = Default
username = nova
password = NOVA_PASS
[DEFAULT]
my_ip = IP_MANAGEMENT_COMPUTE_NODE

[vnc]
enabled = true
server_listen = 0.0.0.0
server_proxyclient_address = $my_ip
novncproxy_base_url = http://controller01:6080/vnc_auto.html

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
identity_api_version = 3
```

## Finalize installation (on the compute node)

Check hardware virtualization support and, if absent, force QEMU:

```bash
egrep -c '(vmx|svm)' /proc/cpuinfo
```

If the result is 0, set `virt_type=qemu` in `/etc/nova/nova-compute.conf`:

```ini
[libvirt]
virt_type = qemu
```

Restart the `nova-compute` service to apply the configuration:

```bash
vagrant@compute01:~$ sudo service nova-compute restart
```

## Add the compute node to cell DB (run on controller)

```bash
vagrant@controller01:~$ source admin-openrc 
vagrant@controller01:~$ sudo su -s /bin/sh -c "nova-manage cell_v2 discover_hosts --verbose" nova
Found 2 cell mappings.
Skipping cell0 since it does not contain hosts.
Getting computes from cell 'cell1': 29e1ed74-59fa-43e3-9651-999d592a2cdf
Checking host mapping for compute host 'compute01': d83ec732-f31c-4358-9326-610b9e660974
Creating host mapping for compute host 'compute01': d83ec732-f31c-4358-9326-610b9e660974
Found 1 unmapped computes in cell: 29e1ed74-59fa-43e3-9651-999d592a2cdf

vagrant@controller01:~$ openstack compute service list --service nova-compute
+--------------------------+--------------+-----------+------+---------+-------+---------------------------+
| ID                       | Binary       | Host      | Zone | Status  | State | Updated At                |
+--------------------------+--------------+-----------+------+---------+-------+---------------------------+
| a6dda039-f310-4b5b-ae5e- | nova-compute | compute01 | nova | enabled | up    | 2025-11-                  |
| 606a4d89592a             |              |           |      |         |       | 02T19:51:01.000000        |
+--------------------------+--------------+-----------+------+---------+-------+---------------------------+
```

To enable periodic discovery, add:

```ini
[scheduler]
discover_hosts_in_cells_interval = 300
```
