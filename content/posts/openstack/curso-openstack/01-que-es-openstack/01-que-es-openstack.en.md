---
title: "01 - What is OpenStack?"
date: 2025-11-23T12:00:00+00:00
description: "A simple explanation of what OpenStack is, its components, and when to use it."
tags: [openstack,introduction]
hero: images/openstack/instalacion-manual/que-es-openstack.png
weight: 1
---

OpenStack is a free and open-source software project that enables you to build and manage private, public, or hybrid clouds, offering full control over infrastructure through open APIs. It is not a product from a single company, but an open ecosystem maintained by a global community under the Apache license. Founded in 2010 by NASA and Rackspace, it has received contributions from organizations such as AT&T, Red Hat, Canonical, Intel, IBM, and Huawei.

Cloud computing consists of accessing applications and data in a decentralized way, without relying on a single physical server. Information is distributed across different locations—often geographically separated—and accessed over the network. This model requires infrastructures that guarantee availability, performance, and security. Data must be protected against unauthorized access and accidental loss, while resources are used efficiently.

OpenStack provides consistent APIs to control compute, networking, and storage, abstracts the complexity of the underlying hardware, and allows users and applications to manage resources autonomously without human approval. Although it runs on Linux and uses hypervisors like KVM or XEN, its true strength lies in interoperability, scalability, and the ability to integrate with other cloud layers such as containers, serverless platforms, or PaaS systems.

## Why use the cloud and OpenStack?

The cloud lets you access compute power, storage, and services without depending on local device hardware. This means you don't need to invest heavily in your own servers, and resources can be adjusted according to real needs, paying only for what you use. This flexible scalability makes the cloud an efficient option for both small startups and large organizations.

OpenStack adds value by offering a free and extensible platform to build private, public, or hybrid clouds. Unlike closed commercial solutions, OpenStack allows organizations to maintain full control of their infrastructure—from managing servers and storage to networking and security. Its open architecture facilitates integration with other cloud layers such as containers, serverless platforms, or PaaS environments, enabling modern applications to make the most of available resources.

In addition, OpenStack incorporates mechanisms that increase security and resilience. Data can be replicated, and resources are isolated across different users or applications, reducing the risks of unauthorized access or accidental loss. All of this makes OpenStack an attractive option for those seeking autonomy, flexibility, and reliability when deploying and managing their own cloud.

## Main OpenStack components

OpenStack is a collection of services that, combined, allow you to build and manage a complete and flexible cloud. At the core of the platform is Nova, the compute service, which manages the execution of virtual machines and abstracts the hardware through virtualization. Nova is compatible with popular hypervisors such as KVM, XEN, and VMware ESXi, allowing organizations to choose the technology that best suits their needs.

User, project, and permission management is handled by Keystone, which acts as the cloud's identity, authentication, and authorization service. Glance manages disk images, functioning as a repository to store, version, and retrieve templates for virtual machine deployment.

Networking in OpenStack is provided by Neutron, which allows you to create virtual networks and subnets, assign IPs, configure VLANs and VPNs, and apply security services such as firewalls and NAT. For block storage, Cinder offers virtual volumes that can be attached to instances, with support for snapshots and integration with different physical backends such as Ceph or GlusterFS. Complementing this, Swift provides distributed object storage, designed for massive replication and high data durability.

For interaction and administration, Horizon provides a web dashboard from which operators and users can manage resources, monitor infrastructure, and launch instances without needing to use the command line.

All these services are designed to work together. Nova uses images from Glance to create instances; Cinder supplies volumes that can be mounted on those machines; Neutron connects nodes to each other and to the outside; Keystone controls access; and Swift serves data in a distributed and reliable way. Horizon provides a complete view of all this, making cloud administration possible from a browser.

In addition to these main services, OpenStack includes many other specialized components to expand functionality, such as:

- Zun: container management.
- Ironic: bare-metal provisioning.
- Cyborg: accelerator and specialized device management.
- Manila: shared file systems.
- Octavia: load balancers.
- Designate: DNS service.
- Heat and Mistral: orchestration and workflows.
- Trove: databases as a service.
- Magnum: container cluster management.
- Barbican: key and secret management.
- Masakari: instance high availability.

These services work in coordination with the main ones, forming a modular and extensible ecosystem that adapts to a wide variety of needs.

See the official documentation for a complete list of all [OpenStack components](https://www.openstack.org/software/project-navigator/openstack-components#openstack-services).

## OpenStack vision

OpenStack is not just a set of cloud services, but a strategic vision of how modern clouds should operate. It is based on principles of:

- Self-service: users and applications manage resources directly through APIs.
- Interoperability: applications are deployed across different clouds without significant changes.
- Hardware abstraction: management of VMs, GPUs, FPGAs, load balancers, and advanced storage.
- Scalability and resilience: resources shared efficiently with high availability and durability.
- Integration with other cloud layers: native support for containers, PaaS, and serverless.

This vision makes OpenStack a modular, flexible, and fully open ecosystem where every service contributes to building autonomous, reliable, and adaptable clouds.
