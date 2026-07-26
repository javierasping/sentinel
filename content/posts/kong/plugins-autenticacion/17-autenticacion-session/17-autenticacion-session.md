---
title: "Session en Kong"
date: 2026-07-26T00:00:00+02:00
description: "Cómo crear y reutilizar una sesión de navegador en Kong Gateway combinando los plugins Session y Key Auth con KIC."
tags: [Kong, Autenticación, Sesiones, Cookies, KIC]
weight: 17
hero: images/kong/session.png
---

El plugin Session permite que un cliente autenticado reutilice su identidad mediante una cookie. No autentica por sí solo: necesita trabajar junto a otro mecanismo que valide la primera petición.

En este laboratorio combinaremos Session con Key Auth. La primera petición presentará una API key, Kong creará una sesión y las siguientes peticiones utilizarán únicamente la cookie. También configuraremos explícitamente la rama anónima para impedir que una petición sin ninguna credencial llegue al backend.

> [!NOTE]
> Este laboratorio continúa exactamente desde el escenario creado en [Instalación de KIC](/posts/kong/03-instalacion-kic/03-instalacion-kic/). Reutiliza el `Gateway` `kong`, el servicio `echo` y la dirección `192.168.121.200` asignada por MetalLB a `kong-gateway-proxy`.
>
> Las pruebas se han realizado con Kong Gateway `3.10.0.16` y Kong Ingress Controller `3.5`.

## 1. ¿Qué es una sesión?

Una sesión permite conservar el resultado de una autenticación durante varias peticiones. En lugar de volver a enviar la credencial principal cada vez, el cliente presenta una cookie protegida por Kong.

En nuestro laboratorio existen dos credenciales:

- La API key `session-api-key`, utilizada para la autenticación inicial.
- La cookie de sesión generada después por Kong.

El flujo es:

1. El cliente envía la API key.
2. Key Auth valida la credencial e identifica al Consumer.
3. Session crea una cookie que representa esa identidad.
4. El cliente almacena la cookie.
5. En peticiones posteriores, Session valida la cookie.
6. Key Auth reconoce que la identidad ya procede de una sesión válida.
7. La petición continúa sin volver a enviar la API key.

La cookie no contiene la API key. Con `storage: cookie`, contiene los datos de sesión cifrados y protegidos criptográficamente.

Una sesión reduce la exposición repetida de la credencial inicial, pero introduce su propio ciclo de vida: creación, renovación, caducidad y cierre. Debe protegerse siempre mediante HTTPS y atributos seguros de cookie.

## 2. ¿Cómo funciona Session en Kong Gateway?

Kong implementa este mecanismo mediante el plugin oficial [`session`](https://developer.konghq.com/plugins/session/). Está disponible para las topologías traditional, hybrid y DB-less y siempre debe combinarse con otro plugin de autenticación.

Session tiene una prioridad superior a Key Auth, por lo que examina la petición primero:

- Si encuentra una sesión válida, restaura el Consumer y la credencial autenticados.
- Si no encuentra sesión, permite que Key Auth intente autenticar la API key.
- Si Key Auth tiene éxito, Session crea la cookie en la respuesta.

Esta combinación funciona como un OR lógico: sesión válida o API key válida. Por este motivo necesitamos controlar explícitamente la rama en la que no existe ninguna de las dos.

Configuraremos `anonymous: anonymous-session` en Key Auth. Cuando no haya una API key válida, Kong asignará temporalmente ese Consumer. El plugin `request-termination`, aplicado al Consumer anónimo, responderá `403 Forbidden`.

Sin esa rama de rechazo, una configuración de autenticación múltiple puede permitir que una petición anónima continúe.

El diagrama muestra las tres ramas. Una cookie válida restaura la identidad. Sin cookie, una API key válida autentica al Consumer y provoca la creación de una nueva sesión. Si no existe ninguna credencial válida, `request-termination` detiene la petición con `403 Forbidden`.

![Flujo de Session y Key Auth en Kong](/kong/plugins-autenticacion/17-autenticacion-session/img/session-auth-flow.svg)

## 3. Consumer autenticado y Consumer anónimo

El laboratorio utiliza dos Consumers:

- `session-client` representa al cliente autenticado y tiene la API key.
- `anonymous-session` representa las peticiones que no han aportado ni sesión ni API key válida.

La relación es:

```text
Route /session
    |
    +-- Session
    |
    +-- Key Auth
            |
            +-- API key válida --> session-client --> upstream
            |
            +-- sin credencial --> anonymous-session --> 403
```

`request-termination` no autentica. Solo finaliza las peticiones que Key Auth ha asociado al Consumer anónimo.

## 4. Configuración de Session con KIC

Este laboratorio añade tres `KongPlugin`, dos `KongConsumer`, un `Secret` y un `HTTPRoute`.

### 4.1. Relación entre los recursos de Kubernetes y Kong

| Recurso de Kubernetes | Función en Kong |
| --- | --- |
| `KongPlugin` Session | Gestiona la cookie y los datos de sesión |
| `KongPlugin` Key Auth | Valida la credencial inicial |
| `Secret` | Crea la API key |
| `KongConsumer` autenticado | Representa al cliente válido |
| `KongPlugin` Request Termination | Construye la respuesta `403` |
| `KongConsumer` anónimo | Recibe las peticiones no autenticadas |
| `HTTPRoute` | Publica la ruta y aplica Session y Key Auth |

### 4.2. Crear el plugin Session

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: session
  namespace: javier
plugin: session
config:
  storage: cookie
  cookie_secure: false
  cookie_http_only: true
  cookie_same_site: Strict
  secret: session-kic-secret-32-bytes-change-me
```

- `storage: cookie` guarda los datos cifrados en la cookie.
- `cookie_http_only: true` impide que JavaScript pueda leerla.
- `cookie_same_site: Strict` reduce el envío en contextos entre sitios.
- `secret` protege criptográficamente la sesión.

`cookie_secure: false` solo es válido porque el laboratorio utiliza HTTP. En producción debe cambiarse a `true` y la ruta debe publicarse mediante HTTPS.

### 4.3. Crear el plugin Key Auth

Aceptaremos la API key únicamente en la cabecera `apikey`. `anonymous` selecciona la identidad utilizada cuando la autenticación inicial falla.

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: session-key-auth
  namespace: javier
plugin: key-auth
config:
  key_names:
    - apikey
  key_in_header: true
  key_in_query: false
  key_in_body: false
  hide_credentials: true
  anonymous: anonymous-session
```

### 4.4. Crear la credencial Key Auth

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: session-key-credential
  namespace: javier
  labels:
    konghq.com/credential: key-auth
stringData:
  key: session-api-key
```

La clave es legible para facilitar el laboratorio. En producción debe generarse aleatoriamente y almacenarse de forma segura.

### 4.5. Crear el Consumer autenticado

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: session-client
  namespace: javier
  annotations:
    kubernetes.io/ingress.class: kong
username: session-client
credentials:
  - session-key-credential
```

### 4.6. Crear el plugin de rechazo

Este plugin construye la respuesta de la rama anónima:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: session-anonymous-deny
  namespace: javier
plugin: request-termination
config:
  status_code: 403
  message: Forbidden
```

### 4.7. Crear el Consumer anónimo

La anotación aplica `request-termination` únicamente a este Consumer:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: anonymous-session
  namespace: javier
  annotations:
    kubernetes.io/ingress.class: kong
    konghq.com/plugins: session-anonymous-deny
username: anonymous-session
```

El valor de `username` coincide con `anonymous` en el plugin Key Auth.

### 4.8. Crear el `HTTPRoute`

El `HTTPRoute` aplica los dos plugins que participan en la autenticación:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: session
  namespace: javier
  annotations:
    konghq.com/plugins: "session,session-key-auth"
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
            value: /session
      backendRefs:
        - name: echo
          port: 80
```

### 4.9. Aplicar los manifiestos

```bash
sudo kubectl apply -f 17-session-session-plugin.yaml
sudo kubectl apply -f 17-session-key-auth-plugin.yaml
sudo kubectl apply -f 17-session-secret.yaml
sudo kubectl apply -f 17-session-consumer.yaml
sudo kubectl apply -f 17-session-anonymous-plugin.yaml
sudo kubectl apply -f 17-session-anonymous-consumer.yaml
sudo kubectl apply -f 17-session-httproute.yaml
```

Comprobamos el estado:

```bash
sudo kubectl get kongplugin -n javier \
  session session-key-auth session-anonymous-deny
sudo kubectl get kongconsumer -n javier \
  session-client anonymous-session
sudo kubectl get httproute session -n javier
sudo kubectl describe httproute session -n javier
```

## 5. Probando la sesión

Las respuestas se han capturado directamente en la VM. El valor de la cookie cambia en cada autenticación.

### 5.1. Petición sin credenciales

```bash
curl -i http://echo.javiercd.es/session
```

Key Auth asigna el Consumer anónimo y `request-termination` responde:

```http
HTTP/1.1 403 Forbidden
Date: Sun, 26 Jul 2026 09:02:20 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
Content-Length: 23
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: b8feb11a7f653b271d9e0307ef677f7c

{"message":"Forbidden"}
```

La petición no llega al upstream.

### 5.2. Autenticación inicial mediante API key

Eliminamos cualquier cookie anterior y enviamos la API key. `-c` guarda las cookies de la respuesta:

```bash
rm -f cookies.txt

curl -i \
  -c cookies.txt \
  -H 'apikey: session-api-key' \
  http://echo.javiercd.es/session
```

Kong valida la API key, identifica a `session-client` y responde `200 OK`. Esta es la respuesta obtenida. El valor de `session` se ha abreviado porque es una credencial temporal:

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: 28
Connection: keep-alive
X-App-Name: http-echo
X-App-Version: 1.0.0
Date: Sun, 26 Jul 2026 09:02:20 GMT
Server: kong/3.10.0.16-enterprise-edition
Set-Cookie: session=<cookie-cifrada>; Path=/; SameSite=Strict; HttpOnly
X-Kong-Upstream-Latency: 0
X-Kong-Proxy-Latency: 1
Via: 1.1 kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 149a9d133f53693ff98ced2907d7fe05

Hola desde Kong Gateway KIC
```

Podemos inspeccionar el fichero:

```bash
sed -n '1,20p' cookies.txt
```

### 5.3. Reutilizar la cookie

Ahora no enviamos la API key. `-b` carga la cookie guardada:

```bash
curl -i \
  -b cookies.txt \
  http://echo.javiercd.es/session
```

Session restaura la identidad del consumidor y la petición vuelve a alcanzar el upstream. Esta segunda respuesta ya no incluye `Set-Cookie`:

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: 28
Connection: keep-alive
X-App-Name: http-echo
X-App-Version: 1.0.0
Date: Sun, 26 Jul 2026 09:02:20 GMT
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Upstream-Latency: 0
X-Kong-Proxy-Latency: 0
Via: 1.1 kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: c521543370e6515210393866dd02a849

Hola desde Kong Gateway KIC
```

### 5.4. Comprobar una cookie inválida

```bash
curl -i \
  -H 'Cookie: session=valor-manipulado' \
  http://echo.javiercd.es/session
```

Kong no puede validar la sesión. Como tampoco existe una API key válida, la petición termina en el Consumer anónimo:

```http
HTTP/1.1 403 Forbidden
Date: Sun, 26 Jul 2026 09:02:20 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
Content-Length: 23
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: e1748807abaf015060939939a9c3db13

{"message":"Forbidden"}
```

Con `storage: cookie`, eliminar `cookies.txt` cierra la sesión desde el punto de vista del cliente. Para disponer de invalidación centralizada y almacenamiento en el gateway se necesita `storage: kong`, una estrategia con base de datos y una configuración acorde con esa topología.

## Fuentes oficiales

- [Session plugin](https://developer.konghq.com/plugins/session/)
- [Session configuration reference](https://developer.konghq.com/plugins/session/reference/)
- [Key Auth plugin](https://developer.konghq.com/plugins/key-auth/)
- [Request Termination plugin](https://developer.konghq.com/plugins/request-termination/)
- [Multiple authentication](https://developer.konghq.com/gateway/authentication/#multiple-authentication)
- [Consumer entity](https://developer.konghq.com/gateway/entities/consumer/)
