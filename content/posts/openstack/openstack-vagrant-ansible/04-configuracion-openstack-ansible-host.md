---
title: "Instalación y configuración de OpenStack-Ansible"
description: "Preparación del host de despliegue e instalación de OpenStack-Ansible para orquestar el despliegue de OpenStack en los nodos Vagrant"
date: 2025-10-26
tags: ["openstack", "openstack-ansible", "ansible", "vagrant", "ubuntu", "deployment"]
weight: 4
hero: images/openstack/openstack-vagrant-ansible/openstack-ansible-install.png
---

## 1. Introducción

En el [post anterior](../03-preparacion-proyecto-vagrant/) levantamos el escenario de 4 VMs con Vagrant (controller, network, compute y storage). Ahora preparamos el **host de despliegue** (tu PC físico) instalando **OpenStack-Ansible (OSA)**, que orquestará la instalación de OpenStack en esos nodos mediante Ansible.

> **Referencia**: [OpenStack-Ansible Deployment Guide](https://docs.openstack.org/project-deploy-guide/openstack-ansible/latest/)

### ¿Qué es OpenStack-Ansible?

**OpenStack-Ansible** es un conjunto de playbooks y roles de Ansible oficiales que automatizan el despliegue de OpenStack. OSA:

- Despliega servicios de OpenStack en **contenedores LXC** sobre los nodos objetivo.
- Gestiona automáticamente la configuración de redes, almacenamiento y alta disponibilidad.
- Soporta múltiples versiones de OpenStack (desde releases antiguos hasta las más recientes).
- Permite personalizar el despliegue mediante archivos YAML de configuración.

En nuestro caso, usaremos la **rama estable 2025.1 (Epoxy)** de OpenStack-Ansible para desplegar OpenStack Epoxy en Ubuntu 22.04.

---

## 2. Preparación del host de despliegue

### 2.1. Actualizar el sistema

```bash
sudo apt update && sudo apt upgrade -y
sudo reboot
```

### 2.2. Instalar dependencias

```bash
sudo apt install -y git python3-dev python3-venv python3-pip   build-essential libssl-dev libffi-dev chrony openssh-server
```

---

## 3. Instalación de OpenStack-Ansible

### 3.1. Clonar el repositorio

```bash
git clone https://opendev.org/openstack/openstack-ansible
cd openstack-ansible
```

### 3.2. Seleccionar la versión estable

```bash
git checkout stable/2025.1
```

### 3.3. Ejecutar el bootstrap de Ansible

El script `bootstrap-ansible.sh` instala **Ansible**, **los roles oficiales de OpenStack-Ansible** y todas las dependencias necesarias.

```bash
sudo scripts/bootstrap-ansible.sh
```

Verifica que el comando `openstack-ansible` esté disponible:

```bash
javiercruces@FJCD-PC:~/openstack-ansible (stable/2025.1) $ openstack-ansible --version
ansible-playbook [core 2.17.11]
  config file = None
  configured module search path = ['/etc/ansible/roles/ceph-ansible/library']
  ansible python module location = /opt/ansible-runtime/lib/python3.13/site-packages/ansible
  ansible collection location = /etc/ansible
  executable location = /opt/ansible-runtime/bin/ansible-playbook
  python version = 3.13.3 (main, Aug 14 2025, 11:53:40) [GCC 14.2.0] (/opt/ansible-runtime/bin/python3)
  jinja version = 3.1.5
  libyaml = True

EXIT NOTICE [Playbook execution success] **************************************
===============================================================================
```

---

## 4. Copiar la configuración base

Copia las plantillas de configuración a `/etc/openstack_deploy`:

```bash
sudo cp -R etc/openstack_deploy /etc/
```

Verifica el contenido:

```bash
ls -la /etc/openstack_deploy
```

Comprueba que existan los archivos:

- openstack_user_config.yml.example
- user_variables.yml o user_variables.yml.example
- user_secrets.yml.example

---

## 5. Configuración del despliegue

A partir de este punto configuramos los archivos que controlan el despliegue completo mediante Ansible.

### 5. Configuración del despliegue — pasos ampliados y comprobaciones

En esta sección se describen con más detalle los pasos que debes realizar en el deployment host (Ubuntu). Incluyo comandos exactos, comprobaciones y recomendaciones para evitar errores comunes.

#### 5.3 Editar `openstack_user_config.yml`


En este fichero se definen qué hosts ejecutan qué contenedores/servicios y cómo se mapean las redes físicas a las redes de contenedor, este debemos de crearlo en la ruta `/etc/openstack_deploy/openstack_user_config.yml` , si quieres puedes copiar mi fichero de ejemplo de mi repositorio .

```bash
sudo cp ~/openstack-vagrant-ansible/ansible-files/openstack_user_config.yml.example /etc/openstack_deploy/openstack_user_config.yml
```

- Campos clave a revisar/editar:
  - `internal_lb_vip_address` / `external_lb_vip_address`: IP del balanceador interno/externo. En laboratorio puedes usar la IP mgmt de `controller01` para ambos.
  - `provider_networks`: define `container_bridge` (ej. `br-vlan`, `br-vxlan`, `br-storage`) y `container_interface` (`ethX` del contenedor). Asegúrate de que los nombres de bridge coincidan con los creados en cada host (ver post 03).
  - Host groups: rellena las secciones `shared-infra_hosts`, `network_hosts`, `compute_hosts`, `storage_hosts` con las IPs mgmt (ej. 10.0.0.11..14). Cada entrada debe tener la clave `ip: <mgmt-ip>`.
  - `lxc_container_ssh_key` (opcional): si no quieres usar `/root/.ssh/id_rsa.pub` del deployment host, pega aquí la pública que usarán los contenedores.

Consejo: deja comentarios y no borres bloques enteros; ve haciendo cambios mínimos y ejecuta `yamllint` tras editar.

#### 5.4 Editar `user_variables.yml` — parámetros relevantes

En este fichero se definen variables críticas que controlan el despliegue de OpenStack-Ansible en los nodos. Debemos crearlo en la ruta /etc/openstack_deploy/user_variables.yml. Puedes copiar el ejemplo de mi repositorio como punto de partida: 

```bash
sudo cp ~/openstack-vagrant-ansible/ansible-files/user_variables.yml.example /etc/openstack_deploy/user_variables.yml
```

Valores importantes a confirmar:
- `install_method`: `source` (default) o `distro`. No cambies esto después del primer despliegue.
- `ansible_user`: usuario usado para SSH hacia los target hosts (`vagrant` en este laboratorio).
- `ansible_ssh_private_key_file`: ruta absoluta a la llave privada que Ansible usará (por ejemplo `/home/<tu_usuario>/openstack-vagrant-ansible/keys/id_rsa`). Asegúrate de que el archivo existe y tiene permisos 600.
- `cinder_backends`: si vas a usar LVM, añade el bloque con `volume_group: cinder-volumes` y `target_helper` (`tgtadm` o `lioadm`). Mantén este bloque comentado hasta que la VG exista.

#### 5.5 Generar `user_secrets.yml` con pw-token-gen.py

Genera contraseñas seguras para todos los servicios; este fichero es crítico.

```bash
cd ~/openstack-ansible
sudo ./scripts/pw-token-gen.py --file /etc/openstack_deploy/user_secrets.yml
```

Notas:
- No compartas `user_secrets.yml` públicamente.
- Para regenerar use `--regen` (peligroso en entornos ya desplegados).

#### 5.6 Ajustar permisos y propiedad

```bash
sudo chown root:root /etc/openstack_deploy/user_secrets.yml
sudo chmod 640 /etc/openstack_deploy/user_secrets.yml
sudo chmod 640 /etc/openstack_deploy/user_variables.yml
sudo chmod 640 /etc/openstack_deploy/openstack_user_config.yml
```

#### 5.7 Syntax-check de playbooks

```bash
cd ~/openstack-ansible/playbooks
sudo openstack-ansible setup-hosts.yml --syntax-check
sudo openstack-ansible setup-infrastructure.yml --syntax-check
sudo openstack-ansible setup-openstack.yml --syntax-check
```

Esto detecta errores de templates o variables faltantes sin ejecutar nada en hosts.

Si todo va bien los tres te devolveran esta salida :

```bash
EXIT NOTICE [Playbook execution success] **************************************
==============================================================================
```

#### 5.10 Probar conectividad Ansible con inventario dinámico

Ansible usa un inventario dinámico generado por OSA. Prueba un ping general:

```bash
sudo ansible -i ~/openstack-ansible/inventory/dynamic_inventory.py all -m ping
```

Si falla, comprueba:
- `ansible_user` en `user_variables.yml`.
- `ansible_ssh_private_key_file` — ruta absoluta y permisos 600.
- Que `/root/.ssh/authorized_keys` (o el usuario `vagrant`) en las VMs contiene la llave pública del deployment host (ver post 03).

#### 5.12 Guardar copia de seguridad de `/etc/openstack_deploy`

Antes de ejecutar playbooks guarda un backup:

```bash
sudo tar -czf /root/backup_openstack_deploy_$(date +%F).tgz /etc/openstack_deploy
```

#### 5.13 Ejecutar los playbooks principales (orden recomendado) y guardar logs

Ejecuta siempre en este orden y guarda salida completa:

```bash
cd /opt/openstack-ansible/playbooks
sudo openstack-ansible setup-hosts.yml 2>&1 | sudo tee /root/setup-hosts.log
sudo openstack-ansible setup-infrastructure.yml 2>&1 | sudo tee /root/setup-infrastructure.log
sudo openstack-ansible setup-openstack.yml 2>&1 | sudo tee /root/setup-openstack.log
```

Comprueba en cada log el `PLAY RECAP` y que `unreachable=0` y `failed=0`.

#### 5.14 Comprobaciones post-despliegue rápidas

Galera (estado de cluster):

```bash
sudo ansible galera_container -m shell -a "mysql -h localhost -e 'show status like \"%wsrep_cluster_%\";'"
```

Utility container y CLI de OpenStack:

```bash
sudo lxc-ls | grep utility
sudo lxc-attach -n <utility_container_name>
. ~/openrc
openstack user list --os-cloud=default
exit
```

Horizon: abrir https://<external_lb_vip_address>/ y loguear con `admin` y la contraseña `keystone_auth_admin_password` de `/etc/openstack_deploy/user_secrets.yml`.

#### 5.15 Problemas comunes y soluciones rápidas

- `openstack-ansible` no encontrado: re-ejecutar `bootstrap-ansible.sh` y exportar `/usr/local/bin`.
- `ansible ping` falla: prueba `ssh -i <key> <ansible_user>@<host>` manualmente, revisa permisos `~/.ssh` y `authorized_keys`.
- `yamllint` muestra errores: arregla indentación, evita tabulaciones.
- VG no visible en storage: revisa `lsblk`, `wipefs -a /dev/vdb` y los pasos de `pvcreate`/`vgcreate`.

---

### Ejemplo de fragmentos útiles (copiar/pegar)

Ejemplo breve `openstack_user_config.yml` (usar como referencia y adaptar):

```yaml
---
global_overrides:
  management_bridge: br-mgmt
  internal_lb_vip_address: 10.0.0.11
  external_lb_vip_address: 192.168.100.11
  provider_networks:
    - network:
        container_bridge: br-mgmt
        container_interface: eth1
        type: raw
    - network:
        container_bridge: br-vxlan
        container_interface: eth10
        type: vxlan

shared-infra_hosts:
  controller01:
    ip: 10.0.0.11

network_hosts:
  network01:
    ip: 10.0.0.12

compute_hosts:
  compute01:
    ip: 10.0.0.13

storage_hosts:
  storage01:
    ip: 10.0.0.14
```

Ejemplo breve `user_variables.yml` con LVM habilitado (activar sólo tras verificar VG):

```yaml
---
install_method: source
ansible_user: vagrant
ansible_ssh_private_key_file: /home/javiercruces/openstack-vagrant-ansible/keys/id_rsa

neutron_plugin_type: ml2
neutron_ml2_drivers_type: "vlan,vxlan"

cinder_backends:
  lvm:
    default: True
    volume_driver: cinder.volume.drivers.lvm.LVMVolumeDriver
    volume_group: cinder-volumes
    volume_backend_name: lvm
    target_helper: tgtadm

haproxy_enabled: false
```

---

Cuando quieras, puedo:
- Validar y ajustar estos ficheros con tus rutas exactas de proyecto (ruta absoluta a `id_rsa`).
- Generar un script `scripts/prepare_deployment_host.sh` en el repo que automatice los pasos repetitivos (copy, pw-token-gen, yamllint check, backup).
 
---

## 6. Verificar la configuración de Ansible

### 6.2. Comprobar sintaxis de playbooks

```bash
cd ~/openstack-ansible/playbooks
openstack-ansible setup-hosts.yml --syntax-check
```

### 6.3. Probar conectividad con los nodos

```bash
sudo ansible -i inventory/dynamic_inventory.py all -m ping
```

---

## 7. Siguientes pasos

En el siguiente post ejecutaremos los tres playbooks principales de OpenStack-Ansible:

1. `setup-hosts.yml`: prepara los nodos (contenedores LXC, red, dependencias).
2. `setup-infrastructure.yml`: despliega la infraestructura base (DB, RabbitMQ, Memcached, repositorio).
3. `setup-openstack.yml`: instala los servicios de OpenStack (Keystone, Glance, Nova, Neutron, Horizon, Cinder).

> Cada playbook puede tardar entre 30 minutos y 2 horas según tu hardware.