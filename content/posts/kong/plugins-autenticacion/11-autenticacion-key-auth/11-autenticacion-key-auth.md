---
title: "Key Auth en kong"
description: "Proteger un HTTPRoute de Kong con una API key y recursos Kubernetes nativos."
weight: 11
aliases:
  - /posts/kong/11-autenticacion-key-auth/11-autenticacion-key-auth/
---

Partimos del `Gateway` `kong` y del Service `echo` creados en [la instalación de KIC](/posts/kong/03-instalacion-kic/03-instalacion-kic/). La configuración se declara con `KongPlugin`, `Secret`, `KongConsumer` y `HTTPRoute`, tal como explica la [guía oficial de Key Authentication para KIC](https://developer.konghq.com/kubernetes-ingress-controller/get-started/key-authentication/).

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

## Preparar el laboratorio

Todos los artículos usan el dominio `echo.javiercd.es`. Este usa `/key-auth`:

```bash
sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
vagrant ssh
cd ~/kic-auth
sudo kubectl get gateway kong -n kong
sudo kubectl get svc echo -n javier
sudo kubectl apply -f 11-key-auth-plugin.yaml
sudo kubectl apply -f 11-key-auth-secret.yaml
sudo kubectl apply -f 11-key-auth-consumer.yaml
sudo kubectl apply -f 11-key-auth-httproute.yaml
```

El `Secret` tiene la etiqueta `konghq.com/credential: key-auth`, y el `KongConsumer` lo referencia. KIC crea la credencial en Kong y la anotación del `HTTPRoute` aplica el plugin únicamente a esta Route.

## Pruebas desde el anfitrión

La ausencia de la key debe producir `401`:

```bash
curl -i http://echo.javiercd.es/key-auth
```

La misma petición con la cabecera `apikey` debe producir `200`:

```bash
curl -i \
  -H 'apikey: my-super-secret-api-key' \
  http://echo.javiercd.es/key-auth
```

También puedes probar el parámetro de query si no desactivas esa opción en `config`. En producción suele ser preferible la cabecera y `hide_credentials: true` para que la API key no llegue al upstream.

## Cómo se relaciona Kubernetes con Kong

KIC observa estos recursos de Kubernetes y los traduce a configuración interna de Kong:

| Fichero | Recurso de Kubernetes | Traducción en Kong |
| --- | --- | --- |
| `11-key-auth-plugin.yaml` | `KongPlugin` | configuración del plugin |
| `11-key-auth-secret.yaml` | `Secret` | credencial de autenticación |
| `11-key-auth-consumer.yaml` | `KongConsumer` | Consumer de Kong |
| `11-key-auth-httproute.yaml` | `HTTPRoute` | Route de Kong y asociación con el backend |

El `Gateway` `kong` y el Service `echo` ya existían porque fueron creados en el post de instalación de KIC. Cada `HTTPRoute` reutiliza ese Gateway y ese Service compartidos.

## Ficheros del laboratorio, paso a paso

### 1. `11-key-auth-plugin.yaml`

Este fichero crea un `KongPlugin`. El campo `plugin` selecciona el plugin que ejecutará Kong y `config` contiene sus opciones. KIC traduce este recurso a una configuración de plugin. En una instalación con base de datos se refleja en la tabla `plugins`, incluida su configuración y sus asociaciones con Routes o Consumers.

Definición del recurso `KongPlugin`:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: key-auth
  namespace: javier
plugin: key-auth
config:
  key_names: [apikey]
  hide_credentials: true
```

### 2. `11-key-auth-secret.yaml`

Este `Secret` contiene la credencial que KIC debe convertir para el plugin correspondiente. La etiqueta `konghq.com/credential` identifica el tipo de credencial. KIC no lo utiliza como variable del backend. En una instalación con base de datos se refleja en la tabla de credenciales del plugin y queda relacionado con el Consumer.

Definición del recurso `Secret`:

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

### 3. `11-key-auth-consumer.yaml`

Este `KongConsumer` representa al usuario o aplicación que se autentica. La lista `credentials` referencia el Secret de credenciales. KIC crea el Consumer y relaciona la credencial con él. En una instalación con base de datos se refleja en `consumers` y en la relación con su credencial.

Definición del recurso `KongConsumer`:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: key-auth-client
  namespace: javier
  annotations:
    kubernetes.io/ingress.class: kong
username: key-client
credentials: [key-auth-credential]
```

### 4. `11-key-auth-httproute.yaml`

Esta `HTTPRoute` publica el endpoint. `parentRefs` la conecta al Gateway `kong`, `hostnames` limita el dominio y `PathPrefix` define la ruta. `backendRefs` apunta al Service `echo`, que ya existía en el escenario de KIC. KIC la traduce principalmente a una Route de Kong y a la asociación con el Service, que internamente se representa mediante Service, Upstream y Targets. La anotación `konghq.com/plugins` vincula el plugin a la Route.

Definición del recurso `HTTPRoute`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: key-auth
  namespace: javier
  annotations:
    konghq.com/plugins: key-auth
spec:
  parentRefs: [{name: kong, namespace: kong}]
  hostnames: [echo.javiercd.es]
  rules:
    - matches: [{path: {type: PathPrefix, value: /key-auth}}]
      backendRefs: [{name: echo, port: 80}]
```
