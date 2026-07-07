---
title: "Laboratorio técnico: instalación de Kong en modo tradicional"
date: 2026-07-02T14:30:00+00:00
description: "Cómo aplicar y gestionar el archivo de licencia en Kong Gateway Enterprise para habilitar funciones avanzadas."
tags: [Kong, Enterprise, Licencias, Administración]
hero: images/kong/07-licencias/hero.png
weight: 3
---

Kong Gateway Enterprise ofrece funcionalidades avanzadas de seguridad, gobernanza y soporte que requieren la aplicación de una licencia válida. Existen diversas formas de introducir esta licencia en el sistema, dependiendo de la agilidad y el método de despliegue preferido.

## Métodos de Aplicación de la Licencia

Kong evalúa la licencia siguiendo un orden de prioridad específico. Si encuentra una licencia en el primer método, ignorará los siguientes.

### 1. Variable de Entorno (`KONG_LICENSE_DATA`)
Es el método más rápido para despliegues efímeros o automatizados. Consiste en pasar el contenido del archivo de licencia directamente como el valor de la variable de entorno `KONG_LICENSE_DATA`.

### 2. Ubicación por Defecto (`/etc/kong/license.json`)
Kong busca automáticamente un archivo llamado `license.json` en el directorio `/etc/kong/`. Es el método estándar para instalaciones en servidores físicos o máquinas virtuales.

### 3. Ruta Personalizada (`KONG_LICENSE_PATH`)
Si el archivo de licencia se encuentra en una ruta no estándar, se puede especificar la ubicación exacta mediante la variable de entorno `KONG_LICENSE_PATH`.

### 4. Admin API (Método Dinámico)
Este es el método más flexible, ya que permite aplicar la licencia **sin reiniciar el servicio**. Se realiza mediante una petición POST al endpoint de licencias:

```bash
curl -X POST http://localhost:8001/licenses \
  -F "payload=@/ruta/al/archivo/license.json"
```

> **Importante en Modo Híbrido:** Cuando se aplica la licencia al **Control Plane** mediante la API, esta se distribuye automáticamente a todos los **Data Planes** conectados en tiempo real.

## Verificación de la Licencia

Para comprobar que la licencia se ha aplicado correctamente y conocer su estado (fecha de expiración, versión de Kong, etc.), se puede utilizar el endpoint de reporte:

```bash
curl http://localhost:8001/license/report
```

La respuesta en JSON detallará la versión de la licencia, la fecha de vencimiento y el número de Data Planes conectados.

Si prefieres una gestión visual, puedes abrir el **Kong Manager**, donde el aviso de "Licencia no aplicada" desaparecerá una vez que el sistema valide el archivo.

---

**Artículo anterior:** [Laboratorio técnico: instalación de Kong con Docker (modo híbrido)](/posts/kong/02-instalacion-docker-hibrido/02-instalacion-docker-hibrido/)  
**Siguiente artículo:** [Laboratorio técnico: instalación de Kong en modo DB-less](/posts/kong/04-instalacion-db-less/04-instalacion-db-less/)
