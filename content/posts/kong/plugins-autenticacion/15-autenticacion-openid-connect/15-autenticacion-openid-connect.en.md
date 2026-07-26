---
title: "OpenID Connect in Kong"
description: "Integrate Kong KIC with Keycloak using OpenID Connect and Gateway API."
weight: 15
---

This Enterprise lab uses `echo.javiercd.es/oidc` and a Keycloak issuer reachable from the Kong pods. Register `http://echo.javiercd.es/oidc/callback` in Keycloak, then configure `15-openid-connect-plugin.yaml` and apply it before `15-openid-connect-httproute.yaml`.

This VM has no Enterprise license, so KIC rejects the plugin. On a licensed installation, run `sudo ./apply-enterprise.sh` after configuring the IdP.

```bash
sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
vagrant ssh
cd ~/kic-auth
sudo kubectl get gateway kong -n kong
sudo kubectl get svc echo -n javier
sudo kubectl apply -f 15-openid-connect-plugin.yaml
sudo kubectl apply -f 15-openid-connect-httproute.yaml
exit
curl -i -L http://echo.javiercd.es/oidc
```

Complete the login in a browser. Use HTTPS and a secure cookie in production. See [OpenID Connect in Kong](https://developer.konghq.com/plugins/openid-connect/).

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
| `15-openid-connect-plugin.yaml` | `KongPlugin` | plugin configuration |
| `15-openid-connect-httproute.yaml` | `HTTPRoute` | Kong Route and backend association |

The `kong` Gateway and the `echo` Service already existed because they were created in the KIC installation post. Each `HTTPRoute` reuses that shared Gateway and Service.

## Lab files, step by step

### 1. `15-openid-connect-plugin.yaml`

This file creates a `KongPlugin`. The `plugin` field selects the plugin Kong will run and `config` contains its options. KIC translates this resource into a Kong plugin configuration. In a database-backed deployment it is represented in the `plugins` table, including its configuration and its Route or Consumer associations.

Definition of the `KongPlugin` resource:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: openid-connect
  namespace: javier
plugin: openid-connect
config:
  issuer: http://keycloak.kong.javiercd.es:8080/realms/kong-lab
  client_id: [kong-gateway]
  client_secret: [kong-gateway-secret]
  client_auth: [client_secret_post]
  auth_methods: [authorization_code, session]
  redirect_uri: [http://echo.javiercd.es/oidc/callback]
  session_secret: OIDCkicSessionSecret32bytesABC12
  session_storage: cookie
  session_cookie_secure: false
  session_cookie_http_only: true
  session_cookie_same_site: Lax
```

### 2. `15-openid-connect-httproute.yaml`

This `HTTPRoute` publishes the endpoint. `parentRefs` attaches it to the `kong` Gateway, `hostnames` limits the domain, and `PathPrefix` defines the path. `backendRefs` points to the existing `echo` Service from the KIC scenario. KIC primarily translates it into a Kong Route and a Service association, internally represented through Service, Upstream, and Targets. The `konghq.com/plugins` annotation links the plugin to the Route.

Definition of the `HTTPRoute` resource:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: openid-connect
  namespace: javier
  annotations: {konghq.com/plugins: openid-connect}
spec:
  parentRefs: [{name: kong, namespace: kong}]
  hostnames: [echo.javiercd.es]
  rules:
    - matches: [{path: {type: PathPrefix, value: /oidc}}]
      backendRefs: [{name: echo, port: 80}]
```
