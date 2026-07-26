---
title: "JWT Auth en kong"
description: "Validar JWT firmados con HS256 en una HTTPRoute administrada por KIC."
weight: 13
---

JWT Auth valida un token firmado antes de enviar la petición al backend. Este laboratorio usa la misma instalación KIC, el dominio `echo.javiercd.es` y el path `/jwt`. La referencia es [JWT Plugin](https://developer.konghq.com/plugins/jwt/).

```bash
sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
vagrant ssh
cd ~/kic-auth
sudo kubectl get gateway kong -n kong
sudo kubectl get svc echo -n javier
sudo kubectl apply -f 13-jwt-plugin.yaml
sudo kubectl apply -f 13-jwt-secret.yaml
sudo kubectl apply -f 13-jwt-consumer.yaml
sudo kubectl apply -f 13-jwt-httproute.yaml
```

El manifiesto crea la credencial JWT del Consumer `jwt-client` y aplica `jwt` al `HTTPRoute`. El ejemplo usa HS256 y el secreto `jwt-shared-secret` únicamente para que la prueba sea reproducible.

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

## Generar un token y probarlo

Requiere `openssl` y `jq` en el anfitrión:

```bash
NOW="$(date +%s)"
HEADER='{"typ":"JWT","alg":"HS256"}'
PAYLOAD="{\"iss\":\"jwt-client\",\"iat\":${NOW},\"exp\":$((NOW+300))}"
b64() {
  printf '%s' "$1" | openssl base64 -A | tr '+/' '-_' | tr -d '='
}
UNSIGNED="$(b64 "$HEADER").$(b64 "$PAYLOAD")"
SIG="$(printf '%s' "$UNSIGNED" | openssl dgst -sha256 -hmac 'jwt-shared-secret' -binary | openssl base64 -A | tr '+/' '-_' | tr -d '=')"
TOKEN="${UNSIGNED}.${SIG}"

curl -i \
  -H "Authorization: Bearer ${TOKEN}" \
  http://echo.javiercd.es/jwt
```

Sin token o con una firma incorrecta la respuesta es `401`. No uses HS256 compartido entre muchos servicios en producción. Una clave asimétrica y una rotación controlada suelen ser mejores.

## Cómo se relaciona Kubernetes con Kong

KIC observa estos recursos de Kubernetes y los traduce a configuración interna de Kong:

| Fichero | Recurso de Kubernetes | Traducción en Kong |
| --- | --- | --- |
| `13-jwt-plugin.yaml` | `KongPlugin` | configuración del plugin |
| `13-jwt-secret.yaml` | `Secret` | credencial de autenticación |
| `13-jwt-consumer.yaml` | `KongConsumer` | Consumer de Kong |
| `13-jwt-httproute.yaml` | `HTTPRoute` | Route de Kong y asociación con el backend |

El `Gateway` `kong` y el Service `echo` ya existían porque fueron creados en el post de instalación de KIC. Cada `HTTPRoute` reutiliza ese Gateway y ese Service compartidos.

## Ficheros del laboratorio, paso a paso

### 1. `13-jwt-plugin.yaml`

Este fichero crea un `KongPlugin`. El campo `plugin` selecciona el plugin que ejecutará Kong y `config` contiene sus opciones. KIC traduce este recurso a una configuración de plugin. En una instalación con base de datos se refleja en la tabla `plugins`, incluida su configuración y sus asociaciones con Routes o Consumers.

Definición del recurso `KongPlugin`:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: jwt
  namespace: javier
plugin: jwt
config:
  claims_to_verify: [exp]
```

### 2. `13-jwt-secret.yaml`

Este `Secret` contiene la credencial que KIC debe convertir para el plugin correspondiente. La etiqueta `konghq.com/credential` identifica el tipo de credencial. KIC no lo utiliza como variable del backend. En una instalación con base de datos se refleja en la tabla de credenciales del plugin y queda relacionado con el Consumer.

Definición del recurso `Secret`:

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

### 3. `13-jwt-consumer.yaml`

Este `KongConsumer` representa al usuario o aplicación que se autentica. La lista `credentials` referencia el Secret de credenciales. KIC crea el Consumer y relaciona la credencial con él. En una instalación con base de datos se refleja en `consumers` y en la relación con su credencial.

Definición del recurso `KongConsumer`:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: jwt-client
  namespace: javier
  annotations: {kubernetes.io/ingress.class: kong}
username: jwt-client
credentials: [jwt-credential]
```

### 4. `13-jwt-httproute.yaml`

Esta `HTTPRoute` publica el endpoint. `parentRefs` la conecta al Gateway `kong`, `hostnames` limita el dominio y `PathPrefix` define la ruta. `backendRefs` apunta al Service `echo`, que ya existía en el escenario de KIC. KIC la traduce principalmente a una Route de Kong y a la asociación con el Service, que internamente se representa mediante Service, Upstream y Targets. La anotación `konghq.com/plugins` vincula el plugin a la Route.

Definición del recurso `HTTPRoute`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: jwt
  namespace: javier
  annotations: {konghq.com/plugins: jwt}
spec:
  parentRefs: [{name: kong, namespace: kong}]
  hostnames: [echo.javiercd.es]
  rules:
    - matches: [{path: {type: PathPrefix, value: /jwt}}]
      backendRefs: [{name: echo, port: 80}]
```
