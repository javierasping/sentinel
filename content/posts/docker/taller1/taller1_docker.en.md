---
title: "Workshop 1: Storage and Networks in Docker"
date: 2024-03-14T10:00:00+00:00
description: "Workshop 1: Storage and Networks in Docker"
tags: [Docker, Kubernetes, Contenedores]
hero: images/docker/taller1.png
---

## Workshop 1: Storage and Networks in Docker

### Storage

Let's work with Docker volumes:

1. Create a Docker volume called "miweb":

    ```bash
    docker volume create miweb
    ```

2. Create a container from the image `php:7.4-apache`, mounting the Docker volume in `/var/www/html` (the _DocumentRoot_ of the server):

    ```bash
    docker run -d --name my-apache-app -v miweb:/var/www/html -p 8080:80 php:7.4-apache
    ```

3. Use the `docker cp` command to copy an `index.html` file (with your name) into `/var/www/html`:

    ```bash
    echo "<h1>Javier Cruces</h1>" > index.html
    docker cp index.html my-apache-app:/var/www/html/
    ```

4. Access the container from the browser to check the `index.html` file:

    ```bash
    curl http://localhost:8080
    ```

    Output:
    ```html
    <h1>Javier Cruces</h1>
    ```

5. Delete the container:

    ```bash
    docker rm -f my-apache-app
    ```

6. Create a new container and mount the same volume:

    ```bash
    docker run -d --name Taller1 -v miweb:/var/www/html -p 8080:80 php:7.4-apache
    ```

7. Access the container again to verify the file is still there:

    ```bash
    curl http://localhost:8080
    ```

    Output:
    ```html
    <h1>Javier Cruces</h1>
    ```

### Bind Mount

1. Create a directory on your host and copy `index.html` into it:

    ```bash
    mkdir taller1
    cp index.html taller1/
    ```

2. Create a container from `php:7.4-apache`, mounting the directory via bind mount:

    ```bash
    docker run -d --name Taller1 -v $(pwd)/taller1:/var/www/html -p 8080:80 php:7.4-apache
    ```

3. Access the container from the browser to verify the file:

    ```bash
    curl http://localhost:8080
    ```

    Output:
    ```html
    <h1>Javier Cruces</h1>
    ```

4. Modify the `index.html` file on your host and check if the content updates in the container:

    ```bash
    echo "<h1>Javier Cruces Doval</h1>" > taller1/index.html
    curl http://localhost:8080
    ```

    Output:
    ```html
    <h1>Javier Cruces Doval</h1>
    ```

5. Delete the container:

    ```bash
    docker rm -f Taller1
    ```

6. Create a new container and mount the same directory:

    ```bash
    docker run -d --name Taller1 -v $(pwd)/taller1:/var/www/html -p 8080:80 php:7.4-apache
    ```

7. Verify the content again:

    ```bash
    curl http://localhost:8080
    ```

    Output:
    ```html
    <h1>Javier Cruces Doval</h1>
    ```

### Networks

#### Nextcloud + MariaDB Deployment

We are going to deploy the Nextcloud application with a database (**NOTE: Use the image `mariadb:10.5` to avoid issues**). You can use the [WordPress deployment guide](https://fp.josedomingo.org/iaw/4_docker/wordpress.html) as reference.

1. Create a bridge-type network:

    ```bash
    docker network create taller1
    ```

2. Create the database container connected to the network. Configure it to create a database and a user, and ensure data persistence using volumes:

    ```bash
    docker run -d --name wp_db \
        --network taller1 \
        -v db_vol:/var/lib/mysql \
        -e MYSQL_ROOT_PASSWORD=wordpress \
        -e MYSQL_DATABASE=wordpress \
        -e MYSQL_USER=wordpress \
        -e MYSQL_PASSWORD=wordpress \
        mariadb:10.5
    ```

3. Create a Nextcloud container connected to the same network, using appropriate environment variables for database connection and persistence:

    ```bash
    docker run -d --name nextcloud \
        --network taller1 \
        -e MYSQL_DATABASE=wordpress \
        -e MYSQL_USER=wordpress \
        -e MYSQL_PASSWORD=wordpress \
        -e MYSQL_HOST=wp_db \
        -p 8080:80 \
        nextcloud:latest
    ```

4. Access the application using a web browser at `http://localhost:8080`.

    ![](/docker/taller1/img/Pasted_image_20240119110827.png)
