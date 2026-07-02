---
title: "Lab: Installing Kong with Docker (Hybrid Mode)"
date: 2026-07-02T14:25:00+00:00
description: "Step-by-step practical guide to deploying Kong Gateway in hybrid mode using Docker Compose."
tags: [Kong, Docker, Docker Compose, Installation]
hero: images/kong/06-docker/hero.png
---

Hybrid mode deployment is one of the most used in production due to its ability to scale the data layer independently of the management layer. In this article, we will perform a practical installation using Docker Compose.

## Lab Architecture

For this deployment, we will use a container structure that includes:
- **PostgreSQL:** Configuration storage for the Control Plane.
- **Kong Control Plane (kong-cp):** Management node and admin API.
- **Kong Data Plane (kong-dp):** Node in charge of processing proxy traffic.
- **Mockbin:** An external backend service for routing tests.

## Installation Step-by-Step

### 1. Network Preparation
First, we must ensure we have an external network created so that containers can communicate with each other:

```bash
docker network create kong-edu-net
```

### 2. SSL Certificate Configuration
In hybrid mode, the CP and DP must communicate securely via mTLS. For this, we need to generate cluster certificates. 

If they are not available, the `kong-cp` node can generate them automatically upon startup using the command:
`kong hybrid gen_cert /etc/kong/ssl/cluster.crt /etc/kong/ssl/cluster.key`

### 3. Deployment with Docker Compose

We will use a `docker-compose.yaml` file to define the services. Key configuration points:

- **For the Control Plane (`kong-cp`):** 
  - Define `KONG_ROLE: control_plane`.
  - Configure Admin API (8001) and Manager (8002) ports.
  - Link the PostgreSQL database.

- **For the Data Plane (`kong-dp`):**
  - Define `KONG_ROLE: data_plane`.
  - Configure `KONG_DATABASE: off` (since the DP does not access the DB).
  - Define `KONG_CLUSTER_CONTROL_PLANE: kong-cp:8005` so it knows where to look for configuration.
  - Open the Proxy port (8000).

To bring up the infrastructure:

```bash
docker compose up -d
```

### 4. Deployment Verification

Once containers are up, we can check that the Gateway is operational by querying the Admin API:

```bash
curl -i http://localhost:8001/
```

If we receive a `200 OK`, the Control Plane is working. To verify the Proxy (Data Plane), we can try to access port 8000:

```bash
curl -i http://localhost:8000/
```

At this point, it is normal to receive a `404 Not Found`, as the Gateway is alive but we have not yet defined any route or service.

---

**Previous article:** [Kong Gateway Configuration Management](/posts/kong/05-configuracion-kong-gateway)  
**Next article:** [License Management in Kong Enterprise](/posts/kong/07-gestion-licencias-enterprise)
