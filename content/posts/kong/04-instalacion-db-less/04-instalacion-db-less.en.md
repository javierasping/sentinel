---
title: "Technical Lab: Installing Kong in DB-less Mode"
date: 2026-07-02T14:35:00+00:00
description: "Professional deployment of Kong Gateway on Kubernetes using KinD and Helm Charts."
tags: [Kong, Kubernetes, Helm, KinD, Cloud Native]
hero: images/kong/08-kubernetes/hero.png
weight: 4
---

Deploying Kong on Kubernetes allows leveraging native orchestration to manage high availability and automatic scaling. In this article, we will use **KinD (Kubernetes in Docker)** and **Helm** to implement a hybrid architecture.

## Step 1: Cluster Preparation with KinD

To start, we create a local cluster using a `KinD.yaml` configuration file. This file is crucial as it defines the port mappings necessary to access the Admin API and the Proxy from outside the cluster.

```bash
kind create cluster --config=KinD.yaml
```

The content of the `KinD.yaml` file is as follows:

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

## Step 2: Secrets and Certificates Management

In Kubernetes, security is managed through `Secrets`. For the Control Plane (CP) and Data Plane (DP) to communicate, we need to create TLS secrets.

### Cluster Certificate Creation
First, we generate a self-signed certificate for internal cluster communication:

```bash
openssl req -new -x509 -nodes \
  -newkey ec:<(openssl ecparam -name secp384r1) \
  -keyout ./cluster.key \
  -out ./cluster.crt \
  -days 1095 \
  -subj "/CN=kong_clustering"
```

### Loading Secrets into Namespaces
We create the namespaces `kong` (for CP) and `kong-dp` (for DP), and load the certificates:

```bash
# For the Control Plane
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

# For the Data Plane
kubectl -n kong-dp create secret tls kong-cluster-cert \
  --cert=./cluster.crt \
  --key=./cluster.key
kubectl -n kong-dp create secret tls kong-proxy-tls \
  --key="/etc/kong/ssl/server.key" \
  --cert="/etc/kong/ssl/server.crt"
```

## Step 3: Deployment with Helm

Helm is the standard package manager for Kubernetes. To install Kong, first add the official repository:

```bash
helm repo add kong https://charts.konghq.com
helm repo update
```

### Deploying the Control Plane
We use a `cp-values.yaml` file where we define the role as `control_plane`, configure the PostgreSQL database, and enable the Kong Manager.

```bash
helm -n kong install -f cp-values.yaml kong kong/kong
```

The content of the `cp-values.yaml` file is as follows:

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

### Deploying the Data Plane
Similarly, we use `dp-values.yaml`, configuring the role as `data_plane` and pointing the `cluster_control_plane` variable towards the previously created CP service.

```bash
helm -n kong-dp install -f dp-values.yaml kong kong/kong
```

The content of the `dp-values.yaml` file is as follows:

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

## Step 4: Status Verification

We can check that the pods are running correctly with:

```bash
kubectl -n kong get pods
kubectl -n kong-dp get pods
```

Once the deployment is ready, the traffic can flow through the Data Plane to backend services, while management is centralized in the Control Plane.

---

**Previous article:** [Technical Lab: Installing Kong in Traditional Mode](/en/posts/kong/03-instalacion-tradicional/03-instalacion-tradicional/)  
**Next article:** [Technical Lab: Installing Kong in Konnect](/en/posts/kong/05-instalacion-kong-connect/05-instalacion-kong-connect/)
