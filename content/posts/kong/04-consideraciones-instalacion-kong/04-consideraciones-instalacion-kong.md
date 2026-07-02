---
title: "Guía de Planificación de la Instalación de Kong"
date: 2026-07-02T14:15:00+00:00
description: "Factores críticos a considerar antes de instalar Kong Gateway: dimensionamiento de recursos, puertos, DNS y seguridad."
tags: [Kong, Planificación, Infraestructura, Redes]
hero: images/kong/04-consideraciones/hero.png
---

Antes de ejecutar cualquier comando de instalación, es vital realizar una fase de planificación. Un despliegue incorrecto de Kong puede derivar en cuellos de botella de rendimiento o vulnerabilidades de seguridad graves.

## Factores Clave de Planificación

Existen seis áreas principales que deben analizarse antes de instalar Kong Gateway.

### 1. Dimensionamiento de Recursos (Resource Sizing)

Kong es extremadamente eficiente, pero el hardware necesario depende del volumen de tráfico. Debes considerar:
- **Ancho de Banda y Throughput:** Volumen de datos por segundo.
- **Latencia:** El impacto del Gateway en el tiempo de respuesta.
- **CPU y RAM:** Especialmente crítico para el número de workers de NGINX y el tamaño de la caché de memoria.
- **Recursos de Base de Datos:** IOPS y memoria para PostgreSQL.

### 2. Puertos Predeterminados

Es fundamental asegurar que los puertos necesarios estén abiertos en el firewall y no estén en uso por otros servicios:

- **Proxy Ports (8000/8443):** Por donde entra el tráfico de los clientes.
- **Admin API (8001/8444):** Para la gestión del Gateway (debe estar estrictamente protegida).
- **Kong Manager (GUI) (8002/8445):** Interfaz gráfica de administración.
- **Dev Portal (HTTP/HTTPS) (8003/8444):** Portal para desarrolladores.

### 3. Consideraciones de DNS

La correcta resolución de nombres es crítica para el funcionamiento de la UI y el Portal:
- **Hostnames:** Definir nombres claros para el Manager y la Admin API.
- **CORS:** Configurar correctamente el *Cross-Origin Resource Sharing* para que la UI pueda comunicarse con la API desde diferentes dominios.
- **Gestión de Cookies:** Asegurar que los dominios permitan el manejo de cookies para las sesiones de usuario.

### 4. Red y Firewall

- **Proxying TCP/TLS:** Definir si el tráfico será transparente o si Kong debe terminar la conexión SSL.
- **Apertura de Puertos:** Configurar reglas para permitir el acceso de los clientes al puerto del Proxy, pero restringir el acceso a la Admin API solo a administradores.

### 5. Seguridad y Certificados

Este es el punto más sensible. Debes planificar:
- **Cifrado de Datos:** Gestión de claves RSA y certificados TLS.
- **Secretos:** Integración con herramientas como HashiCorp Vault para no almacenar contraseñas en texto plano.
- **RBAC:** Configurar el Control de Acceso Basado en Roles (`enforce_rbac`) para limitar quién puede hacer cambios en el Gateway.

### 6. Licenciamiento

Para las versiones Enterprise, es necesario prever la implantación del archivo de licencia y monitorizar su fecha de expiración para evitar la interrupción del servicio.

---

**Artículo anterior:** [Topologías de Despliegue de Kong](/posts/kong/03-topologias-despliegue-kong)  
**Siguiente artículo:** [Gestión de la Configuración de Kong Gateway](/posts/kong/05-configuracion-kong-gateway)
