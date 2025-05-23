---
title: "Taller 2: Escenarios multicontenedor en Docker"
date: 2024-03-14T10:00:00+00:00
description: Taller 2 Escenarios multicontenedor en Docker
tags: [Docker,Kubernetes,Contenedores]
hero: images/docker/taller2.png

---
##  Taller 2: Escenarios multicontenedor en Docker
###  Despliegue de Nextcloud

Vamos a desplegar la aplicación nextcloud con una base de datos (puedes elegir mariadb o PostgreSQL) utilizando la aplicación docker-compose. Puedes coger cómo modelo el fichero `docker-compose.yml` el que hemos estudiado para desplegar WordPress.

1. Instala docker-compose en tu ordenador.

```bash

```

2. Dentro de un directorio crea un fichero `docker-compose.yml` para realizar el despliegue de nextcloud con una base de datos. Recuerda las variables de entorno y la persistencia de información.

```bash
javiercruces@docker:~/taller2$ cat docker-compose.yaml 
version: '2'

volumes:
  nextcloud:
  db:

services:
  db:
    image: mariadb:10.6
    restart: always
    command: --transaction-isolation=READ-COMMITTED --log-bin=binlog --binlog-format=ROW
    volumes:
      - db:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_PASSWORD=javiercruces
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud

  app:
    image: nextcloud
    restart: always
    ports:
      - 8081:80
    links:
      - db
    volumes:
      - nextcloud:/var/www/html
    environment:
      - MYSQL_PASSWORD=javiercruces
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud
      - MYSQL_HOST=db

```

3. Levanta el escenario con `docker-compose`.

```bash
javiercruces@docker:~/taller2$ docker compose up -d 
[+] Running 2/2
 ✔ Container taller2-db-1   Started                                                                0.0s 
 ✔ Container taller2-app-1  Started                                                                0.0s
```

4. Muestra los contenedores con `docker-compose`.

```bash
javiercruces@docker:~/taller2$ docker compose ps
NAME            IMAGE          COMMAND                                                                                              SERVICE   CREATED         STATUS         PORTS
taller2-app-1   nextcloud      "/entrypoint.sh apache2-foreground"                                                                  app       7 minutes ago   Up 5 minutes   0.0.0.0:8081->80/tcp, :::8081->80/tcp
taller2-db-1    mariadb:10.6   "docker-entrypoint.sh --transaction-isolation=READ-COMMITTED --log-bin=binlog --binlog-format=ROW"   db        7 minutes ago   Up 5 minutes   3306/tcp

```

5. Accede a la aplicación y comprueba que funciona.

```bash

```

![](/docker/taller2/img/Pasted_image_20240202091554.png)

6. Comprueba el almacenamiento que has definido y que se ha creado una nueva red de tipo bridge.

```bash
javiercruces@docker:~/taller2$ docker network ls
NETWORK ID     NAME              DRIVER    SCOPE
5dd43eadf03b   bridge            bridge    local
40fad2a3552b   host              host      local
9f5f2450d012   none              null      local
a1f8faf5a100   taller1           bridge    local
fcf9b3b0fed4   taller2_default   bridge    local

javiercruces@docker:~/taller2$ docker volume ls
DRIVER    VOLUME NAME
local     0dd5f1f824800210c4ce522371cb31ef1075c779566ed986b8718a88eb4b50a9
local     5d742d485cd427d22f688488a3d28f562e6e8037ecf2e56f7fb81dc6db71e26b
local     9eeb57dc83abfd57998498152b2a03527b8743ccf1eee5cba2e7ef891030e496
local     87622e5677a467c635c75f868ae123679269507fbe7f6a47b0804999a0845f01
local     d9cb1b25e8892ef2f8b51b1352a00d44451616eb0f52db43cb8d42d391b9ab1b
local     db_vol
local     miweb
local     taller2_db
local     taller2_nextcloud

```

7. Borra el escenario con `docker-compose`.

```bash
javiercruces@docker:~/taller2$ docker compose rm -sf
[+] Stopping 2/2
 ✔ Container taller2-app-1  Stopped                                                                                                                                                                           3.6s 
 ✔ Container taller2-db-1   Stopped                                                                                                                                                                           6.1s 
Going to remove taller2-app-1, taller2-db-1
[+] Removing 2/0
 ✔ Container taller2-db-1   Removed                                                                                                                                                                           0.1s 
 ✔ Container taller2-app-1  Removed               
```

