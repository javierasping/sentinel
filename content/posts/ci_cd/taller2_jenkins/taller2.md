---
title: "Taller 2 Comprobación de HTML5 válido y despliegue en surge.sh (test y deploy)"
date: 2024-03-14T10:00:00+00:00
description: Taller 2 Comprobación de HTML5 válido y despliegue en surge.sh (test y deploy)
tags: [Jenkis,CI/CD]
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

En este ejercicio queremos desplegar una página HTML5 en el servicio _surge.sh_, además queremos comprobar si el código HTML5 es válido. Estas dos operaciones: comprobar si el HTML5 es válido (test) y el despliegue en surge.sh (deploy) lo vamos a hacer con Jenkins de forma automática (IC y DC). Recuerda que el repositorio es [https://github.com/josedom24/ic-html5](https://github.com/josedom24/ic-html5).

Como vimos en el ejemplo 2, para hacer el despliegue necesitamos guardar el token que hemos obtenido de surge para que nos autentifiquemos. veamos como trabajar con credenciales en Jenkins.

## [Crear credenciales](https://fp.josedomingo.org/iaw/5_ic/taller2.html#crear-credenciales)

Podemos crear varios tipos de credenciales: usuario y contraseña, credenciales ssh,… Nosotros vamos a crear un _Secret text_ para guardar el token de surge.



```bash
debian@jenkins:~$ sudo apt install npm

debian@jenkins:~$ sudo npm install -g surge

debian@jenkins:~$ surge token

   Login (or create surge account) by entering email & password.

          email: javierasping@gmail.com
       password: 
```

![](../img/Pasted_image_20240229092356.png)


```bash
pipeline {
    environment {
        TOKEN = credentials('SURGE_TOKEN')
      }
    agent {
        docker { image 'josedom24/debian-npm'
        args '-u root:root'
        }
    }
    stages {
        stage('Clone') {
            steps {
                git branch:'master',url:'https://github.com/javierasping/taller2_ic-html5.git'
            }
        }
        
        stage('Install surge')
        {
            steps {
                sh 'npm install -g surge'
            }
        }
        stage('Deploy')
        {
            steps{
                sh 'surge ./_build/ josedom24.surge.sh --token $TOKEN'
            }
        }
        
    }
}
```

Instalamos y configuraramos Ngrok con nuestro token

```bash
debian@jenkins:~$ curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok

debian@jenkins:~$ ngrok config add-authtoken 2d2CfEVHT
Authtoken saved to configuration file: /home/debian/.config/ngrok/ngrok.yml

```

Indicamos en jenkins que vamos a utilizar un WebHook :

![](../img/Pasted_image_20240306121635.png)

Lanzo un ejemplo de HTML correcto y otro con errores :

![](../img/Pasted_image_20240306121613.png)



![](../img/Pasted_image_20240306121701.png)

Comprobamos que los cambios en el repositorio son recibidos en el WebHook :

![](../img/Pasted_image_20240306121550.png)

En GitHub comprobamos que le esta mandando la petición al  WebHook :

![](../img/Pasted_image_20240306121714.png)

<!-- ![](../img/Pasted_image_20240306121825.png) -->

