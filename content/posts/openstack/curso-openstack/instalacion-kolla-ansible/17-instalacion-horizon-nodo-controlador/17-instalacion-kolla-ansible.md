---
title: "17 - Instalación de OpenStack usando kolla-ansible en máquinas virtuales"
date: 2025-11-23T12:00:00+00:00
description: "Instalamos el panel web Horizon para gestionar OpenStack desde la interfaz gráfica."
tags: [openstack,instalacion,horizon]
hero: images/openstack/instalacion-manual/instalar-configurar-horizon-controlador.png
weight: 17
---

Hasta ahora hemos instalado OpenStack de forma manual, configurando cada paso uno a uno. Ahora damos el salto a la automatización con Ansible, que permite realizar despliegues casi sin intervención humana.

La idea es sencilla: defines la configuración en unos pocos archivos y Ansible se encarga de ejecutar todo el proceso de forma desatendida. Además, estos archivos pueden versionarse en herramientas como Git, facilitando repetir o modificar despliegues en el futuro.

Ansible simplifica mucho OpenStack al concentrar la mayoría de configuraciones en pocos ficheros con valores por defecto razonables, válidos tanto para entornos simples como más complejos (multi-nodo, clustering, redes avanzadas, etc.).

El despliegue se basa en contenedores Docker (versión community), sin necesidad de tecnologías avanzadas como Swarm, lo que mantiene la arquitectura sencilla: cada nodo ejecuta Docker y Ansible orquesta todo.

Eso sí, aunque la automatización ayuda mucho, sigue siendo necesario tener conocimientos de los servicios de OpenStack para evitar errores en la instalación.

Los ficheros que utilizo están disponibles en mi [repositorio](https://github.com/javierasping/openstack-vagrant-ansible#). Puedes clonarlo usando los siguientes comandos, ya sea por SSH o HTTPS:

```bash
git clone git@github.com:javierasping/openstack-vagrant-ansible.git
git clone https://github.com/javierasping/openstack-vagrant-ansible.git
```


## 1. Crear las siguientes redes en KVM (libvirt):

Primero definimos las redes base en libvirt que usarán todas las VMs del laboratorio.

Si utilizas mi repositorio podrás encontrar debajo del directorio `kolla-ansible` las redes definidas en formato xml .

**Red de gestión**
- Tipo: aislada / interna
- Dirección IPv4: 10.0.0.1
- Máscara de red: 255.255.255.0
- DHCP: deshabilitado

**Red provider**
- CIDR de red: 203.0.113.0/24

**Red NAT**
- Usada para acceso a Internet

---

## 2. Nodos del laboratorio

A continuación se describen las características de los nodos que se utilizarán en el laboratorio.  
Esta configuración está definida en el **Vagrantfile del repositorio**, por lo que no es necesario crearlos manualmente.

Puedes modificar estos valores fácilmente (CPU, RAM, discos, etc.) directamente en el Vagrantfile según los recursos de tu máquina o tus necesidades.

---

**Resumen de nodos**

| Nodo       | CPU   | RAM      | Disco(s)                               | Redes                   |
|------------|-------|----------|----------------------------------------|-------------------------|
| controller | 2 vCPU| 6144 MB  | 20 GB                                  | NAT, gestión, provider  |
| compute1   | 1 vCPU| 2048 MB  | 10 GB                                  | NAT, gestión, provider  |
| compute2   | 1 vCPU| 2048 MB  | 10 GB                                  | NAT, gestión, provider  |
| block1     | 1 vCPU| 1024 MB  | 10 GB + 30 GB (Cinder)                 | NAT, gestión, provider  |
| deployment | 1 vCPU| 2048 MB  | 40 GB                                  | NAT, gestión            |

---

💡 **Nota:**  
El modo promiscuo no es necesario en KVM/libvirt (a diferencia de VirtualBox), ya que el networking se gestiona de forma nativa.

Además, puedes:
- Reducir recursos si tu máquina es limitada  
- Añadir más nodos compute  
- Separar roles en distintos nodos para entornos más avanzados  

Este laboratorio está pensado como una base flexible para experimentar con OpenStack.

Puedes crear las redes a mano usando los siguientes comandos , encontraras las definiciones en el repositorio. Aunque el Vagrantfile las creara automáticamente. 

```bash
virsh net-define provider.xml
virsh net-start provider
virsh net-autostart provider

virsh net-define mgmt-net.xml
virsh net-start mgmt-net
virsh net-autostart mgmt-net
```

Para levantar el escenario lanza el siguiente comando:

```bash
javiercruces@FJCD-PC:~/Documentos/openstack-vagrant-ansible/kolla-ansible$ vagrant up
```

## 3. Preparación de los nodos

Aquí dejaremos cada VM con los paquetes base instalados y listas para lanzar Ansible sobre ellas.

La red y las IP de las máquinas se gestionan automáticamente mediante el Vagrantfile, por lo que no es necesario editar `/etc/hosts` ni ajustar IPs manualmente.

### 3.1 Preparación del nodo controller

En el nodo `controller`, ejecuta como superusuario los siguientes comandos:

```bash
apt update -y
apt upgrade -y
apt install -y python python-simplejson glances vim
reboot
```

### 3.2 Preparación los nodos compute1 y compute2

En los nodos `compute1` y `compute2`, ejecuta como superusuario los siguientes comandos:

```bash
apt update -y
apt upgrade -y
apt install -y python python-simplejson glances vim
echo "configfs" >> /etc/modules
update-initramfs -u
reboot
```

### 3.3. Preparación el nodo block1

En el nodo `block1`, ejecuta como superusuario los siguientes comandos:

```bash
apt update -y
apt upgrade -y
apt install -y python python-simplejson glances vim
apt install -y lvm2 thin-provisioning-tools
pvcreate /dev/vdb
vgcreate cinder-volumes /dev/vdb
echo "configfs" >> /etc/modules
update-initramfs -u
reboot
```

### 3.4 Preparación de la VM deployment

En el nodo `deployment`, ejecuta como superusuario los siguientes comandos:

```bash
apt update -y
apt install -y python3-jinja2 python3-pip libssl-dev curl glances vim python3.12-venv
pip install -U pip
apt upgrade -y
reboot
```

**4. Acceso SSH sin contraseña al resto de nodos**

Ahora configuraremos el acceso por ssh en todos los nodos para que Ansible pueda conectarse. Recuerda que la contraseña y usuario por defecto de las máquinas levantadas con Vagrant es `vagrant`.

```bash
ssh-keygen -t rsa
ssh-copy-id vagrant@controller
ssh-copy-id vagrant@compute1
ssh-copy-id vagrant@compute2
ssh-copy-id vagrant@block1
ssh-copy-id vagrant@deployment
ssh vagrant@controller
ssh vagrant@compute1
ssh vagrant@compute2
ssh vagrant@block1
```

**5. Instalar Ansible y Kolla-Ansible en un virtualenv**

Preparamos un entorno Python aislado con las versiones compatibles de Ansible y Kolla-Ansible. Ten en cuenta que las versiones pueden cambiar , asegúrate de contrastarlo en la documentation oficial .

```bash
# Creamos un entorno virtual de Python para aislar dependencias
python3 -m venv /opt/kolla-venv

# Activamos el entorno virtual
source /opt/kolla-venv/bin/activate

# Actualizamos pip a la última versión
pip install -U pip

# Instalamos versiones concretas de Ansible y Kolla-Ansible (compatibles entre sí)
pip install ansible==2.5.2 kolla-ansible==6.0.0

# Descargamos dependencias adicionales (roles y colecciones de Ansible)
kolla-ansible install-deps
```

**6. Sembrar configuración inicial de Kolla**

Copiamos las plantillas base de configuración de Kolla al directorio de trabajo.

```bash
# Creamos el directorio donde Kolla almacenará su configuración
mkdir -p /etc/kolla

# Copiamos los ficheros de configuración base (plantillas por defecto)
cp -r /opt/kolla-venv/share/kolla-ansible/etc_examples/kolla/* /etc/kolla

# Copiamos el inventario de ejemplo multinodo al directorio actual
cp /opt/kolla-venv/share/kolla-ansible/ansible/inventory/multinode .
```

**7. Ajustes de red y servicios en globals.yml**

Ahora editaremos el fichero `globals.yml` para indicarle a Ansible que queremos que despliegue en nuestra instalación de OpenStack.

```bash
# Editamos el fichero principal de configuración de Kolla
nano /etc/kolla/globals.yml


# Estrategia de copia de configuración (siempre sobrescribe configs en contenedores)
config_strategy: "COPY_ALWAYS"

# Tipo de instalación (binarios dentro de contenedores)
kolla_install_type: "binary"

# IP virtual interna (VIP) para acceso a APIs de OpenStack
kolla_internal_vip_address: "10.0.0.10"

# Interfaz de red principal (red de gestión entre nodos)
network_interface: "eth1"

# Interfaz externa usada por Neutron (provider network)
neutron_external_interface: "eth2"

# Plugin de red (Open vSwitch en este caso)
neutron_plugin_agent: "openvswitch"

# ID de VRRP para keepalived (alta disponibilidad)
keepalived_virtual_router_id: "51"

# Consola de acceso a instancias (noVNC vía web)
nova_console: "novnc"

# Activamos Cinder (almacenamiento en bloque)
enable_cinder: "yes"

# Desactivamos backup de Cinder
enable_cinder_backup: "no"

# Backend iSCSI para Cinder
enable_cinder_backend_iscsi: "yes"

# Backend LVM para Cinder (disco local en block1)
enable_cinder_backend_lvm: "yes"

# Activamos HAProxy (balanceador de carga)
enable_ha_proxy: "yes"

# Activamos Heat (orquestación)
enable_heat: "yes"

# Activamos Horizon (dashboard web)
enable_horizon: "yes"

# Activamos Open vSwitch si no usamos linuxbridge
enable_openvswitch: "{{ neutron_plugin_agent != 'linuxbridge' }}"

# Keystone usa tokens tipo fernet (más seguro)
keystone_token_provider: "fernet"

# Expiración de tokens (en segundos)
fernet_token_expiry: 86400

# Glance almacena imágenes en disco local
glance_backend_file: "yes"

# Nombre del volume group usado por Cinder
cinder_volume_group: "cinder-volumes"

# Tipo de virtualización (qemu si no hay soporte VT-x)
nova_compute_virt_type: "qemu"

```
<!-- 
config_strategy: "COPY_ALWAYS"

kolla_internal_vip_address: "10.0.0.10"

network_interface: "eth1"
neutron_external_interface: "eth2"

neutron_plugin_agent: "openvswitch"

enable_horizon: "yes"
enable_heat: "yes"
enable_cinder: "yes"
enable_cinder_backend_lvm: "yes"

nova_compute_virt_type: "qemu" -->



**8. Configurar nova-compute para usar QEMU**

Forzamos que Nova use virtualización por software para evitar problemas de hardware.

```bash
# Creamos directorio de configuración específica de Nova
mkdir -p /etc/kolla/config/nova

# Definimos configuración personalizada para nova-compute
cat > /etc/kolla/config/nova/nova-compute.conf <<'EOF'
[libvirt]
virt_type = qemu   # Virtualización por software (sin aceleración hardware)
cpu_mode = none    # Evita problemas de CPU en entornos virtualizados
EOF
```

**9. Preparar el inventario multinodo** (apunta a las IP ya definidas por el Vagrantfile):

Completamos el inventario `multinode` con las IP y usuarios de cada host.

```bash
# Activamos entorno virtual (por si no lo estaba)
source /opt/kolla-venv/bin/activate

# Copiamos inventario de ejemplo
cp /opt/kolla-venv/share/kolla-ansible/ansible/inventory/multinode .

# Lo editamos
nano multinode
```

Contenido recomendado del inventario `multinode` (Solo tienes que cambiar estos apartados):

```ini
[control]
controller ansible_host=10.0.0.11 ansible_user=vagrant ansible_become=true ansible_ssh_private_key_file=/home/vagrant/.ssh/id_rsa

[network]
controller ansible_host=10.0.0.11 ansible_user=vagrant ansible_become=true ansible_ssh_private_key_file=/home/vagrant/.ssh/id_rsa

[compute]
compute1 ansible_host=10.0.0.31 ansible_user=vagrant ansible_become=true ansible_ssh_private_key_file=/home/vagrant/.ssh/id_rsa
compute2 ansible_host=10.0.0.32 ansible_user=vagrant ansible_become=true ansible_ssh_private_key_file=/home/vagrant/.ssh/id_rsa

[monitoring]
controller ansible_host=10.0.0.11 ansible_user=vagrant ansible_become=true ansible_ssh_private_key_file=/home/vagrant/.ssh/id_rsa

[storage]
block1 ansible_host=10.0.0.41 ansible_user=vagrant ansible_become=true ansible_ssh_private_key_file=/home/vagrant/.ssh/id_rsa

[deployment]
deployment ansible_host=10.0.0.100 ansible_user=vagrant ansible_become=true ansible_ssh_private_key_file=/home/vagrant/.ssh/id_rsa
```

Por último lanza este comando para comprobar que tienes conectividad con todos los nodos :

```bash
ansible -i multinode all -m ping
```


## 10. Despliegue con Kolla-Ansible

Los siguientes comandos se ejecutan en la VM `deployment` (con el virtualenv , activalo si no lo hiciste anteriormente).

**Paso 10: Generar contraseñas**

Kolla-Ansible nos ofrece el siguiente comando el cual nos creará un fichero con contraseñas "seguras" en la siguiente ruta `/etc/kolla/passwords.yml`

```bash
# Genera passwords aleatorias para todos los servicios
kolla-genpwd

# Genera todos los ficheros de configuración de servicios
kolla-ansible genconfig -i multinode
```

**Paso 11: Bootstrap de nodos**

Instalamos dependencias y configuramos Docker y usuarios en todos los hosts.

```bash
# Instala dependencias, configura Docker, usuarios, etc.
kolla-ansible bootstrap-servers -i multinode
```

Asegúrate de que no ha aparecido ningún error en la ejecución :

```bash
PLAY RECAP *********************************************************************************************************************************************************************************************************************************************************************
block1                     : ok=42   changed=2    unreachable=0    failed=0    skipped=30   rescued=0    ignored=0   
compute1                   : ok=42   changed=2    unreachable=0    failed=0    skipped=30   rescued=0    ignored=0   
compute2                   : ok=42   changed=2    unreachable=0    failed=0    skipped=30   rescued=0    ignored=0   
controller                 : ok=42   changed=2    unreachable=0    failed=0    skipped=30   rescued=0    ignored=0   
deployment                 : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
```

**Paso 12: Pre-chequeos**

Verificamos requisitos y conectividad antes del despliegue final.

```bash
# Verifica que todo está correcto antes del despliegue
kolla-ansible prechecks -i multinode
```

Asegúrate de que no ha aparecido ningún error en la ejecución :

```bash
PLAY RECAP *********************************************************************************************************************************************************************************************************************************************************************
block1                     : ok=33   changed=0    unreachable=0    failed=0    skipped=21   rescued=0    ignored=0   
compute1                   : ok=41   changed=0    unreachable=0    failed=0    skipped=29   rescued=0    ignored=0   
compute2                   : ok=41   changed=0    unreachable=0    failed=0    skipped=29   rescued=0    ignored=0   
controller                 : ok=113  changed=0    unreachable=0    failed=0    skipped=146  rescued=0    ignored=0   
deployment                 : ok=14   changed=0    unreachable=0    failed=0    skipped=13   rescued=0    ignored=0   
```

**Paso 13: Despliegue de OpenStack**:

Lanzamos el despliegue completo de servicios OpenStack en contenedores.

```bash
# Despliega OpenStack completo en contenedores Docker
kolla-ansible deploy -i multinode
```

```bash
PLAY RECAP *********************************************************************************************************************************************************************************************************************************************************************
block1                     : ok=50   changed=18   unreachable=0    failed=0    skipped=20   rescued=0    ignored=0   
compute1                   : ok=97   changed=37   unreachable=0    failed=0    skipped=70   rescued=0    ignored=0   
compute2                   : ok=85   changed=36   unreachable=0    failed=0    skipped=65   rescued=0    ignored=0   
controller                 : ok=423  changed=156  unreachable=0    failed=0    skipped=300  rescued=0    ignored=1   
deployment                 : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```

**Paso 14: Verificar contenedores**

Comprobamos que todos los contenedores Docker están en ejecución.

```bash
# Ver todos los contenedores Docker
docker ps -a
```

## 11. Post-despliegue

Aplicamos las tareas posteriores al despliegue para dejar OpenStack utilizable.

**Paso 15: Post-deploy de Kolla**

Generamos credenciales y archivos de entorno tras el despliegue.

```bash
# Genera credenciales y archivos de entorno
kolla-ansible post-deploy -i multinode
```

Una vez ejecutado tendremos creado el fichero `/etc/kolla/admin-openrc.sh`

**Paso 16: Cliente de OpenStack**

Instalamos la CLI oficial para administrar OpenStack desde la terminal.

```bash
# Instalamos CLI para gestionar OpenStack
pip install python-openstackclient
```


## 12. Comprobación de la instalación

Validamos con la CLI que los servicios respondan y se puede consultar el catálogo.

Ahora vamos a comprobar que podemos usar la CLI de openstack , para ello vamos a cargar el fichero de admin y a comprobar la lista de servicios que hemos instalado .

```bash
(kolla-venv) root@deployment:/home/vagrant# source /etc/kolla/admin-openrc.sh
(kolla-venv) root@deployment:/home/vagrant# openstack service list
+----------------------------------+-----------+----------------+
| ID                               | Name      | Type           |
+----------------------------------+-----------+----------------+
| 00a3904eba79406ebc0f76ec9d4d8d99 | heat-cfn  | cloudformation |
| 053eaef825d14a0e9136c2066d885322 | heat      | orchestration  |
| 386dbab3c6b24c5c8cfb24f7fef83f35 | keystone  | identity       |
| 9ff8d3507da14d0b9441820d0c6cbf37 | neutron   | network        |
| acf5ac3c4d2a492595599383b444c3d6 | glance    | image          |
| ae5a937d13934d7ba2fda8d156a7faad | nova      | compute        |
| d594693374cd432eb7a82363f9db596c | cinder    | block-storage  |
| d7bc52c105ce4734810cd49dbeb3e4ad | placement | placement      |
| f8ad38b97b7d4fc0b7dc6bb98a39b24e | cinderv3  | volumev3       |
+----------------------------------+-----------+----------------+
```

Ahora si nos damos una vuelta por las distintas máquinas , veremos que los servicios se han desplegado en contenedores docker :

```bash
root@controller:/home/vagrant# docker ps -a
CONTAINER ID   IMAGE                                                                   COMMAND                  CREATED          STATUS                    PORTS     NAMES
70f846e70b16   quay.io/openstack.kolla/horizon:2025.2-ubuntu-noble                     "dumb-init --single-…"   8 minutes ago    Up 8 minutes (healthy)              horizon
251c4f045166   quay.io/openstack.kolla/heat-engine:2025.2-ubuntu-noble                 "dumb-init --single-…"   9 minutes ago    Up 9 minutes (healthy)              heat_engine
fc7546336818   quay.io/openstack.kolla/heat-api-cfn:2025.2-ubuntu-noble                "dumb-init --single-…"   9 minutes ago    Up 9 minutes (healthy)              heat_api_cfn
cbeccb3898ae   quay.io/openstack.kolla/heat-api:2025.2-ubuntu-noble                    "dumb-init --single-…"   9 minutes ago    Up 9 minutes (healthy)              heat_api
a4e59f311193   quay.io/openstack.kolla/neutron-metadata-agent:2025.2-ubuntu-noble      "dumb-init --single-…"   10 minutes ago   Up 10 minutes                       neutron_metadata_agent
ed0136bb760f   quay.io/openstack.kolla/neutron-l3-agent:2025.2-ubuntu-noble            "dumb-init --single-…"   10 minutes ago   Up 10 minutes (healthy)             neutron_l3_agent
cc042f77dd6a   quay.io/openstack.kolla/neutron-dhcp-agent:2025.2-ubuntu-noble          "dumb-init --single-…"   10 minutes ago   Up 10 minutes (healthy)             neutron_dhcp_agent
7cb1757823df   quay.io/openstack.kolla/neutron-openvswitch-agent:2025.2-ubuntu-noble   "dumb-init --single-…"   10 minutes ago   Up 10 minutes (healthy)             neutron_openvswitch_agent
25bf01708ec4   quay.io/openstack.kolla/neutron-server:2025.2-ubuntu-noble              "dumb-init --single-…"   10 minutes ago   Up 10 minutes (healthy)             neutron_periodic_worker
48de935b5206   quay.io/openstack.kolla/neutron-server:2025.2-ubuntu-noble              "dumb-init --single-…"   10 minutes ago   Up 10 minutes (healthy)             neutron_rpc_server
acac2e42ff89   quay.io/openstack.kolla/neutron-server:2025.2-ubuntu-noble              "dumb-init --single-…"   10 minutes ago   Up 10 minutes (healthy)             neutron_server
545a90b13e81   quay.io/openstack.kolla/nova-novncproxy:2025.2-ubuntu-noble             "dumb-init --single-…"   13 minutes ago   Up 13 minutes (healthy)             nova_novncproxy
92c7176ca90a   quay.io/openstack.kolla/nova-conductor:2025.2-ubuntu-noble              "dumb-init --single-…"   13 minutes ago   Up 13 minutes (healthy)             nova_conductor
696252efbc7f   quay.io/openstack.kolla/nova-api:2025.2-ubuntu-noble                    "dumb-init --single-…"   14 minutes ago   Up 14 minutes (healthy)             nova_metadata
28dc0e43afb3   quay.io/openstack.kolla/nova-api:2025.2-ubuntu-noble                    "dumb-init --single-…"   14 minutes ago   Up 14 minutes (healthy)             nova_api
ed768addf4d2   quay.io/openstack.kolla/nova-scheduler:2025.2-ubuntu-noble              "dumb-init --single-…"   14 minutes ago   Up 14 minutes (healthy)             nova_scheduler
9a8f7c3ef793   quay.io/openstack.kolla/openvswitch-vswitchd:2025.2-ubuntu-noble        "dumb-init --single-…"   15 minutes ago   Up 15 minutes (healthy)             openvswitch_vswitchd
1c343bc14386   quay.io/openstack.kolla/openvswitch-db-server:2025.2-ubuntu-noble       "dumb-init --single-…"   15 minutes ago   Up 15 minutes (healthy)             openvswitch_db
646b26171d09   quay.io/openstack.kolla/placement-api:2025.2-ubuntu-noble               "dumb-init --single-…"   16 minutes ago   Up 16 minutes (healthy)             placement_api
7ae5435c7150   quay.io/openstack.kolla/cinder-scheduler:2025.2-ubuntu-noble            "dumb-init --single-…"   17 minutes ago   Up 17 minutes (healthy)             cinder_scheduler
cbf4d70e2eba   quay.io/openstack.kolla/cinder-api:2025.2-ubuntu-noble                  "dumb-init --single-…"   17 minutes ago   Up 17 minutes (healthy)             cinder_api
7fd547be49b2   quay.io/openstack.kolla/glance-api:2025.2-ubuntu-noble                  "dumb-init --single-…"   17 minutes ago   Up 17 minutes (healthy)             glance_api
8eaa1cba61ea   quay.io/openstack.kolla/keystone:2025.2-ubuntu-noble                    "dumb-init --single-…"   18 minutes ago   Up 18 minutes (healthy)             keystone
ec64c7fcdab7   quay.io/openstack.kolla/keystone-fernet:2025.2-ubuntu-noble             "dumb-init --single-…"   18 minutes ago   Up 18 minutes (healthy)             keystone_fernet
83bc81db454a   quay.io/openstack.kolla/keystone-ssh:2025.2-ubuntu-noble                "dumb-init --single-…"   18 minutes ago   Up 18 minutes (healthy)             keystone_ssh
555ef75d7519   quay.io/openstack.kolla/rabbitmq:2025.2-ubuntu-noble                    "dumb-init --single-…"   19 minutes ago   Up 19 minutes (healthy)             rabbitmq
633f761d4eb1   quay.io/openstack.kolla/memcached:2025.2-ubuntu-noble                   "dumb-init --single-…"   20 minutes ago   Up 20 minutes (healthy)             memcached
6d592fada747   quay.io/openstack.kolla/mariadb-server:2025.2-ubuntu-noble              "dumb-init -- kolla_…"   20 minutes ago   Up 20 minutes (healthy)             mariadb
2678a2f1c157   quay.io/openstack.kolla/keepalived:2025.2-ubuntu-noble                  "dumb-init --single-…"   21 minutes ago   Up 21 minutes                       keepalived
884b969e8ce7   quay.io/openstack.kolla/proxysql:2025.2-ubuntu-noble                    "dumb-init --single-…"   21 minutes ago   Up 21 minutes (healthy)             proxysql
bb7bf77a19f7   quay.io/openstack.kolla/haproxy:2025.2-ubuntu-noble                     "dumb-init --single-…"   21 minutes ago   Up 21 minutes (healthy)             haproxy
f280be196f23   quay.io/openstack.kolla/fluentd:2025.2-ubuntu-noble                     "dumb-init --single-…"   22 minutes ago   Up 22 minutes                       fluentd
0c2c41651f06   quay.io/openstack.kolla/cron:2025.2-ubuntu-noble                        "dumb-init --single-…"   22 minutes ago   Up 22 minutes                       cron
d7081ac57a1f   quay.io/openstack.kolla/kolla-toolbox:2025.2-ubuntu-noble               "dumb-init --single-…"   23 minutes ago   Up 23 minutes                       kolla_toolbox

```

Ademas en ese fichero tendras las credenciales necesarias para conectarte a horizon o si lo prefieres puedes crear un usuario nuevo :

## 13. Validación de redes, seguridad e instancias con la CLI

A continuación se ejecuta todo el flujo para verificar que OpenStack quedó operativo: crear redes pública/privada, ruteo, reglas de seguridad, imagen de prueba, flavor, puerto e instancia. Cada comando incluye su salida para que puedas contrastar.

**1. Crear red externa (flat) `public`** — se marca como externa y se asocia a `physnet1` (provider):

```bash
(kolla-venv) root@deployment:/home/vagrant# openstack network create public \
	--external \
	--provider-network-type flat \
	--provider-physical-network physnet1
+---------------------------+--------------------------------------+
| Field                     | Value                                |
+---------------------------+--------------------------------------+
| admin_state_up            | UP                                   |
| availability_zone_hints   |                                      |
| availability_zones        |                                      |
| created_at                | 2026-03-22T01:08:39Z                 |
| description               |                                      |
| dns_domain                | None                                 |
| id                        | 8bf87f52-d4b0-4723-9c3e-da59cf3a5d29 |
| ipv4_address_scope        | None                                 |
| ipv6_address_scope        | None                                 |
| is_default                | False                                |
| is_vlan_qinq              | None                                 |
| is_vlan_transparent       | None                                 |
| mtu                       | 1500                                 |
| name                      | public                               |
| port_security_enabled     | True                                 |
| project_id                | d994aa166c5d43a8b907bd878c41e53f     |
| provider:network_type     | flat                                 |
| provider:physical_network | physnet1                             |
| provider:segmentation_id  | None                                 |
| qos_policy_id             | None                                 |
| revision_number           | 1                                    |
| router:external           | External                             |
| segments                  | None                                 |
| shared                    | False                                |
| status                    | ACTIVE                               |
| subnets                   |                                      |
| tags                      |                                      |
| updated_at                | 2026-03-22T01:08:39Z                 |
+---------------------------+--------------------------------------+
```

**2. Crear subred pública sin DHCP** — rango `192.168.100.0/24`, puerta `192.168.100.1`:

```bash
(kolla-venv) root@deployment:/home/vagrant# openstack subnet create public-subnet \
	--network public \
	--subnet-range 192.168.100.0/24 \
	--no-dhcp
+----------------------+--------------------------------------+
| Field                | Value                                |
+----------------------+--------------------------------------+
| allocation_pools     | 192.168.100.2-192.168.100.254        |
| cidr                 | 192.168.100.0/24                     |
| created_at           | 2026-03-22T01:08:45Z                 |
| description          |                                      |
| dns_nameservers      |                                      |
| dns_publish_fixed_ip | None                                 |
| enable_dhcp          | False                                |
| gateway_ip           | 192.168.100.1                        |
| host_routes          |                                      |
| id                   | a07f72d8-60b6-448a-8f51-564c769a0438 |
| ip_version           | 4                                    |
| ipv6_address_mode    | None                                 |
| ipv6_ra_mode         | None                                 |
| name                 | public-subnet                        |
| network_id           | 8bf87f52-d4b0-4723-9c3e-da59cf3a5d29 |
| project_id           | d994aa166c5d43a8b907bd878c41e53f     |
| revision_number      | 0                                    |
| router:external      | True                                 |
| segment_id           | None                                 |
| service_types        |                                      |
| subnetpool_id        | None                                 |
| tags                 |                                      |
| updated_at           | 2026-03-22T01:08:45Z                 |
+----------------------+--------------------------------------+
```

**3. Crear red privada VXLAN `private`** — red interna para VMs:

```bash
(kolla-venv) root@deployment:/home/vagrant# openstack network create private
+---------------------------+--------------------------------------+
| Field                     | Value                                |
+---------------------------+--------------------------------------+
| admin_state_up            | UP                                   |
| availability_zone_hints   |                                      |
| availability_zones        |                                      |
| created_at                | 2026-03-22T01:08:52Z                 |
| description               |                                      |
| dns_domain                | None                                 |
| id                        | d0b738ae-0e44-4018-9c07-bbcb6d6af95c |
| ipv4_address_scope        | None                                 |
| ipv6_address_scope        | None                                 |
| is_default                | False                                |
| is_vlan_qinq              | None                                 |
| is_vlan_transparent       | None                                 |
| mtu                       | 1450                                 |
| name                      | private                              |
| port_security_enabled     | True                                 |
| project_id                | d994aa166c5d43a8b907bd878c41e53f     |
| provider:network_type     | vxlan                                |
| provider:physical_network | None                                 |
| provider:segmentation_id  | 729                                  |
| qos_policy_id             | None                                 |
| revision_number           | 1                                    |
| router:external           | Internal                             |
| segments                  | None                                 |
| shared                    | False                                |
| status                    | ACTIVE                               |
| subnets                   |                                      |
| tags                      |                                      |
| updated_at                | 2026-03-22T01:08:52Z                 |
+---------------------------+--------------------------------------+
```

**4. Crear subred privada con DNS** — rango `10.10.0.0/24`, DNS 8.8.8.8:

```bash
(kolla-venv) root@deployment:/home/vagrant# openstack subnet create private-subnet \
	--network private \
	--subnet-range 10.10.0.0/24 \
	--dns-nameserver 8.8.8.8
+----------------------+--------------------------------------+
| Field                | Value                                |
+----------------------+--------------------------------------+
| allocation_pools     | 10.10.0.2-10.10.0.254                |
| cidr                 | 10.10.0.0/24                         |
| created_at           | 2026-03-22T01:08:55Z                 |
| description          |                                      |
| dns_nameservers      | 8.8.8.8                              |
| dns_publish_fixed_ip | None                                 |
| enable_dhcp          | True                                 |
| gateway_ip           | 10.10.0.1                            |
| host_routes          |                                      |
| id                   | 693ee9de-8682-44b9-b496-56fd546e67f7 |
| ip_version           | 4                                    |
| ipv6_address_mode    | None                                 |
| ipv6_ra_mode         | None                                 |
| name                 | private-subnet                       |
| network_id           | d0b738ae-0e44-4018-9c07-bbcb6d6af95c |
| project_id           | d994aa166c5d43a8b907bd878c41e53f     |
| revision_number      | 0                                    |
| router:external      | False                                |
| segment_id           | None                                 |
| service_types        |                                      |
| subnetpool_id        | None                                 |
| tags                 |                                      |
| updated_at           | 2026-03-22T01:08:55Z                 |
+----------------------+--------------------------------------+
```

**5. Crear router (duplicado por error de nombre)** — se creó dos veces `router1`; el duplicado causó ambigüedad al asociar la subred:

```bash
(kolla-venv) root@deployment:/home/vagrant# openstack router create router1
(kolla-venv) root@deployment:/home/vagrant# openstack router add subnet router1 private-subnet
```

**6. Par de claves para las VMs** — se genera y se restringen permisos de la clave privada:

```bash
(kolla-venv) root@deployment:/home/vagrant# openstack keypair create mykey > mykey.pem
chmod 600 mykey.pem
```

**7. Reglas de seguridad** — permitir ICMP y SSH entrante en el grupo por defecto:

```bash
(kolla-venv) root@deployment:/home/vagrant# openstack security group rule create default --proto icmp
(kolla-venv) root@deployment:/home/vagrant# openstack security group rule create default \
	--proto tcp --dst-port 22
```

Salidas completas de las reglas:

```bash
+-------------------------+--------------------------------------+
| Field                   | Value                                |
+-------------------------+--------------------------------------+
| belongs_to_default_sg   | True                                 |
| created_at              | 2026-03-22T01:09:20Z                 |
| description             |                                      |
| direction               | ingress                              |
| ether_type              | IPv4                                 |
| id                      | 17e8c67d-e17a-4b06-bf18-7e5e7159f873 |
| normalized_cidr         | 0.0.0.0/0                            |
| port_range_max          | None                                 |
| port_range_min          | None                                 |
| project_id              | d994aa166c5d43a8b907bd878c41e53f     |
| protocol                | icmp                                 |
| remote_address_group_id | None                                 |
| remote_group_id         | None                                 |
| remote_ip_prefix        | 0.0.0.0/0                            |
| revision_number         | 0                                    |
| security_group_id       | 5b3f4a14-f463-40f2-a316-ef6c2854be73 |
| updated_at              | 2026-03-22T01:09:20Z                 |
+-------------------------+--------------------------------------+

+-------------------------+--------------------------------------+
| Field                   | Value                                |
+-------------------------+--------------------------------------+
| belongs_to_default_sg   | True                                 |
| created_at              | 2026-03-22T01:09:23Z                 |
| description             |                                      |
| direction               | ingress                              |
| ether_type              | IPv4                                 |
| id                      | fd6dea78-be24-460d-b89f-efd22b46b2a4 |
| normalized_cidr         | 0.0.0.0/0                            |
| port_range_max          | 22                                   |
| port_range_min          | 22                                   |
| project_id              | d994aa166c5d43a8b907bd878c41e53f     |
| protocol                | tcp                                  |
| remote_address_group_id | None                                 |
| remote_group_id         | None                                 |
| remote_ip_prefix        | 0.0.0.0/0                            |
| revision_number         | 0                                    |
| security_group_id       | 5b3f4a14-f463-40f2-a316-ef6c2854be73 |
| updated_at              | 2026-03-22T01:09:23Z                 |
+-------------------------+--------------------------------------+
```

**8. Descargar imagen de prueba CirrOS** — imagen base ligera para validar arranques:

```bash
(kolla-venv) root@deployment:/home/vagrant# wget http://download.cirros-cloud.net/0.6.2/cirros-0.6.2-x86_64-disk.img
```

**9. Registrar la imagen en Glance** — se publica como pública en formato QCOW2:

```bash
(kolla-venv) root@deployment:/home/vagrant# openstack image create "cirros" \
	--file cirros-0.6.2-x86_64-disk.img \
	--disk-format qcow2 \
	--container-format bare \
	--public
+------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Field            | Value                                                                                                                                                                                                                                                     |
+------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| checksum         | c8fc807773e5354afe61636071771906                                                                                                                                                                                                                          |
| container_format | bare                                                                                                                                                                                                                                                      |
| created_at       | 2026-03-22T01:09:34Z                                                                                                                                                                                                                                      |
| disk_format      | qcow2                                                                                                                                                                                                                                                     |
| file             | /v2/images/1c14cfdc-499c-4186-8f1b-8c23bc032429/file                                                                                                                                                                                                      |
| id               | 1c14cfdc-499c-4186-8f1b-8c23bc032429                                                                                                                                                                                                                      |
| min_disk         | 0                                                                                                                                                                                                                                                         |
| min_ram          | 0                                                                                                                                                                                                                                                         |
| name             | cirros                                                                                                                                                                                                                                                    |
| owner            | d994aa166c5d43a8b907bd878c41e53f                                                                                                                                                                                                                          |
| properties       | os_hash_algo='sha512', os_hash_value='1103b92ce8ad966e41235a4de260deb791ff571670c0342666c8582fbb9caefe6af07ebb11d34f44f8414b609b29c1bdf1d72ffa6faa39c88e8721d09847952b', os_hidden='False', owner_specified.openstack.md5='',                             |
|                  | owner_specified.openstack.object='images/cirros', owner_specified.openstack.sha256='', stores='file'                                                                                                                                                      |
| protected        | False                                                                                                                                                                                                                                                     |
| schema           | /v2/schemas/image                                                                                                                                                                                                                                         |
| size             | 21430272                                                                                                                                                                                                                                                  |
| status           | active                                                                                                                                                                                                                                                    |
| tags             |                                                                                                                                                                                                                                                           |
| updated_at       | 2026-03-22T01:09:34Z                                                                                                                                                                                                                                      |
| virtual_size     | 117440512                                                                                                                                                                                                                                                 |
| visibility       | public                                                                                                                                                                                                                                                    |
+------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

**10. Crear flavor mínimo `m1.tiny`** — 512 MB RAM, 1 vCPU, 1 GB disco:

```bash
(kolla-venv) root@deployment:/home/vagrant# openstack flavor create m1.tiny \
	--ram 512 \
	--disk 1 \
	--vcpus 1
+----------------------------+--------------------------------------+
| Field                      | Value                                |
+----------------------------+--------------------------------------+
| OS-FLV-DISABLED:disabled   | False                                |
| OS-FLV-EXT-DATA:ephemeral  | 0                                    |
| description                | None                                 |
| disk                       | 1                                    |
| id                         | 50ff37bf-719a-4b9a-9b56-f2e577e5a266 |
| name                       | m1.tiny                              |
| os-flavor-access:is_public | True                                 |
| properties                 |                                      |
| ram                        | 512                                  |
| rxtx_factor                | 1.0                                  |
| swap                       | 0                                    |
| vcpus                      | 1                                    |
+----------------------------+--------------------------------------+
```

**11. Crear un puerto en la red privada** — sirve para fijar IP antes de la VM:

```bash
(kolla-venv) root@deployment:/home/vagrant# openstack port create --network private vm-port
+-------------------------+----------------------------------------------------------------------------+
| Field                   | Value                                                                      |
+-------------------------+----------------------------------------------------------------------------+
| admin_state_up          | UP                                                                         |
| allowed_address_pairs   |                                                                            |
| binding_host_id         |                                                                            |
| binding_profile         |                                                                            |
| binding_vif_details     |                                                                            |
| binding_vif_type        | unbound                                                                    |
| binding_vnic_type       | normal                                                                     |
| created_at              | 2026-03-22T01:09:45Z                                                       |
| data_plane_status       | None                                                                       |
| description             |                                                                            |
| device_id               |                                                                            |
| device_owner            |                                                                            |
| device_profile          | None                                                                       |
| dns_assignment          |                                                                            |
| dns_domain              | None                                                                       |
| dns_name                | None                                                                       |
| extra_dhcp_opts         |                                                                            |
| fixed_ips               | ip_address='10.10.0.146', subnet_id='693ee9de-8682-44b9-b496-56fd546e67f7' |
| hardware_offload_type   | None                                                                       |
| hints                   |                                                                            |
| id                      | 78f15191-8a63-4fb5-b8bd-e3c01414436e                                       |
| ip_allocation           | None                                                                       |
| mac_address             | fa:16:3e:33:14:5d                                                          |
| name                    | vm-port                                                                    |
| network_id              | d0b738ae-0e44-4018-9c07-bbcb6d6af95c                                       |
| numa_affinity_policy    | None                                                                       |
| port_security_enabled   | True                                                                       |
| project_id              | d994aa166c5d43a8b907bd878c41e53f                                           |
| propagate_uplink_status | None                                                                       |
| resource_request        | None                                                                       |
| revision_number         | 1                                                                          |
| qos_network_policy_id   | None                                                                       |
| qos_policy_id           | None                                                                       |
| security_group_ids      | 5b3f4a14-f463-40f2-a316-ef6c2854be73                                       |
| status                  | DOWN                                                                       |
| tags                    |                                                                            |
| trunk_details           | None                                                                       |
| trusted                 | None                                                                       |
| updated_at              | 2026-03-22T01:09:45Z                                                       |
+-------------------------+----------------------------------------------------------------------------+
```

**12. Lanzar una instancia `vm1`** — usa flavor tiny, imagen CirrOS, red privada y la key `mykey`:

```bash
(kolla-venv) root@deployment:/home/vagrant# openstack server create vm1 \
	--flavor m1.tiny \
	--image cirros \
	--nic net-id=$(openstack network show private -f value -c id) \
	--security-group default \
	--key-name mykey
```

Una vez acabe de crearse la instancia deberiamos ver algo asi :

```bash
(kolla-venv) root@deployment:/home/vagrant# openstack server list
+--------------------------------------+------+--------+-------------------------------------+--------+---------+
| ID                                   | Name | Status | Networks                            | Image  | Flavor  |
+--------------------------------------+------+--------+-------------------------------------+--------+---------+
| 91547917-03a6-4fc4-bc85-e54083a6fc9b | vm1  | ACTIVE | private=10.10.0.184, 192.168.100.36 | cirros | m1.tiny |
+--------------------------------------+------+--------+-------------------------------------+--------+---------+
```

## 14. Validacion utilizando horizon

Esto mismo que hemos realizado usando la CLI , podemos comproabarlo usando la interfaz grafica.

Lo primero es loguearnos , recuerda que en neuestro caso puedes sacar la contraseña y el usuario del fichero `/etc/kolla/admin-openrc.sh`.

![](/images/openstack/instalacion-manual/login_openstack.png)

Una vez dentro , podemos ver una vista de los recursos de nuestro cluster de openstack que se estan utilizando:

![](/images/openstack/instalacion-manual/general_vieuw.png) 

Podemos listar la instancia que hemos creado y ver su estado:

![](/images/openstack/instalacion-manual/instances.png)

Por supuesto tambien podemos ver los servicios que hemos instalado:

![](/images/openstack/instalacion-manual/services.png)


Hasta aquí este post,la idea ha sido mostrar, de forma práctica, cómo desplegar una instalación básica de OpenStack en un entorno de laboratorio, entendiendo los pasos clave y los componentes implicados en el proceso.