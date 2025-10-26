---
title: "Despliegue de OpenStack"
date: 2025-10-26
weight: 9
---

### Comprobaciones antes de ejecutar

1. Sintaxis y validación de los playbooks:

```bash
cd /opt/openstack-ansible/playbooks
openstack-ansible setup-infrastructure.yml --syntax-check
```

2. Revisa los ficheros en `/etc/openstack_deploy` y asegúrate de que `user_secrets.yml` y `openstack_user_config.yml` estén configurados.

### Ejecución de playbooks (orden recomendado)

```bash
# Preparar hosts
openstack-ansible setup-hosts.yml 2>&1 | tee /root/setup-hosts.log
# Infraestructura
openstack-ansible setup-infrastructure.yml 2>&1 | tee /root/setup-infra.log
# Servicios OpenStack
openstack-ansible setup-openstack.yml 2>&1 | tee /root/setup-openstack.log
```

### Supervisión y depuración

- Monitorea `PLAY RECAP` y busca `unreachable` o `failed`.
- Revisa logs de contenedores y `systemctl` dentro de los contenedores si una tarea falla.
- Usa `openstack-ansible --limit HOSTNAME playbook.yml` para limitar la ejecución a un host para depuración.

Consejos para errores comunes:
- Problemas de SSH/keys: verifica `authorized_keys` y permisos.
- Recursos insuficientes: comprueba memoria/CPU en los nodos.
- Errores de red: revisa bridges y tablas de enrutamiento.
