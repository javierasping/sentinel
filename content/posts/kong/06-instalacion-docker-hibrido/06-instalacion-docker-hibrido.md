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

### 1. Preparación del Entorno
Primero, crearemos el directorio de trabajo y la estructura de carpetas necesaria para la persistencia de datos y logs de Kong:

```bash
mkdir -p /home/javiercruces/kong/{config,data,logs,mocks,ssl}
cd /home/javiercruces/kong
```

### 2. Variables de Entorno
Creamos un archivo `.env` para centralizar las configuraciones críticas como contraseñas, versiones y el FQDN:

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

### 3. Configuración de la Red y Certificados SSL
Para el modo híbrido, Kong requiere mTLS entre el plano de control y el plano de datos. Generaremos los certificados necesarios para el cluster:

```bash
docker network create kong-edu-net || true
```

### 4. Despliegue con Docker Compose (Infraestructura Base)
Creamos el archivo `docker-compose.yaml` principal para desplegar PostgreSQL y los nodos de Kong.

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

### 5. Troubleshooting y Solución de Problemas (Troubleshooting & Issue Resolution)

Durante el despliegue, pueden surgir errores de permisos en los volúmenes montados por Docker. Si el contenedor `kong-cp` falla al iniciar debido a errores de escritura en `/var/log/kong` o `/etc/kong`, siga estos pasos:

**Corrección de Permisos (Permissions Fix):**
Ajuste los permisos de las carpetas en el host para que el usuario de Kong pueda escribir en ellas:

```bash
sudo chown -R 1000:1000 /home/javiercruces/kong/logs
sudo chmod -R 775 /home/javiercruces/kong/logs
```
*Nota: Si el error persiste, puede usar `KONG_USER=root` en el archivo `.env` como solución temporal rápida.*

**Creación de Red Externa:**
Asegúrese de que la red necesaria exista:

```bash
docker network create kong-edu-net || true
```

**Error de Esquema en Consumidores (Consumer Schema Error):**
Si al intentar crear un consumidor con campos `key` y `secret` recibe un error de "unknown field", es posible que la versión de Kong requiera el uso de `custom_id` para el identificador de la API Key:

```bash
# En lugar de "key", use "custom_id"
curl -i -X POST http://localhost:8001 \
  -d '{
    "name": "test-user",
    "custom_id": "secret-api-key-123"
  }'
```

### 6. Despliegue del Echo Server y Mocks
Creamos el directorio para los mocks y el archivo `docker-compose.yaml` específico para el Echo Server (Mockbin):

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

### 7. Configuración de Kong vía Admin API
Configuraremos el Echo Server como un Servicio, crearemos una Ruta y configuraremos la autenticación mediante la API de administración de Kong.

**Crear el Servicio (Echo Server):**
```bash
curl -i -X POST http://localhost:8001 \
  -d '{
    "name": "echo-server",
    "protocol": "http",
    "host": "mockbin.local",
    "port": 8080
  }'
```

**Crear la Ruta:**
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

**Crear el Consumidor (User) para la API Key:**
```bash
curl -i -X POST http://localhost:8001 \
  -d '{
    "name": "test-user",
    "custom_id": "secret-api-key-123"
  }'
```

### 8. Validación del Funcionamiento
Para validar que la configuración es correcta, realizaremos una petición sin llave (debería fallar con 401) y luego una con la llave correspondiente.

**Petición fallida (Sin API Key):**
```bash
curl -i http://kong.javiercd.es/echo
```
*Salida esperada:* `401 Unauthorized`

**Petición exitosa (Con API Key):**
```bash
curl -i -H "apikey: secret-api-key-123" http://kong.javiercd.es/echo
```
*Salida esperada:* `200 OK` con el cuerpo de respuesta del Mockbin.
