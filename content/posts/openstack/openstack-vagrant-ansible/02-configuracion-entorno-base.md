---
title: "Configuración del entorno base"
date: 2025-10-26
description: "Preparación del entorno local para desplegar OpenStack: configuración de KVM/libvirt, instalación de Vagrant y redes virtuales necesarias."
tags: [openstack, kvm, libvirt, vagrant, ansible, laboratorio]
weight: 2
hero: "/images/openstack/openstack-lab-setup.png"
---
## 1. Introducción

Antes de desplegar OpenStack con Ansible y Vagrant, debemos preparar el entorno base en nuestro **host físico**, que actuará como **nodo de despliegue**.  
Este post cubre la configuración esencial del entorno de virtualización (**KVM/libvirt**), la instalación de **Vagrant** con su **plugin `vagrant-libvirt`**, y la creación de las **redes virtuales** que usaremos más adelante para simular una topología real de OpenStack.

---

## 2. Instalación de KVM y libvirt

Si aún no tienes configurado KVM en tu sistema, revisa las guías de referencia que uso como base:

- [Instalar KVM y libvirt en Linux](https://www.javiercd.es/posts/virtualizacion-kvm-linux/instalacion-kvm/instalar-kvm-libvirt/instalar-kvm-libvirt/)
- [Validación de instalación KVM](https://www.javiercd.es/posts/virtualizacion-kvm-linux/instalacion-kvm/validar-host-kvm/validar-host-kvm/)

## 3. Instalación de Vagrant y del plugin `vagrant-libvirt`

### 3.1. Instalar Vagrant (Ubuntu/Debian)

Sigue la guía oficial de HashiCorp para instalar Vagrant. En Ubuntu/Debian los pasos típicos son:

```bash
# Descargar la clave GPG de hashicorp y añadirla a tu sistema
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
# Actualiza los repositorios y instala vagrant
sudo apt update -y && sudo apt install vagrant -y
```

Verifica la instalación:

```bash
javiercruces@FJCD-PC:~/openstack-vagrant-ansible $ vagrant --version
Vagrant 2.4.9
```

---

El plugin `vagrant-libvirt` permite a Vagrant gestionar máquinas con libvirt/KVM. Antes de instalarlo, instala las dependencias de compilación y los headers necesarios:

```bash
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients ebtables dnsmasq-base   ruby-dev libvirt-dev libxml2-dev libxslt-dev zlib1g-dev ruby-libvirt build-essential
```

Luego instala el plugin:

```bash
vagrant plugin install vagrant-libvirt
```

Comprueba que se instaló correctamente:

```bash
javiercruces@FJCD-PC:~/openstack-vagrant-ansible $ vagrant plugin list
vagrant-libvirt (0.12.2, global)
```
---

## 4. Creación de redes virtuales libvirt

Para simular una instalación real de OpenStack, utilizaremos **dos redes virtuales**:
- Una red de **gestión** (`mgmt-net`).
- Una red **proveedora** (`public-net`), que actuará como red pública.

Estos ficheros puedes encontrarlos en el repositorio https://github.com/javierasping/openstack-vagrant-ansible asi que te recomiendo que te lo clones :

```bash
# Comando para clonar por SSH
git clone git@github.com:javierasping/openstack-vagrant-ansible.git

# Comando para clonar por HTTPS
git clone https://github.com/javierasping/openstack-vagrant-ansible.git
```

Los ficheros los encontraras debajo del directorio networks-definition

### 4.1. Archivos XML de red

#### `mgmt-net.xml`

```xml
<network>
  <name>mgmt-net</name>
  <bridge name="virbr-mgmt" stp="on" delay="0"/>
  <ip address="10.0.0.1" netmask="255.255.255.0">
    <dhcp>
      <range start="10.0.0.100" end="10.0.0.254"/>
    </dhcp>
  </ip>
</network>
```

#### `public-net.xml`

```xml
<network>
  <name>public-net</name>
  <forward mode="nat"/>
  <bridge name="virbr-public" stp="on" delay="0"/>
  <ip address="192.168.100.1" netmask="255.255.255.0">
    <dhcp>
      <range start="192.168.100.100" end="192.168.100.254"/>
    </dhcp>
  </ip>
</network>
```

---

### 4.2. Definir y activar las redes

Ejecuta los siguientes comandos para crear y activar las redes en libvirt, para ello antes de ejecutarlos situate en el directorio `networks-definition` dentro del [repositorio](https://github.com/javierasping/openstack-vagrant-ansible) que has clonado anteriormente 

```bash
sudo virsh net-define mgmt-net.xml
sudo virsh net-start mgmt-net
sudo virsh net-autostart mgmt-net

sudo virsh net-define public-net.xml
sudo virsh net-start public-net
sudo virsh net-autostart public-net
```

Comprueba que están activas:

```bash
javiercruces@FJCD-PC:~/openstack-vagrant-ansible/networks-definition $ virsh net-list --all
 Name         State    Autostart   Persistent
-----------------------------------------------
 default      active   yes         yes
 mgmt-net     active   yes         yes
 public-net   active   yes         yes
```

---

## 5. Configuración de claves SSH para el host y las VMs

Para que Ansible y Vagrant puedan gestionar las máquinas virtuales de forma automática, necesitamos **crear un par de claves SSH** en el host y copiarlas a las VMs. Esto permitirá **acceso sin contraseña** desde el host a cada nodo.

---

### 5.1. Generar claves SSH en el host
En el repositorio clonado debe existir (o se debe crear) una carpeta `keys/` donde almacenaremos la clave privada y la pública que usarán Vagrant y Ansible.

Genera la clave en el host con:

```bash
mkdir -p ~/openstack-vagrant-ansible/keys
ssh-keygen -t rsa -b 4096 -f ~/openstack-vagrant-ansible/keys/id_rsa -N "" -C "openstack-lab"
```

Notas sobre las opciones usadas:
- `-f <ruta>`: ruta y nombre del fichero de la clave privada (la pública se guarda como `<ruta>.pub`).
- `-N ""`: passphrase vacía (sin contraseña) para uso automatizado.
- `-C "openstack-lab"`: comentario para identificar la clave.

Protege la clave privada:

```bash
chmod 600 ~/openstack-vagrant-ansible/keys/id_rsa
```

La estructura esperada en `keys/` después de generar las claves:

```bash
ls -l ~/openstack-vagrant-ansible/keys/
-rw------- 1 javiercruces javiercruces 3381 oct 27 00:40 id_rsa
-rw-r--r-- 1 javiercruces javiercruces  739 oct 27 00:40 id_rsa.pub
```
---