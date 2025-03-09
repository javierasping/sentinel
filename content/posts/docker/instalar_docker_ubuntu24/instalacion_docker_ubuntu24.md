---
title: "Instalación de Docker en Ubuntu 24"
date: 2025-03-09T10:00:00+00:00
description: Instalación de Docker en Ubuntu 24
tags: [Docker,Kubernetes,Contenedores]
hero: images/docker/instalar_docker.png
---

Para comenzar con Docker Engine en Ubuntu, asegúrate de cumplir con los requisitos previos y sigue los pasos de instalación.

## Requisitos Previos

### Requisitos del Sistema Operativo

Para instalar Docker Engine, necesitas la versión de 64 bits de una de estas versiones de Ubuntu:

- Ubuntu Oracular 24.10
- Ubuntu Noble 24.04 (LTS)
- Ubuntu Jammy 22.04 (LTS)
- Ubuntu Focal 20.04 (LTS)

Docker Engine para Ubuntu es compatible con arquitecturas x86_64 (o amd64), armhf, arm64, s390x y ppc64le (ppc64el).

**Nota**: La instalación en distribuciones derivadas de Ubuntu, como Linux Mint, no está oficialmente soportada (aunque puede funcionar).

### Desinstalar versiones antiguas

Antes de instalar Docker Engine, debes desinstalar cualquier paquete conflictivo.

Tu distribución de Linux puede proporcionar paquetes no oficiales de Docker, que pueden entrar en conflicto con los paquetes oficiales proporcionados por Docker. Debes desinstalar estos paquetes antes de instalar la versión oficial de Docker Engine.

Los paquetes no oficiales a desinstalar son:

- `docker.io`
- `docker-compose`
- `docker-compose-v2`
- `docker-doc`
- `podman-docker`

Además, Docker Engine depende de `containerd` y `runc`. Docker Engine agrupa estas dependencias en un solo paquete: `containerd.io`. Si has instalado `containerd` o `runc` anteriormente, desinstálalos para evitar conflictos con las versiones incluidas en Docker Engine.

Ejecuta el siguiente comando para desinstalar todos los paquetes conflictivos:

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

`apt-get` podría informar que no tienes ninguno de estos paquetes instalados.

Las imágenes, contenedores, volúmenes y redes almacenados en `/var/lib/docker/` no se eliminan automáticamente cuando desinstalas Docker. Si deseas empezar con una instalación limpia y limpiar los datos existentes, consulta la sección de desinstalación de Docker Engine.

## Métodos de Instalación

Puedes instalar Docker Engine de diferentes maneras, dependiendo de tus necesidades:

1. Docker Engine viene incluido con Docker Desktop para Linux. Esta es la forma más fácil y rápida de comenzar.
2. Configura e instala Docker Engine desde el repositorio de apt de Docker.
3. Instálalo manualmente y gestiona las actualizaciones manualmente.
4. Usa un script de conveniencia. Solo recomendado para entornos de prueba y desarrollo.

### Instalar usando el repositorio de apt

Antes de instalar Docker Engine por primera vez en una nueva máquina host, necesitas configurar el repositorio de Docker apt. Después, podrás instalar y actualizar Docker desde el repositorio.

Configura el repositorio de apt de Docker:

1. Agrega la clave GPG oficial de Docker:
    ```bash
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    ```

2. Agrega el repositorio a las fuentes de Apt:
    ```bash
    echo       "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu       $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" |       sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    ```

3. Instala los paquetes de Docker:
    ```bash
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```

4. Verifica que la instalación fue exitosa ejecutando la imagen hello-world:
    ```bash
    sudo docker run hello-world
    ```

Este comando descarga una imagen de prueba y la ejecuta en un contenedor. Cuando el contenedor se ejecute, imprimirá un mensaje de confirmación y terminará.

Ahora has instalado y arrancado Docker Engine correctamente.

**Consejo:**  
Si tienes errores al intentar ejecutar sin root, asegúrate de permitir que usuarios no privilegiados ejecuten comandos de Docker. Consulta los pasos posteriores para la instalación en Linux para permitirlo.

### Actualizar Docker Engine

Para actualizar Docker Engine, sigue el paso 2 de las instrucciones de instalación, eligiendo la nueva versión que deseas instalar.

### Instalar desde un paquete

Si no puedes usar el repositorio apt de Docker para instalar Docker Engine, puedes descargar el archivo `.deb` para tu versión y instalarlo manualmente. Deberás descargar un nuevo archivo cada vez que desees actualizar Docker Engine.

Dirígete a [https://download.docker.com/linux/ubuntu/dists/](https://download.docker.com/linux/ubuntu/dists/).

Selecciona tu versión de Ubuntu en la lista, luego ve a `pool/stable/` y selecciona la arquitectura aplicable (amd64, armhf, arm64 o s390x).

Descarga los siguientes archivos `.deb`:

- `containerd.io_<versión>_<arch>.deb`
- `docker-ce_<versión>_<arch>.deb`
- `docker-ce-cli_<versión>_<arch>.deb`
- `docker-buildx-plugin_<versión>_<arch>.deb`
- `docker-compose-plugin_<versión>_<arch>.deb`

Instala los paquetes `.deb`:

```bash
sudo dpkg -i ./containerd.io_<versión>_<arch>.deb   ./docker-ce_<versión>_<arch>.deb   ./docker-ce-cli_<versión>_<arch>.deb   ./docker-buildx-plugin_<versión>_<arch>.deb   ./docker-compose-plugin_<versión>_<arch>.deb
```

El demonio de Docker se iniciará automáticamente.

Verifica que la instalación fue exitosa ejecutando la imagen hello-world:

```bash
sudo service docker start
sudo docker run hello-world
```

Ahora has instalado y arrancado Docker Engine correctamente.

### Instalar utilizando el script de conveniencia

Docker proporciona un script de conveniencia en [https://get.docker.com/](https://get.docker.com/) para instalar Docker en entornos de desarrollo de manera no interactiva. No se recomienda este script para entornos de producción, pero es útil para crear un script de provisión adaptado a tus necesidades.

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
```

### Desinstalar Docker Engine

Para desinstalar Docker Engine, ejecuta el siguiente comando:

```bash
sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
```

Las imágenes, contenedores, volúmenes o archivos de configuración personalizados no se eliminan automáticamente. Para eliminar todos los elementos de Docker, ejecuta:

```bash
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```

Elimina la lista de fuentes y las claves:

```bash
sudo rm /etc/apt/sources.list.d/docker.list
sudo rm /etc/apt/keyrings/docker.asc
```

Deberás eliminar cualquier archivo de configuración editado manualmente.

## Próximos pasos


### Administrar Docker como un usuario no root

El demonio de Docker se vincula a un socket Unix, no a un puerto TCP. Por defecto, el usuario root es el que posee el socket Unix, y otros usuarios solo pueden acceder a él utilizando sudo. El demonio de Docker siempre se ejecuta como usuario root.

Si no deseas anteponer el comando `docker` con `sudo`, puedes crear un grupo Unix llamado `docker` y agregar usuarios a él. Cuando el demonio de Docker se inicia, crea un socket Unix accesible para los miembros del grupo `docker`. En algunas distribuciones de Linux, el sistema crea automáticamente este grupo al instalar Docker Engine utilizando un gestor de paquetes. En ese caso, no es necesario que crees el grupo manualmente.

**Advertencia**

El grupo `docker` otorga privilegios a nivel root al usuario. Para obtener más detalles sobre cómo esto afecta la seguridad en tu sistema, consulta [Docker Daemon Attack Surface](https://docs.docker.com/engine/security/security/).

**Nota**

Para ejecutar Docker sin privilegios de root, consulta [Ejecutar el demonio de Docker como un usuario no root (modo Rootless)](https://docs.docker.com/engine/security/rootless/).

#### Crear el grupo `docker` y agregar tu usuario

##### 1. Crear el grupo `docker`:

```bash
sudo groupadd docker
```

##### 2. Agregar tu usuario al grupo `docker`:

```bash
sudo usermod -aG docker $USER
```

##### 3. Cerrar sesión y volver a iniciar sesión para que se reevalúe tu membresía en el grupo.

Si estás ejecutando Linux en una máquina virtual, puede ser necesario reiniciar la máquina virtual para que los cambios tengan efecto.

También puedes ejecutar el siguiente comando para activar los cambios en los grupos:

```bash
newgrp docker
```

##### 4. Verificar que puedes ejecutar los comandos de Docker sin `sudo`:

```bash
docker run hello-world
```

Este comando descarga una imagen de prueba y la ejecuta en un contenedor. Cuando el contenedor se ejecuta, imprime un mensaje de confirmación y termina.

Si inicialmente ejecutaste los comandos de Docker CLI utilizando `sudo` antes de agregar a tu usuario al grupo `docker`, podrías ver el siguiente error:

```
WARNING: Error loading config file: /home/user/.docker/config.json -
stat /home/user/.docker/config.json: permission denied
```

Este error indica que la configuración de permisos para el directorio `~/.docker/` es incorrecta, debido a que usaste el comando `sudo` anteriormente.

##### Solución

Para solucionar este problema, elimina el directorio `~/.docker/` (se recreará automáticamente, pero se perderán las configuraciones personalizadas), o cambia la propiedad y los permisos utilizando los siguientes comandos:

```bash
sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
sudo chmod g+rwx "$HOME/.docker" -R
```

### Configurar Docker para que se inicie automáticamente con systemd

Muchas distribuciones modernas de Linux utilizan systemd para gestionar qué servicios se inician cuando el sistema arranca. En Debian y Ubuntu, el servicio de Docker se inicia automáticamente al arranque. Para iniciar automáticamente Docker y containerd al arrancar en otras distribuciones de Linux que usan systemd, ejecuta los siguientes comandos:

```bash
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

Para detener este comportamiento, utiliza `disable` en lugar de `enable`:

```bash
sudo systemctl disable docker.service
sudo systemctl disable containerd.service
```

Puedes utilizar archivos de unidad de systemd para configurar el servicio de Docker al inicio, por ejemplo, para agregar un proxy HTTP, establecer un directorio o partición diferente para los archivos de ejecución de Docker, o realizar otras personalizaciones. Para obtener un ejemplo, consulta [Configurar el demonio para usar un proxy](https://docs.docker.com/config/daemon/#http-proxy).

### Configurar el controlador de registro predeterminado

Docker proporciona controladores de registro para recopilar y ver datos de registro de todos los contenedores que se ejecutan en un host. El controlador de registro predeterminado, `json-file`, escribe los datos de registro en archivos con formato JSON en el sistema de archivos del host. Con el tiempo, estos archivos de registro aumentan de tamaño, lo que podría llevar al agotamiento de los recursos del disco.

Para evitar problemas con el uso excesivo del disco debido a los datos de registro, considera una de las siguientes opciones:

- Configura el controlador de registro `json-file` para activar la rotación de registros.
- Utiliza un controlador de registro alternativo como el controlador de registro "local", que realiza rotación de registros de manera predeterminada.
- Utiliza un controlador de registro que envíe los registros a un agregador de registros remoto.