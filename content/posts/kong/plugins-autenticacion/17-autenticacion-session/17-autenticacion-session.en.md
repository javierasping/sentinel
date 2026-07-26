---
title: "Session in Kong"
description: "Create a browser session after an initial Key Auth request."
weight: 17
---

Session is paired with Key Auth for the first request. The route is `echo.javiercd.es/session`. The lab separates the two plugins, their Consumers and credentials, and the HTTPRoute into seven `17-session-*.yaml` files. An anonymous Consumer with Request Termination explicitly rejects requests that have neither a session nor an API key.

```bash
sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
vagrant ssh
cd ~/kic-auth
sudo kubectl get gateway kong -n kong
sudo kubectl get svc echo -n javier
sudo kubectl apply -f 17-session-session-plugin.yaml
sudo kubectl apply -f 17-session-key-auth-plugin.yaml
sudo kubectl apply -f 17-session-secret.yaml
sudo kubectl apply -f 17-session-consumer.yaml
sudo kubectl apply -f 17-session-anonymous-plugin.yaml
sudo kubectl apply -f 17-session-anonymous-consumer.yaml
sudo kubectl apply -f 17-session-httproute.yaml
exit
rm -f cookies.txt
curl -i -c cookies.txt -H 'apikey: session-api-key' http://echo.javiercd.es/session
curl -i -b cookies.txt http://echo.javiercd.es/session
```

`cookie_secure: false` is for this HTTP lab only. Use HTTPS and secure cookies outside the lab.

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
| `17-session-session-plugin.yaml` | `KongPlugin` | session plugin configuration |
| `17-session-key-auth-plugin.yaml` | `KongPlugin` | Key Auth plugin configuration |
| `17-session-secret.yaml` | `Secret` | authentication credential |
| `17-session-consumer.yaml` | `KongConsumer` | Kong Consumer |
| `17-session-anonymous-plugin.yaml` | `KongPlugin` | request-termination plugin configuration |
| `17-session-anonymous-consumer.yaml` | `KongConsumer` | anonymous Kong Consumer |
| `17-session-httproute.yaml` | `HTTPRoute` | Kong Route and backend association |

The `kong` Gateway and the `echo` Service already existed because they were created in the KIC installation post. Each `HTTPRoute` reuses that shared Gateway and Service.

## Lab files, step by step

### 1. `17-session-session-plugin.yaml`

This file creates the Session `KongPlugin`. It configures cookie-based session storage and the security options used by this HTTP lab. KIC translates it into a Kong plugin entry. In a database-backed deployment it is represented in `plugins`.

Definition of the `KongPlugin` resource:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: session
  namespace: javier
plugin: session
config:
  storage: cookie
  cookie_secure: false
  cookie_http_only: true
  cookie_same_site: Strict
  secret: session-kic-secret-32-bytes-change-me
```

### 2. `17-session-key-auth-plugin.yaml`

This file creates a Key Auth `KongPlugin` so Session can accept the initial API key. `anonymous` identifies the Consumer used when a request has no credentials. KIC translates it into a Kong plugin entry. In a database-backed deployment it is represented in `plugins`.

Definition of the `KongPlugin` resource:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: session-key-auth
  namespace: javier
plugin: key-auth
config:
  key_names: [apikey]
  anonymous: anonymous-session
```

### 3. `17-session-secret.yaml`

This `Secret` contains the credential that KIC must convert for the related plugin. The `konghq.com/credential` label identifies the credential type. KIC does not use it as a backend environment variable. In a database-backed deployment it is represented in the plugin credential table and linked to the Consumer.

Definition of the `Secret` resource:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: session-key-credential
  namespace: javier
  labels: {konghq.com/credential: key-auth}
stringData: {key: session-api-key}
```

### 4. `17-session-consumer.yaml`

This `KongConsumer` represents the user or application being authenticated. The `credentials` list references the credential Secret. KIC creates the Consumer and links the credential to it. In a database-backed deployment it is represented in `consumers` and in the relationship with its credential.

Definition of the `KongConsumer` resource:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: session-client
  namespace: javier
  annotations: {kubernetes.io/ingress.class: kong}
username: session-client
credentials: [session-key-credential]
```

### 5. `17-session-anonymous-plugin.yaml`

This `KongPlugin` uses `request-termination` to return `403 Forbidden`. It is applied to the anonymous Consumer and acts as the rejection branch of this lab. In a database-backed deployment it is represented in `plugins`.

Definition of the `KongPlugin` resource:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: session-anonymous-deny
  namespace: javier
plugin: request-termination
config:
  status_code: 403
  message: Forbidden
```

### 6. `17-session-anonymous-consumer.yaml`

This `KongConsumer` represents anonymous requests. Its annotation applies the `request-termination` plugin, so a request without credentials receives `403` instead of reaching the backend. In a database-backed deployment it is represented in `consumers` and in the plugin association.

Definition of the `KongConsumer` resource:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: anonymous-session
  namespace: javier
  annotations:
    kubernetes.io/ingress.class: kong
    konghq.com/plugins: session-anonymous-deny
username: anonymous-session
```

### 7. `17-session-httproute.yaml`

This `HTTPRoute` publishes the endpoint. `parentRefs` attaches it to the `kong` Gateway, `hostnames` limits the domain, and `PathPrefix` defines the path. `backendRefs` points to the existing `echo` Service from the KIC scenario. KIC primarily translates it into a Kong Route and a Service association, internally represented through Service, Upstream, and Targets. The `konghq.com/plugins` annotation links the plugin to the Route.

Definition of the `HTTPRoute` resource:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: session
  namespace: javier
  annotations:
    konghq.com/plugins: "session,session-key-auth"
spec:
  parentRefs: [{name: kong, namespace: kong}]
  hostnames: [echo.javiercd.es]
  rules:
    - matches: [{path: {type: PathPrefix, value: /session}}]
      backendRefs: [{name: echo, port: 80}]
```
