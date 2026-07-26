---
title: "Basic Auth en kong"
date: 2026-07-26T00:00:00+02:00
description: "Cómo funciona HTTP Basic Authentication y cómo proteger un recurso HTTPRoute con el plugin Basic Auth de Kong Gateway y KIC."
tags: [Kong, Autenticación, Basic Auth, KIC, Gateway API]
weight: 10
hero: images/kong/basic-auth.png
aliases:
  - /posts/kong/10-autenticacion-basic-auth/10-autenticacion-basic-auth/
---

Basic Authentication suele parecer un mecanismo trivial porque solo utiliza un usuario y una contraseña. Sin embargo, para utilizarlo correctamente conviene separar tres ideas: el estándar HTTP, la validación que realiza Kong Gateway y la identidad que Kong asocia a unas credenciales válidas.

En este artículo veremos esas tres capas y construiremos un laboratorio reproducible con Kong Ingress Controller. El objetivo no es limitarse a copiar ficheros y aplicarlos sin cabeza. Primero entenderemos qué representa cada recurso, después lo aplicaremos y finalmente comprobaremos qué ocurre dentro de Kong.

> [!NOTE]
> Este laboratorio continúa exactamente desde el escenario creado en [Instalación de KIC](/posts/kong/03-instalacion-kic/03-instalacion-kic/). Reutiliza el `Gateway` `kong`, el servicio `echo` y la dirección `192.168.121.200` asignada por MetalLB a `kong-gateway-proxy`.
>
> Las pruebas de este artículo se han realizado con Kong Gateway `3.10.0.16` y Kong Ingress Controller `3.5`

## 1. ¿Qué es Basic Authentication?

Basic Authentication es un esquema de autenticación definido por [RFC 7617](https://www.rfc-editor.org/rfc/rfc7617.html). Permite que un cliente HTTP envíe un identificador de usuario y una contraseña dentro de la cabecera `Authorization`.

El cliente comienza construyendo una cadena con este formato:

```text
username:password
```

El carácter `:` separa ambos valores. Después, el cliente codifica la cadena con Base64 y añade el resultado a la cabecera HTTP:

```text
username:password
        |
        v
      Base64
        |
        v
Authorization: Basic <credentials>
```

En nuestro laboratorio utilizaremos:

```text
alice:alice-basic-password
```

Podemos calcular su representación Base64 desde la terminal. Utilizamos `-n` para que `echo` no añada un salto de línea al final de la cadena:

```bash
echo -n 'alice:alice-basic-password' | base64
```

El resultado es:

```text
YWxpY2U6YWxpY2UtYmFzaWMtcGFzc3dvcmQ=
```

Por tanto, la cabecera completa es:

```http
Authorization: Basic YWxpY2U6YWxpY2UtYmFzaWMtcGFzc3dvcmQ=
```

Base64 es una codificación, no un cifrado. Cualquiera que capture la cabecera puede decodificarla y recuperar el usuario y la contraseña. Por eso Basic Authentication debe utilizarse sobre HTTPS. TLS es quien aporta confidencialidad e integridad durante el transporte.

El estándar también define el desafío que puede devolver el servidor cuando faltan credenciales. En este artículo nos centraremos en el código `401 Unauthorized` y en la validación que realiza Kong.

## 2. ¿Cómo funciona Basic Authentication en Kong Gateway?

Kong implementa este mecanismo mediante el plugin oficial [`basic-auth`](https://developer.konghq.com/plugins/basic-auth/). El plugin está disponible para las topologías traditional, hybrid y DB-less, y puede aplicarse globalmente, a un `Service` de Gateway o a una `Route`.

En este laboratorio lo aplicaremos únicamente a la `Route` generada a partir de `/basic-auth`. De esta forma, el resto de rutas publicadas en `echo.javiercd.es` no quedan protegidas por este plugin.

Cuando una petición coincide con la `Route`, Kong ejecuta el plugin durante el procesamiento de acceso, antes de enviar la petición al upstream. Según la documentación oficial, busca credenciales en este orden:

1. `Proxy-Authorization`
2. `Authorization`

Si encuentra una cabecera Basic, decodifica el valor, localiza la credencial y compara la contraseña recibida con la almacenada para esa identidad.

El siguiente diagrama resume las dos posibles ramas del plugin. Las credenciales inválidas terminan en Kong con un `401 Unauthorized`. Las credenciales válidas identifican al consumidor (`Consumer`) y permiten continuar hasta el upstream.

![Flujo de Basic Authentication en Kong Gateway](/kong/plugins-autenticacion/10-autenticacion-basic-auth/img/basic-auth-flow.svg)

El comportamiento es el siguiente:

- Si no hay credenciales y no se ha configurado acceso anónimo, Kong responde `401 Unauthorized`.
- Si el usuario no existe, Kong responde `401 Unauthorized`.
- Si la contraseña no coincide, Kong responde `401 Unauthorized`.
- Si las credenciales son válidas, Kong identifica al consumidor (`Consumer`) y permite que la petición continúe.
- Cuando Kong rechaza la autenticación, la petición no llega al upstream.

El plugin Basic Auth no decide por sí mismo a qué backend se envía una petición. La selección del backend sigue siendo responsabilidad de la `Route` y del `Service`. El plugin solo introduce una condición previa, que el cliente debe autenticarse correctamente.

## 3. Consumidores y credenciales Basic Auth

Un consumidor (`Consumer`) es la representación que utiliza Kong para identificar a un cliente de una API. Puede representar a una persona, una aplicación, un servicio, un dispositivo o cualquier otra entidad que necesite consumir una API.

No hay que confundir tres nombres distintos del laboratorio:

- `basic-auth-client` es el nombre del recurso `KongConsumer` en Kubernetes.
- `alice` es el `username` del consumidor (`Consumer`) en Kong.
- `alice` también es el usuario de la credencial Basic Auth.

Aunque en este ejemplo coinciden, el `username` del consumidor (`Consumer`) y el `username` de la credencial son campos diferentes.

La relación es:

```text
Consumidor
    |
    +-- Credencial Basic Auth
            |
            +-- username
            +-- password
```

El consumidor (`Consumer`) aporta la identidad. La credencial aporta la prueba que permite demostrar esa identidad. Cuando la validación termina correctamente, Kong conoce tanto al consumidor autenticado como el identificador de la credencial utilizada.

Un mismo consumidor (`Consumer`) puede tener varias credenciales. Pero lo normal es asignarle una sola credencial por consumidor y asi asegurarnos de controlar quien consume nuestras apis.

## 4. Configuración de Basic Auth en Kong con KIC

Vamos a publicar el servicio `echo` mediante un `HTTPRoute` y proteger esa ruta con Basic Auth.

El post de instalación de KIC ya creó estos recursos compartidos:

- El `Gateway` `kong` en el namespace `kong`.
- El servicio `echo` en el namespace `javier`.
- El proxy de Kong expuesto mediante MetalLB.

No volveremos a crearlos. Este laboratorio solo añade un `KongPlugin`, un `Secret`, un `KongConsumer` y un `HTTPRoute`.

### 4.1. Relación entre los recursos de Kubernetes y Kong

| Recurso de Kubernetes | Recurso interno de Kong |
| --- | --- |
| `KongPlugin` | `plugins` |
| `Secret` | `basicauth_credentials` |
| `KongConsumer` | `consumers` |
| `HTTPRoute` | `routes`, `services`, `upstreams` y `targets` |

En modo DB-less estas traducciones forman parte de la configuración en memoria de Kong. En modo traditional se reflejarían en entidades como `plugins`, `basicauth_credentials`, `consumers`, `routes`, `services`, `upstreams` y `targets`.

### 4.2. Crear el plugin de basic-auth

Este fichero declara el plugin que realizará la validación.

`hide_credentials: true` indica que Kong debe retirar la cabecera utilizada para autenticarse antes de enviar la petición al upstream. `realm` define el ámbito que Kong anuncia mediante `WWW-Authenticate` cuando rechaza la autenticación.

El `KongPlugin` todavía no protege ninguna ruta por sí solo. Quedará asociado cuando añadamos su nombre a la anotación del `HTTPRoute`.

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: basic-auth
  namespace: javier
plugin: basic-auth
config:
  hide_credentials: true
  realm: javier-basic-auth
```

En una instalación con base de datos, esta configuración se traduciría a una entidad de `plugins`. Al asociarla con la `Route`, la entidad tendría una referencia a esa `Route`.

### 4.3. Crear la credencial

KIC utiliza un `Secret` de Kubernetes para declarar las credenciales de los plugins de autenticación.

La etiqueta `konghq.com/credential: basic-auth` es imprescindible. Permite que KIC interprete `username` y `password` como una credencial Basic Auth en lugar de tratar el objeto como un `Secret` genérico.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: basic-auth-credential
  namespace: javier
  labels:
    konghq.com/credential: basic-auth
stringData:
  username: alice
  password: alice-basic-password
```

El uso de `stringData` facilita el laboratorio porque Kubernetes realiza la codificación Base64 al guardar el `Secret`. Esa codificación de Kubernetes tampoco cifra la contraseña.

KIC lee este `Secret` y lo traduce a una credencial Basic Auth. En un Kong con base de datos se correspondería con una entidad de `basicauth_credentials`, no con una tabla genérica de Secrets.

### 4.4. Crear el consumidor `KongConsumer`

El `KongConsumer` crea la identidad `alice` y referencia el `Secret` anterior mediante `credentials`.

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: basic-auth-client
  namespace: javier
  annotations:
    kubernetes.io/ingress.class: kong
username: alice
credentials:
  - basic-auth-credential
```

KIC resuelve la referencia `basic-auth-credential`, crea el consumidor (`Consumer`) y asocia la credencial. En modo traditional, el consumidor se representaría en `consumers` y la credencial mantendría la relación con su identificador.

### 4.5. Crear el `HTTPRoute`

El `HTTPRoute` publica la ruta `/basic-auth` en `echo.javiercd.es`.

`parentRefs` conecta la ruta con el `Gateway` `kong`. `backendRefs` reutiliza el servicio `echo`. La anotación `konghq.com/plugins: basic-auth` aplica el `KongPlugin` creado anteriormente.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: basic-auth
  namespace: javier
  annotations:
    konghq.com/plugins: basic-auth
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
            value: /basic-auth
      backendRefs:
        - name: echo
          port: 80
```

KIC traduce esta definición a una `Route` de Kong. También crea o reutiliza las entidades internas necesarias para alcanzar los endpoints del servicio `echo`. La anotación produce la asociación entre la `Route` y el plugin.

### 4.6. Aplicar los manifiestos

Aplicamos los recursos en el orden en que los hemos explicado:

```bash
sudo kubectl apply -f 10-basic-auth-plugin.yaml
sudo kubectl apply -f 10-basic-auth-secret.yaml
sudo kubectl apply -f 10-basic-auth-consumer.yaml
sudo kubectl apply -f 10-basic-auth-httproute.yaml
```

Comprobamos su estado:

```bash
sudo kubectl get kongplugin basic-auth -n javier
sudo kubectl get kongconsumer basic-auth-client -n javier
sudo kubectl get httproute basic-auth -n javier
sudo kubectl describe httproute basic-auth -n javier
```

El `HTTPRoute` debe aparecer aceptado por el `Gateway`.

## 5. Probando Basic Authentication

Vamos a probar la configuración que hemos desplegado. Las respuestas mostradas a continuación se han capturado directamente en la VM del laboratorio.

### 5.1. Petición sin credenciales

Realizamos la petición sin enviar credenciales:

```bash
curl -i http://echo.javiercd.es/basic-auth
```

La respuesta observada en el laboratorio es:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:01:38 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: Basic realm="javier-basic-auth"
Content-Length: 26
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: da02e8552baa4a0f020f5761b6401524

{"message":"Unauthorized"}
```

No aparece `X-Kong-Upstream-Latency` porque Kong ha generado la respuesta antes de contactar con `echo`.

### 5.2. Credenciales incorrectas

Ahora enviaremos la petición utilizando unas credenciales incorrectas mediante `curl -u`, que construye la cabecera `Authorization: Basic` por nosotros:

```bash
curl -i -u alice:incorrecta \
  http://echo.javiercd.es/basic-auth
```

La respuesta vuelve a ser:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:01:38 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: Basic realm="javier-basic-auth"
Content-Length: 26
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: baf09c5e879385768ab2480cf3c5bc3f

{"message":"Unauthorized"}
```

Kong no revela si el error se debe a un usuario inexistente o a una contraseña incorrecta.

### 5.3. Credenciales correctas

```bash
curl -i -u alice:alice-basic-password \
  http://echo.javiercd.es/basic-auth
```

La respuesta observada es:

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: 28
Connection: keep-alive
X-App-Name: http-echo
X-App-Version: 1.0.0
Date: Sun, 26 Jul 2026 09:01:38 GMT
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Upstream-Latency: 0
X-Kong-Proxy-Latency: 1
Via: 1.1 kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 229ad4616bfa4a0c334d112502217437

Hola desde Kong Gateway KIC
```

Esta vez Kong ha identificado al consumidor (`Consumer`) y ha enviado la petición al upstream.

También podemos enviar la cabecera manualmente:

```bash
curl -i \
  -H 'Authorization: Basic YWxpY2U6YWxpY2UtYmFzaWMtcGFzc3dvcmQ=' \
  http://echo.javiercd.es/basic-auth
```


## Fuentes oficiales

- [RFC 7617: The Basic HTTP Authentication Scheme](https://www.rfc-editor.org/rfc/rfc7617.html)
- [Basic Auth plugin](https://developer.konghq.com/plugins/basic-auth/)
- [Basic Auth configuration reference](https://developer.konghq.com/plugins/basic-auth/reference/)
- [Basic Auth changelog](https://developer.konghq.com/plugins/basic-auth/changelog/)
- [Authenticate Consumers with Basic Auth](https://developer.konghq.com/how-to/authenticate-consumers-with-basic-authentication/)
- [Consumer entity](https://developer.konghq.com/gateway/entities/consumer/)
- [Kong Identity Principals](https://developer.konghq.com/identity/principals/)
- [ACL plugin](https://developer.konghq.com/plugins/acl/)
