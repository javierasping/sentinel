---
title: "HMAC Auth en kong"
description: "Firmar peticiones hacia Kong con HMAC Auth usando Gateway API y KIC."
weight: 12
---

Este ejemplo usa la misma base KIC del artículo de instalación y publica `echo.javiercd.es/hmac-auth`. HMAC Auth es un plugin open source y valida que el cliente conozca el secreto sin enviarlo en claro. Consulta la [referencia oficial de HMAC Auth](https://developer.konghq.com/plugins/hmac-auth/).

```bash
sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
vagrant ssh
cd ~/kic-auth
sudo kubectl get gateway kong -n kong
sudo kubectl get svc echo -n javier
sudo kubectl apply -f 12-hmac-auth-plugin.yaml
sudo kubectl apply -f 12-hmac-auth-secret.yaml
sudo kubectl apply -f 12-hmac-auth-consumer.yaml
sudo kubectl apply -f 12-hmac-auth-httproute.yaml
```

El `KongConsumer` recibe el `Secret` etiquetado como `hmac-auth` y el `HTTPRoute` lleva `konghq.com/plugins: hmac-auth`. El plugin exige que la firma cubra `date`, `@request-target` y `host`.

> [!NOTE]
> Estos posts se han creado a partir del escenario del post de instalación de KIC. Todos reutilizan el mismo `Gateway` `kong`, el `Service` `echo` y la IP que MetalLB asignó a `kong-gateway-proxy`: `192.168.121.200`.
>
> Como estamos trabajando en un laboratorio local, primero hay que preparar el dominio desde el anfitrión:
>
> ```bash
> sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
> echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
> ```
>
> Después entra en la VM y comprueba los recursos creados por el post de instalación de KIC:
>
> ```bash
> vagrant ssh
> cd ~/kic-auth
> sudo kubectl get gateway kong -n kong
> sudo kubectl get svc echo -n javier
> ```
>
>
> Si en tu clúster MetalLB ha asignado otra dirección, sustituye `192.168.121.200` en este aviso, en `/etc/hosts` y en las pruebas. Consulta también la sección [**Dominio y preparación**](http://localhost:1313/posts/kong/10-autenticacion-basic-auth/10-autenticacion-basic-auth/#dominio-y-preparaci%C3%B3n).

## Crear la firma y probar

El siguiente bloque se ejecuta en tu anfitrión. El secreto coincide con el del manifiesto:

```bash
HOST='echo.javiercd.es'
TARGET='/hmac-auth'
DATE="$(LC_ALL=C date -u '+%a, %d %b %Y %H:%M:%S GMT')"
SIGNING_STRING="date: ${DATE}\n@request-target: get ${TARGET}\nhost: ${HOST}"
SIGNATURE="$(printf '%b' "$SIGNING_STRING" | openssl dgst -sha256 -hmac 'hmac-shared-secret' -binary | base64 -w0)"

curl -i \
  -H "Host: ${HOST}" \
  -H "Date: ${DATE}" \
  -H "Authorization: hmac username=\"hmac-client\", algorithm=\"hmac-sha256\", headers=\"date @request-target host\", signature=\"${SIGNATURE}\"" \
  "http://${HOST}${TARGET}"
```

Una petición sin firma debe devolver `401`. En producción usa HTTPS y relojes sincronizados: una fecha fuera de tolerancia invalida la firma.

## Cómo se relaciona Kubernetes con Kong

KIC observa estos recursos de Kubernetes y los traduce a configuración interna de Kong:

| Fichero | Recurso de Kubernetes | Traducción en Kong |
| --- | --- | --- |
| `12-hmac-auth-plugin.yaml` | `KongPlugin` | configuración del plugin |
| `12-hmac-auth-secret.yaml` | `Secret` | credencial de autenticación |
| `12-hmac-auth-consumer.yaml` | `KongConsumer` | Consumer de Kong |
| `12-hmac-auth-httproute.yaml` | `HTTPRoute` | Route de Kong y asociación con el backend |

El `Gateway` `kong` y el Service `echo` ya existían porque fueron creados en el post de instalación de KIC. Cada `HTTPRoute` reutiliza ese Gateway y ese Service compartidos.

## Ficheros del laboratorio, paso a paso

### 1. `12-hmac-auth-plugin.yaml`

Este fichero crea un `KongPlugin`. El campo `plugin` selecciona el plugin que ejecutará Kong y `config` contiene sus opciones. KIC traduce este recurso a una configuración de plugin. En una instalación con base de datos se refleja en la tabla `plugins`, incluida su configuración y sus asociaciones con Routes o Consumers.

Definición del recurso `KongPlugin`:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: hmac-auth
  namespace: javier
plugin: hmac-auth
config:
  enforce_headers: [date, '@request-target', host]
  hide_credentials: true
```

### 2. `12-hmac-auth-secret.yaml`

Este `Secret` contiene la credencial que KIC debe convertir para el plugin correspondiente. La etiqueta `konghq.com/credential` identifica el tipo de credencial. KIC no lo utiliza como variable del backend. En una instalación con base de datos se refleja en la tabla de credenciales del plugin y queda relacionado con el Consumer.

Definición del recurso `Secret`:

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

### 3. `12-hmac-auth-consumer.yaml`

Este `KongConsumer` representa al usuario o aplicación que se autentica. La lista `credentials` referencia el Secret de credenciales. KIC crea el Consumer y relaciona la credencial con él. En una instalación con base de datos se refleja en `consumers` y en la relación con su credencial.

Definición del recurso `KongConsumer`:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: hmac-auth-client
  namespace: javier
  annotations: {kubernetes.io/ingress.class: kong}
username: hmac-client
credentials: [hmac-auth-credential]
```

### 4. `12-hmac-auth-httproute.yaml`

Esta `HTTPRoute` publica el endpoint. `parentRefs` la conecta al Gateway `kong`, `hostnames` limita el dominio y `PathPrefix` define la ruta. `backendRefs` apunta al Service `echo`, que ya existía en el escenario de KIC. KIC la traduce principalmente a una Route de Kong y a la asociación con el Service, que internamente se representa mediante Service, Upstream y Targets. La anotación `konghq.com/plugins` vincula el plugin a la Route.

Definición del recurso `HTTPRoute`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: hmac-auth
  namespace: javier
  annotations: {konghq.com/plugins: hmac-auth}
spec:
  parentRefs: [{name: kong, namespace: kong}]
  hostnames: [echo.javiercd.es]
  rules:
    - matches: [{path: {type: PathPrefix, value: /hmac-auth}}]
      backendRefs: [{name: echo, port: 80}]
```
