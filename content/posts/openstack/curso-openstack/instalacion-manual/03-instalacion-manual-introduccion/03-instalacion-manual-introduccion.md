---
title: "03 - Guía de instalación manual de OpenStack con Vagrant"
date: 2025-11-23T12:00:00+00:00
description: "Aprende a desplegar un laboratorio OpenStack paso a paso usando Vagrant y entornos virtuales."
tags: [openstack,instalacion,vagrant]
hero: ""
weight: 3
---

## Introducción y alcance

En esta serie de posts te ensañare cómo desplegar manualmente una instalación mínima de OpenStack, en este caso es la ultima version disponible en la rama estable de los repositorios de ubuntu Caracal 2024.1, sobre un laboratorio de máquinas virtuales gestionadas con Vagrant. El objetivo no es ofrecer una solución de producción, sino entender los componentes, los ficheros de configuración clave y el orden correcto de despliegue para que una nube básica funcione: Keystone, Glance, Placement, Nova, Neutron, Cinder y Horizon.

Los ficheros que utilizo los puedes tener si accedes a mi [repositorio](https://github.com/javierasping/openstack-vagrant-ansible#):

```bash
git clone git@github.com:javierasping/openstack-vagrant-ansible.git
git clone https://github.com/javierasping/openstack-vagrant-ansible.git
```

Una vez clonado , todo lo referente a estos post esta debajo del directorio `manual-install`.

Los post están pensado para que los leas en orden y te he dejado los comandos para que los puedas copiar y pegar , en el caso de que quieras replicarlo .

## Escenario 

Para el laboratorio de OpenStack utilizamos Vagrant con la imagen base bento/ubuntu-24.04, que nos proporciona un Ubuntu 24.04 limpio y listo para instalar todos los componentes de la nube. Hemos definido un dominio de ejemplo openstack.javiercd.es para facilitar la resolución de nombres y el uso de FQDN en todos los servicios. La red de gestión se llama mgmt-net y cada máquina virtual recibe una IP estática, lo que garantiza una comunicación confiable entre los nodos sin depender de DHCP.

El laboratorio está compuesto por tres nodos con roles bien definidos. El nodo controller01 actúa como controlador y aloja los servicios principales de OpenStack, incluyendo Keystone, Glance API, Nova API, Cinder API y Horizon, con 2 vCPU y aproximadamente 6 GiB de RAM. El nodo compute01 se encarga de ejecutar las instancias y los agentes de red, con 2 vCPU y 4 GiB de RAM. Por último, el nodo storage01 proporciona almacenamiento persistente mediante Cinder con backend LVM, disponiendo de 1 vCPU, 4 GiB de RAM y un disco adicional para los volúmenes. Todo el entorno está pensado para un laboratorio de pruebas, usando libvirt como proveedor recomendado por su estabilidad y eficiencia en Linux.

En cuanto a las redes, como se trata de un entorno de laboratorio, solo configuramos dos por máquina. La red pública, proporcionada por libvirt, permitirá que nuestras máquinas accedan a Internet, y una red privada con IPs estáticas asignadas en el Vagrantfile simulará nuestra red de gestión.

Si quieres, puedes modificar libremente los recursos asignados a cada nodo o cambiar los dominios empleados según tus necesidades.

## Requisitos previos y recomendaciones

Para montar este laboratorio de OpenStack necesitarás que tu máquina tenga al menos 4 núcleos de CPU y 14 GB de RAM y con unos 50 GB de disco libres será suficiente. Yo lo he montado en mi equipo con Ubuntu 25 en el que ya tenía instalados KVM y Vagrant pero en tu caso tendrás que instalar estos paquetes antes de empezar. Además, asegúrate de que tu equipo soporte virtualización anidada para poder levantar correctamente las máquinas virtuales del laboratorio.

## Fuentes

Para realizar este laboratorio he ido recopilando informacion de varias fuentes , asi que para tenerlas centralizadas las dejare en este post:

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