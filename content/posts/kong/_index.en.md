---
title: "Complete Guide to Kong Gateway"
date: 2026-07-02T15:00:00+00:00
description: "Didactic series on the installation, configuration, and professional deployment of Kong Gateway in Docker and Kubernetes environments."
tags: [Kong, API Gateway, DevOps, Kubernetes, Docker]
hero: images/kong/index/hero.png
---

Welcome to the complete guide to **Kong Gateway**. In this series of articles, we will explore from the fundamental concepts to the deployment of a hybrid architecture in production environments.

Kong Gateway is an essential tool for any modern microservices architecture, allowing the centralization of security, traffic, and observability of your APIs.

## Learning Path

The series is structured to lead you by the hand, from basic theory to advanced technical implementation.

### 1. Fundamentals and Architecture
In this section, we lay the theoretical foundations necessary to understand the internal workings of the Gateway.
- [Introduction to Kong Gateway](/posts/kong/01-introduccion-kong-gateway): What it is and why it is fundamental in cloud-native architectures.
- [Architecture and Core Components](/posts/kong/02-componentes-core-kong): The role of the Gateway, Kong Manager, and PostgreSQL.
- [Deployment Topologies](/posts/kong/03-topologias-despliegue-kong): Comparison between Traditional, DB-less, Hybrid, and Konnect models.

### 2. Planning and Installation
We move to the practical phase, preparing the infrastructure and executing the installation.
- [Planning Guide](/posts/kong/04-consideraciones-instalacion-kong): Sizing, ports, DNS, and security.
- [Configuration Management](/posts/kong/05-configuracion-kong-gateway): Use of `.conf` files, environment variables, and API.
- [Installation with Docker (Hybrid Mode)](/posts/kong/06-instalacion-docker-hibrido): Practical lab with Docker Compose and mTLS.
- [Enterprise License Management](/posts/kong/07-gestion-licencias-enterprise): How to apply and validate licenses in professional environments.
- [Installation on Kubernetes (Hybrid Mode)](/posts/kong/08-instalacion-kubernetes-hibrido): Advanced deployment using KinD and Helm Charts.

### 3. Configuration and Validation
Finally, we put the traffic into motion and verify that everything is working correctly.
- [First Steps: Services and Routes](/posts/kong/09-servicios-y-rutas-basicos): Routing logic and backend configuration.
- [Gateway Verification and Testing](/posts/kong/10-verificacion-y-pruebas-gateway): Testing methodologies and final quality checklist.

---

*This series has been designed to provide a progressive and didactic path, ensuring that each concept is clear before moving to the next technical step.*
