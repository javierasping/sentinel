---
title: "Types of Hypervisors"
date: 2025-10-13T10:00:00+00:00
description: Learn what a hypervisor is, its types, differences, and practical usage examples in Linux and Windows environments.
tags: [Virtualization,Linux,KVM,VM,Hypervisor]
hero: images/virtualizacion-kvm-linux/introduccion-kvm/tipos-hipervisores.jpg
---

# Types of Hypervisors

## What is a hypervisor?

A **hypervisor**, also known as a **Virtual Machine Monitor (VMM)**, is a software virtualization layer that allows you to create and run multiple virtual machines (VMs) on a single server, as well as run different operating systems in isolation.  

The physical server running the hypervisor is called the **host machine**, while each individual VM is called a **guest machine**.

The term "hypervisor" was coined in the 1970s based on the concept of a **supervisor** in an operating system kernel. By adding the prefix "hyper-", it is considered the supervisor of the supervisors.  

Hypervisors separate the resources of a VM from the physical hardware and allocate them appropriately, facilitating cloud migration and optimizing costs, accessibility, and scalability.

## Benefits of hypervisors

Using hypervisors provides numerous advantages:

- **Efficiency:** allows more efficient use of physical servers, reducing costs.  
- **Flexibility:** VM resources are abstracted from hardware, facilitating portability and workload distribution.  
- **Cloud scalability:** supports multiple VMs on bare-metal servers or multi-tenant environments.  
- **Security and isolation:** enhances security by separating virtual environments from the host system.

## Types of hypervisors

According to Gerald J. Popek and Robert P. Goldberg, there are **two main types of hypervisors**: type 1 and type 2. Although the distinction is not always completely clear, it is useful for understanding their functionality and use.

### Type 1 Hypervisors (bare-metal)

**Type 1 hypervisors**, also called **bare-metal** or **native hypervisors**, run directly on the host hardware and manage guest operating systems without the need for an intermediate OS.  

- **Functionality:** interact directly with hardware, assigning resources to VMs and sharing them as needed.  
- **Typical use:** data centers, web servers, and high-performance enterprise computing environments.  
- **Advantages:** higher performance, efficiency, and isolation; less vulnerable to attacks because they are separated from the host OS.

#### Examples of Type 1 Hypervisors

- **KVM (Kernel-based Virtual Machine):** integrated into the Linux kernel, supports full virtualization and containers.  
- **VMware ESXi:** enterprise bare-metal hypervisor, part of VMware vSphere.  
- **Microsoft Hyper-V:** hypervisor integrated into Windows Server.  
- **Proxmox VE:** Debian-based open-source virtualization platform, supports LXC and KVM.  
- **XEN:** open-source hypervisor originally developed at Cambridge University, maintained by the Linux Foundation.  
- **Citrix Hypervisor:** based on XEN, designed for enterprise environments.  
- **Red Hat Virtualization (RHV):** KVM-based, enterprise-focused platform.  
- **OpenStack:** open-source cloud platform that uses type 1 hypervisors for deploying VMs in public or private clouds.

### Type 2 Hypervisors (hosted)

**Type 2 hypervisors**, also called **hosted hypervisors**, run on top of a conventional operating system as an application. They abstract guest OSes from the host OS.  

- **Functionality:** request resources from the host OS to run VMs.  
- **Typical use:** desktop environments, testing, development, or individuals who need to run multiple OSes simultaneously.  
- **Advantages:** easy to install and manage, no advanced system knowledge required.  
- **Limitations:** lower performance and isolation compared to type 1 hypervisors.

#### Examples of Type 2 Hypervisors

- **VirtualBox:** open-source hypervisor for Windows, Linux, and macOS.  
- **QEMU:** open-source emulator and virtualizer.  
- **VMware Workstation Player and VMware Fusion:** commercial hypervisors for PCs and Macs.  
- **Parallels Desktop:** allows running Windows on macOS without rebooting.

## Key Differences Between Type 1 and Type 2 Hypervisors

| Feature | Type 1 Hypervisor | Type 2 Hypervisor |
|---------|-----------------|-----------------|
| Also known as | Bare-metal | Hosted |
| Runs on | Physical host hardware | Host operating system |
| Suitable for | Heavy workloads, servers | Desktop, development, and testing |
| Can assign dedicated resources? | Yes | No |
| Knowledge required | System administrator level | Basic user |
| Examples | VMware ESXi, Hyper-V, KVM | VirtualBox, VMware Workstation, Parallels Desktop |
| Performance | High | Medium-low |
| Isolation | High | Medium |

## Conclusion

Hypervisors are the backbone of modern virtualization, enabling multiple virtual machines to run efficiently and securely. Choosing between a type 1 or type 2 hypervisor depends on the **usage environment**, **available resources**, and **performance and security goals**.

In enterprise and cloud environments, type 1 hypervisors are preferred for their high performance and isolation. For development, testing, or personal use, type 2 hypervisors are ideal due to their ease of use and flexibility.