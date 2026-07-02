---
title: "Kong Gateway Deployment Topologies"
date: 2026-07-02T14:10:00+00:00
description: "Comparison of Kong deployment models: Traditional, DB-less, Hybrid, and Kong Connect."
tags: [Kong, Architecture, Deployment, Topologies]
hero: images/kong/03-topologias/hero.png
---

Depending on the needs for scalability, security, and infrastructure management, Kong allows deployment under different models. Choosing the right topology is fundamental to optimizing the performance and maintainability of the system.

## Kong Deployment Models

Below, we analyze the five main topologies supported by Kong.

### 1. Traditional Deployment

In this model, each Kong Gateway node is connected directly to a PostgreSQL database. All configuration details are stored and retrieved from there.

- **Characteristics:** Supports single-node or multi-node clusters.
- **Advantage:** All plugins have direct access to the database to read and write entities.
- **Ideal Use:** Environments requiring dynamic and persistent configuration management.

### 2. DB-less Deployment

Kong can run without depending on an external database, using only in-memory storage. The configuration is defined **declaratively** in a file (usually YAML).

- **Limitations:** Plugins that require a central database to coordinate states (such as some global rate limiting counters) are not fully compatible.
- **Ideal Use:** CI/CD environments, ephemeral deployments, or where maximum startup speed and simplicity are sought.

### 3. Hybrid Deployment (Hybrid Mode)

It is one of Kong's most powerful architectures. Here, nodes are divided into two clearly distinct roles:

- **Control Plane (CP):** The brain. This is where configuration is managed, the Admin API resides, and the Kong Manager is hosted.
- **Data Plane (DP):** The nodes that serve actual traffic. They have no database. Instead, they maintain a real-time connection with the Control Plane to receive configuration updates.

This model allows scaling Data Planes horizontally in a massive way without saturating the central database.

### 4. Kong Connect

Konnect is Kong's SaaS platform. In this scenario, Kong manages the **Control Plane** in its own cloud, while you deploy the **Data Planes** wherever you prefer (on-premise, own cloud, or fully managed by Kong).

### 5. Kong Ingress Controller (KIC)

Specific to Kubernetes, KIC allows running Kong as an Ingress. The controller listens to Kubernetes manifests (CRDs) and automatically translates them into Kong configurations, applying them to the Gateway.

---

## Topology Comparison Table

| Model | Database | Configuration Management | DP Scalability |
| :--- | :--- | :--- | :--- |
| **Traditional** | Yes (PostgreSQL) | Dynamic (API/UI) | Medium |
| **DB-less** | No | Declarative (File) | High |
| **Hybrid** | Yes (CP only) | Centralized in CP | Very High |
| **Connect** | Managed (SaaS) | Centralized in SaaS | Very High |
| **KIC** | Variable | Via Kubernetes CRDs | High |

---

**Previous article:** [Core Components of Kong Gateway](/posts/kong/02-componentes-core-kong)  
**Next article:** [Installation Planning Guide](/posts/kong/04-consideraciones-instalacion-kong)
