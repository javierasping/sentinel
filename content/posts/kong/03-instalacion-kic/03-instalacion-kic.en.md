---
title: "Installing Kong Ingress Controller (KIC)"
date: 2026-07-02T14:45:00+00:00
description: "Step-by-step guide to install Kong Gateway and Kong Ingress Controller on Kubernetes, validate the deployment, and expose the proxy with MetalLB."
tags: [Kong, Testing, Validation, API Gateway]
hero: images/kong/10-verificacion/hero.png
weight: 3
---

In this article, we will move from theory to a real deployment. The goal is to install **Kong Ingress Controller (KIC)** in a Kubernetes cluster, verify that **Kong Gateway** is working properly, and prepare the external exposure of the proxy so that we can publish applications from the cluster itself.

To keep the lab simple, I will use a single virtual machine created with **Vagrant** on which I will run a **k3s** cluster. This choice does not change the way Kong works, but it allows us to focus on what really matters: what KIC installs, why the proxy service initially appears in `Pending`, and how to solve that with **MetalLB**.

It is also worth being clear from the beginning that **KIC is not an independent gateway**. Its job is to observe Kubernetes resources, translate them into Kong configuration, and keep that configuration synchronized. In other words: Kubernetes defines the desired state, and KIC turns it into a real configuration for Kong Gateway.

## Installing Kong Ingress Controller

Once our Kubernetes cluster is working, the next step is to install **Kong Ingress Controller (KIC)** together with **Kong Gateway**.

Kong offers an official Helm repository from which we can deploy both components with a single chart. In this lab, we will pin **Kong Gateway 3.10 open source** to work with a known and reproducible version.

### Add the Helm repository

The first step is to register the official Kong repository and update the index of available charts.

```bash
helm repo add kong https://charts.konghq.com
helm repo update
```

If we want to review which chart versions are available, we can check them with:

```bash
helm search repo kong/ingress --versions
```

### Install Kong Ingress Controller

Now we will install the official Kong chart. With this command, the controller, the gateway, and all the auxiliary resources they need to work inside the cluster will be deployed.

```bash
helm install kong kong/ingress \
  --namespace kong \
  --create-namespace \
  --set gateway.image.repository=kong/kong-gateway \
  --set gateway.image.tag=3.10
```

With this installation, we are doing several things at the same time:

- We create the `kong` namespace if it does not already exist.
- We deploy **Kong Gateway 3.10 open source**.
- We deploy **Kong Ingress Controller**.
- We create the *Deployments*, *Services*, *ConfigMaps*, *Roles*, and other resources needed.
- We register the **CRDs** that Kong uses to integrate with Kubernetes.

Once the installation is complete, we can verify that the pods are running:

```bash
sudo kubectl get pods -n kong
```

```text
NAME                               READY   STATUS    RESTARTS   AGE
kong-controller-79b8f95d99-dtndr   1/1     Running   0          5m53s
kong-gateway-db57d88fc-h72wz       1/1     Running   0          5m53s
```

It is also a good idea to inspect the resources Helm has created in the `kong` namespace:

```bash
sudo kubectl get all -n kong
```

If everything is correct, we should see the controller and gateway pods, the associated services, and the corresponding *Deployments*.

### Verify the CRDs

Since Kong integrates with Kubernetes through custom resources, it is also worth checking that the **CRDs** were installed correctly:

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

If the pods are in **Running** state and the CRDs appear in the list, then **Kong Gateway** and **Kong Ingress Controller** are installed and ready to start publishing traffic.

## Installing MetalLB

When we inspect the service that exposes Kong's proxy, we will see that the **EXTERNAL-IP** appears as `<pending>`.

```bash
sudo kubectl get svc -n kong
```

```text
NAME                 TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)
kong-gateway-proxy   LoadBalancer   10.43.17.15     <pending>     80:32263/TCP,443:32183/TCP
```

This does not mean the installation has failed. What happens is that our cluster does not have a *LoadBalancer* provider that can assign an external IP to the service.

On managed platforms such as **Amazon EKS**, **Google GKE**, or **Azure AKS**, that assignment is handled by the cloud provider itself. However, in a **k3s** lab or an *on-premise* environment, we need an additional solution.

To cover that role, we will use **MetalLB**, which acts as a load balancer for Kubernetes clusters and allows IP addresses to be assigned to services of type `LoadBalancer`.

### Install MetalLB

We will start by applying the official MetalLB manifests:

```bash
sudo kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.15.2/config/manifests/metallb-native.yaml
```

When the installation finishes, we will verify that its main components are active:

```bash
sudo kubectl get pods -n metallb-system
```

```text
NAME                          READY   STATUS    RESTARTS   AGE
controller-6dd55858b4-v9rmh   1/1     Running   0          98s
speaker-4tfcv                 1/1     Running   0          98s
```

## Configure the IP range

MetalLB needs to know which addresses it can hand out to services of type `LoadBalancer`. In this lab, we will use the Vagrant network `192.168.121.0/24`, so we will reserve the range `192.168.121.200-192.168.121.220`.

We will create a file named `metallb-config.yaml` with this configuration:

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

Apply the configuration:

```bash
sudo kubectl apply -f metallb-config.yaml
```

## Check the result

From this point on, MetalLB will detect that a `LoadBalancer` service is waiting for an IP and will assign one of the addresses from the configured pool.

We can verify it with:

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

We can now validate that Kong responds correctly by making an HTTP request to the assigned IP:

```bash
curl http://192.168.121.200
```

```json
{
  "message":"no Route matched with those values",
  "request_id":"fc933367932d940c706aea117a8db358"
}
```

This response is the expected one. Kong is already working and the proxy responds, but we still have not created any `Gateway`, `HTTPRoute`, or `Ingress` resource that tells it how to route traffic to a specific application.

## Publish an application with Gateway API

Once **Kong Gateway** and **Kong Ingress Controller** are installed, we are going to publish a sample application using **Gateway API**, which is the model currently recommended by Kubernetes.

In this lab, we will use the domain:

```text
echo.javiercd.es
```

> **Important:** To resolve this domain, you must add an entry to the `/etc/hosts` file on your machine pointing to the IP address assigned by MetalLB.
>
> ```text
> 192.168.121.200 echo.javiercd.es
> ```

### Create the application namespace

First, we will create an independent namespace for the sample application. This way, we keep the infrastructure resources separate from the application resources.

```bash
sudo kubectl create namespace javier
```

### Deploy the application

We are going to create a small *echo server* that will respond with a fixed message. To do this, we will use `hashicorp/http-echo`.

We will create the file `echo.yaml`:

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

Apply the resources:

```bash
sudo kubectl apply -f echo.yaml
```

And verify that the *Deployment* and the *Service* have been created:

```bash
sudo kubectl get all -n javier
```

### Create the GatewayClass

Kong needs a **GatewayClass** that identifies which controller will manage the `Gateway` resources.

This object is cluster-scoped, so it only needs to be created once. In this lab, we will manage it manually, which is why we add the annotation `konghq.com/gatewayclass-unmanaged: "true"`.

We will create the file `gatewayclass.yaml`:

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

Apply the configuration:

```bash
sudo kubectl apply -f gatewayclass.yaml
```

Verify that it has been created correctly:

```bash
sudo kubectl get gatewayclass
```

```text
NAME   CONTROLLER                          ACCEPTED   AGE
kong   konghq.com/kic-gateway-controller   True       8m13s
```

### Create the Gateway

Now we will create the `Gateway` resource, which represents the entry point for our traffic.

We will store it in the `kong` namespace, since it belongs to the cluster infrastructure rather than a specific application.

We will create the file `gateway.yaml`:

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

Apply the resource:

```bash
sudo kubectl apply -f gateway.yaml
```

And verify its status:

```bash
sudo kubectl get gateway -n kong
```

```text
NAME   CLASS   ADDRESS           PROGRAMMED   AGE
kong   kong    192.168.121.200   True         15m
```

### Publish the application through HTTPRoute

The next step is to connect the `Gateway` to the `echo` service using an `HTTPRoute` resource.

We will create the file `httproute.yaml`:

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

Apply the configuration:

```bash
sudo kubectl apply -f httproute.yaml
```

And verify the resource status:

```bash
sudo kubectl get httproute -n javier
```

```text
NAME   HOSTNAMES              AGE
echo   ["echo.javiercd.es"]   15m
```

### How KIC maps these resources to Kong

KIC observes Kubernetes resources and maintains the equivalent configuration inside Kong Gateway. In this example:

- `GatewayClass` selects the `konghq.com/kic-gateway-controller` controller.
- `Gateway` defines the HTTP entry point that KIC associates with the `kong-gateway-proxy` proxy.
- The `echo` `Deployment` and `Service` form the backend. KIC represents them as a Kong Service and its upstream Pod targets.
- `HTTPRoute` becomes a Kong Route. `hostnames` and the `/echo` prefix are its matching criteria, while `backendRefs` identifies the destination Service.

In the following labs we will add `KongPlugin`, `KongConsumer`, and `Secret` resources. KIC turns them into Kong plugins, Consumers, and credentials, while the `konghq.com/plugins` annotation associates a plugin with the Route.

### Test the application

Since the route is defined with the `/echo` prefix, the request must include that prefix to match the `HTTPRoute`.

```bash
curl http://echo.javiercd.es/echo
```

The response should be similar to this:

```text
Hola desde Kong Gateway
```

## Publish the same application with Ingress

Although **Gateway API** is the model currently recommended, Kong still offers compatibility with traditional **Ingress** resources.

To compare both approaches clearly, we will first delete the previous `HTTPRoute`:

```bash
sudo kubectl delete httproute echo -n javier
```

Now we will create the file `ingress.yaml`:

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

Apply the resource:

```bash
sudo kubectl apply -f ingress.yaml
```

And verify that it has been published:

```bash
sudo kubectl get ingress -n javier
```

```text
NAME   CLASS   HOSTS              ADDRESS           PORTS   AGE
echo   kong    echo.javiercd.es   192.168.121.200   80      2m25s
```

Finally, we test the access. Since the `Ingress` also defines the `/echo` prefix, the domain root does not match and returns `no Route matched`. That is expected:

```bash
curl http://echo.javiercd.es
```

```json
{
  "message":"no Route matched with those values",
  "request_id":"fb0d4260840a3156e1dd8d52a4c44829"
}
```

The valid request must keep the prefix:

```bash
curl http://echo.javiercd.es/echo
```

```text
Hola desde Kong Gateway
```

As you have seen, this article has been a first introduction to **Kong Gateway** and its deployment on a Kubernetes cluster. There are still many aspects to explore, such as placing a load balancer in front of the gateway, designing a high-availability architecture, configuring automatic scaling, improving observability, or applying advanced security measures, among others.

However, that was not the goal of this article. The idea was to offer a first introduction to the platform, understand its architecture, and perform a functional deployment with the minimum configuration needed to get started.

I hope this walkthrough has been useful to you and that it has helped you understand one of the many ways to deploy Kong Gateway. In future articles, we will go deeper little by little, addressing more advanced configurations and real-world scenarios to make the most of the platform.

See you in the next post.

---

**Previous article:** [Lab: Installing Kong in Konnect](/posts/kong/05-instalacion-kong-connect/05-instalacion-kong-connect/)  
**Next article:** [Lab: Installing Kong on Kubernetes (Hybrid Mode)](/posts/kong/07-instalacion-kubernetes-hibrido/07-instalacion-kubernetes-hibrido/)
