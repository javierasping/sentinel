---
title: "Workshop 1: Storage and networks in Docker"
date: 2024-03-14T10:00:00+00:00
Description: Workshop 1 Storage and networks in Docker
tags: [Docker,Kubernetes,Contenedores]
hero: images/docker/taller1.png

---
## Workshop 1: Storage and networks in Docker

### Storage

Let's work with docker volumes:

1. It creates a docker volume called "miweb."

```bash
javiercruces@docker:~$ docker volume create miweb
miweb
```

2. Create a container from the image 'php: 7.4-apache' where you mount in the directory '/ var / www / html' (which we know is the _ DocumentRoot _ of the server that offers us that image) the docker volume you created.

```bash
javiercruces@docker:~$ docker run -d --name my-apache-app -v miweb:/var/www/html -p 8080:80 php:7.4-apache
```

3. Use the 'docker cp' command to copy a 'index.html' file (where your name appears) in the '/ var / www / html' directory.

```bash
javiercruces@docker:~$ echo "<h1>Javier Cruces</h1>" > index.html
javiercruces@docker:~$ docker cp index.html my-apache-app:/var/www/html/
Successfully copied 2.05kB to my-apache-app:/var/www/html/
```

4. Access the container from the browser to see the information offered by the 'index.html' file.

```bash
javiercruces@docker:~$ curl http://localhost:8080
<h1>Javier Cruces</h1>
```

5. Delete the container

```bash
javiercruces@docker:~$ docker rm -f my-apache-app
my-apache-app
```

6. Create a new container and mount the same volume as in the previous exercise.

```bash
javiercruces@docker:~$ docker run -d --name Taller1 -v miweb:/var/www/html -p 8080:80 php:7.4-apache
9edd4b2dd2499f923090ce6a246e44db136f162528a51f84ddb33659503bafd7
```

7. Access the container from the browser to see the information offered by the 'index.html' file. Was that file still in place?

```bash
javiercruces@docker:~$ curl http://localhost:8080
<h1>Javier Cruces</h1>
```

Let's work with bind mount:

1. Create a directory in your host and inside create a 'index.html' file (where your name appears).

```bash
javiercruces@docker:~$ mkdir taller1
javiercruces@docker:~$ cp index.html taller1/
```

2. It creates a container from the image 'php: 7.4-apache' where you mount in the directory '/ var / www / html' the directory you created by means of 'bind mount'.

```bash
javiercruces@docker:~$ docker run -d --name Taller1 -v /home/javiercruces/taller1/:/var/www/html -p 8080:80 php:7.4-apache
```

3. Access the container from the browser to see the information offered by the 'index.html' file.

```bash
javiercruces@docker:~$ curl http://localhost:8080
<h1>Javier Cruces</h1>
```

4. Modify the content of the 'index.html' file in your host and check that when refreshing the page offered by the container, the content has changed.

```bash
javiercruces@docker:~$ echo "<h1>Javier Cruces Doval</h1>" > taller1/index.html
javiercruces@docker:~$ curl http://localhost:8080
<h1>Javier Cruces Doval</h1>

```

5. Delete the container

```bash
javiercruces@docker:~$ docker rm -f Taller1
Taller1
```

6. Create a new container and set up the same directory as in the previous exercise.

```bash
javiercruces@docker:~$ docker run -d --name Taller1 -v /home/javiercruces/taller1/:/var/www/html -p 8080:80 php:7.4-apache
```

7. Access the container from the browser to see the information offered by the 'index.html' file. Do you still see the same content?

```bash
javiercruces@docker:~$ curl http://localhost:8080
<h1>Javier Cruces Doval</h1>
```

### Networks

### Nextcloud + mariadb deployment

We are going to deploy the Nextcloud application with a database (* * NOTE: To keep you from error use the image 'mariadb: 10.5' * *). It can serve you the exercise we have done to deploy [WordPress] (https: / / fp.josedomingo.org / iaw / 4 _ docker / wordpress.html). The following steps are taken:

1. It creates a bridge-type network.

```bash
javiercruces@docker:~$ docker network create taller1          
a1f8faf5a100ad01013bc147e7c2a9577a5a4376d7e33c7d961c5aaca93000b0

```

2. Create the database container connected to the network you created. The database must be configured to create a database and a user. The container must also use storage (volumes or bind mount) to save the information. You can follow the documentation of [mariadb] (https: / / hub.docker.com / _ / mariadb) or [PostgreSQL] (https: / / hub.docker.com / _ / postgres).

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

3. Then, following the image documentation [Nextcloud] (https: / / hub.docker.com / _ / nextcloud), create a container connected to the same network, and indicate the appropriate variables to be properly configured and connected to the database. The container must also be persistent using storage.

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

4. Access the application using a web browser.

```bash

```

![](../img/Pasted_image_20240119110827.png)