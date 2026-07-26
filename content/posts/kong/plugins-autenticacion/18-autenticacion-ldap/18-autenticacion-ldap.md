---
title: "LDAP Auth en kong"
description: "Validar usuario y contraseña contra LDAP desde una HTTPRoute administrada por KIC."
weight: 18
---

Este laboratorio usa el plugin open source [LDAP Authentication](https://developer.konghq.com/plugins/ldap-auth/) y publica `echo.javiercd.es/ldap-auth`. El endpoint LDAP debe ser alcanzable desde los pods de Kong. El manifiesto usa el servidor público de pruebas de Forumsys como ejemplo, pero debes sustituirlo por tu directorio.

```bash
sudo sed -i '/[[:space:]]echo\.javiercd\.es$/d' /etc/hosts
echo '192.168.121.200 echo.javiercd.es' | sudo tee -a /etc/hosts
vagrant ssh
cd ~/kic-auth
sudo kubectl get gateway kong -n kong
sudo kubectl get svc echo -n javier
```

Edita `18-ldap-plugin.yaml` con `ldap_host`, `base_dn`, `attribute` y TLS. La HTTPRoute se define por separado en `18-ldap-httproute.yaml`. `verify_ldap_host: false` solo evita exigir un certificado válido en el laboratorio. En producción debe ser `true`, con la CA instalada en Kong.

```bash
sudo kubectl apply -f 18-ldap-plugin.yaml
sudo kubectl apply -f 18-ldap-httproute.yaml
exit
```

LDAP Auth no usa la sintaxis Basic de `curl -u`. El formato que espera es `Authorization: ldap <base64(usuario:contraseña)>`.

Con el servidor público de laboratorio incluido en el manifiesto, la cuenta `riemann` funciona así:

```bash
LDAP_AUTH="$(printf '%s' 'riemann:password' | base64 -w0)"
curl -i -H "Authorization: ldap ${LDAP_AUTH}" \
  http://echo.javiercd.es/ldap-auth
```

Para tu directorio sustituye la cuenta y conserva el mismo formato. El plugin valida primero `Proxy-Authorization` y después `Authorization`. Un fallo de conexión, DN base o TLS se observa en los logs del gateway, no en el echo server.

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
| `18-ldap-plugin.yaml` | `KongPlugin` | configuración del plugin |
| `18-ldap-httproute.yaml` | `HTTPRoute` | Route de Kong y asociación con el backend |

El `Gateway` `kong` y el Service `echo` ya existían porque fueron creados en el post de instalación de KIC. Cada `HTTPRoute` reutiliza ese Gateway y ese Service compartidos.

## Ficheros del laboratorio, paso a paso

### 1. `18-ldap-plugin.yaml`

Este fichero crea un `KongPlugin`. El campo `plugin` selecciona el plugin que ejecutará Kong y `config` contiene sus opciones. KIC traduce este recurso a una configuración de plugin. En una instalación con base de datos se refleja en la tabla `plugins`, incluida su configuración y sus asociaciones con Routes o Consumers.

Definición del recurso `KongPlugin`:

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
  verify_ldap_host: false
```

### 2. `18-ldap-httproute.yaml`

Esta `HTTPRoute` publica el endpoint. `parentRefs` la conecta al Gateway `kong`, `hostnames` limita el dominio y `PathPrefix` define la ruta. `backendRefs` apunta al Service `echo`, que ya existía en el escenario de KIC. KIC la traduce principalmente a una Route de Kong y a la asociación con el Service, que internamente se representa mediante Service, Upstream y Targets. La anotación `konghq.com/plugins` vincula el plugin a la Route.

Definición del recurso `HTTPRoute`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: ldap-auth
  namespace: javier
  annotations: {konghq.com/plugins: ldap-auth}
spec:
  parentRefs: [{name: kong, namespace: kong}]
  hostnames: [echo.javiercd.es]
  rules:
    - matches: [{path: {type: PathPrefix, value: /ldap-auth}}]
      backendRefs: [{name: echo, port: 80}]
```
