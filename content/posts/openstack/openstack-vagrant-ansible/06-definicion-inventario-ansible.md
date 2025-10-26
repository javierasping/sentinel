---
title: "Definición del inventario Ansible"
date: 2025-10-26
weight: 8
---

### openstack_user_config.yml (inventario de ejemplo)

El archivo `openstack_user_config.yml` define los hosts y su asignación a grupos. Estructura mínima:

```yaml
openstack_hosts:
	controller01:
		networks:
			- mgmt: 10.0.0.11
	network01:
		networks:
			- mgmt: 10.0.0.12
	compute01:
		networks:
			- mgmt: 10.0.0.13
	storage01:
		networks:
			- mgmt: 10.0.0.14
```

Asignación de grupos en `openstack_user_config.yml` (ejemplo simplificado):

```yaml
host_groups:
	control:
		- controller01
	network:
		- network01
	compute:
		- compute01
	storage:
		- storage01
```

### Verificación de conectividad

Tras definir los hosts, verifica que Ansible pueda comunicarse con todos ellos:

```bash
ansible all -m ping
```

Proporciona ejemplos de variables por host en `user_variables.yml` para ajustar rutas, redes y roles específicos.
