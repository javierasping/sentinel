---
title: "Installing Docker Compose on Ubuntu 24"
date: 2025-03-09T10:00:00+00:00
description: Installing Docker Compose on Ubuntu 24
tags: [Docker,Kubernetes,Containers]
hero: images/docker/instalar_docker_compose.png
---

Complete guide to installing and managing Docker Compose on Linux systems.

## Installation from Repository

### For Debian/Ubuntu-based Systems

```bash
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

### For RHEL/CentOS-based Systems

```bash
sudo yum check-update
sudo yum install docker-compose-plugin
```

### For Fedora-based Systems

```bash
sudo dnf update
sudo dnf install docker-compose-plugin
```

---

## Updating the Plugin

### Update on Ubuntu/Debian

```bash
sudo apt-get update && sudo apt-get upgrade docker-compose-plugin
```

### Update on RHEL/CentOS

```bash
sudo yum update docker-compose-plugin
```

---

## Manual Installation

### Direct Download of the Binary

```bash
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.25.0/docker-compose-linux-$(uname -m) -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
```

### Global Installation (for all users)

```bash
sudo curl -SL https://github.com/docker/compose/releases/download/v2.25.0/docker-compose-linux-$(uname -m) -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
```

---