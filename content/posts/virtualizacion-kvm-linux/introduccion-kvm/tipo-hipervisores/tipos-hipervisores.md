---
title: "Tipos de hipervisores"
date: 2025-10-13T10:00:00+00:00
description: Aprende qué es un hipervisor, sus tipos, diferencias y ejemplos prácticos de uso en entornos Linux y Windows.
tags: [Virtualizacion,Linux,KVM,VM,Hypervisor]
hero: images/virtualizacion-kvm-linux/introduccion-kvm/tipos-hipervisores.jpg
---

# Tipos de hipervisores

## ¿Qué es un hipervisor?

Un **hipervisor**, también conocido como **monitor de máquinas virtuales** (VMM, del inglés Virtual Machine Monitor), es una capa de virtualización de software que permite crear y ejecutar múltiples máquinas virtuales (VM) dentro de un único servidor, así como ejecutar diferentes sistemas operativos de forma aislada.  

El servidor físico donde se ejecuta el hipervisor se llama **host machine**, mientras que cada VM individual se denomina **guest machine**.

El término “hipervisor” se acuñó en los años 70 a partir del concepto de **supervisor** del kernel de un sistema operativo. Al usar el prefijo “hiper-”, se considera el supervisor de los supervisores.  

Los hipervisores separan los recursos de la VM del hardware físico y los distribuyen adecuadamente, facilitando la migración a la nube y optimizando costos, accesibilidad y escalabilidad.

## Beneficios de los hipervisores

El uso de hipervisores proporciona numerosas ventajas:

- **Eficiencia:** permite un uso más eficiente de los servidores físicos, reduciendo costos.  
- **Flexibilidad:** los recursos de la VM se abstraen del hardware, lo que facilita la portabilidad y distribución de cargas de trabajo.  
- **Escalabilidad en la nube:** soporta múltiples VMs en servidores bare-metal o entornos multi-inquilino.  
- **Seguridad y aislamiento:** mejora la seguridad al separar los entornos virtuales del sistema host.

## Tipos de hipervisores

Según Gerald J. Popek y Robert P. Goldberg, existen **dos tipos principales de hipervisores**: tipo 1 y tipo 2. Aunque la línea divisoria entre ellos puede no ser siempre clara, la distinción es útil para entender su funcionamiento y uso.

### Hipervisores de tipo 1 (bare-metal)

Los hipervisores de **tipo 1**, también llamados **bare-metal** o **nativos**, se ejecutan directamente sobre el hardware del host y gestionan los sistemas operativos invitados sin necesidad de un sistema operativo intermediario.  

- **Funcionamiento:** interactúan directamente con el hardware, asignando recursos a las VMs y compartiéndolos según sea necesario.  
- **Uso típico:** centros de datos, servidores web y entornos de computación empresarial de alto rendimiento.  
- **Ventajas:** mayor rendimiento, eficiencia y aislamiento; menos propensos a ataques porque están separados del sistema operativo host.

#### Ejemplos de hipervisores de tipo 1

- **KVM (Kernel-based Virtual Machine):** integrado en el kernel de Linux, soporta virtualización completa y contenedores.  
- **VMware ESXi:** hipervisor empresarial bare-metal, parte de VMware vSphere.  
- **Microsoft Hyper-V:** hipervisor de Microsoft, integrado en Windows Server.  
- **Proxmox VE:** plataforma de virtualización de código abierto basada en Debian, soporta LXC y KVM.  
- **XEN:** hipervisor de código abierto desarrollado por la Universidad de Cambridge, mantenido por Linux Foundation.  
- **Citrix Hypervisor:** basado en XEN, orientado a entornos empresariales.  
- **Red Hat Virtualization (RHV):** basado en KVM, orientado a entornos corporativos.  
- **OpenStack:** plataforma cloud de código abierto que utiliza hipervisores tipo 1 para desplegar VMs en cloud público o privado.

### Hipervisores de tipo 2 (alojados)

Los hipervisores de **tipo 2**, también llamados **alojados**, se ejecutan sobre un sistema operativo convencional, como una aplicación. Abstraen los sistemas operativos invitados del host.  

- **Funcionamiento:** negocian recursos con el sistema operativo host para ejecutar las VMs.  
- **Uso típico:** entornos de escritorio, pruebas, desarrollo o usuarios individuales que necesitan ejecutar varios sistemas operativos simultáneamente.  
- **Ventajas:** fácil de instalar y administrar, no requiere conocimientos avanzados de sistemas.  
- **Limitaciones:** menor rendimiento y aislamiento comparado con hipervisores tipo 1.

#### Ejemplos de hipervisores de tipo 2

- **VirtualBox:** hipervisor de código abierto para Windows, Linux y macOS.  
- **QEMU:** emulador y virtualizador de código abierto.  
- **VMware Workstation Player y VMware Fusion:** hipervisores comerciales para PCs y Mac.  
- **Parallels Desktop:** permite ejecutar Windows sobre macOS sin reiniciar.

## Diferencias clave entre hipervisores tipo 1 y tipo 2

| Característica | Hipervisor Tipo 1 | Hipervisor Tipo 2 |
|----------------|-----------------|-----------------|
| También conocido como | Bare-metal | Alojado |
| Se ejecuta en | Hardware físico del host | Sistema operativo host |
| Adecuado para | Cargas de trabajo pesadas o servidores | Escritorio, desarrollo y pruebas |
| Negocia recursos dedicados | Sí | No |
| Requisitos de conocimiento | Nivel administrador de sistemas | Usuario básico |
| Ejemplos | VMware ESXi, Hyper-V, KVM | VirtualBox, VMware Workstation, Parallels Desktop |
| Rendimiento | Alto | Medio-bajo |
| Aislamiento | Alto | Medio |

## Conclusión

Los hipervisores son el corazón de la virtualización moderna, permitiendo ejecutar múltiples máquinas virtuales de manera eficiente y segura. Elegir entre un hipervisor tipo 1 o tipo 2 depende del **entorno de uso**, los **recursos disponibles** y los **objetivos de rendimiento y seguridad**.

En entornos empresariales y de cloud, se prefieren los hipervisores tipo 1 por su alto rendimiento y aislamiento. Para desarrollo, pruebas o uso personal, los hipervisores tipo 2 son ideales por su facilidad de uso y flexibilidad.

---