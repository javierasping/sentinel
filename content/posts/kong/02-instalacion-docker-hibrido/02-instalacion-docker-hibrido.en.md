---
title: "Installing Kong with Docker (Hybrid Mode)"
date: 2026-07-26T00:00:00+02:00
description: "Technical, reproducible guide to install Kong Gateway in Hybrid mode with Docker Compose, bring up an echo server, and validate it with API key authentication."
tags: [Kong, Docker, Docker Compose, Installation, API Key]
hero: images/kong/docker-hybrid.png
weight: 2
---

## Introduction

In this article we will deploy **Kong Gateway 3.10 open source** in **Hybrid mode** using Docker Compose. This architecture, based on the separation between the **Control Plane (CP)** and the **Data Plane (DP)**, is one of the deployment models recommended by Kong for API Gateway environments because of its flexibility, scalability, and high availability.

In a Hybrid deployment, only the **Control Plane** maintains a direct connection to the database and is responsible for managing the full gateway configuration through the **Admin API** and **Kong Manager**. The **Data Planes**, on the other hand, run in *DB-less* mode and automatically receive configuration from the Control Plane through a secure channel protected by **mTLS**. This allows the Data Planes to keep processing traffic even if the Control Plane or the database becomes temporarily unavailable.

This separation brings major advantages over a traditional architecture. It reduces the load on the database, makes it easy to deploy multiple Data Planes across different data centers or regions, improves security by isolating the management plane from the data plane, and simplifies centralized administration of the whole platform.

Throughout this lab we will build a complete infrastructure from scratch using Docker Compose. We will deploy PostgreSQL, a Control Plane, and a Data Plane, analyze the purpose of each component, and understand how they communicate with each other. Once the infrastructure is up, we will publish our first service through Kong using an **Echo Server**, creating the gateway's core resources step by step: **Services**, **Routes**, **Plugins**, **Consumers**, and their credentials.

The goal of this article is not only to get Kong working, but also to understand how a Hybrid architecture works internally and why it is the deployment model used by **Konnect** and by most enterprise Kong Gateway implementations. By the end of the lab, you will have deployed a fully functional platform and you will also understand the complete flow of a request from the proxy to the backend service, as well as how the Control Plane distributes configuration to all Data Planes in the cluster.

## What is Kong Gateway Hybrid mode?

**Hybrid mode** is a Kong Gateway deployment model that separates management and traffic processing responsibilities into two different node types: **Control Plane (CP)** and **Data Plane (DP)**.

Unlike a traditional deployment, where every Kong instance maintains a direct connection to the database, in a Hybrid architecture only the nodes acting as **Control Plane** access PostgreSQL. The **Data Planes** run in **DB-less** mode and receive all their configuration from the Control Plane through a secure channel protected by **mTLS**.

Whenever an administrator makes a change through the **Admin API** or **Kong Manager**, the Control Plane stores the new configuration in the database, generates a declarative representation of it, and automatically distributes it to every connected Data Plane.

This model completely decouples platform administration from request processing, making it easier to scale both components independently and significantly reducing the load on the database.

The following figure shows the general architecture of a Hybrid deployment.

```text
                     PostgreSQL
                          │
                          │
                   Configuration
                          │
                +---------▼---------+
                |   Control Plane   |
                |                   |
                | Admin API         |
                | Kong Manager      |
                +---------+---------+
                          │
                     mTLS (8005/8006)
                          │
          ┌───────────────┴───────────────┐
          │                               │
 +--------▼--------+             +--------▼--------+
 |   Data Plane 1  |             |   Data Plane 2  |
 |                 |             |                 |
 | Proxy HTTP/HTTPS|             | Proxy HTTP/HTTPS|
 +--------+--------+             +--------+--------+
          │                               │
          └───────────────┬───────────────┘
                          │
                       Clients
```

---

### What is a Control Plane?

The **Control Plane** is the component responsible for Kong Gateway administration.

All tasks related to platform management are performed from this node, including the creation and modification of **Services**, **Routes**, **Plugins**, **Consumers**, certificates, authentication, and any other resource supported by Kong Gateway.

The Control Plane also exposes two key interfaces:

- **Admin API**, used to administer Kong programmatically.
- **Kong Manager**, the graphical interface used to manage the platform.

Unlike the Data Plane, the Control Plane maintains a permanent connection to PostgreSQL, where it stores the gateway configuration.

Whenever that configuration changes, the Control Plane automatically generates a new declarative configuration and distributes it to all connected Data Planes through a secure **mTLS** channel.

It is important to note that the Control Plane **does not process client traffic**. Its only responsibility is to manage configuration and synchronize it with the Data Planes.

---

### What is a Data Plane?

The **Data Plane** is the component responsible for receiving and processing client requests.

Every HTTP or HTTPS request that reaches Kong goes through one of the Data Planes, where the full gateway pipeline is executed:

1. Identify the matching Route.
2. Resolve the associated Service.
3. Execute the configured Plugins.
4. Perform load balancing if needed.
5. Forward the request to the backend.

Unlike the Control Plane, the Data Plane **does not have direct access to PostgreSQL**. It receives all the configuration it needs from the Control Plane.

In addition, each Data Plane stores a local copy of the last received configuration in an **LMDB** database (`dbless.lmdb`). Thanks to this mechanism, the gateway can continue processing traffic even if the Control Plane or the database becomes temporarily unavailable.

When the Control Plane becomes available again, the Data Planes automatically restore communication and synchronize any pending changes.

---

### Advantages of Hybrid mode

Hybrid mode brings many advantages over a traditional architecture and is the deployment model Kong recommends for most enterprise use cases.

Its main benefits include:

- **Independent scalability.** You can increase the number of Data Planes without changing the management infrastructure or the database.

- **High availability.** Data Planes continue serving traffic using the last received configuration even when the Control Plane or PostgreSQL are unavailable.

- **Lower database load.** Only the Control Planes maintain connections to PostgreSQL, significantly reducing the number of concurrent accesses.

- **Better security.** Data Planes do not need direct database access and do not expose management interfaces, reducing the attack surface.

- **Centralized administration.** All configuration is handled from one or more Control Planes, simplifying the management of large distributed deployments.

- **Geographically distributed deployments.** You can deploy groups of Data Planes in different regions or data centers without needing a local database at each location.

- **Konnect compatibility.** The architecture used by Kong Konnect is also based on the Control Plane / Data Plane model, so learning this deployment mode makes it easier to move to Kong-managed environments.

## Lab Architecture

To understand how Kong Gateway works in **Hybrid** mode, we will build a complete environment using Docker Compose. Although this is a lab running on a single machine, the architecture is equivalent to the one used in many enterprise deployments, where the **Control Plane** and the **Data Planes** run on different servers or in different data centers.

The infrastructure will be made up of four main services:

- A **PostgreSQL** server, responsible for storing the gateway configuration.
- A **Control Plane**, responsible for managing the Kong Gateway configuration.
- A **Data Plane**, responsible for processing client traffic.
- An **Echo Server**, which will act as a test backend to validate gateway behavior.

The following diagram shows the architecture we will build during this lab.

```text
                           Docker Host
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│  PostgreSQL                                                        │
│      ▲                                                             │
│      │                                                             │
│      │ Configuration                                               │
│      │                                                             │
│  ┌───┴──────────────┐                                               │
│  │   Control Plane  │                                               │
│  │                  │                                               │
│  │ Admin API        │                                               │
│  │ Kong Manager     │                                               │
│  └───────┬──────────┘                                               │
│          │                                                          │
│      mTLS (8005 / 8006)                                             │
│          │                                                          │
│  ┌───────▼──────────┐                                               │
│  │    Data Plane    │                                               │
│  │                  │                                               │
│  │ Proxy HTTP/HTTPS │                                               │
│  └───────┬──────────┘                                               │
│          │                                                          │
│          ▼                                                          │
│    Echo Server                                                      │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

                 Client
                    │
                    ▼
             http://localhost:8000
```

---

## Prerequisites

Before starting this lab, it is a good idea to have the following knowledge and tools available.

### Recommended knowledge

- Basic Docker and Docker Compose concepts.
- Basic TCP/IP networking.
- Using the Linux terminal.
- Basic knowledge of REST APIs and HTTP.

### Required software

- Docker Engine 28 or later.
- Docker Compose v2.
- Kong Gateway 3.10 open source.
- PostgreSQL.
- Curl.
- A web browser to access Kong Manager.

### Lab resources

To complete this lab we will use:

- A single Linux server.
- Internet access to download Docker images.
- At least 4 GB of available RAM.
- Around 5 GB of free disk space.

## Environment Preparation

Before deploying Kong Gateway, we need to prepare the working environment. In this section we will create the directory structure used during the lab and define the environment variables that centralize all deployment configuration.

Although this is a lab running on a single machine, we will organize the resources using a structure similar to what you would find in a production environment. This will make the architecture easier to understand and will also help us extend the lab in later articles of the series.

By the end of this section, everything needed to deploy Kong Gateway with Docker Compose will be ready.

### The Docker Network

All containers in the lab will share a Docker network called **kong-net**.

This network will allow the different services to communicate with each other using their hostnames, without needing to know their IP addresses. For example, the Control Plane will connect to PostgreSQL using the hostname `postgres`, while the Data Plane will communicate with the Control Plane using the hostname `kong-cp`.

Unlike other labs where the network must be created manually, in this case **Docker Compose** will create it automatically during infrastructure deployment.

In the `docker-compose.yaml` file we will define the network.

When we run `docker compose up`, Docker will detect that the network does not exist and will create it automatically before starting the rest of the services.

---

## Proxy Certificate Configuration

In addition to the certificates used to protect communication between the **Control Plane** and the **Data Plane**, we need a second certificate that Kong Gateway will present when clients access the Proxy over HTTPS.

In this lab we will use a **self-signed** certificate for the domain:

```text
*.kong.javiercd.es
```

This certificate will only be used to encrypt HTTPS connections established between clients and the Kong Gateway Proxy.

> **Note**
>
> Because this is a self-signed certificate, browsers will show a warning indicating that the issuing authority is not trusted. This is completely normal in a lab environment.

### Generating the Certificate

We will generate the certificate in the folder where I created the scenario files, and create an `ssl` directory:

```bash
mkdir -p kong/ssl
```

> Note: because the Kong container mounts `./ssl` into `/etc/kong/ssl` and runs as the `kong` user, the host directory must be writable by that user inside the container. If you see errors such as `Permission denied` or `No such file or directory` when generating `cluster.crt`/`cluster.key`, fix the permissions on the directory with:
>
> ```bash
> sudo chown -R 1000:1000 kong/ssl
> chmod 755 kong/ssl
> ```
>
> This ensures the process inside the container can create and modify certificates in the mounted volume.

We create the certificate and private key by running the following command:

```bash
openssl req \
  -x509 \
  -nodes \
  -newkey rsa:4096 \
  -sha256 \
  -days 3650 \
  -keyout ssl/proxy.key \
  -out ssl/proxy.crt \
  -subj "/C=ES/ST=Sevilla/L=Dos Hermanas/O=Javier Cruces/OU=Kong Lab/CN=*.kong.javiercd.es" \
  -addext "subjectAltName=DNS:*.kong.javiercd.es,DNS:kong.javiercd.es"
```

Once the process is complete, the following files will have been generated:

```bash
javiercruces@kong:~/kong$ ls -l ssl/
total 8
-rw-rw-r-- 1 javiercruces javiercruces 2163 Jul  3 20:49 proxy.crt
-rw------- 1 javiercruces javiercruces 3272 Jul  3 20:49 proxy.key
```

Later, we will configure the Data Plane to use these certificates through the following variables:

```yaml
KONG_SSL_CERT: "/etc/kong/ssl/proxy.crt"
KONG_SSL_CERT_KEY: "/etc/kong/ssl/proxy.key"
```

From this point on, any client establishing an HTTPS connection with Kong Gateway will receive this certificate during the TLS handshake.

In a production environment, it is recommended to use certificates issued by a trusted Certificate Authority (CA), such as Let's Encrypt or an internal corporate PKI. However, for a lab, a self-signed certificate is enough to understand how Kong Gateway's HTTPS Proxy works.

### Environment Variables

To avoid duplicating information inside the `docker-compose.yaml`, we will store the configuration parameters in a `.env` file.

This file will centralize the lab configuration, including:

- The Kong Gateway version.
- PostgreSQL credentials.
- The database name.
- The FQDN used by Kong Manager.
- The user used to run Kong.

We create the `.env` file with the following content:

```python
KONG_GW_VERSION=3.10.0.0

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

# Certificates used by the HTTPS Proxy
KONG_SSL_CERT=/etc/kong/ssl/proxy.crt
KONG_SSL_CERT_KEY=/etc/kong/ssl/proxy.key

# Certificates used for CP <-> DP communication
KONG_CLUSTER_CERT=/etc/kong/ssl/cluster.crt
KONG_CLUSTER_CERT_KEY=/etc/kong/ssl/cluster.key

KONG_ADMIN_GUI_URL=https://$FQDN:8445
KONG_ADMIN_GUI_API_URL=https://$FQDN:8444

KONG_USER=kong
```

Docker Compose will automatically load this file during deployment, replacing the `${VARIABLE}` references defined in the `docker-compose.yaml`.

### Creating the Docker Compose file

Now, in the directory we created earlier, create this `docker-compose.yaml` file:

```yaml
javiercruces@kong:~/kong$ cat docker-compose.yaml
volumes:
  kong_data:
    driver: local
networks:
  kong-net:
    name: kong-net
    driver: bridge
services:
  postgres:
    image: postgres:15
    networks:
      - kong-net
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
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_USER: ${POSTGRES_USER:-kong}
  kong-migrations-bootstrap:
    image: kong/kong-gateway:${KONG_GW_VERSION:-3.10.0.0}
    networks:
      - kong-net
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
      KONG_PG_PASSWORD: ${KONG_PG_PASSWORD}
      KONG_PASSWORD: ${KONG_PASSWORD}
      KONG_LOG_LEVEL: "warn"
  kong-cp:
    image: kong/kong-gateway:${KONG_GW_VERSION:-3.10.0.0}
    networks:
      - kong-net
    container_name: kong-cp
    hostname: kong-cp
    user: ${KONG_USER:-kong}
    depends_on:
      kong-migrations-bootstrap:
        condition: service_completed_successfully
    volumes:
      - ./ssl:/etc/kong/ssl
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
          chown kong:kong /etc/kong/ssl/cluster.crt /etc/kong/ssl/cluster.key
          chmod 644 /etc/kong/ssl/cluster.crt
          chmod 640 /etc/kong/ssl/cluster.key
        fi
        kong start --vv
    ports:
      - "8444:8444/tcp"
      - "8445:8445/tcp"
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
      KONG_PG_PASSWORD: ${KONG_PG_PASSWORD}
      KONG_PG_MAX_CONCURRENT_QUERIES: 5
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ERROR_LOG: /dev/stderr
      KONG_ADMIN_GUI_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_GUI_ERROR_LOG: /dev/stderr
      KONG_STATUS_ACCESS_LOG: /dev/stdout
      KONG_STATUS_ERROR_LOG: /dev/stderr
      KONG_AUDIT_LOG: "off"
      KONG_STATUS_SSL_CERT_KEY: /etc/kong/ssl/cluster.key
      KONG_STATUS_SSL_CERT: "/etc/kong/ssl/cluster.crt"
      KONG_ANONYMOUS_REPORTS: "off"
      KONG_ADMIN_SSL_CERT_KEY: /etc/kong/ssl/cluster.key
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
    image: kong/kong-gateway:${KONG_GW_VERSION:-3.10.0.0}
    networks:
      - kong-net
    container_name: kong-dp
    hostname: kong-dp
    user: kong
    depends_on:
      - kong-cp
    volumes:
      - ./ssl:/etc/kong/ssl
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
      - "8000:8000/tcp"
    environment:
      KONG_NEW_DNS_CLIENT: "on"
      KONG_PLUGINS: bundled
      KONG_HEADERS: server_tokens, latency_tokens, X-Kong-Upstream-Status
      KONG_ROLE: "data_plane"
      KONG_CLUSTER_CERT: "/etc/kong/ssl/cluster.crt"
      KONG_CLUSTER_CERT_KEY: /etc/kong/ssl/cluster.key
      KONG_LUA_SSL_TRUSTED_CERTIFICATE: "/etc/kong/ssl/cluster.crt,system"
      KONG_CLUSTER_CONTROL_PLANE: "kong-cp:8005"
      KONG_CLUSTER_TELEMETRY_ENDPOINT: "kong-cp:8006"
      KONG_PROXY_LISTEN: "0.0.0.0:8000, 0.0.0.0:8443 http2 ssl"
      KONG_STREAM_LISTEN: "0.0.0.0:5555, 0.0.0.0:5556 ssl reuseport backlog=65536"
      KONG_STATUS_LISTEN: "0.0.0.0:8101 ssl"
      KONG_PROXY_URI: ${KONG_PROXY_URI:-http://$FQDN:8000}
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_PROXY_STREAM_ACCESS_LOG: "off"
      KONG_PROXY_STREAM_ERROR_LOG: "off"
      KONG_DATABASE: "off"
      KONG_ANONYMOUS_REPORTS: "on"
      KONG_SSL_CERT_KEY: /etc/kong/ssl/cluster.key
      KONG_SSL_CERT: "/etc/kong/ssl/cluster.crt"
      KONG_NGINX_WORKER_PROCESSES: 1
      KONG_LOG_LEVEL: "info"
      KONG_ALLOW_DEBUG_HEADER: "on"
```

## Deploying the Infrastructure

Once all the configuration is ready, we can deploy the infrastructure using Docker Compose.

Run the following command from the lab directory:

```bash
javiercruces@kong:~/kong$ docker compose up -d
[+] Running 6/6
 ✔ Network kong-net                     Created
 ✔ Volume kong_kong_data               Created
 ✔ Container postgres                   Healthy
 ✔ Container kong-migrations-bootstrap  Exited
 ✔ Container kong-cp                    Started
 ✔ Container kong-dp                    Started
```

During this process, Docker Compose automatically performs the following actions:

- Creates the `kong-net` network, used for communication between all containers.
- Creates the persistent volume where PostgreSQL will store its data.
- Starts the PostgreSQL database and waits until it is available.
- Runs the `kong-migrations-bootstrap` container, which initializes Kong Gateway's database schema.
- Starts the **Control Plane** (`kong-cp`).
- Starts the **Data Plane** (`kong-dp`), which automatically establishes a secure connection with the Control Plane through **mTLS**.

> **Note**
>
> It is completely normal for the `kong-migrations-bootstrap` container to finish with status **Exited (0)**. Its only job is to run the initial database migrations and then exit successfully once they are complete.

Next, we verify that all containers were deployed correctly:

```bash
javiercruces@kong:~/kong$ docker ps -a
CONTAINER ID   IMAGE                        COMMAND                  CREATED         STATUS                     PORTS                                                                                                     NAMES
1a53c0c225a2   kong/kong-gateway:3.10.0.0   "/entrypoint.sh kong…"   2 minutes ago   Up 2 minutes (healthy)     8001-8004/tcp, 0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp, 8443-8447/tcp                                 kong-dp
5ffe4b43af60   kong/kong-gateway:3.10.0.0   "/entrypoint.sh /bin…"   2 minutes ago   Up 2 minutes (healthy)     8000-8004/tcp, 8443/tcp, 8446-8447/tcp, 0.0.0.0:8444-8445->8444-8445/tcp, [::]:8444-8445->8444-8445/tcp   kong-cp
705169cc65aa   kong/kong-gateway:3.10.0.0   "/entrypoint.sh kong…"   2 minutes ago   Exited (0) 2 minutes ago                                                                                                             kong-migrations-bootstrap
dce55af755c2   postgres:15                  "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes (healthy)     5432/tcp                                                                                                  postgres
```

If everything went well, we should see that:

- **PostgreSQL** is in a **healthy** state.
- The **Control Plane** (`kong-cp`) is running and ready to manage cluster configuration.
- The **Data Plane** (`kong-dp`) is running and connected to the Control Plane.
- The **kong-migrations-bootstrap** container finished successfully with status **Exited (0)**, indicating that the database migrations were executed correctly.

With the infrastructure deployed, the next step is to confirm that the **Control Plane** and **Data Plane** are communicating properly before we start publishing services through Kong Gateway.

## Deploying the Echo Server

Once the Kong Gateway infrastructure is deployed, the next step is to have a backend service where requests can be forwarded.

For this lab we will use an **Echo Server**, a very simple application whose only purpose is to return to the client all the information from the received HTTP request. This will let us easily verify that Kong is routing requests correctly and observe how the different plugins, header transformations, or authentication mechanisms we configure later affect the request.

### Why use an Echo Server?

The purpose of this lab is to learn how Kong Gateway works, not to build a backend application. By using an Echo Server we eliminate unnecessary complexity and can focus entirely on the behavior of the API Gateway.

Also, because it returns all the information from the received request, we can easily check:

- The URL used.
- The HTTP method used.
- The headers sent by the client.
- The headers added automatically by Kong.
- Request parameters.
- The received body.

### Creating the directory

Create a separate directory for the Echo Server:

```bash
mkdir echo-server
cd echo-server
```

### Creating the Docker Compose file

Inside the `echo-server` directory create the `docker-compose.yaml` file:

```yaml
services:
  echo-server:
    image: hashicorp/http-echo:latest
    container_name: echo-server
    hostname: echo-server
    restart: unless-stopped

    environment:
      ENABLE__ENVIRONMENT: "false"

    networks:
      - kong-net

networks:
  kong-net:
    external: true
```

As you can see, the container connects to the same Docker network (`kong-net`) used by Kong Gateway.

This lets Docker automatically provide DNS resolution between containers belonging to the same network. Thanks to that, Kong can reach the backend using only the service name, without needing to know its IP address.

> **Note**
>
> In this lab the Echo Server **does not expose any port to the host**. It will only be reachable from the internal `kong-net` network, where the Kong Control Plane and Data Plane are also located. This architecture is closer to a production environment, where backend services are usually isolated and only the API Gateway receives connections from the outside.

### Deploying the service

Once the file has been created, start the container:

```bash
javiercruces@openclaw:~/kong2/echo-server$ docker compose up -d
[+] Running 1/1
 ✔ Container echo-server  Started              
```

We can confirm that the container is running with:

```bash
javiercruces@openclaw:~/kong2/echo-server$ docker ps
CONTAINER ID   IMAGE                        COMMAND                  CREATED              STATUS                    PORTS                                                                                                     NAMES
6f4af4c19ed9   hashicorp/http-echo:latest   "/http-echo"             About a minute ago   Up About a minute         5678/tcp                                                                                                  echo-server
1a53c0c225a2   kong/kong-gateway:3.15.0.0   "/entrypoint.sh kong…"   16 minutes ago       Up 16 minutes (healthy)   8001-8004/tcp, 0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp, 8443-8447/tcp                                 kong-dp
5ffe4b43af60   kong/kong-gateway:3.15.0.0   "/entrypoint.sh /bin…"   16 minutes ago       Up 16 minutes (healthy)   8000-8004/tcp, 8443/tcp, 8446-8447/tcp, 0.0.0.0:8444-8445->8444-8445/tcp, [::]:8444-8445->8444-8445/tcp   kong-cp
dce55af755c2   postgres:15                  "docker-entrypoint.s…"   16 minutes ago       Up 16 minutes (healthy)   5432/tcp                                                                                                  postgres
```

## Creating Kong Gateway Resources

With the full infrastructure deployed and the **Echo Server** running, the next step is to publish our first service through **Kong Gateway**.

To do that, we will use the **Admin API** of the **Control Plane**, where we will create the different resources that make up the Gateway configuration. Once stored, the Control Plane will automatically distribute that configuration to all **Data Planes** through the secure channel protected by **mTLS**, without any additional action required.

In this lab we will build the following logical architecture:

```text
                  Client
                     │
        GET http://echo.kong.javiercd.es:8000
                     │
                     ▼
              +----------------+
              |     Route      |
              | Host Routing   |
              +----------------+
                     │
                     ▼
       +----------------------------+
       | Key Authentication Plugin  |
       +----------------------------+
                     │
              Valid API Key
                     │
                     ▼
              +----------------+
              |    Service     |
              +----------------+
                     │
                     ▼
              +----------------+
              |  Echo Server   |
              +----------------+
```

By the end of this section we will have a fully functional API available at:

```text
http://echo.kong.javiercd.es:8000
```

and protected with **API Key** authentication.

---

### Configuring DNS resolution

The route will use the domain `echo.kong.javiercd.es`. Since this is a lab, we will add an entry to the `/etc/hosts` file so that this name resolves to our local machine.

```bash
echo "127.0.0.1 echo.kong.javiercd.es" | sudo tee -a /etc/hosts
```

We can verify that resolution works correctly by running:

```bash
ping -c 1 echo.kong.javiercd.es
```

---

### Creating the Service

The first resource we need to create is the **Service**.

A Service represents a backend service to which Kong will forward requests once they have been processed.

In our case, the backend will be the `echo-server` container, accessible through Docker's internal DNS.

```bash
curl -k -X POST https://localhost:8444/services \
    -H "Content-Type: application/json" \
    -d '{
        "name":"echo-service",
        "url":"http://echo-server:5678"
    }'
```

Once the Service is created, Kong already knows where it should send requests, even though there is still no rule allowing access to it.

---

### Creating the Route

A Route defines under which conditions a request will be sent to the Service.

In this lab we will use **Host Based Routing**, so any request directed to the domain `echo.kong.javiercd.es` will be forwarded to the Echo Server.

```bash
curl -k -X POST https://localhost:8444/routes \
    -H "Content-Type: application/json" \
    -d '{
        "name":"echo-route",
        "hosts":[
            "echo.kong.javiercd.es"
        ],
        "protocols":[
            "http"
        ],
        "service":{
            "name":"echo-service"
        }
    }'
```

From this point on, Kong can identify requests aimed at `echo.kong.javiercd.es` and associate them with the correct Service.

However, we still have not configured any authentication mechanism.

---

### Enabling the Key Authentication Plugin

The next step is to enable the **Key Authentication** plugin, which validates the API Key sent by clients.

In this lab the plugin will be applied only to the Service we just created.

```bash
curl -k -X POST https://localhost:8444/services/echo-service/plugins \
    -H "Content-Type: application/json" \
    -d '{
        "name":"key-auth"
    }'
```

From this point on, any request reaching the Service must include a valid API Key.

---

### Creating the Consumer

In Kong, a **Consumer** represents an application or client authorized to consume the published APIs.

We create a Consumer called `demo-client`.

```bash
curl -k -X POST https://localhost:8444/consumers \
    -H "Content-Type: application/json" \
    -d '{
        "username":"demo-client"
    }'
```

The Consumer does not grant access by itself. We still need to associate a credential with it.

---

### Creating the API Key

Finally, we will create an API Key for the Consumer.

```bash
curl -k -X POST https://localhost:8444/consumers/demo-client/key-auth \
    -H "Content-Type: application/json" \
    -d '{
        "key":"my-super-secret-api-key"
    }'
```

The Consumer now has a valid credential and can authenticate against Kong Gateway.

---

### Verifying the behavior

If we try to access the API without sending any API Key, we will get a **401 Unauthorized** response.

```bash
curl \
    -H "Host: echo.kong.javiercd.es" \
    http://localhost:8000
```

Response:

```bash
javiercruces@openclaw:~$ curl \
    -H "Host: echo.kong.javiercd.es" \
    http://localhost:8000
{
  "message":"No API key found in request",
  "request_id":"3c10804537b79b53fef5e3062d91185a"
}
```

Now we repeat the request, this time including the API Key.

```bash
javiercruces@openclaw:~$ curl \
    -H "Host: echo.kong.javiercd.es" \
    -H "apikey: my-super-secret-api-key" \
    http://localhost:8000
hello-world
```

The request will be accepted by Kong Gateway and automatically forwarded to the Echo Server, which will return a `hello world` in our case.

With this we have published our first API in Kong Gateway using a Hybrid architecture. The Control Plane has stored all the configuration and the Data Plane received it automatically through **mTLS**, allowing it to process requests without direct access to the database.

## Synchronization between Control Plane and Data Plane

Every time a resource is created, modified, or deleted through the **Admin API**, the **Control Plane** generates a new configuration and distributes it automatically to all connected **Data Planes**.

To visualize this process, we can increase the log verbosity by changing the following variable in `docker-compose.yaml`:

```yaml
KONG_LOG_LEVEL: debug
```

| Level | Description |
|--------|-------------|
| **debug** | Provides detailed information about Kong Gateway's internal behavior, including the execution loop of plugins and other components. It should only be used for troubleshooting, since keeping this level enabled continuously can generate a large amount of logs and consume significant disk space. |
| **info** / **notice** | Logs information about normal Kong Gateway operation. Most of these messages are informational and can be ignored during normal operation. `notice` is the default configured level. |
| **warn** | Logs abnormal behavior that does not cause requests to fail, but should be reviewed to avoid future incidents. |
| **error** | Logs errors that cause a request to fail, such as returning an **HTTP 500** status code. It is a good idea to monitor the frequency of these messages to detect system issues. |
| **crit** | Logs critical errors that affect Kong Gateway operation and may impact several clients or services. It is the highest severity level recommended for monitoring critical incidents. |

> **Note:** Kong Gateway uses **`notice`** by default, since it provides a good balance between the amount of information recorded and the volume of logs generated. In labs or troubleshooting sessions, it is recommended to use **`debug`**, while in production environments it is usually better to keep **`notice`** or **`warn`**.

Once the configuration has been applied, open two terminals and inspect the logs for both components.

### Control Plane logs

```bash
docker logs -f kong-cp
```

When a resource is created or modified, the Control Plane generates a new configuration and sends it to the Data Plane.

```text
172.19.0.1 - - [04/Jul/2026:10:08:47 +0000] "POST /services HTTP/2.0" 201

[clustering] config payload size 10634 bytes, configured limit cluster_max_payload 16777216 bytes

[clustering] sent config update to data plane
```

In this example we can see that:

- A new **Service** is created through the Admin API.
- The Control Plane generates a new configuration of **10,634 bytes**.
- Finally, that configuration is sent to the connected Data Plane.

### Data Plane logs

```bash
docker logs -f kong-dp
```

Next, the Data Plane receives the new configuration and applies it automatically.

```text
[clustering] received reconfigure frame from control plane

declarative reconfigure was started on worker #0

building a new router took 0 ms on worker #0

flushing caches as part of the reconfiguration

declarative reconfigure took 0 ms on worker #0

[clustering] sent ping frame to control plane with hash: d29974aa12e71779c93dec0596c56ce9
```

In this case we can confirm that:

- The Data Plane receives a **reconfiguration** instruction sent by the Control Plane.
- It rebuilds the internal router without restarting the process.
- It flushes its caches so the new configuration takes effect immediately.
- Finally, it sends a **ping** to the Control Plane with the new configuration **hash**, confirming that both nodes are synchronized.

This mechanism allows any change made in the Control Plane to propagate automatically to every connected Data Plane without interrupting the traffic they are processing.

## End of the Lab

And that brings us to the end of the lab.

As you have seen, the goal was not to build a production environment or use every feature Kong Gateway offers. The idea was much simpler: understand how to deploy a Hybrid environment and understand the role played by each of its components.

During the lab we deployed a Control Plane, a Data Plane, and a PostgreSQL database. We also published a very simple API, protected it with an API Key, and saw how any change made in the Control Plane is automatically synchronized with the Data Plane.

Although the example is very simple, the concepts we learned are the same ones you will find in much larger real-world deployments. Once you understand this foundation, it will be much easier to grasp the rest of the features Kong Gateway offers, such as authentication, load balancing, observability, or Kubernetes-based deployments.

I hope this lab helped you understand how Kong Gateway works internally and gives you a starting point for continuing to learn. In the next articles we will gradually extend this lab to discover new features and build an increasingly complete environment.

## Bibliography

- Kong Gateway Documentation - Hybrid Mode  
  https://developer.konghq.com/gateway/hybrid-mode/

- Kong Gateway Deployment Topologies  
  https://developer.konghq.com/gateway/deployment-topologies/

- Control Plane / Data Plane Communication  
  https://developer.konghq.com/gateway/cp-dp-communication/

- Kong Gateway Configuration Reference  
  https://developer.konghq.com/gateway/configuration/

- Kong Gateway Admin API Reference  
  https://developer.konghq.com/gateway/admin-api/

---

**Previous article:** [Introduction, architecture and planning for Kong Gateway](/en/posts/kong/01-introduccion-kong-gateway/01-introduccion-kong-gateway/)  
**Next article:** [Lab: Installing Kong in Traditional Mode](/en/posts/kong/03-instalacion-tradicional/03-instalacion-tradicional/)
