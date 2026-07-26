---
title: "SAML en Kong mediante Keycloak"
date: 2026-07-26T00:00:00+02:00
description: "Cómo proteger una ruta de Kong con SAML 2.0 usando Keycloak como broker y un plugin OpenID Connect de código abierto."
tags: [Kong, SAML, OpenID Connect, Keycloak, KIC]
weight: 16
hero: images/kong/saml.png
---

El plugin oficial [`saml`](https://developer.konghq.com/plugins/saml/) de Kong requiere una licencia Enterprise. Después de revisar las alternativas abiertas de la comunidad o de código libre no he encontrado un plugin SAML directo, mantenido y compatible con Kong 3.x que resulte razonable recomendar.

En este laboratorio utilizaremos una arquitectura distinta y completamente abierta: Keycloak actuará como Service Provider SAML y como broker de identidad, mientras Kong utilizará el plugin abierto de la comunidad o código libre `kong-openid-connect` instalado en el artículo anterior. La autenticación del usuario sí ocurre mediante una petición y una respuesta SAML reales. Keycloak valida el XML firmado y entrega a Kong un Authorization Code de OpenID Connect.

Todas las respuestas incluidas en el artículo proceden de la VM del laboratorio.

> [!WARNING]
> El plugin SAML oficial de Kong es propietario y no puede utilizarse sin una licencia Enterprise. Esta solución no es una reimplementación ni un sustituto directo de su API: traslada la terminación SAML a Keycloak y mantiene OIDC entre Keycloak y Kong.

> [!NOTE]
> Este laboratorio continúa desde [OpenID Connect en Kong](/posts/kong/plugins-autenticacion/15-autenticacion-openid-connect/15-autenticacion-openid-connect/). Reutiliza `kong-openid-connect`, el `Gateway` `kong`, el servicio `echo`, KIC `3.5` y la dirección `192.168.121.200`.

## 1. ¿Por qué usar un broker?

SAML 2.0 intercambia autenticación mediante XML, firmas digitales, metadatos, una entidad emisora, una audiencia y un Assertion Consumer Service (`ACS`). Implementar correctamente todas esas validaciones dentro de un plugin Lua pequeño sería una decisión de seguridad difícil de justificar.

Keycloak es un proyecto de código abierto activo que admite identity brokering y proveedores SAML. En esta arquitectura cada componente se encarga del protocolo que conoce:

- Keycloak genera la `SAMLRequest`.
- El IdP autentica al usuario y firma la `SAMLResponse`.
- Keycloak valida firma, destino, audiencia y tiempos de la aserción.
- Keycloak transforma la identidad SAML en una sesión OIDC.
- Kong valida el flujo OIDC y protege la ruta.

No necesitamos crear un `KongConsumer`: la identidad y la sesión se resuelven entre el IdP, el realm broker y el plugin OIDC.

## 2. Flujo completo del laboratorio

![Flujo SAML mediante Keycloak y Kong](/kong/plugins-autenticacion/16-autenticacion-saml/img/saml-flow.svg)

Kong solo participa en el tramo OpenID Connect. El realm `kong-saml-broker` actúa como Service Provider SAML, envía la `AuthnRequest` al IdP y valida la `SAMLResponse` firmada. Después transforma esa identidad en un código OIDC que Kong puede validar para crear la sesión.

Utilizamos dos realms en una única instancia de Keycloak para que el escenario sea autocontenido:

| Realm | Función |
| --- | --- |
| `saml-idp` | IdP SAML y usuario `alice` |
| `kong-saml-broker` | SP SAML para el IdP y proveedor OIDC para Kong |

En producción, `saml-idp` se sustituiría por Entra ID, Okta, ADFS u otro IdP corporativo.

## 3. Requisito: instalar el plugin abierto de la comunidad o código libre

El puente reutiliza el adaptador del post 15, fijado al commit `a4ff261`, y `lua-resty-openidc v1.9.0`:

```bash
cd ~/kic-auth
chmod +x 15-install-community-oidc.sh
./15-install-community-oidc.sh
```

Comprobamos que Kong lo ha cargado:

```bash
sudo kubectl get deployment kong-gateway -n kong \
  -o jsonpath='{.spec.template.spec.containers[?(@.name=="proxy")].env[?(@.name=="KONG_PLUGINS")].value}{"\n"}'
```

```text
bundled,oidc,kong-openid-connect
```

## 4. Desplegar los realms SAML

`16-keycloak.yaml` crea un `ConfigMap`, un `Deployment` y un `Service`. El primer realm registra el cliente OIDC de Kong:

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

El realm `saml-idp` registra como Service Provider al broker:

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

El usuario de prueba es:

```text
Usuario: alice
Contraseña: alice-password
NameID: alice@example.test
```

Keycloak se publica en:

```text
http://saml.192.168.121.200.nip.io
```

> [!WARNING]
> El manifiesto usa `start-dev`, H2 efímero, HTTP y credenciales conocidas. Solo es válido para este laboratorio.

## 5. Configurar la confianza SAML

`16-configure-saml-broker.sh` realiza la parte que normalmente configuraríamos en la consola:

1. Obtiene un token de administración.
2. Descarga el descriptor SAML del realm IdP.
3. Extrae su certificado X.509.
4. Registra `saml-idp` como proveedor del realm broker.
5. Activa la validación de firmas y exige aserciones firmadas.

Las URL relevantes son:

```text
Entity ID del SP:
http://saml.192.168.121.200.nip.io/realms/kong-saml-broker

Single Sign-On Service del IdP:
http://saml.192.168.121.200.nip.io/realms/saml-idp/protocol/saml

ACS:
http://saml.192.168.121.200.nip.io/realms/kong-saml-broker/broker/saml-idp/endpoint
```

El script de despliegue configura la API de administración mediante un `port-forward` al pod nuevo. Esto evita escribir accidentalmente en un pod anterior durante un reinicio.

## 6. Guardar los secretos de Kong

`16-saml-bridge-secrets.yaml` separa el secreto OIDC y la clave de sesión del `KongPlugin`:

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

Las comillas dobles forman parte de los valores porque KIC interpreta los valores de `configPatches` como JSON.

## 7. Configurar Kong

Kong no procesa XML SAML. El parámetro `kc_idp_hint` envía al navegador directamente al proveedor SAML configurado en el broker:

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

La `HTTPRoute` aplica el recurso a `/saml`. El mismo prefijo incluye `/saml/callback`.

## 8. Desplegar el laboratorio

Todos los manifiestos y scripts están en `posts/16-autenticacion-saml` del repositorio de ejemplos:

```bash
cd ~/kic-auth
chmod +x 16-configure-saml-broker.sh
chmod +x 16-deploy-saml-bridge-lab.sh
chmod +x 16-test-saml-bridge.sh
./16-deploy-saml-bridge-lab.sh
```

Salida real:

```text
deployment "keycloak-saml" successfully rolled out
httproute.gateway.networking.k8s.io/keycloak-saml configured
Broker SAML configurado.
kongplugin.configuration.konghq.com/saml unchanged
httproute.gateway.networking.k8s.io/saml configured
Puente SAML a OIDC desplegado.
```

## 9. Probar el flujo SAML

### 9.1. Redirección inicial

```bash
curl -sS -D - -o /dev/null http://echo.javiercd.es/saml
```

Respuesta real, abreviando únicamente la cookie y los valores aleatorios:

```http
HTTP/1.1 302 Moved Temporarily
Set-Cookie: session=<cookie-cifrada>; Path=/; SameSite=Lax; HttpOnly
Location: http://saml.192.168.121.200.nip.io/realms/kong-saml-broker/protocol/openid-connect/auth?scope=openid%20profile%20email&kc_idp_hint=saml-idp&nonce=<nonce>&client_id=kong-saml-gateway&redirect_uri=http%3A%2F%2Fecho.javiercd.es%2Fsaml%2Fcallback&state=<state>&response_type=code
Server: kong/3.10.0.16-enterprise-edition
```

El navegador continúa hacia el endpoint SAML del IdP. La redirección contiene una `SAMLRequest` y un `RelayState` reales.

### 9.2. Login desde el navegador

Abrimos:

```text
http://echo.javiercd.es/saml
```

Iniciamos sesión como `alice`. En el primer acceso, Keycloak puede pedir confirmar el perfil que creará en el realm broker. Después recibiremos:

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8

Hola desde Kong Gateway KIC
```

## Fuentes

- [Kong: plugin SAML](https://developer.konghq.com/plugins/saml/)
- [SAML 2.0](https://www.oasis-open.org/standard/saml/)
- [Keycloak: identity brokering](https://www.keycloak.org/docs/latest/server_admin/#_identity_broker)
- [Keycloak: configuración del hostname](https://www.keycloak.org/server/hostname)
- [cuongntr/kong-openid-connect-plugin](https://github.com/cuongntr/kong-openid-connect-plugin)
- [lua-resty-openidc](https://github.com/zmartzone/lua-resty-openidc)
