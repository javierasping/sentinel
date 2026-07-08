---
title: "Introducción a Kong Gateway"
date: 2026-07-02T14:00:00+00:00
description: "Guía unificada sobre qué es Kong Gateway, sus componentes, topologías de despliegue y la planificación previa a la instalación."
tags: [Kong, API Gateway, Architecture, Planning, Topologies]
hero: images/kong/01-introduccion/hero.png
weight: 1
---

Kong Gateway es un **API Gateway** basado en **NGINX** y desarrollado en **Lua**. Actúa como punto de entrada entre los consumidores de una API y los servicios backend, desempeñando el papel de un **reverse proxy** con capacidades avanzadas para gestionar, proteger y observar el tráfico.

Su función va mucho más allá de reenviar peticiones. Entre las capacidades que proporciona de forma nativa se encuentran:

- Autenticación y autorización mediante mecanismos como API Keys, JWT, Basic Auth u OIDC.
- Control del tráfico mediante políticas de *rate limiting*, cuotas y listas de acceso.
- Transformación de peticiones y respuestas sin modificar las aplicaciones.
- Registro de eventos, métricas y trazas para mejorar la observabilidad.
- Exposición centralizada de múltiples servicios a través de un único punto de entrada.

Gracias a este enfoque, las APIs pueden centrarse exclusivamente en la lógica de negocio, mientras que Kong Gateway asume las funcionalidades comunes relacionadas con la seguridad, el control del tráfico, la observabilidad y la gestión de las comunicaciones.


## Por qué utilizar un API Manager

Cuando una organización empieza a crecer, gestionar las APIs una a una deja de ser práctico. Un API Manager ayuda a centralizar tareas que, de otro modo, acabarían duplicadas en cada servicio:

- Definir políticas comunes, como límites de tamaño o control de tráfico.
- Proteger APIs con mecanismos de autenticación y autorización.
- Transformar cabeceras, rutas o payloads sin tocar el backend.
- Registrar consumo, métricas y rendimiento desde un punto único.
- Exponer las APIs de forma ordenada a consumidores internos o externos.

Kong encaja muy bien en ese escenario porque combina rendimiento, flexibilidad y un ecosistema de plugins bastante amplio.

## Ediciones de Kong Gateway

Kong Gateway se distribuye en dos ediciones principales:

* **Community Edition (CE)**, gratuita y de código abierto.
* **Enterprise Edition (EE)**, la versión comercial desarrollada por Kong Inc.

Ambas comparten el mismo núcleo y permiten publicar, proteger y gestionar APIs mediante la **Admin API**, que es la interfaz oficial para configurar todos los recursos de Kong. En la práctica, la mayoría de las herramientas de automatización, como **decK**, **Terraform** o scripts basados en `curl`, interactúan con esta API.

La principal diferencia es que la edición Enterprise incorpora funcionalidades adicionales orientadas a entornos corporativos, como plugins exclusivos, capacidades avanzadas de seguridad, integración con Konnect, soporte comercial y otras características que no forman parte de la edición Community.

## ¿Qué es Konga?

**Konga** es una interfaz web de terceros que permite administrar instancias de Kong Gateway utilizando la Admin API. Su objetivo es facilitar las tareas de gestión mediante una interfaz gráfica, evitando tener que realizar todas las operaciones desde la línea de comandos o mediante llamadas HTTP.

Aunque resulta útil para laboratorios y entornos de pruebas, es importante tener en cuenta que:

* No expone todas las capacidades disponibles en la Admin API.
* Su desarrollo lleva varios años sin una actividad significativa.
* En entornos de producción es recomendable utilizar las herramientas oficiales del ecosistema de Kong, como **decK**, **Terraform** o la propia Admin API.

## Arquitectura básica

En un despliegue clásico de Kong solemos encontrarnos con estos componentes:

| Componente | Función principal | Comentario |
| :--- | :--- | :--- |
| **Kong Gateway** | Recibe el tráfico, aplica plugins y enruta peticiones | Es el plano que ve el consumidor |
| **Admin API** | Expone la configuración de Kong | Se usa para crear y modificar recursos |
| **Kong Manager / Konga** | Interfaz gráfica de administración | Útil para operar visualmente |
| **PostgreSQL** | Persistencia de la configuración | Habitual en modos con base de datos |

Kong también puede operar sin base de datos, cargando una configuración declarativa en memoria. Esa opción resulta especialmente cómoda en despliegues automatizados y reproducibles.

## Plugins y ámbitos

Uno de los aspectos más potentes de Kong Gateway es su sistema de **plugins**. Gracias a él es posible añadir funcionalidades como autenticación, autorización, limitación de tráfico, transformación de peticiones, registro de métricas o integración con servicios externos sin necesidad de modificar el código de las aplicaciones.

Los plugins pueden aplicarse en distintos ámbitos, dependiendo de dónde quieras que entren en funcionamiento:

- **Global**: se ejecutan para todas las peticiones que pasan por el gateway.
- **Service**: se aplican únicamente a un servicio concreto.
- **Route**: afectan solo a una ruta determinada.
- **Consumer**: se ejecutan para un consumidor específico.

Esta flexibilidad permite aplicar cada política únicamente donde es necesaria y reutilizar la configuración.

## Modelos de despliegue

Kong no obliga a trabajar siempre de la misma forma; de hecho, existen distintas maneras de desplegarlo, pero podemos agruparlas en varios modelos habituales:

| Modelo | Base de datos | Gestión de configuración | Escalado | Comentario |
| :--- | :--- | :--- | :--- | :--- |
| **Traditional** | Sí, normalmente PostgreSQL | Dinámica mediante API o interfaz | Medio | El modelo clásico, útil cuando necesitas persistencia centralizada y cambios en caliente. |
| **DB-less** | No | Declarativa, desde fichero | Alto | Ideal para automatización, entornos efímeros o despliegues muy controlados. |
| **Hybrid** | Sí, solo en el Control Plane | Centralizada en el CP | Muy alto | Separa administración y tráfico en **Control Plane** y **Data Plane** para escalar con facilidad. |
| **Konnect** | Gestionada por el servicio | Centralizada en SaaS | Muy alto | Traslada el plano de control a la oferta gestionada de Kong para reducir carga operativa. |
| **KIC** | Depende del escenario | Mediante CRDs de Kubernetes | Alto | Integra Kong con Kubernetes, que es la vía natural si ese es tu plano principal de operación. |

## Puertos habituales

Por defecto, Kong suele utilizar estos puertos:

- `8000` y `8443` para el tráfico del proxy HTTP y HTTPS.
- `8001` y `8444` para la Admin API.

Además, si habilitas componentes adicionales como administración visual o clustering, puede haber otros puertos asociados. En cualquier caso, es buena práctica exponer solo lo imprescindible y restringir la Admin API todo lo posible.

---

Con esta introducción ya tenemos el mapa completo: qué es Kong, cómo se organiza, qué papel juegan la Admin API y el dashboard, y por qué su modelo de plugins lo convierte en una pieza tan potente para arquitecturas de microservicios.

En el siguiente artículo empezaremos con la parte práctica y veremos cómo desplegar Kong en Docker.

---

**Siguiente artículo:** [Laboratorio: instalación de Kong con Docker (modo híbrido)](/posts/kong/02-instalacion-docker-hibrido/02-instalacion-docker-hibrido/)
