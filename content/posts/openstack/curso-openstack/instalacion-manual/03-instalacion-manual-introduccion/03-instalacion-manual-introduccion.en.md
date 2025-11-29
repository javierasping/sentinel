---
title: "03 - Manual OpenStack installation guide with Vagrant"
date: 2025-11-23T12:00:00+00:00
description: "Learn how to deploy an OpenStack lab step by step using Vagrant and virtual environments."
tags: [openstack,installation,vagrant]
hero: images/openstack/instalacion-manual/guia-instalacion-manual-vagrant.png
weight: 3
---

## Introduction and scope

In this series, I will show you how to manually deploy a minimal OpenStack installation on a lab of virtual machines managed with Vagrant. We'll use Caracal 2024.1, the latest available in Ubuntu's stable repositories. The goal is not to provide a production solution, but to understand the components, key configuration files, and the correct deployment order so that a basic cloud works with Keystone, Glance, Placement, Nova, Neutron, Cinder, and Horizon.

The files I use are available in my [repository](https://github.com/javierasping/openstack-vagrant-ansible#). You can clone it using the following commands, either via SSH or HTTPS:

```bash
git clone git@github.com:javierasping/openstack-vagrant-ansible.git
git clone https://github.com/javierasping/openstack-vagrant-ansible.git
```

Once cloned, everything related to these posts is in the `manual-install` directory.

The posts are meant to be read in order, and I have included commands ready to copy and paste, in case you want to replicate the lab.

## Scenario

For the OpenStack lab, we use Vagrant with the base image bento/ubuntu-24.04, which provides a clean Ubuntu 24.04 ready to install all OpenStack components. We have defined the example domain openstack.javiercd.es to simplify name resolution and the use of FQDN across all services. The management network is called mgmt-net, and each virtual machine receives a static IP on this network.

The lab consists of three nodes, each with its own role.

The controller01 node acts as the controller and hosts OpenStack's main services: Keystone, Glance API, Nova API, Cinder API, and Horizon, with 2 vCPU and 6 GiB of RAM.

The compute01 node is responsible for running instances and network agents, with 2 vCPU and 4 GiB of RAM.

Finally, the storage01 node provides persistent storage via Cinder with an LVM backend, with 1 vCPU, 4 GiB of RAM, and an additional disk for volumes.

For virtualization, we'll use KVM/QEMU and deploy everything on my machine, which runs Ubuntu 25 as the operating system.

Regarding networks, since this is a lab environment, we only configure two per machine. The public network will be Vagrant's default network (192.168.121.0/24), which allows our machines to access the Internet, and a private network with static IPs assigned in the Vagrantfile will simulate our management network (10.0.0.0/24).

If you like, you can freely modify the resources assigned to each node, change the domains used, or adjust IPs as needed. Feel free to adapt it to your liking if you are going to replicate the lab.

## Sources

To carry out this lab, I gathered information from several sources. To keep them centralized, I list them here:

- OpenStack Install Guide — Environment: SQL/Database on Ubuntu
- curso_openstack_ies — José Domingo Muñoz Rodríguez
- OpenStack Install Guide — OpenStack Services (summary)
- Keystone — Installation (2024.1 Caracal)
- Glance — Installation (2024.1 Caracal)
- Placement — Installation (2024.1 Caracal)
- Nova — Installation (2024.1 Caracal)
- Neutron — Installation (2024.1 Caracal)
- Cinder — Installation (2024.1 Caracal)
- Horizon — Installation (2024.1 Caracal)
