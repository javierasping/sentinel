---
title: "Laboratorio: instalación de Kong Ingress Controller (KIC)"
date: 2026-07-02T14:45:00+00:00
description: "Metodologías para validar el correcto funcionamiento de Kong Gateway mediante la Admin API, el Kong Manager y pruebas de tráfico real."
tags: [Kong, Testing, Validación, API Gateway]
hero: images/kong/10-verificacion/hero.png
weight: 6
---

El paso final tras cualquier instalación y configuración es la validación. No basta con que los contenedores estén en estado `Running`. Debemos asegurar que el tráfico fluye correctamente y que el plano de control está sincronizado con el de datos.

## Métodos de Verificación

Existen tres formas principales de validar que Kong Gateway está operando según lo previsto.

### 1. Validación mediante la Admin API

La Admin API es la fuente de verdad técnica. Podemos verificar la salud del nodo y la configuración activa mediante peticiones HTTP:

- **Estado del Nodo:** Consultar el endpoint `/status` para verificar la versión de Kong y el estado de la conexión con la base de datos.
- **Inspección de Rutas:** Verificar que las rutas creadas están correctamente asociadas a sus servicios mediante `GET /routes`.

### 2. Validación Visual con Kong Manager

Para quienes prefieren una interfaz gráfica, el **Kong Manager** ofrece una vista consolidada del estado del sistema:
- **Dashboard:** Permite ver la salud general del Gateway.
- **Workspace:** Podemos navegar por los servicios y rutas para confirmar que los cambios aplicados vía API se reflejan visualmente.
- **Logs de Error:** Útil para diagnosticar problemas de conexión con el backend en tiempo real.

### 3. Pruebas de Tráfico Real (End-to-End)

La prueba definitiva es realizar una petición a través del Proxy. Si hemos configurado correctamente un servicio y una ruta (como vimos en el artículo anterior), la prueba sería:

```bash
curl -i http://localhost:8000/mockbin
```

**¿Qué debemos analizar en la respuesta?**
- **HTTP 200 OK:** Indica que el Gateway recibió la petición, encontró la ruta y el backend respondió correctamente.
- **Encabezados X-Kong:** Kong añade encabezados como `X-Kong-Request-ID` y `Via`, que confirman que la petición ha sido procesada por el Gateway.
- **HTTP 404 Not Found:** Si recibimos este error con el mensaje `"no Route matched with those values"`, significa que el Gateway está vivo, pero la ruta solicitada no existe o está mal configurada.

## Checklist Final de Calidad

Antes de pasar a producción, asegúrate de cumplir estos puntos:
- [ ] El Control Plane puede comunicarse con los Data Planes.
- [ ] La licencia Enterprise ha sido aplicada y validada.
- [ ] Los puertos del Proxy están abiertos al tráfico externo.
- [ ] La Admin API está restringida y no es accesible públicamente.
- [ ] Los certificados SSL están correctamente instalados y no han expirado.

---

**Artículo anterior:** [Laboratorio: instalación de Kong en Konnect](/posts/kong/05-instalacion-kong-connect/05-instalacion-kong-connect/)  
**Siguiente artículo:** [Laboratorio: Instalación de Kong en Kubernetes (Modo Híbrido)](/posts/kong/07-instalacion-kubernetes-hibrido/07-instalacion-kubernetes-hibrido/)
