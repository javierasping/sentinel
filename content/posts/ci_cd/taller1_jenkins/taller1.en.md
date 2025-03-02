---
title: "Workshop 1: Markdown (test)"
date: 2024-03-14T10:00:00+00:00
description: Workshop 1 Ortho-rector of markdown documents (test)
tags: [Jenkis,CI/CD]
hero: images/ci_cd/jenkins/taller1.png
---

## Workshop 1: Ortho-rector of markdown documents (test)

### [What do you have to deliver?](https://fp.josedomingo.org/iaw/5_ic/taller1.html#qu%C3%A9-tienes-que-entregar)

1. The URL of your GitHub repository.

```bash
https://github.com/javierasping/taller1_jenkins_ic-diccionario
```


2. The content of your file 'Jenkinfle'.

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

3. A screenshot where you see the pipeline trigger configuration.

![](/ci_cd/taller1_jenkins/img/Pasted_image_20240229084423.png)

![](/ci_cd/taller1_jenkins/img/Pasted_image_20240229084437.png)

4. A capture of an email received without any error, and another with some error in the execution of the pipeline.

![](/ci_cd/taller1_jenkins/img/Pasted_image_20240229084555.png)

![](/ci_cd/taller1_jenkins/img/Pasted_image_20240229085404.png)


