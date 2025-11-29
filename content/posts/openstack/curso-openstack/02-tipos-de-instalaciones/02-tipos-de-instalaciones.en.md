---
title: "02 - OpenStack installation and deployment methods"
date: 2025-11-23T12:00:00+00:00
description: "Overview of common ways to install and deploy OpenStack (manual, DevStack, OpenStack‑Ansible, Kolla, TripleO, etc.)."
tags: [openstack,installation]
hero: images/openstack/instalacion-manual/metodos-instalacion-openstack.png
weight: 2
---

Before deploying OpenStack, it's important to know that each release has its own installation and maintenance guide, adapted to its components and features. OpenStack releases are published regularly and receive direct support for roughly 18 months. This means it's best to plan deployments around stable releases with active support, rather than always opting for the latest release, which may contain early-stage issues.

You can find official installation guides for each release in the [OpenStack Install Guide](https://docs.openstack.org/install-guide/) and review all published versions along with their support schedule at [OpenStack Releases](https://releases.openstack.org/).

## Deployment and packaging methods for OpenStack

Each OpenStack release can be deployed in several ways, and there are multiple tools and frameworks that automate this process, making installation, upgrades, and cloud maintenance easier. While manual installation is still possible, most deployments today use lifecycle management frameworks and packaging tools.

### Lifecycle Management Frameworks

These frameworks enable consistent and reproducible OpenStack deployments, whether in containers, on virtual machines, or directly on bare-metal:

- OpenStack‑Ansible: Ansible playbooks that install and configure OpenStack in a modular, automated way.
- Kolla / Kolla‑Ansible: OpenStack services packaged in Docker containers, orchestrated via Ansible. Ideal for production.
- OpenStack‑Helm: Deploy OpenStack on Kubernetes using Helm charts.
- Kayobe: Framework focused on deploying containerized OpenStack on bare‑metal servers.
- OpenStack Charms / Juju: Use Juju charms to deploy OpenStack on containers or physical machines.
- Bifrost: Ansible playbooks for bare‑metal provisioning via Ironic.

### Packaging tools

These tools offer recipes and modules to package and deploy OpenStack consistently, integrating with configuration frameworks:

- LOCI: Lightweight OCI containers for reproducible deployments.
- Puppet‑OpenStack: Puppet modules to configure and deploy OpenStack components in an automated way.
- Other Puppet modules: Nova, Neutron, Cinder, Glance, Keystone, Swift, Heat, Horizon, Ironic, etc. These are actively maintained and cover releases from early versions up to the latest (e.g., 27.0.0 in 2025 for most modules).

### Important notes on versions and deployments

Each OpenStack release keeps these tools updated and compatible with included components.
It's recommended to choose the deployment tool best suited to the environment size and infrastructure type: containers, VMs, or bare‑metal.
Modern tools like Kolla‑Ansible, OpenStack‑Ansible, or OpenStack‑Helm are preferred for production, while frameworks like DevStack remain useful for labs and testing.

For details on versions and deployment tool compatibility, see the official page: [OpenStack Flamingo - Deployment and Packaging Tools](https://releases.openstack.org/flamingo/index.html#deployment-and-packaging-tools).
