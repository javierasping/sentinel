---
title: "Installing Docker on Ubuntu 24"
date: 2025-03-09T10:00:00+00:00
description: Installing Docker on Ubuntu 24
tags: [Docker, Kubernetes, Containers]
hero: images/docker/instalar_docker.png
---

To start using Docker Engine on Ubuntu, make sure you meet the prerequisites and follow the installation steps.

## Prerequisites

### Operating System Requirements

To install Docker Engine, you need the 64-bit version of one of these Ubuntu releases:

- Ubuntu Oracular 24.10
- Ubuntu Noble 24.04 (LTS)
- Ubuntu Jammy 22.04 (LTS)
- Ubuntu Focal 20.04 (LTS)

Docker Engine for Ubuntu is compatible with x86_64 (or amd64), armhf, arm64, s390x, and ppc64le (ppc64el) architectures.

**Note**: Installation on Ubuntu-derived distributions, such as Linux Mint, is not officially supported (although it may work).

### Uninstall Older Versions

Before installing Docker Engine, you should uninstall any conflicting packages.

Your Linux distribution may provide unofficial Docker packages that could conflict with the official packages provided by Docker. You need to uninstall these packages before installing the official version of Docker Engine.

The unofficial packages to uninstall are:

- `docker.io`
- `docker-compose`
- `docker-compose-v2`
- `docker-doc`
- `podman-docker`

Additionally, Docker Engine depends on `containerd` and `runc`. Docker Engine packages these dependencies into a single package: `containerd.io`. If you have previously installed `containerd` or `runc`, uninstall them to avoid conflicts with the versions included in Docker Engine.

Run the following command to uninstall all conflicting packages:

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

`apt-get` may report that you have none of these packages installed.

Images, containers, volumes, and networks stored in `/var/lib/docker/` are not automatically removed when you uninstall Docker. If you want to start with a clean installation and remove existing data, refer to the uninstall section for Docker Engine.

## Installation Methods

You can install Docker Engine in various ways, depending on your needs:

1. Docker Engine is included with Docker Desktop for Linux. This is the easiest and fastest way to get started.
2. Set up and install Docker Engine from the Docker apt repository.
3. Install it manually and manage updates manually.
4. Use a convenience script. Only recommended for testing and development environments.

### Install Using the Apt Repository

Before installing Docker Engine for the first time on a new host machine, you need to set up the Docker apt repository. After this, you will be able to install and update Docker from the repository.

Set up the Docker apt repository:

1. Add the official Docker GPG key:
    ```bash
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    ```

2. Add the repository to the Apt sources:
    ```bash
    echo       "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu       $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" |       sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    ```

3. Install Docker packages:
    ```bash
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```

4. Verify that the installation was successful by running the hello-world image:
    ```bash
    sudo docker run hello-world
    ```

This command downloads a test image and runs it in a container. When the container runs, it prints a confirmation message and exits.

You have now correctly installed and started Docker Engine.

**Tip:**  
If you encounter errors trying to run without root, make sure to allow non-privileged users to run Docker commands. See the following steps for installation on Linux to allow this.

### Update Docker Engine

To update Docker Engine, follow step 2 of the installation instructions, choosing the new version you want to install.

### Install from a Package

If you are unable to use the Docker apt repository to install Docker Engine, you can download the `.deb` file for your version and install it manually. You will need to download a new file each time you wish to update Docker Engine.

Go to [https://download.docker.com/linux/ubuntu/dists/](https://download.docker.com/linux/ubuntu/dists/).

Select your version of Ubuntu from the list, then go to `pool/stable/` and select the applicable architecture (amd64, armhf, arm64, or s390x).

Download the following `.deb` files:

- `containerd.io_<version>_<arch>.deb`
- `docker-ce_<version>_<arch>.deb`
- `docker-ce-cli_<version>_<arch>.deb`
- `docker-buildx-plugin_<version>_<arch>.deb`
- `docker-compose-plugin_<version>_<arch>.deb`

Install the `.deb` packages:

```bash
sudo dpkg -i ./containerd.io_<version>_<arch>.deb   ./docker-ce_<version>_<arch>.deb   ./docker-ce-cli_<version>_<arch>.deb   ./docker-buildx-plugin_<version>_<arch>.deb   ./docker-compose-plugin_<version>_<arch>.deb
```

The Docker daemon will automatically start.

Verify that the installation was successful by running the hello-world image:

```bash
sudo service docker start
sudo docker run hello-world
```

You have now correctly installed and started Docker Engine.

### Install Using the Convenience Script

Docker provides a convenience script at [https://get.docker.com/](https://get.docker.com/) to install Docker in non-interactive fashion in development environments. This script is not recommended for production environments, but it is useful for creating a provisioning script tailored to your needs.

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
```

### Uninstall Docker Engine

To uninstall Docker Engine, run the following command:

```bash
sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
```

Images, containers, volumes, or custom configuration files are not automatically deleted. To remove all Docker elements, run:

```bash
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```

Remove the sources list and keys:

```bash
sudo rm /etc/apt/sources.list.d/docker.list
sudo rm /etc/apt/keyrings/docker.asc
```

You will need to remove any manually edited configuration files.

## Next Steps

### Managing Docker as a Non-root User

The Docker daemon binds to a Unix socket, not to a TCP port. By default, the root user owns the Unix socket, and other users can only access it using sudo. The Docker daemon always runs as the root user.

If you do not want to prepend the `docker` command with `sudo`, you can create a Unix group called `docker` and add users to it. When the Docker daemon starts, it creates a Unix socket accessible to members of the `docker` group. On some Linux distributions, the system automatically creates this group when installing Docker Engine using a package manager. In this case, you do not need to create the group manually.

**Warning**

The `docker` group grants root-level privileges to the user. For more details on how this affects security on your system, see [Docker Daemon Attack Surface](https://docs.docker.com/engine/security/security/).

**Note**

To run Docker without root privileges, see [Running the Docker daemon as a non-root user (Rootless mode)](https://docs.docker.com/engine/security/rootless/).

#### Create the `docker` group and add your user

##### 1. Create the `docker` group:

```bash
sudo groupadd docker
```

##### 2. Add your user to the `docker` group:

```bash
sudo usermod -aG docker $USER
```

##### 3. Log out and log back in for your group membership to be reevaluated.

If you are running Linux on a virtual machine, you may need to restart the virtual machine for the changes to take effect.

You can also run the following command to activate the changes in groups:

```bash
newgrp docker
```

##### 4. Verify that you can run Docker commands without `sudo`:

```bash
docker run hello-world
```

This command downloads a test image and runs it in a container. When the container runs, it prints a confirmation message and exits.

If you initially ran Docker CLI commands using `sudo` before adding your user to the `docker` group, you might see the following error:

```
WARNING: Error loading config file: /home/user/.docker/config.json -
stat /home/user/.docker/config.json: permission denied
```

This error indicates that the permission settings for the `~/.docker/` directory are incorrect, due to having used the `sudo` command earlier.

##### Solution

To fix this issue, delete the `~/.docker/` directory (it will be recreated automatically, but any custom settings will be lost), or change the ownership and permissions using the following commands:

```bash
sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
sudo chmod g+rwx "$HOME/.docker" -R
```

### Configure Docker to Start Automatically with systemd

Many modern Linux distributions use systemd to manage which services start when the system boots. On Debian and Ubuntu, the Docker service automatically starts on boot. To automatically start Docker and containerd on boot on other Linux distributions that use systemd, run the following commands:

```bash
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

To stop this behavior, use `disable` instead of `enable`:

```bash
sudo systemctl disable docker.service
sudo systemctl disable containerd.service
```

You can use systemd unit files to configure the Docker service at startup, for example, to add an HTTP proxy, set a different directory or partition for Docker's runtime files, or make other customizations. For an example, see [Configure the daemon to use a proxy](https://docs.docker.com/config/daemon/#http-proxy).

### Configure the Default Logging Driver

Docker provides logging drivers to collect and view log data from all containers running on a host. The default logging driver, `json-file`, writes log data to JSON-formatted files in the host's filesystem. Over time, these log files can increase in size, potentially leading to disk resource exhaustion.

To avoid issues with excessive disk usage due to log data, consider one of the following options:

- Configure the `json-file` logging driver to enable log rotation.
- Use an alternative logging driver such as the "local" logging driver, which performs log rotation by default.
- Use a logging driver that sends logs to a remote logging aggregator.