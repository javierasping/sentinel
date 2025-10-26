# OpenStack-Ansible — Ubuntu Multinodo (borrador)

Esta es una versión adaptada a Ubuntu con notas para la instalación multinodo con OpenStack-Ansible (basada en un ejemplo original para CentOS). Usa este directorio para recopilar playbooks, notas de inventario y pasos de preflight para desplegar OpenStack con OpenStack-Ansible en hosts objetivo.

## Tabla de contenidos

- Preparar el host de despliegue
  - Configurar el sistema operativo (Ubuntu)
  - Configurar claves SSH
  - Configurar la red
  - Instalar el código fuente y dependencias
- Preparar los hosts objetivo
  - Configurar el sistema operativo (Ubuntu)
  - Configurar claves SSH
  - Configurar almacenamiento (LVM)
  - Configurar la red (bridges)
- Configurar el despliegue
  - Configuración inicial del entorno
  - Instalar servicios adicionales
  - Configuración avanzada de servicios
  - Configurar credenciales de servicios
- Ejecutar playbooks
  - Verificar los archivos de configuración
  - Ejecutar los playbooks para instalar OpenStack
- Verificar el funcionamiento de OpenStack
  - Verificar la API
  - Verificar el Dashboard (Horizon)
- Referencias

---

> Estado: borrador. Este README proporciona comandos y notas adaptadas para Ubuntu (las suposiciones aparecen más abajo). Revisa y ajusta versiones y nombres de paquetes para tu versión de Ubuntu (se recomienda 20.04 o 22.04 para ramas recientes de OSA).

## Supuestos y notas

- Se pidió preparar el despliegue en Ubuntu. El ejemplo original era para CentOS 7; muchos nombres de paquetes y herramientas difieren en Ubuntu (apt vs yum, nombres de servicios en systemd, etc.).
- Esta guía es un punto de partida. Valida siempre la documentación oficial del proyecto OpenStack-Ansible (OpenStack-Ansible User Guide / Reference) para conocer la versión de Ubuntu soportada y requisitos específicos de los playbooks.
- Se asume un host de despliegue separado que ejecutará Ansible y orquestará los hosts objetivo. Para entornos de prueba pequeños puedes usar uno de los hosts objetivo como host de despliegue.

## Preparar el host de despliegue

### Configurar el sistema operativo (Ubuntu)

1. Actualizar paquetes y kernel:

```bash
sudo apt update && sudo apt upgrade -y
# Reinicia si se ha actualizado el kernel:
sudo reboot
```

2. Verificar versión del kernel:

```bash
uname -mrs
```

3. Instalar paquetes requeridos (lista de ejemplo — adáptala según convenga):

```bash
sudo apt install -y build-essential git python3-dev python3-venv python3-pip chrony openssh-server sudo
```

4. Asegurarse de que `/usr/local/bin` esté en PATH (algunos scripts de bootstrap de OSA instalan herramientas allí):

```bash
export PATH=/usr/local/bin:$PATH
```

### Configurar claves SSH

Ansible usa autenticación por clave pública SSH. Crea o reutiliza un par de claves en el host de despliegue y copia la clave pública a `/root/.ssh/authorized_keys` en cada host objetivo (o a la cuenta que Ansible vaya a usar).

```bash
ssh-keygen -t rsa -b 4096 -C "root@deployment"
ssh-copy-id root@TARGET_HOST
# probar
ssh root@TARGET_HOST hostname
```

Nota: OpenStack-Ansible espera que exista `/root/.ssh/id_rsa.pub` en el host de despliegue para algunas operaciones (contenedores). Si usas una clave distinta, configura la variable correspondiente en tu configuración de OSA.

### Configurar la red

Asegura que el host de despliegue pueda alcanzar a los hosts objetivo sobre L2 para las redes de gestión de contenedores (br-mgmt). Elige direcciones para la red de gestión de contenedores, por ejemplo `172.29.236.0/22`.

### Instalar el código fuente y dependencias

Clona OpenStack-Ansible y ejecuta el bootstrap:

```bash
sudo git clone https://opendev.org/openstack/openstack-ansible /opt/openstack-ansible
cd /opt/openstack-ansible
# Cambia a una rama/etiqueta estable (ejemplo: stable/train)
sudo git checkout stable/train
sudo scripts/bootstrap-ansible.sh
# Verificar que el comando esté disponible
openstack-ansible --version
```

Notas:
- En Ubuntu el script de bootstrap instalará su propio Python/Ansible en `/usr/local/bin`.
- Usa la etiqueta estable recomendada para tu release de OpenStack. Desplegar desde una etiqueta específica mejora la reproducibilidad.

## Preparar los hosts objetivo

### Configurar el sistema operativo (Ubuntu)

1. Actualizar paquetes y kernel:

```bash
sudo apt update && sudo apt upgrade -y
sudo reboot
```

2. Deshabilitar AppArmor o ajustarlo si es necesario (según políticas). Para LXC/contenedores asegura que los módulos de kernel requeridos estén disponibles.

3. Instalar paquetes requeridos:

```bash
sudo apt install -y bridge-utils lsof lvm2 chrony openssh-server tcpdump python3
```

4. Habilitar módulos de kernel para bonding y 8021q si son necesarios (añadir en `/etc/modules-load.d/openstack-ansible.conf`):

```bash
sudo tee /etc/modules-load.d/openstack-ansible.conf <<'EOF'
bonding
8021q
EOF
```

5. Configurar NTP (chrony):

```bash
sudo systemctl restart chrony
chronyc sources
```

6. Opcional: reducir la verbosidad de logs del kernel (sysctl):

```bash
echo "kernel.printk='4 1 7 4'" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### Configurar claves SSH (hosts objetivo)

Copia la clave pública del host de despliegue en `/root/.ssh/authorized_keys` en cada host objetivo. Prueba el acceso SSH desde el host de despliegue.

### Configurar almacenamiento (LVM)

OpenStack-Ansible auto-configura LVM para algunos servicios, pero puede convenirte preparar dispositivos de bloque dedicados para volúmenes de cinder:

```bash
# Ejemplo: crear PV y VG (reemplaza /dev/sdX por el dispositivo real)
sudo pvcreate --metadatasize 2048 /dev/sdX
sudo vgcreate cinder-volumes /dev/sdX
```

Nota: OSA puede sobrescribir la configuración LVM si lo gestiona automáticamente. Haz copia de seguridad de cualquier configuración LVM existente.

### Configurar la red (bridges)

Crea los bridges en el host que el entorno necesite (ejemplos): `br-mgmt`, `br-storage`, `br-vxlan`, `br-vlan`. Configúralos con la herramienta de red de la distribución (netplan en Ubuntu 18.04+ o `/etc/network/interfaces` en versiones más antiguas) y asegúrate que existan y sean accesibles desde el host de despliegue.

Ejemplo (snippet para netplan):

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp1s0:
      dhcp4: no
  bridges:
    br-mgmt:
      interfaces: [enp1s0]
      addresses: [172.29.236.10/22]
```

Ajusta esto a tu topología física y VLANs.

## Configurar el despliegue

### Configuración inicial del entorno

Copia los archivos de despliegue de referencia desde el repositorio clonado de OSA a `/etc/openstack_deploy` y edítalos:

```bash
sudo cp -R /opt/openstack-ansible/etc/openstack_deploy /etc
cd /etc/openstack_deploy
sudo cp openstack_user_config.yml.example openstack_user_config.yml
# Edita openstack_user_config.yml para asignar hosts y redes
sudo vim openstack_user_config.yml
```

Edita `user_variables.yml` y otros archivos de configuración según sea necesario. Presta atención a `install_method` (source vs paquetes de la distro) y a las asignaciones de grupos de hosts.

### Configurar credenciales de servicios

Establece secretos en `/etc/openstack_deploy/user_secrets.yml`. Usa `pw-token-gen.py` para generar valores aleatorios seguros:

```bash
cd /opt/openstack-ansible
sudo ./scripts/pw-token-gen.py --file /etc/openstack_deploy/user_secrets.yml
```

Protege los permisos del fichero.

## Ejecutar playbooks

1. Comprobar sintaxis de los archivos (recomendado):

```bash
cd /opt/openstack-ansible/playbooks
openstack-ansible setup-infrastructure.yml --syntax-check
```

2. Ejecutar los playbooks en orden:

```bash
# Preparar hosts
openstack-ansible setup-hosts.yml 2>&1 | tee /root/setup-hosts.log
# Infraestructura
openstack-ansible setup-infrastructure.yml 2>&1 | tee /root/setup-infra.log
# Servicios OpenStack
openstack-ansible setup-openstack.yml 2>&1 | tee /root/setup-openstack.log
```

Monitoriza el `PLAY RECAP` para que `unreachable=0` y `failed=0`.

## Verificar el funcionamiento de OpenStack

- Entra en un contenedor utilitario y haz `source` del `openrc` para probar la CLI de OpenStack:

```bash
lxc-ls | grep utility
lxc-attach -n infra1_utility_container-XXXX
. ~/openrc
openstack user list --os-cloud=default
```

- Accede a Horizon mediante la IP del balanceador externo por HTTPS (puerto 443) e inicia sesión con `admin` / `keystone_auth_admin_password`.

## Referencias

- OpenStack-Ansible Reference Guide
- OpenStack-Ansible User Guide
- OpenStack-Ansible Architecture - Container Networking

---

Si quieres, puedo:

- añadir más archivos (ejemplo `openstack_user_config.yml.example` con snippets, diagramas de red),
- crear una pequeña checklist `preflight.md` con comandos de validación rápida,
- o generar un esqueleto de inventario y snippets de configuración Ansible bajo este nuevo directorio.

Dime cuál de las opciones prefieres y lo añado.