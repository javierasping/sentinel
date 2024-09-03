---
title: "Creación de un sistema automatizado de instalación"
date: 2023-11-29T10:00:00+00:00
description: Creación de un sistema automatizado de instalación
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/creacion_de_un_sistema_automatizado_de_instalacion.jpg
---



## Instalación automática de una iso

En la pagina oficial de debian nos descargaremos una imagen de debian , en mi caso he seleccionado una netinstall :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.001.png)

Una vez descargada la imagen de debian, vamos a copiar su contenido en una carpeta para después hacer unas modificaciones. Para ello montaremos la iso como dispositivo loop :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.002.png)

Una vez montada podremos ver su contenido :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.003.jpeg)

Vamos a hacernos una copia de los ficheros que vamos a utilizar  a un directorio nuestro para poder realizar cambios en los mismos , una vez hagamos esto podemos desmontar la imagen :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.004.png)

Una vez copiados los ficheros vamos a movernos al directorio para crear el archivo preseed :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.005.png)

Dentro del mismo copiaremos el fichero de plantilla de bookworm que nos proporciona debian , lo puedes encontrar en su pagina oficial → https://www.debian.org/releases/bookworm/example-preseed.txt . Yo metere este fichero dentro de la carpeta fjcd\_auto .

Procederemos a editar la plantilla y seleccionaremos las distintas opciones :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.006.jpeg)

Una vez configurado el fichero preseed.cfg , le damos permisos al directorio install.amd y descomprimimos el initrd.gz :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.007.png)

Añadimos las lineas de nuestro fichero preseed al initrd :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.008.png)

Volvemos a comprimir el fichero initrd y le quitamos los permisos dados anteriormente al directorio padre :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.009.png)

Ahora añadiremos una entrada a este fichero para que al arrancar la iso tendríamos una entrada que realizara automáticamente la instalación con nuestro fichero preseed.cfg:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.010.jpeg)

Por ultimo queda sacar los hash de los distintos archivos de la iso y añadirlos al fichero md5sum.txt:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.011.png)

Con esto ya solo nos queda  generar la iso :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.012.png)

Si arrancamos con la iso veremos la entrada que hemos creado :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.013.png)

Resultado :

![ref1]

## Servidor PXE

Ahora vamos a preparar el servidor PXE para que hagamos una instalación en red , para ello configurare SNAT en el mismo para que los clientes tengan internet :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.015.png)

Para que el cambio sea permanente tengo instalado  y configurado iptables-persistent , además recuerda activar el bit del forwarding 

Ahora instalamos vamos a instalar dnsmasq :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.016.png)

Y configuraremos el servicio:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.017.png)

Reiniciamos el servicio para que se aplique la configuración :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.018.png)

Ahora en el directorio root de nuestro tftp vamos a descargarnos el netboot de nuestra version de debian :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.019.png)

Ahora vamos a descomprimir el siguiente contenido :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.020.png)

Una vez descomprimido el fichero crearemos enlaces simbólicos a los siguientes ficheros :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.021.png)

Ahora nos queda configurar el servidor web para pasar el fichero preseed.cfg , yo lo he puesto en el document root del virtual host por defecto :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.022.png)

Por ultimo nos queda configurar la entrada del menú de la iso que hemos descargado , indicamos que el archivo preseed.cfg esta en la siguiente url :

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.023.jpeg)

Ahora podemos arrancar la maquina por pxe: 

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.024.jpeg)

Y si pulsamos sobre la entrada personalizada que acabamos de crear se instalara automáticamente a partir del fichero preseed.cfg:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.025.jpeg)


Resultado :

![ref1]


[ref1]: ../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.014.jpeg
