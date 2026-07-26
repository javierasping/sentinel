---
title: "OAuth 2.0 Introspection en kong"
description: "Validar access tokens opacos contra un IdP desde Kong KIC."
weight: 14
---

Este artículo usa `echo.javiercd.es/oauth2-introspection` y el plugin [OAuth 2.0 Introspection](https://developer.konghq.com/plugins/oauth2-introspection/). Es Enterprise y el IdP debe ser accesible desde los pods de Kong. No se consulta el Admin API: KIC entrega el `KongPlugin` desde Kubernetes.

```bash
sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
vagrant ssh
cd ~/kic-auth
sudo kubectl get gateway kong -n kong
sudo kubectl get svc echo -n javier
```

Edita `14-oauth2-introspection-plugin.yaml`: sustituye `authorization_value` por las credenciales Basic del cliente de tu IdP y comprueba que `introspection_url` sea accesible desde el namespace `kong`. La HTTPRoute está en `14-oauth2-introspection-httproute.yaml`.

Esta VM no tiene una licencia Enterprise, por lo que KIC rechazará el `KongPlugin` con el error `plugin ... is an enterprise only plugin`. Con una licencia válida, aplica los tres laboratorios Enterprise mediante `sudo ./apply-enterprise.sh`. El script valida primero los manifiestos para no dejar `HTTPRoute` huérfanas si falta la licencia.

```bash
sudo kubectl apply -f 14-oauth2-introspection-plugin.yaml
sudo kubectl apply -f 14-oauth2-introspection-httproute.yaml
exit
```

La petición de prueba necesita un token real emitido por ese IdP:

```bash
export ACCESS_TOKEN='pega-aqui-un-access-token-real'
curl -i \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  http://echo.javiercd.es/oauth2-introspection
```

Un token activo produce `200`. Uno revocado, caducado o desconocido produce `401`. Kong documenta que este plugin asume un servidor OAuth 2.0 externo y que puede asociar la respuesta a un Consumer.

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
| `14-oauth2-introspection-plugin.yaml` | `KongPlugin` | configuración del plugin |
| `14-oauth2-introspection-httproute.yaml` | `HTTPRoute` | Route de Kong y asociación con el backend |

El `Gateway` `kong` y el Service `echo` ya existían porque fueron creados en el post de instalación de KIC. Cada `HTTPRoute` reutiliza ese Gateway y ese Service compartidos.

## Ficheros del laboratorio, paso a paso

### 1. `14-oauth2-introspection-plugin.yaml`

Este fichero crea un `KongPlugin`. El campo `plugin` selecciona el plugin que ejecutará Kong y `config` contiene sus opciones. KIC traduce este recurso a una configuración de plugin. En una instalación con base de datos se refleja en la tabla `plugins`, incluida su configuración y sus asociaciones con Routes o Consumers.

Definición del recurso `KongPlugin`:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: oauth2-introspection
  namespace: javier
plugin: oauth2-introspection
config:
  introspection_url: http://keycloak.kong.javiercd.es:8080/realms/kong-lab/protocol/openid-connect/token/introspect
  authorization_value: Basic REPLACE_WITH_BASE64_CLIENT_CREDENTIALS
  token_type_hint: access_token
  ttl: 30
```

### 2. `14-oauth2-introspection-httproute.yaml`

Esta `HTTPRoute` publica el endpoint. `parentRefs` la conecta al Gateway `kong`, `hostnames` limita el dominio y `PathPrefix` define la ruta. `backendRefs` apunta al Service `echo`, que ya existía en el escenario de KIC. KIC la traduce principalmente a una Route de Kong y a la asociación con el Service, que internamente se representa mediante Service, Upstream y Targets. La anotación `konghq.com/plugins` vincula el plugin a la Route.

Definición del recurso `HTTPRoute`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: oauth2-introspection
  namespace: javier
  annotations: {konghq.com/plugins: oauth2-introspection}
spec:
  parentRefs: [{name: kong, namespace: kong}]
  hostnames: [echo.javiercd.es]
  rules:
    - matches: [{path: {type: PathPrefix, value: /oauth2-introspection}}]
      backendRefs: [{name: echo, port: 80}]
```
