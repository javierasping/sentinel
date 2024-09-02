---
title: "Taller 1: Almacenamiento y redes en Docker"
date: 2024-03-14T10:00:00+00:00
description: Taller 1 Almacenamiento y redes en Docker
tags: [Docker,Kubernetes,Contenedores]
hero: images/ci_cd/jenkins/jenkins.png

---
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GVDYVWJLRH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GVDYVWJLRH');
</script>

##  Taller 1: Almacenamiento y redes en Docker

###  Almacenamiento

Vamos a trabajar con volúmenes docker:

1. Crea un volumen docker que se llame `miweb`.

```bash
javiercruces@docker:~$ docker volume create miweb
miweb
```

2. Crea un contenedor desde la imagen `php:7.4-apache` donde montes en el directorio `/var/www/html` (que sabemos que es el _DocumentRoot_ del servidor que nos ofrece esa imagen) el volumen docker que has creado.

```bash
javiercruces@docker:~$ docker run -d --name my-apache-app -v miweb:/var/www/html -p 8080:80 php:7.4-apache
```

3. Utiliza el comando `docker cp` para copiar un fichero `index.html` (donde aparece tu nombre) en el directorio `/var/www/html`.

```bash
javiercruces@docker:~$ echo "<h1>Javier Cruces</h1>" > index.html
javiercruces@docker:~$ docker cp index.html my-apache-app:/var/www/html/
Successfully copied 2.05kB to my-apache-app:/var/www/html/
```

4. Accede al contenedor desde el navegador para ver la información ofrecida por el fichero `index.html`.

```bash
javiercruces@docker:~$ curl http://localhost:8080
<h1>Javier Cruces</h1>
```

5. Borra el contenedor

```bash
javiercruces@docker:~$ docker rm -f my-apache-app
my-apache-app
```

6. Crea un nuevo contenedor y monta el mismo volumen como en el ejercicio anterior.

```bash
javiercruces@docker:~$ docker run -d --name Taller1 -v miweb:/var/www/html -p 8080:80 php:7.4-apache
9edd4b2dd2499f923090ce6a246e44db136f162528a51f84ddb33659503bafd7
```

7. Accede al contenedor desde el navegador para ver la información ofrecida por el fichero `index.html`. ¿Seguía existiendo ese fichero?

```bash
javiercruces@docker:~$ curl http://localhost:8080
<h1>Javier Cruces</h1>
```

Vamos a trabajar con bind mount:

1. Crea un directorio en tu host y dentro crea un fichero `index.html` (donde aparece tu nombre).

```bash
javiercruces@docker:~$ mkdir taller1
javiercruces@docker:~$ cp index.html taller1/
```

2. Crea un contenedor desde la imagen `php:7.4-apache` donde montes en el directorio `/var/www/html` el directorio que has creado por medio de `bind mount`.

```bash
javiercruces@docker:~$ docker run -d --name Taller1 -v /home/javiercruces/taller1/:/var/www/html -p 8080:80 php:7.4-apache
```

3. Accede al contenedor desde el navegador para ver la información ofrecida por el fichero `index.html`.

```bash
javiercruces@docker:~$ curl http://localhost:8080
<h1>Javier Cruces</h1>
```

4. Modifica el contenido del fichero `index.html` en tu host y comprueba que al refrescar la página ofrecida por el contenedor, el contenido ha cambiado.

```bash
javiercruces@docker:~$ echo "<h1>Javier Cruces Doval</h1>" > taller1/index.html
javiercruces@docker:~$ curl http://localhost:8080
<h1>Javier Cruces Doval</h1>

```

5. Borra el contenedor

```bash
javiercruces@docker:~$ docker rm -f Taller1
Taller1
```

6. Crea un nuevo contenedor y monta el mismo directorio como en el ejercicio anterior.

```bash
javiercruces@docker:~$ docker run -d --name Taller1 -v /home/javiercruces/taller1/:/var/www/html -p 8080:80 php:7.4-apache
```

7. Accede al contenedor desde el navegador para ver la información ofrecida por el fichero `index.html`. ¿Se sigue viendo el mismo contenido?

```bash
javiercruces@docker:~$ curl http://localhost:8080
<h1>Javier Cruces Doval</h1>
```

### Redes

#### Despliegue de Nextcloud + mariadb

Vamos a desplegar la aplicación Nextcloud con una base de datos (**NOTA: Para que no te de errores utiliza la imagen `mariadb:10.5`**). Te puede servir el ejercicio que hemos realizado para desplegar [Wordpress](https://fp.josedomingo.org/iaw/4_docker/wordpress.html). Para ello sigue los siguientes pasos:

1. Crea una red de tipo bridge.

```bash
javiercruces@docker:~$ docker network create taller1          
a1f8faf5a100ad01013bc147e7c2a9577a5a4376d7e33c7d961c5aaca93000b0

```

2. Crea el contenedor de la base de datos conectado a la red que has creado. La base de datos se debe configurar para crear una base de datos y un usuario. Además el contenedor debe utilizar almacenamiento (volúmenes o bind mount) para guardar la información. Puedes seguir la documentación de [mariadb](https://hub.docker.com/_/mariadb) o la de [PostgreSQL](https://hub.docker.com/_/postgres).

```bash
javiercruces@docker:~$ docker run -d --name wp_db \
    --network taller1 \
    -v db_vol:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=wordpress \
    -e MYSQL_DATABASE=wordpress \
    -e MYSQL_USER=wordpress \
    -e MYSQL_PASSWORD=wordpress \
    mariadb:10.5
```

3. A continuación, siguiendo la documentación de la imagen [Nextcloud](https://hub.docker.com/_/nextcloud), crea un contenedor conectado a la misma red, e indica las variables adecuadas para que se configure de forma adecuada y realice la conexión a la base de datos. El contenedor también debe ser persistente usando almacenamiento.

```bash
javiercruces@docker:~$ docker run -d --name nextcloud \
    --network taller1 \
    -e MYSQL_DATABASE=wordpress \
    -e MYSQL_USER=wordpress \
    -e MYSQL_PASSWORD=wordpress \
    -e MYSQL_HOST=wp_db \
    -p 8080:80 \
    nextcloud:latest

```

4. Accede a la aplicación usando un navegador web.

```bash

```

![](../img/Pasted_image_20240119110827.png)
