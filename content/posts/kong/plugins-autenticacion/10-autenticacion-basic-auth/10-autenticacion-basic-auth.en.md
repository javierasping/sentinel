---
title: "Basic Auth in Kong"
description: "How HTTP Basic Authentication works and how to protect an HTTPRoute resource with Kong Gateway's Basic Auth plugin and KIC."
weight: 10
aliases:
  - /posts/kong/10-autenticacion-basic-auth/10-autenticacion-basic-auth/
---

Basic Authentication may seem like a trivial mechanism because it only uses a username and a password. However, using it correctly means separating three ideas: the HTTP standard, the validation performed by Kong Gateway, and the identity that Kong associates with valid credentials.

In this article we will look at those three layers and build a reproducible lab with Kong Ingress Controller, Gateway API, and an `HTTPRoute`. The goal is not simply to copy manifests. First we will understand what each resource represents, then we will apply it, and finally we will check what happens inside Kong.

> [!NOTE]
> This lab continues exactly from the scenario created in the [KIC installation post](/posts/kong/03-instalacion-kic/03-instalacion-kic/). It reuses the `Gateway` `kong`, the `echo` Service, and the `192.168.121.200` address assigned by MetalLB to `kong-gateway-proxy`.
>
> The tests in this article were carried out with Kong Gateway `3.10.0.16` and Kong Ingress Controller `3.5`. The current official documentation also describes features added later. Whenever an option requires Kong Gateway 3.13 or 3.15, this is stated explicitly.

## 1. What is Basic Authentication?

Basic Authentication is an authentication scheme defined by [RFC 7617](https://www.rfc-editor.org/rfc/rfc7617.html). It allows an HTTP client to send a username and password inside the `Authorization` header.

The client starts by building a string with this format:

```text
username:password
```

The `:` character separates both values. The client then encodes the string with Base64 and adds the result to the HTTP header:

```text
username:password
        |
        v
      Base64
        |
        v
Authorization: Basic <credentials>
```

In our lab we will use:

```text
alice:alice-basic-password
```

We can calculate its Base64 representation from the terminal. We use `-n` so that `echo` does not append a newline to the end of the string:

```bash
echo -n 'alice:alice-basic-password' | base64
```

The result is:

```text
YWxpY2U6YWxpY2UtYmFzaWMtcGFzc3dvcmQ=
```

Therefore, the complete header is:

```http
Authorization: Basic YWxpY2U6YWxpY2UtYmFzaWMtcGFzc3dvcmQ=
```

Base64 is an encoding, not encryption. Anyone who captures the header can decode it and recover the username and password. For this reason, Basic Authentication must be used over HTTPS. TLS provides confidentiality and integrity during transport.

The standard also defines the challenge that a server can return when credentials are missing. In this article we will focus on the `401 Unauthorized` status code and the validation performed by Kong.

## 2. How does Basic Authentication work in Kong Gateway?

Kong implements this mechanism through the official [`basic-auth`](https://developer.konghq.com/plugins/basic-auth/) plugin. The plugin is available for traditional, hybrid, and DB-less topologies, and can be applied globally, to a Gateway `Service`, or to a `Route`.

In this lab we will apply it only to the `Route` generated from `/basic-auth`. This means that the other routes published on `echo.javiercd.es` are not protected by this plugin.

When a request matches the `Route`, Kong runs the plugin during access processing, before sending the request to the upstream. According to the official documentation, it looks for credentials in this order:

1. `Proxy-Authorization`
2. `Authorization`

If it finds a Basic header, it decodes the value, locates the credential, and compares the received password with the password stored for that identity.

The following diagram summarizes the two possible branches of the plugin. Invalid credentials end at Kong with a `401 Unauthorized` response. Valid credentials identify the Consumer and allow the request to continue to the upstream.

![Basic Authentication flow in Kong Gateway](/kong/plugins-autenticacion/10-autenticacion-basic-auth/img/basic-auth-flow-en.svg)

The behavior is as follows:

- If there are no credentials and anonymous access has not been configured, Kong returns `401 Unauthorized`.
- If the user does not exist, Kong returns `401 Unauthorized`.
- If the password does not match, Kong returns `401 Unauthorized`.
- If the credentials are valid, Kong identifies the Consumer and allows the request to continue.
- When Kong rejects authentication, the request does not reach the upstream.

In the lab version, both missing credentials and an incorrect password produce this response:

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{"message":"Unauthorized"}
```

The Basic Auth plugin does not decide which backend receives a request. Backend selection remains the responsibility of the `Route` and the `Service`. The plugin only adds a prerequisite: the identity must be authenticated successfully.

## 3. Consumers and Basic Auth credentials

A Consumer is the representation Kong uses to identify an API client. It can represent a person, an application, a service, a device, or any other entity that needs to consume an API.

Do not confuse these three names in the lab:

- `basic-auth-client` is the name of the `KongConsumer` resource in Kubernetes.
- `alice` is the Consumer's `username` in Kong.
- `alice` is also the username in the Basic Auth credential.

Although they match in this example, the Consumer's `username` and the credential's `username` are different fields.

The relationship is:

```text
Consumer
    |
    +-- Basic Auth credential
            |
            +-- username
            +-- password
```

The Consumer provides the identity. The credential provides the proof used to demonstrate that identity. Once validation finishes successfully, Kong knows both the authenticated Consumer and the identifier of the credential that was used.

A single Consumer can have several credentials. This makes it possible, for example, to rotate credentials by creating a new credential before revoking the previous one.

## 4. Configuring Basic Auth in Kong with KIC

We will publish the `echo` Service through an `HTTPRoute` and protect that route with Basic Auth:

```text
Client
   |
   v
HTTPRoute /basic-auth
   |
Basic Auth plugin
   |
   v
echo Service
   |
   v
Upstream service

KongConsumer alice
   |
Basic Auth credential
```

The KIC installation post already created these shared resources:

- The `Gateway` `kong` in the `kong` namespace.
- The `echo` Service in the `javier` namespace.
- Kong's proxy exposed through MetalLB.

We will not create them again. This lab only adds a `KongPlugin`, a `Secret`, a `KongConsumer`, and an `HTTPRoute`.

### 4.1. Relationship between Kubernetes and Kong resources

| Kubernetes resource | Kong internal resource |
| --- | --- |
| `KongPlugin` | `plugins` |
| `Secret` | `basicauth_credentials` |
| `KongConsumer` | `consumers` |
| `HTTPRoute` | `routes`, `services`, `upstreams`, and `targets` |

In DB-less mode, these translations are part of Kong's in-memory configuration. In traditional mode, they would be reflected in entities such as `plugins`, `basicauth_credentials`, `consumers`, `routes`, `services`, `upstreams`, and `targets`.

### 4.2. Create the basic-auth plugin

This file declares the plugin that will perform the validation.

`hide_credentials: true` tells Kong to remove the header used for authentication before sending the request to the upstream.

The `KongPlugin` does not protect any route by itself. It becomes associated with a route when we add its name to the `HTTPRoute` annotation.

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: basic-auth
  namespace: javier
plugin: basic-auth
config:
  hide_credentials: true
```

In a database-backed installation, this configuration would become a `plugins` entity. When associated with the `Route`, the entity would contain a reference to that `Route`.

### 4.3. Create the credential

KIC uses a Kubernetes `Secret` to declare authentication plugin credentials.

The `konghq.com/credential: basic-auth` label is required. It tells KIC to interpret `username` and `password` as a Basic Auth credential instead of treating the object as a generic `Secret`.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: basic-auth-credential
  namespace: javier
  labels:
    konghq.com/credential: basic-auth
stringData:
  username: alice
  password: alice-basic-password
```

Using `stringData` makes the lab easier because Kubernetes performs the Base64 encoding when it stores the `Secret`. That Kubernetes encoding does not encrypt the password either.

KIC reads this `Secret` and translates it into a Basic Auth credential. In a database-backed Kong deployment, it would correspond to a `basicauth_credentials` entity, not to a generic Secrets table.

### 4.4. Create the `KongConsumer`

The `KongConsumer` creates the `alice` identity and references the previous `Secret` through `credentials`.

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: basic-auth-client
  namespace: javier
  annotations:
    kubernetes.io/ingress.class: kong
username: alice
credentials:
  - basic-auth-credential
```

KIC resolves the `basic-auth-credential` reference, creates the Consumer, and associates the credential. In traditional mode, the Consumer would be represented in `consumers` and the credential would retain the relationship through its identifier.

### 4.5. Create the `HTTPRoute`

The `HTTPRoute` publishes the `/basic-auth` route on `echo.javiercd.es`.

`parentRefs` connects the route to the `kong` `Gateway`. `backendRefs` reuses the `echo` Service. The `konghq.com/plugins: basic-auth` annotation applies the previously created `KongPlugin`.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: basic-auth
  namespace: javier
  annotations:
    konghq.com/plugins: basic-auth
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
            value: /basic-auth
      backendRefs:
        - name: echo
          port: 80
```

KIC translates this definition into a Kong `Route`. It also creates or reuses the internal entities needed to reach the `echo` Service endpoints. The annotation creates the association between the `Route` and the plugin.

### 4.6. Apply the manifests

Apply the resources in the order in which we have explained them:

```bash
sudo kubectl apply -f 10-basic-auth-plugin.yaml
sudo kubectl apply -f 10-basic-auth-secret.yaml
sudo kubectl apply -f 10-basic-auth-consumer.yaml
sudo kubectl apply -f 10-basic-auth-httproute.yaml
```

Check their status:

```bash
sudo kubectl get kongplugin basic-auth -n javier
sudo kubectl get kongconsumer basic-auth-client -n javier
sudo kubectl get httproute basic-auth -n javier
sudo kubectl describe httproute basic-auth -n javier
```

The `HTTPRoute` should be accepted by the `Gateway`.

## 5. Testing Basic Authentication

Now we will test the configuration we have deployed.

### 5.1. Request without credentials

```text
Client
   |
   | No Authorization header
   v
Kong
   |
   +-- 401 Unauthorized
```

Run:

```bash
curl -i http://echo.javiercd.es/basic-auth
```

The response observed in the lab is:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 00:51:58 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: Basic realm="javier-basic-auth"
Content-Length: 26
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 1f06711dd1f40a26aaa91059dea08d07

{"message":"Unauthorized"}
```

`X-Kong-Upstream-Latency` is absent because Kong generated the response before contacting `echo`.

### 5.2. Incorrect credentials

`curl -u` builds the `Authorization: Basic` header for us:

```bash
curl -i -u alice:incorrecta \
  http://echo.javiercd.es/basic-auth
```

The response is again:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 00:52:33 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: Basic realm="javier-basic-auth"
Content-Length: 26
X-Kong-Response-Latency: 1
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 27065c1c980b170d78dc2f58adf26a6e

{"message":"Unauthorized"}
```

Kong does not reveal whether the error is caused by a missing user or by an incorrect password.

### 5.3. Correct credentials

```bash
curl -i -u alice:alice-basic-password \
  http://echo.javiercd.es/basic-auth
```

The observed response is:

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: 28
Connection: keep-alive
X-App-Name: http-echo
X-App-Version: 1.0.0
Date: Sun, 26 Jul 2026 00:52:54 GMT
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Upstream-Latency: 1
X-Kong-Proxy-Latency: 0
Via: 1.1 kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 7f7c177c2462212be44bd8068f016b44

Hola desde Kong Gateway KIC
```

This time Kong identified the Consumer and sent the request to the upstream.

We can also send the header manually:

```bash
curl -i \
  -H 'Authorization: Basic YWxpY2U6YWxpY2UtYmFzaWMtcGFzc3dvcmQ=' \
  http://echo.javiercd.es/basic-auth
```

## Official sources

- [RFC 7617: The Basic HTTP Authentication Scheme](https://www.rfc-editor.org/rfc/rfc7617.html)
- [Basic Auth plugin](https://developer.konghq.com/plugins/basic-auth/)
- [Basic Auth configuration reference](https://developer.konghq.com/plugins/basic-auth/reference/)
- [Basic Auth changelog](https://developer.konghq.com/plugins/basic-auth/changelog/)
- [Authenticate Consumers with Basic Auth](https://developer.konghq.com/how-to/authenticate-consumers-with-basic-authentication/)
- [Consumer entity](https://developer.konghq.com/gateway/entities/consumer/)
- [Kong Identity Principals](https://developer.konghq.com/identity/principals/)
- [ACL plugin](https://developer.konghq.com/plugins/acl/)
