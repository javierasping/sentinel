---
title: "Instalación de Oracle 19c bajo Debian 12"
date: 2024-09-01T10:00:00+00:00
description: Instalación de Oracle 19c bajo Debian 12
tags: [Oracle,Debian]
hero: images/base_de_datos/instalar_oracle/instalacion_oracle.png

---


Instalar Oracle 19c en Debian 12 puede parecer complicado, pero no te preocupes, estoy aquí para guiarte en cada paso. En este post, te explicaré de manera sencilla cómo preparar tu sistema y realizar la instalación de Oracle 19c en Debian 12.

## Actualizar los repositorios

Lo primero es actualizar los repositorios de nuestra máquina virtual y, en el caso de que falte algún paquete, actualizarlo:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.001.png)

## Instalar dependencias

Lo siguiente será instalar las dependencias de Oracle en nuestro sistema:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.002.png)

- **libaio1** : Proporciona acceso asíncrono a E/S.
- **Unixodbc** : Es un controlador ODBC para conectividad de bases de datos.
- **Bc** : Es una calculadora de precisión arbitraria.
- **Ksh** : Es el shell Korn para scripts.
- **Gawk** : Es una versión mejorada de Awk para procesamiento de texto y datos.

## Añadir usuario oracle

Crearemos el grupo dba y el usuario oracle:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.003.png)

Comprobamos que podemos acceder al usuario oracle:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.004.png)

## Configuración de red

Tenemos que tener configurada una IP estática:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.005.png)

Además tenemos que tener una entrada en el fichero hosts con nuestra dirección privada:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.006.png)

## Descargar el archivo de instalación del sitio web de Oracle

Una vez comprobado que podemos instalarlo en nuestro sistema o máquina virtual, procederemos a descargarlo desde su página web oficial.

Rápidamente nos daremos cuenta de que Oracle no da soporte oficial a Debian; el paquete se encuentra en formato .rpm, lo que significa que está preparado para distribuciones basadas en Red Hat. 

Para que nosotros podamos usar este paquete, debemos transformarlo a .deb. Para ello, utilizaremos la herramienta `alien`, que convierte el paquete para que sea compatible.

Instalamos la herramienta:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.007.png)

Ahora utilizaremos `wget` para descargar el metapaquete de Oracle:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.008.png)

Una vez descargado, usaremos la utilidad `alien` para transformarlo. Este proceso puede tardar un poco, por lo que, para agilizarlo, he realizado la transformación en mi máquina física:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.009.png)

Nos lo pasamos a nuestra máquina virtual usando `scp`.

Ahora ya que tenemos nuestro paquete transformado a .deb, lo instalaremos usando `dpkg` en nuestra máquina virtual:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.010.jpeg)

Comenzaremos la instalación. Este proceso tardará un buen rato, así que es necesario tener paciencia:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.011.jpeg)

Una vez finalice, en el bashrc de nuestro usuario añadiremos las variables de entorno de Oracle. `ORACLE_SID` se nos indicará al final de la instalación; las demás dependerán de los directorios configurados en los pasos anteriores:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.012.png)

## Solución de errores

### Error [FATAL] [DBT-50000] No se ha podido comprobar la memoria disponible

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.013.png)

Se produce un error que indica que no se puede comprobar la memoria disponible. Podemos solucionar esto desactivando la comprobación de parámetros de configuración en la línea 164 del fichero `/etc/init.d/oracledb_ORCLCDB-19c`:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.014.jpeg)

Sustituimos la línea por la siguiente (línea 164 completa):     

`    `$SU -s /bin/bash  $ORACLE\_OWNER -c "$DBCA -silent -createDatabase -gdbName $ORACLE\_SID  -templateName  $TEMPLATE\_NAME  -characterSet  $CHARSET  - createAsContainerDatabase  $CREATE\_AS\_CDB  -numberOfPDBs  $NUMBER\_OF\_PDBS  - pdbName  $PDB\_NAME  -createListener  $LISTENER\_NAME:$LISTENER\_PORT  - datafileDestination $ORACLE\_DATA\_LOCATION -sid $ORACLE\_SID -autoGeneratePasswords -emConfiguration DBEXPRESS -emExpressPort $EM\_EXPRESS\_PORT -J- Doracle.assistants.dbca.validate.ConfigurationParams=false"

He subrayado el contenido que debes añadir; también puedes sustituir la línea entera.

Otro error común es que no se encuentre el comando `netstat`:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.015.png)

Se soluciona fácilmente instalando `net-tools`.

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.016.png)

### ORA-65096: Nombre de usuario o rol común no válido

Si ocurre un error al intentar crear un usuario:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.017.png)

Con esta modificación, podremos crear usuarios.

### Primeros pasos con Oracle

Nos conectaremos como administradores en la base de datos:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/conn_oracle.png)

Lo primero será crear un usuario, asignarle los permisos necesarios y comprobar la conexión:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.018.png)

Asignamos los permisos necesarios al usuario:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.019.png)

Probamos la conexión con el nuevo usuario:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.020.png)

Con esto habremos finalizado la instalación básica de Oracle 19c sobre Debian 12. Es recomendable instalar un cliente como SQL*Plus o SQL Developer para gestionar la base de datos.

## Instalación de SQL*Plus

Nos descargamos el paquete básico de SQL*Plus para Linux (archivo .zip):

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.021.jpeg)

Nos descargamos el segundo paquete de SQL*Plus:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.022.jpeg)

Nos creamos el directorio `/opt/oracle`:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.023.png)

Descomprimimos los archivos zip en el directorio recién creado:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.024.png)

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.025.png)

Nos metemos en el directorio y listamos su contenido:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.026.jpeg)

Y a continuación exportaremos la variable de las librerías de SQL*Plus y aplicaremos los cambios:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.027.png)

Para que el cambio sea permanente, lo añadiremos al archivo `.bashrc`:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.028.png)


