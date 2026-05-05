---
title: "Instalación de Prometheus con docker-compose y Node Exporter en Debian 12"
date: 2025-04-17T10:00:00+00:00
description: Guía paso a paso para la instalación de Prometheus con Docker Compose y Node Exporter en Debian 12.
tags: [Métricas,Prometheus,Observabilidad]
hero: /images/observabilidad/metricas/prometheus/prometheus_docker_compose.png
---

Esta guía es un tutorial introductorio que muestra cómo instalar, configurar y utilizar una instancia básica de Prometheus mediante Docker Compose. Además, se configurará un equipo con Linux (en este caso Debian 12) para que exponga sus métricas del sistema, las cuales serán recolectadas por Prometheus mediante el uso de Node Exporter.

## Requisitos previos

- Tener instalado Docker y Docker compose
- Tener un equipo Linux con el que cuentes con permisos de administrador 

## Creación de ficheros

### Creación del docker-compose

Todos los ficheros utilizados en este post los podrás encontrar en mi [github](https://github.com/javierasping/learn_observability) . 

Lo primero que haremos será crear nuestro archivo `docker-compose.yaml`.

En este archivo destacaremos dos puntos:

- El puerto de Prometheus es el 9090; en mi caso, lo mantendré sin cambios.
- El archivo de configuración que añadiremos al contenedor, lo cual facilitará la modificación de su configuración.

```bash
javiercruces@HPOMEN15:~/learn_observability/exercise1$ cat docker-compose.yaml 
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

```

### Creación del archivo `prometheus.yml`

El archivo `prometheus.yml` es el principal fichero de configuración de Prometheus. En él definimos tanto los parámetros globales como los targets desde los que Prometheus recogerá las métricas. También se pueden configurar etiquetas y personalizar la frecuencia de muestreo.

Utilizando el ejemplo de la página [Getting Started](https://prometheus.io/docs/prometheus/latest/getting_started/) de Prometheus, añadiremos nuestra máquina Debian 12. Dado que Prometheus se ejecuta en Docker, he utilizado la IP de la puerta de enlace de la red para referenciar mi máquina física Debian 12.

Para más detalles sobre todas las opciones disponibles, consulta la [documentación oficial de Prometheus](https://prometheus.io/docs/prometheus/latest/configuration/configuration/).



```yaml
global:
  scrape_interval: 15s  

  external_labels:
    monitor: 'javiercd-metrics'

# En esta sección configuraremos todos los targets de los cual vamos a extraer métricas
scrape_configs:
    # Scrape del propio Prometheus
  - job_name: 'prometheus'        
    scrape_interval: 5s           
    static_configs:
      - targets: ['localhost:9090']
    
    # Monitorización del sistema Debian 12
  - job_name: 'node-exporter-debian12' 
    scrape_interval: 5s
    static_configs:
      - targets: ['172.17.0.1:9100']

```

## Configuración del Node Exporter en Debian 12

Para permitir que Prometheus recoja métricas del sistema operativo, instalaremos **Node Exporter**, un servicio encargado de extraer las métricas del sistema para que Prometheus pueda recolectarlas (scrapearlas).

### Instalación del paquete

Ejecuta el siguiente comando para instalar `prometheus-node-exporter` desde los repositorios de Debian:

```bash
javiercruces@HPOMEN15:~/learn_observability/exercise1$ sudo apt install prometheus-node-exporter
```

### Verificación del servicio

Una vez instalado, el demonio se ejecutará automáticamente en el sistema, pero puedes utilizar el siguiente comando para confirmarlo:

```bash
javiercruces@HPOMEN15:~/learn_observability/exercise1$ sudo systemctl is-enabled prometheus-node-exporter
enabled
```

También puedes comprobarlo y obtener más información con el siguiente comando:

Salida esperada (resumida):

```bash
javiercruces@HPOMEN15:~/learn_observability/exercise1$ sudo systemctl status prometheus-node-exporter
● prometheus-node-exporter.service - Prometheus exporter for machine metrics
     Loaded: loaded (/lib/systemd/system/prometheus-node-exporter.service; enabled; preset: enabled)
     Active: active (running) since Sat 2025-05-17 01:59:00 CEST; 1min 10s ago
       Docs: https://github.com/prometheus/node_exporter
   Main PID: 8488 (prometheus-node)
      Tasks: 6 (limit: 18302)
     Memory: 3.7M
        CPU: 6ms
     CGroup: /system.slice/prometheus-node-exporter.service
             └─8488 /usr/bin/prometheus-node-exporter

may 17 01:59:00 HPOMEN15 prometheus-node-exporter[8488]: ts=2025-05-16T23:59:00.893Z caller=node_exporter.go:117 level=info collector=thermal_zone
may 17 01:59:00 HPOMEN15 prometheus-node-exporter[8488]: ts=2025-05-16T23:59:00.893Z caller=node_exporter.go:117 level=info collector=time
may 17 01:59:00 HPOMEN15 prometheus-node-exporter[8488]: ts=2025-05-16T23:59:00.893Z caller=node_exporter.go:117 level=info collector=timex
may 17 01:59:00 HPOMEN15 prometheus-node-exporter[8488]: ts=2025-05-16T23:59:00.893Z caller=node_exporter.go:117 level=info collector=udp_queues
may 17 01:59:00 HPOMEN15 prometheus-node-exporter[8488]: ts=2025-05-16T23:59:00.893Z caller=node_exporter.go:117 level=info collector=uname
may 17 01:59:00 HPOMEN15 prometheus-node-exporter[8488]: ts=2025-05-16T23:59:00.893Z caller=node_exporter.go:117 level=info collector=vmstat
may 17 01:59:00 HPOMEN15 prometheus-node-exporter[8488]: ts=2025-05-16T23:59:00.893Z caller=node_exporter.go:117 level=info collector=xfs
may 17 01:59:00 HPOMEN15 prometheus-node-exporter[8488]: ts=2025-05-16T23:59:00.893Z caller=node_exporter.go:117 level=info collector=zfs
may 17 01:59:00 HPOMEN15 prometheus-node-exporter[8488]: ts=2025-05-16T23:59:00.893Z caller=tls_config.go:232 level=info msg="Listening on" address=[::]:9100
may 17 01:59:00 HPOMEN15 prometheus-node-exporter[8488]: ts=2025-05-16T23:59:00.893Z caller=tls_config.go:235 level=info msg="TLS is disabled." http2=false address=[::]:9100
```

Si observas las dos últimas líneas, verás que el servicio está escuchando en el puerto 9100.
Como información adicional, la ruta de la unidad de systemd se encuentra en `/lib/systemd/system/prometheus-node-exporter.service` y la configuración de Node Exporter en `/etc/default/prometheus-node-exporter`.

## Levantamos el escenario

Una vez preparado el archivo de configuración de Prometheus y con Node Exporter funcionando, levantaremos Prometheus:

```bash
javiercruces@HPOMEN15:~/learn_observability/exercise1$ docker compose up -d
```

Una vez levantado, accederemos a través del navegador al puerto expuesto de Prometheus (en mi caso, el 9090):

![](/observabilidad/metricas/prometheus/acceso_prometheus.png)

Comprobaremos que Prometheus recibe las métricas de Debian 12 accediendo a `http://localhost:9090/targets`; en mi caso, ambos servicios están activos y recibiendo métricas:

![](/observabilidad/metricas/prometheus/targets_prometheus.png)

Por último, consultaremos un par de métricas:

![](/observabilidad/metricas/prometheus/network_metric.png)

![](/observabilidad/metricas/prometheus/memory_metric.png)

## Bibliografia 

- [Getting started Prometheus](https://prometheus.io/docs/prometheus/latest/getting_started/)
- [Prometheus configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)
- [DockerHub Prometheus](https://hub.docker.com/r/prom/prometheus)
- [Node-exporter](https://prometheus.io/docs/guides/node-exporter/)
