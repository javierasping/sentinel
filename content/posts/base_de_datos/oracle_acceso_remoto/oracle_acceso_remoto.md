---
title: "Configuración de acceso remoto en Oracle"
date: 2024-09-01T10:00:00+00:00
description: Configuración de acceso remoto en Oracle
tags: [Oracle,Debian]
hero: images/base_de_datos/instalar_oracle/acceso_remoto_oracle.png

---


Para configurar el acceso remoto en Oracle, es fundamental ajustar correctamente los archivos de red ubicados en `$ORACLE_HOME/network/admin`. Estos archivos, como `listener.ora` y `tnsnames.ora`, permiten definir cómo se conectarán los clientes a la base de datos y qué equipos tendrán acceso.

## Configuración del acceso remoto

La configuración de Oracle con respecto a la red se guarda en el directorio definido como home de Oracle: `$ORACLE_HOME/network/admin` :

![](/base_de_datos/oracle_acceso_remoto/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.029.png)

- **listener.ora**: Este archivo sirve para configurar el servicio de escucha (listener) de Oracle. Contiene información sobre los puntos de conexión y los protocolos que el servidor de Oracle utilizará para aceptar conexiones de clientes.
- **samples**: Dentro de este directorio, hay ejemplos de archivos de configuración para varios componentes de Oracle. Estos archivos de muestra son útiles como referencia cuando necesitamos crear archivos de configuración.
- **shrept.lst**: Este archivo forma parte del proceso de recuperación de Oracle y se utiliza para rastrear la replicación de registros de cambios en tiempo real. Es esencial cuando se trabaja con replicación de datos.
- **sqlnet.ora**: En este archivo se configuran las opciones de red de Oracle. Aquí se define cómo se resuelven los nombres de los servidores, se configuran medidas de seguridad y se ajusta la capa de seguridad.
- **tnsnames.ora**: Aquí se definen los alias que Oracle utilizará.

Comenzaremos configurando el `listener.ora` e indicaremos qué equipos se pueden conectar a la base de datos. En mi caso, permitiremos todos:

![](/base_de_datos/oracle_acceso_remoto/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.030.png)

Una vez hecho esto, iniciaremos sesión con el usuario `oracle` y arrancaremos el servicio de escucha de Oracle para poder conectarnos en red:

![](/base_de_datos/oracle_acceso_remoto/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.031.jpeg)

*Ten en cuenta que debes añadir las variables de Oracle en el `.bashrc` del usuario `oracle` para poder iniciar el servicio; de lo contrario, el sistema no encontrará el comando.

En el equipo cliente donde vayamos a realizar la conexión, deberemos editar el fichero `tnsnames.ora` y añadir la dirección y el puerto donde está alojado nuestro servidor:

![](/base_de_datos/oracle_acceso_remoto/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.032.jpeg)

Una vez hecho esto, el comando para conectarnos es el siguiente:

![](/base_de_datos/oracle_acceso_remoto/img/IMG_20231028_213222.jpg)

La sintaxis es `usuario/contraseña@//IP:PUERTO/SID`.

Podemos consultar tablas; he añadido el esquema del proyecto del año anterior:

![](/base_de_datos/oracle_acceso_remoto/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.034.png)