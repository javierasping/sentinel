---
title: "Gestión de Procesos en Linux"
date: 2023-09-08T10:00:00+00:00
description: En el ecosistema de Linux, un proceso es la ejecución de un programa específico que realiza una tarea particular. Cada proceso tiene su propio identificador único (PID) y está compuesto por un conjunto de recursos, como memoria y CPU, que le permiten funcionar de manera independiente.
tags: [Debian 12,Sistemas,ISO,ASO]
hero: images/sistemas/comandos_procesos/portata_procesos.jpg
---
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GVDYVWJLRH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GVDYVWJLRH');
</script>

En el ecosistema de Linux, un proceso es la ejecución de un programa específico que realiza una tarea particular. Cada proceso tiene su propio identificador único (PID) y está compuesto por un conjunto de recursos, como memoria y CPU, que le permiten funcionar de manera independiente.

En el universo de Linux, la gestión efectiva de procesos es una habilidad crucial para optimizar el rendimiento y asegurar la estabilidad del sistema. Este post te sumergirá en los fundamentos esenciales de la gestión de procesos

## PS

Si no añadimos ningún parámetro, ps mostrará los procesos del usuario con el que estamos logueados. Por otra parte, los parámetros más básicos a conocer son los siguientes:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.001.png)

**aux** : Lista los procesos de todos los usuarios con información añadida (destacamos más abajo).

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.002.png)

**-a** Lista los procesos de todos los usuarios.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.003.png)

**-u** Lista información del proceso como por ejemplo el usuario que lo está corriendo, la utilización de CPU y memoria, etc.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.004.png)

**-x** Lista procesos de todas las terminales y usuarios

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.005.png)

**-l** Muestra información que incluye el UID y el valor «nice«.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.006.png)

**–-forest**  Muestra el listado procesos en un formato tipo árbol que permite ver como los procesos interactúan entre si, podría ser algo similar al comando pstree.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.007.png)

## PSTREE

El programa pstree facilita información sobre la finalización de una serie de procesos relacionados entre sí, esto es, todos los descendientes de un proceso particular. El programa deja claro desde un principio que proceso es el primario y cuales son los secundarios. Esto evita buscar las relaciones entre los diversos procesos de manera manual.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.008.png)

Parámetros comúnmente utilizados :

**-H**: Si nos interesa podemos ver el árbol de un proceso específico:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.009.png)

**-g**: Nos agrupara los procesos por grupos :

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.010.png)

**-n**: Nos permite ordenar la salida por el numero de PID:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.011.png)

**-p**: Muestra el numero de PID

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.012.png)

**-s**:Muestra los procesos padres  

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.013.png)

## SYSTEMCTL STATUS

Este comando se utiliza para ver el estado en el que se encuentra un servicio , Específicamente, muestra información sobre si el servicio o unidad está activo o inactivo, y si está en ejecución o detenido. También muestra cualquier mensaje de error o advertencia relacionado con el servicio o unidad. Este comando es útil para verificar el estado de un servicio o unidad en el sistema y para resolver problemas relacionados con ellos.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.014.png)

## TOP

Es un programa todo en uno: simultáneamente cumple las funciones de ps y kill. Es un comando de modo consola, por lo que debe iniciarlo desde una terminal . 

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.015.png)

Dentro de este podemos controlarlo usando las siguientes teclas:

**-k**: este comando se usa para enviar una señal a un proceso. Luego, top le preguntará por el PID del proceso, seguido del número de la señal a enviar (predeterminadamente TERM — o 15);

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.016.png)

**-M**: este comando se usa para ordenar el listado de los procesos de acuerdo a la memoria que usan (campo %MEM);

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.017.png)

**-P**: este comando se usa para 

ordenar el listado de procesos de acuerdo al tiempo de CPU que consumen(campo %CPU; este es el método de ordenamiento predeterminado);

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.018.png)

**-u**: este comando se usa para mostrar los procesos de un usuario en particular, top le preguntará de cual. Debe ingresar el nombre del usuario. 

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.019.png)

**-i**: este comando actúa como un interruptor; predeterminadamente se muestran todos los procesos, incluso los que están dormidos; este comando asegura que se muestran sólo los procesos que están en curso de ejecución :

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.020.png)

## HTOP

Htop es la version mejorada y actual de top la cual tiene una interfaz mas amigable y mas funcionalidades las cuales nos ayudaran a la supervisión de procesos . Este se divide en varias partes :

El encabezado divide la parte superior de la interfaz en secciones izquierda y derecha. Estos muestran el uso de la CPU/memoria, el espacio de intercambio, el tiempo de actividad de la máquina, las tareas y la carga promedio.

La sección superior izquierda muestra una línea para cada núcleo de CPU. Por ejemplo, la captura de pantalla anterior muestra dos núcleos de CPU, con el porcentaje que representa la carga en cada uno.

También puede ver el código de colores proporcionado por htop para identificar qué tipo de procesos utilizan la CPU:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.021.png)

- Rojo: porcentaje ocupado por procesos del sistema 
- Azul: porcentaje ocupado por proceso de baja prioridad
- Verde: porcentaje ocupado por procesos de usuario

Las líneas de memoria también usan códigos de colores, esta vez para representar:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.022.png)

- Amarillo: porcentaje ocupado por caché contenido
- Verde: porcentaje ocupado por la memoria utilizada
- Azul: porcentaje ocupado por contenido buffer

El panel central muestra todos los procesos en ejecución con sus estadísticas asociadas según la utilización de la CPU. Muestra la siguiente información para cada proceso:

- ID de proceso (PID) 
- El propietario (Usuario) 
- Consumo de memoria virtual porcentaje de procesador memoria física

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.023.png)

Para finalizar este programa también es interactivo , abajo tenemos un índice donde podemos comprobar las funciones que nos permite usar :

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.024.png)

Además disponemos de varios atajos de teclados :

- u Ordenar procesos por nombre de usuario
- p Alternar con la ruta del programa
- F2 o S Entrar en Configuración
- F3 o / Proceso de búsqueda
- F5 o t Vista ordenada o de árbol
- F6 +/- Seleccione el proceso principal para expandir/contraer el árbol
- F7 o [ Aumentar la prioridad solo para root
- F8 o ] Prioridad baja (bueno +)
- F9 o k Matar proceso
- H Alterna con subprocesos de proceso de usuario
- K Alterna con subprocesos de proceso del kernel

## &

El símbolo & es un operador de shell en Unix y Linux que permite ejecutar un proceso en segundo plano. Al colocar & al final de un comando, se ejecutará el proceso en segundo plano y se le asignará una tarea en segundo plano. Esto significa que el proceso se ejecutará en paralelo con otras tareas y no bloqueará la terminal o la línea de comandos hasta que finalice.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.025.png)

## JOBS

Este comando listara los procesos que se encuentran en segundo pano así como su estado , nos permite saber su PID:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.026.png)

## FG

Complementando al comando anterior , este nos permite reanudar en primer plano el último trabajo que fue suspendido.:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.027.png)

Listando con jobs podemos mandar un proceso en especifico a primer plano :

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.028.png)

## BG

Cuando un comando se está ejecutando puedes suspenderlo usando ctrl-Z. El comando se detendrá inmediatamente, y volverás al shell de la terminal.

Puedes reanudar la ejecución del comando en segundo plano, así que seguirá ejecutándose pero no te impedirá hacer otro trabajo en la terminal.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.029.png)

## KILL

Los procesos de Linux pueden recibir señales y reaccionar a ellas. Esa es una forma en la que podemos interactuar con los programas en ejecución. El programa kill puede enviar una variedad de señales a un programa. No sólo se usa para terminar un programa, como el nombre lo sugiere, sino que es su principal trabajo Por defecto, este manda una señal TERM al identificador de proceso indicado.

Podemos listar las señales con kill -l :

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.030.png)

Mandamos una señal con el parámetro -s seguida del numero de esta y el PID del proceso :

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.031.png)

## XKILL

Este es el método más sencillo y el más práctico. El cursor del mouse se transformará en una pequeña calavera. Todo lo que resta es hacer clic en la ventana que querés cerrar y voilá. Chau proceso.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.032.png)

## KILLALL

Similar al comando kill, killall enviará la señal a múltiples procesos a la vez en lugar de enviar una señal a un identificador de proceso específico . Por ejemplo, puedes tener múltiples instancias del programa top en ejecución, y killall top terminará con todos ellos.

Puedes especificar la señal, como con kill :

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.033.png)

Por ejemplo podemos matar todos los tops :

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.034.png)

## PIDOF

Te permite encontrar el ID del proceso de un programa en ejecución:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.035.png)

**-s**: Petición única - ordena al programa devolver un único identificador de proceso

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.036.png)

## PID BASH

**echo t$$ → id bash**

Es una forma rápida de encontrar el identificador actual de la bash :

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.037.png)

## NICE

Ejecuta un comando con una prioridad determinada, o modifica la prioridad a de un proceso (programa en ejecución). Utiliza una prioridad variable que parte de la prioridad del shell y suma o resta valores. Mientras menor es el valor de la prioridad mayor prioridad tiene el proceso.

El valor de la prioridad del proceso find aumenta en 5, disminuye su prioridad.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.038.png)

## RENICE

Sirve para cambiar la prioridad de un proceso :

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.039.png)

## PKILL

Este comando nos permite matar un proceso del que conocemos su nombre completo o parte de él. Veamos un ejemplo:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.040.png)

## Bibliografía

- [Guía de uso pstree](https://www.ochobitshacenunbyte.com/2018/06/04/visualizar-arbol-de-procesos-en-linux-con-pstree/)
- [Guía de uso envío de señales ](https://ergodic.ugr.es/cphysn/LECCIONES/UNIX/Command-Line10.pdf)
- [Guía de uso htop](https://blog.elhacker.net/2022/01/top-sustituye-htop-y-monitoriza-procesos-recursos-servidores-linux-tiempo-real.html)
- [Guía de uso nice , renice , kill ...](https://www.digitalocean.com/community/tutorials/how-to-use-ps-kill-and-nice-to-manage-processes-in-linux-es)

