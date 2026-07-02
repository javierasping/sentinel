---
title: "Architecture and Core Components of Kong Gateway"
date: 2026-07-02T14:05:00+00:00
description: "Analysis of the fundamental pillars of Kong: the Gateway, the Kong Manager, and the PostgreSQL database."
tags: [Kong, Architecture, PostgreSQL, Kong Manager]
hero: images/kong/02-componentes-core/hero.png
---

To understand how Kong Gateway works, it is necessary to break down its architecture into the logical components that enable its operation. Although some of these components may reside in the same binary, they perform very different functions.

## The three pillars of Kong's infrastructure

Kong's basic infrastructure is supported by three main components: the Kong Gateway, the Kong Manager and, in most deployments, a PostgreSQL database.

### 1. Kong Gateway (The Core)

It is the heart of the system. It is the component responsible for receiving all client requests, applying routing rules, and executing configured plugins before redirecting the request to the backend service (upstream).

Its goal is to be extremely efficient in resource consumption and offer minimum latency, as every API call must pass through it.

### 2. Kong Manager (The Interface)

While the Gateway handles traffic, the **Kong Manager** is the management tool. It is a browser-based user interface that allows for the visual monitoring and administration of the Gateway.

Through the Manager, administrators can create services, define routes, and configure plugins without needing to interact directly with the administration API via terminal commands.

### 3. Database (PostgreSQL)

By default, Kong uses **PostgreSQL** as its storage engine. The database is where all configured entities are stored, such as:

- **Services:** Backend definitions.
- **Routes:** Access rules to those services.
- **Plugins:** Security configurations, rate limiting, etc.
- **Consumers:** Information about who accesses the API.

> **Note:** It is important to mention that Kong also supports a **DB-less** mode (without a database), where the configuration is managed declaratively via a YAML file, loading everything into memory to maximize speed.

## Component Summary

| Component | Main Function | Type |
| :--- | :--- | :--- |
| **Kong Gateway** | Traffic brokering and plugin execution | Data Plane |
| **Kong Manager** | Visual management and monitoring | Control Plane (UI) |
| **PostgreSQL** | Persistence storage of the configuration | Storage |

---

**Previous article:** [Introduction to Kong Gateway](/posts/kong/01-introduccion-kong-gateway)  
**Next article:** [Kong Deployment Topologies](/posts/kong/03-topologias-despliegue-kong)
