---
title: "Topologías de Despliegue de Kong Gateway"
date: 2026-07-02T14:10:00+00:00
description: "Comparativa de los modelos de despliegue de Kong: Traditional, DB-less, Hybrid y Kong Connect."
tags: [Kong, Arquitectura, Despliegue, Topologías]
hero: images/kong/03-topologias/hero.png
---

Dependiendo de las necesidades de escalabilidad, seguridad y gestión de la infraestructura, Kong permite desplegarse bajo diferentes modelos. Elegir la topología correcta es fundamental para optimizar el rendimiento y la mantenibilidad del sistema.

## Modelos de Despliegue de Kong

A continuación, analizamos las cinco topologías principales soportadas por Kong.

### 1. Despliegue Tradicional (Traditional)

En este modelo, cada nodo de Kong Gateway está conectado directamente a una base de datos PostgreSQL. Todos los detalles de configuración se almacenan y recuperan desde allí.

- **Características:** Soporta clusters de un solo nodo o multi-nodo.
- **Ventaja:** Todos los plugins tienen acceso directo a la base de datos para leer y escribir entidades.
- **Uso ideal:** Entornos donde se requiere una gestión dinámica y persistente de la configuración.

### 2. Despliegue Sin Base de Datos (DB-less)

Kong puede ejecutarse sin depender de una base de datos externa, utilizando únicamente el almacenamiento en memoria. La configuración se define de forma **declarativa** en un archivo (usualmente YAML).

- **Limitaciones:** Los plugins que requieren una base de datos central para coordinar estados (como algunos contadores globales de rate limiting) no son totalmente compatibles.
- **Uso ideal:** Entornos de CI/CD, despliegues efímeros o donde se busca la máxima velocidad de arranque y simplicidad.

### 3. Despliegue Híbrido (Hybrid Mode)

Es una de las arquitecturas más potentes de Kong. Aquí, los nodos se dividen en dos roles claramente diferenciados:

- **Control Plane (CP):** Es el cerebro. Aquí se gestiona la configuración, reside la API de Administración y el Kong Manager.
- **Data Plane (DP):** Son los nodos que sirven el tráfico real. No tienen base de datos; en su lugar, mantienen una conexión en tiempo real con el Control Plane para recibir las actualizaciones de configuración.

Este modelo permite escalar los Data Planes horizontalmente de forma masiva sin saturar la base de datos central.

### 4. Kong Connect

Konnect es la plataforma SaaS de Kong. En este escenario, Kong gestiona el **Control Plane** en su propia nube, mientras que tú despliegas los **Data Planes** donde prefieras (on-premise, nube propia o totalmente gestionado por Kong).

### 5. Kong Ingress Controller (KIC)

Específico para Kubernetes, KIC permite ejecutar Kong como un Ingress. El controlador escucha los manifiestos de Kubernetes (CRDs) y los traduce automáticamente en configuraciones de Kong, aplicándolas al Gateway.

---

## Tabla Comparativa de Topologías

| Modelo | Base de Datos | Gestión de Configuración | Escalabilidad DP |
| :--- | :--- | :--- | :--- |
| **Tradicional** | Sí (PostgreSQL) | Dinámica (API/UI) | Media |
| **DB-less** | No | Declarativa (Archivo) | Alta |
| **Híbrido** | Sí (solo en CP) | Centralizada en CP | Muy Alta |
| **Connect** | Gestionada (SaaS) | Centralizada en SaaS | Muy Alta |
| **KIC** | Variable | Vía Kubernetes CRDs | Alta |

---

**Artículo anterior:** [Componentes Core de Kong Gateway](/posts/kong/02-componentes-core-kong)  
**Siguiente artículo:** [Guía de Planificación de la Instalación](/posts/kong/04-consideraciones-instalacion-kong)
