---
title: "JWT Auth en Kong"
date: 2026-07-26T00:00:00+02:00
description: "Cómo funciona un JSON Web Token y cómo proteger un recurso HTTPRoute con el plugin JWT de Kong Gateway y KIC."
tags: [Kong, Autenticación, JWT, JSON Web Token, KIC]
weight: 13
hero: images/kong/jwt-auth.png
---

Un JSON Web Token permite transportar afirmaciones sobre una identidad dentro de un token firmado. Kong puede verificar esa firma y sus fechas antes de que la petición llegue al backend.

En este artículo separaremos la estructura del token, la credencial criptográfica almacenada en Kong y el consumidor que representa al cliente. Después construiremos un laboratorio reproducible con Kong Ingress Controller, JWT firmado con HS256 y una ruta `/jwt`.

> [!NOTE]
> Este laboratorio continúa exactamente desde el escenario creado en [Instalación de KIC](/posts/kong/03-instalacion-kic/03-instalacion-kic/). Reutiliza el `Gateway` `kong`, el servicio `echo` y la dirección `192.168.121.200` asignada por MetalLB a `kong-gateway-proxy`.
>
> Las pruebas de este artículo se han realizado con Kong Gateway `3.10.0.16` y Kong Ingress Controller `3.5`.

## 1. ¿Qué es un JWT?

JWT, de *JSON Web Token*, es un formato definido por [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519.html). Un token contiene tres partes separadas por puntos:

```text
header.payload.signature
```

El `header` describe el tipo de token y el algoritmo utilizado:

```json
{
  "typ": "JWT",
  "alg": "HS256"
}
```

El `payload` contiene las afirmaciones o *claims*. En nuestro laboratorio utilizaremos:

```json
{
  "iss": "jwt-client",
  "iat": 1785052800,
  "exp": 1785053100
}
```

- `iss` identifica al emisor y permite a Kong localizar la credencial JWT.
- `iat` indica cuándo se emitió el token.
- `exp` indica cuándo deja de ser válido.

Las dos primeras partes se codifican mediante Base64URL. Después el emisor firma el resultado:

```text
Base64URL(header) + "." + Base64URL(payload)
                         |
                         v
                  HMAC-SHA256
                         |
                         v
                  firma Base64URL
```

Base64URL es una codificación, no un cifrado. Cualquiera que reciba el token puede leer su contenido. La firma permite detectar modificaciones, pero los JWT deben enviarse mediante HTTPS y no deben contener secretos en el `payload`.

En este laboratorio usaremos HS256, un algoritmo simétrico: quien emite el token y Kong comparten el mismo secreto. Es adecuado para comprender el flujo, pero en arquitecturas con varios emisores o verificadores suele ser preferible un algoritmo asimétrico, porque Kong solo necesita conocer la clave pública.

## 2. ¿Cómo funciona el plugin JWT en Kong Gateway?

Kong implementa la validación mediante el plugin oficial [`jwt`](https://developer.konghq.com/plugins/jwt/). Está disponible para las topologías traditional, hybrid y DB-less y puede aplicarse globalmente, a un `Service` o a una `Route`.

En este laboratorio el plugin se aplicará únicamente a la `Route` `/jwt`.

El cliente enviará el token como credencial Bearer:

```http
Authorization: Bearer <token>
```

Cuando una petición coincide con la `Route`, Kong realiza estas comprobaciones:

1. Extrae el JWT de la petición.
2. Decodifica su `header` y su `payload`.
3. Lee el claim configurado como identificador. Por defecto utiliza `iss`.
4. Busca una credencial JWT cuyo campo `key` coincida con ese valor.
5. Comprueba que el algoritmo del token coincida con el de la credencial.
6. Verifica la firma.
7. Comprueba el claim `exp`, porque lo hemos incluido en `claims_to_verify`.
8. Si todo es válido, identifica al consumidor y envía la petición al upstream.

El siguiente diagrama reúne estas comprobaciones. El plugin no confía en el contenido del JWT por el simple hecho de poder decodificarlo. Debe localizar la credencial mediante `iss` y validar el algoritmo, la firma y la expiración.

![Flujo de JWT Auth en Kong Gateway](/kong/plugins-autenticacion/13-autenticacion-jwt/img/jwt-auth-flow.svg)

El comportamiento es el siguiente:

- Si no se envía un token, Kong responde `401 Unauthorized`.
- Si el token está mal formado, la firma no coincide o `iss` no tiene una credencial asociada, Kong responde `401 Unauthorized`.
- Si el token ha caducado, Kong responde `401 Unauthorized`.
- Si el token es válido, Kong identifica al consumidor (`Consumer`) y permite que la petición continúe.
- Cuando Kong rechaza el JWT, la petición no llega al upstream.

El plugin autentica la identidad asociada a la credencial, pero no concede permisos detallados por sí solo. La autorización puede añadirse con ACL u otro plugin que utilice el consumidor o los claims ya validados.

## 3. Consumidores, credenciales y tokens JWT

En este laboratorio intervienen tres objetos diferentes:

- El consumidor representa al cliente dentro de Kong.
- La credencial JWT contiene el identificador, el algoritmo y el material criptográfico.
- El token es la prueba temporal que el cliente presenta en cada petición.

No hay que confundir estos valores:

- `jwt-client` es el nombre del recurso `KongConsumer`.
- `jwt-client` también es el `username` del consumidor.
- `jwt-client` es el campo `key` de la credencial y el valor de `iss` dentro del token.
- `jwt-shared-secret` es el secreto utilizado para firmar y verificar.

La relación es:

```text
Consumidor
    |
    +-- Credencial JWT
            |
            +-- key
            +-- algorithm
            +-- secret
                    |
                    +-- verifica la firma del token
```

Aunque varios valores coinciden para facilitar el laboratorio, pertenecen a campos diferentes. Kong no identifica al consumidor por el texto del token sin más: primero localiza la credencial mediante `iss` y después valida criptográficamente la firma.

## 4. Configuración de JWT en Kong con KIC

Vamos a publicar el servicio `echo` mediante un `HTTPRoute` y proteger esa ruta con el plugin JWT.

El laboratorio reutiliza el `Gateway` `kong`, el servicio `echo` y el proxy creados durante la instalación de KIC. Solo añadiremos un `KongPlugin`, un `Secret`, un `KongConsumer` y un `HTTPRoute`.

### 4.1. Relación entre los recursos de Kubernetes y Kong

| Recurso de Kubernetes | Recurso interno de Kong |
| --- | --- |
| `KongPlugin` | `plugins` |
| `Secret` | `jwt_secrets` |
| `KongConsumer` | `consumers` |
| `HTTPRoute` | `routes`, `services`, `upstreams` y `targets` |

En modo DB-less estas entidades forman parte de la configuración en memoria. En modo traditional se almacenarían en la base de datos de Kong.

### 4.2. Crear el plugin JWT

`claims_to_verify` indica qué claims temporales debe comprobar Kong. En este caso exigimos que el token no haya superado `exp`.

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: jwt
  namespace: javier
plugin: jwt
config:
  claims_to_verify:
    - exp
```

El plugin todavía no queda asociado a ninguna ruta. La asociación se realizará desde el `HTTPRoute`.

### 4.3. Crear la credencial JWT

La etiqueta `konghq.com/credential: jwt` indica a KIC cómo debe interpretar los campos del `Secret`.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: jwt-credential
  namespace: javier
  labels:
    konghq.com/credential: jwt
stringData:
  key: jwt-client
  secret: jwt-shared-secret
  algorithm: HS256
```

`key` es el valor que Kong buscará en el claim `iss`. `secret` contiene la clave simétrica y `algorithm` impide aceptar un algoritmo distinto al esperado.

El uso de `stringData` no cifra estos valores. Kubernetes los codifica en Base64 al almacenar el `Secret`.

### 4.4. Crear el consumidor `KongConsumer`

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: jwt-client
  namespace: javier
  annotations:
    kubernetes.io/ingress.class: kong
username: jwt-client
credentials:
  - jwt-credential
```

KIC crea el consumidor y asocia la credencial JWT. En modo traditional se representarían mediante `consumers` y `jwt_secrets`.

### 4.5. Crear el `HTTPRoute`

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: jwt
  namespace: javier
  annotations:
    konghq.com/plugins: jwt
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
            value: /jwt
      backendRefs:
        - name: echo
          port: 80
```

La anotación aplica el `KongPlugin` únicamente a la `Route` generada desde este recurso.

### 4.6. Aplicar los manifiestos

```bash
sudo kubectl apply -f 13-jwt-plugin.yaml
sudo kubectl apply -f 13-jwt-secret.yaml
sudo kubectl apply -f 13-jwt-consumer.yaml
sudo kubectl apply -f 13-jwt-httproute.yaml
```

Comprobamos el estado:

```bash
sudo kubectl get kongplugin jwt -n javier
sudo kubectl get kongconsumer jwt-client -n javier
sudo kubectl get httproute jwt -n javier
sudo kubectl describe httproute jwt -n javier
```

## 5. Probando la autenticación JWT

Las respuestas mostradas se han obtenido directamente del Kong Gateway desplegado en la VM.

### 5.1. Petición sin token

```bash
curl -i http://echo.javiercd.es/jwt
```

Kong responde antes de contactar con el upstream:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:02:01 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: Bearer
Content-Length: 26
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 748a483ab408712bc869dd29814f1426

{"message":"Unauthorized"}
```

### 5.2. Generar un JWT válido

El siguiente bloque crea manualmente un token HS256 válido durante cinco minutos. Debe ejecutarse desde el anfitrión y requiere `openssl`:

```bash
NOW="$(date +%s)"
HEADER='{"typ":"JWT","alg":"HS256"}'
PAYLOAD="{\"iss\":\"jwt-client\",\"iat\":${NOW},\"exp\":$((NOW+300))}"

b64url() {
  echo -n "$1" \
    | openssl base64 -A \
    | tr '+/' '-_' \
    | tr -d '='
}

UNSIGNED="$(b64url "${HEADER}").$(b64url "${PAYLOAD}")"
SIGNATURE="$(echo -n "${UNSIGNED}" \
  | openssl dgst -sha256 -hmac 'jwt-shared-secret' -binary \
  | openssl base64 -A \
  | tr '+/' '-_' \
  | tr -d '=')"
TOKEN="${UNSIGNED}.${SIGNATURE}"
```

Podemos inspeccionar el token generado:

```bash
echo "${TOKEN}"
```

### 5.3. Enviar el JWT correcto

```bash
curl -i \
  -H "Authorization: Bearer ${TOKEN}" \
  http://echo.javiercd.es/jwt
```

Kong localiza la credencial mediante `iss`, valida la firma y comprueba `exp`. La petición alcanza el upstream:

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: 28
Connection: keep-alive
X-App-Name: http-echo
X-App-Version: 1.0.0
Date: Sun, 26 Jul 2026 09:02:01 GMT
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Upstream-Latency: 0
X-Kong-Proxy-Latency: 1
Via: 1.1 kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: d3bba04b5e08ff056419853b6d34f67a

Hola desde Kong Gateway KIC
```

### 5.4. Comprobar una firma incorrecta

Modificamos un carácter de la firma:

```bash
INVALID_TOKEN="${UNSIGNED}.A${SIGNATURE:1}"

curl -i \
  -H "Authorization: Bearer ${INVALID_TOKEN}" \
  http://echo.javiercd.es/jwt
```

El contenido sigue teniendo la forma de un JWT, pero la firma ya no corresponde al `header` y al `payload`. La respuesta real es:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:02:01 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: Bearer error="invalid_token"
Content-Length: 31
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 1625d86d92126922fa34d20c91149009

{"message":"Invalid signature"}
```

### 5.5. Comprobar la caducidad

Podemos generar otro token con `exp` en el pasado:

```bash
EXPIRED_PAYLOAD="{\"iss\":\"jwt-client\",\"iat\":$((NOW-600)),\"exp\":$((NOW-300))}"
EXPIRED_UNSIGNED="$(b64url "${HEADER}").$(b64url "${EXPIRED_PAYLOAD}")"
EXPIRED_SIGNATURE="$(echo -n "${EXPIRED_UNSIGNED}" \
  | openssl dgst -sha256 -hmac 'jwt-shared-secret' -binary \
  | openssl base64 -A \
  | tr '+/' '-_' \
  | tr -d '=')"
EXPIRED_TOKEN="${EXPIRED_UNSIGNED}.${EXPIRED_SIGNATURE}"

curl -i \
  -H "Authorization: Bearer ${EXPIRED_TOKEN}" \
  http://echo.javiercd.es/jwt
```

La firma es correcta, pero el token ha caducado. Como hemos configurado `claims_to_verify: [exp]`, Kong lo rechaza:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:02:01 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: Bearer error="invalid_token"
Content-Length: 23
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 6aaf9d5956c01c57fa807168eefe7942

{"exp":"token expired"}
```

## Fuentes oficiales

- [RFC 7519: JSON Web Token](https://www.rfc-editor.org/rfc/rfc7519.html)
- [JWT plugin](https://developer.konghq.com/plugins/jwt/)
- [JWT configuration reference](https://developer.konghq.com/plugins/jwt/reference/)
- [Verify registered claims](https://developer.konghq.com/plugins/jwt/examples/verified-claim/)
- [Consumer entity](https://developer.konghq.com/gateway/entities/consumer/)
- [ACL plugin](https://developer.konghq.com/plugins/acl/)
