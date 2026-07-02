---
title: "Kong Installation Planning Guide"
date: 2026-07-02T14:15:00+00:00
description: "Critical factors to consider before installing Kong Gateway: resource sizing, ports, DNS, and security."
tags: [Kong, Planning, Infrastructure, Networks]
hero: images/kong/04-consideraciones/hero.png
---

Before running any installation command, it is vital to conduct a planning phase. An incorrect deployment of Kong can lead to performance bottlenecks or serious security vulnerabilities.

## Key Planning Factors

There are six main areas that must be analyzed before installing Kong Gateway.

### 1. Resource Sizing

Kong is extremely efficient, but the required hardware depends on the traffic volume. You must consider:
- **Bandwidth and Throughput:** Data volume per second.
- **Latency:** The impact of the Gateway on response time.
- **CPU and RAM:** Especially critical for the number of NGINX workers and the size of the memory cache.
- **Database Resources:** IOPS and memory for PostgreSQL.

### 2. Default Ports

It is fundamental to ensure that the necessary ports are open in the firewall and not in use by other services:

- **Proxy Ports (8000/8443):** Where client traffic enters.
- **Admin API (8001/8444):** For Gateway management (must be strictly protected).
- **Kong Manager (GUI) (8002/8445):** Graphical administration interface.
- **Dev Portal (HTTP/HTTPS) (8003/8444):** Portal for developers.

### 3. DNS Considerations

Correct name resolution is critical for the operation of the UI and Portal:
- **Hostnames:** Define clear names for the Manager and Admin API.
- **CORS:** Correctly configure Cross-Origin Resource Sharing so the UI can communicate with the API from different domains.
- **Cookie Management:** Ensure that domains allow cookie handling for user sessions.

### 4. Network and Firewall

- **Proxying TCP/TLS:** Define if traffic will be transparent or if Kong should terminate the SSL connection.
- **Port Opening:** Configure rules to allow client access to the Proxy port, but restrict Admin API access to administrators only.

### 5. Security and Certificates

This is the most sensitive point. You must plan:
- **Data Encryption:** Management of RSA keys and TLS certificates.
- **Secrets:** Integration with tools like HashiCorp Vault to avoid storing passwords in plain text.
- **RBAC:** Configure Role-Based Access Control (`enforce_rbac`) to limit who can make changes to the Gateway.

### 6. Licensing

For Enterprise versions, it is necessary to plan the deployment of the license file and monitor its expiration date to avoid service interruption.

---

**Previous article:** [Kong Deployment Topologies](/posts/kong/03-topologias-despliegue-kong)  
**Next article:** [Kong Gateway Configuration Management](/posts/kong/05-configuracion-kong-gateway)
