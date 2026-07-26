---
title: "HMAC Auth in Kong"
date: 2026-07-26T00:00:00+02:00
description: "How HMAC signatures work and how to protect an HTTPRoute with Kong Gateway's HMAC Auth plugin and KIC."
tags: [Kong, Authentication, HMAC, Signatures, KIC]
weight: 12
hero: images/kong/hmac-auth.png
---

HMAC Authentication proves that a request was created by a client that knows a shared secret without sending that secret in the request. In addition to authenticating the client, the signature detects changes to the signed elements while they are in transit.

This article explains how an HMAC signature is built and validated by Kong Gateway, and how the Consumer relates to its credential. We then build a reproducible Kong Ingress Controller lab and protect `/hmac-auth`.

> [!NOTE]
> This lab continues directly from [Installing KIC](/posts/kong/03-instalacion-kic/03-instalacion-kic/). It reuses the `kong` Gateway, the `echo` Service, and the `192.168.121.200` address assigned by MetalLB to `kong-gateway-proxy`.
>
> The tests were run with Kong Gateway `3.10.0.16` and Kong Ingress Controller `3.5`.

## 1. What is an HMAC signature?

HMAC, or *Hash-based Message Authentication Code*, combines a hash function with a shared secret. Both the client and Kong know the secret, but they never need to send it over the network.

The client selects the request components to protect and builds a canonical string. This lab signs:

- `date`, to limit how long the request can be reused.
- `@request-target`, containing the HTTP method and requested path.
- `host`, identifying the destination host.

For a `GET` request to `/hmac-auth`, the string has this form:

```text
date: Sun, 26 Jul 2026 10:00:00 GMT
@request-target: get /hmac-auth
host: echo.javiercd.es
```

The client processes that string with HMAC-SHA256 and the shared secret:

```text
Canonical string + secret
            |
            v
       HMAC-SHA256
            |
            v
    Base64-encoded signature
```

It sends the result in `Authorization`:

```http
Authorization: hmac username="hmac-client", algorithm="hmac-sha256", headers="date @request-target host", signature="<signature>"
```

HMAC does not encrypt the request. An observer can still read it over HTTP, so HTTPS remains mandatory: TLS provides confidentiality, while HMAC proves the integrity of the signed data and knowledge of the secret.

The date also reduces replay attacks. Kong checks that the client's clock is within the configured window, which defaults to 300 seconds. Clients and Kong nodes must keep their clocks synchronized.

## 2. How does HMAC Auth work in Kong Gateway?

Kong implements this mechanism through the official [`hmac-auth`](https://developer.konghq.com/plugins/hmac-auth/) plugin. It supports traditional, hybrid, and DB-less topologies and can be applied globally, to a Gateway Service, or to a Route.

This lab applies it only to the Route generated from `/hmac-auth`.

When a request matches the Route, Kong runs the plugin before contacting the upstream:

1. It looks for the signature first in `Proxy-Authorization` and then in `Authorization`.
2. It reads the `username` declared by the client.
3. It finds the HMAC credential associated with that name.
4. It checks that the signature covers `date`, `@request-target`, and `host`.
5. It reconstructs the canonical string from the request.
6. It calculates the signature with the stored secret and compares both values.
7. It verifies that the date is inside the allowed clock window.
8. If every check passes, it identifies the Consumer and continues.

The diagram shows the two resulting branches. Kong rejects a signature that is incorrect, incomplete, or outside the allowed time window. If the calculated signature matches and the date is valid, Kong associates the request with the Consumer and proxies it upstream.

![HMAC Auth flow in Kong Gateway](/kong/plugins-autenticacion/12-autenticacion-hmac-auth/img/hmac-auth-flow-en.svg)

The resulting behavior is:

- A missing signature returns `401 Unauthorized`.
- An unknown user, mismatched signature, or missing required header returns `401 Unauthorized`.
- A date outside the allowed window is rejected.
- A valid signature identifies the Consumer and forwards the request upstream.
- Rejected requests never reach `echo`.

`hide_credentials: true` removes the authentication header before proxying. Kong can instead add `X-Consumer-ID`, `X-Consumer-Username`, and `X-Credential-Identifier`.

HMAC Auth authenticates the Consumer but does not select the backend or authorize individual resources. Routing belongs to the Route and Service. Additional authorization can be implemented with ACL.

## 3. Consumers and HMAC credentials

A Consumer represents the API client. The HMAC credential contains the name declared in the signature and the shared secret used to calculate it.

Do not confuse these lab values:

- `hmac-auth-client` is the Kubernetes `KongConsumer` resource name.
- `hmac-client` is the Consumer username in Kong.
- `hmac-client` is also the HMAC credential username.
- `hmac-shared-secret` is the shared secret.

Their relationship is:

```text
Consumer
    |
    +-- HMAC credential
            |
            +-- username
            +-- secret
```

The Consumer provides identity. The credential provides the data Kong needs to verify the signature. Although both username fields match in this lab, they belong to different objects.

The example secret makes the lab reproducible. In production it must be generated randomly, stored in a secrets manager, and distributed only to the client that signs requests.

## 4. Configuring HMAC Auth in Kong with KIC

We publish the `echo` Service through an `HTTPRoute` and protect it with HMAC Auth.

The KIC installation already created the `kong` Gateway, the `echo` Service, and the proxy exposed by MetalLB. This lab adds only a `KongPlugin`, a `Secret`, a `KongConsumer`, and an `HTTPRoute`.

### 4.1. Relationship between Kubernetes and Kong resources

| Kubernetes resource | Internal Kong resource |
| --- | --- |
| `KongPlugin` | `plugins` |
| `Secret` | `hmacauth_credentials` |
| `KongConsumer` | `consumers` |
| `HTTPRoute` | `routes`, `services`, `upstreams`, and `targets` |

In DB-less mode these translations form part of Kong's in-memory configuration. In traditional mode they correspond to database entities.

### 4.2. Create the hmac-auth plugin

`enforce_headers` requires the signature to protect the three recommended minimum elements. Order also matters because the client must construct the string in the same order declared in `Authorization`.

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: hmac-auth
  namespace: javier
plugin: hmac-auth
config:
  enforce_headers:
    - date
    - "@request-target"
    - host
  hide_credentials: true
```

The `KongPlugin` does not protect a Route by itself. The `HTTPRoute` annotation attaches it.

### 4.3. Create the credential

The `konghq.com/credential: hmac-auth` label tells KIC to translate the Secret into an HMAC credential.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: hmac-auth-credential
  namespace: javier
  labels:
    konghq.com/credential: hmac-auth
stringData:
  username: hmac-client
  secret: hmac-shared-secret
```

Kubernetes Base64-encodes `stringData` when storing the Secret. That encoding is not encryption.

### 4.4. Create the `KongConsumer`

The `KongConsumer` creates the `hmac-client` identity and references the credential:

```yaml
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: hmac-auth-client
  namespace: javier
  annotations:
    kubernetes.io/ingress.class: kong
username: hmac-client
credentials:
  - hmac-auth-credential
```

KIC creates the Consumer and associates the HMAC credential. In traditional mode they are represented through `consumers` and `hmacauth_credentials`.

### 4.5. Create the `HTTPRoute`

The `HTTPRoute` publishes `/hmac-auth` and applies the plugin through `konghq.com/plugins: hmac-auth`.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: hmac-auth
  namespace: javier
  annotations:
    konghq.com/plugins: hmac-auth
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
            value: /hmac-auth
      backendRefs:
        - name: echo
          port: 80
```

### 4.6. Apply the manifests

```bash
sudo kubectl apply -f 12-hmac-auth-plugin.yaml
sudo kubectl apply -f 12-hmac-auth-secret.yaml
sudo kubectl apply -f 12-hmac-auth-consumer.yaml
sudo kubectl apply -f 12-hmac-auth-httproute.yaml
```

Check the resources:

```bash
sudo kubectl get kongplugin hmac-auth -n javier
sudo kubectl get kongconsumer hmac-auth-client -n javier
sudo kubectl get httproute hmac-auth -n javier
sudo kubectl describe httproute hmac-auth -n javier
```

## 5. Testing HMAC Authentication

The following responses were captured directly in the lab VM.

### 5.1. Request without a signature

```bash
curl -i http://echo.javiercd.es/hmac-auth
```

Kong returns `401 Unauthorized` without contacting the upstream:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:01:48 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: hmac
Content-Length: 81
X-Kong-Response-Latency: 0
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 1a794543e980ec54d493cd1edd88800c

{
  "message":"Unauthorized",
  "request_id":"1a794543e980ec54d493cd1edd88800c"
}
```

### 5.2. Create a valid signature

Run the following block on the host. It builds the date, canonical string, and signature with the secret declared in Kubernetes:

```bash
HOST='echo.javiercd.es'
TARGET='/hmac-auth'
DATE="$(LC_ALL=C date -u '+%a, %d %b %Y %H:%M:%S GMT')"
SIGNING_STRING="date: ${DATE}\n@request-target: get ${TARGET}\nhost: ${HOST}"
SIGNATURE="$(echo -en "${SIGNING_STRING}" \
  | openssl dgst -sha256 -hmac 'hmac-shared-secret' -binary \
  | base64 -w0)"
```

Inspect the exact values being signed:

```bash
echo -e "${SIGNING_STRING}"
echo "${SIGNATURE}"
```

### 5.3. Send the signed request

```bash
curl -i \
  -H "Date: ${DATE}" \
  -H "Authorization: hmac username=\"hmac-client\", algorithm=\"hmac-sha256\", headers=\"date @request-target host\", signature=\"${SIGNATURE}\"" \
  "http://${HOST}${TARGET}"
```

Kong rebuilds the string, validates the signature, and identifies `hmac-client`. The real response is:

```http
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: 28
Connection: keep-alive
X-App-Name: http-echo
X-App-Version: 1.0.0
Date: Sun, 26 Jul 2026 09:01:48 GMT
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Upstream-Latency: 0
X-Kong-Proxy-Latency: 0
Via: 1.1 kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 0dc5cb6b1fb32f20969e215ce2c97015

Hola desde Kong Gateway KIC
```

### 5.4. Verify that the signature protects the path

Reuse the same signature but change the destination:

```bash
curl -i \
  -H "Date: ${DATE}" \
  -H "Authorization: hmac username=\"hmac-client\", algorithm=\"hmac-sha256\", headers=\"date @request-target host\", signature=\"${SIGNATURE}\"" \
  "http://${HOST}/hmac-auth/otra-ruta"
```

The signature is invalid because `@request-target` no longer matches the signed value. Kong explains the failure without contacting the upstream:

```http
HTTP/1.1 401 Unauthorized
Date: Sun, 26 Jul 2026 09:01:48 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
WWW-Authenticate: hmac
Content-Length: 98
X-Kong-Response-Latency: 1
Server: kong/3.10.0.16-enterprise-edition
X-Kong-Request-Id: 9a78552fb81cd9672ef9e3668d00dc11

{
  "message":"HMAC signature does not match",
  "request_id":"9a78552fb81cd9672ef9e3668d00dc11"
}
```

The request is also rejected if reused after the clock window expires. Clients must therefore generate a fresh date and signature for every request.

## Official sources

- [HMAC Auth plugin](https://developer.konghq.com/plugins/hmac-auth/)
- [HMAC Auth configuration reference](https://developer.konghq.com/plugins/hmac-auth/reference/)
- [HMAC Auth changelog](https://developer.konghq.com/plugins/hmac-auth/changelog/)
- [Consumer entity](https://developer.konghq.com/gateway/entities/consumer/)
- [ACL plugin](https://developer.konghq.com/plugins/acl/)
