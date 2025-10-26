---
title: "Tipos de redes en KVM (NAT, aisladas y puenteadas)"
date: 2025-10-18T09:00:00+00:00
description: "Descripción teórica de los tipos de redes disponibles en KVM/libvirt: NAT, aisladas, muy aisladas, bridge externo y macvtap; diferencias, conectividad y casos de uso."
tags: [KVM,Virtualizacion,Libvirt,Redes,Linux]
hero: images/virtualizacion-kvm-linux/redes/tipos-de-redes.png
weight: 1
---

# Tipos de redes en KVM

En KVM, la virtualización de redes se gestiona principalmente mediante **libvirt**, que nos permite crear y administrar diferentes tipos de redes virtuales a las que se conectan nuestras máquinas virtuales. Entender los tipos de redes disponibles es clave para configurar adecuadamente la conectividad de los invitados y la interacción con el host.

Existen dos grandes categorías de redes en KVM:

* **Redes Virtuales Privadas**: Redes internas aisladas del exterior, gestionadas mediante bridges virtuales creados por libvirt.
* **Redes Puente (Bridged)**: Redes que conectan directamente las máquinas virtuales a la red física del host.

---

## Redes Virtuales Privadas

Estas redes se crean dentro del host y ofrecen un entorno controlado para las máquinas virtuales. Se clasifican en tres tipos principales:

### 1. NAT (Network Address Translation)

Es la red privada más común y suele utilizarse en la red `default` de libvirt. Sus características son:

* Las máquinas virtuales tienen direcciones privadas y acceden al exterior a través del host mediante NAT.
* Se crea un **bridge virtual** (`virbr0` en la red `default`) al que se conectan las máquinas virtuales y el host.
* El host funciona como **router y servidor DHCP** para asignar direcciones dinámicas.
* El host también puede proporcionar **servidor DNS** a los invitados.

Casos de uso: laboratorios, entornos de desarrollo y pruebas donde las VMs necesiten salir a Internet sin ser accesibles directamente desde la red física.

### 2. Redes aisladas (Isolated)

Son redes privadas donde las máquinas virtuales no tienen acceso al exterior:

* Se conectan a un bridge virtual, pero no hay **NAT** ni enrutamiento hacia el exterior.
* El host puede (opcionalmente) tener una IP en ese bridge para comunicarse con las VMs y, si se desea, ofrecer **DHCP/DNS** internos.

Casos de uso: segmentación interna de servicios, entornos de pruebas con control total del direccionamiento y sin salida al exterior.


### 3. Redes muy aisladas (Very Isolated)

En este caso, las máquinas virtuales están completamente separadas del host:

* No hay servicios L3 del host (sin IP del host en el bridge) ni **DHCP/DNS** proporcionados por libvirt.
* La configuración de red normalmente se hace de forma estática en cada VM o mediante un servicio interno desplegado por el propio usuario.

Notas: aunque el host no tenga IP en el bridge (sin conectividad L3), las VMs siguen compartiendo el mismo segmento L2 entre ellas.


---

## Redes Puente (Bridged)

Estas redes permiten que las máquinas virtuales se conecten directamente a la red física del host. Se pueden implementar de dos formas:

### 1. Bridge externo

Se crea un **bridge virtual** (`br0`) al que se conecta la interfaz física del host y las máquinas virtuales:

* Las VM se integran en la misma red que el host.
* Pueden obtener direcciones IP del DHCP del router de la red física.
* Ideal para entornos donde las VM deben ser accesibles desde otros dispositivos de la red.

### 2. Macvtap

Permite conectar las VM directamente a la interfaz física del host sin pasar por un bridge:

* Las VM reciben direcciones IP de la red física.
* No existe comunicación directa entre host y VM por defecto (limitación conocida de macvtap en la mayoría de modos).
* Útil para entornos donde se requiere un acceso directo a la red física sin configuración adicional de bridges.

Nota: en ciertos escenarios avanzados se puede habilitar comunicación host↔VM creando una interfaz auxiliar (macvlan) en el host; no obstante, no es el comportamiento por defecto.

---

## Tabla resumen

| Tipo de red           | Conectividad host         | Conectividad exterior     | DHCP disponible                 |
|-----------------------|---------------------------|---------------------------|---------------------------------|
| NAT                   | Sí                        | Sí (vía NAT del host)     | Sí                              |
| Aislada               | Sí (si el host tiene IP)  | No                        | Opcional                        |
| Muy aislada           | No (sin IP del host)      | No                        | No                              |
| Bridge externo        | Sí                        | Sí (directa)              | Sí (DHCP de red física)         |
| Macvtap               | No directa (limitada)     | Sí (directa)              | Sí (DHCP de red física)         |


---

## Referencias

- [curso_virtualizacion_linux — GitHub](https://github.com/josedom24/curso_virtualizacion_linux)
- [Libvirt: Virtual networking overview](https://libvirt.org/network.html)
- [Libvirt: Network XML format](https://libvirt.org/formatnetwork.html)
- [Libvirt: Domain XML (interfaces, tipos de NIC)](https://libvirt.org/formatdomain.html)
- [Libvirt Wiki: Guest networking (macvtap, bridge)](https://wiki.libvirt.org/page/Guest_Networking)