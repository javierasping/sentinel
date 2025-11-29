---
title: "12 - Configure Neutron on compute nodes"
date: 2025-11-23T12:00:00+00:00
description: "Connect your compute nodes to OpenStack's virtual network with Neutron."
tags: [openstack,installation,neutron]
hero: images/openstack/instalacion-manual/instalar-configurar-neutron-computo.png
weight: 12
---

On this page, we configure Neutron on the compute node (`compute01`). The compute node manages network connectivity and security groups for the instances that run on it.

## Prerequisites

Make sure you have completed all previous posts before starting.

## Install the components

```bash
vagrant@compute01:~$ sudo apt install -y neutron-linuxbridge-agent
```

## Configure the common component

Edit `/etc/neutron/neutron.conf` to configure authentication and the message queue.

In `[DEFAULT]`, configure access to RabbitMQ and the authentication strategy:

```ini
[DEFAULT]
transport_url = rabbit://openstack:RABBIT_PASS@controller01
auth_strategy = keystone

In `[keystone_authtoken]`, configure authentication with Keystone:

[keystone_authtoken]
auth_uri = http://controller01:5000
auth_url = http://controller01:5000
memcached_servers = controller01:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = neutron
password = NEUTRON_PASS

In `[oslo_concurrency]`, define the lock path:

[oslo_concurrency]
lock_path = /var/lib/neutron/tmp
```

## Configure the Linux Bridge agent

The Linux bridge agent builds the virtual network infrastructure and manages security groups for instances.

Edit `/etc/neutron/plugins/ml2/linuxbridge_agent.ini` and configure the options.

In `[linux_bridge]`, assign the physical interface mapped to the provider network (in this case `eth0`):

Edit `/etc/neutron/plugins/ml2/linuxbridge_agent.ini`:

```ini
[linux_bridge]
physical_interface_mappings = provider:eth0
```

In `[vxlan]`, enable VXLAN for self-service networks and set the local IP for VXLAN traffic (replace `10.0.0.3` with your compute node's management IP):

```ini
[vxlan]
enable_vxlan = true
local_ip = 10.0.0.3
l2_population = true
```

In `[securitygroup]`, enable security groups and configure the iptables firewall:

```ini
[securitygroup]
enable_security_group = true
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
```

## Configure Nova to use Neutron

Edit `/etc/nova/nova.conf` so Nova uses Neutron on this node.

In `[neutron]`, configure the access parameters:

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
password = NEUTRON_PASS
```

## Restart services and check agents

```bash
vagrant@compute01:~$ sudo service nova-compute restart
vagrant@compute01:~$ sudo service neutron-linuxbridge-agent restart
```

From the controller, check that all agents are active:

```bash
vagrant@controller01:~$ openstack network agent list
```

You should see the `Linux bridge` agent from the compute node (`compute01`) in `UP` state, along with the controller agents:

```bash
vagrant@controller01:~$ openstack network agent list
+------------------+------------------+--------------+-------------------+-------+-------+------------------+
| ID               | Agent Type       | Host         | Availability Zone | Alive | State | Binary           |
+------------------+------------------+--------------+-------------------+-------+-------+------------------+
| 5103a975-977d-   | Linux bridge     | compute01    | None              | :-)   | UP    | neutron-         |
| 4adb-885c-       | agent            |              |                   |       |       | linuxbridge-     |
| d51cb92bf2de     |                  |              |                   |       |       | agent            |
| 52a6a02e-6e7a-   | L3 agent         | controller01 | nova              | :-)   | UP    | neutron-l3-agent |
| 43a6-ac66-       |                  |              |                   |       |       |                  |
| 85d27c779a6f     |                  |              |                   |       |       |                  |
| 58d07bea-0a2e-   | Metadata agent   | controller01 | None              | :-)   | UP    | neutron-         |
| 499d-89d1-       |                  |              |                   |       |       | metadata-agent   |
| fa3705f6c0cb     |                  |              |                   |       |       |                  |
| ce87bffc-ab25-   | Linux bridge     | controller01 | None              | :-)   | UP    | neutron-         |
| 431e-99d1-       | agent            |              |                   |       |       | linuxbridge-     |
| 55d13cc69a04     |                  |              |                   |       |       | agent            |
| d705285c-b40a-   | DHCP agent       | controller01 | nova              | :-)   | UP    | neutron-dhcp-    |
| 4041-bbb6-       |                  |              |                   |       |       | agent            |
| 3e8be304f156     |                  |              |                   |       |       |                  |
+------------------+------------------+--------------+-------------------+-------+-------+------------------+
```
