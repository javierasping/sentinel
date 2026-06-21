---
title: "Creación de un sistema automatizado de instalación"
date: 2023-11-29T10:00:00+00:00
description: Creación de un sistema automatizado de instalación
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/creacion_de_un_sistema_automatizado_de_instalacion.jpg
---



## Instalación automática de una iso

En la página oficial de Debian nos descargaremos una imagen de Debian, en mi caso he seleccionado una netinstall:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.001.png)

Una vez descargada la imagen de debian, vamos a copiar su contenido en una carpeta para después hacer unas modificaciones. Para ello montaremos la iso como dispositivo loop :

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.002.png)

Una vez montada podremos ver su contenido :

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.003.jpeg)

Vamos a hacernos una copia de los ficheros que vamos a utilizar en un directorio nuestro para poder realizar cambios en ellos, una vez hagamos esto podemos desmontar la imagen:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.004.png)

Una vez copiados los ficheros vamos a movernos al directorio para crear el archivo preseed :

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.005.png)

Dentro del mismo copiaremos el fichero de plantilla de Bookworm que nos proporciona Debian, lo puedes encontrar en su página oficial → https://www.debian.org/releases/bookworm/example-preseed.txt. Yo meteré este fichero dentro de la carpeta fjcd\_auto.

Procederemos a editar la plantilla y seleccionaremos las distintas opciones :

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.006.jpeg)

Una vez configurado el fichero `preseed.cfg`, le damos permisos al directorio `install.amd` y descomprimimos el `initrd.gz`:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.007.png)

Añadimos las líneas de nuestro fichero `preseed` al `initrd`:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.008.png)

Volvemos a comprimir el fichero initrd y le quitamos los permisos dados anteriormente al directorio padre :

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.009.png)

Ahora añadiremos una entrada a este fichero para que, al arrancar la ISO, tengamos una entrada que realice automáticamente la instalación con nuestro fichero `preseed.cfg`:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.010.jpeg)

Por último, queda sacar los hash de los distintos archivos de la ISO y añadirlos al fichero `md5sum.txt`:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.011.png)

Con esto ya solo nos queda generar la ISO:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.012.png)

Si arrancamos con la ISO veremos la entrada que hemos creado:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.013.png)

Resultado :

![ref1]

## Servidor PXE

Ahora vamos a preparar el servidor PXE para que hagamos una instalación en red, para ello configuraré SNAT en el mismo para que los clientes tengan internet:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.015.png)

Para que el cambio sea permanente, tengo instalado y configurado `iptables-persistent`, además, recuerda activar el bit del forwarding.

Ahora vamos a instalar `dnsmasq`:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.016.png)

Y configuraremos el servicio:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.017.png)

Reiniciamos el servicio para que se aplique la configuración :

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.018.png)

Ahora, en el directorio raíz de nuestro TFTP, vamos a descargarnos el netboot de nuestra versión de Debian:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.019.png)

Ahora vamos a descomprimir el siguiente contenido:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.020.png)

Una vez descomprimido el fichero crearemos enlaces simbólicos a los siguientes ficheros :

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.021.png)

Ahora nos queda configurar el servidor web para pasar el fichero `preseed.cfg`, yo lo he puesto en el `DocumentRoot` del virtual host por defecto:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.022.png)

Por último, nos queda configurar la entrada del menú de la ISO que hemos descargado, indicamos que el archivo `preseed.cfg` está en la siguiente URL:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.023.jpeg)

Ahora podemos arrancar la máquina por PXE:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.024.jpeg)

Y si pulsamos sobre la entrada personalizada que acabamos de crear se instalará automáticamente a partir del fichero `preseed.cfg`:

![](/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.025.jpeg)


Resultado :

![ref1]


[ref1]: ../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.014.jpeg
