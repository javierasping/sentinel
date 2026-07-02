---
title: "Laboratorio: Instalación de Kong en Kubernetes (Modo Híbrido)"
date: 2026-07-02T14:35:00+00:00
description: Despliegue profesional de Kong Gateway en Kubernetes utilizando KinD y Helm Charts.
tags: [Kong, Kubernetes, Helm, KinD, Cloud Native]
hero: images/kong/08-kubernetes/hero.png
---

Desplegar Kong en Kubernetes permite aprovechar la orquestación nativa para gestionar la alta disponibilidad y el escalado automático. En este artículo, utilizaremos **KinD (Kubernetes in Docker)** y **Helm** para implementar una arquitectura híbrida.

## Paso 1: Preparación del Cluster con KinD

Para iniciar, creamos un cluster local utilizando un archivo de configuración `KinD.yaml`. Este archivo es crucial ya que define los mapeos de puertos necesarios para acceder a la Admin API y al Proxy desde fuera del cluster.

```bash
kind create cluster --config=KinD.yaml
```

## Paso 2: Gestión de Secretos y Certificados

En Kubernetes, la seguridad se gestiona mediante `Secrets`. Para que el Control Plane (CP) y el Data Plane (DP) se comuniquen, necesitamos crear secretos de TLS.

### Creación del Certificado de Cluster
Primero, generamos un certificado auto-firmado para la comunicación interna del cluster:

```bash
openssl req -new -x509 -nodes \
  -newkey ec:<(openssl ecparam -name secp384r1) \
  -keyout ./cluster.key \
  -out ./cluster.crt \
  -days 1095 \
  -subj "/CN=kong_clustering"
```

### Carga de Secretos en los Namespaces
Creamos los namespaces `kong` (para el CP) y `kong-dp` (para el DP), y cargamos los certificados:

```bash
# Para el Control Plane
kubectl -n kong create secret tls kong-cluster-cert \
  --cert=./cluster.crt \
  --key=./cluster.key
kubectl -n kong create secret tls kong-manager-tls \
  --key="/etc/kong/ssl/server.key" \
  --cert="/etc/kong/ssl/server.crt"
kubectl -n kong create secret tls kong-admin-tls \
  --key="/etc/kong/ssl/server.key" \
  --cert="/etc/kong/ssl/server.crt"
kubectl -n kong create secret generic kong-enterprise-superuser-password \
  --from-literal=password=password

# Para el Data Plane
kubectl -n kong-dp create secret tls kong-cluster-cert \
  --cert=./cluster.crt \
  --key=./cluster.key
kubectl -n kong-dp create secret tls kong-proxy-tls \
  --key="/etc/kong/ssl/server.key" \
  --cert="/etc/kong/ssl/server.crt"
```

## Paso 3: Despliegue con Helm

Helm es el gestor de paquetes estándar de Kubernetes. Para instalar Kong, primero añadimos el repositorio oficial:

```bash
helm repo add kong https://charts.konghq.com
helm repo update
```

### Desplegando el Control Plane
Utilizamos un archivo `cp-values.yaml` donde definimos que el rol es `control_plane`, configuramos la base de datos PostgreSQL y habilitamos el Kong Manager.

```bash
helm -n kong install -f cp-values.yaml kong kong/kong
```

### Desplegando el Data Plane
De forma similar, usamos `dp-values.yaml`, configurando el rol como `data_plane` y apuntando la variable `cluster_control_plane` hacia el servicio del CP creado anteriormente.

```bash
helm -n kong-dp install -f dp-values.yaml kong kong/kong
```

## Paso 4: Verificación del Estado

Podemos comprobar que los pods están corriendo correctamente con:

```bash
kubectl -n kong get pods
kubectl -n kong-dp get pods
```

Una vez que el despliegue esté listo, el tráfico podrá fluir a través del Data Plane hacia los servicios backend, mientras que la gestión se centraliza en el Control Plane.

---

**Artículo anterior:** [Gestión de Licencias en Kong Enterprise](/posts/kong/07-gestion-licencias-enterprise)  
**Siguiente artículo:** [Primeros Pasos: Servicios y Rutas](/posts/kong/09-servicios-y-rutas-basicos)
