---
title: "Interconexión de servidores de bases de datos"
date: 2024-09-01T10:00:00+00:00
description: Interconexión de servidores de bases de datos
tags: [Oracle, Mysql, PostgreSQL, Debian]
hero: images/base_de_datos/interconexion_de_servidores/interconexion_de_servidores.png
---

Este post aborda cómo configurar y gestionar conexiones entre diferentes bases de datos, tanto homogéneas como heterogéneas, para facilitar la interoperabilidad entre sistemas de bases de datos diversos. A lo largo del artículo, se exploran distintos escenarios de conexión, comenzando con configuraciones entre bases de datos del mismo tipo, como Oracle a Oracle o PostgreSQL a PostgreSQL, y luego avanzando hacia conexiones heterogéneas entre diferentes tecnologías, como Oracle a MySQL, PostgreSQL a Oracle, y viceversa. También se cubren los pasos necesarios para configurar enlaces, crear usuarios, y modificar archivos de configuración clave, permitiendo así realizar consultas remotas 

## Conexiones homogéneas 

### Oracle a Oracle

Vamos a interconectar dos bases de datos Oracle, a las cuales llamaremos **oracle1** y **oracle2** para diferenciarlas a lo largo de esta práctica.

---

#### Creación de usuarios en Oracle1

Primero, crearemos un usuario en Oracle1 que tenga permisos para conectarse a la base de datos y para crear enlaces de base de datos:

![Creación de usuario en Oracle1](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.001.png)

Para verificar que el usuario se ha creado correctamente, desconéctate del usuario actual y vuelve a conectarte con el nuevo usuario:

![Verificación de usuario](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.002.png)

---

#### Creación de usuarios en Oracle2

Repite los pasos realizados en Oracle1 para crear un usuario en Oracle2 con permisos adecuados para conectarse remotamente y crear enlaces de base de datos:

![Creación de usuario en Oracle2](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.003.png)

Verifica la conexión con el nuevo usuario creado:

![Verificación de conexión en Oracle2](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.004.png)

#### Configuración de los ficheros listener.ora y tnsnames.ora en ORACLE1

Para garantizar la interconexión, debemos configurar los ficheros `listener.ora` y `tnsnames.ora`. Esto permitirá que ORACLE1 escuche las conexiones y reconozca la ubicación de ORACLE2.

##### Configuración de listener.ora

Edita el fichero `listener.ora` para que ORACLE1 pueda escuchar conexiones en la red:

![Configuración de listener.ora](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.006.jpeg)

> **Nota:** Aunque se recomienda permitir conexiones solo desde direcciones específicas, en este entorno de pruebas hemos habilitado acceso general. En este archivo también se define el puerto utilizado por Oracle.

##### Configuración de tnsnames.ora

Ahora configuraremos el fichero `tnsnames.ora` para que ORACLE1 sepa dónde está ORACLE2:

![Configuración de tnsnames.ora](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.007.jpeg)

En este ejemplo, ORACLE2 está configurado bajo la IP `192.168.122.13` y escucha en el puerto `1521`. También es importante conocer el nombre del servicio remoto. Si no lo sabes, puedes ejecutarlo en ORACLE2 utilizando:

![Consulta del nombre del servicio](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.008.png)

##### Verificación de conectividad

Para confirmar que ORACLE1 puede comunicarse con ORACLE2, utilizaremos la herramienta `tnsping` con el alias configurado:

![Verificación con tnsping](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.009.jpeg)

> **¡Recuerda!** Si no configuraste el `listener.ora` en el servidor remoto (ORACLE2), esta prueba fallará.

---

#### Configuración de los ficheros listener.ora y tnsnames.ora en ORACLE2

Ahora repetiremos los mismos pasos en ORACLE2 para que pueda comunicarse con ORACLE1.

##### Configuración de listener.ora

Edita el fichero `listener.ora` para que ORACLE2 escuche conexiones entrantes:

![Configuración de listener.ora](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.010.jpeg)

En este caso, hemos configurado ORACLE2 para escuchar en cualquier dirección, utilizando el puerto `1521`, al igual que en ORACLE1.

##### Configuración de tnsnames.ora

Edita el fichero `tnsnames.ora` para definir un alias que permita a ORACLE2 comunicarse con ORACLE1:

![Configuración de tnsnames.ora](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.011.jpeg)

##### Verificación de conectividad

Usa la herramienta `tnsping` en ORACLE2 con el alias configurado para ORACLE1:

![Verificación con tnsping](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.012.jpeg)

Si la salida es exitosa, significa que ORACLE2 puede comunicarse con ORACLE1.

> **¡Recuerda!** Si no configuraste el `listener.ora` en el servidor remoto (ORACLE1), esta prueba fallará.

---

#### Creación del enlace de ORACLE1 a ORACLE2

En esta etapa, estableceremos un enlace desde ORACLE1 hacia ORACLE2. Utilizaremos un usuario con privilegios de creación de enlaces, como **javiercruces1**, que fue creado anteriormente.

El enlace recibirá un nombre, en este caso, `ORACLE2_LINK`. Especificaremos que utilizaremos las credenciales del usuario remoto **javiercruces2** y la conexión definida en el fichero `tnsnames.ora` para ORACLE2.

![Creación del enlace ORACLE1 a ORACLE2](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.013.jpeg)

##### Verificación del enlace

Para verificar, crearemos la tabla `dept` en ORACLE2 y realizaremos una consulta desde ORACLE1:

![Consulta desde ORACLE1](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.014.jpeg)

---

#### Creación del enlace de ORACLE2 a ORACLE1

Ahora configuraremos el enlace en la dirección opuesta, de ORACLE2 a ORACLE1. Seguiremos el mismo procedimiento.

Con el usuario **javiercruces2**, crearemos un enlace llamado `ORACLE1_LINK`. Este enlace usará las credenciales del usuario remoto **javiercruces1** y la conexión definida en el fichero `tnsnames.ora` para ORACLE1:

![Creación del enlace ORACLE2 a ORACLE1](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.015.jpeg)

##### Verificación del enlace

Realizaremos una consulta sencilla utilizando el enlace recién creado:

![Consulta desde ORACLE2](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.016.jpeg)

---

#### Consultas simultáneas entre ORACLE1 y ORACLE2

Ahora, comprobaremos que es posible realizar consultas utilizando ambas bases de datos simultáneamente desde ORACLE1:

![Consulta simultánea desde ORACLE1](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.017.jpeg)

Esta misma consulta puede realizarse desde ORACLE2 también:

![Consulta simultánea desde ORACLE2](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.018.jpeg)

---
### PostgreSQL a PostgreSQL

Para permitir la interconexión, es esencial configurar ambas máquinas para que escuchen peticiones. Esto se logra definiendo las IPs y puertos en el archivo de configuración ubicado en `/etc/postgresql/15/main/postgresql.conf`:

![Configuración de escucha en postgresql.conf](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.019.jpeg)

Además, es necesario configurar las redes desde las cuales se aceptarán conexiones. Esto se realiza en el archivo `pg_hba.conf`:

![Configuración de pg_hba.conf](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.020.png)

Después de realizar estos cambios, reiniciaremos el servicio PostgreSQL para aplicarlos:

![Reinicio del servicio PostgreSQL](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.021.png)

Al igual que en el apartado anterior, usaremos el esquema de tablas *Scott*, colocando una tabla en cada base de datos para realizar consultas "remotas".

---

#### Interconectar PostgreSQL1 a PostgreSQL2

Para interconectar las bases de datos, utilizaremos **dblink**, un módulo que permite realizar consultas y operaciones distribuidas entre bases de datos PostgreSQL. Esto se logra estableciendo conexiones directas entre ellas.

##### Creación de usuarios y base de datos en PostgreSQL1

Primero, creamos los usuarios y la base de datos en PostgreSQL1:

![Creación de usuarios y base de datos](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.022.png)

##### Habilitar extensión dblink

Activaremos la extensión `dblink` en PostgreSQL1:

![Habilitar dblink](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.023.png)

##### Creación de la conexión hacia PostgreSQL2

Usaremos el módulo `dblink` para establecer una conexión hacia PostgreSQL2:

![Creación de conexión hacia PostgreSQL2](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.024.png)

##### Realizar consultas utilizando dblink

Una vez creada la conexión, podemos realizar consultas remotas desde PostgreSQL1:

![Consulta remota utilizando dblink](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.025.png)

> **Nota:** Es un poco tedioso definir los campos para cada consulta remota, lo que puede dificultar su uso en consultas más complejas.

---

#### Interconectar PostgreSQL2 a PostgreSQL1

##### Creación de usuarios y base de datos en PostgreSQL2

Crearemos los usuarios y la base de datos en PostgreSQL2 siguiendo un proceso similar al realizado en PostgreSQL1:

![Creación de usuarios y base de datos](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.026.png)

##### Habilitar extensión dblink y crear conexión hacia PostgreSQL1

Activaremos la extensión `dblink` y configuraremos la conexión hacia PostgreSQL1:

![Habilitar dblink y crear conexión hacia PostgreSQL1](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.027.png)

##### Realizar consultas hacia PostgreSQL1

Ahora, podemos realizar consultas desde PostgreSQL2 hacia PostgreSQL1:

![Consulta remota desde PostgreSQL2](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.028.jpeg)

---

#### Consultas simultáneas entre PostgreSQL1 y PostgreSQL2

Para simplificar consultas remotas entre ambas bases de datos, podemos crear vistas. Esto evita la necesidad de definir manualmente el tipo de cada campo en las consultas:

![Consulta remota simultánea utilizando vistas](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.029.jpeg)

La misma consulta puede realizarse desde PostgreSQL1 hacia PostgreSQL2:

![Consulta simultánea desde PostgreSQL1](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.030.jpeg)

---

## Conexión Heterogénea

### Oracle a MySQL

#### Instalación del driver ODBC para MySQL

Primero, descargamos el driver ODBC para MySQL junto con las dependencias necesarias:

![Descarga de dependencias](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.031.png)

Accedemos a la página oficial de MySQL para descargar los drivers y proceder a su instalación:

![Instalación del driver ODBC](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.032.jpeg)

#### Configuración de Heterogeneous Services en Oracle

Accedemos al directorio `hs/admin` dentro de nuestra instalación de Oracle:

![Acceso al directorio hs/admin](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.033.png)

Editamos el archivo `initMYSQL.ora` con el siguiente contenido para configurar Heterogeneous Services:

![Configuración de initMYSQL.ora](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.034.png)

#### Configuración de ODBC para MySQL

Configuramos ODBC para MySQL, asegurándonos de incluir las credenciales correctas para conectar con la base de datos MySQL:

![Configuración de ODBC](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.035.png)

#### Configuración del listener en Oracle

Actualizamos la configuración del listener para incluir `localhost` y el puerto de escucha de Oracle:

![Configuración del listener](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.036.jpeg)

Reiniciamos el servicio del listener de Oracle para aplicar los cambios:

![Reinicio del listener](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.037.png)

#### Comprobación del driver ODBC

Verificamos que el driver ODBC está funcionando correctamente conectándonos a la base de datos MySQL. También podemos utilizar el driver `isql` para comprobar la conexión:

![Prueba del driver ODBC con MySQL](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.038.jpeg)

#### Creación del enlace entre Oracle y MySQL

Creamos el enlace en Oracle para conectarnos a la base de datos MySQL:

![Creación del enlace](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.039.png)

#### Realizar consultas entre Oracle y MySQL

Podemos realizar una consulta sencilla hacia la base de datos MySQL:

![Consulta simple a MySQL](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.040.jpeg)

También es posible realizar consultas utilizando ambas bases de datos simultáneamente. Es importante encerrar en comillas dobles los nombres de los campos y tablas de MySQL para que sean interpretados correctamente:

![Consulta combinada entre Oracle y MySQL](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.041.jpeg)


### Mysql a Oracle

<!-- ![](../img/when-i-think-i_ve-found-all-the-issues-in-our-infrastructure-but-then-find-something-that-shows-me-it-was-all-just-the-tip-of-the-iceberg.webp) -->

<img src="../img/when-i-think-i_ve-found-all-the-issues-in-our-infrastructure-but-then-find-something-that-shows-me-it-was-all-just-the-tip-of-the-iceberg.webp" style="width: 75%; height: auto; max-height: 100vh; object-fit: contain;">

---

### Oracle a PostgreSQL

> **Nota:** Para este apartado se utilizó una máquina con Oracle Linux 8 y Oracle Database 23.

#### Configuración previa en Oracle

Como paso inicial, creamos nuevamente un usuario y base de datos en Oracle, asignando los permisos adecuados:

![Creación de usuario y base de datos en Oracle](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.042.jpeg)

#### Instalación del driver para PostgreSQL

Instalamos el driver de PostgreSQL usando `dnf`. Este comando también instalará las librerías necesarias como dependencias:

![Instalación del driver PostgreSQL](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.043.jpeg)

#### Configuración del archivo `odbcinst.ini`

El archivo `/etc/odbcinst.ini` se utiliza en sistemas Linux para configurar los controladores ODBC. Editamos este archivo para registrar el driver de PostgreSQL:

![Configuración de odbcinst.ini](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.044.jpeg)

#### Configuración del archivo `odbc.ini`

El archivo `/etc/odbc.ini` contiene configuraciones específicas para cada conexión a una base de datos. Aquí configuramos los detalles de la conexión a la base de datos PostgreSQL:

![Configuración de odbc.ini](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.045.jpeg)

#### Configuración en Oracle para usar el driver

Configuramos Oracle para que pueda utilizar el driver ODBC. Esto incluye actualizar los archivos necesarios para establecer la conexión:

![Configuración de Oracle para usar el driver](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.046.jpeg)

#### Configuración del Listener en Oracle

Configuramos el archivo del listener para habilitar la comunicación con la base de datos PostgreSQL:

![Configuración del listener](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.047.jpeg)

#### Configuración del archivo `tnsnames.ora`

Añadimos una entrada al archivo `tnsnames.ora` para definir la conexión a PostgreSQL:

![Configuración de tnsnames.ora](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.048.jpeg)

#### Reinicio del Listener

Reiniciamos el servicio del listener para aplicar los cambios:

![Reinicio del listener](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.049.jpeg)

#### Prueba de conexión

Verificamos la conectividad utilizando `tnsping`:

![Prueba de conexión con tnsping](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.050.jpeg)

Además, probamos la conexión utilizando el driver ODBC desde la terminal:

![Conexión usando el driver ODBC](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.051.jpeg)

#### Creación del enlace en Oracle

Conectamos a Oracle y creamos el enlace a la base de datos PostgreSQL. En las consultas, los nombres de campos y tablas deben ir entre comillas dobles, y los valores entre comillas simples:

![Creación del enlace](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.052.png)

#### Consultas simultáneas entre Oracle y PostgreSQL

Podemos realizar consultas combinadas entre ambas bases de datos:

![Consulta combinada entre Oracle y PostgreSQL](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.053.png)


### PostgreSQL a Oracle

#### Descarga e instalación de paquetes necesarios

Desde la página oficial de Oracle descargaremos los siguientes paquetes requeridos:

![Paquetes para conexión a Oracle](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.054.png)

Dado que el sistema utilizado es Debian, es necesario convertir los paquetes de formato RPM a DEB utilizando `alien`. El proceso tardará aproximadamente 5 minutos, y los paquetes se instalarán automáticamente al utilizar el parámetro `-i`:

![Conversión e instalación con alien](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.055.png)

#### Prueba de conexión a Oracle

Una vez instalados los paquetes, verificamos que es posible conectarse remotamente a la base de datos Oracle para garantizar que la configuración es correcta:

![Prueba de conexión a Oracle](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.056.jpeg)

#### Descarga y compilación de oracle_fdw

El siguiente paso es instalar `oracle_fdw`, una extensión para PostgreSQL que permite conectarse a Oracle. Descargamos la versión más reciente desde el repositorio oficial:

- **Repositorio:** [oracle_fdw en GitHub](https://github.com/laurenz/oracle_fdw)

Clonamos el repositorio y compilamos el código fuente:

![Clonación y compilación del repositorio](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.057.png)

Dentro del directorio descargado, ejecutamos `make` para compilar:

![Ejecución de make](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.058.png)

Finalmente, instalamos la extensión con el comando `make install`:

![Ejecución de make install](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.059.png)

#### Configuración de PostgreSQL

1. **Creación de la extensión:**
   Nos conectamos a la base de datos PostgreSQL donde queremos crear el enlace y configuramos la extensión `oracle_fdw`:

   ![Creación de la extensión oracle_fdw](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.063.png)

2. **Creación del esquema y servidor foráneo:**
   Creamos un esquema llamado `oracle` y configuramos un servidor foráneo apuntando a la base de datos Oracle:

   ![Configuración del servidor foráneo](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.063.png)

3. **Mapeo de usuarios:**
   Creamos un mapeo entre el usuario local de PostgreSQL (`javiercruces1`) y el usuario remoto de Oracle (`javiercruces3`). También otorgamos los permisos necesarios sobre el esquema y el servidor foráneo:

   ![Mapeo de usuarios y permisos](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.063.png)

4. **Importación del esquema:**
   Con el usuario local de PostgreSQL, importamos el esquema de tablas del usuario de Oracle hacia el servidor foráneo local:

   ![Importación del esquema](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.064.png)

#### Consultas combinadas

Finalmente, podemos realizar consultas que involucren datos de ambas bases de datos (PostgreSQL y Oracle). Esto permite trabajar con información distribuida de manera integrada:

![Consultas combinadas](../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.065.png)



[ref1]: ../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.060.jpeg
[ref2]: ../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.061.jpeg
[ref3]: ../img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.062.jpeg
