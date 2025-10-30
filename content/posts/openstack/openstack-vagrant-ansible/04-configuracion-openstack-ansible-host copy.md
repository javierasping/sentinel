---

title: "Instalación y configuración de OpenStack-Ansible"
description: "Preparación del host de despliegue e instalación de OpenStack-Ansible para orquestar el despliegue de OpenStack en los nodos Vagrant"
date: 2025-10-26
tags: ["openstack", "openstack-ansible", "ansible", "vagrant", "ubuntu", "deployment"]
weight: 4
hero: images/openstack/openstack-vagrant-ansible/openstack-ansible-install.png
------------------------------------------------------------------------------

## 1. Introducción

En el [post anterior](../03-preparacion-proyecto-vagrant/) levantamos el escenario de 4 VMs con Vagrant (controller, network, compute y storage). Ahora preparamos el **host de despliegue** (tu PC físico) instalando **OpenStack-Ansible (OSA)**, que orquestará la instalación de OpenStack en esos nodos mediante Ansible.

> **Referencia**: [OpenStack-Ansible Deployment Guide](https://docs.openstack.org/project-deploy-guide/openstack-ansible/latest/)

### 1.1. ¿Qué es OpenStack-Ansible?

**OpenStack-Ansible** es un conjunto de playbooks y roles de Ansible oficiales que automatizan el despliegue de OpenStack. OSA:

* Despliega servicios de OpenStack en **contenedores LXC** sobre los nodos objetivo.
* Gestiona automáticamente la configuración de redes, almacenamiento y alta disponibilidad.
* Soporta múltiples versiones de OpenStack.
* Permite personalizar el despliegue mediante archivos YAML de configuración.

En nuestro caso, usaremos la **rama estable 2025.1** de OpenStack-Ansible para desplegar OpenStack Epoxy en Ubuntu 22.04.

---

## 2. Preparación del host de despliegue

### 2.1. Actualizar el sistema

```bash
javiercruces@FJCD-PC:~$ sudo apt update && sudo apt upgrade -y
```

Si se actualizó el kernel, reinicia el sistema:

```bash
javiercruces@FJCD-PC:~$ sudo reboot
```

### 2.2. Instalar dependencias

```bash
javiercruces@FJCD-PC:~$ sudo apt install -y git python3-dev python3-venv python3-pip \
  build-essential libssl-dev libffi-dev chrony openssh-server
```

**Paquetes instalados:**

* **git**: para clonar el repositorio.
* **python3-dev, python3-pip**: Python3 y herramientas para instalar módulos.
* **build-essential, libssl-dev, libffi-dev**: librerías para compilar módulos de Python.
* **chrony**: sincronización de tiempo.
* **openssh-server**: acceso SSH desde/hacia los nodos.

---

## 3. Instalación de OpenStack-Ansible

### 3.1. Clonar el repositorio

```bash
javiercruces@FJCD-PC:~$ git clone https://opendev.org/openstack/openstack-ansible
javiercruces@FJCD-PC:~$ cd openstack-ansible
```

### 3.2. Seleccionar la versión estable

```bash
javiercruces@FJCD-PC:~/openstack-ansible$ git branch -r | grep stable
  origin/stable/2023.2
  origin/stable/2024.1
  origin/stable/2024.2
  origin/stable/2025.1
```

Cambiamos a la rama estable 2025.1:

```bash
javiercruces@FJCD-PC:~/openstack-ansible$ git checkout stable/2025.1
```

### 3.3. Bootstrap de Ansible

```bash
javiercruces@FJCD-PC:/opt/openstack-ansible$ sudo scripts/bootstrap-ansible.sh
```

Verifica que `openstack-ansible` esté disponible:

```bash
javiercruces@FJCD-PC:/opt/openstack-ansible$ openstack-ansible --version
```

---

## 4. Estructura de directorios y archivos clave

### 4.1. Repositorio clonado

* `playbooks/`: playbooks principales (`setup-hosts.yml`, `setup-infrastructure.yml`, `setup-openstack.yml`).
* `ansible_collections/`: colecciones de roles de Ansible.
* `etc/openstack_deploy/`: plantillas de configuración.
* `scripts/`: scripts de utilidad (`bootstrap-ansible.sh`, `pw-token-gen.py`).
* `tests/`: ejemplos para entornos AIO.

### 4.2. Directorio `/etc/openstack_deploy`

```bash
javiercruces@FJCD-PC:/opt/openstack-ansible$ sudo cp -R etc/openstack_deploy /etc/
javiercruces@FJCD-PC:/opt/openstack-ansible$ ls -la /etc/openstack_deploy
```

Archivos clave:

* `openstack_user_config.yml`: arquitectura del despliegue.
* `user_variables.yml`: variables de configuración global.
* `user_secrets.yml`: contraseñas de servicios.
* `conf.d/` y `env.d/`: configuraciones opcionales y definiciones de entorno.

---

## 5. Configuración del despliegue

### 5.1. Preparar los nodos objetivo

#### 5.1.1. Módulos de kernel para VLAN y bonding

```bash
javiercruces@FJCD-PC:~/openstack-vagrant-ansible$ for ip in 10.0.0.11 10.0.0.12 10.0.0.13 10.0.0.14; do
  ssh -i keys/id_rsa root@$ip 'grep -qxF "8021q" /etc/modules || echo "8021q" >> /etc/modules && grep -qxF "bonding" /etc/modules || echo "bonding" >> /etc/modules && modprobe 8021q && modprobe bonding'
done
```

#### 5.1.2. Configurar almacenamiento LVM en `storage01` (/dev/vdb)

```bash
vagrant@storage01:~$ sudo apt update && sudo apt install -y lvm2 thin-provisioning-tools
vagrant@storage01:~$ sudo wipefs -a /dev/vdb
vagrant@storage01:~$ sudo pvcreate /dev/vdb
vagrant@storage01:~$ sudo vgcreate cinder-volumes /dev/vdb
vagrant@storage01:~$ sudo vgs
```

> No crees particiones ni formatees `/dev/vdb`. LVM trabajará sobre el disco completo.

### 5.2. `openstack_user_config.yml`

```bash
sudo tee /etc/openstack_deploy/openstack_user_config.yml > /dev/null <<'EOF'
---
# Archivo adaptado a 4 nodos (controller, network, compute, storage)
...
EOF
```

*(El contenido de las redes y hosts permanece igual, solo revisa comillas y sintaxis YAML.)*

### 5.3. `user_variables.yml`

```bash
sudo tee /etc/openstack_deploy/user_variables.yml > /dev/null <<'EOF'
---
install_method: source
neutron_plugin_type: ml2.linuxbridge
neutron_ml2_drivers_type: "flat,vlan,vxlan"
...
EOF
```

> Corrige `ml2.lxb` a `ml2.linuxbridge` y revisa los backends de Cinder si usas LVM.

### 5.4. Generar secretos

```bash
python3 scripts/pw-token-gen.py --file etc/openstack_deploy/user_secrets.yml
```

### 5.5. Ajustar permisos

```bash
sudo chmod 640 etc/openstack_deploy/user_secrets.yml
sudo chmod 640 etc/openstack_deploy/user_variables.yml
sudo chmod 640 etc/openstack_deploy/openstack_user_config.yml
```

---

## 6. Verificación

### 6.1. Validar sintaxis YAML

```bash
sudo apt install -y yamllint
yamllint etc/openstack_deploy/openstack_user_config.yml
yamllint etc/openstack_deploy/user_variables.yml
```

### 6.2. Inventario dinámico y conectividad

```bash
cd ~/openstack-ansible/playbooks
openstack-ansible setup-hosts.yml --syntax-check
sudo ansible -i inventory/dynamic_inventory.py all -m ping
```

> Es normal que falle antes de generar el inventario completo.

---

## 7. Siguientes pasos

En el próximo post ejecutaremos los playbooks para desplegar OpenStack:

1. `setup-hosts.yml`
2. `setup-infrastructure.yml`
3. `setup-openstack.yml`

Cada playbook puede tardar entre 30 minutos y 2 horas, dependiendo de tu hardware.

> **Repositorio del proyecto**: [https://github.com/javierasping/openstack-vagrant-ansible](https://github.com/javierasping/openstack-vagrant-ansible)