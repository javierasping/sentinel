---
title: "Arquitectura y Componentes Core de Kong Gateway"
date: 2026-07-02T14:05:00+00:00
description: Análisis de los pilares fundamentales de Kong: el Gateway, el Kong Manager y la base de datos PostgreSQL.
tags: [Kong, Arquitectura, PostgreSQL, Kong Manager]
hero: images/kong/02-componentes-core/hero.png
---

Para entender cómo funciona Kong Gateway, es necesario desglosar su arquitectura en los componentes lógicos que permiten su operación. Aunque algunos de estos componentes pueden residir en el mismo binario, cumplen funciones muy distintas.

## Los tres pilares de la infraestructura de Kong

La infraestructura básica de Kong se sostiene sobre tres componentes principales: el Kong Gateway, el Kong Manager y, en la mayoría de los despliegues, una base de datos PostgreSQL.

### 1. Kong Gateway (El Core)

Es el corazón del sistema. Es el componente responsable de recibir todas las peticiones de los clientes, aplicar las reglas de routing y ejecutar los plugins configurados antes de redirigir la petición al servicio backend (upstream).

Su objetivo es ser extremadamente eficiente en el consumo de recursos y ofrecer una latencia mínima, ya que cada llamada a la API debe pasar obligatoriamente por él.

### 2. Kong Manager (La Interfaz)

Mientras que el Gateway se encarga del tráfico, el **Kong Manager** es la herramienta de gestión. Se trata de una interfaz de usuario basada en el navegador que permite monitorizar y administrar el Gateway de forma visual.

A través del Manager, los administradores pueden crear servicios, definir rutas y configurar plugins sin necesidad de interactuar directamente con la API de administración mediante comandos de terminal.

### 3. Base de Datos (PostgreSQL)

Por defecto, Kong utiliza **PostgreSQL** como su motor de almacenamiento. La base de datos es donde se guardan todas las entidades configuradas, tales como:

- **Servicios (Services):** Definiciones de los backends.
- **Rutas (Routes):** Reglas de acceso a esos servicios.
- **Plugins:** Configuraciones de seguridad, rate limiting, etc.
- **Consumidores:** Información sobre quién accede a la API.

> **Nota:** Es importante mencionar que Kong también soporta un modo **DB-less** (sin base de datos), donde la configuración se gestiona de forma declarativa mediante un archivo YAML, cargando todo en memoria para maximizar la velocidad.

## Resumen de Componentes

| Componente | Función Principal | Tipo |
| :--- | :--- | :--- |
| **Kong Gateway** | Brokering de tráfico y ejecución de plugins | Plano de Datos |
| **Kong Manager** | Gestión visual y monitorización | Plano de Control (UI) |
| **PostgreSQL** | Almacenamiento de persistencia de la configuración | Almacenamiento |

---

**Artículo anterior:** [Introducción a Kong Gateway](/posts/kong/01-introduccion-kong-gateway)  
**Siguiente artículo:** [Topologías de Despliegue de Kong](/posts/kong/03-topologias-despliegue-kong)
