---
title: "Levantamiento del entorno"
date: 2025-10-26
weight: 6
---

Arranque del entorno:
- `vagrant up --provider=libvirt`
- Verificar IPs: `vagrant ssh -c "ip addr" NODENAME` o `virsh domifaddr`.
- Pruebas de conectividad: `ping` y `ssh` entre nodos.

Comprobaciones y resolución de problemas comunes durante el primer arranque.
