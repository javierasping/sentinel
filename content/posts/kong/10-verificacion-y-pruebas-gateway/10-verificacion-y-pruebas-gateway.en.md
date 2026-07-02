---
title: "Gateway Verification and Testing"
date: 2026-07-02T14:45:00+00:00
description: "Methodologies for validating the correct operation of Kong Gateway through the Admin API, the Kong Manager, and real traffic tests."
tags: [Kong, Testing, Validation, API Gateway]
hero: images/kong/10-verificacion/hero.png
---

The final step after any installation and configuration is validation. It's not enough that containers are in `Running` state. We must ensure traffic flows correctly and the control plane is synchronized with the data plane.

## Verification Methods

There are three main ways to validate that Kong Gateway is operating as expected.

### 1. Validation via Admin API

The Admin API is the technical source of truth. We can verify node health and active configuration via HTTP requests:
- **Node Status:** Check the `/status` endpoint for Kong version and DB connection.
- **Route Inspection:** Verify that created routes are correctly associated with services via `GET /routes`.

### 2. Visual Validation with Kong Manager

For those who prefer a graphical interface, the **Kong Manager** offers a consolidated view of the system state:
- **Dashboard:** Allows viewing the general health of the Gateway.
- **Workspace:** We can navigate through services and routes to confirm that API changes are reflected visually.
- **Error Logs:** Useful for diagnosing backend connection issues in real-time.

### 3. Real Traffic Tests (End-to-End)

The ultimate test is making a request through the Proxy. If we've correctly configured a service and route, the test would be:

```bash
curl -i http://localhost:8000/mockbin
```

**What should we analyze in the response?**
- **HTTP 200 OK:** Indicates that the Gateway received the request, found the route, and the backend responded correctly.
- **X-Kong Headers:** Kong adds headers like `X-Kong-Request-ID` and `Via`, confirming that the request has been processed by the Gateway.
- **HTTP 404 Not Found:** If we receive this error with the message `"no Route matched with those values"`, it means the Gateway is alive, but the requested route does not exist or is misconfigured.

## Final Quality Checklist

Before going to production, ensure these points are met:
- [ ] The Control Plane can communicate with the Data Planes.
- [ ] The Enterprise license has been applied and validated.
- [ ] The Proxy ports are open to external traffic.
- [ ] The Admin API is restricted and not publicly accessible.
- [ ] SSL certificates are correctly installed and not expired.

---

**Previous article:** [First Steps: Services and Routes](/posts/kong/09-servicios-y-rutas-basicos)  
**Summary of the series:** You have completed the installation and basic configuration guide for Kong Gateway. Now you are ready to explore the implementation of advanced Plugins.
