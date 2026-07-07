---
title: "Guía Completa de Kong Gateway"
date: 2026-07-02T15:00:00+00:00
description: "Serie didáctica sobre la instalación, configuración y despliegue profesional de Kong Gateway en entornos Docker y Kubernetes."
tags: [Kong, API Gateway, DevOps, Kubernetes, Docker]
hero: images/kong/index/hero.png
menu:
  sidebar:
    name: "Kong Gateway"
    identifier: Kong
    weight: 200
---

Bienvenido a la guía completa de **Kong Gateway**. En esta serie de artículos, exploraremos desde los conceptos fundamentales hasta el despliegue de una arquitectura híbrida en entornos de producción.

Kong Gateway es una herramienta esencial para cualquier arquitectura de microservicios moderna, permitiendo centralizar la seguridad, el tráfico y la observabilidad de tus APIs.

## Ruta de Aprendizaje

La serie está estructurada para llevarte de la mano, desde la teoría básica hasta la implementación técnica avanzada.

### 1. Fundamentos y Arquitectura
En esta sección sentamos las bases teóricas necesarias para entender el funcionamiento interno del Gateway.
- [Introducción, arquitectura y planificación](/posts/kong/01-introduccion-kong-gateway): Qué es Kong Gateway, cómo se estructura y qué revisar antes de instalarlo.

### 2. Instalaciones y Despliegues
Pasamos a la fase práctica, preparando la configuración base y ejecutando cada modo de instalación.
- [Instalación con Docker (Modo Híbrido)](/posts/kong/02-instalacion-docker-hibrido): Laboratorio práctico con Docker Compose y mTLS.
- [Instalación en modo tradicional](/posts/kong/03-instalacion-tradicional): Despliegue database-backed con PostgreSQL, Admin API y Kong Manager.
- [Instalación en modo DB-less](/posts/kong/04-instalacion-db-less): Despliegue declarativo sin base de datos.
- [Instalación en Konnect](/posts/kong/05-instalacion-kong-connect): Control plane gestionado en SaaS y data planes conectados.
- [Instalación de Kong Ingress Controller (KIC)](/posts/kong/06-instalacion-kic): Integración nativa con Kubernetes mediante Helm y CRDs.
- [Instalación en Kubernetes (Modo Híbrido)](/posts/kong/07-instalacion-kubernetes-hibrido): Despliegue avanzado utilizando KinD y Helm Charts.
- [Primeros Pasos: Servicios y Rutas](/posts/kong/08-servicios-y-rutas-basicos): Lógica de routing y configuración de backends.
- [Verificación y Pruebas del Gateway](/posts/kong/09-verificacion-y-pruebas-gateway): Metodologías de testeo y checklist final de calidad.

---

*Esta serie ha sido diseñada para proporcionar un camino progresivo y didáctico, asegurando que cada concepto quede claro antes de avanzar al siguiente paso técnico.*
