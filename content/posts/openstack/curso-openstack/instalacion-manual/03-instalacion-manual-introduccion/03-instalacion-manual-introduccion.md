---
title: "03 - Guía de instalación manual de OpenStack con Vagrant"
date: 2025-11-23T12:00:00+00:00
description: "Aprende a desplegar un laboratorio OpenStack paso a paso usando Vagrant y entornos virtuales."
tags: [openstack,instalacion,vagrant]
hero: ""
weight: 3
---

## Introducción y alcance

En esta serie de posts te enseñaré cómo desplegar manualmente una instalación mínima de OpenStack sobre un laboratorio de máquinas virtuales gestionadas con Vagrant. Usaremos la versión Caracal 2024.1, la última disponible en la rama estable de los repositorios de Ubuntu. El objetivo no es ofrecer una solución de producción, sino entender los componentes, los ficheros de configuración clave y el orden correcto de despliegue para que una nube básica funcione con Keystone, Glance, Placement, Nova, Neutron, Cinder y Horizon.

Los ficheros que utilizo están disponibles en mi [repositorio](https://github.com/javierasping/openstack-vagrant-ansible#). Puedes clonarlo usando los siguientes comandos, ya sea por SSH o HTTPS:

```bash
git clone git@github.com:javierasping/openstack-vagrant-ansible.git
git clone https://github.com/javierasping/openstack-vagrant-ansible.git
```

Una vez clonado, todo lo referente a estos posts está en el directorio `manual-install`.

Los posts están pensados para leerse en orden y he incluido los comandos listos para copiar y pegar, por si quieres replicar el laboratorio.

## Escenario

Para el laboratorio de OpenStack utilizamos Vagrant con la imagen base bento/ubuntu-24.04, que proporciona un Ubuntu 24.04 limpio y listo para instalar todos los componentes de OpenStack. Hemos definido el dominio de ejemplo openstack.javiercd.es para facilitar la resolución de nombres y el uso de FQDN en todos los servicios. La red de gestión se llama mgmt-net y cada máquina virtual recibe una IP estática en esta red.

El laboratorio está compuesto por tres nodos, cada uno con su propio rol. 

El nodo controller01 actúa como controlador y aloja los servicios principales de OpenStack: Keystone, Glance API, Nova API, Cinder API y Horizon, con 2 vCPU y 6 GiB de RAM.

El nodo compute01 se encarga de ejecutar las instancias y los agentes de red, con 2 vCPU y 4 GiB de RAM.

Por último, el nodo storage01 proporciona almacenamiento persistente mediante Cinder con backend LVM, con 1 vCPU, 4 GiB de RAM y un disco adicional para los volúmenes.

Para virtualizar usaremos KVM/QEMU y desplegaré todo en mi máquina, que tiene Ubuntu 25 como sistema operativo.

En cuanto a las redes, como se trata de un entorno de laboratorio, solo configuramos dos por máquina. La red pública será la red por defecto de Vagrant (192.168.121.0/24), que permitirá que nuestras máquinas accedan a Internet, y una red privada con IPs estáticas asignadas en el Vagrantfile simulará nuestra red de gestión (10.0.0.0/24).

Si quieres, puedes modificar libremente los recursos asignados a cada nodo, cambiar los dominios empleados o ajustar las IPs según tus necesidades. Siéntete libre de adaptarlo a tu gusto si vas a replicar el laboratorio.

## Fuentes

Para realizar este laboratorio he recopilado información de varias fuentes. Para tenerlas centralizadas, las dejo en este post:

- [OpenStack Install Guide — Environment: SQL/Database on Ubuntu](https://docs.openstack.org/install-guide/environment-sql-database-ubuntu.html)
- [curso_openstack_ies - José Domingo Muñoz Rodríguez](https://github.com/josedom24/curso_openstack_ies/tree/main)
- [OpenStack Install Guide — OpenStack Services (resumen)](https://docs.openstack.org/install-guide/openstack-services.html)
- [Keystone — Instalación (2024.1 Caracal)](https://docs.openstack.org/keystone/2024.1/install/)
- [Glance — Instalación (2024.1 Caracal)](https://docs.openstack.org/glance/2024.1/install/)
- [Placement — Instalación (2024.1 Caracal)](https://docs.openstack.org/placement/2024.1/install/)
- [Nova — Instalación (2024.1 Caracal)](https://docs.openstack.org/nova/2024.1/install/)
- [Neutron — Instalación (2024.1 Caracal)](https://docs.openstack.org/neutron/2024.1/install/)
- [Cinder — Instalación (2024.1 Caracal)](https://docs.openstack.org/cinder/2024.1/install/)
- [Horizon — Instalación (2024.1 Caracal)](https://docs.openstack.org/horizon/2024.1/install/)