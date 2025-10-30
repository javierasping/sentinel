---
title: "OpenStack-Ansible CentOS 7 Multinode — Guía completa (deployment & configuración)"
date: 2025-10-29
weight: 50
tags: [openstack, openstack-ansible, centos7, multinode, guia]
hero: "/images/openstack/osa-centos7-hero.png"
---

## OpenStack-Ansible CentOS 7 Multinode — Guía completa

Esta guía recopila, paso a paso, todo lo necesario para preparar un deployment host con OpenStack-Ansible (OSA) y preparar los target hosts para un despliegue multinodo basado en CentOS 7. Incluye comandos reproducibles, fragmentos de configuración para `/etc/openstack_deploy` y comprobaciones de verificación.

Tabla de contenidos
- Prepare the deployment host
  - Configuring the operating system
  - Configure SSH keys
  - Configure the network
  - Install the source and dependencies
- Prepare the target hosts
  - Configuring the operating system
  - Configure SSH keys
  - Configuring the storage
  - Configuring the network
  - Host network bridges information
- Configure the deployment
  - Initial environment configuration
  - Installing additional services
  - Advanced service configuration
  - Configuring service credentials
- Run playbooks
  - Checking the integrity of the configuration files
  - Run the playbooks to install OpenStack
- Verifying OpenStack operation
  - Verify the API
  - Verifying the Dashboard (horizon)
- Resumen de archivos del repositorio `openstack-ansible/`
- Referencias

---

## Prepare the deployment host

Referencia: OpenStack-Ansible "Prepare the deployment host" (adaptado a CentOS 7)

> Nota: en producción se recomienda un host separado para deployment (Ansible). En entornos de laboratorio es aceptable usar uno de los infrastructure hosts como deployment host.

### Configuring the operating system

Asegurarse de que el deployment host tenga conectividad a Internet o a repositorios locales.

1. Actualizar paquetes y kernel

```bash
sudo -i
yum upgrade -y
# Si el kernel fue actualizado, reiniciar:
sudo reboot
```

2. Verificar versión de kernel

```bash
uname -mrs
yum list installed kernel
```

3. Instalar RDO (ejemplo Train/RDO - ajustar a la release deseada)

```bash
sudo yum install -y https://rdoproject.org/repos/openstack-train/rdo-release-train.rpm
```

4. Paquetes básicos recomendados

```bash
sudo yum install -y vim chrony openssh-server python-devel sudo '@Development Tools' lsof lvm2 bridge-utils iputils
```

5. Git (instalar Git 2.x en CentOS 7)

Por defecto CentOS 7 puede traer una versión antigua de git. Para instalar Git 2.x usando Wandisco:

```bash
cat << EOF | sudo tee /etc/yum.repos.d/wandisco-git.repo
[wandisco-git]
name=Wandisco GIT Repository
baseurl=http://opensource.wandisco.com/centos/7/git/\$basearch/
enabled=1
gpgcheck=1
gpgkey=http://opensource.wandisco.com/RPM-GPG-KEY-WANdisco
EOF

sudo rpm --import http://opensource.wandisco.com/RPM-GPG-KEY-WANdisco
sudo yum install -y git
git --version
```

6. NTP (chrony) configuración y verificación

```bash
sudo yum install -y chrony
sudo systemctl enable --now chronyd
chronyc sources
```

7. Firewall/SELinux

OpenStack-Ansible espera que firewalld esté deshabilitado en muchos despliegues de laboratorio. También se recomienda desactivar SELinux en CentOS 7 para evitar problemas durante la instalación (en entornos de producción prefiera estrategias más seguras).

```bash
sudo systemctl stop firewalld
sudo systemctl mask firewalld
# Deshabilitar SELinux (editar /etc/selinux/config o usar sed):
sudo sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
sudo sed -i 's/SELINUX=permissive/SELINUX=disabled/g' /etc/selinux/config
# Reiniciar si se cambió SELinux o kernel:
sudo reboot
```

> Nota: si en su entorno requiere SELinux habilitado, consulte documentación oficial para ajustes finos.

### Configure SSH keys

Ansible usa SSH con autenticación por llave pública. Desde el deployment host genere (si no existe) la llave RSA y copie la pública a los target hosts:

```bash
# En deployment host (como root o usuario que use Ansible):
ssh-keygen -t rsa -b 4096 -C "root@deployment" -f /root/.ssh/id_rsa -N ""
# Copiar la llave pública a cada target host:
ssh-copy-id -i /root/.ssh/id_rsa.pub root@TARGET_IP
# Probar:
ssh -o BatchMode=yes root@TARGET_IP 'hostname'
```

Important: OSA requiere que exista `/root/.ssh/id_rsa.pub` en el deployment host (es usada para inyectar la llave en los contenedores). Si usa otra llave, configure `lxc_container_ssh_key` en `openstack_user_config.yml`.

### Configure the network (deployment host)

El deployment host debe poder SSH a los target hosts en la red de administración (br-mgmt). Asigne una IP al deployment host dentro del rango designado para br-mgmt (por ejemplo en la guía se usa 172.29.236.0/22).

Ejemplo (ajuste a sus interfaces):

```bash
# /etc/sysconfig/network-scripts/ifcfg-bond0, ifcfg-bond0.10, etc. — dependen de su topología
# Asegure que el deployment host tenga una IP en la red br-mgmt
```

### Install the source and dependencies (OpenStack-Ansible)

Asegúrese de que `/usr/local/bin` esté en `$PATH` antes de ejecutar el bootstrap (el script coloca binarios allí):

```bash
export PATH=/usr/local/bin:$PATH
```

Clonar OpenStack-Ansible y moverse al directorio:

```bash
sudo git clone https://opendev.org/openstack/openstack-ansible /opt/openstack-ansible
cd /opt/openstack-ansible
# Elegir branch o tag estable. Ejemplo: stable/train
sudo git checkout stable/train
# Opcional: elegir un tag concreto (git describe --abbrev=0 --tags)
```

Bootstrap (descarga de Ansible y requisitos):

```bash
sudo scripts/bootstrap-ansible.sh
# Verificar comando
openstack-ansible --version
```

> El bootstrap puede tardar varios minutos (descarga de roles, pip, etc.)

---

## Prepare the target hosts

Referencia: OpenStack-Ansible "Prepare the target hosts"

Estas instrucciones deben ser ejecutadas en cada target host (compute, storage, network, infra según el rol asignado).

### Configuring the operating system

1. Actualizar paquetes y kernel

```bash
sudo -i
sudo yum upgrade -y
sudo reboot  # si se actualiza kernel
```

2. Desactivar SELinux

```bash
sudo sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
sudo sed -i 's/SELINUX=permissive/SELINUX=disabled/g' /etc/selinux/config
```

3. Instalar paquetes recomendados

```bash
sudo yum install -y bridge-utils iputils lsof lvm2 chrony openssh-server sudo tcpdump python
```

4. Módulos de kernel para bonding y VLAN (añadir a carga al arranque)

```bash
echo 'bonding' | sudo tee /etc/modules-load.d/openstack-ansible.conf
echo '8021q' | sudo tee -a /etc/modules-load.d/openstack-ansible.conf
sudo modprobe bonding
sudo modprobe 8021q
```

5. NTP

```bash
sudo yum install -y chrony
sudo systemctl enable --now chronyd
chronyc sources
```

6. Ajustes de kernel (opcional) — ejemplo para reducir verbosidad del log

```bash
echo "kernel.printk='4 1 7 4'" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

> Reiniciar si se cambian módulos críticos o kernel.

### Configure SSH keys (target hosts)

Como en la sección del deployment host: asegúrese de que la llave pública del deployment host esté presente en `/root/.ssh/authorized_keys` de cada target host.

```bash
# Desde el deployment host:
ssh-copy-id -i /root/.ssh/id_rsa.pub root@TARGET_IP
```

### Configuring the storage (ejemplo /dev/vdb -> cinder-volumes)

En el host de storage (por ejemplo `storage01`), si se dispone de un disco dedicado (ej. `/dev/vdb`) crear un PV/LV group para Cinder:

```bash
# ADVERTENCIA: los siguientes comandos destruyen datos en /dev/vdb
sudo wipefs -a /dev/vdb
sudo pvcreate --metadatasize 2048 /dev/vdb
sudo vgcreate cinder-volumes /dev/vdb
sudo vgs
```

OpenStack-Ansible detectará la VG `cinder-volumes` si está correctamente configurada y se puede usar para el backend LVM de Cinder.

> Nota: en la guía para Ubuntu hemos usado /dev/vdb; en CentOS reemplazar por el device correcto (/dev/sdb, /dev/vdb, etc.).

### Configuring the network (bridges)

OSA espera bridges concretos en cada host. Crear los bridges y asociarlos a interfaces físicas o a subinterfaces VLAN según sea necesario. Ejemplo de creación rápida (ajustar a su naming):

```bash
# Ejemplo simple para crear br-mgmt y asociarlo a una interfaz fisica (ej: eno1)
sudo nmcli connection add type bridge autoconnect yes con-name br-mgmt ifname br-mgmt
sudo nmcli connection add type ethernet autoconnect yes con-name br-mgmt-port ifname eno1 master br-mgmt
# Asignar IP estática a br-mgmt si corresponde
sudo nmcli connection modify br-mgmt ipv4.addresses 172.29.236.11/22 ipv4.method manual
sudo nmcli connection up br-mgmt
```

Para entornos basados en `ifcfg-*`, cree `/etc/sysconfig/network-scripts/ifcfg-br-mgmt` y los `ifcfg-` de las interfaces esclavas.

### Host network bridges information

Puentes requeridos (resumen):
- `br-mgmt` — Always: management (eth1 en contenedores)
- `br-storage` — storage traffic (eth2 en contenedores)
- `br-vxlan` — tunnel traffic (eth10 en contenedores) si usa VXLAN
- `br-vlan` — provider/VLAN networks (eth11 en contenedores) — no se asigna IP

Consulte `openstack_user_config.yml` para mapear interfaces y nombres de bridges a los ethX de los contenedores.

---

## Configure the deployment

Referencia: OpenStack-Ansible "Configure the deployment"

### Initial environment configuration

1. Copiar los templates de configuración de OSA a `/etc/openstack_deploy`:

```bash
sudo cp -R /opt/openstack-ansible/etc/openstack_deploy /etc/
sudo chown -R root:root /etc/openstack_deploy
cd /etc/openstack_deploy
```

2. Crear `openstack_user_config.yml` a partir del ejemplo y editarlo para su topología:

```bash
sudo cp openstack_user_config.yml.example openstack_user_config.yml
sudo vim openstack_user_config.yml
```

Puntos clave a editar en `openstack_user_config.yml`:
- Lista de hosts y grupos (shared-infra_hosts, compute_hosts, storage_hosts, network_hosts, etc.)
- provider_networks: definir networks provider y mapping a interfaces
- external_lb_vip_address (IP del LB público/horizon)
- lxc_container_ssh_key (si no usa `/root/.ssh/id_rsa.pub`)

Ejemplo parcial (provider_networks):

```yaml
provider_networks:
  - network: provider
    type: vlan
    vlan_range: 100:200
    bridge: br-vlan
    container_bridge: eth11
    mtu: 1500
```

3. Revisar y editar `user_variables.yml` (opciones globales)

```bash
sudo cp user_variables.yml.example user_variables.yml
sudo vim user_variables.yml
```

Variables importantes:
- `install_method`: source o distro (no se puede cambiar tras la instalación)
- `openstack_release`: ajuste según el branch/tag usado
- `lxc_container_ssh_key` si aplica

#### Habilitar backend LVM para Cinder (ejemplo)

Si creó la VG `cinder-volumes` en el host de storage, puede añadir este snippet en `user_variables.yml` (buscar `cinder_backends` y ajustar):

```yaml
cinder_backends:
  lvm:
    default: True
    description: LVM local backend
    volume_driver: cinder.volume.drivers.lvm.LVMVolumeDriver
    volume_backend_name: lvm
    volume_group: cinder-volumes
    target_helper: lioadm
```

- `target_helper`: opciones usuales: `lioadm` (recommended for recent kernels/userspace) o `tgtadm` (`tgt` package). Seleccione e instale el paquete correspondiente en `storage` host(s).

> Decisión pendiene: activar o no el backend LVM ahora. Si desea automatizarlo, descomente/añada este bloque antes de ejecutar `setup-openstack.yml`.

4. Generar `user_secrets.yml` con `pw-token-gen.py` y ajustar permisos

```bash
sudo /opt/openstack-ansible/scripts/pw-token-gen.py --file /etc/openstack_deploy/user_secrets.yml
sudo chown root:root /etc/openstack_deploy/user_secrets.yml
sudo chmod 640 /etc/openstack_deploy/user_secrets.yml
```

> Para regenerar contraseñas use `--regen`. No cambie contraseñas en un entorno ya desplegado sin las consideraciones necesarias.

5. Verificar sintaxis YAML (recomendado instalar `yamllint` en el deployment host)

```bash
# Instalar yamllint (ejemplo con pip)
sudo pip install yamllint
yamllint /etc/openstack_deploy/*.yml
```

### Installing additional services / Advanced configuration

- Añadir servicios usando los ficheros en `/etc/openstack_deploy/conf.d/` (copiar ejemplos y asignar hostgroups).
- Para configuración avanzada de roles, consulte la documentación de cada rol en la guía oficial.

### Configuring service credentials

- Ver `user_secrets.yml` y confirme `keystone_auth_admin_password` y otras variables.
- Considere usar Ansible Vault para mayor seguridad (fuera del alcance de esta guía básica).

---

## Run playbooks

Referencia: OpenStack-Ansible Run playbooks

### Checking the integrity of the configuration files

En el deployment host, desde `/opt/openstack-ansible/playbooks`:

```bash
cd /opt/openstack-ansible/playbooks
openstack-ansible setup-infrastructure.yml --syntax-check
openstack-ansible setup-openstack.yml --syntax-check
```

Asegúrese de que `yamllint` no reporte errores y que la sintaxis de los playbooks sea correcta.

### Run the playbooks to install OpenStack

Ejecute los playbooks en el orden recomendado. Es buena práctica guardar la salida en ficheros de log.

```bash
cd /opt/openstack-ansible/playbooks
# 1) Preparar hosts
openstack-ansible setup-hosts.yml 2>&1 | sudo tee /root/setup-hosts.log
# 2) Instalar infraestructura (Galera, RabbitMQ, utility container, etc.)
openstack-ansible setup-infrastructure.yml 2>&1 | sudo tee /root/setup-infrastructure.log
# 3) Instalar OpenStack
openstack-ansible setup-openstack.yml 2>&1 | sudo tee /root/setup-openstack.log
```

Confirmar `PLAY RECAP` con `unreachable=0` y `failed=0` para cada playbook.

> Recomendación: en entornos de laboratorio primero probar con `--limit` en grupos pequeños para reducir blast radius.

---

## Verifying OpenStack operation

Referencia: OpenStack-Ansible Verifying OpenStack operation

### Verify the API

1. Encontrar y adjuntarse al `utility` container (proporciona CLI):

```bash
lxc-ls | grep utility
# ejemplo:
lxc-attach -n infra1_utility_container-<id>
# dentro del contenedor:
. ~/openrc
openstack user list --os-cloud=default
```

2. Verificar servicios: ejemplo Galera

```bash
ansible galera_container -m shell -a "mysql -h localhost -e 'show status like \"%wsrep_cluster_%\";'"
```

### Verifying the Dashboard (Horizon)

- Abrir en navegador la IP `external_lb_vip_address` (https://EXTERNAL_LB_IP/).
- Autenticarse con usuario `admin` y contraseña definida en `user_secrets.yml` (`keystone_auth_admin_password`).

---

## Resumen de archivos del repositorio `openstack-ansible/`

Archivos clave (ubicación relativa a /opt/openstack-ansible):

- `/opt/openstack-ansible/etc/openstack_deploy/openstack_user_config.yml` — mapea hosts y redes
- `/opt/openstack-ansible/etc/openstack_deploy/user_variables.yml` — variables globales de despliegue
- `/opt/openstack-ansible/etc/openstack_deploy/user_secrets.yml` — contraseñas y secretos
- `/opt/openstack-ansible/etc/openstack_deploy/conf.d/*.yml` — configuración por servicio/rol
- `/opt/openstack-ansible/playbooks/setup-hosts.yml`
- `/opt/openstack-ansible/playbooks/setup-infrastructure.yml`
- `/opt/openstack-ansible/playbooks/setup-openstack.yml`

El directorio `etc/openstack_deploy/conf.d/` contiene ejemplos para cada servicio (glance.yml.aio, cinder.yml.aio, nova.yml.aio, etc.).

---

## Referencias

- OpenStack-Ansible Reference Guide
- OpenStack-Ansible User Guide
- OpenStack-Ansible Architecture - Container networking
- RDO Project (repositorios y paquetes para CentOS)

---

## Notas finales y checklist rápida antes de correr los playbooks

- [ ] Confirmar que el deployment host tiene su `/root/.ssh/id_rsa.pub` y que todos los target hosts aceptan esa llave.
- [ ] Confirmar `br-mgmt` y demás bridges configurados y que deployment host está en la misma L2 que br-mgmt.
- [ ] Si usará LVM para Cinder, confirmar `vgdisplay cinder-volumes` en los storage hosts.
- [ ] Ejecutar `yamllint /etc/openstack_deploy/*.yml` y `openstack-ansible <playbook> --syntax-check` antes de ejecutar los playbooks.
- [ ] Guardar logs: `openstack-ansible setup-hosts.yml 2>&1 | tee /root/setup-hosts.log`.


---

Si quiere, puedo:
- Añadir ejemplos reales y anonimizados de `openstack_user_config.yml` y `user_variables.yml` adaptados a su topología (indíqueme IPs/roles). 
- Habilitar el bloque LVM en el ejemplo de `user_variables.yml` y añadir instrucciones para instalar `lioadm`/`tgt` en los hosts de storage.
- Integrar esta guía en una entrada existente del sitio Hugo y ajustar frontmatter/links.

Indíqueme cuál es el siguiente paso que desea: 1) ajustar la guía con ejemplos de su topología (IPs/hosts), 2) habilitar el backend LVM en el archivo ejemplo ahora, o 3) integrar el archivo en otra sección del site.
