---
title: "Configuración de OpenStack-Ansible en el host"
date: 2025-10-26
weight: 7
---

### Instalación de requisitos en el host de despliegue

1. Actualizar paquetes y kernel:

```bash
sudo apt update && sudo apt upgrade -y
# Reinicia si se ha actualizado el kernel:
sudo reboot
```

2. Instalar paquetes requeridos para el host de despliegue:

```bash
sudo apt install -y git python3-dev python3-venv python3-pip build-essential chrony openssh-server sudo
```

3. Clonar OpenStack-Ansible y preparar el entorno:

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
- En Ubuntu, el script `bootstrap-ansible.sh` puede instalar su propio Python/Ansible en `/usr/local/bin`.
- Para reproducibilidad, despliega desde una etiqueta estable recomendada para tu release de OpenStack.

### Estructura de `/etc/openstack_deploy`

Tras copiar los ficheros de ejemplo, los ficheros clave a editar son:

- `openstack_user_config.yml`: asignación de hosts a grupos (control, network, compute, storage).
- `user_variables.yml`: variables de configuración (redes, paths, etc.).
- `user_secrets.yml`: secretos y contraseñas (genera con `pw-token-gen.py`).

Copiar los ficheros de ejemplo:

```bash
sudo cp -R /opt/openstack-ansible/etc/openstack_deploy /etc
cd /etc/openstack_deploy
sudo cp openstack_user_config.yml.example openstack_user_config.yml
```

Edita los archivos según tu topología y requisitos.
