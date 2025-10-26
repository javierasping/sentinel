---
title: "Acceso y validación"
date: 2025-10-26
weight: 10
---

### Verificar los servicios de OpenStack

- Accede a Horizon usando la IP/hostname del balanceador externo por HTTPS (puerto 443).
- Inicia sesión con las credenciales de admin (revisa `user_secrets.yml` para la contraseña generada).

### Probar la CLI desde un contenedor utilitario

```bash
lxc-ls | grep utility
lxc-attach -n infra1_utility_container-XXXX
. ~/openrc
openstack user list --os-cloud=default
```

### Creación de usuarios, proyectos y prueba de instancias

1. Crear un proyecto y un usuario de pruebas desde la CLI o Horizon.
2. Lanza una instancia usando una imagen (Glance) y una flavor válida.
3. Asigna una IP flotante desde la red pública y verifica conectividad desde la instancia hacia el exterior.

### Comprobaciones de red desde las instancias

- Verifica reglas de seguridad (security groups) y que el router tenga rutas y SNAT habilitado para la red pública.
- Usa `ping`, `traceroute` y revisa las tablas de enrutamiento si hay problemas de conectividad.
