---
title: "Introspección de tokens OAuth 2.0 en Kong"
date: 2026-07-26T00:00:00+02:00
description: "Cómo instalar un plugin abierto de la comunidad o código libre para introspección OAuth 2.0 en Kong Gateway, desplegar Keycloak y proteger una HTTPRoute con KIC."
tags: [Kong, OAuth 2.0, Introspección de tokens, Keycloak, KIC]
weight: 14
hero: images/kong/oauth2-introspection.png
aliases:
  - /posts/kong/plugins-autenticacion/oauth2/14-autenticacion-oauth2-introspection/14-autenticacion-oauth2-introspection/
---

La edición Enterprise de Kong incluye un plugin oficial de OAuth 2.0 Introspection, pero requiere licencia. En este laboratorio resolveremos esa limitación instalando un plugin abierto de la comunidad o código libre sobre Kong Gateway 3.10.

Además del plugin, desplegaremos Keycloak dentro de Kubernetes. Keycloak emitirá access tokens mediante `client_credentials` y expondrá el endpoint de introspección definido por RFC 7662. Todas las respuestas del artículo proceden de este escenario real.

> [!NOTE]
> El laboratorio continúa desde [Instalación de KIC](/posts/kong/03-instalacion-kic/03-instalacion-kic/). Reutiliza el `Gateway` `kong`, el servicio `echo`, KIC `3.5` y `192.168.121.200` como dirección de `kong-gateway-proxy`.

> [!WARNING]
> [`revomatico/kong-oidc`](https://github.com/revomatico/kong-oidc) está publicado con licencia Apache-2.0, pero el repositorio fue archivado en 2024. Es válido para este laboratorio y lo hemos probado con Kong `3.10.0.16`, pero no tiene soporte oficial de Kong ni mantenimiento activo. Antes de utilizarlo en producción debemos auditarlo, mantener nuestro propio fork y aplicar las actualizaciones de sus dependencias.

## 1. ¿Qué es la introspección de tokens?

Un servidor de recursos puede recibir un token que no sabe validar localmente. [RFC 7662](https://www.rfc-editor.org/rfc/rfc7662.html) define un endpoint al que puede enviar ese token para consultar su estado:

```http
POST /realms/kong-lab/protocol/openid-connect/token/introspect
Authorization: Basic <client-id:client-secret>
Content-Type: application/x-www-form-urlencoded

token=<access-token>
```

La propiedad principal de la respuesta es `active`:

```json
{
  "active": true,
  "client_id": "kong-introspection",
  "username": "service-account-kong-introspection"
}
```

Si el token ha caducado, ha sido revocado o no pertenece al servidor de autorización, la respuesta es:

```json
{
  "active": false
}
```

En nuestro escenario Keycloak emite un JWT, pero Kong no valida su firma localmente. Lo trata como una credencial Bearer y consulta a Keycloak en cada petición. El mismo mecanismo también sirve para tokens opacos.

Hay dos credenciales diferentes:

- El access token que el cliente presenta a Kong.
- El `client_id` y `client_secret` con los que Kong se autentica ante Keycloak.

## 2. Arquitectura del laboratorio

El flujo completo es:

![Flujo de introspección OAuth 2.0 en Kong](/kong/plugins-autenticacion/14-autenticacion-oauth2-introspection/img/oauth2-introspection-flow.svg)

El cliente solo conoce su access token. Kong utiliza unas credenciales diferentes para consultar el endpoint de introspección de Keycloak. El plugin permite llegar a `echo` cuando recibe `active: true` y responde `401 Unauthorized` cuando el token no está activo.

Utilizaremos estos componentes:

| Componente | Versión | Función |
| --- | --- | --- |
| Kong Gateway | `3.10.0.16` | Proxy y ejecución del plugin |
| KIC | `3.5` | Traducción de `KongPlugin` y `HTTPRoute` |
| `revomatico/kong-oidc` | `v1.4.0-1` | Introspección mediante un plugin abierto de la comunidad o código libre |
| `lua-resty-openidc` | `v1.7.6` | Cliente RFC 7662 utilizado por el plugin |
| Keycloak | `26.7.0` | Emisión e introspección de tokens |

No utilizamos el nombre Enterprise `oauth2-introspection` en el campo `plugin`. El recurso de Kubernetes conserva ese nombre para describir el laboratorio, pero carga el plugin abierto de la comunidad o código libre `oidc`.

## 3. Instalar el plugin abierto de la comunidad o código libre

Kong permite distribuir plugins Lua mediante `ConfigMap`. El código se monta en el pod y `KONG_PLUGINS` indica qué módulos debe cargar.

El script [`14-install-community-oidc.sh`](https://github.com/javierasping/kong/blob/main/posts/14-autenticacion-oauth2-introspection/14-install-community-oidc.sh) realiza estas operaciones:

1. Descarga `revomatico/kong-oidc` desde la etiqueta `v1.4.0-1`.
2. Descarga `lua-resty-openidc` desde la etiqueta `v1.7.6`.
3. Verifica el SHA-256 de cada fichero.
4. Crea los `ConfigMap` `kong-plugin-oidc` y `kong-resty-openidc`.
5. Actualiza la release Helm de Kong.
6. Espera a que el nuevo pod supere las sondas de disponibilidad.

Las versiones y checksums son importantes. Descargar directamente una rama cambiante durante cada despliegue impediría saber qué código está ejecutando el Gateway.

### 3.1. Valores de Helm

El fichero `14-community-oidc-values.yaml` contiene:

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

`gateway.plugins.configMaps` monta los ficheros Lua en `/opt/kong/plugins/oidc` y añade `oidc` a `KONG_PLUGINS`. El volumen adicional coloca `openidc.lua` bajo `/opt/resty`, una ubicación incluida en `KONG_LUA_PACKAGE_PATH`.

También conservamos la imagen 3.10 y la dirección de MetalLB. De lo contrario, una actualización Helm podría devolver Kong a la imagen predeterminada del chart o liberar `.200`.

### 3.2. Ejecutar la instalación

Dentro de la VM:

```bash
cd ~/kic-auth
chmod +x 14-install-community-oidc.sh
./14-install-community-oidc.sh
```

El resultado real es:

```text
configmap/kong-plugin-oidc created
configmap/kong-resty-openidc created
Release "kong" has been upgraded. Happy Helming!
STATUS: deployed
deployment "kong-gateway" successfully rolled out
Plugin abierto de la comunidad o código libre oidc instalado en Kong Gateway.
```

Comprobamos la versión, la IP y los plugins cargados:

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

Que el binario se identifique como Enterprise no significa que exista una licencia. El plugin `oidc` que acabamos de cargar es código libre mantenido por la comunidad y no depende de ella.

## 4. Desplegar Keycloak

El fichero `14-keycloak.yaml` contiene un `ConfigMap`, un `Deployment` y un `Service`.

### 4.1. Importar el realm

La parte principal del realm es:

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

Los tokens duran sesenta segundos. Este margen permite ejecutar cómodamente una prueba manual y sigue siendo lo bastante corto para demostrar la caducidad. El mapper añade `kong-introspection` a `aud`. Keycloak 26 rechaza la introspección si el cliente que la solicita no aparece en la audiencia del token.

El cliente solo permite `client_credentials`. No habilitamos login interactivo ni password grant.

### 4.2. Deployment y nombre canónico

La configuración relevante del contenedor es:

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

`KC_HOSTNAME` evita un error sutil: si obtenemos el token mediante un port-forward y Keycloak utiliza `127.0.0.1` como issuer, Kong lo enviará después al DNS interno y Keycloak rechazará el JWT por no coincidir `iss`. Fijar el hostname del `Service` hace que emisión e introspección compartan el mismo issuer.

Este despliegue utiliza `start-dev` y almacenamiento H2 efímero. Es deliberadamente un laboratorio, no una configuración de producción.

## 5. Guardar el secreto de introspección

Creamos `14-oidc-client-secret.yaml`:

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

Las comillas dobles forman parte del valor porque `configPatches` interpreta el contenido como JSON. El `Secret` no cifra el dato. Evita incluirlo en el `KongPlugin` y permite aplicar controles RBAC.

## 6. Configurar el `KongPlugin`

El fichero `14-oauth2-introspection-plugin.yaml` contiene:

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

- `plugin: oidc` selecciona el plugin abierto de la comunidad o código libre.
- `bearer_only: "yes"` desactiva redirecciones de navegador: sin Bearer token devuelve `401`.
- `introspection_endpoint_auth_method` hace que Kong utilice HTTP Basic ante Keycloak.
- `introspection_cache_ignore: "yes"` obliga a consultar el estado en cada petición. Es útil para observar la caducidad inmediata.
- `realm` aparece en `WWW-Authenticate`.
- `configPatches` obtiene el secreto mediante KIC 3.5 antes de enviar la configuración a Kong.
- `ssl_verify: "no"` solo es aceptable porque el IdP del laboratorio utiliza HTTP interno.

## 7. Publicar la ruta

El `HTTPRoute` aplica el `KongPlugin` únicamente a `/oauth2-introspection`:

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

Aplicamos todo con:

```bash
cd ~/kic-auth
chmod +x 14-deploy-community-oidc-lab.sh
./14-deploy-community-oidc-lab.sh
```

El script valida primero el esquema del plugin mediante `--dry-run=server`. Si `oidc` no está cargado, se detiene antes de publicar la ruta. También reinicia el Deployment de Keycloak después de aplicar el `ConfigMap`, porque la importación del realm solo ocurre durante el arranque.

## 8. Probar la introspección

### 8.1. Petición sin token

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

### 8.2. Token desconocido

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

### 8.3. Obtener un token real

Abrimos temporalmente el Service de Keycloak dentro de la VM:

```bash
sudo kubectl port-forward -n javier service/keycloak 18080:8080
```

En otro terminal:

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

La respuesta real, abreviando únicamente la credencial temporal, es:

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

Podemos consultar directamente RFC 7662:

```bash
curl -sS \
  -u kong-introspection:client-secret \
  --data-urlencode "token=${ACCESS_TOKEN}" \
  http://127.0.0.1:18080/realms/kong-lab/protocol/openid-connect/token/introspect
```

Esta es una respuesta real y completa del endpoint de introspección para un
token activo:

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

`iat` indica cuándo se emitió el token y `exp` cuándo deja de ser válido. En
este ejemplo hay exactamente 60 segundos entre ambos valores. `active: true`
confirma que Keycloak todavía lo considera válido en el momento de la consulta.

### 8.4. Token activo

Debemos realizar esta petición antes de que transcurran los segundos indicados
por `expires_in`:

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

### 8.5. El mismo token después de caducar

Esperamos hasta que termine la vida útil indicada por Keycloak y repetimos
exactamente la petición:

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

El resultado demuestra que Kong no se limita a reconocer el formato del token: consulta su estado y deja de aceptarlo cuando Keycloak responde que ya no está activo.

> [!WARNING]
> Un `401` con `error="invalid token"` también es la respuesta correcta cuando el token ya ha caducado. Debemos comparar la hora de la petición con `iat` y `exp` de la introspección. Por ejemplo, un token con `iat=1785089182` se emitió a las `18:06:22 UTC` y con `exp=1785089192` caducó a las `18:06:32 UTC`. Una petición que llegue a Kong a las `18:06:43 UTC` debe recibir `401`.


## Fuentes

- [RFC 7662: OAuth 2.0 Token Introspection](https://www.rfc-editor.org/rfc/rfc7662.html)
- [revomatico/kong-oidc v1.4.0-1](https://github.com/revomatico/kong-oidc/releases/tag/v1.4.0-1)
- [lua-resty-openidc v1.7.6](https://github.com/zmartzone/lua-resty-openidc/releases/tag/v1.7.6)
- [Kong: despliegue de plugins personalizados](https://developer.konghq.com/custom-plugins/deployment-options/)
- [KIC: plugins personalizados](https://developer.konghq.com/kubernetes-ingress-controller/custom-plugins/)
- [KIC: Secrets en plugins](https://developer.konghq.com/kubernetes-ingress-controller/reference/secrets-in-plugins/)
- [Keycloak: ejecución en contenedores](https://www.keycloak.org/server/containers)
- [Keycloak: importación de realms](https://www.keycloak.org/server/importExport)
- [Keycloak: endpoint de introspección](https://www.keycloak.org/securing-apps/oidc-layers)
