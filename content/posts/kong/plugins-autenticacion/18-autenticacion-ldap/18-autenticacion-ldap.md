---
title: "LDAP Auth en Kong"
date: 2026-07-26T00:00:00+02:00
description: "Cómo validar un usuario y una contraseña contra un directorio LDAP desde un HTTPRoute administrado por Kong Gateway y KIC."
tags: [Kong, Autenticación, LDAP, Servicios de directorio, KIC]
weight: 18
hero: images/kong/ldap-auth.png
---

LDAP Authentication permite que Kong valide directamente un usuario y una contraseña contra un directorio corporativo. El backend no recibe esas credenciales ni necesita implementar el protocolo LDAP.

En este artículo veremos cómo se construye la cabecera de autenticación, cómo localiza Kong al usuario dentro del directorio y cómo proteger una ruta `/ldap-auth` mediante Kong Ingress Controller.

> [!NOTE]
> Este laboratorio continúa desde el escenario creado en [Instalación de KIC](/posts/kong/03-instalacion-kic/03-instalacion-kic/). Reutiliza el `Gateway` `kong`, el servicio `echo` y la dirección `192.168.121.200` asignada por MetalLB a `kong-gateway-proxy`.
>
> Las pruebas utilizan Kong Gateway `3.10.0.16`, KIC `3.5` y el servidor LDAP público de Forum Systems. Este servicio externo puede no estar disponible y utiliza LDAP sin TLS, por lo que solo debe emplearse como demostración.

## 1. ¿Qué es LDAP Authentication?

LDAP, de *Lightweight Directory Access Protocol*, permite consultar y autenticar identidades almacenadas en un servicio de directorio.

Cada entrada se identifica mediante un Distinguished Name o DN. En el directorio del laboratorio, el usuario `riemann` se encuentra bajo:

```text
uid=riemann,dc=example,dc=com
```

La configuración del plugin indica a Kong cómo construir esa búsqueda:

- `base_dn: dc=example,dc=com` establece el punto de partida.
- `attribute: uid` indica qué atributo contiene el nombre de usuario.
- `ldap_host` y `ldap_port` identifican al servidor.

El cliente construye una cadena con el usuario y la contraseña:

```text
riemann:password
```

Después la codifica en Base64 y la envía con el esquema configurado:

```http
Authorization: ldap cmllbWFubjpwYXNzd29yZA==
```

LDAP Auth no utiliza automáticamente la sintaxis Basic de `curl -u`. Aunque el contenido codificado también tenga la forma `usuario:contraseña`, el esquema de este laboratorio es `ldap`, no `Basic`.

Base64 no cifra las credenciales. En un entorno real, el cliente debe comunicarse con Kong mediante HTTPS y Kong debe conectarse al directorio mediante LDAPS o StartTLS.

## 2. ¿Cómo funciona LDAP Auth en Kong Gateway?

Kong implementa este mecanismo mediante el plugin oficial [`ldap-auth`](https://developer.konghq.com/plugins/ldap-auth/). Está disponible para las topologías traditional, hybrid y DB-less.

En este laboratorio lo aplicaremos únicamente a la `Route` `/ldap-auth`.

Cuando una petición coincide con la ruta, Kong realiza este proceso:

1. Busca credenciales primero en `Proxy-Authorization` y después en `Authorization`.
2. Comprueba que la cabecera utilice el esquema configurado en `header_type`.
3. Decodifica el usuario y la contraseña.
4. Construye el DN utilizando `attribute` y `base_dn`.
5. Intenta autenticar ese usuario contra el servidor LDAP.
6. Almacena temporalmente el resultado en caché.
7. Si la autenticación es válida, elimina la credencial y permite llegar al upstream.

El siguiente diagrama muestra que la contraseña no se valida contra una credencial local de Kong. El plugin construye el DN y realiza un bind contra el directorio LDAP. Solo un bind válido permite que la petición continúe.

![Flujo de LDAP Auth en Kong Gateway](/kong/plugins-autenticacion/18-autenticacion-ldap/img/ldap-auth-flow.svg)

El comportamiento es el siguiente:

- Si falta la cabecera, Kong responde `401 Unauthorized`.
- Si el usuario no existe o la contraseña no coincide, Kong responde `401 Unauthorized`.
- Si el directorio no es accesible, Kong no puede completar la autenticación.
- Si las credenciales son válidas, la petición continúa hasta el upstream.
- Cuando Kong rechaza la autenticación, el servicio `echo` no recibe la petición.

El plugin utiliza una caché cuyo TTL predeterminado es de 60 segundos. Esto reduce la carga del directorio, pero puede retrasar durante ese periodo el efecto de algunos cambios en las credenciales.

## 3. Identidad LDAP y Consumers de Kong

En este laboratorio la identidad reside en el directorio LDAP. No crearemos un `Secret` con la contraseña ni un `KongConsumer` por cada usuario.

La relación mínima es:

```text
Cliente
    |
    +-- usuario y contraseña
            |
            v
          Kong
            |
            +-- bind LDAP
                    |
                    v
              Directorio LDAP
```

Esto diferencia LDAP Auth de Basic Auth, Key Auth o JWT, donde las credenciales del laboratorio se declaran como recursos de Kubernetes y se asocian a Consumers locales.

Si necesitamos funcionalidades más avanzadas de identidad, autorización por grupos o mapeos específicos, debemos valorar LDAP Authentication Advanced u otra integración de identidad.

## 4. Configuración de LDAP Auth con KIC

Vamos a proteger `/ldap-auth` sobre el servicio `echo`. Solo necesitamos un `KongPlugin` y un `HTTPRoute`.

### 4.1. Relación entre los recursos de Kubernetes y Kong

| Recurso de Kubernetes | Recurso interno de Kong |
| --- | --- |
| `KongPlugin` | `plugins` |
| `HTTPRoute` | `routes`, `services`, `upstreams` y `targets` |

El directorio LDAP permanece externo a Kubernetes y debe ser accesible desde los pods de Kong.

### 4.2. Crear el plugin ldap-auth

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: ldap-auth
  namespace: javier
plugin: ldap-auth
config:
  ldap_host: ldap.forumsys.com
  ldap_port: 389
  start_tls: false
  ldaps: false
  base_dn: dc=example,dc=com
  attribute: uid
  header_type: ldap
  hide_credentials: true
  verify_ldap_host: false
```

Esta configuración permite reproducir el ejemplo público, pero no es segura para producción:

- `ldap_port: 389` utiliza el puerto LDAP convencional.
- `start_tls: false` y `ldaps: false` dejan la conexión sin cifrar.
- `verify_ldap_host: false` no valida la identidad del servidor.

En producción debemos elegir una de estas alternativas:

- LDAPS mediante `ldaps: true`, puerto `636` y `start_tls: false`.
- StartTLS mediante `start_tls: true`, puerto `389` y `ldaps: false`.

En ambos casos debemos utilizar `verify_ldap_host: true` y configurar en Kong la CA que firma el certificado del directorio.

### 4.3. Crear el `HTTPRoute`

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: ldap-auth
  namespace: javier
  annotations:
    konghq.com/plugins: ldap-auth
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
            value: /ldap-auth
      backendRefs:
        - name: echo
          port: 80
```

### 4.4. Aplicar los manifiestos

```bash
sudo kubectl apply -f 18-ldap-plugin.yaml
sudo kubectl apply -f 18-ldap-httproute.yaml
```

Comprobamos su estado:

```bash
sudo kubectl get kongplugin ldap-auth -n javier
sudo kubectl get httproute ldap-auth -n javier
sudo kubectl describe httproute ldap-auth -n javier
```

## 5. Probando LDAP Authentication

Las respuestas de esta sección se han capturado directamente contra el directorio público configurado en el manifiesto.

### 5.1. Petición sin credenciales

```bash
curl -i http://echo.javiercd.es/ldap-auth
```

Kong responde antes de contactar con el upstream:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:02:10 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: LDAP
Content-Length: 81
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 3769cd619434626c22b565380a256e2d

{
  "message":"Unauthorized",
  "request_id":"3769cd619434626c22b565380a256e2d"
}
```

### 5.2. Credenciales incorrectas

Codificamos una contraseña que no existe:

```bash
LDAP_AUTH="$(echo -n 'riemann:incorrecta' | base64 -w0)"

curl -i \
  -H "Authorization: ldap ${LDAP_AUTH}" \
  http://echo.javiercd.es/ldap-auth
```

El bind LDAP falla y Kong responde:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:02:10 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: LDAP
Content-Length: 81
X-Kong-Response-Latency: 237
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: f33c617286ceea737759642809623960

{
  "message":"Unauthorized",
  "request_id":"f33c617286ceea737759642809623960"
}
```

### 5.3. Credenciales correctas

Las cuentas públicas de Forum Systems utilizan la contraseña `password`:

```bash
LDAP_AUTH="$(echo -n 'riemann:password' | base64 -w0)"

curl -i \
  -H "Authorization: ldap ${LDAP_AUTH}" \
  http://echo.javiercd.es/ldap-auth
```

Si el servidor público está disponible, Kong valida el usuario y permite alcanzar el upstream:

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: 28
Connection: keep-alive
X-App-Name: http-echo
X-App-Version: 1.0.0
Date: Sun, 26 Jul 2026 09:02:10 GMT
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Upstream-Latency: 1
X-Kong-Proxy-Latency: 119
Via: 1.1 kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 18e15316718e36359b76c9698390f16f

Hola desde Kong Gateway KIC
```

### 5.4. Diagnosticar la conexión LDAP

Si las credenciales son correctas pero la petición falla, revisamos los logs:

```bash
sudo kubectl logs -n kong deployment/kong-gateway --tail=100
```

Los fallos habituales son:

- El host LDAP no resuelve desde el pod.
- El puerto está bloqueado.
- `base_dn` o `attribute` no corresponden al directorio.
- Se han habilitado simultáneamente LDAPS y StartTLS.
- El certificado no puede validarse con las CA configuradas en Kong.

Estos errores ocurren entre Kong y LDAP. No aparecerán en el servicio `echo`.

## Fuentes oficiales

- [LDAP Authentication plugin](https://developer.konghq.com/plugins/ldap-auth/)
- [LDAP Authentication configuration reference](https://developer.konghq.com/plugins/ldap-auth/reference/)
- [LDAP Authentication changelog](https://developer.konghq.com/plugins/ldap-auth/changelog/)
- [LDAP Authentication Advanced](https://developer.konghq.com/plugins/ldap-auth-advanced/)
- [Forum Systems LDAP test server](https://www.forumsys.com/category/tutorials/integration-how-to/)
