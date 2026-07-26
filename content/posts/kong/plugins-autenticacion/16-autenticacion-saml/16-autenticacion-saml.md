---
title: "SAML en kong"
description: "Publicar un flujo SAML SP-initiated detrás de Kong KIC y Gateway API."
weight: 16
---

SAML es Enterprise y está orientado a aplicaciones de navegador. El plugin de Kong actúa como Service Provider y necesita un IdP real, su certificado y su URL SSO. La referencia oficial es [SAML](https://developer.konghq.com/plugins/saml/).

La Route será `http://echo.javiercd.es/saml` y comparte el dominio del post de instalación:

```bash
sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
vagrant ssh
cd ~/kic-auth
sudo kubectl get gateway kong -n kong
sudo kubectl get svc echo -n javier
```

Edita `16-saml-plugin.yaml` y sustituye `idp_certificate`, `idp_sso_url` e `issuer` por los datos de tu IdP. La HTTPRoute se define por separado en `16-saml-httproute.yaml`. Registra en el IdP el ACS `http://echo.javiercd.es/saml/callback`.

Esta VM no tiene licencia Enterprise. Sin ella, el webhook de KIC rechazará el `KongPlugin`. En una instalación licenciada, usa `sudo ./apply-enterprise.sh` después de configurar el IdP.

```bash
sudo kubectl apply -f 16-saml-plugin.yaml
sudo kubectl apply -f 16-saml-httproute.yaml
exit
curl -i -L http://echo.javiercd.es/saml
```

La última prueba requiere navegador porque el IdP devuelve un formulario SAML firmado. En cualquier entorno real usa HTTPS y un `session_secret` aleatorio de 32 caracteres.

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
| `16-saml-plugin.yaml` | `KongPlugin` | configuración del plugin |
| `16-saml-httproute.yaml` | `HTTPRoute` | Route de Kong y asociación con el backend |

El `Gateway` `kong` y el Service `echo` ya existían porque fueron creados en el post de instalación de KIC. Cada `HTTPRoute` reutiliza ese Gateway y ese Service compartidos.

## Ficheros del laboratorio, paso a paso

### 1. `16-saml-plugin.yaml`

Este fichero crea un `KongPlugin`. El campo `plugin` selecciona el plugin que ejecutará Kong y `config` contiene sus opciones. KIC traduce este recurso a una configuración de plugin. En una instalación con base de datos se refleja en la tabla `plugins`, incluida su configuración y sus asociaciones con Routes o Consumers.

Definición del recurso `KongPlugin`:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: saml
  namespace: javier
plugin: saml
config:
  idp_certificate: REPLACE_WITH_IDP_X509_CERTIFICATE
  idp_sso_url: https://idp.example.test/saml/sso
  issuer: https://echo.javiercd.es/saml
  assertion_consumer_path: /saml/callback
  session_secret: SAMLkicSessionSecret32bytesABC12
  session_storage: cookie
  validate_assertion_signature: true
```

### 2. `16-saml-httproute.yaml`

Esta `HTTPRoute` publica el endpoint. `parentRefs` la conecta al Gateway `kong`, `hostnames` limita el dominio y `PathPrefix` define la ruta. `backendRefs` apunta al Service `echo`, que ya existía en el escenario de KIC. KIC la traduce principalmente a una Route de Kong y a la asociación con el Service, que internamente se representa mediante Service, Upstream y Targets. La anotación `konghq.com/plugins` vincula el plugin a la Route.

Definición del recurso `HTTPRoute`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: saml
  namespace: javier
  annotations: {konghq.com/plugins: saml}
spec:
  parentRefs: [{name: kong, namespace: kong}]
  hostnames: [echo.javiercd.es]
  rules:
    - matches: [{path: {type: PathPrefix, value: /saml}}]
      backendRefs: [{name: echo, port: 80}]
```
