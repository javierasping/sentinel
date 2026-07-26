---
title: "OAuth 2.0 Token Introspection in Kong"
date: 2026-07-26T00:00:00+02:00
description: "How to install an open-source OAuth 2.0 introspection plugin in Kong Gateway, deploy Keycloak, and protect an HTTPRoute with KIC."
tags: [Kong, OAuth 2.0, Token Introspection, Keycloak, KIC]
weight: 14
hero: images/kong/oauth2-introspection.png
aliases:
  - /posts/kong/plugins-autenticacion/oauth2/14-autenticacion-oauth2-introspection/14-autenticacion-oauth2-introspection/
---

Kong Enterprise includes an official OAuth 2.0 Introspection plugin, but it requires a license. In this lab, we will overcome that limitation by installing an open community or free-software plugin on Kong Gateway 3.10.

In addition to the plugin, we will deploy Keycloak in Kubernetes. Keycloak will issue access tokens through `client_credentials` and expose the introspection endpoint defined by RFC 7662. Every response shown in this article comes from this real scenario.

> [!NOTE]
> This lab continues from the [KIC installation](/posts/kong/03-instalacion-kic/03-instalacion-kic/) scenario. It reuses the `kong` Gateway, the `echo` Service, KIC `3.5`, and `192.168.121.200` as the address of `kong-gateway-proxy`.

> [!WARNING]
> [`revomatico/kong-oidc`](https://github.com/revomatico/kong-oidc) is published under the Apache-2.0 license, but the repository was archived in 2024. It is suitable for this lab and we tested it with Kong `3.10.0.16`, but it has no official Kong support or active maintenance. Before using it in production, we must audit it, maintain our own fork, and keep its dependencies updated.

## 1. What is token introspection?

A resource server may receive a token that it cannot validate locally. [RFC 7662](https://www.rfc-editor.org/rfc/rfc7662.html) defines an endpoint to which the server can send that token to query its status:

```http
POST /realms/kong-lab/protocol/openid-connect/token/introspect
Authorization: Basic <client-id:client-secret>
Content-Type: application/x-www-form-urlencoded

token=<access-token>
```

The main property in the response is `active`:

```json
{
  "active": true,
  "client_id": "kong-introspection",
  "username": "service-account-kong-introspection"
}
```

If the token has expired, has been revoked, or does not belong to the authorization server, the response is:

```json
{
  "active": false
}
```

In our scenario, Keycloak issues a JWT, but Kong does not validate its signature locally. It treats the token as a Bearer credential and queries Keycloak on every request. The same mechanism also works with opaque tokens.

There are two different credentials:

- The access token that the client presents to Kong.
- The `client_id` and `client_secret` that Kong uses to authenticate to Keycloak.

## 2. Lab architecture

The complete flow is:

![OAuth 2.0 introspection flow in Kong](/kong/plugins-autenticacion/14-autenticacion-oauth2-introspection/img/oauth2-introspection-flow-en.svg)

The client knows only its access token. Kong uses separate credentials to query Keycloak's introspection endpoint. The plugin reaches `echo` when it receives `active: true` and returns `401 Unauthorized` when the token is not active.

We will use these components:

| Component | Version | Purpose |
| --- | --- | --- |
| Kong Gateway | `3.10.0.16` | Proxy and plugin execution |
| KIC | `3.5` | Translation of `KongPlugin` and `HTTPRoute` resources |
| `revomatico/kong-oidc` | `v1.4.0-1` | Introspection through an open community or free-software plugin |
| `lua-resty-openidc` | `v1.7.6` | RFC 7662 client used by the plugin |
| Keycloak | `26.7.0` | Token issuance and introspection |

We do not use the Enterprise name `oauth2-introspection` in the `plugin` field. The Kubernetes resource keeps that name to describe the lab, but it loads the open community or free-software `oidc` plugin.

## 3. Install the open community or free-software plugin

Kong can distribute Lua plugins through a `ConfigMap`. The code is mounted in the pod, and `KONG_PLUGINS` tells Kong which modules to load.

The [`14-install-community-oidc.sh`](https://github.com/javierasping/kong/blob/main/posts/14-autenticacion-oauth2-introspection/14-install-community-oidc.sh) script performs these operations:

1. Downloads `revomatico/kong-oidc` from the `v1.4.0-1` tag.
2. Downloads `lua-resty-openidc` from the `v1.7.6` tag.
3. Verifies the SHA-256 checksum of every file.
4. Creates the `kong-plugin-oidc` and `kong-resty-openidc` `ConfigMap` resources.
5. Upgrades the Kong Helm release.
6. Waits for the new pod to pass its readiness probes.

Pinned versions and checksums are important. Downloading a changing branch during every deployment would make it impossible to know exactly which code the Gateway is running.

### 3.1. Helm values

The `14-community-oidc-values.yaml` file contains:

```yaml
gateway:
  image:
    repository: kong/kong-gateway
    tag: "3.10"
  proxy:
    loadBalancerIP: 192.168.121.200
  plugins:
    configMaps:
      - name: kong-plugin-oidc
        pluginName: oidc
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

`gateway.plugins.configMaps` mounts the Lua files at `/opt/kong/plugins/oidc` and adds `oidc` to `KONG_PLUGINS`. The additional volume places `openidc.lua` under `/opt/resty`, a location included in `KONG_LUA_PACKAGE_PATH`.

We also preserve the 3.10 image and the MetalLB address. Otherwise, a Helm upgrade could restore the chart's default Kong image or release `.200`.

### 3.2. Run the installation

Inside the VM:

```bash
cd ~/kic-auth
chmod +x 14-install-community-oidc.sh
./14-install-community-oidc.sh
```

The real result is:

```text
configmap/kong-plugin-oidc created
configmap/kong-resty-openidc created
Release "kong" has been upgraded. Happy Helming!
STATUS: deployed
deployment "kong-gateway" successfully rolled out
Open community or free-software oidc plugin installed in Kong Gateway.
```

Check the version, IP address, and loaded plugins:

```bash
sudo kubectl exec -n kong deployment/kong-gateway \
  -c proxy -- kong version

sudo kubectl get service kong-gateway-proxy -n kong

sudo kubectl get deployment kong-gateway -n kong \
  -o jsonpath='{.spec.template.spec.containers[?(@.name=="proxy")].env[?(@.name=="KONG_PLUGINS")].value}{"\n"}'
```

```text
Kong Enterprise 3.10.0.16
bundled,oidc
```

The fact that the binary identifies itself as Enterprise does not mean that a license is installed. The `oidc` plugin we have just loaded is free software maintained by the community and does not depend on an Enterprise license.

## 4. Deploy Keycloak

The `14-keycloak.yaml` file contains a `ConfigMap`, a `Deployment`, and a `Service`.

### 4.1. Import the realm

The main part of the realm is:

```json
{
  "realm": "kong-lab",
  "enabled": true,
  "accessTokenLifespan": 60,
  "clients": [
    {
      "clientId": "kong-introspection",
      "enabled": true,
      "protocol": "openid-connect",
      "publicClient": false,
      "secret": "client-secret",
      "standardFlowEnabled": false,
      "directAccessGrantsEnabled": false,
      "serviceAccountsEnabled": true,
      "protocolMappers": [
        {
          "name": "kong-introspection-audience",
          "protocol": "openid-connect",
          "protocolMapper": "oidc-audience-mapper",
          "config": {
            "included.client.audience": "kong-introspection",
            "access.token.claim": "true"
          }
        }
      ]
    }
  ]
}
```

Tokens remain valid for sixty seconds. This gives us enough time to perform a manual test while remaining short enough to demonstrate expiration. The mapper adds `kong-introspection` to `aud`. Keycloak 26 rejects introspection when the requesting client is not included in the token audience.

The client only allows `client_credentials`. We do not enable interactive login or the password grant.

### 4.2. Deployment and canonical hostname

The relevant container configuration is:

```yaml
containers:
  - name: keycloak
    image: quay.io/keycloak/keycloak:26.7.0
    args:
      - start-dev
      - --import-realm
    env:
      - name: KC_BOOTSTRAP_ADMIN_USERNAME
        value: admin
      - name: KC_BOOTSTRAP_ADMIN_PASSWORD
        value: admin
      - name: KC_HOSTNAME
        value: http://keycloak.javier.svc.cluster.local:8080
      - name: JAVA_OPTS_KC_HEAP
        value: -Xms256m -Xmx512m
```

`KC_HOSTNAME` prevents a subtle error: if we obtain the token through a port forward and Keycloak uses `127.0.0.1` as its issuer, Kong will later send it to the internal DNS name and Keycloak will reject the JWT because `iss` does not match. Setting the `Service` hostname ensures that token issuance and introspection use the same issuer.

This deployment uses `start-dev` and ephemeral H2 storage. It is deliberately a lab setup, not a production configuration.

## 5. Store the introspection secret

Create `14-oidc-client-secret.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: oidc-introspection-client
  namespace: javier
stringData:
  client-secret: '"client-secret"'
type: Opaque
```

The double quotes are part of the value because `configPatches` interprets the content as JSON. A `Secret` does not encrypt the value. It keeps it out of the `KongPlugin` and allows us to apply RBAC controls.

## 6. Configure the `KongPlugin`

The `14-oauth2-introspection-plugin.yaml` file contains:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: oauth2-introspection
  namespace: javier
plugin: oidc
config:
  client_id: kong-introspection
  discovery: http://keycloak.javier.svc.cluster.local:8080/realms/kong-lab/.well-known/openid-configuration
  introspection_endpoint: http://keycloak.javier.svc.cluster.local:8080/realms/kong-lab/protocol/openid-connect/token/introspect
  introspection_endpoint_auth_method: client_secret_basic
  introspection_cache_ignore: "yes"
  bearer_only: "yes"
  realm: javier-oauth2-introspection
  ssl_verify: "no"
configPatches:
  - path: /client_secret
    valueFrom:
      secretKeyRef:
        name: oidc-introspection-client
        key: client-secret
```

- `plugin: oidc` selects the open community or free-software plugin.
- `bearer_only: "yes"` disables browser redirects: a request without a Bearer token returns `401`.
- `introspection_endpoint_auth_method` makes Kong use HTTP Basic when connecting to Keycloak.
- `introspection_cache_ignore: "yes"` forces a status query on every request. This is useful for observing expiration immediately.
- `realm` appears in `WWW-Authenticate`.
- `configPatches` retrieves the secret through KIC 3.5 before sending the configuration to Kong.
- `ssl_verify: "no"` is acceptable only because the lab IdP uses internal HTTP.

## 7. Publish the route

The `HTTPRoute` applies the `KongPlugin` only to `/oauth2-introspection`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: oauth2-introspection
  namespace: javier
  annotations:
    konghq.com/plugins: oauth2-introspection
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
            value: /oauth2-introspection
      backendRefs:
        - name: echo
          port: 80
```

Apply everything with:

```bash
cd ~/kic-auth
chmod +x 14-deploy-community-oidc-lab.sh
./14-deploy-community-oidc-lab.sh
```

The script first validates the plugin schema with `--dry-run=server`. If `oidc` is not loaded, it stops before publishing the route. It also restarts the Keycloak Deployment after applying the `ConfigMap`, because the realm is imported only at startup.

## 8. Test introspection

### 8.1. Request without a token

```bash
curl -i http://echo.javiercd.es/oauth2-introspection
```

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 14:25:08 GMT
Content-Type: application/json; charset=utf-8
WWW-Authenticate: Bearer realm="javier-oauth2-introspection",error="no Authorization header found"
X-Kong-Response-Latency: 1
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 53d12f1d1758227f11cb807895683b32

{
  "message":"Unauthorized",
  "request_id":"53d12f1d1758227f11cb807895683b32"
}
```

### 8.2. Unknown token

```bash
curl -i \
  -H 'Authorization: Bearer token-inventado' \
  http://echo.javiercd.es/oauth2-introspection
```

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 14:25:08 GMT
Content-Type: application/json; charset=utf-8
WWW-Authenticate: Bearer realm="javier-oauth2-introspection",error="invalid token"
X-Kong-Response-Latency: 3
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 09af500ea95a0658315e687637489361

{
  "message":"Unauthorized",
  "request_id":"09af500ea95a0658315e687637489361"
}
```

### 8.3. Obtain a real token

Temporarily forward the Keycloak Service inside the VM:

```bash
sudo kubectl port-forward -n javier service/keycloak 18080:8080
```

In another terminal:

```bash
TOKEN_RESPONSE="$(curl -sS \
  -u kong-introspection:client-secret \
  -d 'grant_type=client_credentials' \
  http://127.0.0.1:18080/realms/kong-lab/protocol/openid-connect/token)"

ACCESS_TOKEN="$(echo "${TOKEN_RESPONSE}" \
  | sed -n 's/.*"access_token":"\([^"]*\)".*/\1/p')"

EXPIRES_IN="$(echo "${TOKEN_RESPONSE}" \
  | sed -n 's/.*"expires_in":\([0-9]*\).*/\1/p')"

test -n "${ACCESS_TOKEN}"
test -n "${EXPIRES_IN}"
```

The real response, abbreviating only the temporary credential, is:

```json
{
  "access_token": "<access-token>",
  "expires_in": 60,
  "refresh_expires_in": 0,
  "token_type": "Bearer",
  "not-before-policy": 0,
  "scope": "email profile"
}
```

We can query RFC 7662 directly:

```bash
curl -sS \
  -u kong-introspection:client-secret \
  --data-urlencode "token=${ACCESS_TOKEN}" \
  http://127.0.0.1:18080/realms/kong-lab/protocol/openid-connect/token/introspect
```

This is a complete, real response from the introspection endpoint for an active token:

```json
{
  "exp": 1785089806,
  "iat": 1785089746,
  "jti": "trrtcc:d2c36e46-acad-37b7-f91b-6abc60d0d4a0",
  "iss": "http://keycloak.javier.svc.cluster.local:8080/realms/kong-lab",
  "aud": [
    "kong-introspection",
    "account"
  ],
  "sub": "487121b1-22ad-4f6f-93f0-babfa3309442",
  "typ": "Bearer",
  "azp": "kong-introspection",
  "acr": "1",
  "realm_access": {
    "roles": [
      "default-roles-kong-lab",
      "offline_access",
      "uma_authorization"
    ]
  },
  "resource_access": {
    "account": {
      "roles": [
        "manage-account",
        "manage-account-links",
        "view-profile"
      ]
    }
  },
  "scope": "email profile",
  "email_verified": false,
  "preferred_username": "service-account-kong-introspection",
  "client_id": "kong-introspection",
  "username": "service-account-kong-introspection",
  "token_type": "Bearer",
  "active": true
}
```

`iat` indicates when the token was issued and `exp` when it stops being valid. In this example, there are exactly 60 seconds between both values. `active: true` confirms that Keycloak still considers it valid at the time of the query.

### 8.4. Active token

We must send this request before the number of seconds indicated by `expires_in` has elapsed:

```bash
curl -i \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  http://echo.javiercd.es/oauth2-introspection
```

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: 28
X-App-Name: http-echo
X-App-Version: 1.0.0
Date: Sun, 26 Jul 2026 18:11:32 GMT
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Upstream-Latency: 0
X-Kong-Proxy-Latency: 8
Via: 1.1 kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 65b4012a5e99543f246b7336a747aa42

Hola desde Kong Gateway KIC
```

### 8.5. The same token after expiration

Wait until the lifetime reported by Keycloak has elapsed and repeat the exact same request:

```bash
curl -i \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  http://echo.javiercd.es/oauth2-introspection
```

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 18:12:44 GMT
Content-Type: application/json; charset=utf-8
WWW-Authenticate: Bearer realm="javier-oauth2-introspection",error="invalid token"
X-Kong-Response-Latency: 6
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 6a17c37134a8e67d9d3f300cf65c5454

{
  "message":"Unauthorized",
  "request_id":"6a17c37134a8e67d9d3f300cf65c5454"
}
```

This result proves that Kong does more than recognize the token format: it queries its status and stops accepting it as soon as Keycloak reports that it is no longer active.

> [!WARNING]
> A `401` response with `error="invalid token"` is also the correct response when the token has expired. Compare the request time with the `iat` and `exp` values in the introspection response. For example, a token with `iat=1785089182` was issued at `18:06:22 UTC`, and with `exp=1785089192` it expired at `18:06:32 UTC`. A request that reaches Kong at `18:06:43 UTC` must receive `401`.

## Sources

- [RFC 7662: OAuth 2.0 Token Introspection](https://www.rfc-editor.org/rfc/rfc7662.html)
- [revomatico/kong-oidc v1.4.0-1](https://github.com/revomatico/kong-oidc/releases/tag/v1.4.0-1)
- [lua-resty-openidc v1.7.6](https://github.com/zmartzone/lua-resty-openidc/releases/tag/v1.7.6)
- [Kong: custom plugin deployment](https://developer.konghq.com/custom-plugins/deployment-options/)
- [KIC: custom plugins](https://developer.konghq.com/kubernetes-ingress-controller/custom-plugins/)
- [KIC: secrets in plugins](https://developer.konghq.com/kubernetes-ingress-controller/reference/secrets-in-plugins/)
- [Keycloak: running in containers](https://www.keycloak.org/server/containers)
- [Keycloak: importing and exporting realms](https://www.keycloak.org/server/importExport)
- [Keycloak: introspection endpoint](https://www.keycloak.org/securing-apps/oidc-layers)
