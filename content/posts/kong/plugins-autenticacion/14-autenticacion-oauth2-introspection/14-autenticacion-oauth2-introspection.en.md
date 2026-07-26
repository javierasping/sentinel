---
title: "OAuth 2.0 Introspection in Kong"
description: "Validate opaque OAuth access tokens through an external IdP."
weight: 14
---

This Enterprise lab uses `echo.javiercd.es/oauth2-introspection`. Replace the introspection URL and authorization value in `14-oauth2-introspection-plugin.yaml`. The separate HTTPRoute is in `14-oauth2-introspection-httproute.yaml`.

This VM has no Enterprise license, so KIC rejects the `KongPlugin` with an enterprise-only plugin error. On a licensed installation, run `sudo ./apply-enterprise.sh` after configuring the IdP. The script validates all manifests first so a failed license check does not leave orphan `HTTPRoute` objects.

```bash
sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
vagrant ssh
cd ~/kic-auth
sudo kubectl get gateway kong -n kong
sudo kubectl get svc echo -n javier
sudo kubectl apply -f 14-oauth2-introspection-plugin.yaml
sudo kubectl apply -f 14-oauth2-introspection-httproute.yaml
exit
curl -i -H 'Authorization: Bearer REAL_ACCESS_TOKEN' http://echo.javiercd.es/oauth2-introspection
```

An active token returns `200`. An expired or revoked token returns `401`. See the [official plugin documentation](https://developer.konghq.com/plugins/oauth2-introspection/).

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
| `14-oauth2-introspection-plugin.yaml` | `KongPlugin` | plugin configuration |
| `14-oauth2-introspection-httproute.yaml` | `HTTPRoute` | Kong Route and backend association |

The `kong` Gateway and the `echo` Service already existed because they were created in the KIC installation post. Each `HTTPRoute` reuses that shared Gateway and Service.

## Lab files, step by step

### 1. `14-oauth2-introspection-plugin.yaml`

This file creates a `KongPlugin`. The `plugin` field selects the plugin Kong will run and `config` contains its options. KIC translates this resource into a Kong plugin configuration. In a database-backed deployment it is represented in the `plugins` table, including its configuration and its Route or Consumer associations.

Definition of the `KongPlugin` resource:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: oauth2-introspection
  namespace: javier
plugin: oauth2-introspection
config:
  introspection_url: http://keycloak.kong.javiercd.es:8080/realms/kong-lab/protocol/openid-connect/token/introspect
  authorization_value: Basic REPLACE_WITH_BASE64_CLIENT_CREDENTIALS
  token_type_hint: access_token
  ttl: 30
```

### 2. `14-oauth2-introspection-httproute.yaml`

This `HTTPRoute` publishes the endpoint. `parentRefs` attaches it to the `kong` Gateway, `hostnames` limits the domain, and `PathPrefix` defines the path. `backendRefs` points to the existing `echo` Service from the KIC scenario. KIC primarily translates it into a Kong Route and a Service association, internally represented through Service, Upstream, and Targets. The `konghq.com/plugins` annotation links the plugin to the Route.

Definition of the `HTTPRoute` resource:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: oauth2-introspection
  namespace: javier
  annotations: {konghq.com/plugins: oauth2-introspection}
spec:
  parentRefs: [{name: kong, namespace: kong}]
  hostnames: [echo.javiercd.es]
  rules:
    - matches: [{path: {type: PathPrefix, value: /oauth2-introspection}}]
      backendRefs: [{name: echo, port: 80}]
```
