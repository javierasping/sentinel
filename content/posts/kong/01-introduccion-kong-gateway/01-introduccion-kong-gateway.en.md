---
title: "Introduction to Kong Gateway"
date: 2026-07-02T14:00:00+00:00
description: "Discover what Kong Gateway is, how it works as an API Gateway and Reverse Proxy, and why it is fundamental in cloud-native architectures."
tags: [Kong, API Gateway, Reverse Proxy, Cloud Native]
hero: images/kong/01-introduccion/hero.png
---

In today's ecosystem of microservices and cloud-native applications, API management has become a critical piece to ensure the security, performance, and scalability of systems. This is where **Kong Gateway** comes into play.

## What is Kong Gateway?

Kong Gateway is an open-source, lightweight, fast, and flexible API Gateway designed to act as the single entry point for all requests arriving at your backend services. In essence, it works as an advanced **Reverse Proxy** that accepts API calls from clients and redirects them to the appropriate backend service.

### The role of an API Gateway

An API Gateway is not simply a traffic "pass-through". Its value lies in the ability to centralize cross-cutting functionalities that would otherwise have to be implemented repeatedly in each microservice. Some of these capabilities include:

- **Security and Authentication:** Implementing OAuth2, JWT, or API Keys in one place.
- **Traffic Control:** Rate limiting and quota management to prevent service saturation.
- **Transformation:** Modifying requests and responses on the fly (validation, header changes, etc.).
- **Observability:** Centralizing logs and monitoring of all API calls.
- **Multi-format Support:** Ability to work with REST, gRPC, SOAP, and GraphQL.

## Advantages of Kong Gateway

Kong is distinguished by being agnostic to the platform and environment. It can be deployed anywhere: from on-premise servers to public clouds, Kubernetes environments, or even serverless architectures. 

Furthermore, it offers exceptional flexibility in its deployment, allowing configurations with or without a database, and hybrid or cloud-managed (SaaS) operation modes.

In the following articles of this series, we will explore in depth its components, different deployment topologies, and how to carry out a professional installation step by step.

---

**Next article:** [Core Components of Kong Gateway](/posts/kong/02-componentes-core-kong)
