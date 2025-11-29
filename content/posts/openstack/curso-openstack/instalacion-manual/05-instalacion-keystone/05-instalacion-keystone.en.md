---
title: "05 - Install and configure Keystone on the controller node"
date: 2025-11-23T12:00:00+00:00
description: "Step‑by‑step to install the Keystone identity service on the OpenStack controller node."
tags: [openstack,installation,keystone]
hero: images/openstack/instalacion-manual/instalar-keystone-nodo-controlador.png
weight: 5
---

OpenStack is made up of many services, and Keystone (Identity) handles authentication, authorization, and the service catalog. In this post, I will install Keystone on the `controller01` node, explain the main files, and check that it works.

Make sure you've completed the steps from the previous post.

All commands in this post are executed on the `controller01` node.

## Create the Keystone database

Connect to the database server as root:

```bash
sudo mysql
```

Create the `keystone` database:

```bash
CREATE DATABASE keystone;
```

Create users and grant privileges on the `keystone` database:

```bash
CREATE USER 'keystone'@'localhost' IDENTIFIED BY 'KEYSTONE-DBPASS';
GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost';
CREATE USER 'keystone'@'%' IDENTIFIED BY 'KEYSTONE-DBPASS';
GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%';
```

Exit the database client:

```bash
exit
```

## Configure Keystone

We use Apache with mod_wsgi to serve Keystone on port 5000. The package typically creates the required Apache configuration automatically, but verify that it is correct for your case.

Install the required packages:

```bash
sudo apt install keystone apache2 libapache2-mod-wsgi-py3 -y
```

Edit `/etc/keystone/keystone.conf` and configure the database connection:

```ini
[database]
connection = mysql+pymysql://keystone:KEYSTONE_DBPASS@10.0.0.2/keystone
```

Replace `KEYSTONE_DBPASS` with the password you chose for the database.

In the `[token]` section, set Fernet:

```ini
[token]
provider = fernet
```

Update the Keystone database with the service migrations—this will create the tables in the database:

```bash
sudo su -s /bin/sh -c "keystone-manage db_sync" keystone
```

Note: the `--keystone-user` and `--keystone-group` options allow running Keystone with a different user/group than the default. Here we use `keystone`.

Initialize the Fernet keys and the protected credentials:

```bash
sudo keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
sudo keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
```

Bootstrap the Identity service (this creates the initial `admin` user and `admin` project):

```bash
sudo keystone-manage bootstrap --bootstrap-password ADMIN_PASS \
  --bootstrap-admin-url http://controller01:5000/v3/ \
  --bootstrap-internal-url http://controller01:5000/v3/ \
  --bootstrap-public-url http://controller01:5000/v3/ \
  --bootstrap-region-id RegionOne
```

Replace `ADMIN_PASS` with the password you want to use for the administrator user.

## Configure the Apache web server

Edit `/etc/apache2/apache2.conf` and add the `ServerName` pointing to the controller node:

```apache
ServerName controller01
```

Restart the service and make sure it is up:

```bash
sudo systemctl restart apache2
sudo systemctl status apache2
```

We won't use TLS/HTTPS since this is a lab, so that completes the Apache configuration.

## Finish the installation

Create an administrative account by creating an `admin-openrc` file with the following environment variables:

```bash
nano admin-openrc
export OS_USERNAME=admin
export OS_PASSWORD=keystone_auth_admin_password
export OS_PROJECT_NAME=admin
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_AUTH_URL=http://controller01:5000/v3
export OS_IDENTITY_API_VERSION=3
```

These values are those created by `keystone-manage bootstrap` by default.

Replace `ADMIN_PASS` with the password you used in the `keystone-manage bootstrap` command.

Finally, source `admin-openrc` to load the variables:

```bash
source admin-openrc
```

Verify that you can issue a token to check that Keystone responds correctly:

```bash
openstack token issue
```

If you get a similar output, the Keystone installation on the controller node is complete.
