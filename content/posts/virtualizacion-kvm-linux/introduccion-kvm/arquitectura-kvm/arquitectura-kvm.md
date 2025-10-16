---
title: "Arquitectura y funcionamiento de KVM"
date: 2025-10-13T10:00:00+00:00
description: Aprende qué es KVM, cómo funciona, su arquitectura y cómo se utiliza para virtualizar sistemas en Linux.
tags: [Virtualizacion,Linux,KVM,VM,Hypervisor]
hero: images/virtualizacion-kvm-linux/introduccion-kvm/arquitectura-kvm.jpg
---

# Arquitectura y funcionamiento de KVM

## ¿Qué es KVM?

KVM, o **Kernel-based Virtual Machine**, es una característica de software que se puede instalar en sistemas Linux para crear máquinas virtuales (VMs). Una máquina virtual actúa como un equipo independiente dentro de otra máquina física, compartiendo recursos como CPU, memoria y ancho de banda de red con el sistema host.  

KVM es un componente del kernel de Linux que proporciona soporte nativo para la virtualización desde 2007, convirtiendo cualquier máquina Linux en un **hipervisor bare-metal**.

## Importancia de KVM

KVM permite a los desarrolladores y administradores de sistemas:

- Escalar la infraestructura de cómputo sin necesidad de nuevo hardware.  
- Automatizar el aprovisionamiento de entornos virtuales.  
- Implementar rápidamente un gran número de VMs, especialmente en entornos de nube.

Las principales ventajas de KVM son:

- **Alto rendimiento:** la virtualización se realiza cerca del hardware, reduciendo la latencia.  
- **Seguridad:** las VMs aprovechan las características de seguridad de Linux, incluyendo SELinux.  
- **Estabilidad:** KVM cuenta con más de una década de desarrollo y soporte de una comunidad activa de código abierto.  
- **Rentabilidad:** es gratuito y de código abierto, sin necesidad de licencias adicionales.  
- **Flexibilidad:** soporta diferentes configuraciones de hardware y aprovisionamiento fino de recursos.

## Cómo funciona KVM

Para ejecutar KVM, se requiere:

- Una CPU que soporte extensiones de virtualización (Intel VT-x o AMD-V).  
- Un kernel de Linux actualizado.  
- Componentes adicionales: módulo del kernel, módulo específico del procesador, emulador y paquetes Linux complementarios.

### Arquitectura de KVM

KVM se basa en **dos componentes principales**:

1. **Módulos del kernel:**  
   - `kvm.ko`, `kvm-intel.ko` y `kvm-amd.ko`.  
   - Proporcionan la infraestructura de virtualización y controladores específicos del procesador.

2. **Espacio de usuario (User space):**  
   - `qemu-system-ARCH` emula dispositivos virtuales y controla las VMs.  
   - Se puede gestionar mediante herramientas de QEMU (`qemu-img`, `qemu-monitor`) o mediante pila libvirt (`virsh`, `virt-manager`, `virt-install`).

En la práctica, el término **KVM** se usa tanto para referirse a la funcionalidad del kernel como al componente de espacio de usuario.

### Funcionamiento de las VMs en KVM

- Las VMs se ejecutan como **procesos Linux normales** en el host.  
- Cada vCPU se implementa como **hilo normal**, gestionado por el planificador de Linux.  
- Las características avanzadas del kernel (NUMA, huge pages) no se heredan automáticamente.  
- El rendimiento de disco y red depende de la configuración del host.  
- El tráfico de red suele pasar por un **puente de software**.  
- La emulación de dispositivos específicos puede generar **sobrecarga adicional**.

## Diferencias entre KVM y VMware ESXi

| Característica | KVM | VMware ESXi |
|----------------|-----|------------|
| Licencia | Código abierto | Comercial |
| Integración | Kernel de Linux | Kernel propio |
| Soporte | Comunidad de código abierto | Soporte profesional |
| Flexibilidad | Alta, aprovisionamiento fino | Alta, pero depende de licencia |
| Entorno | Linux | Linux/Windows |


