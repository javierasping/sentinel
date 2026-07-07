---
title: "Technical Lab: Installing Kong in Konnect"
date: 2026-07-02T14:40:00+00:00
description: "Learn how to configure Kong's routing logic by creating your first Services and Routes through the Admin API."
tags: [Kong, API Routing, Admin API, Microservices]
hero: images/kong/09-routing/hero.png
---

Once the Gateway is installed and running, the next step is to make traffic reach your applications. To achieve this, Kong uses two fundamental concepts: **Services** and **Routes**.

## Understanding Routing Logic

For Kong to know where to send a request, it must follow a logical flow:
`Client` $\rightarrow$ `Route` $\rightarrow$ `Service` $\rightarrow$ `Backend (Upstream)`

### What is a Service?
A Service is the abstract representation of your backend API. Instead of referencing the real server URL in every rule, you define a Service that contains the base URL, port, and protocol of the backend.

### What is a Route?
A Route is the rule that defines how a Service is accessed. It can be based on:
- **Paths:** For example, any request starting with `/payments` is redirected to the payments service.
- **Hosts:** Requests directed to `api.mysite.com`.
- **HTTP Methods:** Only `POST` requests to a specific endpoint.

---

## Practical Configuration via Admin API

Imagine we have a test service called **Mockbin**. Let's expose it through Kong.

### 1. Creating the Service
First, we define the service indicating the name and the real backend URL:

```bash
curl -X POST http://localhost:8001/services \
  -d "name=mockbin_service" \
  -d "url=http://mockbin.local/request"
```

### 2. Creating the Route
Now, we create a route that associates the path `/mockbin` with the service we just created:

```bash
curl -X POST http://localhost:8001/services/mockbin_service/routes \
  -d "name=mockbin_route" \
  -d "paths[]=/mockbin"
```

### 3. Verifying the Configuration
We can check that the objects have been created correctly by querying the Admin API endpoints:

```bash
# List all services
curl http://localhost:8001/services

# List all routes
curl http://localhost:8001/routes
```

With this configuration, any request sent to the Kong Proxy port on the `/mockbin` path will be automatically redirected to the Mockbin backend.

---

**Previous article:** [Technical Lab: Installing Kong in DB-less Mode](/en/posts/kong/04-instalacion-db-less/04-instalacion-db-less/)  
**Next article:** [Technical Lab: Installing Kong Ingress Controller (KIC)](/en/posts/kong/06-instalacion-kic/06-instalacion-kic/)
