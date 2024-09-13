---
title: "Taller 1: Corrector ortográfico de documentos markdown (test)"
date: 2024-03-14T10:00:00+00:00
description: Taller 1 Corrector ortográfico de documentos markdown (test)
tags: [Jenkis,CI/CD]
hero: images/ci_cd/jenkins/taller1.png

---


# Taller 1: Corrector ortográfico de documentos markdown (test)

## [¿Qué tienes que entregar?](https://fp.josedomingo.org/iaw/5_ic/taller1.html#qu%C3%A9-tienes-que-entregar)

1. La URL del tu repositorio GitHub.

```bash
https://github.com/javierasping/taller1_jenkins_ic-diccionario
```


2. El contenido de la tu fichero `Jenkinfile`.

```bash
pipeline {
    agent {
        docker {
            image 'debian'
            args '-u root:root'
        }
    }
    stages {
        stage('Clone') {
            steps {
                git branch:'master', url:'https://github.com/javierasping/taller1_jenkins_ic-diccionario.git'
            }
        }
        stage('Install') {
            steps {
                sh 'apt-get update && apt-get install -y aspell-es ' 
            }
        }
        stage('Test') {
            steps {
                sh '''
                export LC_ALL=C.UTF-8
                OUTPUT=`cat doc/*.md | aspell list -d es -p ./.aspell.es.pws`
                if [ -n "$OUTPUT" ]; then
                    echo $OUTPUT
                    exit 1
                fi
                '''
            }
        }
    }
    post {
        always {
            mail to: 'javierasping@gmail.com',
            subject: "Status of pipeline: ${currentBuild.fullDisplayName}",
            body: "${env.BUILD_URL} has result ${currentBuild.result}"
        }
    }
}
```

3. Una captura de pantalla donde se vea la configuración del disparador del pipeline.

![](../img/Pasted_image_20240229084423.png)

![](../img/Pasted_image_20240229084437.png)

4. Una captura de un correo electrónico recibido sin ningún error, y otro con algún error en al ejecución del pipeline.

![](../img/Pasted_image_20240229084555.png)

![](../img/Pasted_image_20240229085404.png)


