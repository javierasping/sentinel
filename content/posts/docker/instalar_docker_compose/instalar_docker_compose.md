---
title: "Instalación de Docker Compose en Ubuntu 24"
date: 2025-03-09T10:00:00+00:00
description: Instalación de Docker Compose en Ubuntu 24
tags: [Docker,Kubernetes,Contenedores]
hero: images/docker/instalar_docker_compose.png
---

Guía completa para instalar y gestionar Docker Compose en sistemas Linux.

## Instalación desde repositorio

### Para sistemas basados en Debian/Ubuntu

```bash
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

### Para sistemas basados en RHEL/CentOS

```bash
sudo yum check-update
sudo yum install docker-compose-plugin
```

### Para sistemas basados en Fedora

```bash
sudo dnf update
sudo dnf install docker-compose-plugin
```

---

## Actualización del complemento

### Actualizar en Ubuntu/Debian

```bash
sudo apt-get update && sudo apt-get upgrade docker-compose-plugin
```

### Actualizar en RHEL/CentOS

```bash
sudo yum update docker-compose-plugin
```

---

## Instalación manual

### Descarga directa del binario

```bash
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.25.0/docker-compose-linux-$(uname -m) -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
```

### Instalación global (todos los usuarios)

```bash
sudo curl -SL https://github.com/docker/compose/releases/download/v2.25.0/docker-compose-linux-$(uname -m) -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
```

---