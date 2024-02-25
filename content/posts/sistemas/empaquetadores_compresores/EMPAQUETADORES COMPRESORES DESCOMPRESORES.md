---
title: "Empaquetadores y compresores en Linux"
date: 2023-09-08T10:00:00+00:00
description: Aprende cómo tratar ficheros comprimidos y empaquetados
tags: [Linux,Sistemas,ISO,ASO]
hero: images/sistemas/empaquetadores/portada.jpg
---

Los empaquetadores y compresores son elementos fundamentales en la gestión de archivos y datos en el ámbito informático. Los empaquetadores permiten agrupar varios archivos en un solo contenedor, facilitando su manipulación y transporte. Por otro lado, los compresores aplican técnicas para reducir el tamaño de los archivos, contribuyendo al ahorro de espacio de almacenamiento y agilizando la transferencia de datos. Estas herramientas desempeñan un papel crucial en la optimización de recursos y la eficiencia operativa al organizar, distribuir y respaldar información de manera más eficaz.

## TAR

Es un empaquetador de archivos que como su propio nombre indica utiliza el formato .tar, básicamente se utiliza para almacenar ficheros y directorios en un mismo archivo.

El nombre del paquete es tar .

### Crear un archivo .tar 

Puedes crear compresiones .tar tanto para un archivo como para directorios. Un ejemplo de este tipo de archivo es:

```bash
tar -cvf sampleArchive.tar /home/sampleArchive
```

Aquí /home/sampleArchive es el directorio que necesita ser comprimido creandosampleArchive.tar. Este comando usa las opciones –cvf que significan:

- c – crear un nuevo archivo .tar
- v – muestra una descripción detallada del progreso de la compresión
- f – nombre del archivo

### Crear un archivo .tar.gz

Si deseas una mejor compresión, también puedes usar .tar.gz. Un ejemplo de esto es:

```bash
tar -cvzf sampleArchive.tar.gz /home/sampleArchive
```

La opción adicional **z** representa la compresión gzip. Alternativamente, puedes crear un archivo .tgz que sea similar a tar.gz. Te mostramos un ejemplo de esto último a continuación:

```bash
tar -cvzf sampleArchive.tgz /home/sampleArchive 
```

### Crear un archivo .tar.bz2 

El archivo .bz2 proporciona más compresión en comparación con gzip. Sin embargo, esta alternativa tomará mas tiempo para comprimir y descomprimir. Para usarla, debes usar la opción -j. Un ejemplo de cómo se vería la operación es el siguiente:

```bash
tar -cvjf sampleArchive.tar.bz2 /home/sampleArchive
```

Dicha operación es similar a .tar.tbz o .tar.tb2. Te muestro  un ejemplo a continuación:

```bash
tar -cvjf sampleArchive.tar.tbz /home/sampleArchive tar -cvjf sampleArchive.tar.tb2 /home/sampleArchive
```

### Cómo descomprimir archivos .tar

El comando Tar de Linux también se puede utilizar para extraer un archivo. El siguiente comando extraerá los archivos en el directorio actual:

```bash
tar -xvf sampleArchive.tar
```

Si deseas extraer tus archivos a un directorio diferente, puedes usar la opción -C. Te mostramos un ejemplo de esto a continuación:

```bash
tar -xvf sampleArchive.tar -C /home/ExtractedFiles/
```
Puedes usar un comando similar para descomprimir archivos .tar.gz, tal como se muestra a continuación:

```bash
tar -xvf sampleArchive.tar.gz

tar -xvf sampleArchive.tar.gz -C /home/ExtractedFiles/
```

Los archivos .tar.bz2 o .tar.tbz o .tar.tb2 pueden descomprimirse de manera similar. Para esto deberás teclear el siguiente comando en la línea de comando:

```bash
tar -xvf sampleArchive.tar.bz2
```
### Cómo listar el contenido de un archivo .tar

Una vez que hayas creado el archivo, puedes listar el contenido mediante un comando similar al siguiente:

```bash
tar -tvf sampleArchive.tar
```

Esto mostrará la lista completa de archivos junto con las marcas de tiempo y los permisos. Del mismo modo, para .tar.gz, puedes usar un comando como:

```bash
tar -tvf sampleArchive.tar.gz
```

Esto también funcionaría para archivos .tar.bz2 como se muestra a continuación: tar -tvf sampleArchive.tar.bz2

### Cómo descomprimir un único archivo .tar

Una vez que creas un archivo comprimido, puedes extraer un único archivo de ese comprimido. Esto lo puedes lograr con el comando que te mostramos a continuación:

```bash
tar -xvf sampleArchive.tar example.sh
```

Aquí example.sh es un archivo único  que  se  extraerá del  comprimido sampleArchive.tar. Alternativamente, también puedes usar el siguiente comando:

```bash
tar --extract --file= sampleArchive.tar example.sh
```
Para extraer un solo archivo de un comprimido .tar.gz puedes usar un comando similar al mostrado a continuación:

```bash
tar -zxvf sampleArchive.tar.gz example.sh
```

O alternativamente:

```bash
tar --extract --file= sampleArchive.tar.gz example.sh
```
Para extraer un solo archivo de un comprimido .tar.bz2 puedes usar un comando como este: 

```bash
tar -jxvf sampleArchive.tar.bz2 example.sh
```
O, alternativamente, uno como este:

```bash
tar --extract --file= sampleArchive.tar.bz2 example.sh
```

### Cómo extraer múltiples archivos de los archivos .tar

En caso de que desees extraer varios archivos, usa el siguiente formato del comando:

```bash
tar -xvf sampleArchive.tar "file1" "file2" 
```

Para .tar.gz puedes usar:

```bash
tar -zxvf sampleArchive.tar.gz "file1" "file2" 
```

Para .tar.bz2 puedes usar:
```bash
tar -jxvf sampleArchive.tar.bz2 "file1" "file2"
```

### Extraer múltiples archivos con un patrón

Si deseas extraer del comprimido patrones específicos de archivos como solo los .jpg, usa el comando wildcards. Una muestra de dicho comando se muestra a continuación:
```bash
tar -xvf sampleArchive.tar --wildcards '\*.jpg' 
```

Para .tar.gz puedes usar:

```bash
tar -zxvf sampleArchive.tar.gz --wildcards '\*.jpg' 
```

Para .tar.bz2 puedes usar:

```bash
tar -jxvf sampleArchive.tar.bz2 --wildcards '\*.jpg'
```

### Cómo agregar archivos a un archivo .tar

Si bien puedes extraer archivos específicos, también puedes agregar archivos nuevos a un archivo comprimido existente. Para hacerlo, debes usar la opción -r que significa agregar. El comando Tar puede agregar tanto archivos como directorios.

A  continuación  se  muestra  un  ejemplo  en  el  que  estamos  agregando  example.jpg  al sampleArchive.tar existente.

```bash
tar -rvf sampleArchive.tar example.jpg
```

También podemos agregar un directorio. En el ejemplo que te mostramos a continuación, el directorio image\_dir se agrega al archivo sampleArchive.tar

```bash
tar -rvf sampleArchive.tar image\_dir
```

No puedes agregar archivos o carpetas a comprimidos .tar.gz o .tar.bz2.

### Cómo verificar un archivo .tar 

Usando Tar puedes verificar un archivo. Esta es una de las formas en que puedes hacerlo:

```bash
tar -tvf sampleArchive.tar
```

Esto no se puede aplicar en archivos .tar.gz o .tar.bz2.

### Cómo verificar el tamaño del archivo .tar

Una vez que crees un archivo, puedes verificar su tamaño. Este se mostrará en KB (Kilobytes).

A continuación te mostramos varios ejemplos del comando a usar para verificar el tamaño de diferentes tipos de archivos comprimidos:

```bash
tar -czf - sampleArchive.tar | wc -c
tar -czf - sampleArchive.tar.gz | wc -c tar -czf - sampleArchive.tar.bz2 | wc -c
```

## GZIP

Puede comprimir un archivo usando  gzip con el comando llamado gzip . El nombre de este paquete es gzip .

Este es el uso más simple: gzip filename

Esto comprimirá el archivo y agregará un .gz extensión a ella. Se elimina el archivo original. Para evitar esto, puede utilizar el- c y use la redirección de salida para escribir la salida en elfilename.gzexpediente:

```bash
gzip -c filename > filename.gz
```

los -c La opción especifica que la salida irá al flujo de salida estándar, dejando el archivo original intacto o puede usar el -k opción: 

```bash
gzip -k filename
```

Hay varios niveles de compresión. Cuanto mayor sea la compresión, más tiempo llevará comprimir (y descomprimir). Los niveles van de 1 (más rápido, peor compresión) a 9 (más lento, mejor compresión), y el valor predeterminado es 6.

Puede elegir un nivel específico con el -<NUMBER> opción:

```bash
gzip -1 filename
```

Puede comprimir varios archivos enumerándolos:

```bash
gzip filename1 filename2
```

Puede comprimir todos los archivos de un directorio, de forma recursiva, utilizando el -r : 

```bash
gzip -r folder
```

gziptambién se puede utilizar para descomprimir un archivo, utilizando el -d opción: 

```bash
gzip -d filename.gz
```

## BZIP2

El bzip2 es muy similar al programa gzip. La principal diferencia es que utiliza un algoritmo de compresión diferente llamado algoritmo de compresión de texto de clasificación de bloques Burrows-Wheeler y codificación Huffman. Los archivos comprimidos con bzip2 finalizarán con la extensión .bz2.

Como dije, el uso de bzip2 es casi lo mismo que gzip. Simplemente tendremos que reemplazar gzip en los ejemplos anteriores por bzip2, gunzip por bunzip2, zcat con bzcat y así sucesivamente.

**Para comprimir un archivo usando bzip2, reemplazándolo por una versión comprimida, ejecutaremos:**
```bash
bzip2 prueba.txt # Nos creara un archivo prueba.txt.bz2 
```
**Comprimir los archivos sin eliminar el archivo original**

Si no queremos reemplazar el archivo original, utilizaremos la opción -c y escribiremos el resultado en un nuevo archivo.

```bash
Bzip2 -c prueba.txt  # prueba.txt.bz2
```

**Descomprimir archivos**

Para descomprimir un archivo comprimido utilizaremos alguna de las dos siguientes posibilidades: 

```bash
bzip2 -d prueba.txt.bz2
bunzip2 prueba.txt.bz2
```

**Ver el contenido de los archivos comprimidos sin descomprimirlos**

Para ver el contenido de un archivo comprimido sin descomprimirlo, no tendremos más que utilizar cualquiera de las opciones:

```bash
bunzip2 -c ubunlog.txt.bz2 bzcat ubunlog.txt.bz2
```

## XZ

El paquetes es xz-utils

**Comprimir**

El ejemplo más simple de compresión de un archivo con xz es el siguiente. Compresión de archivos con XZ

```bash
xz  deb.iso
```

También se puede utilizar la opción -z para realizar la compresión:

```bash
xz -z  deb.iso
```

Estas órdenes comprimirán el fichero, pero eliminará el archivo origen. Si no buscamos borrar los archivos de origen, usaremos la opción -k de la siguiente manera:

```bash
xz -k deb.iso
```

**Descomprimir**

Para descomprimir un archivo, vamos a poder utilizar la opción -d: 

```bash
xz -d deb.iso
unxz deb.iso
```

**Forzar compresión**

Si una operación falla, por ejemplo, si existe un archivo comprimido con el mismo nombre, usaremos la opción -f para forzar el proceso:

```bash
xz -kf deb.iso
```

**Establecer niveles de compresión**

Esta herramienta admite diferentes niveles preestablecidos de compresión (de 0 a 9. Con un valor predeterminado de 6). También vamos a poder utilizar alias como –fast (será rápido, pero con menos compresión) para establecer como valor 0 y –best para establecer como valor 9 (compresión lenta pero más alta). Algunos ejemplos de cómo establecer estos niveles, son los siguientes:

```bash
xz -k -8 deb.iso
xz -k --best deb.iso 
```

**Limitar la memoria**

En caso de tener una cantidad pequeña de memoria del sistema y querer comprimir un archivo enorme, vamos a tener la posibilidad de utilizar la opción -memory = límite (el valor límite puede estar en MB o como porcentaje de RAM) para establecer un límite de uso de memoria para la compresión:

```bash
xz -k --best --memlimit-compress=10% deb.iso
```


**Habilitar modo silencioso**

Si nos interesa ejecutar la compresión en modo silencioso solo habrá que añadir la opción -q. También podremos habilitar el modo detallado con -v, como se muestra a continuación:

```bash
xz -k -q deb.iso
xz -k -qv deb.iso
```

**Crear un archivo tar.xz**

El siguiente es un ejemplo del uso para conseguir un archivo con la extensión tar.xz. 

```bash
tar -cf *.txt | xz -7 > deb.tar.xz
```

Crear un archivo tar.xz opción 2

```bash
tar -cJf deb.tar.xz *.txt
```

**Comprobar la integridad de los archivos comprimidos**

Podremos probar la integridad de los archivos comprimidos utilizando la opción -t. Utilizando -l podremos ver la información sobre un archivo comprimido.

```bash
xz -t deb.tar.xz xz -l deb.tar.xz
```

## 7Z

Este compresor cuenta con dos paquetes :

- p7zip ofrece soporte para 7zr (una versión ligera de 7z y 7za). Permite comprimir y descomprimir paquetes en estos formatos mediante la herramienta gráfica de tu sistema (file-roller en Ubuntu y Debian) pero no dispone de la funcionalidad de cifrado.
- p7zip-full es, por decirlo de algún modo, la versión más completa. Soporta los formatos 7z y 7za e incorpora la funcionalidad de cifrado, además de las herramientas para la compresión 

## ZIP

**Comprimir Uno o Varios Archivos**

El formato es siempre es la misma, consiste en colocar 7z, seguido de la opción a (para comprimir o empaquetar), seguido del nombre que quieres dar al paquete final (no hace falta colocar la extensión .7z) y acabando con el nombre del archivo a comprimir. Podrás observar que 7-Zip es capaz de aprovechar todos los núcleos de tu procesador durante la operación.

```bash
7z a paquete-comprimido archivo-a-comprimir 7z a paquete-comprimido archivo-1 archivo-2
```

Si queremos ponerle contraseña utilizamos el parámetro -p : 

```bash
7z  a -p paquete-comprimido archivo-a-comprimir
```

7-Zip soporta varios formatos de compresión o empaquetado, aparte del suyo propio, con esta sentencia podrás optar por indicar explícitamente que formato quieres utilizar (puedes escoger entre 7z, zip, gzip, bzip2 o tar).

```bash
7z a -tgzip paquete-comprimido archivo-a-comprimir
```

**Listar Contenido de la Carpeta Comprimido**

Otra opción interesante puede ser listar el contenido dentro de un archivador y ver los detalles. Para ello tienes que situarte igualmente en el directorio en el que se encuentra el archivador o carpeta comprimida y teclear la siguiente sentencia.

```bash
7z l paquete-comprimido.7z
```

**Descomprimir Paquete y Extraer Ficheros**

Una vez conocido el contenido dentro del archivador, para extraer de golpe todo el contenido dentro del directorio de trabajo actual, puedes valerte del siguiente comando:

```bash
7z e paquete-comprimido.7z
```

**Comprobar Integridad de los Datos**

Como opción adicional, también puedes comprobar la integridad de los diferentes archivos que se encuentran dentro del fichero comprimido. Para ello utiliza esto:

```bash
7z t paquete-comprimida.7z
```

## RAR

El paquete para instalarlo es rar .

**Cómo comprimir RAR en Linux**

Para comprimir un fichero o todos los de una carpeta:

```bash
rar a nombre_fichero_comprimido.rar nombre_fichero_a_comprimir rar a nombre_fichero_comprimido.rar 
```
**Cómo descomprimir RAR en Linux**

Y para descomprimir en el mismo directorio o en otro diferente: 

```bash
unrar x nombre\_del\_rar.rar

unrar x nombre\_del\_rar.rar /ruta/destino/descomprimido

```

## ZIP

El nombre del paquete es zip.

Para comprimir archivos : 

```bash
zip archivo.zip archivos
```

Para descomprimir archivos : 

```bash
unzip archivo.zip
```

Ver contenido :

```bash
unzip -v archivo.zip
```

## Bibliografía

- [Guía comando tar ](https://www.hostinger.es/tutoriales/como-usar-comando-tar-linux)
- [Guía comando gzip ](https://tech-wiki.online/es/linux-command-gzip.html)
- [Guía comando bzip2 ](https://ubunlog.com/comprimir-descomprimir-gzip-bzip2/#El_programa_bzip2)
- [Guía xz](https://ubunlog.com/compresion-xz-datos-sin-perdidas/)
- [Guía comando 7z ](https://computernewage.com/2016/01/10/7-zip-linux-guia-para-comprimir-y-descomprimir-archivos/#instalar-7-zip)
- [Guía comando rar](https://www.linuxadictos.com/tutorial-para-instalar-rar-en-linux-y-aprender-utilizarlo.html)

