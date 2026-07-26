---
title: "LDAP Auth in Kong"
description: "Validate username and password against LDAP from a KIC HTTPRoute."
weight: 18
---

This open source lab publishes `echo.javiercd.es/ldap-auth`. Replace the LDAP host, base DN, attribute, and TLS settings in `18-ldap-plugin.yaml`. The HTTPRoute is defined separately in `18-ldap-httproute.yaml`:

```bash
sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
vagrant ssh
cd ~/kic-auth
sudo kubectl get gateway kong -n kong
sudo kubectl get svc echo -n javier
sudo kubectl apply -f 18-ldap-plugin.yaml
sudo kubectl apply -f 18-ldap-httproute.yaml
exit
LDAP_AUTH="$(printf '%s' 'riemann:password' | base64 -w0)"
curl -i -H "Authorization: ldap ${LDAP_AUTH}" http://echo.javiercd.es/ldap-auth
```

LDAP Auth does not use Basic Auth syntax. Use `Authorization: ldap <base64(username:password)>`. The Forumsys lab account `riemann:password` works with this manifest. Replace it with your own directory credentials. Use `verify_ldap_host: true` and a trusted CA in production. See the [official LDAP Authentication documentation](https://developer.konghq.com/plugins/ldap-auth/).

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
| `18-ldap-plugin.yaml` | `KongPlugin` | plugin configuration |
| `18-ldap-httproute.yaml` | `HTTPRoute` | Kong Route and backend association |

The `kong` Gateway and the `echo` Service already existed because they were created in the KIC installation post. Each `HTTPRoute` reuses that shared Gateway and Service.

## Lab files, step by step

### 1. `18-ldap-plugin.yaml`

This file creates a `KongPlugin`. The `plugin` field selects the plugin Kong will run and `config` contains its options. KIC translates this resource into a Kong plugin configuration. In a database-backed deployment it is represented in the `plugins` table, including its configuration and its Route or Consumer associations.

Definition of the `KongPlugin` resource:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: ldap-auth
  namespace: javier
plugin: ldap-auth
config:
  ldap_host: ldap.forumsys.com
  ldap_port: 389
  start_tls: false
  ldaps: false
  base_dn: dc=example,dc=com
  attribute: uid
  header_type: ldap
  verify_ldap_host: false
```

### 2. `18-ldap-httproute.yaml`

This `HTTPRoute` publishes the endpoint. `parentRefs` attaches it to the `kong` Gateway, `hostnames` limits the domain, and `PathPrefix` defines the path. `backendRefs` points to the existing `echo` Service from the KIC scenario. KIC primarily translates it into a Kong Route and a Service association, internally represented through Service, Upstream, and Targets. The `konghq.com/plugins` annotation links the plugin to the Route.

Definition of the `HTTPRoute` resource:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: ldap-auth
  namespace: javier
  annotations: {konghq.com/plugins: ldap-auth}
spec:
  parentRefs: [{name: kong, namespace: kong}]
  hostnames: [echo.javiercd.es]
  rules:
    - matches: [{path: {type: PathPrefix, value: /ldap-auth}}]
      backendRefs: [{name: echo, port: 80}]
```
