---
title: "Gestión de la Configuración de Kong Gateway"
date: 2026-07-02T14:20:00+00:00
description: Cómo gestionar los parámetros de configuración de Kong mediante archivos, variables de entorno y categorías de ajuste.
tags: [Kong, Configuración, DevOps, SysAdmin]
hero: images/kong/05-configuracion/hero.png
---

Kong Gateway ofrece una enorme cantidad de parámetros de configuración que permiten ajustar desde el comportamiento del proxy hasta la seguridad del plano de control. Dependiendo del método de despliegue, la forma de aplicar estos cambios varía.

## Métodos de Configuración

Existen tres formas principales de inyectar configuración en Kong:

### 1. Archivos de Configuración (`.conf` o `.yaml`)

Es el método tradicional. El archivo varía según la plataforma:
- **Bare Metal o VM:** Se utiliza el archivo `/etc/kong/kong.conf`.
- **Docker:** Se define a través del archivo `docker-compose.yaml`.
- **Kubernetes:** Se gestionan mediante los archivos de valores de Helm (`values.yaml`).

### 2. Variables de Entorno

Es la forma más común y recomendada en entornos modernos (contenedores). Cualquier propiedad de configuración puede ser sobrescrita mediante una variable de entorno siguiendo esta regla:
**Nombre de la propiedad $\rightarrow$ MAYÚSCULAS y prefijo `KONG_`**

*Ejemplos:*
- `proxy_error_log` $\rightarrow$ `KONG_PROXY_ERROR_LOG`
- `admin_gui_api_url` $\rightarrow$ `KONG_ADMIN_GUI_API_URL`

### 3. API de Administración

Algunos parámetros pueden modificarse en tiempo real mediante la Admin API sin necesidad de reiniciar el servicio.

---

## Categorías de Parámetros

Para facilitar la administración, los parámetros de configuración se agrupan en categorías:

### Ajustes Generales
Incluyen los niveles de log (`log_levels`) y la lista de plugins que deben cargarse al iniciar el Gateway.

### Modo Híbrido
Configuraciones específicas para la comunicación entre el Control Plane y el Data Plane, incluyendo certificados mTLS (`cluster_cert` y `cluster_cert_keys`).

### Ajustes de NGINX
Dado que Kong está construido sobre NGINX, permite ajustar:
- Cifrados y protocolos SSL.
- Tiempos de espera TCP (*timeouts*).
- Directorios de HTTP.

### Base de Datos y DNS
Configuraciones de TTL (*Time to Live*), caché y parámetros de conexión a PostgreSQL.

### Kong Manager
Definición de URLs y puertos específicos para la interfaz gráfica.

---

**Artículo anterior:** [Guía de Planificación de la Instalación](/posts/kong/04-consideraciones-instalacion-kong)  
**Siguiente artículo:** [Laboratorio: Instalación con Docker (Modo Híbrido)](/posts/kong/06-instalacion-docker-hibrido)
