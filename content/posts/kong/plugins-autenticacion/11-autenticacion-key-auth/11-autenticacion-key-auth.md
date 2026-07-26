---
title: "Key Auth en Kong"
date: 2026-07-26T00:00:00+02:00
description: "Cómo funciona la autenticación mediante API keys y cómo proteger un recurso HTTPRoute con el plugin Key Auth de Kong Gateway y KIC."
tags: [Kong, Autenticación, API Key, Key Auth, KIC]
weight: 11
hero: images/kong/key-auth.png
aliases:
  - /posts/kong/11-autenticacion-key-auth/11-autenticacion-key-auth/
---

Una API key suele parecer poco más que una cadena aleatoria que el cliente añade a cada petición. Sin embargo, para utilizarla correctamente conviene separar tres ideas: la credencial que presenta el cliente, la validación que realiza Kong Gateway y la identidad del consumidor (`Consumer`) asociado a esa credencial.

En este artículo veremos esas tres capas y construiremos un laboratorio reproducible con Kong Ingress Controller. El objetivo no es limitarse a copiar ficheros y aplicarlos sin cabeza. Primero entenderemos qué representa cada recurso, después lo aplicaremos y finalmente comprobaremos qué ocurre dentro de Kong.

> [!NOTE]
> Este laboratorio continúa exactamente desde el escenario creado en [Instalación de KIC](/posts/kong/03-instalacion-kic/03-instalacion-kic/). Reutiliza el `Gateway` `kong`, el servicio `echo` y la dirección `192.168.121.200` asignada por MetalLB a `kong-gateway-proxy`.
>
> Las pruebas de este artículo se han realizado con Kong Gateway `3.10.0.16` y Kong Ingress Controller `3.5`.

## 1. ¿Qué es una API key?

Una API key es una credencial que una aplicación utiliza para identificarse ante una API. Normalmente se genera como una cadena larga y difícil de adivinar:

```text
my-super-secret-api-key
```

A diferencia de Basic Authentication, el cliente no envía un usuario y una contraseña. Envía directamente una clave que Kong puede relacionar con una credencial y, a través de ella, con un consumidor (`Consumer`).

Key Auth no define una cabecera HTTP universal. El nombre y la ubicación de la API key dependen de la configuración del gateway. Kong puede buscarla en:

- Una cabecera HTTP.
- Un parámetro de la URL.
- El cuerpo de la petición.

En este laboratorio utilizaremos una cabecera llamada `apikey`:

```http
apikey: my-super-secret-api-key
```

La API key es un secreto compartido. Cualquier cliente que la conozca puede utilizarla mientras siga siendo válida. No debe incluirse directamente en el código fuente ni publicarse en un repositorio y, al igual que una contraseña, debe enviarse siempre mediante HTTPS.

También conviene evitar las API keys en parámetros de la URL. Las URLs pueden quedar registradas en historiales, proxies, herramientas de observabilidad y logs de acceso. Por este motivo configuraremos el plugin para aceptar la clave únicamente desde una cabecera.

La autenticación mediante API key demuestra que el cliente conoce una credencial válida. No cifra la petición ni sustituye a TLS. Tampoco decide por sí sola qué recursos puede utilizar el consumidor. Esa segunda decisión corresponde a la autorización y puede implementarse, por ejemplo, con el plugin ACL.

## 2. ¿Cómo funciona Key Auth en Kong Gateway?

Kong implementa este mecanismo mediante el plugin oficial [`key-auth`](https://developer.konghq.com/plugins/key-auth/). El plugin está disponible para las topologías traditional, hybrid y DB-less, y puede aplicarse globalmente, a un `Service` de Gateway o a una `Route`.

En este laboratorio lo aplicaremos únicamente a la `Route` generada a partir de `/key-auth`. De esta forma, el resto de rutas publicadas en `echo.javiercd.es` no quedan protegidas por este plugin.

Cuando una petición coincide con la `Route`, Kong ejecuta el plugin durante el procesamiento de acceso, antes de enviar la petición al upstream. En nuestra configuración ocurre lo siguiente:

1. Kong busca una cabecera llamada `apikey`.
2. Si no existe, rechaza la petición.
3. Si existe, busca una credencial con ese valor.
4. Si la credencial no existe, rechaza la petición.
5. Si la credencial es válida, identifica al consumidor asociado.
6. Antes de contactar con el upstream, elimina la cabecera `apikey`.
7. Kong añade cabeceras con la identidad del consumidor y permite que la petición continúe.

El siguiente diagrama resume el flujo completo. Una clave ausente o desconocida termina en Kong con un `401 Unauthorized`. Una clave válida identifica al Consumer, se elimina antes de enviar la petición y se sustituye por cabeceras de identidad.

![Flujo de Key Auth en Kong Gateway](/kong/plugins-autenticacion/11-autenticacion-key-auth/img/key-auth-flow.svg)

El comportamiento es el siguiente:

- Si no se envía una API key y no se ha configurado acceso anónimo, Kong responde `401 Unauthorized`.
- Si se envía una API key desconocida, Kong responde `401 Unauthorized`.
- Si la credencial es válida, Kong identifica al consumidor (`Consumer`) y permite que la petición continúe.
- Cuando Kong rechaza la autenticación, la petición no llega al upstream.

Después de autenticar al consumidor, Kong puede añadir cabeceras como `X-Consumer-ID`, `X-Consumer-Username` y `X-Credential-Identifier`. Estas cabeceras permiten que el backend conozca la identidad validada sin recibir la API key original.

El plugin Key Auth no decide por sí mismo a qué backend se envía una petición. La selección del backend sigue siendo responsabilidad de la `Route` y del `Service`. El plugin solo introduce una condición previa, que el cliente debe autenticarse correctamente.

## 3. Consumidores y credenciales Key Auth

Un consumidor (`Consumer`) es la representación que utiliza Kong para identificar a un cliente de una API. Puede representar a una persona, una aplicación, un servicio, un dispositivo o cualquier otra entidad que necesite consumir una API.

No hay que confundir los tres valores del laboratorio:

- `key-auth-client` es el nombre del recurso `KongConsumer` en Kubernetes.
- `key-client` es el `username` del consumidor (`Consumer`) en Kong.
- `my-super-secret-api-key` es el valor de la credencial Key Auth.

La relación es:

```text
Consumidor
    |
    +-- Credencial Key Auth
            |
            +-- key
```

El consumidor (`Consumer`) aporta la identidad. La API key aporta la prueba que permite demostrar esa identidad. Cuando la validación termina correctamente, Kong conoce tanto al consumidor autenticado como el identificador de la credencial utilizada.

Un mismo consumidor (`Consumer`) puede tener varias credenciales. Pero lo normal es asignarle una sola credencial por consumidor y así asegurarnos de controlar quién consume nuestras APIs.

La clave `my-super-secret-api-key` facilita la lectura del laboratorio, pero no es una credencial apropiada para producción. En un entorno real debe generarse con suficiente entropía, almacenarse en un gestor de secretos y rotarse cuando sea necesario.

## 4. Configuración de Key Auth en Kong con KIC

Vamos a publicar el servicio `echo` mediante un `HTTPRoute` y proteger esa ruta con Key Auth.

El post de instalación de KIC ya creó estos recursos compartidos:

- El `Gateway` `kong` en el namespace `kong`.
- El servicio `echo` en el namespace `javier`.
- El proxy de Kong expuesto mediante MetalLB.

No volveremos a crearlos. Este laboratorio solo añade un `KongPlugin`, un `Secret`, un `KongConsumer` y un `HTTPRoute`.

### 4.1. Relación entre los recursos de Kubernetes y Kong

| Recurso de Kubernetes | Recurso interno de Kong |
| --- | --- |
| `KongPlugin` | `plugins` |
| `Secret` | `keyauth_credentials` |
| `KongConsumer` | `consumers` |
| `HTTPRoute` | `routes`, `services`, `upstreams` y `targets` |

En modo DB-less estas traducciones forman parte de la configuración en memoria de Kong. En modo traditional se reflejarían en entidades como `plugins`, `keyauth_credentials`, `consumers`, `routes`, `services`, `upstreams` y `targets`.

### 4.2. Crear el plugin de key-auth

Este fichero declara el plugin que realizará la validación.

`key_names` define el nombre de la cabecera que contendrá la API key. `key_in_header: true` permite buscarla en las cabeceras, mientras que `key_in_query: false` y `key_in_body: false` desactivan las otras ubicaciones.

`hide_credentials: true` indica que Kong debe retirar la API key antes de enviar la petición al upstream.

El `KongPlugin` todavía no protege ninguna ruta por sí solo. Quedará asociado cuando añadamos su nombre a la anotación del `HTTPRoute`.

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: key-auth
  namespace: javier
plugin: key-auth
config:
  key_names:
    - apikey
  key_in_header: true
  key_in_query: false
  key_in_body: false
  hide_credentials: true
```

En una instalación con base de datos, esta configuración se traduciría a una entidad de `plugins`. Al asociarla con la `Route`, la entidad tendría una referencia a esa `Route`.

### 4.3. Crear la credencial

KIC utiliza un `Secret` de Kubernetes para declarar las credenciales de los plugins de autenticación.

La etiqueta `konghq.com/credential: key-auth` es imprescindible. Permite que KIC interprete el campo `key` como una credencial Key Auth en lugar de tratar el objeto como un `Secret` genérico.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: key-auth-credential
  namespace: javier
  labels:
    konghq.com/credential: key-auth
stringData:
  key: my-super-secret-api-key
```

El uso de `stringData` facilita el laboratorio porque Kubernetes realiza la codificación Base64 al guardar el `Secret`. Esa codificación de Kubernetes no cifra la API key.

KIC lee este `Secret` y lo traduce a una credencial Key Auth. En un Kong con base de datos se correspondería con una entidad de `keyauth_credentials`, no con una tabla genérica de Secrets.

### 4.4. Crear el consumidor `KongConsumer`

El `KongConsumer` crea la identidad `key-client` y referencia el `Secret` anterior mediante `credentials`.

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: key-auth-client
  namespace: javier
  annotations:
    kubernetes.io/ingress.class: kong
username: key-client
credentials:
  - key-auth-credential
```

KIC resuelve la referencia `key-auth-credential`, crea el consumidor (`Consumer`) y asocia la credencial. En modo traditional, el consumidor se representaría en `consumers` y la credencial mantendría la relación con su identificador.

### 4.5. Crear el `HTTPRoute`

El `HTTPRoute` publica la ruta `/key-auth` en `echo.javiercd.es`.

`parentRefs` conecta la ruta con el `Gateway` `kong`. `backendRefs` reutiliza el servicio `echo`. La anotación `konghq.com/plugins: key-auth` aplica el `KongPlugin` creado anteriormente.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: key-auth
  namespace: javier
  annotations:
    konghq.com/plugins: key-auth
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
            value: /key-auth
      backendRefs:
        - name: echo
          port: 80
```

KIC traduce esta definición a una `Route` de Kong. También crea o reutiliza las entidades internas necesarias para alcanzar los endpoints del servicio `echo`. La anotación produce la asociación entre la `Route` y el plugin.

### 4.6. Aplicar los manifiestos

Aplicamos los recursos en el orden en que los hemos explicado:

```bash
sudo kubectl apply -f 11-key-auth-plugin.yaml
sudo kubectl apply -f 11-key-auth-secret.yaml
sudo kubectl apply -f 11-key-auth-consumer.yaml
sudo kubectl apply -f 11-key-auth-httproute.yaml
```

Comprobamos su estado:

```bash
sudo kubectl get kongplugin key-auth -n javier
sudo kubectl get kongconsumer key-auth-client -n javier
sudo kubectl get httproute key-auth -n javier
sudo kubectl describe httproute key-auth -n javier
```

El `HTTPRoute` debe aparecer aceptado por el `Gateway`.

## 5. Probando la autenticación mediante API key

Vamos a probar la configuración que hemos desplegado. Las respuestas mostradas se han capturado directamente en la VM después de que KIC sincronizara el plugin con Kong.

### 5.1. Petición sin API key

Realizamos la petición sin enviar ninguna credencial:

```bash
curl -i http://echo.javiercd.es/key-auth
```

Kong responde antes de contactar con el upstream:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:01:38 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: Key
Content-Length: 96
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 33d2aa6620e5600619ef1f3cc9262529

{
  "message":"No API key found in request",
  "request_id":"33d2aa6620e5600619ef1f3cc9262529"
}
```

La respuesta no contiene `X-Kong-Upstream-Latency` porque Kong la ha generado antes de contactar con `echo`.

### 5.2. API key incorrecta

Ahora enviaremos una API key que Kong no tiene asociada a ninguna credencial:

```bash
curl -i \
  -H 'apikey: incorrecta' \
  http://echo.javiercd.es/key-auth
```

Kong vuelve a responder `401 Unauthorized`:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:01:38 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: Key
Content-Length: 81
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 821af909aa88af45730f05506213df07

{
  "message":"Unauthorized",
  "request_id":"821af909aa88af45730f05506213df07"
}
```

Kong distingue internamente entre la ausencia de una API key y una credencial desconocida, pero en ambos casos bloquea la petición antes de llegar al upstream.

### 5.3. API key correcta

Enviamos la clave definida en el `Secret`:

```bash
curl -i \
  -H 'apikey: my-super-secret-api-key' \
  http://echo.javiercd.es/key-auth
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
X-Kong-Upstream-Latency: 1
X-Kong-Proxy-Latency: 0
Via: 1.1 kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: c20f3b492444df164a1f6201b915a14f

Hola desde Kong Gateway KIC
```

Esta vez Kong ha localizado la credencial, ha identificado al consumidor `key-client` y ha enviado la petición al upstream.

Como hemos configurado `hide_credentials: true`, el servicio `echo` no recibe la cabecera `apikey`. Kong puede enviar en su lugar las cabeceras de identidad `X-Consumer-ID`, `X-Consumer-Username` y `X-Credential-Identifier`.

La API key tampoco puede enviarse mediante la URL:

```bash
curl -i \
  'http://echo.javiercd.es/key-auth?apikey=my-super-secret-api-key'
```

Aunque `key_in_query` está habilitado por defecto en el plugin, nuestra configuración lo ha desactivado expresamente. La respuesta real es:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:01:38 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: Key
Content-Length: 96
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: d504a5297bc5250f227eb70b4c2f7351

{
  "message":"No API key found in request",
  "request_id":"d504a5297bc5250f227eb70b4c2f7351"
}
```

## Fuentes oficiales

- [Key Auth plugin](https://developer.konghq.com/plugins/key-auth/)
- [Key Auth configuration reference](https://developer.konghq.com/plugins/key-auth/reference/)
- [Key Authentication con KIC](https://developer.konghq.com/kubernetes-ingress-controller/get-started/key-authentication/)
- [Consumer entity](https://developer.konghq.com/gateway/entities/consumer/)
- [KIC annotation reference](https://developer.konghq.com/kubernetes-ingress-controller/reference/annotations/)
- [ACL con KIC](https://developer.konghq.com/kubernetes-ingress-controller/acl/)
