---
title: "Basic Virtualization Concepts in Linux"
date: 2025-10-13T10:00:00+00:00
description: Learn in a simple way what virtualization is, how virtual machines work, and why it is useful.
tags: [Virtualization,Linux,KVM,VM]
hero: images/virtualizacion-kvm-linux/introduccion/conceptos-basicos.png
weight: 1
---

# Basic Virtualization Concepts in Linux

If you have ever wondered how multiple "machines" can run inside a single physical machine, the answer is **virtualization**. Let's explain it in a simple way.

## What is virtualization?

Virtualization is a technology that allows you to create **digital versions of machines** inside a real machine. Each of these "virtual machines" is called a **virtual machine** (VM) and can run its own operating system and applications, just like an independent computer.  

Think of your computer as a building, and the virtual machines as apartments within that building. Each apartment operates independently, although all share the same structure and services (electricity, water, internet… or in our case, CPU, memory, and disk).

## How virtual machines work

The physical machine where VMs run is called the **host machine** or simply **host**. The virtual machines using the host’s resources are called **guests**.  

The software that allows you to create and manage VMs is called a **hypervisor**. Its job is to isolate and allocate the host’s resources (CPU, memory, storage) among the different VMs so that each has what it needs without affecting the others.  

Each operating system inside a VM runs just like it would on a physical machine, so the user experience is almost identical. Additionally, virtual machines can be configured with data files, which makes it easy to reproduce them on different computers.

If a VM needs more resources while running, the hypervisor dynamically manages and assigns them. This allows the physical hardware to be used more efficiently.

On Linux, the built-in hypervisor is called **KVM** (Kernel-based Virtual Machine). Other options include **Xen** (open source) and **Microsoft Hyper-V**.

### Types of hypervisors

- **Type 1 (bare metal):** installed directly on the hardware. They are very efficient and used on high-performance servers. KVM is an example of a Type 1 hypervisor.  
- **Type 2 (hosted):** installed on top of an existing operating system. Easier to use for testing or desktop environments. VMware Workstation and VirtualBox are examples of Type 2 hypervisors.

## Why is it useful?

- **Resource saving:** you can run multiple VMs on a single physical machine, avoiding the need to buy and maintain many machines.  
- **Flexibility:** run different operating systems at the same time without rebooting.  
- **Safe testing and experiments:** try software or configurations without affecting your main machine.  
- **Fast recovery:** if something goes wrong in a VM, you can restore it without touching the hardware.

## Types of virtualization

Virtualization is not only for full machines. There are several categories:

- **Server virtualization:** split a physical server into multiple virtual servers.  
- **Storage virtualization:** combine multiple disks and storage systems into a single virtual unit.  
- **Network virtualization:** manage networks and their components virtually.  
- **Data virtualization:** combine data from different sources and make it uniformly accessible.  
- **Application virtualization:** run applications on systems different from those they were designed for.  
- **Desktop virtualization:** provide virtual desktops accessible from anywhere.

## Difference with containers

Virtual machines include **a full operating system**, while containers only include the application and its dependencies. This makes VMs heavier but fully independent, while containers are lighter and start faster.

## Relation to the cloud

Virtualization is the foundation of cloud computing. Thanks to it, providers like AWS or Google Cloud can offer servers, storage, and networks on demand, accessible from anywhere.