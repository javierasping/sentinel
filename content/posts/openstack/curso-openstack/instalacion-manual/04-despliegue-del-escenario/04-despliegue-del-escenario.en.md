---
title: "04 - Environment deployment and preparation"
date: 2025-11-23T12:00:00+00:00
description: "Set up your OpenStack test environment with all the nodes needed for the lab."
tags: [openstack,installation,vagrant]
hero: images/openstack/instalacion-manual/despliegue-escenario.png
weight: 4
---

First, we need to bring up our environment. As mentioned in the previous post, clone my [repository](https://github.com/javierasping/openstack-vagrant-ansible#):

```bash
git clone git@github.com:javierasping/openstack-vagrant-ansible.git
git clone https://github.com/javierasping/openstack-vagrant-ansible.git
```

Once cloned, everything related to these posts is in the `manual-install` directory, so cd into it.

## Bring up the machines with Vagrant

Inside the repository you'll find the Vagrantfile. Simply run:

```bash
vagrant up
```

After launching, make sure the machines are up:

```bash
vagrant status

Current machine states:

controller01              running (libvirt)
compute01                 running (libvirt)
storage01                 running (libvirt)
```

To connect to the VMs, you can use:

```bash
vagrant ssh controller01
vagrant ssh compute01
vagrant ssh storage01
```

I recommend connecting to each of them in separate terminals for convenience.

## Install the OpenStack client

Since we just brought up the machines, the repositories are not up to date, so we'll update the repos and install the OpenStack client. Do this on all three nodes.

From my machine, I run it from the lab directory, in my case `~/openstack-vagrant-ansible/manual-install`:

```bash
for name in controller01 compute01 storage01; do
  vagrant ssh "$name" -c "sudo apt update && sudo apt install -y python3-openstackclient"
done
```

## Install the database (MariaDB) on the controller node

OpenStack uses a database to store information for its various services. We'll install MariaDB and the Python client on the controller node for later use:

```bash
vagrant ssh controller01 -c "sudo apt update && sudo apt install -y mariadb-server python3-pymysql"
```

Create and edit the configuration file to allow remote connections to the databases stored on the controller:

```bash
vagrant ssh controller01 -c "sudo tee /etc/mysql/mariadb.conf.d/99-openstack.cnf > /dev/null <<'EOF'
[mysqld]
bind-address = 10.0.0.2

default-storage-engine = innodb
innodb_file_per_table = on
max_connections = 4096
collation-server = utf8_general_ci
character-set-server = utf8
EOF"
```

Note: replace `10.0.0.2` with the controller's management IP in your environment.

Restart the database service to apply the new configuration:

```bash
vagrant ssh controller01 -c "sudo systemctl restart mariadb || sudo systemctl restart mysql"
```

Run MariaDB's security wizard to remove test users and secure root:

```bash
sudo mysql_secure_installation
```

## Install message queue (RabbitMQ)

OpenStack uses a message queue to coordinate operations and state exchange among services. The message queue service typically runs on the controller node. OpenStack supports several queue engines, such as RabbitMQ and Qpid, but most distributions that package OpenStack tend to support one in particular. This guide implements RabbitMQ because it is the most commonly supported; if you prefer another engine, consult its documentation.

Install RabbitMQ on the controller node:

```bash
sudo apt install rabbitmq-server -y
```

Create the RabbitMQ user for OpenStack (in my example I use `RABBIT_PASS` as a placeholder—use a strong password in your environment):

```bash
sudo rabbitmqctl add_user openstack RABIT_PASSWORD
```

Grant config, write, and read permissions to the `openstack` user:

```bash
sudo rabbitmqctl set_permissions openstack ".*" ".*" ".*"
```

## Install Memcached

Keystone's authentication mechanism uses Memcached to cache tokens. Memcached usually runs on the controller node. In production, combine firewalling, authentication, and encryption to protect the service.

Install Memcached and the Python client on the controller (used by Keystone/Horizon):

```bash
sudo apt install memcached python3-memcache -y
```

Edit `/etc/memcached.conf` so Memcached listens on the controller's management IP:

```bash
sudo nano /etc/memcached.conf

# Specify which IP address to listen on. The default is to listen on all IP addresses
# This parameter is one of the only security measures that memcached has, so make sure
# it's listening on a firewalled interface.
-l 127.16.0.11 # Change this
```

Restart the Memcached service to apply changes:

```bash
sudo service memcached restart
```

## Install etcd

Some OpenStack services can use etcd, a reliable distributed key‑value store—useful for distributed locking, configuration storage, service availability tracking, and more.

The `etcd` service usually runs on the controller node.

Install `etcd` on the controller node (optional for some services):

```bash
sudo apt install etcd-server -y
```

Adjust the `etcd` configuration with cluster URLs and the management IP:

```bash
sudo nano /etc/default/etcd
ETCD_NAME="controller01"
ETCD_DATA_DIR="/var/lib/etcd"
ETCD_INITIAL_CLUSTER_STATE="new"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster-01"
ETCD_INITIAL_CLUSTER="controller01=http://10.0.0.2:2380"
ETCD_INITIAL_ADVERTISE_PEER_URLS="http://10.0.0.2:2380"
ETCD_ADVERTISE_CLIENT_URLS="http://10.0.0.2:2379"
ETCD_LISTEN_PEER_URLS="http://0.0.0.0:2380"
ETCD_LISTEN_CLIENT_URLS="http://10.0.0.2:2379"
```

Enable and start the `etcd` service:

```bash
sudo systemctl enable etcd
sudo systemctl start etcd
```

With this, we have prepared the machines to begin installing OpenStack services.
