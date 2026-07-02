---
title: "Kong Gateway Configuration Management"
date: 2026-07-02T14:20:00+00:00
description: "How to manage Kong configuration parameters via files, environment variables, and adjustment categories."
tags: [Kong, Configuration, DevOps, SysAdmin]
hero: images/kong/05-configuracion/hero.png
---

Kong Gateway offers a huge amount of configuration parameters that allow adjusting everything from proxy behavior to control plane security. Depending on the deployment method, the way to apply these changes varies.

## Configuration Methods

There are three main ways to inject configuration into Kong:

### 1. Configuration Files (`.conf` or `.yaml`)

This is the traditional method. The file varies by platform:
- **Bare Metal or VM:** The `/etc/kong/kong.conf` file is used.
- **Docker:** Defined through the `docker-compose.yaml` file.
- **Kubernetes:** Managed via Helm values files (`values.yaml`).

### 2. Environment Variables

This is the most common and recommended way in modern environments (containers). Any configuration property can be overwritten via an environment variable following this rule:
**Property Name $\rightarrow$ UPPERCASE and `KONG_` prefix**

*Examples:*
- `proxy_error_log` $\rightarrow$ `KONG_PROXY_ERROR_LOG`
- `admin_gui_api_url` $\rightarrow$ `KONG_ADMIN_GUI_API_URL`

### 3. Administration API

Some parameters can be modified in real-time via the Admin API without needing to restart the service.

---

## Parameter Categories

To facilitate administration, configuration parameters are grouped into categories:

### General Settings
Include log levels (`log_levels`) and the list of plugins to be loaded upon Gateway startup.

### Hybrid Mode
Specific configurations for communication between the Control Plane and the Data Plane, including mTLS certificates (`cluster_cert` and `cluster_cert_keys`).

### NGINX Settings
Since Kong is built on NGINX, it allows adjusting: SSL ciphers and protocols, TCP timeouts, and HTTP directories.

### Database and DNS
TTL (Time to Live), cache, and PostgreSQL connection parameters.

### Kong Manager
Specific URLs and ports for the graphical interface.

---

**Previous article:** [Installation Planning Guide](/posts/kong/04-consideraciones-instalacion-kong)  
**Next article:** [Lab: Installation with Docker (Hybrid Mode)](/posts/kong/06-instalacion-docker-hibrido)
