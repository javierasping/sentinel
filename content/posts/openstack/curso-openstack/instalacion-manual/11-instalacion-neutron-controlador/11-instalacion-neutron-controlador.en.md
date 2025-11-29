---
title: "11 - Configure Neutron on the controller node"
date: 2025-11-23T12:00:00+00:00
description: "Complete guide to configure Neutron, OpenStack's networking service, on the controller."
tags: [openstack,installation,neutron]
hero: images/openstack/instalacion-manual/instalar-configurar-neutron-controlador.png
weight: 11
---

This page installs and configures the Neutron networking service on the controller node (`controller01`). Neutron manages virtual networks, routers, subnets, and other networking components for instances.

## Prerequisites

Before starting, ensure you have:

- Keystone installed and reachable.
- A MySQL/MariaDB database available.
- Administrative credentials (`admin-openrc`) to create users and services.

## Create the database

Connect to the database server as `root` to create the Neutron database:

1. Access the SQL client:

```bash
vagrant@controller01:~$ sudo mysql           
```

2. Create the `neutron` database:

```sql
MariaDB [(none)]> CREATE DATABASE neutron;
```

3. Grant privileges to user `neutron` (replace `NEUTRON_DBPASS` with your password):

```sql
MariaDB [(none)]> GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'localhost' \
	IDENTIFIED BY 'NEUTRON_DBPASS';
MariaDB [(none)]> GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'%' \
	IDENTIFIED BY 'NEUTRON_DBPASS';
```

4. Exit the client when finished.

## Create the user and service endpoints

Load your admin credentials to work with the OpenStack CLI:

1. Load environment variables:

```bash
vagrant@controller01:~$ source admin-openrc 
```

2. Create the `neutron` user in Keystone (use `NEUTRON_PASSWORD` as an example password):

```bash
vagrant@controller01:~$ openstack user create --domain default --password NEUTRON_PASSWORD neutron
```

3. Add the `admin` role to the `neutron` user within the `service` project:

```bash
vagrant@controller01:~$ openstack role add --project service --user neutron admin
```

4. Register the Neutron service in Keystone's catalog:

```bash
vagrant@controller01:~$ openstack service create --name neutron --description "OpenStack Networking" network
```

5. Create the public, internal, and admin endpoints pointing to port 9696:

```bash
vagrant@controller01:~$ openstack endpoint create --region RegionOne network public http://controller01:9696
vagrant@controller01:~$ openstack endpoint create --region RegionOne network internal http://controller01:9696 
vagrant@controller01:~$ openstack endpoint create --region RegionOne network admin http://controller01:9696
```

## Install and configure Neutron components

```bash
sudo apt install -y neutron-server neutron-plugin-ml2 neutron-linuxbridge-agent neutron-l3-agent neutron-dhcp-agent neutron-metadata-agent
```

Edit `/etc/neutron/neutron.conf` and configure the key sections.

```ini
[database]
connection = mysql+pymysql://neutron:NEUTRON_DBPASS@controller01/neutron

[DEFAULT]
core_plugin = ml2
service_plugins = router
allow_overlapping_ips = true
transport_url = rabbit://openstack:RABBIT_PASS@controller
notify_nova_on_port_status_changes = true
notify_nova_on_port_data_changes = true

[api]
auth_strategy = keystone

[keystone_authtoken]
www_authenticate_uri = http://controller01:5000
auth_url = http://controller01:5000
memcached_servers = controller01:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = neutron
password = NEUTRON_PASS

[nova]
auth_url = http://controller01:5000
auth_type = password
project_domain_name = Default
user_domain_name = Default
region_name = RegionOne
project_name = service
username = nova
password = NOVA_PASS

[oslo_concurrency]
lock_path = /var/lib/neutron/tmp
```

### Configure the Modular Layer 2 (ML2) plugin

ML2 connects network types with the mechanism (linuxbridge). Edit `/etc/neutron/plugins/ml2/ml2_conf.ini` to enable drivers and types.

```ini
[ml2]
type_drivers = flat,vlan,vxlan
tenant_network_types = vxlan
mechanism_drivers = linuxbridge,l2population
extension_drivers = port_security

[ml2_type_flat]
flat_networks = provider

[ml2_type_vxlan]
vni_ranges = 1:1000

[securitygroup]
enable_security_group = true
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
```

### Configure the Linux Bridge Agent

In `/etc/neutron/plugins/ml2/linuxbridge_agent.ini` set the physical interface and local IP for VXLAN:

```ini
[linux_bridge]
physical_interface_mappings = provider:eth0

[vxlan]
enable_vxlan = true
local_ip = 10.0.0.2
l2_population = true

[securitygroup]
enable_security_group = true
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
```

### Configure the L3 Agent

```ini
[DEFAULT]
interface_driver = linuxbridge
```

### Configure the DHCP Agent

```ini
[DEFAULT]
interface_driver = linuxbridge
dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq
enable_isolated_metadata = true
```

### Configure the Metadata Agent

```ini
[DEFAULT]
nova_metadata_host = controller01
metadata_proxy_shared_secret = openstack
```

### Configure Nova to use Neutron

In `/etc/nova/nova.conf` configure the `[neutron]` section so Nova uses the networking service:

```ini
[neutron]
url = http://controller01:9696
auth_url = http://controller01:5000
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = neutron
password = openstack
service_metadata_proxy = true
metadata_proxy_shared_secret = openstack
```

### Populate the Neutron database

Run the migrations to create the required tables:

```bash
sudo su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron
```

If all goes well you will see alembic messages applying migrations and finally `OK`.

## Restart services and check agents

Restart the services to apply the configuration:

```bash
sudo service nova-api restart
sudo service neutron-server restart
sudo service neutron-linuxbridge-agent restart
sudo service neutron-dhcp-agent restart
sudo service neutron-metadata-agent restart
sudo service neutron-l3-agent restart
```

Check the status of the agents:

```bash
vagrant@controller01:~$ openstack network agent list
```

You should see the `Linux bridge`, `DHCP`, `L3` and `Metadata` agents in `UP` state:

```bash
+--------------------------------------+--------------------+--------------+-------------------+-------+-------+---------------------------+
| ID                                   | Agent Type         | Host         | Availability Zone | Alive | State | Binary                    |
+--------------------------------------+--------------------+--------------+-------------------+-------+-------+---------------------------+
| 94434668-d4b3-4960-8363-54c1be53d0a5 | Linux bridge agent | controller01 | None              | :-)   | UP    | neutron-linuxbridge-agent |
| ca0e8819-add4-4c03-991f-35d2f5bf112d | DHCP agent         | controller01 | nova              | :-)   | UP    | neutron-dhcp-agent        |
| d121bb9a-d44d-4ae0-829e-6623d17e8e13 | L3 agent           | controller01 | nova              | :-)   | UP    | neutron-l3-agent          |
| d6849ebc-86f2-4ed2-80fc-cf3f9fce7d76 | Metadata agent     | controller01 | None              | :-)   | UP    | neutron-metadata-agent    |
+--------------------------------------+--------------------+--------------+-------------------+-------+-------+---------------------------+
```

Check agents:

```bash
openstack network agent list
```
