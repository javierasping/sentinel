---
title: "Lab: Installing Kong in Traditional Mode"
date: 2026-07-02T14:30:00+00:00
description: "How to apply and manage the license file in Kong Gateway Enterprise to enable advanced features."
tags: [Kong, Enterprise, Licenses, Administration]
hero: images/kong/07-licencias/hero.png
weight: 3
---

Kong Gateway Enterprise offers advanced security, governance, and support features that require the application of a valid license. There are several ways to introduce this license into the system, depending on the preferred agility and deployment method.

## License Application Methods

Kong evaluates the license following a specific order of priority. If it finds a license in the first method, it will ignore the subsequent ones.

### 1. Environment Variable (`KONG_LICENSE_DATA`)
The fastest method for ephemeral or automated deployments. It consists of passing the content of the license file directly as the value of the `KONG_LICENSE_DATA` environment variable.

### 2. Default Location (`/etc/kong/license.json`)
Kong automatically looks for a file called `license.json` in the `/etc/kong/` directory. This is the standard method for installations on physical servers or virtual machines.

### 3. Custom Path (`KONG_LICENSE_PATH`)
If the license file is in a non-standard path, the exact location can be specified via the `KONG_LICENSE_PATH` environment variable.

### 4. Admin API (Dynamic Method)
The most flexible method, as it allows applying the license **without restarting the service**. This is done via a POST request to the license endpoint:

```bash
curl -X POST http://localhost:8001/licenses \
  -F "payload=@/path/to/file/license.json"
```

> **Important in Hybrid Mode:** When the license is applied to the **Control Plane** via the API, it is automatically distributed to all connected **Data Planes** in real-time.

## License Verification

To check that the license has been correctly applied and to know its status (expiration date, Kong version, etc.), the report endpoint can be used:

```bash
curl http://localhost:8001/license/report
```

The JSON response will detail the license version, expiration date, and the number of connected Data Planes.

If you prefer visual management, you can open the **Kong Manager**, where the 'License not applied' warning will disappear once the system validates the file.

---

**Previous article:** [Lab: Installing Kong with Docker (Hybrid Mode)](/en/posts/kong/02-instalacion-docker-hibrido/02-instalacion-docker-hibrido/)  
**Next article:** [Lab: Installing Kong in DB-less Mode](/en/posts/kong/04-instalacion-db-less/04-instalacion-db-less/)
