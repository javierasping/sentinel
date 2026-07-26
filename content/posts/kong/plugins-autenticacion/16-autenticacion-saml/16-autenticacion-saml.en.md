---
title: "SAML in Kong through Keycloak"
date: 2026-07-26T00:00:00+02:00
description: "How to protect a Kong route with SAML 2.0 by using Keycloak as a broker and an open-source OpenID Connect plugin."
tags: [Kong, SAML, OpenID Connect, Keycloak, KIC]
weight: 16
hero: images/kong/saml.png
---

Kong's official [`saml`](https://developer.konghq.com/plugins/saml/) plugin requires an Enterprise license. After reviewing the open community and free-software alternatives, I could not find a direct, maintained SAML plugin compatible with Kong 3.x that would be responsible to recommend.

This lab therefore uses a different, fully open architecture: Keycloak acts as the SAML Service Provider and identity broker, while Kong uses the open community or free-software `kong-openid-connect` plugin installed in the previous article. User authentication still performs a real SAML request and response. Keycloak validates the signed XML and returns an OpenID Connect Authorization Code to Kong.

Every response shown in this article comes from the lab VM.

> [!WARNING]
> Kong's official SAML plugin is proprietary and cannot be used without an Enterprise license. This solution is neither a reimplementation nor a drop-in replacement for its API: it terminates SAML at Keycloak and uses OIDC between Keycloak and Kong.

> [!NOTE]
> This lab continues from [OpenID Connect in Kong](/posts/kong/plugins-autenticacion/15-autenticacion-openid-connect/15-autenticacion-openid-connect/). It reuses `kong-openid-connect`, the `kong` Gateway, the `echo` Service, KIC `3.5`, and `192.168.121.200`.

## 1. Why use a broker?

SAML 2.0 exchanges authentication data through XML, digital signatures, metadata, an issuer, an audience, and an Assertion Consumer Service (`ACS`). Implementing all those checks correctly inside a small Lua plugin would create an unnecessary security risk.

Keycloak is an active open-source project with identity brokering and SAML provider support. Each component handles the protocol it understands:

- Keycloak creates the `SAMLRequest`.
- The IdP authenticates the user and signs the `SAMLResponse`.
- Keycloak validates the assertion signature, destination, audience, and time bounds.
- Keycloak converts the SAML identity into an OIDC session.
- Kong validates OIDC and protects the route.

No `KongConsumer` is required: the IdP, broker realm, and OIDC plugin resolve identity and session state.

## 2. Complete lab flow

![SAML flow through Keycloak and Kong](/kong/plugins-autenticacion/16-autenticacion-saml/img/saml-flow-en.svg)

Kong participates only in the OpenID Connect segment. The `kong-saml-broker` realm acts as the SAML Service Provider, sends the `AuthnRequest` to the IdP, and validates the signed `SAMLResponse`. It then transforms that identity into an OIDC code that Kong can validate to create the session.

The self-contained scenario uses two realms in one Keycloak instance:

| Realm | Purpose |
| --- | --- |
| `saml-idp` | SAML IdP and user `alice` |
| `kong-saml-broker` | SAML SP for the IdP and OIDC provider for Kong |

In production, Entra ID, Okta, ADFS, or another corporate IdP would replace `saml-idp`.

## 3. Requirement: install the open community or free-software plugin

The bridge reuses the adapter from post 15, pinned to commit `a4ff261`, and `lua-resty-openidc v1.9.0`:

```bash
cd ~/kic-auth
chmod +x 15-install-community-oidc.sh
./15-install-community-oidc.sh
```

Verify that Kong loaded it:

```bash
sudo kubectl get deployment kong-gateway -n kong \
  -o jsonpath='{.spec.template.spec.containers[?(@.name=="proxy")].env[?(@.name=="KONG_PLUGINS")].value}{"\n"}'
```

```text
bundled,oidc,kong-openid-connect
```

## 4. Deploy the SAML realms

`16-keycloak.yaml` creates a `ConfigMap`, a `Deployment`, and a `Service`. The first realm registers Kong's OIDC client:

```json
{
  "clientId": "kong-saml-gateway",
  "protocol": "openid-connect",
  "publicClient": false,
  "secret": "kong-saml-gateway-secret",
  "standardFlowEnabled": true,
  "redirectUris": ["http://echo.javiercd.es/saml/callback"]
}
```

The `saml-idp` realm registers the broker as its Service Provider:

```json
{
  "clientId": "http://saml.192.168.121.200.nip.io/realms/kong-saml-broker",
  "protocol": "saml",
  "redirectUris": [
    "http://saml.192.168.121.200.nip.io/realms/kong-saml-broker/broker/saml-idp/endpoint"
  ],
  "attributes": {
    "saml.assertion.signature": "true",
    "saml.server.signature": "true",
    "saml.force.post.binding": "true",
    "saml_name_id_format": "email"
  }
}
```

Use these test credentials:

```text
Username: alice
Password: alice-password
NameID: alice@example.test
```

Keycloak is published at:

```text
http://saml.192.168.121.200.nip.io
```

> [!WARNING]
> The manifest uses `start-dev`, ephemeral H2 storage, HTTP, and known credentials. It is suitable only for this lab.

## 5. Configure SAML trust

`16-configure-saml-broker.sh` automates the work normally performed in the administration console:

1. Gets an administration token.
2. Downloads the IdP realm's SAML descriptor.
3. Extracts its X.509 certificate.
4. Registers `saml-idp` as a provider in the broker realm.
5. Enables signature validation and requires signed assertions.

The relevant URLs are:

```text
SP Entity ID:
http://saml.192.168.121.200.nip.io/realms/kong-saml-broker

IdP Single Sign-On Service:
http://saml.192.168.121.200.nip.io/realms/saml-idp/protocol/saml

ACS:
http://saml.192.168.121.200.nip.io/realms/kong-saml-broker/broker/saml-idp/endpoint
```

The deployment script reaches the new pod's administration API through a `port-forward`. This avoids accidentally updating an old pod while a restart is finishing.

## 6. Store Kong secrets

`16-saml-bridge-secrets.yaml` keeps the OIDC client secret and session key outside the `KongPlugin`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: saml-bridge-secrets
  namespace: javier
stringData:
  client-secret: '"kong-saml-gateway-secret"'
  session-secret: '"SAMLbridgeSessionSecret32bytes12"'
type: Opaque
```

The double quotes are part of each value because KIC parses `configPatches` values as JSON.

## 7. Configure Kong

Kong does not process SAML XML. The `kc_idp_hint` parameter sends the browser directly to the SAML provider configured in the broker:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: saml
  namespace: javier
plugin: kong-openid-connect
config:
  client_id: kong-saml-gateway
  discovery: http://saml.192.168.121.200.nip.io/realms/kong-saml-broker/.well-known/openid-configuration
  redirect_uri: http://echo.javiercd.es/saml/callback
  scope: openid profile email
  response_type: code
  token_endpoint_auth_method: client_secret_post
  authorization_params:
    kc_idp_hint: saml-idp
  session_cookie_name: kong_saml_bridge_session
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
        name: saml-bridge-secrets
        key: client-secret
  - path: /session_secret
    valueFrom:
      secretKeyRef:
        name: saml-bridge-secrets
        key: session-secret
```

The `HTTPRoute` applies the resource to `/saml`. The same prefix includes `/saml/callback`.

## 8. Deploy the lab

All manifests and scripts are stored under `posts/16-autenticacion-saml` in the examples repository:

```bash
cd ~/kic-auth
chmod +x 16-configure-saml-broker.sh
chmod +x 16-deploy-saml-bridge-lab.sh
chmod +x 16-test-saml-bridge.sh
./16-deploy-saml-bridge-lab.sh
```

Real output:

```text
deployment "keycloak-saml" successfully rolled out
httproute.gateway.networking.k8s.io/keycloak-saml configured
Broker SAML configurado.
kongplugin.configuration.konghq.com/saml unchanged
httproute.gateway.networking.k8s.io/saml configured
Puente SAML a OIDC desplegado.
```

## 9. Test the SAML flow

### 9.1. Initial redirect

```bash
curl -sS -D - -o /dev/null http://echo.javiercd.es/saml
```

Real response, abbreviating only the cookie and random values:

```http
HTTP/1.1 302 Moved Temporarily
Set-Cookie: session=<encrypted-cookie>; Path=/; SameSite=Lax; HttpOnly
Location: http://saml.192.168.121.200.nip.io/realms/kong-saml-broker/protocol/openid-connect/auth?scope=openid%20profile%20email&kc_idp_hint=saml-idp&nonce=<nonce>&client_id=kong-saml-gateway&redirect_uri=http%3A%2F%2Fecho.javiercd.es%2Fsaml%2Fcallback&state=<state>&response_type=code
Server: kong/3.10.0.16-enterprise-edition
```

The browser continues to the IdP's SAML endpoint. That redirect contains real `SAMLRequest` and `RelayState` values.

### 9.2. Browser login

Open:

```text
http://echo.javiercd.es/saml
```

Sign in as `alice`. On first access, Keycloak may ask for confirmation of the profile it creates in the broker realm. The final response is:

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8

Hola desde Kong Gateway KIC
```

## Sources

- [Kong SAML plugin](https://developer.konghq.com/plugins/saml/)
- [SAML 2.0](https://www.oasis-open.org/standard/saml/)
- [Keycloak identity brokering](https://www.keycloak.org/docs/latest/server_admin/#_identity_broker)
- [Keycloak hostname configuration](https://www.keycloak.org/server/hostname)
- [cuongntr/kong-openid-connect-plugin](https://github.com/cuongntr/kong-openid-connect-plugin)
- [lua-resty-openidc](https://github.com/zmartzone/lua-resty-openidc)
