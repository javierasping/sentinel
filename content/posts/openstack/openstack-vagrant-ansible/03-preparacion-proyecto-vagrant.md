---
title: "Preparación del proyecto Vagrant"
date: 2025-10-26
weight: 5
---

5.1. Estructura de directorios propuesta
```
openstack-vagrant-ansible/
├── Vagrantfile
├── keys/
│   ├── id_rsa
│   └── id_rsa.pub
├── mgmt-net.xml
├── provider-net.xml
└── setup-kvm.sh
```

5.2. Generación de claves SSH
- `ssh-keygen -t rsa -b 4096` y permisos adecuados.
- Uso compartido entre host y VMs mediante carpetas compartidas o provisioning scripts.

5.3. Creación del Vagrantfile
- Definición de VMs con IPs fijas, memoria, CPUs y conexiones a redes definidas.
- Ejemplo mínimo de provisión para instalar Python/SSH y habilitar Ansible desde el host.
