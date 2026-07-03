---
title: "Lab: Installing Kong with Docker (Hybrid Mode)"
date: 2026-07-02T14:25:00+00:00
description: "A practical step-by-step guide to deploying Kong Gateway in hybrid mode using Docker Compose."
tags: [Kong, Docker, Docker Compose, Installation]
hero: images/kong/06-docker/hero.png
---

Hybrid mode deployment is one of the most common in production due to its ability to scale the data layer independently from the management layer. In this article, we will perform a practical installation using Docker Compose.

## Lab Architecture

For this deployment, we will use a container structure that includes:
- **PostgreSQL:** Configuration storage for the Control Plane.
- **Kong Control Plane (kong-cp):** Management node and admin API.
- **Kong Data Plane (kong-dp):** Node responsible for processing proxy traffic.
- **Mockbin:** An external backend service to perform routing tests.

## Step-by-Step Installation

### 1. Environment Preparation
First, we will create the workspace directory and the folder structure needed for data and log persistence:

```bash
mkdir -p /home/javiercruces/kong/{config,data,logs,mocks,ssl}
cd /home/javiercruces/kong
```

### 2. Environment Variables
We create a `.env` file to centralize critical configurations such as passwords, versions, and the FQDN:

```bash
cat <<EOF > .env
KONG_GW_VERSION=3.10
POSTGRES_USER=kong
POSTGRES_PASSWORD=kong_password_secure_123
POSTGRES_DB=kong
KONG_DATABASE=postgres
KONG_PG_HOST=postgres
KONG_PG_DATABASE=kong
KONG_PG_USER=kong
KONG_PG_PASSWORD=kong_password_secure_123
KONG_PASSWORD=kong_password_secure_123
FQDN=kong.javiercd.es
KONG_ADMIN_GUI_URL=https://$FQDN:8445
KONG_ADMIN_GUI_API_URL=https://$FQDN:8444
EOF
```

### 3. Network Configuration and SSL Certificates
For hybrid mode, Kong requires mTLS between the control plane and the data plane. We will generate the necessary cluster certificates:

```bash
docker network create kong-edu-net || true
```

### 4. Deployment with Docker Compose (Base Infrastructure)
We create the main `docker-compose.yaml` file to deploy PostgreSQL and the Kong nodes.

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
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_USER: ${POSTGRES_USER}
  kong-migrations-bootstrap:
    image: kong/kong-gateway:${KONG_GW_VERSION}
    networks:
      - kong-edu-net
    container_name: kong-migrations-bootstrap
    depends_on:
      postgres:
        condition: service_healthy
    command: kong migrations bootstrap --vv
    restart: on-failure
    environment:
      KONG_DATABASE: ${KONG_DATABASE}
      KONG_PG_HOST: ${KONG_PG_HOST}
      KONG_PG_DATABASE: ${KONG_PG_DATABASE}
      KONG_PG_USER: ${KONG_PG_USER}
      KONG_PG_PASSWORD: ${KONG_PG_PASSWORD}
      KONG_PASSWORD: ${KONG_PASSWORD}
      KONG_LOG_LEVEL: "warn"
  kong-cp:
    image: kong/kong-gateway:${KONG_GW_VERSION}
    networks:
      - kong-edu-net
    container_name: kong-cp
    hostname: kong-cp
    user: ${KONG_USER:-kong}
    depends_on:
      kong-migrations-bootstrap:
        condition: service_completed_successfully
    volumes:
      - ./ssl:/etc/kong/ssl
      - ./logs:/var/log/kong
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
      KONG_DATABASE: ${KONG_DATABASE}
      KONG_PG_HOST: ${KONG_PG_HOST}
      KONG_PG_DATABASE: ${KONG_PG_DATABASE}
      KONG_PG_USER: ${KONG_PG_USER}
      KONG_PG_PASSWORD: ${KONG_PG_PASSWORD}
      KONG_PG_MAX_CONCURRENT_QUERIES: 5
      KONG_ADMIN_ACCESS_LOG: /var/log/kong/admin_access.log
      KONG_ADMIN_ERROR_LOG: /var/log/kong/admin_error.log
      KONG_ADMIN_GUI_ACCESS_LOG: /var/log/kong/admingui_access.log
      KONG_ADMIN_GUI_ERROR_LOG: /var/log/kong/admingui_error.log
      KONG_STATUS_ACCESS_LOG: /var/log/kong/status_access.log
      KONG_STATUS_ERROR_LOG: /var/log/kong/status_error.log
      KONG_AUDIT_LOG: "off"
      KONG_STATUS_SSL_CERT_KEY: "/etc/kong/ssl/cluster.key"
      KONG_STATUS_SSL_CERT: "/etc/kong/ssl/cluster.crt"
      KONG_ANONYMOUS_REPORTS: "off"
      KONG_ADMIN_SSL_CERT_KEY: "/etc/kong/ssl/cluster.key"
      KONG_ADMIN_SSL_CERT: "/etc/kong/ssl/cluster.crt"
      KONG_ADMIN_GUI_URL: ${KONG_ADMIN_GUI_URL}
      KONG_ADMIN_GUI_API_URL: ${KONG_ADMIN_GUI_API_URL}
      KONG_ADMIN_EMAILS_FROM: "kongtest@gmail.com"
      KONG_ADMIN_EMAILS_REPLY_TO: "kongtest@gmail.com"
      KONG_SMTP_MOCK: "on"
      KONG_NGINX_WORKER_PROCESSES: 1
      KONG_LUA_SSL_TRUSTED_CERTIFICATE: "/etc/kong/ssl/cluster.crt,system"
      KONG_LOG_LEVEL: "info"
      KONG_ENFORCE_RBAC: off
  kong-dp:
    image: kong/kong-gateway:${KONG_GW_VERSION}
    networks:
      - kong-edu-net
    container_name: kong-dp
    hostname: kong-dp
    depends_on:
      - kong-cp
    volumes:
      - ./ssl:/etc/kong/ssl
      - ./logs:/var/log/kong
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
      KONG_PROXY_STREAM_ACCESS_LOG: /var/log/kong/proxystream_access_log basic
      KONG_PROXY_STREAM_ERROR_LOG: /var/log/kong/proxystream_error_log
      KONG_DATABASE: "off"
      KONG_ANONYMOUS_REPORTS: "on"
      KONG_SSL_CERT_KEY: "/etc/kong/ssl/cluster.key"
      KONG_SSL_CERT: "/etc/kong/ssl/cluster.crt"
      KONG_NGINX_WORKER_PROCESSES: 1
      KONG_LOG_LEVEL: "info"
      KONG_ALLOW_DEBUG_HEADER: "on"
```

Para iniciar la infraestructura base:

```bash
docker compose up -d
```

### 5. Deployment of the Echo Server and Mocks
We create the directory for mocks and the specific `docker-compose.yaml` file for the Echo Server (Mockbin):

```bash
mkdir -p /home/javiercruces/kong/mocks
cat <<EOF > /home/javiercruces/kong/mocks/docker-compose.yaml
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
EOF

docker compose -f /home/javiercruces/kong/mocks/docker-compose.yaml up -d
```

### 6. Kong Configuration via Admin API
We will configure the Echo Server as a Service, create a Route, and set up authentication via the Kong Admin API.

**Create the Service (Echo Server):**
```bash
curl -i -X POST http://localhost:8001 \
  -d '{
    "name": "echo-server",
    "protocol": "http",
    "host": "mockbin.local",
    "port": 8080
  }'
```

**Create the Route:**
```bash
curl -i -X POST http://localhost:8001 \
  -d '{
    "plugins": ["key-auth"],
    "routes": [{
      "paths": ["/echo"],
      "service": "echo-server"
    }]
  }'
```

**Create the Consumer (User) for the API Key:**
```bash
curl -i -X POST http://localhost:8001 \
  -d '{
    "name": "test-user",
    "key": "secret-api-key-123"
  }'
```

### 7. Validation of Functionality
To validate that the configuration is correct, we will perform a request without a key (should fail with 401) and then one with the corresponding key.

**Failed request (No API Key):**
```bash
curl -i http://kong.javiercd.es/echo
```
*Expected output:* `401 Unauthorized`

**Successful request (With API Key):**
```bash
curl -i -H "apikey: secret-api-key-123" http://kong.javiercd.es/echo
```
*Expected output:* `200 OK` with the Mockbin response body.

---

**Previous article:** [Kong Gateway Configuration Management](/posts/kong/05-configuracion-kong-gateway)  
**Next article:** [Kong Enterprise License Management](/posts/kong/07-gestion-licencias-enterprise)
