---
title: "Compilación de un kernel"
date: 2023-11-29T10:00:00+00:00
description: Compilación de un kernel
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/compilacion_de_un_kernel/compilacion_de_un_kernel.jpg
---
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GVDYVWJLRH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GVDYVWJLRH');
</script>


## Introducción

Para la realización de la practica voy a elegir el kernel 6.4.4 que me he descargado desde el repositorio backports :

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.001.jpeg)

Para descargarnos el código fuente usaremos apt source :

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.002.png)

Nos creara un directorio con el código fuente 

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.003.png)


Si listamos el contenido del directorio con el código fuente veremos que la estructura es la misma que para compilar un paquete en C .

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.004.jpeg)

## Primera compilación

Lo primero que vamos a hacer es usar el fichero .config que tiene cargado nuestro kernel , actualmente el mio tiene 10640 lineas.

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.005.png)

A continuación vamos a lanzar la orden make oldconfig para que utilice el fichero actual del kernel que estemos usando .

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.006.png)

Si vemos tenemos configurados 2413 módulos de forma estática y 3855 de forma dinámica:

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.007.png)

Vamos a pasarle el parámetro localmodconfig , dejare el enter pulsado para que seleccione las distintos parámetros por defecto .

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.008.png)

Vemos que con este parámetro hemos bajado significativamente el numero de módulos , ya que con el método usado en el paso anterior solo se utilizan los que tenemos actualmente cargados en el kernel :

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.009.png)

Compilaremos el kernel y lo probaremos , en mi caso arranca :

![ref1]

## Segunda compilación

Voy a quitar algunos componentes manualmente usando la herramienta make xconfig :

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.011.jpeg)

Después de eliminar varios puntos del .config se me ha quedado con : 

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.012.png)

Ahora vamos a usar un método para compilar el cual nos hará paquetes .deb y utilizaremos 15 núcleos para ello : 

![ref1]

Nos generara 4 paquetes .deb en el directorio superior :

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.013.jpeg)

Vamos a instalárnoslos , para ello haremos uso de un comodín para instalar  todos los .deb :

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.014.png)

Por ultimo vamos a asegurarnos de que el kernel se ha instalado :

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.015.png)



## Firmar un kernel

Como tengo el arranque seguro activado en el portátil sera necesario que firme el kernel para poder arrancarlo . 

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.016.png)

Así que para ello vamos a seguir los pasos que nos indica debian para realizarlo .

Si deseas saber qué claves están en uso en tu sistema, varias otras llamadas de mokutil te ayudarán, por ejemplo, sudo mokutil --list-enrolled para mostrar la lista actual de claves MOK

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.017.jpeg)

Para generarnos unas nuevas keys para firmar el kernel nos crearemos el siguiente directorio :

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.018.png)

Vamos a generarnos  la clave privada y certificado en formato DER

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.019.jpeg)

Ahora vamos a convertir el certificado DER a formato PEM:

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.020.png)

Ahora para inscribir una nueva clave MOK, primero emito la solicitud utilizando el comando mokutil. Ejecuto el siguiente comando:

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.021.png)

Durante este proceso, se me solicitará ingresar un "one-time password" (contraseña de un solo uso) para confirmar la inscripción. Esta contraseña es crucial para validar y autorizar la operación.

Luego de emitir la solicitud y proporcionar la contraseña, la inscripción de la clave no se completa de inmediato. En lugar de eso, necesito reiniciar el sistema.

Cuando reiniciemos nos aparecerá una pantalla azul , nos dirigiremos a la segunda opción enroll MOK:

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.022.jpeg)

Nos dirá si queremos añadir las llaves :

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.023.jpeg)

Y nos pedirá que pongamos la contraseña que hemos indicado de un solo uso :

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.024.jpeg)

Una vez hecho esto  reiniciamos el equipo : 

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.025.jpeg)

Una vez añadida la llave podemos comprobarlo con el siguiente comando :

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.026.png)

Para que DKMS (Dynamic Kernel Module Support) firme automáticamente los módulos del kernel, es necesario indicarle con qué clave debe firmar el módulo. Esto se realiza añadiendo dos valores de configuración al archivo "/etc/dkms/framework.conf", ajustando las rutas según sea necesario. 

Además añadiremos el siguiente script :

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.027.png)

El script tendrá el siguiente contenido :

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.028.png)

Ahora vamos a definir las variables necesarios para proceder a firmar el kernel , la de versión la hace con uname -r en la documentación de debian pero mis módulos tienen el prefijo 6.4.4 . Puedes comprobarlo en la ruta ls /lib/modules/ . 

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.029.png)

Ahora vamos a firmar el kernel :

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.030.png)

Una vez firmado el kernel podemos reiniciarlo y comprobar que arranca . A mi me ha tardado mas de lo normal al arrancarme pero en 2 min aproximadamente finalmente arranca .

![](../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.031.png)


[ref1]: ../img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.010.png
