---
title: "HMAC Auth in Kong"
description: "Sign requests to Kong with HMAC Auth and Gateway API."
weight: 12
---

The route is `http://echo.javiercd.es/hmac-auth`. The Plugin, credential Secret, Consumer, and HTTPRoute are separate files with the `12-hmac-auth-` prefix. The Consumer credential is `hmac-client` / `hmac-shared-secret`, and the plugin requires `date`, `@request-target`, and `host` in the signature.

```bash
sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
vagrant ssh
cd ~/kic-auth
sudo kubectl get gateway kong -n kong
sudo kubectl get svc echo -n javier
sudo kubectl apply -f 12-hmac-auth-plugin.yaml
sudo kubectl apply -f 12-hmac-auth-secret.yaml
sudo kubectl apply -f 12-hmac-auth-consumer.yaml
sudo kubectl apply -f 12-hmac-auth-httproute.yaml
exit
```

Build the HMAC signature on the host with the algorithm and headers documented in [HMAC Auth](https://developer.konghq.com/plugins/hmac-auth/), then send it to `/hmac-auth`. An unsigned request must return `401`.

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
| `12-hmac-auth-plugin.yaml` | `KongPlugin` | plugin configuration |
| `12-hmac-auth-secret.yaml` | `Secret` | authentication credential |
| `12-hmac-auth-consumer.yaml` | `KongConsumer` | Kong Consumer |
| `12-hmac-auth-httproute.yaml` | `HTTPRoute` | Kong Route and backend association |

The `kong` Gateway and the `echo` Service already existed because they were created in the KIC installation post. Each `HTTPRoute` reuses that shared Gateway and Service.

## Lab files, step by step

### 1. `12-hmac-auth-plugin.yaml`

This file creates a `KongPlugin`. The `plugin` field selects the plugin Kong will run and `config` contains its options. KIC translates this resource into a Kong plugin configuration. In a database-backed deployment it is represented in the `plugins` table, including its configuration and its Route or Consumer associations.

Definition of the `KongPlugin` resource:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: hmac-auth
  namespace: javier
plugin: hmac-auth
config:
  enforce_headers: [date, '@request-target', host]
  hide_credentials: true
```

### 2. `12-hmac-auth-secret.yaml`

This `Secret` contains the credential that KIC must convert for the related plugin. The `konghq.com/credential` label identifies the credential type. KIC does not use it as a backend environment variable. In a database-backed deployment it is represented in the plugin credential table and linked to the Consumer.

Definition of the `Secret` resource:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: hmac-auth-credential
  namespace: javier
  labels:
    konghq.com/credential: hmac-auth
stringData:
  username: hmac-client
  secret: hmac-shared-secret
```

### 3. `12-hmac-auth-consumer.yaml`

This `KongConsumer` represents the user or application being authenticated. The `credentials` list references the credential Secret. KIC creates the Consumer and links the credential to it. In a database-backed deployment it is represented in `consumers` and in the relationship with its credential.

Definition of the `KongConsumer` resource:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: hmac-auth-client
  namespace: javier
  annotations: {kubernetes.io/ingress.class: kong}
username: hmac-client
credentials: [hmac-auth-credential]
```

### 4. `12-hmac-auth-httproute.yaml`

This `HTTPRoute` publishes the endpoint. `parentRefs` attaches it to the `kong` Gateway, `hostnames` limits the domain, and `PathPrefix` defines the path. `backendRefs` points to the existing `echo` Service from the KIC scenario. KIC primarily translates it into a Kong Route and a Service association, internally represented through Service, Upstream, and Targets. The `konghq.com/plugins` annotation links the plugin to the Route.

Definition of the `HTTPRoute` resource:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: hmac-auth
  namespace: javier
  annotations: {konghq.com/plugins: hmac-auth}
spec:
  parentRefs: [{name: kong, namespace: kong}]
  hostnames: [echo.javiercd.es]
  rules:
    - matches: [{path: {type: PathPrefix, value: /hmac-auth}}]
      backendRefs: [{name: echo, port: 80}]
```
