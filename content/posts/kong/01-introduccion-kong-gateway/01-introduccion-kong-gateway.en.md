---
title: "Introduction to Kong Gateway"
date: 2026-07-26T00:00:00+02:00
description: "A unified guide to what Kong Gateway is, its components, deployment topologies, and the planning work to do before installation."
tags: [Kong, API Gateway, Architecture, Planning, Topologies]
hero: images/kong/introduction.png
weight: 1
---

Kong Gateway is an **API Gateway** built on **NGINX** and developed in **Lua**. It acts as the entry point between API consumers and backend services, playing the role of an advanced **reverse proxy** with powerful capabilities for managing, securing, and observing traffic.

Its purpose goes far beyond forwarding requests. Some of the native capabilities it provides are:

- Authentication and authorization through mechanisms such as API Keys, JWT, Basic Auth, or OIDC.
- Traffic control through rate limiting policies, quotas, and allow lists.
- Request and response transformations without changing the applications.
- Event, metric, and trace logging to improve observability.
- Centralized exposure of multiple services through a single entry point.

Thanks to this approach, APIs can focus exclusively on business logic while Kong Gateway takes care of common concerns such as security, traffic control, observability, and communication handling.

## Why Use an API Manager

When an organization starts to grow, managing APIs one by one stops being practical. An API Manager helps centralize tasks that would otherwise end up duplicated in every service:

- Define shared policies, such as payload size limits or traffic control.
- Protect APIs with authentication and authorization mechanisms.
- Transform headers, routes, or payloads without touching the backend.
- Record usage, metrics, and performance data from a single place.
- Expose APIs in an orderly way to internal or external consumers.

Kong fits that scenario very well because it combines performance, flexibility, and a broad plugin ecosystem.

## Kong Gateway Editions

Kong Gateway is distributed in two main editions:

- **Community Edition (CE)**, which is free and open source.
- **Enterprise Edition (EE)**, the commercial version developed by Kong Inc.

Both share the same core and allow you to publish, protect, and manage APIs through the **Admin API**, which is the official interface for configuring Kong resources. In practice, most automation tools such as **decK**, **Terraform**, or `curl`-based scripts interact with this API.

The main difference is that the Enterprise edition adds extra capabilities aimed at corporate environments, such as exclusive plugins, advanced security features, Konnect integration, commercial support, and other functions that are not part of the Community edition.

## What Is Konga?

**Konga** is a third-party web interface that allows you to administer Kong Gateway instances through the Admin API. Its goal is to make management tasks easier through a graphical interface, avoiding the need to perform every operation from the command line or through HTTP calls.

Although it is useful for labs and test environments, it is important to keep in mind that:

- It does not expose all the capabilities available in the Admin API.
- Its development has not seen significant activity for several years.
- In production environments, it is better to rely on the official Kong ecosystem tools, such as **decK**, **Terraform**, or the Admin API itself.

## Basic Architecture

In a classic Kong deployment, these are the components we usually find:

| Component | Main function | Notes |
| :--- | :--- | :--- |
| **Kong Gateway** | Receives traffic, applies plugins, and routes requests | This is the plane the consumer interacts with |
| **Admin API** | Exposes Kong configuration | Used to create and modify resources |
| **Kong Manager / Konga** | Graphical administration interface | Useful for visual operation |
| **PostgreSQL** | Configuration persistence | Common in database-backed modes |

Kong can also operate without a database, loading a declarative configuration into memory. That option is especially convenient in automated and reproducible deployments.

## Plugins and Scopes

One of the most powerful aspects of Kong Gateway is its **plugin** system. It makes it possible to add capabilities such as authentication, authorization, traffic limiting, request transformation, metrics collection, or integration with external services without changing application code.

Plugins can be applied at different scopes depending on where you want them to take effect:

- **Global**: they run for every request that passes through the gateway.
- **Service**: they apply only to a specific service.
- **Route**: they affect only one specific route.
- **Consumer**: they run for a specific consumer.

This flexibility lets you apply each policy only where it is needed and reuse configuration effectively.

## Deployment Models

Kong does not force you to work in just one way. In fact, there are several ways to deploy Kong, but we can group them into a few common models:

| Model | Database | Configuration Management | Scaling | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Traditional** | Yes, usually PostgreSQL | Dynamic through API or interface | Medium | The classic model, useful when you need centralized persistence and live changes. |
| **DB-less** | No | Declarative, from a file | High | Ideal for automation, ephemeral environments, or tightly controlled deployments. |
| **Hybrid** | Yes, only on the Control Plane | Centralized in the CP | Very high | Separates management and traffic into **Control Plane** and **Data Plane** for easy scale-out. |
| **Konnect** | Managed by the service | Centralized in SaaS | Very high | Moves the control plane to Kong's managed offering to reduce operational overhead. |
| **KIC** | Depends on the setup | Through Kubernetes CRDs | High | Integrates Kong with Kubernetes, which is the natural path if that is your main platform. |

## Common Ports

By default, Kong usually uses these ports:

- `8000` and `8443` for HTTP and HTTPS proxy traffic.
- `8001` and `8444` for the Admin API.

If you enable additional components such as visual administration or clustering, there may be other associated ports. In any case, it is good practice to expose only the essentials and restrict the Admin API as much as possible.

---

With this introduction we now have the full map: what Kong is, how it is organized, what role the Admin API and the dashboard play, and why its plugin model makes it such a powerful piece for microservices architectures.

In the next article we will start with the practical part and see how to deploy Kong with Docker.

---

**Next article:** [Lab: Installing Kong with Docker (Hybrid Mode)](/en/posts/kong/02-instalacion-docker-hibrido/02-instalacion-docker-hibrido/)
