---
title: "OAuth 2.0 en kong"
description: "Limitación de topología del plugin OAuth 2.0 Authentication y alternativa correcta para KIC."
weight: 19
---

Este post queda como aclaración importante. El plugin [OAuth 2.0 Authentication](https://developer.konghq.com/plugins/oauth2/) no debe configurarse con el KIC del artículo de instalación: Kong documenta que requiere topología `traditional` porque genera, elimina y persiste tokens en la base de datos. No existe por tanto un `HTTPRoute` funcional que podamos aplicar honestamente a este laboratorio DB-less/KIC.

El dominio reservado para esta familia sería `echo.javiercd.es/oauth2`, pero el fichero [`19-oauth2-configmap.yaml`](https://github.com/javiercruces/sentinel/blob/main/examples/kong/kic-auth/19-oauth2-configmap.yaml) solo crea un `ConfigMap` explicativo y no intenta activar el plugin.

Para validar OAuth 2.0 desde KIC usa [OAuth 2.0 Introspection](/posts/kong/plugins-autenticacion/14-autenticacion-oauth2-introspection/14-autenticacion-oauth2-introspection/), que valida el token contra el IdP y sí está soportado en hybrid/db-less según la documentación oficial. Si necesitas emitir tokens con el plugin OAuth2, despliega Kong en `traditional`, con PostgreSQL, y sigue un laboratorio separado.

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

En este caso no hay `HTTPRoute` ni `KongPlugin` aplicable. El `ConfigMap` solo documenta la incompatibilidad y no crea una entidad de Kong.

## Crear el ConfigMap explicativo

Este es el único recurso de este post. No activa OAuth 2.0 Authentication ni crea una Route. Sirve para dejar la decisión documentada dentro del namespace del laboratorio:

```bash
vagrant ssh
cd ~/kic-auth
sudo kubectl apply -f 19-oauth2-configmap.yaml
sudo kubectl get configmap oauth2-kic-not-supported -n javier
exit
```

## Ficheros del laboratorio, paso a paso

### 1. `19-oauth2-configmap.yaml`

Este `ConfigMap` no crea autenticación en Kong. Documenta que el plugin OAuth2 Authentication no forma parte de este laboratorio KIC. No se traduce a una fila de `plugins`, `routes` ni `consumers`. Es solo una salvaguarda para evitar aplicar por error una configuración no compatible.

Definición del recurso `ConfigMap`:

```yaml
# OAuth2 Authentication is intentionally not a KIC lab. Kong documents it as
# traditional-only because it writes tokens to the database. This manifest is
# kept as a guardrail so it is not accidentally applied to the KIC Gateway.
apiVersion: v1
kind: ConfigMap
metadata:
  name: oauth2-kic-not-supported
  namespace: javier
data:
  reason: traditional-only
  route-host: echo.javiercd.es
  route-path: /oauth2
```
