---
title: "Configuración de acceso remoto en Oracle"
date: 2024-09-01T10:00:00+00:00
description: Configuración de acceso remoto en Oracle
tags: [Oracle,Debian]
hero: images/base_de_datos/instalar_oracle/acceso_remoto_oracle.png

---


Para configurar el acceso remoto en Oracle, es fundamental ajustar correctamente los archivos de red ubicados en $ORACLE_HOME/network/admin. Estos archivos, como listener.ora y tnsnames.ora, permiten definir cómo se conectarán los clientes a la base de datos y qué equipos tendrán acceso.

## Configuración acceso remoto

La configuración de oracle con respecto a la red se guarda en el directorio que hayamos definido como home de oracle  $ORACLE\_HOME/network/admin :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.029.png)

- **listener.ora**: Este archivo sirve para configurar el servicio de escucha (listener) de Oracle. Contiene información sobre los puntos de conexión y los protocolos que el servidor de Oracle utilizará para aceptar conexiones de clientes.
- **samples**: Dentro de este directorio, hay ejemplos de archivos de configuración para varios componentes de Oracle. Estos archivos de muestra son útiles como referencia cuando necesitamos crear archivos de configuración.
- **shrept.lst**: Este archivo forma parte del proceso de recuperación de Oracle y se utiliza para rastrear la replicación de registros de cambios en tiempo real. Es esencial cuando se trabaja con replicación de datos.
- **sqlnet.ora**: Este archivo se configuran las opciones de red de Oracle. Aquí se define cómo se resuelven los nombres de los servidores, configurar medidas de seguridad y ajustar la capa de seguridad .
- **tnsnames.ora**: Aquí se definen los alias que oracle va a utilizar .

Comenzaremos configurando el listener.ora y indicaremos que equipos se pueden conectar a la base de datos en mi caso todos :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.030.png)

Una vez hecho esto iniciaremos sesión con el usuario oracle y iniciaremos el servicio de escucha de oracle para poder conectarnos en red:

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.031.jpeg)

\*Ten en cuenta que tienes que añadir las variables de oracle en el .bashrc del usuario oracle para que puedas iniciar el servicio , si no lo has hecho no te encontrara el comando .

En el equipo cliente donde vayamos a realizar la conexión deberemos de editar el fichero tsnames.ora y añadir la dirección y el puerto donde esta alojado nuestro servidor :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.032.jpeg)

Una vez hecho esto el comando para conectarnos es el siguiente :

![](../img/IMG_20231028_213222.jpg)

La sintaxis es usuario/contraseña@//IP:PUERTO/SID

Podemos consultar tablas , he añadido el esquema del proyecto del año anterior :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.034.png)