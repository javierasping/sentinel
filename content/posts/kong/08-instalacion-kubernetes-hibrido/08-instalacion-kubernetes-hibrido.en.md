---
title: "Lab: Installing Kong on Kubernetes (Hybrid Mode)"
date: 2026-07-02T14:35:00+00:00
description: "Professional deployment of Kong Gateway on Kubernetes using KinD and Helm Charts."
tags: [Kong, Kubernetes, Helm, KinD, Cloud Native]
hero: images/kong/08-kubernetes/hero.png
---

Deploying Kong on Kubernetes allows leveraging native orchestration to manage high availability and automatic scaling. In this article, we will use **KinD (Kubernetes in Docker)** and **Helm** to implement a hybrid architecture.

## Step 1: Cluster Preparation with KinD

To start, we create a local cluster using a `KinD.yaml` configuration file. This file is crucial as it defines the port mappings necessary to access the Admin API and the Proxy from outside the cluster.

```bash
kind create cluster --config=KinD.yaml
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

### Deploying the Data Plane
Similarly, we use `dp-values.yaml`, configuring the role as `data_plane` and pointing the `cluster_control_plane` variable towards the previously created CP service.

```bash
helm -n kong-dp install -f dp-values.yaml kong kong/kong
```

## Step 4: Status Verification

We can check that the pods are running correctly with:

```bash
kubectl -n kong get pods
kubectl -n kong-dp get pods
```

Once the deployment is ready, the traffic can flow through the Data Plane to backend services, while management is centralized in the Control Plane.

---

**Previous article:** [License Management in Kong Enterprise](/posts/kong/07-gestion-licencias-enterprise)  
**Next article:** [First Steps: Services and Routes](/posts/kong/09-servicios-y-rutas-basicos)
