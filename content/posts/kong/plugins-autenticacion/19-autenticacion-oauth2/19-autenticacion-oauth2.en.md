---
title: "OAuth 2.0 in Kong"
description: "Why the OAuth2 Authentication plugin must use traditional topology."
weight: 19
---

The OAuth 2.0 Authentication plugin is intentionally not applied to the KIC installation. Kong documents that it requires `traditional` topology because it creates, deletes, and persists tokens in the database. The [`19-oauth2-configmap.yaml`](https://github.com/javiercruces/sentinel/blob/main/examples/kong/kic-auth/19-oauth2-configmap.yaml) file is only a guardrail.

For KIC, use [OAuth 2.0 Introspection](/posts/kong/plugins-autenticacion/14-autenticacion-oauth2-introspection/14-autenticacion-oauth2-introspection/) to validate tokens issued by an external IdP. If token issuance through Kong is required, create a separate traditional PostgreSQL deployment. See the [official OAuth2 documentation](https://developer.konghq.com/plugins/oauth2/).

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

There is no applicable `HTTPRoute` or `KongPlugin` in this lab. The `ConfigMap` only documents the incompatibility and creates no Kong entity.

## Create the explanatory ConfigMap

This is the only resource in this post. It does not activate OAuth 2.0 Authentication or create a Route. It records the decision inside the laboratory namespace:

```bash
vagrant ssh
cd ~/kic-auth
sudo kubectl apply -f 19-oauth2-configmap.yaml
sudo kubectl get configmap oauth2-kic-not-supported -n javier
exit
```

## Lab files, step by step

### 1. `19-oauth2-configmap.yaml`

This `ConfigMap` does not create OAuth2 authentication in Kong. It documents that the OAuth2 Authentication plugin is not part of this KIC lab. It is not translated into a `plugins`, `routes`, or `consumers` row. It is only a guardrail to prevent applying an incompatible configuration by mistake.

Definition of the `ConfigMap` resource:

```yaml
# OAuth2 Authentication is intentionally not a KIC lab. Kong documents it as
# traditional-only because it writes tokens to the database. This manifest is
# kept as a guardrail so it is not accidentally applied to the KIC Gateway.
apiVersion: v1
kind: ConfigMap
metadata:
  name: oauth2-kic-not-supported
  namespace: javier
data:
  reason: traditional-only
  route-host: echo.javiercd.es
  route-path: /oauth2
```
