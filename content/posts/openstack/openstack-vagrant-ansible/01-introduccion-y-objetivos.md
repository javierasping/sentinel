---
title: "Introducción y objetivos"
date: 2025-10-26
description: "Laboratorio para desplegar OpenStack usando Vagrant, KVM y OpenStack-Ansible. Topología multinodo, redes libvirt, Vagrantfile y preparación del host de despliegue."
tags: [openstack, vagrant, kvm, ansible, openstack-ansible, laboratorio]
weight: 1
hero: "/images/openstack/portada_openstack.png"
---

## Introducción

El objetivo de esta serie de artículos es mostrar cómo montar un **laboratorio de OpenStack** en un entorno **local** utilizando un **único host físico**, de forma que puedas **aprender sus componentes** y comprender el **proceso de instalación completo** de manera práctica y controlada.

Para conseguirlo, usaremos **Vagrant + KVM/libvirt** para crear y gestionar las máquinas virtuales del entorno, y **OpenStack-Ansible (OSA)** como herramienta de despliegue automatizado.  
Este enfoque permite simular una instalación multinodo real de OpenStack sin necesidad de disponer de varios equipos físicos.

---

## Enfoque y fuentes

El laboratorio se basa en la **documentación oficial de OpenStack-Ansible**, adaptada y comentada paso a paso para un escenario local.  
Cada fase se explicará con ejemplos prácticos, configuraciones reales y recomendaciones basadas en pruebas, con el objetivo de que puedas reproducir el entorno completo desde tu propio ordenador.

---

## Objetivo del laboratorio

La meta es **simular una instalación profesional de OpenStack**, utilizando **máquinas virtuales gestionadas por Vagrant y libvirt**, mientras el **host físico actúa como nodo de despliegue** (donde se ejecutan Ansible y OSA).  
De esta forma, podrás probar y entender la arquitectura típica de una nube OpenStack sin necesidad de un entorno de producción.

---

## Arquitectura del escenario

A continuación se muestra la arquitectura propuesta para este laboratorio:

| Nodo (host/VM) | Rol | IP (mgmt) | IP (provider) | vCPU | RAM | Notas |
|-----------------|------|------------|----------------|------|------|--------|
| **Tu PC (host)** | Nodo de despliegue / Ansible | 10.0.0.10 | 192.168.100.10 | — | — | Ejecuta Ansible, Git y OpenStack-Ansible (no forma parte del clúster) |
| **controller01** | Control principal | 10.0.0.11 | 192.168.100.11 | 4 | 8 GB | Keystone, Glance, APIs y servicios centrales |
| **network01** | Nodo de red | 10.0.0.12 | 192.168.100.12 | 4 | 6 GB | Neutron (L3, DHCP, metadata), agentes de red |
| **compute01** | Nodo de cómputo | 10.0.0.13 | 192.168.100.13 | 8 | 16 GB | Nova compute (KVM) para instancias |
| **storage01** | Nodo de almacenamiento | 10.0.0.14 | 192.168.100.14 | 4 | 8 GB | Cinder o backend de almacenamiento (Ceph/dummy) |

> **Requisitos mínimos del host:** alrededor de **20 vCPU** y **38 GB de RAM** disponibles, dejando margen para el sistema base y herramientas locales.

---

## Componentes de OpenStack desplegados

OpenStack es una plataforma modular compuesta por múltiples servicios. A continuación, se describen brevemente los componentes principales que instalaremos en cada nodo:

### **Controller (controller01)**

El nodo de control ejecuta los **servicios centrales** de OpenStack:

- **Keystone** (Identidad): servicio de autenticación y autorización centralizado. Gestiona usuarios, proyectos (tenants) y permisos.
- **Glance** (Imágenes): almacena y gestiona imágenes de sistemas operativos (Ubuntu, CentOS, etc.) que se usan para crear instancias.
- **Nova API** y **Scheduler**: orquestan el lanzamiento de instancias, deciden en qué nodo de cómputo ejecutarlas y gestionan el ciclo de vida de las máquinas virtuales.
- **Neutron Server**: proporciona la API y el control lógico de las redes virtuales (redes, subredes, routers, security groups).
- **Horizon** (Dashboard web): interfaz gráfica de administración y gestión de OpenStack para usuarios finales y administradores.
- **Cinder API** y **Scheduler** (opcional): orquestan la creación y asignación de volúmenes de almacenamiento en bloque.
- **Bases de datos (MariaDB/MySQL)** y **RabbitMQ**: almacenamiento de metadatos y mensajería entre servicios.

### **Network (network01)**

El nodo de red ejecuta los **agentes de red de Neutron**, encargados de:

- **L3 Agent**: proporciona routing entre redes internas y externas, incluyendo NAT (SNAT/DNAT) y asignación de IPs flotantes.
- **DHCP Agent**: asigna direcciones IP dinámicas a las instancias en redes privadas.
- **Metadata Agent**: proporciona información de configuración (cloud-init) a las instancias durante el arranque.
- **Agentes de red (OVS/Linux Bridge/OVN)**: implementan la conectividad L2 (bridges, VLANs, VXLAN, GRE) entre instancias y redes externas.

Este nodo actúa como **gateway** para las instancias que necesitan acceso a redes externas (internet o provider networks).

### **Compute (compute01)**

El nodo de cómputo es donde **se ejecutan las instancias** (máquinas virtuales de usuarios):

- **Nova Compute**: servicio que gestiona el hipervisor (KVM en este caso) y ejecuta las instancias solicitadas por los usuarios.
- **Hypervisor (KVM/libvirt)**: tecnología de virtualización que crea y gestiona las VMs a nivel de hardware.
- **Neutron agents** (L2 local): conectan las interfaces de red de las instancias a las redes virtuales definidas en Neutron.

El compute es el **corazón del cómputo** en OpenStack: cuantos más nodos compute tengas, más capacidad de procesamiento tendrá tu nube.

### **Storage (storage01)**

El nodo de almacenamiento proporciona **volúmenes persistentes** para las instancias:

- **Cinder Volume**: servicio que crea, elimina y gestiona volúmenes de almacenamiento en bloque (similares a discos duros virtuales) que se pueden asociar a instancias.
- **Backend de almacenamiento**: puede ser LVM (local), Ceph RBD, iSCSI, NFS, etc. En este laboratorio usaremos un backend simple (LVM o dummy) para demostración.

Los volúmenes de Cinder son **independientes del ciclo de vida de las instancias**: si eliminas una instancia, el volumen puede conservarse y reutilizarse.

---

## Repositorio del proyecto

El código fuente y los archivos de configuración utilizados en esta serie se encuentran disponibles en el siguiente repositorio:

🔗 [https://github.com/javierasping/openstack-vagrant-ansible](https://github.com/javierasping/openstack-vagrant-ansible)

Allí encontrarás los **Vagrantfiles**, **archivos de red libvirt**, **claves SSH** y **scripts auxiliares** empleados durante todo el proceso.

---