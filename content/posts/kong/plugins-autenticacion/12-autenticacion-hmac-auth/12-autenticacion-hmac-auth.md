---
title: "HMAC Auth en Kong"
date: 2026-07-26T00:00:00+02:00
description: "Cómo funciona la firma HMAC y cómo proteger un recurso HTTPRoute con el plugin HMAC Auth de Kong Gateway y KIC."
tags: [Kong, Autenticación, HMAC, Firmas, KIC]
weight: 12
hero: images/kong/hmac-auth.png
---

HMAC Authentication permite demostrar que una petición ha sido construida por un cliente que conoce un secreto compartido sin enviar ese secreto dentro de la petición. Además de autenticar al cliente, la firma permite detectar si los elementos firmados se han modificado durante el transporte.

En este artículo veremos cómo se construye una firma HMAC, cómo la valida Kong Gateway y cómo se relacionan el consumidor y su credencial. Después construiremos un laboratorio reproducible con Kong Ingress Controller y protegeremos la ruta `/hmac-auth`.

> [!NOTE]
> Este laboratorio continúa exactamente desde el escenario creado en [Instalación de KIC](/posts/kong/03-instalacion-kic/03-instalacion-kic/). Reutiliza el `Gateway` `kong`, el servicio `echo` y la dirección `192.168.121.200` asignada por MetalLB a `kong-gateway-proxy`.
>
> Las pruebas de este artículo se han realizado con Kong Gateway `3.10.0.16` y Kong Ingress Controller `3.5`.

## 1. ¿Qué es una firma HMAC?

HMAC, de *Hash-based Message Authentication Code*, combina una función hash con un secreto compartido. Tanto el cliente como Kong conocen ese secreto, pero no necesitan enviarlo por la red.

El cliente selecciona los componentes de la petición que quiere proteger y construye una cadena canónica. En nuestro laboratorio firmaremos:

- `date`, para limitar durante cuánto tiempo puede reutilizarse la petición.
- `@request-target`, que contiene el método y la ruta solicitada.
- `host`, que identifica el host de destino.

Para una petición `GET` a `/hmac-auth`, la cadena tendrá esta forma:

```text
date: Sun, 26 Jul 2026 10:00:00 GMT
@request-target: get /hmac-auth
host: echo.javiercd.es
```

El cliente procesa esa cadena con HMAC-SHA256 y el secreto compartido:

```text
Cadena canónica + secreto
            |
            v
       HMAC-SHA256
            |
            v
    Firma codificada en Base64
```

Después envía el resultado en la cabecera `Authorization`:

```http
Authorization: hmac username="hmac-client", algorithm="hmac-sha256", headers="date @request-target host", signature="<firma>"
```

HMAC no cifra la petición. Un observador todavía puede leer su contenido si se utiliza HTTP. Por eso debe emplearse HTTPS: TLS aporta confidencialidad y HMAC demuestra la integridad de los datos firmados y el conocimiento del secreto.

La fecha también ayuda a reducir los ataques de repetición. Kong comprueba que el reloj del cliente se encuentre dentro del margen configurado, que por defecto es de 300 segundos. El cliente y los nodos de Kong deben mantener sus relojes sincronizados.

## 2. ¿Cómo funciona HMAC Auth en Kong Gateway?

Kong implementa este mecanismo mediante el plugin oficial [`hmac-auth`](https://developer.konghq.com/plugins/hmac-auth/). El plugin está disponible para las topologías traditional, hybrid y DB-less, y puede aplicarse globalmente, a un `Service` de Gateway o a una `Route`.

En este laboratorio lo aplicaremos únicamente a la `Route` generada a partir de `/hmac-auth`.

Cuando una petición coincide con la `Route`, Kong ejecuta el plugin antes de contactar con el upstream:

1. Busca la firma primero en `Proxy-Authorization` y después en `Authorization`.
2. Obtiene el `username` indicado por el cliente.
3. Localiza la credencial HMAC asociada a ese nombre.
4. Comprueba que la firma incluya `date`, `@request-target` y `host`.
5. Reconstruye la misma cadena canónica con los datos de la petición.
6. Calcula la firma con el secreto almacenado y la compara con la recibida.
7. Comprueba que la fecha se encuentre dentro del margen permitido.
8. Si todo es correcto, identifica al consumidor y permite continuar.

El diagrama muestra las dos ramas resultantes. Kong rechaza una firma incorrecta, incompleta o fuera del margen temporal. Si la firma calculada coincide y la fecha es válida, asocia la petición al Consumer y la envía al upstream.

![Flujo de HMAC Auth en Kong Gateway](/kong/plugins-autenticacion/12-autenticacion-hmac-auth/img/hmac-auth-flow.svg)

El comportamiento es el siguiente:

- Si no hay firma, Kong responde `401 Unauthorized`.
- Si el usuario no existe, la firma no coincide o falta una cabecera obligatoria, Kong responde `401 Unauthorized`.
- Si la fecha queda fuera del margen permitido, Kong rechaza la petición.
- Si la firma es válida, Kong identifica al consumidor (`Consumer`) y envía la petición al upstream.
- Cuando Kong rechaza la autenticación, la petición no llega al servicio `echo`.

`hide_credentials: true` hace que Kong retire la cabecera utilizada para autenticarse antes de enviar la petición al upstream. Kong puede añadir en su lugar cabeceras como `X-Consumer-ID`, `X-Consumer-Username` y `X-Credential-Identifier`.

HMAC Auth autentica al consumidor, pero no decide a qué backend se envía la petición ni qué consumidores están autorizados para cada recurso. La selección del backend corresponde a la `Route` y al `Service`. Una autorización adicional puede implementarse con ACL.

## 3. Consumidores y credenciales HMAC

Un consumidor (`Consumer`) representa al cliente que utiliza la API. La credencial HMAC contiene el nombre que el cliente declara en la firma y el secreto compartido utilizado para calcularla.

No hay que confundir los tres valores del laboratorio:

- `hmac-auth-client` es el nombre del recurso `KongConsumer` en Kubernetes.
- `hmac-client` es el `username` del consumidor en Kong.
- `hmac-client` también es el `username` de la credencial HMAC.
- `hmac-shared-secret` es el secreto compartido.

La relación es:

```text
Consumidor
    |
    +-- Credencial HMAC
            |
            +-- username
            +-- secret
```

El consumidor aporta la identidad. La credencial aporta la información que Kong necesita para verificar la firma. Aunque los dos campos `username` coinciden en este laboratorio, pertenecen a objetos diferentes.

El secreto utilizado aquí facilita la reproducción del ejemplo. En producción debe generarse aleatoriamente, almacenarse en un gestor de secretos y distribuirse solo al cliente que vaya a firmar las peticiones.

## 4. Configuración de HMAC Auth en Kong con KIC

Vamos a publicar el servicio `echo` mediante un `HTTPRoute` y proteger esa ruta con HMAC Auth.

El post de instalación de KIC ya creó el `Gateway` `kong`, el servicio `echo` y el proxy expuesto mediante MetalLB. Este laboratorio solo añade un `KongPlugin`, un `Secret`, un `KongConsumer` y un `HTTPRoute`.

### 4.1. Relación entre los recursos de Kubernetes y Kong

| Recurso de Kubernetes | Recurso interno de Kong |
| --- | --- |
| `KongPlugin` | `plugins` |
| `Secret` | `hmacauth_credentials` |
| `KongConsumer` | `consumers` |
| `HTTPRoute` | `routes`, `services`, `upstreams` y `targets` |

En modo DB-less estas traducciones forman parte de la configuración en memoria de Kong. En modo traditional se reflejarían en las entidades correspondientes de la base de datos.

### 4.2. Crear el plugin de hmac-auth

`enforce_headers` obliga a que la firma proteja los tres elementos mínimos recomendados. El orden también importa, porque el cliente debe construir la cadena siguiendo el mismo orden declarado en `Authorization`.

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: hmac-auth
  namespace: javier
plugin: hmac-auth
config:
  enforce_headers:
    - date
    - "@request-target"
    - host
  hide_credentials: true
```

El `KongPlugin` no protege ninguna ruta por sí solo. Quedará asociado mediante la anotación del `HTTPRoute`.

### 4.3. Crear la credencial

La etiqueta `konghq.com/credential: hmac-auth` indica a KIC que debe traducir el `Secret` a una credencial HMAC.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: hmac-auth-credential
  namespace: javier
  labels:
    konghq.com/credential: hmac-auth
stringData:
  username: hmac-client
  secret: hmac-shared-secret
```

Kubernetes codifica los valores de `stringData` en Base64 al guardar el `Secret`. Esa codificación no cifra el secreto.

### 4.4. Crear el consumidor `KongConsumer`

El `KongConsumer` crea la identidad `hmac-client` y referencia la credencial anterior:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: hmac-auth-client
  namespace: javier
  annotations:
    kubernetes.io/ingress.class: kong
username: hmac-client
credentials:
  - hmac-auth-credential
```

KIC crea el consumidor y asocia la credencial HMAC. En modo traditional se representarían mediante `consumers` y `hmacauth_credentials`.

### 4.5. Crear el `HTTPRoute`

El `HTTPRoute` publica `/hmac-auth` y aplica el plugin mediante `konghq.com/plugins: hmac-auth`.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: hmac-auth
  namespace: javier
  annotations:
    konghq.com/plugins: hmac-auth
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
            value: /hmac-auth
      backendRefs:
        - name: echo
          port: 80
```

### 4.6. Aplicar los manifiestos

```bash
sudo kubectl apply -f 12-hmac-auth-plugin.yaml
sudo kubectl apply -f 12-hmac-auth-secret.yaml
sudo kubectl apply -f 12-hmac-auth-consumer.yaml
sudo kubectl apply -f 12-hmac-auth-httproute.yaml
```

Comprobamos el estado:

```bash
sudo kubectl get kongplugin hmac-auth -n javier
sudo kubectl get kongconsumer hmac-auth-client -n javier
sudo kubectl get httproute hmac-auth -n javier
sudo kubectl describe httproute hmac-auth -n javier
```

## 5. Probando HMAC Authentication

Las respuestas de esta sección se han capturado directamente en la VM del laboratorio.

### 5.1. Petición sin firma

```bash
curl -i http://echo.javiercd.es/hmac-auth
```

Kong responde `401 Unauthorized` y no contacta con el upstream:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:01:48 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: hmac
Content-Length: 81
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 1a794543e980ec54d493cd1edd88800c

{
  "message":"Unauthorized",
  "request_id":"1a794543e980ec54d493cd1edd88800c"
}
```

### 5.2. Crear una firma válida

El siguiente bloque debe ejecutarse desde el anfitrión. Construye la fecha, la cadena canónica y la firma con el mismo secreto que hemos declarado en Kubernetes:

```bash
HOST='echo.javiercd.es'
TARGET='/hmac-auth'
DATE="$(LC_ALL=C date -u '+%a, %d %b %Y %H:%M:%S GMT')"
SIGNING_STRING="date: ${DATE}\n@request-target: get ${TARGET}\nhost: ${HOST}"
SIGNATURE="$(echo -en "${SIGNING_STRING}" \
  | openssl dgst -sha256 -hmac 'hmac-shared-secret' -binary \
  | base64 -w0)"
```

Podemos revisar exactamente qué datos se van a firmar:

```bash
echo -e "${SIGNING_STRING}"
echo "${SIGNATURE}"
```

### 5.3. Enviar la petición firmada

```bash
curl -i \
  -H "Date: ${DATE}" \
  -H "Authorization: hmac username=\"hmac-client\", algorithm=\"hmac-sha256\", headers=\"date @request-target host\", signature=\"${SIGNATURE}\"" \
  "http://${HOST}${TARGET}"
```

Kong reconstruye la cadena, valida la firma e identifica al consumidor `hmac-client`. La respuesta real es:

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: 28
Connection: keep-alive
X-App-Name: http-echo
X-App-Version: 1.0.0
Date: Sun, 26 Jul 2026 09:01:48 GMT
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Upstream-Latency: 0
X-Kong-Proxy-Latency: 0
Via: 1.1 kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 0dc5cb6b1fb32f20969e215ce2c97015

Hola desde Kong Gateway KIC
```

### 5.4. Comprobar que la firma protege la ruta

Reutilizamos la misma firma, pero cambiamos el destino:

```bash
curl -i \
  -H "Date: ${DATE}" \
  -H "Authorization: hmac username=\"hmac-client\", algorithm=\"hmac-sha256\", headers=\"date @request-target host\", signature=\"${SIGNATURE}\"" \
  "http://${HOST}/hmac-auth/otra-ruta"
```

La firma deja de ser válida porque `@request-target` ya no coincide con el valor firmado. Kong explica el motivo sin contactar con el upstream:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:01:48 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: hmac
Content-Length: 98
X-Kong-Response-Latency: 1
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 9a78552fb81cd9672ef9e3668d00dc11

{
  "message":"HMAC signature does not match",
  "request_id":"9a78552fb81cd9672ef9e3668d00dc11"
}
```

La petición también será rechazada si se reutiliza después de superar el margen de reloj. Por eso los clientes deben generar una fecha y una firma nuevas para cada petición.

## Fuentes oficiales

- [HMAC Auth plugin](https://developer.konghq.com/plugins/hmac-auth/)
- [HMAC Auth configuration reference](https://developer.konghq.com/plugins/hmac-auth/reference/)
- [HMAC Auth changelog](https://developer.konghq.com/plugins/hmac-auth/changelog/)
- [Consumer entity](https://developer.konghq.com/gateway/entities/consumer/)
- [ACL plugin](https://developer.konghq.com/plugins/acl/)
