---
title: "04 - Despliegue y preparación del escenario"
date: 2025-11-23T12:00:00+00:00
description: "Configura tu entorno de pruebas OpenStack con todos los nodos necesarios para el laboratorio."
tags: [openstack,instalacion,vagrant]
hero: images/openstack/instalacion-manual/despliegue-escenario.png
weight: 4
---

Lo primero es desplegar nuestro escenario. Para ello, como comenté en el post anterior, clona mi [repositorio](https://github.com/javierasping/openstack-vagrant-ansible#):

```bash
git clone git@github.com:javierasping/openstack-vagrant-ansible.git
git clone https://github.com/javierasping/openstack-vagrant-ansible.git
```

Una vez clonado, accederemos al directorio `manual-install`, donde se encuentra todo el contenido relacionado con estos posts.

## Levantar las máquinas con Vagrant

Dentro del repositorio encontrarás el `Vagrantfile`. Para iniciar el despliegue, ejecuta el siguiente comando:

```bash
javiercruces@FJCD-PC:~/openstack-vagrant-ansible/manual-install$ vagrant up
```

Tras ejecutar el comando, verifica que las máquinas virtuales se hayan iniciado correctamente:

```bash
vagrant status

Current machine states:

controller01              running (libvirt)
compute01                 running (libvirt)
storage01                 running (libvirt)
```

Para acceder a las máquinas virtuales, puedes utilizar los siguientes comandos:

```bash
vagrant ssh controller01
vagrant ssh compute01
vagrant ssh storage01
```

Se recomienda abrir una terminal independiente para cada nodo, facilitando así el seguimiento de la instalación.

## Instalación del cliente de OpenStack

Dado que las máquinas acaban de ser desplegadas, es necesario actualizar los repositorios e instalar el cliente de OpenStack en los tres nodos.

Si ejecutas el comando desde el directorio del laboratorio (por ejemplo, `~/openstack-vagrant-ansible/manual-install`), puedes utilizar el siguiente bucle:

```bash
for name in controller01 compute01 storage01; do
  vagrant ssh "$name" -c "sudo apt update && sudo apt install -y python3-openstackclient"
done
```

## Instalación de la base de datos (MariaDB) en el nodo controlador

OpenStack requiere una base de datos para almacenar la información de sus servicios. Instalaremos MariaDB y el cliente de Python en el nodo controlador:

```bash
vagrant ssh controller01 -c "sudo apt update && sudo apt install -y mariadb-server python3-pymysql"
```

Crea y edita el archivo de configuración para habilitar la conexión remota a las bases de datos alojadas en el controlador:

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

Nota: sustituye `10.0.0.2` por la dirección IP de gestión del nodo controlador de tu entorno.

Reiniciaremos el servicio de la base de datos para aplicar la nueva configuración:

```bash
vagrant ssh controller01 -c "sudo systemctl restart mariadb || sudo systemctl restart mysql"
```

A continuación, ejecutaremos el asistente de seguridad de MariaDB para eliminar los usuarios anónimos y asegurar la cuenta root:

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

OpenStack utiliza un sistema de colas de mensajes para coordinar las operaciones y el intercambio de estados entre los servicios. Habitualmente, este servicio se ejecuta en el nodo controlador. Aunque existen diversos motores, como RabbitMQ o Qpid, la mayoría de las distribuciones soportan RabbitMQ, por lo que utilizaremos este en la guía. Si prefieres otro motor, consulta su documentación específica.

Instalaremos RabbitMQ en el nodo controlador:

```bash
vagrant@controller01:~$ sudo apt install rabbitmq-server -y
```

Crearemos el usuario de RabbitMQ para OpenStack (utiliza una contraseña segura en lugar del marcador `RABBIT_PASS`):

```bash
vagrant@controller01:~$ sudo rabbitmqctl add_user openstack RABIT_PASSWORD
Adding user "openstack" ...
Done. Don't forget to grant the user permissions to some virtual hosts! See 'rabbitmqctl help set_permissions' to learn more.

```

Recuerda sustituir `RABBIT_PASS` por una contraseña segura.

Asignaremos permisos de configuración, lectura y escritura al usuario `openstack`:

```bash
vagrant@controller01:~$ sudo rabbitmqctl set_permissions openstack ".*" ".*" ".*"
Setting permissions for user "openstack" in vhost "/" ...
```

## Instalación de Memcached

El servicio de identidad (Keystone) utiliza Memcached para el almacenamiento en caché de los tokens. Habitualmente, Memcached se ejecuta en el nodo controlador. En entornos de producción, es fundamental combinar el uso de firewalls, autenticación y cifrado para proteger este servicio.

Instalaremos Memcached y el cliente de Python en el nodo controlador (utilizado por Keystone y Horizon):

```bash
vagrant@controller01:~$ sudo apt install memcached python3-memcache -y
```

Editaremos `/etc/memcached.conf` para que Memcached escuche en la dirección IP de gestión del controlador:

```bash
vagrant@controller01:~$ sudo nano /etc/memcached.conf

# Specify which IP address to listen on. The default is to listen on all IP addresses
# This parameter is one of the only security measures that memcached has, so make sure
# it's listening on a firewalled interface.
-l 127.16.0.11 # Change this
```

Reiniciaremos el servicio Memcached para aplicar los cambios:

```bash
vagrant@controller01:~$ sudo service memcached restart
```

## Instalación de etcd

Algunos servicios de OpenStack pueden utilizar `etcd`, un almacén de pares clave-valor distribuido y fiable, útil para el bloqueo distribuido, la gestión de la configuración y el seguimiento de la disponibilidad de los servicios.

El servicio `etcd` se ejecuta habitualmente en el nodo controlador.

Instalaremos `etcd` en el nodo controlador (este paso es opcional para algunos servicios):

```bash
vagrant@controller01:~$ sudo apt install etcd-server -y
```

Ajustaremos la configuración de `etcd` definiendo las URLs del clúster y la IP de gestión:

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

Habilitaremos e iniciaremos el servicio `etcd`:

```bash
vagrant@controller01:~$ sudo systemctl enable etcd
Synchronizing state of etcd.service with SysV service script with /usr/lib/systemd/systemd-sysv-install.
Executing: /usr/lib/systemd/systemd-sysv-install enable etcd

vagrant@controller01:~$ sudo systemctl start etcd
```

Con estos pasos, habremos preparado la infraestructura básica para iniciar la instalación de los servicios de OpenStack.