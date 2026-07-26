---
title: "SAML in Kong"
description: "Publish a browser-based SAML flow behind Kong KIC."
weight: 16
---

SAML is an Enterprise, browser-oriented plugin. The route is `echo.javiercd.es/saml`. Replace the IdP certificate, SSO URL, issuer, and ACS settings in `16-saml-plugin.yaml`. The HTTPRoute is defined separately in `16-saml-httproute.yaml`:

This VM has no Enterprise license, so KIC rejects the plugin. On a licensed installation, run `sudo ./apply-enterprise.sh` after configuring the IdP.

```bash
sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
vagrant ssh
cd ~/kic-auth
sudo kubectl get gateway kong -n kong
sudo kubectl get svc echo -n javier
sudo kubectl apply -f 16-saml-plugin.yaml
sudo kubectl apply -f 16-saml-httproute.yaml
exit
curl -i -L http://echo.javiercd.es/saml
```

The complete exchange requires a browser and a real IdP. See the [official SAML plugin documentation](https://developer.konghq.com/plugins/saml/).

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
| `16-saml-plugin.yaml` | `KongPlugin` | plugin configuration |
| `16-saml-httproute.yaml` | `HTTPRoute` | Kong Route and backend association |

The `kong` Gateway and the `echo` Service already existed because they were created in the KIC installation post. Each `HTTPRoute` reuses that shared Gateway and Service.

## Lab files, step by step

### 1. `16-saml-plugin.yaml`

This file creates a `KongPlugin`. The `plugin` field selects the plugin Kong will run and `config` contains its options. KIC translates this resource into a Kong plugin configuration. In a database-backed deployment it is represented in the `plugins` table, including its configuration and its Route or Consumer associations.

Definition of the `KongPlugin` resource:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: saml
  namespace: javier
plugin: saml
config:
  idp_certificate: REPLACE_WITH_IDP_X509_CERTIFICATE
  idp_sso_url: https://idp.example.test/saml/sso
  issuer: https://echo.javiercd.es/saml
  assertion_consumer_path: /saml/callback
  session_secret: SAMLkicSessionSecret32bytesABC12
  session_storage: cookie
  validate_assertion_signature: true
```

### 2. `16-saml-httproute.yaml`

This `HTTPRoute` publishes the endpoint. `parentRefs` attaches it to the `kong` Gateway, `hostnames` limits the domain, and `PathPrefix` defines the path. `backendRefs` points to the existing `echo` Service from the KIC scenario. KIC primarily translates it into a Kong Route and a Service association, internally represented through Service, Upstream, and Targets. The `konghq.com/plugins` annotation links the plugin to the Route.

Definition of the `HTTPRoute` resource:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: saml
  namespace: javier
  annotations: {konghq.com/plugins: saml}
spec:
  parentRefs: [{name: kong, namespace: kong}]
  hostnames: [echo.javiercd.es]
  rules:
    - matches: [{path: {type: PathPrefix, value: /saml}}]
      backendRefs: [{name: echo, port: 80}]
```
