---
title: "Session en kong"
description: "Crear una sesión de navegador en Kong usando Session y Key Auth sobre Gateway API."
weight: 17
---

Session no sustituye a un mecanismo de autenticación inicial. En este laboratorio se combina con Key Auth: la primera petición lleva la API key, Kong crea una cookie y las siguientes reutilizan la sesión. Se publica en `echo.javiercd.es/session`.

```bash
sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
vagrant ssh
cd ~/kic-auth
sudo kubectl get gateway kong -n kong
sudo kubectl get svc echo -n javier
sudo kubectl apply -f 17-session-session-plugin.yaml
sudo kubectl apply -f 17-session-key-auth-plugin.yaml
sudo kubectl apply -f 17-session-secret.yaml
sudo kubectl apply -f 17-session-consumer.yaml
sudo kubectl apply -f 17-session-anonymous-plugin.yaml
sudo kubectl apply -f 17-session-anonymous-consumer.yaml
sudo kubectl apply -f 17-session-httproute.yaml
```

El `HTTPRoute` aplica `session` y `session-key-auth`. El plugin de Key Auth usa el Consumer anónimo `anonymous-session`, que tiene asociado `request-termination` para devolver `403` cuando no existe ni sesión ni API key. `cookie_secure: false` solo permite probar contra HTTP local. En producción debe ser `true` y debe usarse HTTPS.

```bash
rm -f cookies.txt
curl -i -c cookies.txt \
  -H 'apikey: session-api-key' \
  http://echo.javiercd.es/session

curl -i -b cookies.txt \
  http://echo.javiercd.es/session
```

La primera respuesta debe incluir `Set-Cookie` y la segunda no necesita la API key porque reutiliza la cookie. Sin ninguna credencial, la respuesta correcta es `403`.

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

## Cómo se relaciona Kubernetes con Kong

KIC observa estos recursos de Kubernetes y los traduce a configuración interna de Kong:

| Fichero | Recurso de Kubernetes | Traducción en Kong |
| --- | --- | --- |
| `17-session-session-plugin.yaml` | `KongPlugin` | configuración del plugin Session |
| `17-session-key-auth-plugin.yaml` | `KongPlugin` | configuración del plugin Key Auth |
| `17-session-secret.yaml` | `Secret` | credencial de autenticación |
| `17-session-consumer.yaml` | `KongConsumer` | Consumer de Kong |
| `17-session-anonymous-plugin.yaml` | `KongPlugin` | configuración del plugin request-termination |
| `17-session-anonymous-consumer.yaml` | `KongConsumer` | Consumer anónimo de Kong |
| `17-session-httproute.yaml` | `HTTPRoute` | Route de Kong y asociación con el backend |

El `Gateway` `kong` y el Service `echo` ya existían porque fueron creados en el post de instalación de KIC. Cada `HTTPRoute` reutiliza ese Gateway y ese Service compartidos.

## Ficheros del laboratorio, paso a paso

### 1. `17-session-session-plugin.yaml`

Este fichero crea el `KongPlugin` de Session. Configura el almacenamiento de la sesión en una cookie y sus opciones de seguridad para este laboratorio HTTP. KIC lo traduce a una entrada de plugin en Kong. En una instalación con base de datos se refleja en `plugins`.

Definición del recurso `KongPlugin`:

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

### 2. `17-session-key-auth-plugin.yaml`

Este fichero crea un `KongPlugin` de Key Auth para que Session pueda aceptar la API key inicial. `anonymous` indica el Consumer que se usará cuando la petición no tenga credenciales. KIC lo traduce a una entrada de plugin en Kong. En una instalación con base de datos se refleja en `plugins`.

Definición del recurso `KongPlugin`:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: session-key-auth
  namespace: javier
plugin: key-auth
config:
  key_names: [apikey]
  anonymous: anonymous-session
```

### 3. `17-session-secret.yaml`

Este `Secret` contiene la credencial que KIC debe convertir para el plugin correspondiente. La etiqueta `konghq.com/credential` identifica el tipo de credencial. KIC no lo utiliza como variable del backend. En una instalación con base de datos se refleja en la tabla de credenciales del plugin y queda relacionado con el Consumer.

Definición del recurso `Secret`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: session-key-credential
  namespace: javier
  labels: {konghq.com/credential: key-auth}
stringData: {key: session-api-key}
```

### 4. `17-session-consumer.yaml`

Este `KongConsumer` representa al usuario o aplicación que se autentica. La lista `credentials` referencia el Secret de credenciales. KIC crea el Consumer y relaciona la credencial con él. En una instalación con base de datos se refleja en `consumers` y en la relación con su credencial.

Definición del recurso `KongConsumer`:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: session-client
  namespace: javier
  annotations: {kubernetes.io/ingress.class: kong}
username: session-client
credentials: [session-key-credential]
```

### 5. `17-session-anonymous-plugin.yaml`

Este `KongPlugin` usa `request-termination` para responder `403 Forbidden`. Se aplica al Consumer anónimo y actúa como la rama de rechazo de este laboratorio. En una instalación con base de datos se refleja en `plugins`.

Definición del recurso `KongPlugin`:

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

### 6. `17-session-anonymous-consumer.yaml`

Este `KongConsumer` representa las peticiones anónimas. Su anotación aplica el plugin `request-termination`, de modo que una petición sin credenciales recibe `403` en lugar de alcanzar el backend. En una instalación con base de datos se refleja en `consumers` y en la asociación del plugin.

Definición del recurso `KongConsumer`:

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

### 7. `17-session-httproute.yaml`

Esta `HTTPRoute` publica el endpoint. `parentRefs` la conecta al Gateway `kong`, `hostnames` limita el dominio y `PathPrefix` define la ruta. `backendRefs` apunta al Service `echo`, que ya existía en el escenario de KIC. KIC la traduce principalmente a una Route de Kong y a la asociación con el Service, que internamente se representa mediante Service, Upstream y Targets. La anotación `konghq.com/plugins` vincula el plugin a la Route.

Definición del recurso `HTTPRoute`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: session
  namespace: javier
  annotations:
    konghq.com/plugins: "session,session-key-auth"
spec:
  parentRefs: [{name: kong, namespace: kong}]
  hostnames: [echo.javiercd.es]
  rules:
    - matches: [{path: {type: PathPrefix, value: /session}}]
      backendRefs: [{name: echo, port: 80}]
```
