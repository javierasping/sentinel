---
title: "Práctica CI/CD con Jenkins"
date: 2024-03-14T10:00:00+00:00
description: Práctica CI/CD con Jenkins
tags: [Jenkis,CI/CD]
hero: images/ci_cd/jenkins/jenkins.png

---


El objetivo de esta práctica es el desarrollo gradual de un Pipeline que vaya realizando tareas sobre el repositorio de una aplicación.

La aplicación con la que vamos a trabajar será tu fork de la aplicación django Polls. Como hemos visto esta aplicación que implementa el tutorial de Django tiene implementado un módulo de pruebas.

Vamos a construir el Pipeline en varias fases:

## [Ejercicio 1: Construcción de una imagen docker](https://fp.josedomingo.org/iaw/5_ic/practica.html#ejercicio-1-construcci%C3%B3n-de-una-imagen-docker)

Partimos del pipeline que hemos desarrollado en el [Taller 3: Integración continua de aplicación django (Test)](https://fp.josedomingo.org/iaw/5_ic/taller3.html), donde hemos automatizado el test de la aplicación.

Modifica el pipeline para que después de hacer el test sobre la aplicación, genere una imagen docker. tienes que tener en cuenta que los pasos para generar la imagen lo tienes que realizar en la máquina donde está instalado Jenkins. Tendrás que añadir las siguientes acciones:

1. Construir la imagen con el `Dockerfile` que tengas en el repositorio.
2. Subir la imagen a tu cuenta de Docker Hub.
3. Borrar la imagen que se ha creado.

Por lo tanto tienes que estudiar el apartado [Ejecución de un pipeline en varios runner](https://fp.josedomingo.org/iaw/5_ic/jenkins/runner.html) para ejecutar el pipeline en dos runner:

- En el contenedor docker a partir de la imagen `python:3` los pasos del taller 3.
- En la máquina de Jenkins los pasos de este ejercicio.

Otras consideraciones:

- Cuando termine de ejecutar el pipeline te mandará un correo de notificación.
- El pipeline se guardará en un fichero `Jenkinsfile` en tu repositorio, y la configuración del pipeline hará referencia a él.

### [Entrega](https://fp.josedomingo.org/iaw/5_ic/practica.html#entrega)

1. Una captura de pantalla donde se vea la salida de un build que se ha ejecutado de manera correcta.

```bash

```

![](../img/Pasted_image_20240307100704.png)


2. Una captura de pantalla de tu cuenta de Docker Hub donde se vea la imagen subida de último build.

```bash

```

![](../img/Pasted_image_20240307100721.png)

3. Introduce un fallo en el `Dockerfile` y muestra la salida del build donde se produce el error.

```bash

```

![](../img/Pasted_image_20240307100737.png)

4. Entrega la URL del repositorio para ver el `Jenkinsfile`.

```bash
https://github.com/javierasping/django_tutorial_docker.git
```


5. Pantallazo con el correo que has recibido de la ejecución del pipeline.

```bash

```

![](../img/Pasted_image_20240307100824.png)


## [Ejercicio 2: Despliegue de la aplicación](https://fp.josedomingo.org/iaw/5_ic/practica.html#ejercicio-2-despliegue-de-la-aplicaci%C3%B3n)

Amplía el pipeline anterior para que tenga una última etapa donde se haga el despliegue de la imagen que se ha subido a Docker Hub en tu entorno de producción (VPS). Algunas pistas:

- Busca información de cómo hacer el despliegue a un servidor remoto (ssh, buscando algún plugin con esa funcionalidad,…)
- Si vas a hacer conexiones por ssh, tendrás que guardar una credencial en tu Jenkins con el nombre de usuario y contraseña.
- Para el despliegue deberá usar el fichero `docker-compose.yaml` que has generado en otras prácticas.
- Se deberá borrar el contenedor con la versión anterior, descargar la nueva imagen y crear un nuevo contenedor.

Otras consideraciones:

- Cambia el disparador del pipeline. Configúralo con un webhook de github, para que cada vez que se produce un push se ejecute el pipeline. Para que el webhook pueda acceder a tu Jenkins puedes usar [ngrok](https://ngrok.com/).

### [Entrega](https://fp.josedomingo.org/iaw/5_ic/practica.html#entrega)

1. El contenido del fichero `Jenkinsfile`.
2. Las credenciales que has guardado en Jenkins.

![](../img/Pasted_image_20240307151636.png)

3. Demuestra al profesor como se realiza la IC/DC completo.

Ejecución normal del pipeline :

![](../img/Pasted_image_20240307151713.png)

La configuración de nginx y los contenedores ejecutandose

```bash
javiercruces@atlas:~$ sudo cat /etc/nginx/sites-available/django_docker 
server {
    listen 80;
    server_name djangodocker.javiercd.es;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name djangodocker.javiercd.es;

    ssl_certificate /etc/letsencrypt/live/javiercd.es/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/javiercd.es/privkey.pem;

    location / {
        proxy_pass http://localhost:8082;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

javiercruces@atlas:~$ docker ps
CONTAINER ID   IMAGE                             COMMAND                  CREATED          STATUS          PORTS                                       NAMES
4d7947fc359f   javierasping/django_tutorial_ic   "/bin/sh -c 'python3…"   33 minutes ago   Up 33 minutes   0.0.0.0:8082->3000/tcp, :::8082->3000/tcp   django_tutorial_web
bdf947a4bccc   mariadb                           "docker-entrypoint.s…"   33 minutes ago   Up 33 minutes   3306/tcp                                    mariadb-django

```
La aplicación funcionando en el VPS :

![](../img/Pasted_image_20240307191739.png)

La configuración de Ngrok y el Webhook

```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok

javiercruces@atlas:~$ ngrok config add-authtoken 2d2CfE


debian@jenkins:~$ ngrok http http://localhost:8082

```

![](../img/Pasted_image_20240307195316.png)

![](../img/Pasted_image_20240307192546.png)
![](../img/Pasted_image_20240307194954.png)

![](../img/Pasted_image_20240307195210.png)
![](../img/Pasted_image_20240307195252.png)

Si provocamos el fallo :

![](../img/Pasted_image_20240307195917.png)
