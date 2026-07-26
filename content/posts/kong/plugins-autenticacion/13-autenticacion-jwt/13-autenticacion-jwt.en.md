---
title: "JWT Auth in Kong"
description: "Validate HS256 JWTs on a Kong HTTPRoute managed by KIC."
weight: 13
---

This Kubernetes-native lab publishes `echo.javiercd.es/jwt`. The KIC installation resources already exist, and the authentication resources are split into four `13-jwt-*.yaml` files. The Consumer credential uses `iss: jwt-client`, algorithm `HS256`, and the lab secret `jwt-shared-secret`.

```bash
sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
vagrant ssh
cd ~/kic-auth
sudo kubectl get gateway kong -n kong
sudo kubectl get svc echo -n javier
sudo kubectl apply -f 13-jwt-plugin.yaml
sudo kubectl apply -f 13-jwt-secret.yaml
sudo kubectl apply -f 13-jwt-consumer.yaml
sudo kubectl apply -f 13-jwt-httproute.yaml
exit
```

Generate a short-lived JWT on the host, send it as `Authorization: Bearer`, and call `/jwt`. Missing or invalid tokens return `401`. See the [official JWT plugin reference](https://developer.konghq.com/plugins/jwt/).

> [!NOTE]
> These posts are built on the KIC installation scenario. They reuse the same `kong` Gateway, `echo` Service, and the MetalLB address assigned to `kong-gateway-proxy`: `192.168.121.200`.
>
> Because this is a local lab, first prepare the domain from the host:
>
> ```bash
> sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
> echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
> ```
>
> Then enter the VM and verify the resources created by the KIC installation post:
>
> ```bash
> vagrant ssh
> cd ~/kic-auth
> sudo kubectl get gateway kong -n kong
> sudo kubectl get svc echo -n javier
> ```
>
> The KIC installation post already created these shared resources, so this authentication lab only adds its own files.
>
> If MetalLB assigned a different address in your cluster, replace `192.168.121.200` in this notice, in `/etc/hosts`, and in the tests. See also the [**Dominio y preparación**](http://localhost:1313/posts/kong/10-autenticacion-basic-auth/10-autenticacion-basic-auth/#dominio-y-preparaci%C3%B3n) section.

## How Kubernetes relates to Kong

KIC watches these Kubernetes resources and translates them into Kong configuration:

| File | Kubernetes resource | Kong translation |
| --- | --- | --- |
| `13-jwt-plugin.yaml` | `KongPlugin` | plugin configuration |
| `13-jwt-secret.yaml` | `Secret` | authentication credential |
| `13-jwt-consumer.yaml` | `KongConsumer` | Kong Consumer |
| `13-jwt-httproute.yaml` | `HTTPRoute` | Kong Route and backend association |

The `kong` Gateway and the `echo` Service already existed because they were created in the KIC installation post. Each `HTTPRoute` reuses that shared Gateway and Service.

## Lab files, step by step

### 1. `13-jwt-plugin.yaml`

This file creates a `KongPlugin`. The `plugin` field selects the plugin Kong will run and `config` contains its options. KIC translates this resource into a Kong plugin configuration. In a database-backed deployment it is represented in the `plugins` table, including its configuration and its Route or Consumer associations.

Definition of the `KongPlugin` resource:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: jwt
  namespace: javier
plugin: jwt
config:
  claims_to_verify: [exp]
```

### 2. `13-jwt-secret.yaml`

This `Secret` contains the credential that KIC must convert for the related plugin. The `konghq.com/credential` label identifies the credential type. KIC does not use it as a backend environment variable. In a database-backed deployment it is represented in the plugin credential table and linked to the Consumer.

Definition of the `Secret` resource:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: jwt-credential
  namespace: javier
  labels:
    konghq.com/credential: jwt
stringData:
  key: jwt-client
  secret: jwt-shared-secret
  algorithm: HS256
```

### 3. `13-jwt-consumer.yaml`

This `KongConsumer` represents the user or application being authenticated. The `credentials` list references the credential Secret. KIC creates the Consumer and links the credential to it. In a database-backed deployment it is represented in `consumers` and in the relationship with its credential.

Definition of the `KongConsumer` resource:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: jwt-client
  namespace: javier
  annotations: {kubernetes.io/ingress.class: kong}
username: jwt-client
credentials: [jwt-credential]
```

### 4. `13-jwt-httproute.yaml`

This `HTTPRoute` publishes the endpoint. `parentRefs` attaches it to the `kong` Gateway, `hostnames` limits the domain, and `PathPrefix` defines the path. `backendRefs` points to the existing `echo` Service from the KIC scenario. KIC primarily translates it into a Kong Route and a Service association, internally represented through Service, Upstream, and Targets. The `konghq.com/plugins` annotation links the plugin to the Route.

Definition of the `HTTPRoute` resource:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: jwt
  namespace: javier
  annotations: {konghq.com/plugins: jwt}
spec:
  parentRefs: [{name: kong, namespace: kong}]
  hostnames: [echo.javiercd.es]
  rules:
    - matches: [{path: {type: PathPrefix, value: /jwt}}]
      backendRefs: [{name: echo, port: 80}]
```
