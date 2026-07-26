---
title: "Instalación de Kong Ingress Controller (KIC)"
date: 2026-07-26T00:00:00+02:00
description: "Guía paso a paso para instalar Kong Gateway y Kong Ingress Controller en Kubernetes, validar el despliegue y exponer el proxy con MetalLB."
tags: [Kong, Testing, Validación, API Gateway]
hero: images/kong/kic.png
weight: 3
---

En este artículo vamos a pasar de la teoría al despliegue real. El objetivo es instalar **Kong Ingress Controller (KIC)** en un clúster de Kubernetes, comprobar que **Kong Gateway** está funcionando correctamente y preparar la exposición externa del proxy para poder publicar aplicaciones desde el propio clúster.

Para mantener el laboratorio simple, usaré una única máquina virtual creada con **Vagrant** sobre la que ejecutaré un clúster **k3s**. Esta elección no cambia el funcionamiento de Kong, pero nos permite centrarnos en lo importante: qué instala KIC, por qué el servicio de proxy aparece inicialmente en estado `Pending` y cómo resolverlo con **MetalLB**.

También conviene dejar claro desde el principio que **KIC no es un gateway independiente**. Su trabajo es observar los recursos de Kubernetes, traducirlos a configuración de Kong y mantener esa configuración sincronizada. Dicho de otra forma: Kubernetes define el estado deseado y KIC lo convierte en una configuración real para Kong Gateway.

## Instalación de Kong Ingress Controller

Una vez que nuestro clúster de Kubernetes está funcionando, el siguiente paso es instalar **Kong Ingress Controller (KIC)** junto con **Kong Gateway**.

Kong ofrece un repositorio oficial de Helm desde el que podemos desplegar ambos componentes con un único chart. En este laboratorio fijaremos la versión de **Kong Gateway 3.10 open source** para trabajar con una versión conocida y reproducible.

### Añadir el repositorio de Helm

Lo primero será registrar el repositorio oficial de Kong y actualizar el índice de charts disponibles.

```bash
helm repo add kong https://charts.konghq.com
helm repo update
```

Si queremos revisar qué versiones del chart tenemos disponibles, podemos consultarlas con:

```bash
helm search repo kong/ingress --versions
```

### Instalar Kong Ingress Controller

Ahora instalaremos el chart oficial de Kong. Con este comando se desplegarán el controlador, el gateway y todos los recursos auxiliares que necesitan para funcionar dentro del clúster.

```bash
helm install kong kong/ingress \
  --namespace kong \
  --create-namespace \
  --set gateway.image.repository=kong/kong-gateway \
  --set gateway.image.tag=3.10
```

Con esta instalación estamos haciendo varias cosas al mismo tiempo:

- Creamos el *namespace* `kong` si todavía no existe.
- Desplegamos **Kong Gateway 3.10 open source**.
- Desplegamos **Kong Ingress Controller**.
- Creamos los *Deployments*, *Services*, *ConfigMaps*, *Roles* y demás recursos necesarios.
- Registramos los **CRDs** que Kong utiliza para integrarse con Kubernetes.

Una vez finalizada la instalación, podemos comprobar que los pods están en ejecución:

```bash
sudo kubectl get pods -n kong
```

```text
NAME                               READY   STATUS    RESTARTS   AGE
kong-controller-79b8f95d99-dtndr   1/1     Running   0          5m53s
kong-gateway-db57d88fc-h72wz       1/1     Running   0          5m53s
```

También es buena idea inspeccionar qué recursos ha creado Helm en el *namespace* `kong`:

```bash
sudo kubectl get all -n kong
```

Si todo está correcto, veremos los pods del controlador y del gateway, los servicios asociados y sus correspondientes *Deployments*.

### Verificar los CRDs

Como Kong se integra con Kubernetes mediante recursos personalizados, también conviene comprobar que los **CRDs** se han instalado correctamente:

```bash
sudo kubectl get crd | grep konghq
```

```text
ingressclassparameterses.configuration.konghq.com   2026-07-12T22:15:26Z
kongclusterplugins.configuration.konghq.com         2026-07-12T22:15:26Z
kongconsumergroups.configuration.konghq.com         2026-07-12T22:15:26Z
kongconsumers.configuration.konghq.com              2026-07-12T22:15:26Z
kongcustomentities.configuration.konghq.com         2026-07-12T22:15:26Z
kongingresses.configuration.konghq.com              2026-07-12T22:15:26Z
konglicenses.configuration.konghq.com               2026-07-12T22:15:26Z
kongplugins.configuration.konghq.com                2026-07-12T22:15:26Z
kongupstreampolicies.configuration.konghq.com       2026-07-12T22:15:26Z
kongvaults.configuration.konghq.com                 2026-07-12T22:15:26Z
tcpingresses.configuration.konghq.com               2026-07-12T22:15:26Z
udpingresses.configuration.konghq.com               2026-07-12T22:15:26Z
```

Si los pods están en estado **Running** y los CRDs aparecen en la lista, ya tendremos **Kong Gateway** y **Kong Ingress Controller** instalados y listos para empezar a publicar tráfico.

## Instalación de MetalLB

Al revisar el servicio que expone el proxy de Kong veremos que su dirección **EXTERNAL-IP** aparece como `<pending>`.

```bash
sudo kubectl get svc -n kong
```

```text
NAME                 TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)
kong-gateway-proxy   LoadBalancer   10.43.17.15     <pending>     80:32263/TCP,443:32183/TCP
```

Esto no significa que la instalación haya fallado. Lo que ocurre es que nuestro clúster no dispone de un proveedor de *LoadBalancer* que pueda asignar una IP externa al servicio.

En plataformas gestionadas como **Amazon EKS**, **Google GKE** o **Azure AKS** esa asignación la realiza el propio proveedor cloud. Sin embargo, en un laboratorio basado en **k3s** o en un entorno *on-premise* necesitamos una solución adicional.

Para cubrir esa función utilizaremos **MetalLB**, que actúa como balanceador de carga para clústeres Kubernetes y permite asignar direcciones IP a los servicios de tipo `LoadBalancer`.

### Instalar MetalLB

Comenzaremos aplicando los manifiestos oficiales de MetalLB:

```bash
sudo kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.15.2/config/manifests/metallb-native.yaml
```

Cuando termine la instalación, comprobaremos que sus componentes principales están activos:

```bash
sudo kubectl get pods -n metallb-system
```

```text
NAME                          READY   STATUS    RESTARTS   AGE
controller-6dd55858b4-v9rmh   1/1     Running   0          98s
speaker-4tfcv                 1/1     Running   0          98s
```

## Configurar el rango de IP

MetalLB necesita saber qué direcciones puede repartir entre los servicios de tipo `LoadBalancer`. En este laboratorio utilizaremos la red de Vagrant `192.168.121.0/24`, así que reservaremos el rango `192.168.121.200-192.168.121.220`.

Crearemos el fichero `metallb-config.yaml` con esta configuración:

```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: default-pool
  namespace: metallb-system
spec:
  addresses:
    - 192.168.121.200-192.168.121.220
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: default
  namespace: metallb-system
```

Aplicamos la configuración:

```bash
sudo kubectl patch service traefik \
  --namespace kube-system \
  --type merge \
  --patch '{"spec":{"loadBalancerIP":"192.168.121.202"}}'

sudo kubectl patch service kong-gateway-proxy \
  --namespace kong \
  --type merge \
  --patch '{"spec":{"loadBalancerIP":"192.168.121.200"}}'

sudo kubectl apply -f metallb-config.yaml
```

Fijamos las direcciones antes de activar el pool porque k3s instala Traefik como otro servicio `LoadBalancer`. Si dejamos que MetalLB reparta las IP por orden de llegada, Traefik puede recibir `.200` y Kong `.201`. Con estos dos parches el resto de la serie puede utilizar siempre `192.168.121.200` para acceder al proxy de Kong.

## Comprobar el funcionamiento

A partir de este momento, MetalLB detectará que existe un servicio `LoadBalancer` esperando una IP y le asignará una de las direcciones del pool configurado.

Podemos comprobarlo con:

```bash
sudo kubectl get svc -n kong
```

```text
NAME                                 TYPE           CLUSTER-IP      EXTERNAL-IP       PORT(S)
kong-controller-metrics              ClusterIP      10.43.111.50    <none>            10255/TCP,10254/TCP
kong-controller-validation-webhook   ClusterIP      10.43.170.230   <none>            443/TCP
kong-gateway-admin                   ClusterIP      None            <none>            8444/TCP
kong-gateway-manager                 NodePort       10.43.153.49    <none>            8002:31168/TCP,8445:31598/TCP
kong-gateway-proxy                   LoadBalancer   10.43.17.15     192.168.121.200   80:32263/TCP,443:32183/TCP
```

Ya podemos validar que Kong responde correctamente realizando una petición HTTP a la IP asignada:

```bash
curl http://192.168.121.200
```

```json
{
  "message":"no Route matched with those values",
  "request_id":"fc933367932d940c706aea117a8db358"
}
```

Esta respuesta es la esperada. Kong ya está funcionando y el proxy responde, pero todavía no hemos creado ningún recurso `Gateway`, `HTTPRoute` o `Ingress` que le indique cómo enrutar las peticiones hacia una aplicación concreta.

## Publicar una aplicación mediante Gateway API

Una vez instalado **Kong Gateway** y **Kong Ingress Controller**, vamos a publicar una aplicación de ejemplo usando **Gateway API**, que es el modelo recomendado actualmente por Kubernetes.

En este laboratorio utilizaremos el dominio:

```text
echo.javiercd.es
```

> **Importante:** Para resolver este dominio debes añadir una entrada en el fichero `/etc/hosts` de tu equipo apuntando a la dirección IP asignada por MetalLB.
>
> ```text
> 192.168.121.200 echo.javiercd.es
> ```

### Crear el namespace de la aplicación

Primero crearemos un *namespace* independiente para la aplicación de ejemplo. Así mantenemos separados los recursos de infraestructura y los recursos de la aplicación.

```bash
sudo kubectl create namespace javier
```

### Desplegar la aplicación

Vamos a crear un pequeño *echo server* que responderá con un texto fijo. Para ello usaremos `hashicorp/http-echo`.

Crearemos el fichero `echo.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: echo
  namespace: javier
spec:
  replicas: 1
  selector:
    matchLabels:
      app: echo
  template:
    metadata:
      labels:
        app: echo
    spec:
      containers:
        - name: echo
          image: hashicorp/http-echo
          args:
            - "-text=Hola desde Kong Gateway"
          ports:
            - containerPort: 5678
---
apiVersion: v1
kind: Service
metadata:
  name: echo
  namespace: javier
spec:
  selector:
    app: echo
  ports:
    - port: 80
      targetPort: 5678
```

Aplicamos los recursos:

```bash
sudo kubectl apply -f echo.yaml
```

Y verificamos que el *Deployment* y el *Service* han quedado creados:

```bash
sudo kubectl get all -n javier
```

### Crear el GatewayClass

Kong necesita un **GatewayClass** que identifique qué controlador se encargará de gestionar los recursos `Gateway`.

Este objeto es de ámbito de clúster, por lo que solo hay que crearlo una vez. En este laboratorio lo gestionaremos manualmente, por eso añadimos la anotación `konghq.com/gatewayclass-unmanaged: "true"`.

Crearemos el fichero `gatewayclass.yaml`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: kong
  annotations:
    konghq.com/gatewayclass-unmanaged: "true"
spec:
  controllerName: konghq.com/kic-gateway-controller
```

Aplicamos la configuración:

```bash
sudo kubectl apply -f gatewayclass.yaml
```

Comprobamos que se ha creado correctamente:

```bash
sudo kubectl get gatewayclass
```

```text
NAME   CONTROLLER                          ACCEPTED   AGE
kong   konghq.com/kic-gateway-controller   True       8m13s
```

### Crear el Gateway

Ahora crearemos el recurso `Gateway`, que representa el punto de entrada de nuestro tráfico.

Lo almacenaremos en el *namespace* `kong`, ya que forma parte de la infraestructura del clúster y no de una aplicación concreta.

Crearemos el fichero `gateway.yaml`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: kong
  namespace: kong
spec:
  gatewayClassName: kong
  listeners:
    - name: http
      protocol: HTTP
      port: 80
      allowedRoutes:
        namespaces:
          from: All
```

Aplicamos el recurso:

```bash
sudo kubectl apply -f gateway.yaml
```

Y verificamos su estado:

```bash
sudo kubectl get gateway -n kong
```

```text
NAME   CLASS   ADDRESS           PROGRAMMED   AGE
kong   kong    192.168.121.200   True         15m
```

### Publicar la aplicación mediante HTTPRoute

El siguiente paso es conectar el `Gateway` con el servicio `echo` mediante un recurso `HTTPRoute`.

Crearemos el fichero `httproute.yaml`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: echo
  namespace: javier
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
            value: /echo
      backendRefs:
        - name: echo
          port: 80
```

Aplicamos la configuración:

```bash
sudo kubectl apply -f httproute.yaml
```

Y comprobamos el estado del recurso:

```bash
sudo kubectl get httproute -n javier
```

```text
NAME   HOSTNAMES              AGE
echo   ["echo.javiercd.es"]   15m
```

### Cómo traduce KIC estos recursos a Kong

KIC observa los recursos Kubernetes y mantiene la configuración equivalente dentro de Kong Gateway. En este ejemplo:

- `GatewayClass` selecciona el controlador `konghq.com/kic-gateway-controller`.
- `Gateway` define el punto de entrada HTTP que KIC asociará al proxy `kong-gateway-proxy`.
- `Deployment` y `Service` `echo` forman el backend. KIC los representa como un Service de Kong y sus targets upstream.
- `HTTPRoute` se convierte en una Route de Kong. `hostnames` y el prefijo `/echo` son sus criterios de coincidencia, y `backendRefs` indica el Service destino.

En los siguientes laboratorios añadiremos `KongPlugin`, `KongConsumer` y `Secret`. KIC los convertirá respectivamente en plugins, Consumers y credenciales de Kong, y la anotación `konghq.com/plugins` asociará el plugin a la Route.

### Probar la aplicación

Como la ruta se ha definido con el prefijo `/echo`, la petición debe incluir ese prefijo para coincidir con el `HTTPRoute`.

```bash
curl http://echo.javiercd.es/echo
```

La respuesta debe ser similar a esta:

```text
Hola desde Kong Gateway
```

## Publicar la misma aplicación mediante Ingress

Aunque **Gateway API** es el modelo recomendado actualmente, Kong sigue ofreciendo compatibilidad con los recursos **Ingress** tradicionales.

Para comparar ambos enfoques de forma limpia, eliminaremos primero el `HTTPRoute` anterior:

```bash
sudo kubectl delete httproute echo -n javier
```

Ahora crearemos el fichero `ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: echo
  namespace: javier
spec:
  ingressClassName: kong
  rules:
    - host: echo.javiercd.es
      http:
        paths:
          - path: /echo
            pathType: Prefix
            backend:
              service:
                name: echo
                port:
                  number: 80
```

Aplicamos el recurso:

```bash
sudo kubectl apply -f ingress.yaml
```

Y verificamos que ha quedado publicado:

```bash
sudo kubectl get ingress -n javier
```

```text
NAME   CLASS   HOSTS              ADDRESS           PORTS   AGE
echo   kong    echo.javiercd.es   192.168.121.200   80      2m25s
```

Finalmente, probamos el acceso. Como el `Ingress` también define el prefijo `/echo`, la raíz del dominio no coincide y devuelve `no Route matched`. Es el comportamiento esperado:

```bash
curl http://echo.javiercd.es
```

```json
{
  "message":"no Route matched with those values",
  "request_id":"fb0d4260840a3156e1dd8d52a4c44829"
}
```

La petición válida debe conservar el prefijo:

```bash
curl http://echo.javiercd.es/echo
```

```text
Hola desde Kong Gateway
```

Como has podido ver, este artículo ha sido una primera introducción a **Kong Gateway** y a su despliegue sobre un clúster de Kubernetes. Evidentemente, todavía quedan muchos aspectos por explorar, como colocar un balanceador de carga delante del gateway, diseñar una arquitectura de alta disponibilidad, configurar el escalado automático, mejorar la observabilidad o aplicar medidas avanzadas de seguridad, entre otros.

Sin embargo, ese no era el objetivo de este artículo. La idea era ofrecer una primera toma de contacto con la plataforma, comprender su arquitectura y realizar un despliegue funcional con la configuración mínima necesaria para empezar a trabajar con ella.

Espero que este recorrido te haya resultado útil y que te haya servido para conocer una de las muchas formas de desplegar Kong Gateway. En los próximos artículos iremos profundizando poco a poco, abordando configuraciones más avanzadas y escenarios reales para sacar todo el partido a la plataforma.

Nos vemos en el siguiente post.

---

**Artículo anterior:** [Laboratorio: instalación de Kong en Konnect](/posts/kong/05-instalacion-kong-connect/05-instalacion-kong-connect/)  
**Siguiente artículo:** [Laboratorio: Instalación de Kong en Kubernetes (Modo Híbrido)](/posts/kong/07-instalacion-kubernetes-hibrido/07-instalacion-kubernetes-hibrido/)
