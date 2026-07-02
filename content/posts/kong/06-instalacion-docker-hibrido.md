---
title: "Laboratorio: Instalación de Kong con Docker (Modo Híbrido)"
date: 2026-07-02T14:25:00+00:00
description: Guía práctica paso a paso para desplegar Kong Gateway en modo híbrido utilizando Docker Compose.
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

Utilizaremos un archivo `docker-compose.yaml` que defina los servicios. Puntos clave de la configuración:

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

En este punto es normal recibir un `404 Not Found`, ya que el Gateway está vivo pero aún no hemos definido ninguna ruta ni servicio.

---

**Artículo anterior:** [Gestión de la Configuración de Kong Gateway](/posts/kong/05-configuracion-kong-gateway)  
**Siguiente artículo:** [Gestión de Licencias en Kong Enterprise](/posts/kong/07-gestion-licencias-enterprise)
