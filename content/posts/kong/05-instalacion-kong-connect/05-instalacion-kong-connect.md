---
title: "Laboratorio técnico: instalación de Kong en Konnect"
date: 2026-07-02T14:40:00+00:00
description: "Aprende a configurar la lógica de routing de Kong creando tus primeros Servicios y Rutas a través de la Admin API."
tags: [Kong, API Routing, Admin API, Microservicios]
hero: images/kong/09-routing/hero.png
---

Una vez que el Gateway está instalado y funcionando, el siguiente paso es hacer que el tráfico llegue a tus aplicaciones. Para lograr esto, Kong utiliza dos conceptos fundamentales: **Servicios** y **Rutas**.

## Entendiendo la Lógica de Routing

Para que Kong sepa a dónde enviar una petición, debe seguir un flujo lógico:
`Cliente` $\rightarrow$ `Ruta (Route)` $\rightarrow$ `Servicio (Service)` $\rightarrow$ `Backend (Upstream)`

### ¿Qué es un Servicio (Service)?
Un Servicio es la representación abstracta de tu API backend. En lugar de referenciar la URL del servidor real en cada regla, defines un Servicio que contiene la URL base, el puerto y el protocolo del backend.

### ¿Qué es una Ruta (Route)?
Una Ruta es la regla que define cómo se accede a un Servicio. Puede basarse en:
- **Paths:** Por ejemplo, cualquier petición que empiece por `/pagos` se redirige al servicio de pagos.
- **Hosts:** Peticiones dirigidas a `api.misitio.com`.
- **Métodos HTTP:** Solo peticiones `POST` hacia un endpoint específico.

---

## Configuración Práctica vía Admin API

Imaginemos que tenemos un servicio de prueba llamado **Mockbin**. Vamos a exponerlo a través de Kong.

### 1. Creación del Servicio
Primero, definimos el servicio indicando el nombre y la URL del backend real:

```bash
curl -X POST http://localhost:8001/services \
  -d "name=mockbin_service" \
  -d "url=http://mockbin.local/request"
```

### 2. Creación de la Ruta
Ahora, creamos una ruta que asocie el path `/mockbin` con el servicio que acabamos de crear:

```bash
curl -X POST http://localhost:8001/services/mockbin_service/routes \
  -d "name=mockbin_route" \
  -d "paths[]=/mockbin"
```

### 3. Verificación de la Configuración
Podemos comprobar que los objetos se han creado correctamente consultando los endpoints de la Admin API:

```bash
# Listar todos los servicios
curl http://localhost:8001/services

# Listar todas las rutas
curl http://localhost:8001/routes
```

Con esta configuración, cualquier petición enviada al puerto del Proxy de Kong en la ruta `/mockbin` será redirigida automáticamente al backend de Mockbin.

---

**Artículo anterior:** [Laboratorio técnico: instalación de Kong en modo DB-less](/posts/kong/04-instalacion-db-less/04-instalacion-db-less/)  
**Siguiente artículo:** [Laboratorio técnico: instalación de Kong Ingress Controller (KIC)](/posts/kong/06-instalacion-kic/06-instalacion-kic/)
