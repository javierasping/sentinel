---
title: "Laboratorio: Instalación de Kong en Kubernetes (Modo Híbrido)"
date: 2026-07-02T14:35:00+00:00
description: "Despliegue profesional de Kong Gateway en Kubernetes utilizando KinD y Helm Charts."
tags: [Kong, Kubernetes, Helm, KinD, Cloud Native]
hero: images/kong/08-kubernetes/hero.png
---

Desplegar Kong en Kubernetes permite aprovechar la orquestación nativa para gestionar la alta disponibilidad y el escalado automático. En este artículo, utilizaremos **KinD (Kubernetes in Docker)** y **Helm** para implementar una arquitectura híbrida.

## Paso 1: Preparación del Cluster con KinD

Para iniciar, creamos un cluster local utilizando un archivo de configuración `KinD.yaml`. Este archivo es crucial ya que define los mapeos de puertos necesarios para acceder a la Admin API y al Proxy desde fuera del cluster.

```bash
kind create cluster --config=KinD.yaml
```

El contenido del archivo `KinD.yaml` es el siguiente:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: kongacademy
nodes:
- role: control-plane
  extraMounts:
  - hostPath: /home/ubuntu
    containerPath: /mnt/host-ubuntu
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 30000
    hostPort: 8000 # Proxy
    protocol: TCP
  - containerPort: 30443
    hostPort: 8443 # Proxy
    protocol: TCP
  - containerPort: 30001
    hostPort: 8001 # Admin api
    protocol: TCP
  - containerPort: 30501
    hostPort: 8444 # Admin api
    protocol: TCP
  - containerPort: 30002
    hostPort: 8002 # Manager
    protocol: TCP
  - containerPort: 30500
    hostPort: 8445 # Manager
    protocol: TCP
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

El contenido del archivo `cp-values.yaml` es el siguiente:

```yaml
ingressController:
  enabled: false
deployment:
  kong:
    enabled: true
    daemonset: false
  userDefinedVolumes:
  - name: custom-template
    emptyDir: {}
image:
  repository: kong/kong-gateway
  tag: "3.10"
env:
  nginx_http_more_clear_headers: "Access-Control-Allow-Credentials"
  audit_log: "off"
  database: "postgres"
  role: "control_plane"
  cluster_cert: "/etc/secrets/kong-cluster-cert/tls.crt"
  cluster_cert_key: "/etc/secrets/kong-cluster-cert/tls.key"
  status_listen: 0.0.0.0:8100
  password:
    valueFrom:
      secretKeyRef:
        name: kong-enterprise-superuser-password
        key: password
  admin_gui_url: ${KONG_ADMIN_GUI_URL}
  admin_gui_api_url: ${KONG_ADMIN_API_URI}
  admin_gui_ssl_cert:  /etc/secrets/kong-manager-tls/tls.crt
  admin_gui_ssl_cert_key:  /etc/secrets/kong-manager-tls/tls.key
  admin_ssl_cert: /etc/secrets/kong-admin-tls/tls.crt
  admin_ssl_cert_key:  /etc/secrets/kong-admin-tls/tls.key
cluster:
  enabled: true
  tls:
    enabled: true
    servicePort: 8005
    containerPort: 8005
clustertelemetry:
  enabled: true
  tls:
    enabled: true
    servicePort: 8006
    containerPort: 8006
proxy:
  enabled: false
portal:
  enabled: false
portalapi:
  enabled: false
admin:
  enabled: true
  labels:
    enable-metrics: "true"
  type: NodePort
  http:
    enabled: true
    nodePort: 30001
  tls:
    enabled: true
    nodePort: 30501
  ingress:
    enabled: false
enterprise:
  enabled: true
  rbac:
    enabled: false
  smtp:
    enabled: false
  ingress:
    enabled: false
manager:
  enabled: true
  type: NodePort
  http:
    nodePort: 30002
  tls:
    enabled: true
    nodePort: 30500
  ingress:
    enabled: false
secretVolumes:
  - kong-cluster-cert
  - kong-manager-tls
  - kong-admin-tls
postgresql:
  enabled: true
  auth:
    username: kong
    database: kong
    password: kong
  image:
    registry: docker.io
    repository: bitnamilegacy/postgresql
    tag: 15
  service:
    ports:
      postgresql: "5432"
serviceMonitor:
  enabled: true
  namespace: monitoring
status:
  enabled: true
  type: ClusterIP
```

### Desplegando el Data Plane
De forma similar, usamos `dp-values.yaml`, configurando el rol como `data_plane` y apuntando la variable `cluster_control_plane` hacia el servicio del CP creado anteriormente.

```bash
helm -n kong-dp install -f dp-values.yaml kong kong/kong
```

El contenido del archivo `dp-values.yaml` es el siguiente:

```yaml
ingressController:
  enabled: false
image:
  repository: kong/kong-gateway
  tag: "3.10"
env:
  database: "off"
  role: "data_plane"
  cluster_cert: "/etc/secrets/kong-cluster-cert/tls.crt"
  cluster_cert_key: "/etc/secrets/kong-cluster-cert/tls.key"
  ssl_cert: /etc/secrets/kong-proxy-tls/tls.crt
  ssl_cert_key: /etc/secrets/kong-proxy-tls/tls.key
  status_listen: 0.0.0.0:8100
  lua_ssl_trusted_certificate: "/etc/secrets/kong-cluster-cert/tls.crt"
  cluster_control_plane: "kong-kong-cluster.kong.svc.cluster.local:8005"
  cluster_telemetry_endpoint: kong-kong-clustertelemetry.kong.svc.cluster.local:8006
proxy:
  http:
    enabled: true
    nodePort: 30000
  labels:
    enable-metrics: "true"
  tls:
    enabled: true
    nodePort: 30443
  type: NodePort
  ingress:
    enabled: true
enterprise:
  enabled: true
  rbac:
    enabled: false
  smtp:
    enabled: false
  portal:
    enabled: false
manager:
  enabled: false
secretVolumes:
- kong-cluster-cert
- kong-proxy-tls
portal:
  enabled: false
portalapi:
  enabled: false
admin:
  enabled: false
serviceMonitor:
  enabled: true
  namespace: monitoring
status:
  enabled: true
  type: ClusterIP
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
