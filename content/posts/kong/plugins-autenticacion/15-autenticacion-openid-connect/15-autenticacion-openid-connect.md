---
title: "OpenID Connect en kong"
description: "Integrar Kong KIC con Keycloak mediante OpenID Connect y Gateway API."
weight: 15
---

OpenID Connect es Enterprise y convierte a Kong en relying party y resource server. Usaremos el mismo dominio `echo.javiercd.es`, con `/oidc`, y un Keycloak accesible desde Kong. La documentación oficial es [OpenID Connect](https://developer.konghq.com/plugins/openid-connect/) y el ejemplo de Keycloak está en `examples/kong/oidc-keycloak`.

```bash
sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
vagrant ssh
cd ~/kic-auth
sudo kubectl get gateway kong -n kong
sudo kubectl get svc echo -n javier
```

Antes de aplicar el manifiesto, registra en Keycloak el redirect exacto `http://echo.javiercd.es/oidc/callback` y asegúrate de que `keycloak.kong.javiercd.es` resuelve desde los pods de Kong.

Esta VM no tiene licencia Enterprise. Sin ella, el webhook de KIC rechazará el `KongPlugin`. En una instalación licenciada, usa `sudo ./apply-enterprise.sh` después de configurar el IdP.

```bash
sudo kubectl apply -f 15-openid-connect-plugin.yaml
sudo kubectl apply -f 15-openid-connect-httproute.yaml
exit
```

Abre el flujo desde el anfitrión:

```bash
curl -i -L http://echo.javiercd.es/oidc
```

Para completar login, consentimiento y MFA usa un navegador. En producción cambia a HTTPS, `session_cookie_secure: true` y un secreto generado aleatoriamente. Los valores del manifiesto son de laboratorio.

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
| `15-openid-connect-plugin.yaml` | `KongPlugin` | configuración del plugin |
| `15-openid-connect-httproute.yaml` | `HTTPRoute` | Route de Kong y asociación con el backend |

El `Gateway` `kong` y el Service `echo` ya existían porque fueron creados en el post de instalación de KIC. Cada `HTTPRoute` reutiliza ese Gateway y ese Service compartidos.

## Ficheros del laboratorio, paso a paso

### 1. `15-openid-connect-plugin.yaml`

Este fichero crea un `KongPlugin`. El campo `plugin` selecciona el plugin que ejecutará Kong y `config` contiene sus opciones. KIC traduce este recurso a una configuración de plugin. En una instalación con base de datos se refleja en la tabla `plugins`, incluida su configuración y sus asociaciones con Routes o Consumers.

Definición del recurso `KongPlugin`:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: openid-connect
  namespace: javier
plugin: openid-connect
config:
  issuer: http://keycloak.kong.javiercd.es:8080/realms/kong-lab
  client_id: [kong-gateway]
  client_secret: [kong-gateway-secret]
  client_auth: [client_secret_post]
  auth_methods: [authorization_code, session]
  redirect_uri: [http://echo.javiercd.es/oidc/callback]
  session_secret: OIDCkicSessionSecret32bytesABC12
  session_storage: cookie
  session_cookie_secure: false
  session_cookie_http_only: true
  session_cookie_same_site: Lax
```

### 2. `15-openid-connect-httproute.yaml`

Esta `HTTPRoute` publica el endpoint. `parentRefs` la conecta al Gateway `kong`, `hostnames` limita el dominio y `PathPrefix` define la ruta. `backendRefs` apunta al Service `echo`, que ya existía en el escenario de KIC. KIC la traduce principalmente a una Route de Kong y a la asociación con el Service, que internamente se representa mediante Service, Upstream y Targets. La anotación `konghq.com/plugins` vincula el plugin a la Route.

Definición del recurso `HTTPRoute`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: openid-connect
  namespace: javier
  annotations: {konghq.com/plugins: openid-connect}
spec:
  parentRefs: [{name: kong, namespace: kong}]
  hostnames: [echo.javiercd.es]
  rules:
    - matches: [{path: {type: PathPrefix, value: /oidc}}]
      backendRefs: [{name: echo, port: 80}]
```
