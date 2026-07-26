---
title: "OpenID Connect in Kong"
date: 2026-07-26T00:00:00+02:00
description: "How to install an open-source OpenID Connect alternative, deploy Keycloak, and complete Authorization Code with KIC."
tags: [Kong, OpenID Connect, OAuth 2.0, Keycloak, KIC]
weight: 15
hero: images/kong/openid-connect.png
---

Kong's official OpenID Connect plugin requires an Enterprise license. In this lab, we use the open community or free-software [`cuongntr/kong-openid-connect-plugin`](https://github.com/cuongntr/kong-openid-connect-plugin) adapter on top of [`lua-resty-openidc`](https://github.com/zmartzone/lua-resty-openidc) to complete an Authorization Code flow without a license.

We will deploy a separate Keycloak instance in Kubernetes, log in with a real user, and verify both the callback and cookie reuse. Every response in this article comes from the lab VM.

> [!NOTE]
> This lab continues from [Installing KIC](/posts/kong/03-instalacion-kic/03-instalacion-kic/). It reuses the `kong` Gateway, the `echo` Service, KIC `3.5`, and `192.168.121.200` as the `kong-gateway-proxy` address.

> [!WARNING]
> `kong-openid-connect-plugin` is not archived, uses the modern plugin API, and declares compatibility with Kong 3.x, but it is a young project: its latest commit is from July 2025, it has few contributors, and it offers no official support. The underlying `lua-resty-openidc` library is active and released `v1.9.0` in July 2026. We pin versions and checksums, but a production deployment should audit the adapter and maintain its own fork.

## 1. What is OpenID Connect?

OAuth 2.0 defines how to obtain authorization to access resources. OpenID Connect adds an identity layer that allows an application to delegate login to an identity provider.

The Authorization Code flow in this lab works as follows:

1. The browser requests `/oidc`.
2. Kong creates `state` and `nonce`, stores state in a cookie, and redirects to Keycloak.
3. Keycloak authenticates the user.
4. The browser returns a temporary code to Kong's callback.
5. Kong exchanges the code for tokens directly with Keycloak.
6. Kong validates the response and creates a session.
7. Later requests reuse the cookie without repeating login.

The code is not an access token, and the `client_secret` never reaches the browser.

## 2. Lab components and flow

![OpenID Connect Authorization Code flow in Kong](/kong/plugins-autenticacion/15-autenticacion-openid-connect/img/openid-connect-flow-en.svg)

The browser never gives the password to Kong. Keycloak authenticates `alice` and returns a single-use authorization code. Kong validates the callback, exchanges the code for tokens, and creates an encrypted session before proxying the request to the `echo` service.

| Component | Version | Purpose |
| --- | --- | --- |
| Kong Gateway | `3.10.0.16` | Proxy and plugin execution |
| KIC | `3.5` | Translation of `KongPlugin` and `HTTPRoute` |
| `kong-openid-connect-plugin` | commit `a4ff261` | OIDC adapter for Kong 3.x |
| `lua-resty-openidc` | `v1.9.0` | OpenID Connect implementation |
| Keycloak | `26.7.0` | Identity provider |

The official plugin is named `openid-connect`. To avoid ambiguity, this lab explicitly loads `plugin: kong-openid-connect`.

## 3. Install the open community or free-software plugin

The [`15-install-community-oidc.sh`](https://github.com/javierasping/kong/blob/main/posts/15-autenticacion-openid-connect/15-install-community-oidc.sh) script:

1. Downloads the adapter from the pinned commit.
2. Downloads `lua-resty-openidc v1.9.0`.
3. Verifies all four SHA-256 checksums.
4. Creates the plugin and library `ConfigMap` resources.
5. Preserves the `oidc` plugin used by post 14.
6. upgrades the Helm release and waits for the new pod.

The relevant Helm values are:

```yaml
gateway:
  plugins:
    configMaps:
      - name: kong-plugin-oidc
        pluginName: oidc
      - name: kong-plugin-openid-connect
        pluginName: kong-openid-connect
  deployment:
    userDefinedVolumes:
      - name: kong-resty-openidc
        configMap:
          name: kong-resty-openidc
    userDefinedVolumeMounts:
      - name: kong-resty-openidc
        mountPath: /opt/resty
        readOnly: true
```

Run inside the VM:

```bash
cd ~/kic-auth
chmod +x 15-install-community-oidc.sh
./15-install-community-oidc.sh
```

Verify the loaded plugins:

```bash
sudo kubectl get deployment kong-gateway -n kong \
  -o jsonpath='{.spec.template.spec.containers[?(@.name=="proxy")].env[?(@.name=="KONG_PLUGINS")].value}{"\n"}'
```

```text
bundled,oidc,kong-openid-connect
```

## 4. Deploy Keycloak

`15-keycloak.yaml` imports the `kong-oidc-lab` realm with:

- The confidential `kong-gateway` client.
- Authorization Code enabled.
- Callback `http://echo.javiercd.es/oidc/callback`.
- User `alice` with password `alice-password`.

A separate `HTTPRoute` publishes Keycloak at:

```text
http://keycloak.192.168.121.200.nip.io
```

The `nip.io` hostname resolves to `192.168.121.200` from both the browser and the pods, so all endpoints advertised by discovery are reachable through both channels.

> [!WARNING]
> Keycloak uses `start-dev`, ephemeral H2 storage, HTTP, and sample credentials. This setup is for the lab only.

## 5. Store the secrets

`15-openid-connect-secrets.yaml` keeps both secrets out of the `KongPlugin`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: openid-connect-secrets
  namespace: javier
stringData:
  client-secret: '"kong-gateway-secret"'
  session-secret: '"OIDCkicSessionSecret32bytesABC12"'
type: Opaque
```

The double quotes are part of each value because KIC treats `configPatches` values as JSON.

## 6. Configure the `KongPlugin`

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: openid-connect
  namespace: javier
plugin: kong-openid-connect
config:
  client_id: kong-gateway
  discovery: http://keycloak.192.168.121.200.nip.io/realms/kong-oidc-lab/.well-known/openid-configuration
  redirect_uri: http://echo.javiercd.es/oidc/callback
  scope: openid profile email
  response_type: code
  token_endpoint_auth_method: client_secret_post
  session_cookie_name: kong_oidc_session
  session_cookie_lifetime: 3600
  session_storage: cookie
  session_cookie_secure: false
  session_cookie_httponly: true
  session_cookie_samesite: Lax
  ssl_verify: false
configPatches:
  - path: /client_secret
    valueFrom:
      secretKeyRef:
        name: openid-connect-secrets
        key: client-secret
  - path: /session_secret
    valueFrom:
      secretKeyRef:
        name: openid-connect-secrets
        key: session-secret
```

`session_cookie_secure: false` and `ssl_verify: false` are acceptable only because the entire lab uses HTTP.

## 7. Publish and deploy the routes

The protected route uses `/oidc`, which also covers `/oidc/callback`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: openid-connect
  namespace: javier
  annotations:
    konghq.com/plugins: openid-connect
spec:
  parentRefs:
    - name: kong
      namespace: kong
  hostnames:
    - echo.javiercd.es
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /oidc
      backendRefs:
        - name: echo
          port: 80
```

Deploy the lab:

```bash
cd ~/kic-auth
chmod +x 15-deploy-community-oidc-lab.sh
./15-deploy-community-oidc-lab.sh
```

The script validates the schema first, restarts Keycloak to import the realm, and only then publishes the routes.

## 8. Test Authorization Code

### 8.1. Initial redirect

```bash
curl -sS -D - -o /dev/null http://echo.javiercd.es/oidc
```

Real response, abbreviating only the cookie, `state`, and `nonce`:

```http
HTTP/1.1 302 Moved Temporarily
Date: Sun, 26 Jul 2026 18:30:12 GMT
Set-Cookie: session=<encrypted-cookie>; Path=/; SameSite=Lax; HttpOnly
Location: http://keycloak.192.168.121.200.nip.io/realms/kong-oidc-lab/protocol/openid-connect/auth?scope=openid%20profile%20email&nonce=<nonce>&client_id=kong-gateway&redirect_uri=http%3A%2F%2Fecho.javiercd.es%2Foidc%2Fcallback&state=<state>&response_type=code
X-Kong-Response-Latency: 73
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: ed129124d4228f45464e0f09105a0a41
```

### 8.2. Login and callback

Open `http://echo.javiercd.es/oidc` in a browser and sign in:

```text
Username: alice
Password: alice-password
```

The first screenshot shows the redirect from Kong to the `kong-oidc-lab` realm sign-in form in Keycloak:

![Keycloak sign-in form during the OpenID Connect flow](/kong/plugins-autenticacion/15-autenticacion-openid-connect/img/oidc-keycloak-login.png)

The real response after the callback is:

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: 28
Date: Sun, 26 Jul 2026 18:30:45 GMT
X-Kong-Upstream-Latency: 1
X-Kong-Proxy-Latency: 0
X-Kong-Request-Id: 9eff8c47538e9f09c0749f576573fb17

Hola desde Kong Gateway KIC
```

The second screenshot confirms that Keycloak returned the browser to the callback, Kong validated the Authorization Code, and the authenticated request reached the `echo` service:

![Echo service response after completing OpenID Connect in Kong](/kong/plugins-autenticacion/15-autenticacion-openid-connect/img/oidc-authenticated-response.png)

A second request with the same cookie returns `200` without displaying the login form again.

## Sources

- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- [cuongntr/kong-openid-connect-plugin](https://github.com/cuongntr/kong-openid-connect-plugin)
- [kong-openid-connect on LuaRocks](https://luarocks.org/modules/cuongntr/kong-openid-connect)
- [lua-resty-openidc v1.9.0](https://github.com/zmartzone/lua-resty-openidc/releases/tag/v1.9.0)
- [Kong: custom plugin deployment](https://developer.konghq.com/custom-plugins/deployment-options/)
- [KIC: custom plugins](https://developer.konghq.com/kubernetes-ingress-controller/custom-plugins/)
- [KIC: secrets in plugins](https://developer.konghq.com/kubernetes-ingress-controller/reference/secrets-in-plugins/)
- [Keycloak: configuring the hostname](https://www.keycloak.org/server/hostname)
