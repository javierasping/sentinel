---
title: "Instalación de Kong con Docker (modo híbrido)"
date: 2026-07-26T00:00:00+02:00
description: "Guía técnica y reproducible para instalar Kong Gateway en modo híbrido con Docker Compose, levantar un echo server y validarlo con autenticación por API key."
tags: [Kong, Docker, Docker Compose, Instalación, API Key]
hero: images/kong/docker-hybrid.png
weight: 2
---

## Introducción

En este artículo desplegaremos **Kong Gateway 3.10 open source** en **modo Hybrid** utilizando Docker Compose. Esta arquitectura, basada en la separación entre **Control Plane (CP)** y **Data Plane (DP)**, es una de las opciones recomendadas por Kong para entornos de API Gateway debido a su flexibilidad, escalabilidad y alta disponibilidad.

En un despliegue Hybrid, únicamente el **Control Plane** mantiene una conexión directa con la base de datos y es responsable de gestionar toda la configuración del gateway mediante la **Admin API** y **Kong Manager**. Por su parte, los **Data Planes** funcionan en modo *DB-less* y reciben automáticamente la configuración desde el Control Plane a través de un canal seguro protegido mediante **mTLS**. Esto permite que los Data Planes continúen procesando tráfico incluso si el Control Plane o la base de datos dejan de estar disponibles temporalmente.

Esta separación aporta importantes ventajas frente a una arquitectura tradicional. Reduce la carga sobre la base de datos, facilita el despliegue de múltiples Data Planes distribuidos entre diferentes centros de datos o regiones, mejora la seguridad al aislar el plano de gestión del plano de datos y simplifica la administración centralizada de toda la plataforma.

A lo largo de este laboratorio construiremos una infraestructura completa desde cero utilizando Docker Compose. Desplegaremos PostgreSQL, un Control Plane y un Data Plane, analizaremos el propósito de cada componente y comprenderemos cómo se comunican entre sí. Una vez que la infraestructura esté funcionando, publicaremos nuestro primer servicio a través de Kong utilizando un **Echo Server**, creando paso a paso los recursos fundamentales del gateway: **Services**, **Routes**, **Plugins**, **Consumers** y sus credenciales.

El objetivo de este artículo no es únicamente conseguir que Kong funcione, sino comprender cómo trabaja internamente una arquitectura Hybrid y por qué es el modelo de despliegue utilizado por **Konnect** y por la mayoría de implementaciones empresariales de Kong Gateway. Al finalizar el laboratorio no solo habrás desplegado una plataforma completamente funcional, sino que también entenderás el flujo completo de una petición desde que llega al proxy hasta que alcanza el servicio backend, así como el proceso mediante el cual el Control Plane distribuye la configuración a todos los Data Planes del clúster.

## ¿Qué es el modo Hybrid de Kong Gateway?

El **modo Hybrid** es un modelo de despliegue de Kong Gateway que separa las responsabilidades de administración y procesamiento del tráfico en dos tipos de nodos diferentes: **Control Plane (CP)** y **Data Plane (DP)**.

A diferencia de un despliegue tradicional, donde todas las instancias de Kong mantienen una conexión directa con la base de datos, en una arquitectura Hybrid únicamente los nodos que desempeñan el rol de **Control Plane** acceden a PostgreSQL. Los **Data Planes** funcionan en modo **DB-less** y reciben toda su configuración desde el Control Plane mediante un canal seguro protegido por **mTLS**.

Cada vez que un administrador realiza un cambio a través de la **Admin API** o de **Kong Manager**, el Control Plane almacena la nueva configuración en la base de datos, genera una representación declarativa de la misma y la distribuye automáticamente a todos los Data Planes conectados.

Este modelo permite desacoplar completamente la administración de la plataforma del procesamiento de las peticiones, facilitando el escalado independiente de ambos componentes y reduciendo considerablemente la carga sobre la base de datos.

En la siguiente figura puede observarse la arquitectura general de un despliegue Hybrid.

```text
                     PostgreSQL
                          │
                          │
                  Configuración
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
                      Clientes
```

---

### ¿Qué es un Control Plane?

El **Control Plane** es el componente encargado de la administración de Kong Gateway.

Todas las tareas relacionadas con la gestión de la plataforma se realizan desde este nodo, incluyendo la creación y modificación de **Services**, **Routes**, **Plugins**, **Consumers**, certificados, autenticación y cualquier otro recurso soportado por Kong Gateway.

El Control Plane también expone dos interfaces fundamentales:

- **Admin API**, utilizada para administrar Kong de forma programática.
- **Kong Manager**, la interfaz gráfica para gestionar la plataforma.

A diferencia del Data Plane, el Control Plane mantiene una conexión permanente con PostgreSQL, donde almacena toda la configuración del gateway.

Cada vez que dicha configuración cambia, el Control Plane genera automáticamente una nueva configuración declarativa y la distribuye a todos los Data Planes conectados mediante un canal seguro basado en **mTLS**.

Es importante destacar que el Control Plane **no procesa tráfico de clientes**. Su única responsabilidad es administrar la configuración y sincronizarla con los Data Planes.

---

### ¿Qué es un Data Plane?

El **Data Plane** es el componente encargado de recibir y procesar las peticiones de los clientes.

Cada solicitud HTTP o HTTPS que llega a Kong atraviesa uno de los Data Planes, donde se ejecuta todo el pipeline del gateway:

1. Identificación de la Route correspondiente.
2. Resolución del Service asociado.
3. Ejecución de los Plugins configurados.
4. Balanceo de carga (si procede).
5. Envío de la petición al backend.

A diferencia del Control Plane, el Data Plane **no tiene acceso directo a PostgreSQL**. Toda la configuración que necesita para funcionar la recibe desde el Control Plane.

Además, cada Data Plane almacena localmente una copia de la última configuración recibida en una base de datos **LMDB** (`dbless.lmdb`). Gracias a este mecanismo, el gateway puede continuar procesando tráfico incluso si el Control Plane o la base de datos dejan de estar disponibles temporalmente.

Cuando el Control Plane vuelve a estar operativo, los Data Planes restablecen automáticamente la comunicación y sincronizan cualquier cambio pendiente.

---

### Ventajas del modo Hybrid

El modo Hybrid aporta numerosas ventajas frente a una arquitectura tradicional y es el modelo recomendado por Kong para la mayoría de despliegues empresariales.

Entre sus principales beneficios destacan:

- **Escalabilidad independiente.** Es posible aumentar el número de Data Planes sin modificar la infraestructura de administración ni la base de datos.

- **Alta disponibilidad.** Los Data Planes continúan sirviendo tráfico utilizando la última configuración recibida incluso cuando el Control Plane o PostgreSQL no están disponibles.

- **Menor carga sobre la base de datos.** Solo los Control Planes mantienen conexiones con PostgreSQL, reduciendo significativamente el número de accesos concurrentes.

- **Mayor seguridad.** Los Data Planes no necesitan acceso a la base de datos ni exponen interfaces de administración, reduciendo la superficie de ataque.

- **Administración centralizada.** Toda la configuración se realiza desde uno o varios Control Planes, simplificando la gestión de grandes despliegues distribuidos.

- **Despliegues geográficamente distribuidos.** Es posible desplegar grupos de Data Planes en distintas regiones o centros de datos sin necesidad de disponer de una base de datos local en cada ubicación.

- **Compatibilidad con Konnect.** La arquitectura utilizada por Kong Konnect también está basada en el modelo Control Plane / Data Plane, por lo que aprender este modo de despliegue facilita la transición hacia entornos gestionados por Kong.

## Arquitectura del laboratorio

Para comprender el funcionamiento de Kong Gateway en modo **Hybrid**, construiremos un entorno completo utilizando Docker Compose. Aunque se trata de un laboratorio ejecutado sobre una única máquina, la arquitectura es equivalente a la utilizada en numerosos despliegues empresariales, donde el **Control Plane** y los **Data Planes** se ejecutan en servidores o centros de datos diferentes.

La infraestructura estará compuesta por cuatro servicios principales:

- Un servidor **PostgreSQL**, encargado de almacenar la configuración del gateway.
- Un **Control Plane**, responsable de administrar la configuración de Kong Gateway.
- Un **Data Plane**, encargado de procesar el tráfico de los clientes.
- Un **Echo Server**, que actuará como backend de pruebas para validar el funcionamiento del gateway.

El siguiente diagrama muestra la arquitectura que construiremos durante este laboratorio.

```text
                           Docker Host
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│  PostgreSQL                                                        │
│      ▲                                                             │
│      │                                                             │
│      │ Configuración                                               │
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

                 Cliente
                    │
                    ▼
             http://localhost:8000
```

---

## Requisitos previos

Antes de comenzar este laboratorio es recomendable disponer de los siguientes conocimientos y herramientas.

### Conocimientos recomendados

- Conceptos básicos de Docker y Docker Compose.
- Funcionamiento básico de redes TCP/IP.
- Uso de la terminal de Linux.
- Conocimientos básicos sobre APIs REST y HTTP.

### Software necesario

- Docker Engine 28 o superior.
- Docker Compose v2.
- Kong Gateway 3.10 open source.
- PostgreSQL.
- Curl.
- Un navegador web para acceder a Kong Manager.

### Recursos del laboratorio

Para realizar este laboratorio utilizaremos:

- Un único servidor Linux.
- Acceso a Internet para descargar las imágenes Docker.
- Al menos 4 GB de memoria RAM disponibles.
- Aproximadamente 5 GB de espacio libre en disco.

## Preparación del entorno

Antes de desplegar Kong Gateway es necesario preparar el entorno de trabajo. En esta sección crearemos la estructura de directorios que utilizaremos durante el laboratorio y definiremos las variables de entorno que centralizarán toda la configuración del despliegue.

Aunque se trata de un laboratorio ejecutado sobre una única máquina, organizaremos los recursos siguiendo una estructura similar a la que podría encontrarse en un entorno de producción. Esto facilitará la comprensión de la arquitectura y permitirá ampliar el laboratorio en los siguientes artículos de la serie.

Al finalizar esta sección tendremos preparado todo lo necesario para desplegar Kong Gateway mediante Docker Compose.

### La red Docker

Todos los contenedores del laboratorio compartirán una red Docker denominada **kong-net**.

Esta red permitirá que los distintos servicios puedan comunicarse entre sí utilizando su nombre de host, sin necesidad de conocer sus direcciones IP. Por ejemplo, el Control Plane podrá conectarse a PostgreSQL utilizando simplemente el hostname `postgres`, mientras que el Data Plane podrá establecer la comunicación con el Control Plane utilizando el hostname `kong-cp`.

A diferencia de otros laboratorios donde la red debe crearse manualmente, en este caso será el propio **Docker Compose** quien la cree automáticamente durante el despliegue de la infraestructura.

En el archivo `docker-compose.yaml` definiremos la red.

Cuando ejecutemos `docker compose up`, Docker detectará que la red no existe y la creará automáticamente antes de iniciar el resto de los servicios.

---

## Configuración de certificados para el Proxy

Además de los certificados utilizados para proteger la comunicación entre el **Control Plane** y el **Data Plane**, necesitaremos un segundo certificado que será presentado por Kong Gateway cuando los clientes accedan al Proxy mediante HTTPS.

En este laboratorio utilizaremos un certificado **autofirmado** para el dominio:

```text
*.kong.javiercd.es
```

Este certificado únicamente será utilizado para cifrar las conexiones HTTPS establecidas entre los clientes y el Proxy de Kong Gateway.

> **Nota**
>
> Al tratarse de un certificado autofirmado, los navegadores mostrarán una advertencia indicando que la entidad emisora no es de confianza. Esto es completamente normal en un entorno de laboratorio.

### Generación del certificado

Vamos a generar el certificado en la carpeta donde hemos creado los ficheros del escenario. Para ello, crearemos un directorio `ssl`:

```bash
mkdir -p kong/ssl
```

> **Nota:** Los contenedores de Kong se ejecutan con el usuario `kong` (UID/GID `1001` en la imagen oficial `kong/kong-gateway:3.10`). Como el directorio `ssl` se monta como volumen dentro del contenedor, es necesario asignar la propiedad de los certificados a ese usuario para que Kong pueda leerlos y, si es necesario, generar o actualizar los certificados del clúster durante el arranque.
>
> ```bash
> sudo chown -R 1001:1001 ssl
> ```
>
> Si utilizas una versión diferente de la imagen de Kong, puedes comprobar el UID/GID del usuario `kong` con:
>
> ```bash
> docker run --rm --entrypoint id kong/kong-gateway:<VERSION> kong
> ```

Creamos el certificado y la clave privada ejecutando el siguiente comando:

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

Una vez finalizado el proceso, se habrán generado los siguientes archivos:

```bash
javiercruces@kong:~/kong$ ls -l ssl/
total 8
-rw-rw-r-- 1 1001 1001 2163 Jul  8 21:47 proxy.crt
-rw------- 1 1001 1001 3268 Jul  8 21:47 proxy.key
```

Posteriormente, configuraremos el Data Plane para utilizar estos certificados mediante las siguientes variables:

```yaml
KONG_SSL_CERT: "/etc/kong/ssl/proxy.crt"
KONG_SSL_CERT_KEY: "/etc/kong/ssl/proxy.key"
```

A partir de este momento, cualquier cliente que establezca una conexión HTTPS con Kong Gateway recibirá este certificado durante el proceso de negociación TLS.

En un entorno de producción se recomienda utilizar certificados emitidos por una Autoridad de Certificación (CA) de confianza, como Let's Encrypt o una PKI corporativa. Sin embargo, para un laboratorio, un certificado autofirmado es suficiente para comprender el funcionamiento del Proxy HTTPS de Kong Gateway.

### Variables de entorno

Para evitar duplicar información dentro del `docker-compose.yaml`, almacenaremos los parámetros de configuración en un archivo `.env`.

Este fichero centralizará la configuración del laboratorio, incluyendo:

- La versión de Kong Gateway.
- Las credenciales de PostgreSQL.
- El nombre de la base de datos.
- El FQDN utilizado por Kong Manager.
- El usuario con el que se ejecutará Kong.

Creamos el archivo `.env` con el siguiente contenido:

```python
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

# Certificados utilizados por el Proxy HTTPS
KONG_SSL_CERT=/etc/kong/ssl/proxy.crt
KONG_SSL_CERT_KEY=/etc/kong/ssl/proxy.key

# Certificados utilizados para la comunicación CP <-> DP
KONG_CLUSTER_CERT=/etc/kong/ssl/cluster.crt
KONG_CLUSTER_CERT_KEY=/etc/kong/ssl/cluster.key

KONG_ADMIN_GUI_URL=https://$FQDN:8445
KONG_ADMIN_GUI_API_URL=https://$FQDN:8444

KONG_USER=kong
```

Docker Compose cargará automáticamente este archivo durante el despliegue, sustituyendo las referencias `${VARIABLE}` definidas en el `docker-compose.yaml`.

### Creación del Docker Compose

Ahora, en el directorio que hemos creado antes, crearemos este fichero `docker-compose.yaml`:

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
    image: kong/kong-gateway:${KONG_GW_VERSION:-3.10}
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
    image: kong/kong-gateway:${KONG_GW_VERSION:-3.10}
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
      KONG_NGINX_EVENTS_WORKER_CONNECTIONS: 8192
      KONG_LUA_SSL_TRUSTED_CERTIFICATE: "/etc/kong/ssl/cluster.crt,system"
      KONG_LOG_LEVEL: "info"
      KONG_ENFORCE_RBAC: off
  kong-dp:
    image: kong/kong-gateway:${KONG_GW_VERSION:-3.10}
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
      KONG_NGINX_EVENTS_WORKER_CONNECTIONS: 8192
```

## Despliegue de la infraestructura

Una vez preparada toda la configuración, ya podemos desplegar la infraestructura utilizando Docker Compose.

Ejecutamos el siguiente comando desde el directorio del laboratorio:

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

Durante este proceso Docker Compose realiza automáticamente las siguientes acciones:

- Crea la red `kong-net`, utilizada para la comunicación entre todos los contenedores.
- Crea el volumen persistente donde PostgreSQL almacenará los datos.
- Inicia la base de datos PostgreSQL y espera a que esté disponible.
- Ejecuta el contenedor `kong-migrations-bootstrap`, encargado de inicializar el esquema de la base de datos de Kong Gateway.
- Inicia el **Control Plane** (`kong-cp`).
- Inicia el **Data Plane** (`kong-dp`), que establecerá automáticamente una conexión segura con el Control Plane mediante **mTLS**.

> **Nota**
>
> Es completamente normal que el contenedor `kong-migrations-bootstrap` finalice con estado **Exited (0)**. Su única función es ejecutar las migraciones iniciales de la base de datos y finalizar correctamente una vez completadas.

A continuación, verificamos que todos los contenedores se han desplegado correctamente:

```bash
javiercruces@kong:~/kong$ docker ps -a
CONTAINER ID   IMAGE                        COMMAND                  CREATED         STATUS                     PORTS                                                                                                     NAMES
1a53c0c225a2   kong/kong-gateway:3.10   "/entrypoint.sh kong…"   2 minutes ago   Up 2 minutes (healthy)     8001-8004/tcp, 0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp, 8443-8447/tcp                                 kong-dp
5ffe4b43af60   kong/kong-gateway:3.10   "/entrypoint.sh /bin…"   2 minutes ago   Up 2 minutes (healthy)     8000-8004/tcp, 8443/tcp, 8446-8447/tcp, 0.0.0.0:8444-8445->8444-8445/tcp, [::]:8444-8445->8444-8445/tcp   kong-cp
705169cc65aa   kong/kong-gateway:3.10   "/entrypoint.sh kong…"   2 minutes ago   Exited (0) 2 minutes ago                                                                                                             kong-migrations-bootstrap
dce55af755c2   postgres:15                  "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes (healthy)     5432/tcp                                                                                                  postgres
```

Si todo ha ido correctamente, observaremos que:

- **PostgreSQL** se encuentra en estado **healthy**.
- El **Control Plane** (`kong-cp`) está en ejecución y preparado para administrar la configuración del clúster.
- El **Data Plane** (`kong-dp`) está en ejecución y conectado al Control Plane.
- El contenedor **kong-migrations-bootstrap** ha finalizado correctamente con estado **Exited (0)**, indicando que las migraciones de la base de datos se han ejecutado con éxito.

Con la infraestructura ya desplegada, el siguiente paso será comprobar que el **Control Plane** y el **Data Plane** se están comunicando correctamente antes de comenzar a publicar servicios a través de Kong Gateway.

## Despliegue del Echo Server

Una vez desplegada la infraestructura de Kong Gateway, el siguiente paso será disponer de un servicio backend al que reenviar las peticiones.

Para este laboratorio utilizaremos un **Echo Server**, una aplicación muy sencilla cuya única función es devolver al cliente toda la información de la petición HTTP recibida. Gracias a ello podremos verificar fácilmente que Kong está encaminando correctamente las solicitudes y observar cómo afectan posteriormente los distintos plugins, transformaciones de cabeceras o mecanismos de autenticación que iremos configurando.

### ¿Por qué utilizar un Echo Server?

El objetivo de este laboratorio es aprender el funcionamiento de Kong Gateway, no desarrollar una aplicación backend. Utilizando un Echo Server eliminamos cualquier complejidad innecesaria y podremos centrarnos exclusivamente en el comportamiento del API Gateway.

Además, al devolver toda la información de la petición recibida, podremos comprobar fácilmente:

- La URL utilizada.
- El método HTTP empleado.
- Las cabeceras enviadas por el cliente.
- Las cabeceras añadidas automáticamente por Kong.
- Los parámetros de la petición.
- El cuerpo (Body) recibido.

### Creación del directorio

Creamos un directorio independiente para el Echo Server:

```bash
mkdir echo-server
cd echo-server
```

### Creación del Docker Compose

Dentro del directorio `echo-server` creamos el fichero `docker-compose.yaml`:

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

Como puede observarse, el contenedor se conecta a la misma red Docker (`kong-net`) utilizada por Kong Gateway.

Esto permite que Docker proporcione resolución DNS automáticamente entre los contenedores pertenecientes a la misma red. Gracias a ello, Kong podrá acceder al backend utilizando simplemente el nombre del servicio, sin necesidad de conocer su dirección IP.

> **Nota**
>
> En este laboratorio el Echo Server **no expone ningún puerto al host**. Únicamente será accesible desde la red interna `kong-net`, donde también se encuentran el Control Plane y el Data Plane de Kong Gateway. Esta arquitectura se asemeja a un entorno de producción, donde normalmente los servicios backend permanecen aislados y únicamente el API Gateway recibe conexiones desde el exterior.

### Despliegue del servicio

Una vez creado el fichero, iniciamos el contenedor:

```bash
javiercruces@openclaw:~/kong2/echo-server$ docker compose up -d
[+] Running 1/1
 ✔ Container echo-server  Started              
```

Podemos comprobar que el contenedor se encuentra en ejecución mediante:

```bash
javiercruces@openclaw:~/kong2/echo-server$ docker ps
CONTAINER ID   IMAGE                        COMMAND                  CREATED              STATUS                    PORTS                                                                                                     NAMES
6f4af4c19ed9   hashicorp/http-echo:latest   "/http-echo"             About a minute ago   Up About a minute         5678/tcp                                                                                                  echo-server
1a53c0c225a2   kong/kong-gateway:3.10   "/entrypoint.sh kong…"   16 minutes ago       Up 16 minutes (healthy)   8001-8004/tcp, 0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp, 8443-8447/tcp                                 kong-dp
5ffe4b43af60   kong/kong-gateway:3.10   "/entrypoint.sh /bin…"   16 minutes ago       Up 16 minutes (healthy)   8000-8004/tcp, 8443/tcp, 8446-8447/tcp, 0.0.0.0:8444-8445->8444-8445/tcp, [::]:8444-8445->8444-8445/tcp   kong-cp
dce55af755c2   postgres:15                  "docker-entrypoint.s…"   16 minutes ago       Up 16 minutes (healthy)   5432/tcp                                                                                                  postgres
```

## Creación de los recursos de Kong Gateway

Con toda la infraestructura ya desplegada y el **Echo Server** en funcionamiento, el siguiente paso consiste en publicar nuestro primer servicio a través de **Kong Gateway**.

Para ello utilizaremos la **Admin API** del **Control Plane**, donde iremos creando los distintos recursos que forman parte de la configuración del Gateway. Una vez almacenados, el Control Plane distribuirá automáticamente esta configuración a todos los **Data Planes** mediante el canal seguro protegido con **mTLS**, sin necesidad de realizar ninguna acción adicional.

En este laboratorio construiremos la siguiente arquitectura lógica:

```text
                  Cliente
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
              API Key válida
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

Al finalizar este apartado dispondremos de una API completamente funcional accesible mediante el dominio:

```text
http://echo.kong.javiercd.es:8000
```

y protegida mediante autenticación basada en **API Keys**.

---

### Configuración de la resolución DNS

La ruta utilizará el dominio `echo.kong.javiercd.es`. Como se trata de un laboratorio, añadiremos una entrada al fichero `/etc/hosts` para que dicho nombre resuelva a nuestro equipo local.

```bash
echo "127.0.0.1 echo.kong.javiercd.es" | sudo tee -a /etc/hosts
```

Podemos comprobar que la resolución funciona correctamente ejecutando:

```bash
ping -c 1 echo.kong.javiercd.es
```

---

### Creación del Service

El primer recurso que debemos crear es el **Service**.

Un Service representa un servicio backend al que Kong reenviará las peticiones una vez hayan sido procesadas.

En nuestro caso el backend será el contenedor `echo-server`, accesible mediante el DNS interno de Docker.

```bash
curl -k -X POST https://localhost:8444/services \
    -H "Content-Type: application/json" \
    -d '{
        "name":"echo-service",
        "url":"http://echo-server:5678"
    }'
```

Una vez creado el Service, Kong ya conoce dónde debe enviar las peticiones, aunque todavía no existe ninguna regla que permita acceder a él.

---

### Creación de la Route

Una Route define bajo qué condiciones una petición será enviada al Service.

En este laboratorio utilizaremos **Host Based Routing**, de forma que cualquier petición dirigida al dominio `echo.kong.javiercd.es` será reenviada al Echo Server.

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

A partir de este momento Kong ya es capaz de identificar las peticiones destinadas al dominio `echo.kong.javiercd.es` y asociarlas con el Service correspondiente.

Sin embargo, todavía no hemos configurado ningún mecanismo de autenticación.

---

### Habilitación del plugin Key Authentication

El siguiente paso consiste en habilitar el plugin **Key Authentication**, encargado de validar la API Key enviada por los clientes.

En este laboratorio el plugin se aplicará únicamente sobre el Service que acabamos de crear.

```bash
curl -k -X POST https://localhost:8444/services/echo-service/plugins \
    -H "Content-Type: application/json" \
    -d '{
        "name":"key-auth"
    }'
```

A partir de este momento cualquier petición que llegue al Service deberá incluir una API Key válida.

---

### Creación del Consumer

En Kong, un **Consumer** representa una aplicación o cliente autorizado para consumir las APIs publicadas.

Creamos un Consumer llamado `demo-client`.

```bash
curl -k -X POST https://localhost:8444/consumers \
    -H "Content-Type: application/json" \
    -d '{
        "username":"demo-client"
    }'
```

El Consumer no concede acceso por sí mismo. Será necesario asociarle una credencial.

---

### Creación de la API Key

Por último, crearemos una API Key para el Consumer.

```bash
curl -k -X POST https://localhost:8444/consumers/demo-client/key-auth \
    -H "Content-Type: application/json" \
    -d '{
        "key":"my-super-secret-api-key"
    }'
```

El Consumer ya dispone de una credencial válida y podrá autenticarse frente a Kong Gateway.

---

### Verificación del funcionamiento

Si intentamos acceder a la API sin enviar ninguna API Key obtendremos una respuesta **401 Unauthorized**.

```bash
curl \
    -H "Host: echo.kong.javiercd.es" \
    http://localhost:8000
```

Respuesta:

```bash
javiercruces@openclaw:~$ curl \
    -H "Host: echo.kong.javiercd.es" \
    http://localhost:8000
{
  "message":"No API key found in request",
  "request_id":"3c10804537b79b53fef5e3062d91185a"
}
```

Ahora realizamos la misma petición incluyendo la API Key.

```bash
javiercruces@openclaw:~$ curl \
    -H "Host: echo.kong.javiercd.es" \
    -H "apikey: my-super-secret-api-key" \
    http://localhost:8000
hello-world
```

La petición será aceptada por Kong Gateway y reenviada automáticamente al Echo Server, que devolverá en nuestro caso un `hello-world`.

Con esto hemos publicado nuestra primera API en Kong Gateway utilizando una arquitectura Hybrid. El Control Plane ha almacenado toda la configuración y el Data Plane la ha recibido automáticamente mediante **mTLS**, siendo capaz de procesar las peticiones sin necesidad de acceder directamente a la base de datos.

## Sincronización entre Control Plane y Data Plane

Cada vez que se crea, modifica o elimina un recurso mediante la **Admin API**, el **Control Plane** genera una nueva configuración y la distribuye automáticamente a todos los **Data Planes** conectados.

Para visualizar este proceso podemos aumentar el nivel de detalle de los logs modificando la siguiente variable del `docker-compose.yaml`:

```yaml
KONG_LOG_LEVEL: debug
```

| Nivel | Descripción |
|--------|-------------|
| **debug** | Proporciona información detallada sobre el funcionamiento interno de Kong Gateway, incluyendo el bucle de ejecución de los plugins y del resto de componentes. Debe utilizarse únicamente durante tareas de depuración, ya que mantener este nivel de forma continuada puede generar un gran volumen de logs y un consumo elevado de espacio en disco. |
| **info** / **notice** | Registra información sobre el funcionamiento normal de Kong Gateway. La mayoría de estos mensajes son informativos y pueden ignorarse durante la operación habitual. `notice` es el nivel configurado por defecto. |
| **warn** | Registra comportamientos anómalos que no provocan el rechazo de las peticiones, pero que deberían revisarse para evitar posibles incidencias futuras. |
| **error** | Registra errores que provocan el fallo de una petición, como la devolución de un código **HTTP 500**. Es recomendable monitorizar la frecuencia de estos mensajes para detectar problemas en el sistema. |
| **crit** | Registra errores críticos que afectan al funcionamiento de Kong Gateway y pueden impactar a varios clientes o servicios. Es el nivel de mayor severidad recomendado para la monitorización de incidencias críticas. |

> **Nota:** Kong Gateway utiliza por defecto el nivel **`notice`**, ya que ofrece un equilibrio adecuado entre la cantidad de información registrada y el volumen de logs generado. En laboratorios o durante tareas de depuración es recomendable utilizar **`debug`**, mientras que en entornos de producción suele ser preferible mantener los niveles **`notice`** o **`warn`**.

Una vez aplicada la configuración, abrimos dos terminales y visualizamos los logs de ambos componentes.

### Logs del Control Plane

```bash
docker logs -f kong-cp
```

Al crear o modificar un recurso, el Control Plane genera una nueva configuración y la envía al Data Plane.

```text
172.19.0.1 - - [04/Jul/2026:10:08:47 +0000] "POST /services HTTP/2.0" 201

[clustering] config payload size 10634 bytes, configured limit cluster_max_payload 16777216 bytes

[clustering] sent config update to data plane
```

En este ejemplo podemos observar cómo:

- Se crea un nuevo **Service** mediante la Admin API.
- El Control Plane genera una nueva configuración de **10.634 bytes**.
- Finalmente, dicha configuración es enviada al Data Plane conectado.

### Logs del Data Plane

```bash
docker logs -f kong-dp
```

A continuación, el Data Plane recibe la nueva configuración y la aplica automáticamente.

```text
[clustering] received reconfigure frame from control plane

declarative reconfigure was started on worker #0

building a new router took 0 ms on worker #0

flushing caches as part of the reconfiguration

declarative reconfigure took 0 ms on worker #0

[clustering] sent ping frame to control plane with hash: d29974aa12e71779c93dec0596c56ce9
```

En este caso podemos comprobar que:

- El Data Plane recibe una orden de **reconfiguración** enviada por el Control Plane.
- Reconstruye el router interno sin necesidad de reiniciar el proceso.
- Limpia las cachés para que la nueva configuración entre en funcionamiento inmediatamente.
- Finalmente envía un **ping** al Control Plane indicando el nuevo **hash** de configuración, confirmando que ambos nodos se encuentran sincronizados.

Este mecanismo permite que cualquier cambio realizado en el Control Plane se propague automáticamente a todos los Data Planes conectados, sin interrumpir el tráfico que están procesando.

## Fin del laboratorio

Y con esto llegamos al final del laboratorio.

Como has podido comprobar, el objetivo no era montar un entorno de producción ni utilizar todas las funcionalidades que ofrece Kong Gateway. La idea era mucho más sencilla: comprender cómo se despliega un entorno Hybrid y entender el papel que desempeña cada uno de sus componentes.

Durante el laboratorio hemos desplegado un Control Plane, un Data Plane y una base de datos PostgreSQL. También hemos publicado una API muy sencilla, la hemos protegido mediante una API Key y hemos visto cómo cualquier cambio realizado en el Control Plane se sincroniza automáticamente con el Data Plane.

Aunque el ejemplo es muy simple, los conceptos que hemos aprendido son los mismos que encontrarás en despliegues reales mucho más grandes. Una vez entiendas esta base, te resultará mucho más fácil comprender el resto de funcionalidades que ofrece Kong Gateway, como la autenticación, el balanceo de carga, la observabilidad o los despliegues sobre Kubernetes.

Espero que este laboratorio te haya ayudado a entender cómo funciona Kong Gateway por dentro y que te sirva como punto de partida para seguir aprendiendo. En los próximos artículos iremos ampliando poco a poco este laboratorio para descubrir nuevas funcionalidades y construir un entorno cada vez más completo.

## Bibliografía

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

**Artículo anterior:** [Introducción, arquitectura y planificación de Kong Gateway](/posts/kong/01-introduccion-kong-gateway/01-introduccion-kong-gateway/)  
**Siguiente artículo:** [Laboratorio: instalación de Kong en modo tradicional](/posts/kong/03-instalacion-tradicional/03-instalacion-tradicional/)
