---
title: "Complete Guide to Kong Gateway"
date: 2026-07-02T15:00:00+00:00
description: "Didactic series on the installation, configuration, and professional deployment of Kong Gateway in Docker and Kubernetes environments."
tags: [Kong, API Gateway, DevOps, Kubernetes, Docker]
hero: images/kong/index/hero.png
menu:
  sidebar:
    name: "Kong Gateway"
    identifier: Kong
    weight: 200
---

Welcome to the complete guide to **Kong Gateway**. In this series of articles, we will explore from the fundamental concepts to the deployment of a hybrid architecture in production environments.

Kong Gateway is an essential tool for any modern microservices architecture, allowing the centralization of security, traffic, and observability of your APIs.

## Learning Path

The series is structured to lead you by the hand, from basic theory to advanced technical implementation.

### 1. Fundamentals and Architecture
In this section, we lay the theoretical foundations necessary to understand the internal workings of the Gateway.
- [Introduction, architecture and planning](/posts/kong/01-introduccion-kong-gateway): What Kong Gateway is, how it is structured, and what to review before installing it.

### 2. Installations and Deployments
We move to the practical phase, preparing the base configuration and executing each installation mode.
- [Installation with Docker (Hybrid Mode)](/posts/kong/02-instalacion-docker-hibrido): Practical lab with Docker Compose and mTLS.
- [Installation in Traditional Mode](/posts/kong/03-instalacion-tradicional): Database-backed deployment with PostgreSQL, the Admin API, and Kong Manager.
- [Installation in DB-less Mode](/posts/kong/04-instalacion-db-less): Declarative deployment without a database.
- [Installation in Konnect](/posts/kong/05-instalacion-kong-connect): SaaS-managed control plane and connected data planes.
- [Installing Kong Ingress Controller (KIC)](/posts/kong/06-instalacion-kic): Native Kubernetes integration through Helm and CRDs.
- [Installation on Kubernetes (Hybrid Mode)](/posts/kong/07-instalacion-kubernetes-hibrido): Advanced deployment using KinD and Helm Charts.
- [First Steps: Services and Routes](/posts/kong/08-servicios-y-rutas-basicos): Routing logic and backend configuration.
- [Gateway Verification and Testing](/posts/kong/09-verificacion-y-pruebas-gateway): Testing methodologies and final quality checklist.

---

*This series has been designed to provide a progressive and didactic path, ensuring that each concept is clear before moving to the next technical step.*
