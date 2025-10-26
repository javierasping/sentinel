---
title: "Conceptos básicos de virtualización en Linux"
date: 2025-10-13T10:00:00+00:00
description: Aprende de forma sencilla qué es la virtualización, cómo funcionan las máquinas virtuales y para qué sirve.
tags: [Virtualizacion,Linux,KVM,VM]
hero: images/virtualizacion-kvm-linux/introduccion/conceptos-basicos.png
weight: 1
---

# Conceptos básicos de virtualización en Linux

Si alguna vez te has preguntado cómo varias "máquinas" pueden funcionar dentro de una sola máquina física, la respuesta está en la **virtualización**. Vamos a explicarlo de forma sencilla.

## ¿Qué es la virtualización?

La virtualización es una tecnología que permite crear **versiones digitales de máquinas** dentro de una máquina real. Cada una de estas "máquinas virtuales" se llama **máquina virtual** (VM) y puede ejecutar su propio sistema operativo y aplicaciones, como si fuera un equipo independiente.  

Piensa en tu máquina como un edificio, y las máquinas virtuales como apartamentos dentro de ese edificio. Cada apartamento funciona de forma independiente, aunque todos comparten la misma estructura y servicios (electricidad, agua, internet… o en nuestro caso, CPU, memoria y disco).

## Funcionamiento de las máquinas virtuales

El equipo físico donde se ejecutan las VMs se llama **máquina host** o simplemente **host**. Las máquinas virtuales que utilizan los recursos del host se llaman **guests**.  

El software que permite crear y gestionar las VMs se llama **hipervisor**. Su función es aislar y repartir los recursos del host (CPU, memoria, almacenamiento) entre las distintas VMs, de manera que cada una tenga lo que necesita sin afectar a las demás.  

Cada sistema operativo dentro de una VM funciona igual que si estuviera en una máquina física, por lo que la experiencia para el usuario es prácticamente idéntica. Además, las máquinas virtuales pueden configurarse mediante archivos de datos, lo que permite reproducirlas fácilmente en distintos equipos.

Si una VM necesita más recursos mientras se ejecuta, el hipervisor se encarga de gestionar y asignar esos recursos dinámicamente. Esto hace que el hardware físico se aproveche de forma más eficiente.

En Linux, el hipervisor integrado se llama **KVM** (Kernel-based Virtual Machine). Otras opciones incluyen **Xen** (open source) y **Microsoft Hyper-V**.

### Tipos de hipervisores

- **Tipo 1 (bare metal):** se instalan directamente en el hardware. Son muy eficientes y se usan en servidores de alto rendimiento. KVM es un ejemplo de hipervisor tipo 1.  
- **Tipo 2 (alojado):** se instalan sobre un sistema operativo ya existente. Son más fáciles de usar para pruebas o entornos de escritorio. VMware Workstation y VirtualBox son ejemplos de hipervisores tipo 2.

## ¿Por qué es útil?

- **Ahorro de recursos:** puedes ejecutar varias VMs en un solo equipo físico, evitando comprar y mantener muchas máquinas.  
- **Flexibilidad:** puedes usar distintos sistemas operativos al mismo tiempo, sin reiniciar.  
- **Pruebas y experimentos seguros:** puedes probar software o configuraciones sin afectar tu máquina principal.  
- **Recuperación rápida:** si algo falla en una VM, puedes restaurarla sin tocar el hardware.

## Tipos de virtualización

La virtualización no solo se aplica a máquinas completas. Existen varias categorías:

- **Virtualización de servidores:** dividir un servidor físico en varios servidores virtuales.  
- **Virtualización de almacenamiento:** combinar varios discos y sistemas de almacenamiento en una sola unidad virtual.  
- **Virtualización de red:** administrar redes y sus componentes de forma virtual.  
- **Virtualización de datos:** combinar datos de distintos orígenes y hacerlos accesibles de manera uniforme.  
- **Virtualización de aplicaciones:** ejecutar aplicaciones en sistemas distintos a los que fueron diseñadas.  
- **Virtualización de escritorios:** ofrecer escritorios virtuales accesibles desde cualquier lugar.

## Diferencia con contenedores

Las máquinas virtuales incluyen **un sistema operativo completo**, mientras que los contenedores solo incluyen la aplicación y sus dependencias. Por eso, las VMs son más pesadas pero totalmente independientes, y los contenedores son más ligeros y rápidos de iniciar.

## Relación con la nube

La virtualización es la base de la computación en la nube. Gracias a ella, los proveedores como AWS o Google Cloud pueden ofrecer servidores, almacenamiento y redes bajo demanda, accesibles desde cualquier lugar.

---