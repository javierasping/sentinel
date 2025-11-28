---
title: "04 - Despliegue y preparación del escenario"
date: 2025-11-23T12:00:00+00:00
description: "Configura tu entorno de pruebas OpenStack con todos los nodos necesarios para el laboratorio."
tags: [openstack,instalacion,vagrant]
hero: ""
weight: 4
---

Lo primero es levantar nuestro escenario. Para ello, como comenté en el post anterior, clona mi [repositorio](https://github.com/javierasping/openstack-vagrant-ansible#):

```bash
git clone git@github.com:javierasping/openstack-vagrant-ansible.git
git clone https://github.com/javierasping/openstack-vagrant-ansible.git
```

Una vez clonado, todo lo referente a estos posts está en el directorio `manual-install`, así que entra dentro de él.

## Levantar las máquinas con Vagrant

Como te dije, dentro del repositorio encontrarás el Vagrantfile. Simplemente tienes que lanzar el siguiente comando:

```bash
javiercruces@FJCD-PC:~/openstack-vagrant-ansible/manual-install$ vagrant up
```

Una vez lanzado, asegúrate de que las máquinas están levantadas:

```bash
vagrant status

Current machine states:

controller01              running (libvirt)
compute01                 running (libvirt)
storage01                 running (libvirt)
```

Para conectarte a las VMs puedes utilizar los siguientes comandos:

```bash
vagrant ssh controller01
vagrant ssh compute01
vagrant ssh storage01
```

Te recomiendo que te conectes a cada una de ellas en terminales independientes, así te será más cómodo.

## Instalación del cliente de OpenStack

Como acabamos de levantar las máquinas, los repositorios no están actualizados, así que actualizaremos los repositorios e instalaremos el cliente de OpenStack. Esto hay que hacerlo en los tres nodos.

En mi equipo lo ejecuto desde el directorio del laboratorio, en mi caso `~/openstack-vagrant-ansible/manual-install`:

```bash
for name in controller01 compute01 storage01; do
  vagrant ssh "$name" -c "sudo apt update && sudo apt install -y python3-openstackclient"
done
```

## Instalación de la base de datos (MariaDB) en el nodo controlador

OpenStack utiliza una base de datos para almacenar la información de los diferentes servicios. En mi caso voy a instalar MariaDB y el cliente Python en el nodo controlador, que utilizaremos posteriormente:

```bash
vagrant ssh controller01 -c "sudo apt update && sudo apt install -y mariadb-server python3-pymysql"
```

Crea y edita el fichero de configuración para permitir la conexión remota a las bases de datos almacenadas en el controlador:

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

Nota: sustituye `10.0.0.2` por la dirección IP de gestión del nodo controlador en tu entorno.

Voy a reiniciar el servicio de base de datos para aplicar la nueva configuración:

```bash
vagrant ssh controller01 -c "sudo systemctl restart mariadb || sudo systemctl restart mysql"
```

Ahora ejecuto el asistente de seguridad de MariaDB para eliminar usuarios de prueba y asegurar el root:

```bash
vagrant@controller01:~$ sudo mysql_secure_installation

NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MariaDB
      SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!

In order to log into MariaDB to secure it, we'll need the current
password for the root user. If you've just installed MariaDB, and
haven't set the root password yet, you should just press enter here.

Enter current password for root (enter for none): 
OK, successfully used password, moving on...

Setting the root password or using the unix_socket ensures that nobody
can log into the MariaDB root user without the proper authorisation.

You already have your root account protected, so you can safely answer 'n'.

Switch to unix_socket authentication [Y/n] n
 ... skipping.

You already have your root account protected, so you can safely answer 'n'.

Change the root password? [Y/n] n
 ... skipping.

By default, a MariaDB installation has an anonymous user, allowing anyone
to log into MariaDB without having to have a user account created for
them.  This is intended only for testing, and to make the installation
go a bit smoother.  You should remove them before moving into a
production environment.

Remove anonymous users? [Y/n] y
 ... Success!

Normally, root should only be allowed to connect from 'localhost'.  This
ensures that someone cannot guess at the root password from the network.

Disallow root login remotely? [Y/n] n
 ... skipping.

By default, MariaDB comes with a database named 'test' that anyone can
access.  This is also intended only for testing, and should be removed
before moving into a production environment.

Remove test database and access to it? [Y/n] y
 - Dropping test database...
 ... Success!
 - Removing privileges on test database...
 ... Success!

Reloading the privilege tables will ensure that all changes made so far
will take effect immediately.

Reload privilege tables now? [Y/n] y
 ... Success!

Cleaning up...

All done!  If you've completed all of the above steps, your MariaDB
installation should now be secure.

Thanks for using MariaDB!
```

## Instalar cola de mensajes (RabbitMQ)

OpenStack utiliza una cola de mensajes para coordinar las operaciones y el intercambio de estado entre los distintos servicios. El servicio de cola de mensajes normalmente se ejecuta en el nodo controlador. OpenStack admite varios motores de colas, como RabbitMQ y Qpid, pero la mayoría de las distribuciones que empaquetan OpenStack suelen ofrecer soporte para uno en concreto. Esta guía implementa RabbitMQ porque es el más habitualmente soportado; si prefieres otro motor, consulta la documentación específica del mismo.

Instalamos RabbitMQ en el nodo controlador:

```bash
vagrant@controller01:~$ sudo apt install rabbitmq-server -y
```

Creamos el usuario de RabbitMQ para OpenStack (en mi ejemplo uso `RABBIT_PASS` como marcador, usa una contraseña segura en tu entorno):

```bash
vagrant@controller01:~$ sudo rabbitmqctl add_user openstack RABIT_PASSWORD
Adding user "openstack" ...
Done. Don't forget to grant the user permissions to some virtual hosts! See 'rabbitmqctl help set_permissions' to learn more.

```

Yo uso `RABBIT_PASS` como marcador, asegúrate de usar una contraseña segura en tu entorno.

Le concedemos permisos de configuración, escritura y lectura al usuario `openstack`:

```bash
vagrant@controller01:~$ sudo rabbitmqctl set_permissions openstack ".*" ".*" ".*"
Setting permissions for user "openstack" in vhost "/" ...
```

## Instalación de Memcached

El mecanismo de autenticación del servicio Identity (keystone) usa Memcached para cachear tokens. El servicio memcached suele ejecutarse en el nodo controlador. En entornos de producción se recomienda combinar firewall, autenticación y cifrado para proteger el servicio.

Instala Memcached y el cliente Python en el controlador (usado por Keystone/Horizon):

```bash
vagrant@controller01:~$ sudo apt install memcached python3-memcache -y
```

Edita `/etc/memcached.conf` para que Memcached escuche en la IP de gestión del controlador:

```bash
vagrant@controller01:~$ sudo nano /etc/memcached.conf

# Specify which IP address to listen on. The default is to listen on all IP addresses
# This parameter is one of the only security measures that memcached has, so make sure
# it's listening on a firewalled interface.
-l 127.16.0.11 # Change this
```

Reinicia el servicio Memcached para aplicar los cambios:

```bash
vagrant@controller01:~$ sudo service memcached restart
```

## Instalación de etcd

Algunos servicios de OpenStack pueden usar etcd, un almacén de pares clave-valor distribuido y fiable, útil para bloqueo distribuido, almacenamiento de configuración, seguimiento de la disponibilidad de servicios y otros casos.

El servicio `etcd` se ejecuta normalmente en el nodo controlador.

Instala `etcd` en el nodo controlador (opcional para algunos servicios):

```bash
vagrant@controller01:~$ sudo apt install etcd-server -y
```

Ajusta la configuración de `etcd` con las URLs de cluster y la IP de gestión:

```bash
vagrant@controller01:~$ sudo nano /etc/default/etcd
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

Habilita y arranca el servicio `etcd`:

```bash
vagrant@controller01:~$ sudo systemctl enable etcd
Synchronizing state of etcd.service with SysV service script with /usr/lib/systemd/systemd-sysv-install.
Executing: /usr/lib/systemd/systemd-sysv-install enable etcd

vagrant@controller01:~$ sudo systemctl start etcd
```

Con esto ya hemos preparado las máquinas para comenzar la instalación de los servicios de OpenStack.