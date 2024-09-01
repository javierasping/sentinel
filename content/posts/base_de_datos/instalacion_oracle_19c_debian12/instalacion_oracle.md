---
title: "Instalación de Oracle 19c bajo Debian 12"
date: 2024-09-01T10:00:00+00:00
description: Instalación de Oracle 19c bajo Debian 12
tags: [Oracle,Debian]
hero: images/base_de_datos/instalar_oracle/oracle19.png

---
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GVDYVWJLRH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GVDYVWJLRH');
</script>

Instalar Oracle 19c en Debian 12 puede parecer complicado, pero no te preocupes, estoy aquí para guiarte en cada paso. En este post, te explicaré de manera sencilla cómo preparar tu sistema y realizar la instalación de Oracle 19c en Debian 12.

## Actualizar los repositorios

Lo primero es actualizar los repositorios de nuestra maquina virtual y en el caso de que no tengamos algún paquete lo actualizamos :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.001.png)

## Instalar dependencias

Lo siguiente sera instalar las dependencias de Oracle en nuestro sistema :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.002.png)

- **libaio1** : Proporciona acceso asíncrono a E/S.
- **Unixodbc** : Es un controlador ODBC para conectividad de bases de datos.
- **Bc** : Es una calculadora de precisión arbitraria.
- **Ksh** : Es el shell Korn para scripts.
- **Gawk** : Es una versión mejorada de Awk para procesamiento de texto y datos.

## Añadir usuario oracle

Crearemos el grupo dba y crearemos el usuario oracle :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.003.png)

Comprobamos que podemos acceder al usuario oracle :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.004.png)

## Configuración de red

Tenemos que tener configurada una ip estática :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.005.png)

Además tenemos que tener una entrada en el fichero hosts de nuestra dirección privada :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.006.png)

## Descargar el archivo de instalación del sitio web de Oracle

Una vez comprobado que podemos instalarlo en nuestro sistema o maquina virtual vamos a descargarnos desde su pagina web oficial .

Rápidamente nos daremos cuenta de que Oracle no da soporte a Debian ya que encontraremos el paquete en formato .rpm esto quiere decir que este esta preparado para instalarse en distribuciones basadas en red hat . 

Para que nosotros podamos usar este paquete deberemos transformarlo a .deb para ello existe una herramienta llamada alien que nos convertirá el paquete para que lo podamos usar .

Nos instalamos la herramienta :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.007.png)

Ahora usando wget nos descargaremos el metapaquete de Oracle :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.008.png)

Una vez descargado usaremos la utilidad alien para que nos transforme , esto tardara un ratillo aproximadamente para aligerar el proceso lo he transformado en mi maquina física :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.009.png)

Nos lo pasamos a nuestra maquina virtual usando scp .

Ahora ya que tenemos nuestro paquete transformado a .deb nos lo instalamos usando dpkg en nuestra maquina virtual 

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.010.jpeg)

Comenzaremos la instalación , tardara un buen rato así que hay que tener paciencia :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.011.jpeg)

Una vez finalice en el bashrc de nuestro usuario añadiremos las variables de entorno de oracle , ORACLE\_SID nos la dirá al final de la instalación , las demás dependerán de los directorio que hayamos puesto en pasos anteriores   :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.012.png)

## Solución errores

### Error [FATAL] [DBT-50000] No se ha podido comprobar la memoria disponible

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.013.png)

Nos devuelve un error , este nos indica que no puede comprobar la memoria disponible , este error lo podemos solucionar desactivando la comprobación de parámetros de configuración para ello en la linea 164 del fichero →  /etc/init.d/oracledb\_ORCLCDB-19c 

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.014.jpeg)

La cambiaremos por la siguiente (linea 164 completa) :     

`    `$SU -s /bin/bash  $ORACLE\_OWNER -c "$DBCA -silent -createDatabase -gdbName $ORACLE\_SID  -templateName  $TEMPLATE\_NAME  -characterSet  $CHARSET  - createAsContainerDatabase  $CREATE\_AS\_CDB  -numberOfPDBs  $NUMBER\_OF\_PDBS  - pdbName  $PDB\_NAME  -createListener  $LISTENER\_NAME:$LISTENER\_PORT  - datafileDestination $ORACLE\_DATA\_LOCATION -sid $ORACLE\_SID -autoGeneratePasswords -emConfiguration DBEXPRESS -emExpressPort $EM\_EXPRESS\_PORT -J- Doracle.assistants.dbca.validate.ConfigurationParams=false"

\*Subrayo el contenido que debes añadir , también puedes sustituir la linea entera .

Otro error que nos puede dar es que no encuentre netstat :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.015.png)

Se soluciona fácilmente instalando net-tools.

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.016.png)

### ORA-65096: nombre de usuario o rol común no valido

Si no nos deja crear un usuario :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.017.png)

Con esta modificación nos dejara crear usuarios 

### Primeros pasos con Oracle

Nos conectaremos como administradores en la base de datos : 

![](../img/conn_oracle.png)

Lo primero que tenemos que hacer sera crear un usuario , darle permisos que necesitemos e comprobar que nos podemos conectar con el :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.018.png)

Y le damos los permisos que consideremos al mismo :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.019.png)

Después probamos a conectarnos con el mismo :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.020.png)

Con esto habremos finalizado la instalación básica de Oracle 19c sobre Debian 12 . Es recomendable que si vas a utilizar la base de datos te instales un cliente como SQLplus o SQLdeveloper .

## Instalación SQLplus

Nos descargamos el paquete básico SQLplus para Linux , es un .zip :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.021.jpeg)

Nos descargamos el segundo paquete de SQLplus :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.022.jpeg)

Nos creamos el directorio /opt/oracle :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.023.png)

Descomprimimos los ficheros zip en el directorio que acabamos de crear :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.024.png)

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.025.png)

Nos metemos en el directorio y listamos el contenido :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.026.jpeg)

Y a continuación exportaremos la variable de las librería SQLplus y ejecutamos los cambios :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.027.png)

Si queremos que se mantenga lo añadiremos al bashrc :

![](../img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.028.png)


