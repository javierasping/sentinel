---
title: "OpenID Connect en Kong"
date: 2026-07-26T00:00:00+02:00
description: "Cómo instalar una alternativa OpenID Connect de código abierto, desplegar Keycloak y completar Authorization Code con KIC."
tags: [Kong, OpenID Connect, OAuth 2.0, Keycloak, KIC]
weight: 15
hero: images/kong/openid-connect.png
---

El plugin oficial OpenID Connect de Kong requiere una licencia Enterprise. En este laboratorio utilizaremos el adaptador abierto de la comunidad o código libre [`cuongntr/kong-openid-connect-plugin`](https://github.com/cuongntr/kong-openid-connect-plugin) sobre la librería [`lua-resty-openidc`](https://github.com/zmartzone/lua-resty-openidc) para completar un flujo Authorization Code sin licencia.

Desplegaremos un Keycloak independiente dentro de Kubernetes, iniciaremos sesión con un usuario real y comprobaremos tanto el callback como la reutilización de la cookie. Todas las respuestas del artículo proceden de la VM del laboratorio.

> [!NOTE]
> Este laboratorio continúa desde [Instalación de KIC](/posts/kong/03-instalacion-kic/03-instalacion-kic/). Reutiliza el `Gateway` `kong`, el servicio `echo`, KIC `3.5` y `192.168.121.200` como dirección de `kong-gateway-proxy`.

> [!WARNING]
> El adaptador `kong-openid-connect-plugin` no está archivado, usa la API moderna de plugins y declara compatibilidad con Kong 3.x, pero es un proyecto joven: su último commit es de julio de 2025, tiene pocos colaboradores y no ofrece soporte oficial. La librería subyacente `lua-resty-openidc` sí mantiene actividad y publicó `v1.9.0` en julio de 2026. Hemos fijado versiones y checksums, pero antes de producción debemos auditar el adaptador y mantener nuestro propio fork.

## 1. ¿Qué es OpenID Connect?

OAuth 2.0 define cómo obtener autorización para acceder a recursos. OpenID Connect añade una capa de identidad y permite que una aplicación delegue el inicio de sesión en un proveedor de identidad.

En Authorization Code intervienen:

1. El navegador solicita `/oidc`.
2. Kong crea `state` y `nonce`, guarda el estado en una cookie y redirige a Keycloak.
3. Keycloak autentica al usuario.
4. El navegador devuelve un código temporal al callback de Kong.
5. Kong intercambia el código por tokens directamente con Keycloak.
6. Kong valida la respuesta y crea una sesión.
7. Las peticiones posteriores reutilizan la cookie sin repetir el login.

El código no es un access token y el `client_secret` nunca llega al navegador.

## 2. Componentes y flujo del laboratorio

![Flujo OpenID Connect Authorization Code en Kong](/kong/plugins-autenticacion/15-autenticacion-openid-connect/img/openid-connect-flow.svg)

El navegador nunca entrega la contraseña a Kong. Keycloak autentica a `alice` y devuelve un código de autorización de un solo uso. Kong valida el callback, intercambia el código por tokens y crea una sesión cifrada antes de enviar la petición al servicio `echo`.

| Componente | Versión | Función |
| --- | --- | --- |
| Kong Gateway | `3.10.0.16` | Proxy y ejecución del plugin |
| KIC | `3.5` | Traducción de `KongPlugin` y `HTTPRoute` |
| `kong-openid-connect-plugin` | commit `a4ff261` | Adaptador OIDC para Kong 3.x |
| `lua-resty-openidc` | `v1.9.0` | Implementación OpenID Connect |
| Keycloak | `26.7.0` | Proveedor de identidad |

El plugin oficial se llama `openid-connect`. Para evitar cualquier ambigüedad, el recurso del laboratorio carga `plugin: kong-openid-connect`.

## 3. Instalar el plugin abierto de la comunidad o código libre

El script [`15-install-community-oidc.sh`](https://github.com/javierasping/kong/blob/main/posts/15-autenticacion-openid-connect/15-install-community-oidc.sh):

1. Descarga el adaptador desde el commit fijado.
2. Descarga `lua-resty-openidc v1.9.0`.
3. Verifica el SHA-256 de los cuatro ficheros.
4. Crea los `ConfigMap` del plugin y de la librería.
5. Conserva también el plugin `oidc` utilizado por el post 14.
6. Actualiza la release Helm y espera al nuevo pod.

Los valores principales son:

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

Dentro de la VM:

```bash
cd ~/kic-auth
chmod +x 15-install-community-oidc.sh
./15-install-community-oidc.sh
```

Comprobamos los plugins cargados:

```bash
sudo kubectl get deployment kong-gateway -n kong \
  -o jsonpath='{.spec.template.spec.containers[?(@.name=="proxy")].env[?(@.name=="KONG_PLUGINS")].value}{"\n"}'
```

```text
bundled,oidc,kong-openid-connect
```

## 4. Desplegar Keycloak

`15-keycloak.yaml` importa el realm `kong-oidc-lab` con:

- El cliente confidencial `kong-gateway`.
- Authorization Code habilitado.
- Callback `http://echo.javiercd.es/oidc/callback`.
- El usuario `alice` con contraseña `alice-password`.

Keycloak se publica mediante una `HTTPRoute` independiente:

```text
http://keycloak.192.168.121.200.nip.io
```

El nombre `nip.io` resuelve a `192.168.121.200` tanto desde el navegador como desde los pods. Así, los endpoints anunciados por el documento de descubrimiento son accesibles en ambos canales.

> [!WARNING]
> Keycloak utiliza `start-dev`, H2 efímero, HTTP y credenciales de ejemplo. Esta configuración solo sirve para el laboratorio.

## 5. Guardar los secretos

`15-openid-connect-secrets.yaml` evita incluir los secretos directamente en el `KongPlugin`:

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

Las comillas dobles forman parte de cada valor porque KIC interpreta `configPatches` como JSON.

## 6. Configurar el `KongPlugin`

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

`session_cookie_secure: false` y `ssl_verify: false` solo son aceptables porque todo el laboratorio utiliza HTTP.

## 7. Publicar y desplegar las rutas

La ruta protegida conserva el prefijo `/oidc`, que también cubre `/oidc/callback`:

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

Aplicamos el laboratorio:

```bash
cd ~/kic-auth
chmod +x 15-deploy-community-oidc-lab.sh
./15-deploy-community-oidc-lab.sh
```

El script valida primero el esquema, reinicia Keycloak para importar el realm y solo entonces publica las rutas.

## 8. Probar Authorization Code

### 8.1. Redirección inicial

```bash
curl -sS -D - -o /dev/null http://echo.javiercd.es/oidc
```

Respuesta real, abreviando únicamente la cookie, `state` y `nonce`:

```http
HTTP/1.1 302 Moved Temporarily
Date: Sun, 26 Jul 2026 18:30:12 GMT
Set-Cookie: session=<cookie-cifrada>; Path=/; SameSite=Lax; HttpOnly
Location: http://keycloak.192.168.121.200.nip.io/realms/kong-oidc-lab/protocol/openid-connect/auth?scope=openid%20profile%20email&nonce=<nonce>&client_id=kong-gateway&redirect_uri=http%3A%2F%2Fecho.javiercd.es%2Foidc%2Fcallback&state=<state>&response_type=code
X-Kong-Response-Latency: 73
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: ed129124d4228f45464e0f09105a0a41
```

### 8.2. Login y callback

Abrimos `http://echo.javiercd.es/oidc` en el navegador e iniciamos sesión:

```text
Usuario: alice
Contraseña: alice-password
```

La primera captura muestra la redirección desde Kong al formulario de inicio de sesión del realm `kong-oidc-lab` en Keycloak:

![Formulario de inicio de sesión de Keycloak durante el flujo OpenID Connect](/kong/plugins-autenticacion/15-autenticacion-openid-connect/img/oidc-keycloak-login.png)

Después del callback, la respuesta real es:

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

La segunda captura confirma que Keycloak devolvió el navegador al callback, Kong validó el Authorization Code y la petición autenticada llegó al servicio `echo`:

![Respuesta del servicio echo después de completar OpenID Connect en Kong](/kong/plugins-autenticacion/15-autenticacion-openid-connect/img/oidc-authenticated-response.png)

Una segunda petición con la misma cookie devuelve `200` sin volver a mostrar el login.

## Fuentes

- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- [cuongntr/kong-openid-connect-plugin](https://github.com/cuongntr/kong-openid-connect-plugin)
- [kong-openid-connect en LuaRocks](https://luarocks.org/modules/cuongntr/kong-openid-connect)
- [lua-resty-openidc v1.9.0](https://github.com/zmartzone/lua-resty-openidc/releases/tag/v1.9.0)
- [Kong: despliegue de plugins personalizados](https://developer.konghq.com/custom-plugins/deployment-options/)
- [KIC: plugins personalizados](https://developer.konghq.com/kubernetes-ingress-controller/custom-plugins/)
- [KIC: Secrets en plugins](https://developer.konghq.com/kubernetes-ingress-controller/reference/secrets-in-plugins/)
- [Keycloak: configuración del hostname](https://www.keycloak.org/server/hostname)
