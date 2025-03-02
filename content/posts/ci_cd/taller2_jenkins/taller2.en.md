---
title: "Workshop 2: Valid HTML5 Check and surge.sh Deployment (Test and Deploy)"
date: 2024-03-14T10:00:00+00:00
description: "Workshop 2: Valid HTML5 Check and surge.sh Deployment (Test and Deploy)"
tags: [Jenkins, CI/CD]
hero: images/ci_cd/jenkins/taller2.png
---

In this exercise, we want to deploy an HTML5 page on the service _surge.sh_. We also want to check if the HTML5 code is valid. These two operations—checking if the HTML5 is valid (test) and deploying to surge.sh (deploy)—will be automated using Jenkins (CI/CD). 

Remember that the repository is [https://github.com/josedom24/ic-html5](https://github.com/josedom24/ic-html5).

As we saw in Example 2, to do the deployment, we need to save the token obtained from surge.sh. Let's see how to work with credentials in Jenkins.

## [Create credentials](https://fp.josedomingo.org/iaw/5_ic/taller2.html#crear-credenciales)

We can create several types of credentials: user and password, SSH credentials, etc. We will create a _Secret text_ credential to store the surge token.

```bash
debian@jenkins:~$ sudo apt install npm

debian@jenkins:~$ sudo npm install -g surge

debian@jenkins:~$ surge token

   Login (or create a surge account) by entering your email & password.

          email: javierasping@gmail.com
       password: 
```

![Surge Token](/ci_cd/taller2_jenkins/img/Pasted_image_20240229092356.png)

```groovy
pipeline {
    environment {
        TOKEN = credentials('SURGE_TOKEN')
    }
    agent {
        docker { 
            image 'josedom24/debian-npm'
            args '-u root:root'
        }
    }
    stages {
        stage('Clone') {
            steps {
                git branch: 'master', url: 'https://github.com/javierasping/taller2_ic-html5.git'
            }
        }
        
        stage('Install surge') {
            steps {
                sh 'npm install -g surge'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'surge ./_build/ josedom24.surge.sh --token $TOKEN'
            }
        }
    }
}
```

We install and configure Ngrok with our token:

```bash
debian@jenkins:~$ curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok

debian@jenkins:~$ ngrok config add-authtoken 2d2CfEVHT
Authtoken saved to configuration file: /home/debian/.config/ngrok/ngrok.yml
```

We indicate in Jenkins that we will use a WebHook:

![Jenkins WebHook](/ci_cd/taller2_jenkins/img/Pasted_image_20240306121635.png)

I launch a correct HTML example and one with errors:

![Valid HTML Example](/ci_cd/taller2_jenkins/img/Pasted_image_20240306121613.png)

![Invalid HTML Example](/ci_cd/taller2_jenkins/img/Pasted_image_20240306121701.png)

We check that the changes in the repository are received by the WebHook:

![WebHook Received](/ci_cd/taller2_jenkins/img/Pasted_image_20240306121550.png)

On GitHub, we check that it is sending the request to the WebHook:

![GitHub WebHook](/ci_cd/taller2_jenkins/img/Pasted_image_20240306121714.png)

![Another GitHub WebHook Image](/ci_cd/taller2_jenkins/img/Pasted_image_20240306121825.png)
