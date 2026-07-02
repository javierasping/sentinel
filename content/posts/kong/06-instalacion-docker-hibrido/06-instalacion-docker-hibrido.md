---
title: "Laboratorio: Instalación de Kong con Docker (Modo Híbrido)"
date: 2026-07-02T14:25:00+00:00
description: "Guía práctica paso a paso para desplegar Kong Gateway en modo híbrido utilizando Docker Compose."
tags: [Kong, Docker, Docker Compose, Instalación]
hero: images/kong/06-docker/hero.png
---

El despliegue en modo híbrido es uno de los más utilizados en producción debido a su capacidad de escalar la capa de datos independientemente de la de gestión. En este artículo, realizaremos una instalación práctica utilizando Docker Compose.

## Arquitectura del Laboratorio

Para este despliegue, utilizaremos una estructura de contenedores que incluye:
- **PostgreSQL:** Almacenamiento de la configuración para el Control Plane.
- **Kong Control Plane (kong-cp):** Nodo de gestión y API de administración.
- **Kong Data Plane (kong-dp):** Nodo encargado de procesar el tráfico del proxy.
- **Mockbin:** Un servicio backend externo para realizar pruebas de routing.

## Paso a Paso de la Instalación

### 1. Preparación de la Red
Primero, debemos asegurarnos de tener una red externa creada para que los contenedores se comuniquen entre sí:

```bash
docker network create kong-edu-net
```

### 2. Configuración de Certificados SSL
En el modo híbrido, el CP y el DP deben comunicarse de forma segura mediante mTLS. Para ello, necesitamos generar certificados de cluster. 

Si no disponemos de ellos, el nodo `kong-cp` puede generarlos automáticamente al iniciar mediante el comando:
`kong hybrid gen_cert /etc/kong/ssl/cluster.crt /etc/kong/ssl/cluster.key`

### 3. Despliegue con Docker Compose

Utilizaremos un archivo `docker-compose.yaml` para definir los servicios. A continuación, presentamos el contenido del fichero base necesario para este despliegue:

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

Puntos clave de la configuración:


- **Para el Control Plane (`kong-cp`):** 
  - Definimos `KONG_ROLE: control_plane`.
  - Configuramos los puertos de la Admin API (8001) y el Manager (8002).
  - Vinculamos la base de datos PostgreSQL.

- **Para el Data Plane (`kong-dp`):**
  - Definimos `KONG_ROLE: data_plane`.
  - Configuramos `KONG_DATABASE: off` (ya que el DP no accede a la BD).
  - Definimos `KONG_CLUSTER_CONTROL_PLANE: kong-cp:8005` para que sepa dónde buscar la configuración.
  - Abrimos el puerto del Proxy (8000).

Para levantar la infraestructura:

```bash
docker compose up -d
```

### 4. Verificación del Despliegue

Una vez levantados los contenedores, podemos comprobar que el Gateway está operativo consultando la Admin API:

```bash
curl -i http://localhost:8001/
```

Si recibimos un `200 OK`, el Control Plane está funcionando. Para verificar el Proxy (Data Plane), podemos intentar acceder al puerto 8000:

```bash
curl -i http://localhost:8000/
```



### 5. Despliegue de servicios de prueba (Mockbin)

Para verificar que el Gateway procesa el tráfico correctamente, desplegaremos un servicio de prueba llamado Mockbin. Este servicio actúa como un backend simple que devuelve la información de las peticiones recibidas.

Utilizaremos el siguiente archivo `docker-compose.yaml` específico para Mockbin:

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

Para desplegarlo, ejecutamos:

```bash
docker compose -f mockbin/docker-compose.yaml up -d
```

---

**Artículo anterior:** [Gestión de la Configuración de Kong Gateway](/posts/kong/05-configuracion-kong-gateway)  
**Siguiente artículo:** [Gestión de Licencias en Kong Enterprise](/posts/kong/07-gestion-licencias-enterprise)
