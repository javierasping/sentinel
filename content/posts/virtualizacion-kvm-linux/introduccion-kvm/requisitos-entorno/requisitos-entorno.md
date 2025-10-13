---
title: "Requisitos y preparación del entorno para KVM"
date: 2025-10-13T10:00:00+00:00
description: Conoce los requisitos de hardware y software necesarios para preparar un entorno Linux listo para virtualización con KVM.
tags: [Virtualizacion,Linux,KVM,VM,Hypervisor]
hero: images/virtualizacion-kvm-linux/introduccion-kvm/requisitos-entorno.jpg
---

# Requisitos y preparación del entorno para KVM

Para poder ejecutar máquinas virtuales con **KVM** es fundamental que el host Linux cumpla ciertos **requisitos de hardware y software**. A continuación se detallan los aspectos más importantes a considerar antes de iniciar la virtualización.


1. **CPU con soporte de virtualización**
   - Intel: VT-x  
   - AMD: AMD-V  
   - Debe estar habilitada en la BIOS/UEFI.  
   - Desde Linux se puede verificar con:
     ```bash
     grep --color -Ew 'svm|vmx|lm' /proc/cpuinfo
     ```
     - `vmx` → CPU Intel con VT-x  
     - `svm` → CPU AMD con AMD-V  
     - `lm` → Soporte de 64 bits

2. **Memoria RAM**
   - Dependerá del número de VMs y la carga de trabajo.  
   - Cada VM requiere memoria dedicada; para entornos de prueba se recomiendan al menos 8 GB.

3. **Almacenamiento**
   - Suficiente espacio para imágenes de VMs y snapshots.  

4. **Red**
   - Adaptador de red compatible con Linux para crear puentes y permitir conectividad de las VMs.
