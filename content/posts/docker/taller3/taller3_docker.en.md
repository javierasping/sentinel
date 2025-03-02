---
title: "Workshop 3: Docker Imaging"
date: 2024-03-14T10:00:00+00:00
description: Workshop 3 Image creation Docker
tags: [Docker,Kubernetes,Contenedores]
hero: images/docker/taller3.png

---

## Workshop 3: Docker Image Creation

Creating an image from a Dockerfile

1.Create a static website (e.g. search for an HTML5 template). Or just create an index.htm ml.

```bash

```

2.Create a Dockerfile file to create an image with a web server by serving the page. You can use a debian or ubuntu base image, or an image that already has a web service, as we have seen in Example 1: Image construction with a static page.

```bash
javiercruces@docker:~/taller3$ cat Dockerfile 
#syntax=docker/dockerfile:1
FROM httpd:2.4
COPY ./public_html/ /usr/local/apache2/htdocs/
EXPOSE 80

```

3. Run the docker command that creates the new image. The image should be called / my _ server _ web: v1.

```bash
javiercruces@docker:~/taller3$ docker build -t javiersaping/mi_servidor_web:v1 .
Sending build context to Docker daemon  3.584kB
Step 1/3 : FROM httpd:2.4
 ---> 92fa43a2ff60
Step 2/3 : COPY ./public_html/ /usr/local/apache2/htdocs/
 ---> b03556dd59b6
Step 3/3 : EXPOSE 80
 ---> Running in 1cc04e1deee4
Removing intermediate container 1cc04e1deee4
 ---> 3078183767ef
Successfully built 3078183767ef
Successfully tagged javiersaping/mi_servidor_web:v1

javiercruces@docker:~/taller3$ docker run -d -p 8081:80 javiersaping/mi_servidor_web:v1
2a753adcd098c49b7b215b7c97267a09e09194303bee131150765222a4295dea

```

![](../img/Pasted_image_20240208085015.png)


4. Connect to Docker Hub and upload the image you just created.

```bash
javiercruces@docker:~/taller3$ docker login
javiercruces@docker:~/taller3$ docker push javiersaping/mi_servidor_web:v1
The push refers to repository [docker.io/javiersaping/mi_servidor_web]
c2a1a8df6153: Pushed 
daede99f9966: Mounted from library/httpd 
a7eff924c5ac: Mounted from library/httpd 
24282ddb8cca: Mounted from library/httpd 
5f70bf18a086: Mounted from library/httpd 
8ba5f6d45106: Mounted from library/httpd 
571ade696b26: Mounted from library/nextcloud 
v1: digest: sha256:85a8e341e3fd89b313a263a45c91ad846d673f198301e482c4f07352aef8bd42 size: 1779
```

5. Download the image to another computer where you have docker installed, and create a container from it. (If you don't have another computer with docker installed, delete the image on your computer and download it from Docker Hub).

```bash
javiercruces@docker:~/taller3$ docker image ls 
REPOSITORY                     TAG          IMAGE ID       CREATED         SIZE
javiersaping/mi_servidor_web   v1           3078183767ef   7 minutes ago   167MB
nextcloud                      latest       142b11cc42d8   3 weeks ago     1.21GB
wordpress                      latest       fe93c4b645b9   8 weeks ago     739MB
mariadb                        latest       2b54778e06a3   2 months ago    404MB
mariadb                        10.6         10fbb70b8165   2 months ago    396MB
mariadb                        10.5         72610f6b03ac   2 months ago    393MB
httpd                          2.4          92fa43a2ff60   3 months ago    167MB
php                            7.4-apache   20a3732f422b   14 months ago   453MB
javiercruces@docker:~/taller3$ docker image rm 3078183767ef
Untagged: javiersaping/mi_servidor_web:v1
Untagged: javiersaping/mi_servidor_web@sha256:85a8e341e3fd89b313a263a45c91ad846d673f198301e482c4f07352aef8bd42
Deleted: sha256:3078183767efd71fffccce7fb4e6806afa46a4cff42c37ad505d376e0b842108
Deleted: sha256:b03556dd59b6f2ab935450b4d5eb09dedfc4ee86f4c11a9140d8e17f89d89a73
Deleted: sha256:5f245addf2a19a8f2d9314dc1283ab53d0f85ae6a6a73aa5d264f070f0d71e01

javiercruces@docker:~/taller3$ docker pull javiersaping/mi_servidor_web:v1
v1: Pulling from javiersaping/mi_servidor_web
2f44b7a888fa: Already exists 
5abb3599da34: Already exists 
4f4fb700ef54: Already exists 
fa608a886227: Already exists 
afe6bbf00437: Already exists 
fd0ef2a49677: Already exists 
6d9a1035e41b: Pull complete 
Digest: sha256:85a8e341e3fd89b313a263a45c91ad846d673f198301e482c4f07352aef8bd42
Status: Downloaded newer image for javiersaping/mi_servidor_web:v1
docker.io/javiersaping/mi_servidor_web:v1

```

6.Let's make a modification of the website: make a modification to the index.html file.

```bash
javiercruces@docker:~/taller3/public_html$ echo "<h1>Taller3 FJCD V2</h1>" > index.html
```

7.Re-create a new image, in this case put a v2 tag. Get her up to Docker Hub.

```bash
javiercruces@docker:~/taller3$ docker build -t javiersaping/mi_servidor_web:v2 .
Sending build context to Docker daemon  3.584kB
Step 1/3 : FROM httpd:2.4
 ---> 92fa43a2ff60
Step 2/3 : COPY ./public_html/ /usr/local/apache2/htdocs/
 ---> 94e5c065b88a
Step 3/3 : EXPOSE 80
 ---> Running in 5849a7ba6b3b
Removing intermediate container 5849a7ba6b3b
 ---> 2e68e7708285
Successfully built 2e68e7708285
Successfully tagged javiersaping/mi_servidor_web:v2
javiercruces@docker:~/taller3$ docker push javiersaping/mi_servidor_web:v2
The push refers to repository [docker.io/javiersaping/mi_servidor_web]
1f5b52d08ce0: Pushed 
daede99f9966: Layer already exists 
a7eff924c5ac: Layer already exists 
24282ddb8cca: Layer already exists 
5f70bf18a086: Layer already exists 
8ba5f6d45106: Layer already exists 
571ade696b26: Layer already exists 
v2: digest: sha256:a2af8396c3dfaa8d0312868161bff238c17b742cd46d57296ed304a9495b2a7a size: 1779

```

8. Finally, put the new image down on the computer where the container is running. To implement the new version you must delete the container and create a new one from the new version of the image.

```bash
javiercruces@docker:~/taller3$ docker ps
CONTAINER ID   IMAGE                             COMMAND                  CREATED         STATUS         PORTS                                   NAMES
2a753adcd098   javiersaping/mi_servidor_web:v1   "httpd-foreground"       3 minutes ago   Up 3 minutes   0.0.0.0:8081->80/tcp, :::8081->80/tcp   nervous_lewin
5a362b768a25   nextcloud:latest                  "/entrypoint.sh apac…"   2 weeks ago     Up 2 weeks     0.0.0.0:8080->80/tcp, :::8080->80/tcp   nextcloud
dcc9f10a6cad   mariadb:10.5                      "docker-entrypoint.s…"   2 weeks ago     Up 2 weeks     3306/tcp                                wp_db
javiercruces@docker:~/taller3$ docker rm -f 2a753adcd098
2a753adcd098

javiercruces@docker:~/taller3$ docker run -d -p 8081:80 javiersaping/mi_servidor_web:v2
e632b46bb8cf8aac8019effdf5ac69cc20d8b9e76b17342638bc4858c63aef32

```


![](../img/Pasted_image_20240208085341.png)

