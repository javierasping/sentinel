---
title: "Key Auth in Kong"
date: 2026-07-26T00:00:00+02:00
description: "How API key authentication works and how to protect an HTTPRoute with Kong Gateway's Key Auth plugin and KIC."
tags: [Kong, Authentication, API Key, Key Auth, KIC]
weight: 11
hero: images/kong/key-auth.png
aliases:
  - /posts/kong/11-autenticacion-key-auth/11-autenticacion-key-auth/
---

An API key may look like little more than a random string that a client adds to every request. To use it correctly, however, it helps to separate three ideas: the credential presented by the client, the validation performed by Kong Gateway, and the identity of the Consumer associated with that credential.

This article covers those three layers and builds a reproducible lab with Kong Ingress Controller. We will first understand each resource, then apply it, and finally verify what happens inside Kong.

> [!NOTE]
> This lab continues directly from [Installing KIC](/posts/kong/03-instalacion-kic/03-instalacion-kic/). It reuses the `kong` Gateway, the `echo` Service, and the `192.168.121.200` address assigned by MetalLB to `kong-gateway-proxy`.
>
> The tests in this article were run with Kong Gateway `3.10.0.16` and Kong Ingress Controller `3.5`.

## 1. What is an API key?

An API key is a credential that an application uses to identify itself to an API. It is normally generated as a long, hard-to-guess string:

```text
my-super-secret-api-key
```

Unlike Basic Authentication, the client does not send a username and password. It sends a key that Kong can associate with a credential and, through that credential, with a Consumer.

Key Auth does not define a universal HTTP header. The name and location of the API key depend on the gateway configuration. Kong can look for it in:

- An HTTP header.
- A URL parameter.
- The request body.

This lab uses a header named `apikey`:

```http
apikey: my-super-secret-api-key
```

The API key is a shared secret. Any client that knows it can use it while it remains valid. It must not be committed to source code or a repository and, like a password, must always be sent over HTTPS.

API keys should also be avoided in URL parameters because URLs can be recorded in browser history, proxies, observability tools, and access logs. We will therefore configure the plugin to accept the key only from a header.

API key authentication proves that the client knows a valid credential. It does not encrypt the request or replace TLS, and it does not decide which resources the Consumer may use. That second decision is authorization and can, for example, be implemented with the ACL plugin.

## 2. How does Key Auth work in Kong Gateway?

Kong implements this mechanism through the official [`key-auth`](https://developer.konghq.com/plugins/key-auth/) plugin. It supports traditional, hybrid, and DB-less topologies and can be applied globally, to a Gateway Service, or to a Route.

In this lab it is applied only to the Route generated from `/key-auth`, so other routes published on `echo.javiercd.es` are not protected by this plugin.

When a request matches the Route, Kong runs the plugin during the access phase, before forwarding the request upstream:

1. Kong looks for a header named `apikey`.
2. If it is missing, Kong rejects the request.
3. If it exists, Kong looks for a credential with that value.
4. If the credential does not exist, Kong rejects the request.
5. If it is valid, Kong identifies the associated Consumer.
6. Before contacting the upstream, Kong removes the `apikey` header.
7. Kong adds Consumer identity headers and allows the request to continue.

The following diagram summarizes the complete flow. A missing or unknown key ends at Kong with `401 Unauthorized`. A valid key identifies the Consumer, is removed before proxying, and is replaced with identity headers.

![Key Auth flow in Kong Gateway](/kong/plugins-autenticacion/11-autenticacion-key-auth/img/key-auth-flow-en.svg)

The resulting behavior is:

- No API key and no anonymous access returns `401 Unauthorized`.
- An unknown API key returns `401 Unauthorized`.
- A valid credential identifies the Consumer and allows the request through.
- When authentication fails, the request never reaches the upstream.

After authentication, Kong can add headers such as `X-Consumer-ID`, `X-Consumer-Username`, and `X-Credential-Identifier`. The backend can therefore receive the validated identity without receiving the original API key.

Key Auth does not choose the backend. Routing remains the responsibility of the Route and Service. The plugin only adds the prerequisite that the client must authenticate successfully.

## 3. Consumers and Key Auth credentials

A Consumer is Kong's representation of an API client. It can represent a person, application, service, device, or any other entity that needs to consume an API.

Do not confuse these three lab values:

- `key-auth-client` is the Kubernetes `KongConsumer` resource name.
- `key-client` is the Consumer `username` in Kong.
- `my-super-secret-api-key` is the Key Auth credential value.

Their relationship is:

```text
Consumer
    |
    +-- Key Auth credential
            |
            +-- key
```

The Consumer provides the identity. The API key provides the proof used to establish that identity. Once validation succeeds, Kong knows both the authenticated Consumer and the credential identifier.

A Consumer can have multiple credentials, although assigning a separate credential per client generally makes usage and rotation easier to control.

`my-super-secret-api-key` keeps the lab readable but is not suitable for production. A real key must have sufficient entropy, be stored in a secrets manager, and be rotated when required.

## 4. Configuring Key Auth in Kong with KIC

We will publish the `echo` Service through an `HTTPRoute` and protect it with Key Auth.

The KIC installation article already created:

- The `kong` Gateway in the `kong` namespace.
- The `echo` Service in the `javier` namespace.
- Kong's proxy exposed through MetalLB.

This lab adds only a `KongPlugin`, a `Secret`, a `KongConsumer`, and an `HTTPRoute`.

### 4.1. Relationship between Kubernetes and Kong resources

| Kubernetes resource | Internal Kong resource |
| --- | --- |
| `KongPlugin` | `plugins` |
| `Secret` | `keyauth_credentials` |
| `KongConsumer` | `consumers` |
| `HTTPRoute` | `routes`, `services`, `upstreams`, and `targets` |

In DB-less mode, these translations form part of Kong's in-memory configuration. In traditional mode, they correspond to entities such as `plugins`, `keyauth_credentials`, `consumers`, `routes`, `services`, `upstreams`, and `targets`.

### 4.2. Create the key-auth plugin

This file declares the plugin that validates the credential.

`key_names` defines the header containing the API key. `key_in_header: true` enables header lookup, while `key_in_query: false` and `key_in_body: false` disable the other locations.

`hide_credentials: true` tells Kong to remove the API key before forwarding the request upstream.

The `KongPlugin` does not protect a route by itself. We attach it later through the `HTTPRoute` annotation.

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: key-auth
  namespace: javier
plugin: key-auth
config:
  key_names:
    - apikey
  key_in_header: true
  key_in_query: false
  key_in_body: false
  hide_credentials: true
```

In a database-backed deployment, this configuration would become a `plugins` entity associated with the Route.

### 4.3. Create the credential

KIC uses a Kubernetes `Secret` to declare authentication plugin credentials.

The `konghq.com/credential: key-auth` label is required. It tells KIC to interpret `key` as a Key Auth credential instead of treating the object as a generic Secret.

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

`stringData` keeps the example readable because Kubernetes performs Base64 encoding when storing the Secret. Base64 does not encrypt the API key.

KIC translates this Secret into a Key Auth credential. In database-backed Kong, it would correspond to a `keyauth_credentials` entity.

### 4.4. Create the `KongConsumer`

The `KongConsumer` creates the `key-client` identity and references the Secret through `credentials`.

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: key-auth-client
  namespace: javier
  annotations:
    kubernetes.io/ingress.class: kong
username: key-client
credentials:
  - key-auth-credential
```

KIC resolves `key-auth-credential`, creates the Consumer, and attaches the credential. In traditional mode, the Consumer is represented in `consumers` and the credential retains its relationship with that Consumer.

### 4.5. Create the `HTTPRoute`

The `HTTPRoute` publishes `/key-auth` on `echo.javiercd.es`.

`parentRefs` attaches the route to the `kong` Gateway, `backendRefs` reuses the `echo` Service, and `konghq.com/plugins: key-auth` attaches the plugin.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: key-auth
  namespace: javier
  annotations:
    konghq.com/plugins: key-auth
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
            value: /key-auth
      backendRefs:
        - name: echo
          port: 80
```

KIC translates this definition into a Kong Route and the internal entities required to reach the `echo` endpoints. The annotation creates the Route-to-plugin association.

### 4.6. Apply the manifests

Apply the resources in the order used above:

```bash
sudo kubectl apply -f 11-key-auth-plugin.yaml
sudo kubectl apply -f 11-key-auth-secret.yaml
sudo kubectl apply -f 11-key-auth-consumer.yaml
sudo kubectl apply -f 11-key-auth-httproute.yaml
```

Check their status:

```bash
sudo kubectl get kongplugin key-auth -n javier
sudo kubectl get kongconsumer key-auth-client -n javier
sudo kubectl get httproute key-auth -n javier
sudo kubectl describe httproute key-auth -n javier
```

The `HTTPRoute` must be accepted by the Gateway.

## 5. Testing API key authentication

The following responses were captured directly in the VM after KIC synchronized the plugin with Kong.

### 5.1. Request without an API key

Send a request without credentials:

```bash
curl -i http://echo.javiercd.es/key-auth
```

Kong responds before contacting the upstream:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:01:38 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: Key
Content-Length: 96
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 33d2aa6620e5600619ef1f3cc9262529

{
  "message":"No API key found in request",
  "request_id":"33d2aa6620e5600619ef1f3cc9262529"
}
```

There is no `X-Kong-Upstream-Latency` header because Kong generated the response without contacting `echo`.

### 5.2. Incorrect API key

Send a key that does not match any credential:

```bash
curl -i \
  -H 'apikey: incorrecta' \
  http://echo.javiercd.es/key-auth
```

Kong again returns `401 Unauthorized`:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:01:38 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: Key
Content-Length: 81
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 821af909aa88af45730f05506213df07

{
  "message":"Unauthorized",
  "request_id":"821af909aa88af45730f05506213df07"
}
```

Kong distinguishes internally between a missing key and an unknown credential, but both are blocked before reaching the upstream.

### 5.3. Correct API key

Send the key defined in the Secret:

```bash
curl -i \
  -H 'apikey: my-super-secret-api-key' \
  http://echo.javiercd.es/key-auth
```

The observed response is:

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: 28
Connection: keep-alive
X-App-Name: http-echo
X-App-Version: 1.0.0
Date: Sun, 26 Jul 2026 09:01:38 GMT
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Upstream-Latency: 1
X-Kong-Proxy-Latency: 0
Via: 1.1 kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: c20f3b492444df164a1f6201b915a14f

Hola desde Kong Gateway KIC
```

Kong found the credential, identified the `key-client` Consumer, and forwarded the request upstream.

Because `hide_credentials: true`, `echo` does not receive `apikey`. Kong can instead forward `X-Consumer-ID`, `X-Consumer-Username`, and `X-Credential-Identifier`.

The API key cannot be sent through the URL:

```bash
curl -i \
  'http://echo.javiercd.es/key-auth?apikey=my-super-secret-api-key'
```

Although `key_in_query` is enabled by default, this configuration explicitly disables it. The real response is:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:01:38 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: Key
Content-Length: 96
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: d504a5297bc5250f227eb70b4c2f7351

{
  "message":"No API key found in request",
  "request_id":"d504a5297bc5250f227eb70b4c2f7351"
}
```

## Official sources

- [Key Auth plugin](https://developer.konghq.com/plugins/key-auth/)
- [Key Auth configuration reference](https://developer.konghq.com/plugins/key-auth/reference/)
- [Key Authentication with KIC](https://developer.konghq.com/kubernetes-ingress-controller/get-started/key-authentication/)
- [Consumer entity](https://developer.konghq.com/gateway/entities/consumer/)
- [KIC annotation reference](https://developer.konghq.com/kubernetes-ingress-controller/reference/annotations/)
- [ACL with KIC](https://developer.konghq.com/kubernetes-ingress-controller/acl/)
