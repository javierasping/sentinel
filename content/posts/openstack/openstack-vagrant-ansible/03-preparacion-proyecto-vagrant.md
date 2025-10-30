---
title: "Levantando las VMs con Vagrant"
date: 2025-10-26
description: "Construcción del Vagrantfile para levantar el escenario multinodo de OpenStack con KVM/libvirt, configuración de redes y verificación de conectividad."
tags: [openstack, vagrant, kvm, libvirt, ansible, laboratorio]
weight: 3
hero: "/images/openstack/vagrant-setup.png"
---

## 1. Introducción

En los posts anteriores preparamos el entorno base (KVM, libvirt, Vagrant y redes virtuales) y generamos las claves SSH. Ahora toca **construir el `Vagrantfile`** que definirá y levantará las **4 máquinas virtuales** de nuestro laboratorio OpenStack:

- **controller01** (control)
- **network01** (red)
- **compute01** (cómputo)
- **storage01** (almacenamiento)

Este post explica la estructura del `Vagrantfile`, cómo arranca cada nodo, cómo se conectan a las redes `mgmt-net` y `public-net`, y cómo verificar que todo está listo para el despliegue de OpenStack-Ansible.

---

## 2. Estructura del proyecto

La estructura del repositorio clonado debe ser:

```
openstack-vagrant-ansible/
├── Vagrantfile
├── keys/
│   ├── id_rsa
│   └── id_rsa.pub
├── networks-definition/
│   ├── mgmt-net.xml
│   └── public-net.xml
└── README.md
```

Si ya clonaste el repositorio y generaste las claves SSH en el post anterior, esta estructura debería estar lista.

---

## 3. El Vagrantfile

A continuación se muestra el `Vagrantfile` completo que usaremos. Este archivo define los 4 nodos con sus recursos (CPU, RAM), IPs fijas en las dos redes y provisioning inicial:

```ruby
Vagrant.configure("2") do |config|
  IMAGE = "bento/ubuntu-24.04"
  SSH_KEY_PATH = "keys/id_rsa"

  config.ssh.insert_key = false
  config.vm.box_check_update = false

  nodes = [
    { name: "controller01", ip_mgmt: "10.0.0.11", ip_pub: "192.168.100.11", cpu: 4,  mem: 8192 },
    { name: "network01",    ip_mgmt: "10.0.0.12", ip_pub: "192.168.100.12", cpu: 4,  mem: 6144 },
    { name: "compute01",    ip_mgmt: "10.0.0.13", ip_pub: "192.168.100.13", cpu: 8,  mem: 16384 },
    { name: "storage01",    ip_mgmt: "10.0.0.14", ip_pub: "192.168.100.14", cpu: 4,  mem: 8192 }
  ]

  # Desactivar red NAT por defecto de libvirt
  config.vm.provider :libvirt do |lv|
    lv.default_network = nil
    lv.nic_model_type = "virtio"
  end

  nodes.each do |node|
    config.vm.define node[:name] do |node_cfg|
      node_cfg.vm.box = IMAGE
      node_cfg.vm.hostname = "#{node[:name]}.local"

      node_cfg.vm.provider :libvirt do |lv|
        lv.cpus = node[:cpu]
        lv.memory = node[:mem]
        lv.nested = true
      end

      # Asignar IPs estáticas en mgmt-net y public-net
      node_cfg.vm.network :private_network, ip: node[:ip_mgmt],
        libvirt__network_name: "mgmt-net", libvirt__dhcp_enabled: false

      node_cfg.vm.network :private_network, ip: node[:ip_pub],
        libvirt__network_name: "public-net", libvirt__dhcp_enabled: false

      node_cfg.vm.provision "shell", inline: <<-SHELL
        apt update -y
        apt install -y python3 python3-pip git vim net-tools openssh-server
        mkdir -p /root/.ssh
        echo "$(cat /vagrant/keys/id_rsa.pub)" >> /root/.ssh/authorized_keys
        chmod 600 /root/.ssh/authorized_keys
        echo "Host *\n  StrictHostKeyChecking no\n" >> /root/.ssh/config
      SHELL
    end
  end
end
```

### 3.1. Explicación del Vagrantfile

- **IMAGE**: imagen base de Ubuntu 22.04 LTS (generic/ubuntu2204).
- **nodes**: array con los 4 nodos (nombre, IPs, CPU, RAM).
- **config.vm.network**: define las dos redes privadas (`mgmt-net` y `public-net`) sin DHCP (usamos IPs estáticas).
- **lv.nested = true**: habilita virtualización anidada en el nodo `compute01` (necesaria para que KVM funcione dentro de la VM).
- **Provisioning shell**: actualiza paquetes, instala Python3 (requerido por Ansible), Git, herramientas de red, copia la clave pública SSH a `/root/.ssh/authorized_keys` y deshabilita `StrictHostKeyChecking` para conexiones entre nodos.

---

## 4. Verificar las redes libvirt

Antes de levantar las VMs, verifica que las redes `mgmt-net` y `public-net` que creamos en el **post anterior** están activas:

```bash
javiercruces@FJCD-PC:~/openstack-vagrant-ansible $ virsh net-list --all
 Name              State    Autostart   Persistent
----------------------------------------------------
 default           active   yes         yes
 mgmt-net          active   no          yes
 public-net        active   no          yes
```

Si alguna red no está activa o no aparece, revisa el post anterior donde se detalla cómo crearlas y activarlas.

---

## 5. Levantar el entorno

Desde el directorio raíz del proyecto (`~/openstack-vagrant-ansible`), ejecuta:

```bash
vagrant up
```

Este comando:

1. Descarga la imagen `bento/ubuntu-24.04` si no la tienes (Utilizamos esta imagen ya que actualmente no existe una version oficial en vagrant de la version 24 de Ubuntu).
2. Crea las 4 VMs con los recursos asignados.
3. Configura las interfaces de red en `mgmt-net` y `public-net` con IPs estáticas.
4. Ejecuta el script de provisioning (actualiza paquetes, instala Python3, copia claves SSH).

Una vez completado, comprueba que todas las VMs están corriendo:

```bash
javiercruces@FJCD-PC:~/openstack-vagrant-ansible $ vagrant status
Current machine states:

controller01              running (libvirt)
network01                 running (libvirt)
compute01                 running (libvirt)
storage01                 running (libvirt)
```

También puedes verificar con `virsh`:

```bash
javiercruces@FJCD-PC:~/openstack-vagrant-ansible $ virsh list
 Id   Name                                     State
--------------------------------------------------------
 5    openstack-vagrant-ansible_network01      running
 6    openstack-vagrant-ansible_storage01      running
 7    openstack-vagrant-ansible_compute01      running
 8    openstack-vagrant-ansible_controller01   running
```

### 5.1. Preparación básica de las VMs (swap y módulos de kernel)

Antes de proceder con la preparación de almacenamiento o con OpenStack-Ansible, asegúrate de aplicar estas configuraciones básicas en todas las VMs (controller01, network01, compute01 y storage01):

- Añadir módulos de kernel necesarios para networking (8021q, bonding).

Instalar y cargar los módulos de kernel (8021q y bonding) en todos los nodos:

```bash
javiercruces@FJCD-PC:~/openstack-vagrant-ansible$ for ip in 10.0.0.11 10.0.0.12 10.0.0.13 10.0.0.14; do \
  ssh -i keys/id_rsa vagrant@$ip 'grep -qxF "8021q" /etc/modules || echo "8021q" | sudo tee -a /etc/modules; grep -qxF "bonding" /etc/modules || echo "bonding" | sudo tee -a /etc/modules; sudo modprobe 8021q; sudo modprobe bonding'; \
done
```

Verifica en un nodo cualquiera que los módulos están cargados

## 6. Configurar almacenamiento en `storage01` 

Si vas a usar Cinder con backend **LVM**, y ya añadiste un disco extra a la VM `storage01` (por ejemplo `/dev/vdb` de 500G), aquí tienes los pasos recomendados para prepararlo. Este apartado se colocó aquí porque la adición física del disco se realiza al crear la VM (post anterior), y la preparación LVM conviene ejecutarla antes de lanzar los playbooks de OSA.

1) Conéctate a `storage01` e instala las utilidades LVM:

```bash
javiercruces@FJCD-PC:~/openstack-vagrant-ansible$ ssh -i keys/id_rsa vagrant@10.0.0.14
vagrant@storage01:~$ sudo apt update && sudo apt install -y lvm2 thin-provisioning-tools
```

2) Verifica dispositivos disponibles (`vdb` debe ser el disco extra sin particiones):

```bash
vagrant@storage01:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
vda                       253:0    0   64G  0 disk 
├─vda1                    253:1    0    1M  0 part 
├─vda2                    253:2    0    2G  0 part /boot
└─vda3                    253:3    0   62G  0 part 
  └─ubuntu--vg-ubuntu--lv 252:0    0   31G  0 lvm  /
vdb                       253:16   0  500G  0 disk 
```

3) Limpia firmas previas y crea un Physical Volume sobre `/dev/vdb`:

```bash
vagrant@storage01:~$ sudo wipefs -a /dev/vdb
vagrant@storage01:~$ sudo pvcreate /dev/vdb
```

4) Crea el Volume Group que usará Cinder (`cinder-volumes`):

```bash
vagrant@storage01:~$ sudo vgcreate cinder-volumes /dev/vdb
```

5) Verifica el Volume Group:

```bash
vagrant@storage01:~$ sudo vgs
VG             #PV #LV #SN Attr   VSize   VFree
cinder-volumes   1   0   0 wz--n- 500.00g 500.00g
```

Notas importantes:
- No crees particiones ni formatees `/dev/vdb`. LVM trabajará sobre el disco completo.
- En Ubuntu, cuando actives el backend LVM en `user_variables.yml`, el `target_helper` recomendable puede ser `lioadm` o `tgtadm` según la versión y paquetes instalados; revisa la documentación del role de Cinder.

Cuando hayas preparado el VG, Cinder (si está configurado con LVM) podrá usar `cinder-volumes` para crear volúmenes.

---

## 7. Conexión SSH a las VMs

### 7.1. ¿Por qué no funciona `vagrant ssh`?

Como hemos desactivado la **red NAT por defecto** de Vagrant (`lv.management_network_name = nil`), el comando `vagrant ssh` **no funcionará**. Vagrant depende de esa red NAT para establecer túneles SSH automáticos.

En su lugar, usaremos **SSH directo** a través de las IPs de `mgmt-net` (10.0.0.x) con las claves SSH que generamos en el post anterior , que se encuentran debajo de `keys/`.

### 7.2. Conexión SSH con claves

Conéctate a cada nodo usando:

```bash
ssh -i keys/id_rsa vagrant@10.0.0.11  # controller01
ssh -i keys/id_rsa vagrant@10.0.0.12  # network01
ssh -i keys/id_rsa vagrant@10.0.0.13  # compute01
ssh -i keys/id_rsa vagrant@10.0.0.14  # storage01
```

También puedes conectarte como root (el provisioning copia la clave pública a `/root/.ssh/authorized_keys`):

```bash
ssh -i keys/id_rsa root@10.0.0.11
```

### 7.3. Crear alias para facilitar el acceso

Para no tener que escribir el comando completo cada vez, puedes crear alias en tu shell. Añade estas líneas al final de tu archivo `~/.bashrc` o `~/.zshrc`:

```bash
alias ssh-controller='ssh -i ~/ruta/a/tu/proyecto/keys/id_rsa vagrant@10.0.0.11'
alias ssh-network='ssh -i ~/ruta/a/tu/proyecto/keys/id_rsa vagrant@10.0.0.12'
alias ssh-compute='ssh -i ~/ruta/a/tu/proyecto/keys/id_rsa vagrant@10.0.0.13'
alias ssh-storage='ssh -i ~/ruta/a/tu/proyecto/keys/id_rsa vagrant@10.0.0.14'
```

> **Nota**: cambia `~/ruta/a/tu/proyecto/` por la ruta absoluta donde clonaste el repositorio.

Luego recarga el archivo de configuración:

```bash
source ~/.bashrc
```

Ahora puedes conectarte simplemente usando alias:

```bash
ssh-controller
ssh-network
ssh-compute
ssh-storage
```

### 7.4. Verificar conectividad entre nodos

Desde el host, verifica que puedes hacer ping a todos los nodos:

```bash
ping -c 2 10.0.0.11
ping -c 2 10.0.0.12
ping -c 2 10.0.0.13
ping -c 2 10.0.0.14
```

Si quieres verificar conectividad desde dentro de una VM:

```bash
ssh -i keys/id_rsa vagrant@10.0.0.11
ping -c 2 10.0.0.12  # Hacer ping a network01
ping -c 2 192.168.100.13  # Hacer ping a compute01 en la red pública
exit
```

---
