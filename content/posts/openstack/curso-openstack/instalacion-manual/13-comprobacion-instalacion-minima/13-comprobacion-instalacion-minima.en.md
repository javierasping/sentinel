---
title: "13 - Verify the Minimum OpenStack Installation"
date: 2025-11-23T12:00:00+00:00
description: "End-to-end verification: agents, networks, router, image, instance, floating IP and connectivity."
tags: [openstack,installation,verification]
hero: images/openstack/instalacion-manual/verificar-intalacion-minima.png
weight: 13
---

On this post we perform an end-to-end verification from the controller node (`controller01`). First we check the network agents, then we create the internal network and subnet, configure a router, prepare the external network, check image and flavor, create an SSH keypair, launch an instance and validate connectivity (ICMP/SSH) using a floating IP. Example outputs are included to compare against your environment.

Before starting, load your admin credentials if they are not already in the environment:

```bash
vagrant@controller01:~$ source ~/admin-openrc
```

## Step 1: Verify network agents

Check that Neutron agents (linuxbridge, DHCP, L3, metadata) are alive and in UP state:

```bash
vagrant@controller01:~$ openstack network agent list
```

Example output:

```
+------------------+------------------+--------------+-------------------+-------+-------+------------------+
| ID               | Agent Type       | Host         | Availability Zone | Alive | State | Binary           |
+------------------+------------------+--------------+-------------------+-------+-------+------------------+
| 94434668-d4b3-   | Linux bridge     | controller01 | None              | :-)   | UP    | neutron-         |
| 4960-8363-       | agent            |              |                   |       |       | linuxbridge-     |
| 54c1be53d0a5     |                  |              |                   |       |       | agent            |
| a2717b0e-fd22-   | Linux bridge     | compute01    | None              | :-)   | UP    | neutron-         |
| 4e52-910c-       | agent            |              |                   |       |       | linuxbridge-     |
| 556f3ad29a67     |                  |              |                   |       |       | agent            |
| ca0e8819-add4-   | DHCP agent       | controller01 | nova              | :-)   | UP    | neutron-dhcp-    |
| 4c03-991f-       |                  |              |                   |       |       | agent            |
| 35d2f5bf112d     |                  |              |                   |       |       |                  |
| d121bb9a-d44d-   | L3 agent         | controller01 | nova              | :-)   | UP    | neutron-l3-agent |
| 4ae0-829e-       |                  |              |                   |       |       |                  |
| 6623d17e8e13     |                  |              |                   |       |       |                  |
| d6849ebc-86f2-   | Metadata agent   | controller01 | None              | :-)   | UP    | neutron-         |
| 4ed2-80fc-       |                  |              |                   |       |       | metadata-agent   |
| cf3f9fce7d76     |                  |              |                   |       |       |                  |
+------------------+------------------+--------------+-------------------+-------+-------+------------------+
```

Note: if any agent appears as DOWN, check its logs in `/var/log/neutron/`.

## Step 2: Create internal network and subnet

Create the project network `test-net` that will be used by the instance:

```bash
vagrant@controller01:~$ openstack network create test-net
```

Example output (IDs and segmentation_id can differ):

```
+---------------------------+--------------------------------------+
| Field                     | Value                                |
+---------------------------+--------------------------------------+
| admin_state_up            | UP                                   |
| availability_zone_hints   |                                      |
| availability_zones        |                                      |
| created_at                | 2025-11-02T23:19:16Z                 |
| description               |                                      |
| dns_domain                | None                                 |
| id                        | f3b76e27-fe00-4ad1-88a1-fd3528c4e412 |
| mtu                       | 1450                                 |
| name                      | test-net                             |
| port_security_enabled     | True                                 |
| project_id                | 69782314638942ef831e8754cda5e41d     |
| provider:network_type     | vxlan                                |
| provider:physical_network | None                                 |
| provider:segmentation_id  | 612                                  |
| router:external           | Internal                             |
| shared                    | False                                |
| status                    | ACTIVE                               |
+---------------------------+--------------------------------------+
```

Create the subnet `test-subnet` within the network (define range and gateway):

```bash
vagrant@controller01:~$ openstack subnet create --network test-net --subnet-range 192.168.50.0/24 test-subnet
```

Example output:

```
+----------------------+--------------------------------------+
| Field                | Value                                |
+----------------------+--------------------------------------+
| allocation_pools     | 192.168.50.2-192.168.50.254          |
| cidr                 | 192.168.50.0/24                      |
| created_at           | 2025-11-02T23:19:21Z                 |
| enable_dhcp          | True                                 |
| gateway_ip           | 192.168.50.1                         |
| id                   | 6f9e499d-6b04-4f92-b4fa-3f4c4df225f5 |
| ip_version           | 4                                    |
| name                 | test-subnet                          |
| network_id           | f3b76e27-fe00-4ad1-88a1-fd3528c4e412 |
| router:external      | False                                |
| status               | ACTIVE                               |
+----------------------+--------------------------------------+
```

## Step 3: Create router and attach the subnet

Create the router `test-router` to connect the internal network with the external network:

```bash
vagrant@controller01:~$ openstack router create test-router
```

Initial output (without external gateway yet):

```
+-------------------------+--------------------------------------+
| Field                   | Value                                |
+-------------------------+--------------------------------------+
| admin_state_up          | UP                                   |
| created_at              | 2025-11-02T23:19:25Z                 |
| distributed             | False                                |
| external_gateway_info   | null                                 |
| ha                      | False                                |
| id                      | 954c7398-6e05-42d9-bd81-2a780835b832 |
| name                    | test-router                          |
| status                  | ACTIVE                               |
+-------------------------+--------------------------------------+
```

Add the internal subnet as an interface so the router manages `192.168.50.0/24`:

```bash
vagrant@controller01:~$ openstack router add subnet test-router test-subnet
```

## Step 4: Create external network and set gateway

Create the external network `ext-net` (flat) that represents external connectivity:

```bash
vagrant@controller01:~$ openstack network create --external \
    --provider-physical-network provider \
    --provider-network-type flat ext-net
```

Create the external subnet `ext-subnet` with a pool of floating IPs:

```bash
vagrant@controller01:~$ openstack subnet create --network ext-net \
    --subnet-range 192.168.121.0/24 \
    --gateway 192.168.121.1 \
    --allocation-pool start=192.168.121.200,end=192.168.121.254 \
    --dns-nameserver 8.8.8.8 ext-subnet
```

Associate the external network to the router to enable SNAT and outgoing traffic:

```bash
vagrant@controller01:~$ openstack router set test-router --external-gateway ext-net
```

Verify the router details (should show `external_fixed_ips` and `enable_snat: true`):

```bash
vagrant@controller01:~$ openstack router show test-router
```

## Step 5: Quick diagnostics

- Agent DOWN: check `/var/log/neutron/*` and systemd service status.
- Error creating external network: validate `bridge_mappings` and existence of the physical device/bridge.
- `No Network found for provider`: misspelled name or missing definition in ML2.
- Low MTU / erratic connectivity: compare the network `mtu` with the physical interface and adjust if necessary.

## Step 6: Image, flavor and keypair

Check that the base image exists (for example `cirros`):

```bash
vagrant@controller01:~$ openstack image list
```

Create a keypair `testkey` and secure the private file:

```bash
vagrant@controller01:~$ openstack keypair create testkey > testkey.pem
vagrant@controller01:~$ chmod 600 testkey.pem
```

If the flavor `m1.tiny` does not exist, create it (RAM 512 MiB, disk 1 GiB, 1 vCPU):

```bash
vagrant@controller01:~$ openstack flavor create --id m1.tiny --ram 512 --disk 1 --vcpus 1 m1.tiny
```

Launch the instance `test-vm` on the internal network (the `net-id` corresponds to your `test-net`):

```bash
vagrant@controller01:~$ openstack server create --flavor m1.tiny --image cirros --nic net-id=9d446c54-f58c-4301-a515-428598f460ca --security-group default --key-name testkey test-vm
```

Check that its state moves from BUILD to ACTIVE:

```bash
vagrant@controller01:~$ openstack server list
vagrant@controller01:~$ openstack server show test-vm | grep -E "status|addresses|flavor|image"
```

If it remains in BUILD or goes to ERROR, check `openstack console log show test-vm` and Nova logs.

For external access (lab only), add rules to the `default` security group:

```bash
vagrant@controller01:~$ openstack security group rule create --proto tcp --dst-port 22 default
vagrant@controller01:~$ openstack security group rule create --proto icmp default
```

Create a floating IP and associate it (replace `<FLOATING_IP>` with the allocated address):

```bash
vagrant@controller01:~$ openstack floating ip create ext-net
vagrant@controller01:~$ openstack server add floating ip test-vm <FLOATING_IP>
```

## Step 7: Access the instance and validate network

SSH to the instance using the floating IP (Cirros default password `gocubsgo` if needed):

```bash
vagrant@controller01:~$ ssh -i .ssh/testkey.pem cirros@192.168.121.212
```

Inside the instance check the interface and hostname:

```bash
$ ip -4 a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc pfifo_fast qlen 1000
    inet 192.168.50.225/24 brd 192.168.50.255 scope global eth0
       valid_lft forever preferred_lft forever
$ hostname
test-vm
```

Check connectivity to the router's internal gateway and to the Internet:

```bash
$ ping 192.168.50.1 -c 1
PING 192.168.50.1 (192.168.50.1): 56 data bytes
64 bytes from 192.168.50.1: seq=0 ttl=64 time=0.650 ms

--- 192.168.50.1 ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max = 0.650/0.650/0.650 ms
$ ping 1.1.1.1 -c 1
PING 1.1.1.1 (1.1.1.1): 56 data bytes
64 bytes from 1.1.1.1: seq=0 ttl=54 time=9.840 ms

--- 1.1.1.1 ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max = 9.840/9.840/9.840 ms
```

## Step 8: Validate connectivity from the host

From the host machine ping the floating IP and confirm the internal IP is not reachable:

```bash
javiercruces@FJCD-PC:~/openstack-vagrant-ansible/manual-install (main) [prd-eu-west|]
$ ping -c 1 192.168.121.212
PING 192.168.121.212 (192.168.121.212) 56(84) bytes of data.
64 bytes from 192.168.121.212: icmp_seq=1 ttl=63 time=0.824 ms

--- 192.168.121.212 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.824/0.824/0.824/0.000 ms

javiercruces@FJCD-PC:~/openstack-vagrant-ansible/manual-install (main) [prd-eu-west|]
$ ping -c 1 192.168.50.225
PING 192.168.50.225 (192.168.50.225) 56(84) bytes of data.
^C
--- 192.168.50.225 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss, time 0ms
```

Note: the internal IP (192.168.50.x) is isolated by Neutron; only the floating IP is reachable from outside.

With this we have verified the installed components are working as expected.
