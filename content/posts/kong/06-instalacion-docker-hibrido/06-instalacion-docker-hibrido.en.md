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

We will use a `docker-compose.yaml` file to define the services. Below is the content of the base file required for this deployment:

```yaml
volumes:
  kong_data:
    driver: local
networks:
  kong-edu-net:
    name: kong-edu-net
    driver: bridge
    external: true
services:
  postgres:
    image: postgres:15
    networks:
      - kong-edu-net
    container_name: postgres
    hostname: postgres
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "kong"]
      interval: 12s
      timeout: 6s
      retries: 3
    restart: unless-stopped
    stdin_open: true
    tty: true
    volumes:
      - kong_data:/var/lib/postgresql/data
    logging:
      driver: "syslog"
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-kong}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-kong}
      POSTGRES_USER: ${POSTGRES_USER:-kong}
  kong-migrations-bootstrap:
    image: kong/kong-gateway:${KONG_GW_VERSION:-3.10}
    networks:
      - kong-edu-net
    container_name: kong-migrations-bootstrap
    depends_on:
      postgres:
        condition: service_healthy
    command: kong migrations bootstrap --vv
    restart: on-failure
    logging:
      driver: "syslog"
    environment:
      KONG_DATABASE: ${KONG_DATABASE:-postgres}
      KONG_PG_HOST: ${KONG_PG_HOST:-postgres}
      KONG_PG_DATABASE: ${KONG_PG_DATABASE:-kong}
      KONG_PG_USER: ${KONG_PG_USER:-kong}
      KONG_PG_PASSWORD: ${KONG_PG_PASSWORD:-kong}
      KONG_PASSWORD: ${KONG_PASSWORD:-kong}
      KONG_LOG_LEVEL: "warn"
  kong-cp:
    image: kong/kong-gateway:${KONG_GW_VERSION:-3.10}
    networks:
      - kong-edu-net
    container_name: kong-cp
    hostname: kong-cp
    user: ${KONG_USER:-kong}
    depends_on:
      kong-migrations-bootstrap:
        condition: service_completed_successfully
    volumes:
      - /etc/kong/ssl:/etc/kong/ssl
      - /var/log/kong:/var/log/kong
    healthcheck:
      test: ["CMD", "kong", "health"]
      interval: 12s
      timeout: 6s
      retries: 3
    restart: on-failure
    logging:
      driver: "syslog"
    command:
      - /bin/sh
      - -c
      - |
        if [ ! -f /etc/kong/ssl/cluster.crt ]; then
          kong hybrid gen_cert /etc/kong/ssl/cluster.crt /etc/kong/ssl/cluster.key
        fi
        kong start --vv
    ports:
      - "8444-8447:8444-8447/tcp"
      - "8001-8004:8001-8004/tcp"
      - "8005-8006:8005-8006/tcp"
      - "8100:8100/tcp"
    environment:
      KONG_NGINX_HTTP_MORE_CLEAR_HEADERS: "Access-Control-Allow-Credentials"
      KONG_ROLE: control_plane
      KONG_CLUSTER_CERT: /etc/kong/ssl/cluster.crt
      KONG_CLUSTER_CERT_KEY: /etc/kong/ssl/cluster.key
      KONG_CLUSTER_DATA_PLANE_PURGE_DELAY: 600
      KONG_ADMIN_LISTEN: "0.0.0.0:8001, 0.0.0.0:8444 http2 ssl"
      KONG_ADMIN_GUI_LISTEN: "0.0.0.0:8002, 0.0.0.0:8445 http2 ssl"
      KONG_STATUS_LISTEN: "0.0.0.0:8100 ssl"
      KONG_CLUSTER_LISTEN: "0.0.0.0:8005"
      KONG_CLUSTER_TELEMETRY_LISTEN: "0.0.0.0:8006"
      KONG_DATABASE: ${KONG_DATABASE:-postgres}
      KONG_PG_HOST: ${KONG_PG_HOST:-postgres}
      KONG_PG_DATABASE: ${KONG_PG_DATABASE:-kong}
      KONG_PG_USER: ${KONG_PG_USER:-kong}
      KONG_PG_PASSWORD: ${KONG_PG_PASSWORD:-kong}
      KONG_PG_MAX_CONCURRENT_QUERIES: 5
      KONG_ADMIN_ACCESS_LOG: /var/log/kong/admin_access.log
      KONG_ADMIN_ERROR_LOG: /var/log/kong/admin_error.log
      KONG_ADMIN_GUI_ACCESS_LOG: /var/log/kong/admingui_access.log
      KONG_ADMIN_GUI_ERROR_LOG: /var/log/kong/admingui_error.log
      KONG_STATUS_ACCESS_LOG: /var/log/kong/status_access.log
      KONG_STATUS_ERROR_LOG: /var/log/kong/status_error.log
      KONG_AUDIT_LOG: "off"
      KONG_STATUS_SSL_CERT_KEY: "/etc/kong/ssl/server.key"
      KONG_STATUS_SSL_CERT: "/etc/kong/ssl/server.crt"
      KONG_ANONYMOUS_REPORTS: "off"
      KONG_ADMIN_SSL_CERT_KEY: "/etc/kong/ssl/server.key"
      KONG_ADMIN_SSL_CERT: "/etc/kong/ssl/server.crt"
      KONG_ADMIN_GUI_URL: ${KONG_ADMIN_GUI_URL-https://$FQDN:8445}
      KONG_ADMIN_GUI_API_URL: ${KONG_ADMIN_GUI_API_URL:-https://$FQDN:8444}
      KONG_ADMIN_GUI_SSL_CERT_KEY: "/etc/kong/ssl/server.key"
      KONG_ADMIN_GUI_SSL_CERT: "/etc/kong/ssl/server.crt"
      KONG_ADMIN_EMAILS_FROM: "kongtest@gmail.com"
      KONG_ADMIN_EMAILS_REPLY_TO: "kongtest@gmail.com"
      KONG_SMTP_MOCK: "on"
      KONG_NGINX_WORKER_PROCESSES: 1
      KONG_LUA_SSL_TRUSTED_CERTIFICATE: "/etc/kong/ssl/cluster.crt,system"
      KONG_LOG_LEVEL: "info"
      KONG_ENFORCE_RBAC: off
  kong-dp:
    image: kong/kong-gateway:${KONG_GW_VERSION:-3.10}
    networks:
      - kong-edu-net
    container_name: kong-dp
    hostname: kong-dp
    depends_on:
      - kong-cp
    volumes:
      - /etc/kong/ssl:/etc/kong/ssl
      - /var/log/kong:/var/log/kong
    healthcheck:
      test: ["CMD", "kong", "health"]
      interval: 12s
      timeout: 6s
      retries: 3
    restart: on-failure
    logging:
      driver: "syslog"
    command: kong start --vv
    ports:
      - "8443:8443/tcp"
      - "8000:8000/tcp"
      - "8101:8101/tcp"
    environment:
      KONG_NEW_DNS_CLIENT: "on"
      KONG_PLUGINS: bundled
      KONG_HEADERS: server_tokens, latency_tokens, X-Kong-Upstream-Status
      KONG_ROLE: "data_plane"
      KONG_CLUSTER_CERT: "/etc/kong/ssl/cluster.crt"
      KONG_CLUSTER_CERT_KEY: "/etc/kong/ssl/cluster.key"
      KONG_LUA_SSL_TRUSTED_CERTIFICATE: "/etc/kong/ssl/cluster.crt,system"
      KONG_CLUSTER_CONTROL_PLANE: "kong-cp:8005"
      KONG_CLUSTER_TELEMETRY_ENDPOINT: "kong-cp:8006"
      KONG_PROXY_LISTEN: "0.0.0.0:8000, 0.0.0.0:8443 http2 ssl"
      KONG_STREAM_LISTEN: "0.0.0.0:5555, 0.0.0.0:5556 ssl reuseport backlog=65536"
      KONG_STATUS_LISTEN: "0.0.0.0:8101 ssl"
      KONG_PROXY_URI: ${KONG_PROXY_URI:-http://$FQDN:8000}
      KONG_PROXY_ACCESS_LOG: /var/log/kong/proxy_access.log
      KONG_PROXY_ERROR_LOG: /var/log/kong/proxy_error.log
      KONG_PROXY_STREAM_ACCESS_LOG: /var/log/kong/proxystream_access.log basic
      KONG_PROXY_STREAM_ERROR_LOG: /var/log/kong/proxystream_error.log
      KONG_DATABASE: "off"
      KONG_ANONYMOUS_REPORTS: "on"
      KONG_SSL_CERT_KEY: "/etc/kong/ssl/server.key"
      KONG_SSL_CERT: "/etc/kong/ssl/server.crt"
      KONG_NGINX_WORKER_PROCESSES: 1
      KONG_LOG_LEVEL: "info"
      KONG_ALLOW_DEBUG_HEADER: "on"
```

Key configuration points:


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



### 5. Deployment of Test Services (Mockbin)

To verify that the Gateway processes traffic correctly, we will deploy a test service called Mockbin. This service acts as a simple backend that returns information about the requests received.

We will use the following `docker-compose.yaml` file specifically for Mockbin:

```yaml
networks:
  kong-edu-net:
    name: kong-edu-net
    driver: bridge
    external: true

services:
  mockbin:
    networks:
    - kong-edu-net
    image: mashape/mockbin:latest
    container_name: mockbin.local
    hostname: mockbin.local
    healthcheck:
      test: ["CMD-SHELL", "exit 0"]
      interval: 30s
      timeout: 30s
      retries: 3        
    restart: on-failure
    ports:
    - "8888:8080/tcp"
```

To deploy it, run:

```bash
docker compose -f mockbin/docker-compose.yaml up -d
```

---

**Previous article:** [Kong Gateway Configuration Management](/posts/kong/05-configuracion-kong-gateway)  
**Next article:** [License Management in Kong Enterprise](/posts/kong/07-gestion-licencias-enterprise)
