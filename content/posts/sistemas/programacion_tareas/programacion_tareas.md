---
title: "Comandos programación de tareas en Linux"
date: 2023-09-20T10:00:00+00:00
description: En el ecosistema de Linux, un proceso es la ejecución de un programa específico que realiza una tarea particular. Cada proceso tiene su propio identificador único (PID) y está compuesto por un conjunto de recursos, como memoria y CPU, que le permiten funcionar de manera independiente.
tags: [Debian 12,sistemas,ISO,ASO]
hero: images/sistemas/comandos_procesos/portata_procesos.jpg
---
# Comandos programación de tareas en Linux

La gestión eficiente de tareas programadas es esencial para los administradores de sistemas, ya que facilita la ejecución automática de procesos rutinarios. En este contexto, contar con un conjunto sólido de comandos en Linux para programar y controlar tareas se convierte en una herramienta fundamental. 

## Comando sleep

El comando sleep pausa la ejecución en la terminal durante un intervalo de tiempo especificado antes de regresar a la línea de comandos. Puedes indicar el tiempo en segundos, minutos, horas o días. Este comando se encuentra en el paquete coreutils.

- s : segundos
- m : minutos
- h : horas
- d : días

Ej: sleep 10m –> esperar 10 min 

Por si solo no tiene ninguna utilidad , sin embargo es muy útil en Scripts .  Aquí un pequeño ejemplo :

date +"%H:%M:%S";sleep 5;date +"%H:%M:%S"

![](../img/Aspose.Words.cdeb5ac3-4737-4a2f-b87a-694716c02a3b.001.png)

## Comando watch

La utilidad watch es parte del paquete procps (o procps-ng) que está preinstalado en casi todas las distribuciones Gnu/Linux.

Cuando se usa sin argumentos, esta utilidad ejecutará el comando especificado cada dos segundos:

![](../img/Aspose.Words.cdeb5ac3-4737-4a2f-b87a-694716c02a3b.002.png)

![](../img/Aspose.Words.cdeb5ac3-4737-4a2f-b87a-694716c02a3b.003.png)

Podemos especificar el tiempo de repetición utilizando el parámetro -n , especificando el parámetro en segundos :

watch -n 5 date –> Cada 5 segundos 

Si queremos eliminar el encabezado , es decir que nos muestre cada cuanto tiempo se repite , utilizamos el parámetro -t :

![](../img/Aspose.Words.cdeb5ac3-4737-4a2f-b87a-694716c02a3b.004.png)

Si queremos poner un mensaje de error en caso de que el comando no pueda ejecutarse utilizamos el parámetro -e seguido del mensaje de error :

watch -e ‘error’

La opción -b de watch emite un pitido cada vez que el comando sale con un código de estado distinto de cero.

watch -b

Con el parámetro -d nos señala los cambios que han ocurrido en la ejecución del comando : watch -d

![](../img/Aspose.Words.cdeb5ac3-4737-4a2f-b87a-694716c02a3b.005.png)

## Comando at

Este comando se usa para ejecutar comandos a una determinada hora , principalmente se usa para programar tareas periódicas como puedes ser , copias de seguridad . 

Los principales parámetros son : 

- **V** :imprime el número de versión en el error estándar y sale con éxito.

- **m** :Enviar correo al usuario cuando el trabajo haya finalizado aunque no haya habido salida.        -M: Nunca envía correo al usuario.

- **f** :archivo Lee el trabajo desde un archivo en lugar de la entrada estándar.

- **t** :time Ejecuta el trabajo a la hora, dada en el formato [[CC]YY]MMDDhhmm[.ss]

- **l** :Es un alias para atq.

- **r** :Es un alias para atrm.

- **d**: Es un alias para atrm.

- **b**: Es un alias para batch.

- **v**: Muestra el tiempo que se ejecutará el trabajo antes de leerlo.

- **Los** tiempos mostrados estarán en el formato "Thu Feb 20 14:50:00 1997".

- **c** recoge los trabajos listados en la línea de comandos en la salida estándar.

Podemos programar tareas desde la linea de comandos , con echo :

echo "sh copia-seguridad.sh" | at 10:00 PM

Ha esta tarea se le asignara un numero automáticamente , para listar las tareas que tenemos invocamos el comando at sin ningún parámetro 

Si queremos borrar una tarea programada , utilizamos el parámetro -c seguido con el numero de la tarea a eliminar  .

Algunos ejemplos para programar tareas son :

- Dentro de 30 min : at now + 30 minutes
- 11AM del próximo 14 abril : at 11:00 AM April 14

## Comando crontab

El comando crontab se utiliza en sistemas UNIX para programar la ejecución de otros comandos, es decir, para automatizar tareas. Podemos ver los crontabs que se están programados y también editarlos, lógicamente.

Para verlos, utilizamos este comando: sudo crontab -l Para editarlos: sudo crontab -e

Las tareas cron siguen una determinada sintaxis. Tienen 5 asteriscos seguidos del comando a ejecutar. Ahora explicaré para qué sirve cada cosa.

\* \* \* \* \* /bin/ejecutar/script.sh

Los 5 asteriscos , de izquierda a derecha, los asteriscos representan:

- Minutos: de 0 a 59.
- Horas: de 0 a 23.
- Día del mes: de 1 a 31.
- Mes: de 1 a 12.
- Día de la semana: de 0 a 6, siendo 0 el domingo.

Si se deja un asterisco, quiere decir "cada" minuto, hora, día de mes, mes o día de la semana. 

Si queremos que un archivo se ejecute a las 5 de la mañana todos los días : 0 5 \* \* \* ruta\_absoluta\_del\_script

Para que se ejecute dos veces al día a las 6 AM Y a las 6  PM: 0 6,18 \* \* \* ruta\_absoluta\_del\_script

Muchas veces tenemos palabras reservadas para facilitar el uso de programas o lenguajes de programación. Cron no podía ser menos, así que tenemos algunas que suelen ser las más comunes. Ya cada uno que lo configure conforme a sus necesidades. Aquí van:

- @reboot: se ejecuta una única vez al inicio.
- @yearly/@annually: ejecutar cada año.
- @monthly: ejecutar una vez al mes.
- @weekly: una vez a la semana.
- @daily/@midnight: una vez al día.
- @hourly: cada hora.

También debemos conocer los usos de los parámetros :

crontab archivo.cron (establecerá el archivo.cron como el crontab del usuario)

crontab -e           (abrirá el editor preestablecido donde se podrá crear o editar el archivo crontab)   crontab -l           (lista el crontab actual del usuario, sus tareas de cron)

crontab -r           (elimina el crontab actual del usuario)

Cuando hagamos algún cambio deberemos de reiniciar el servicio para asegurarnos de que nuestros cambios surtan efecto :

service crond restart

Estos comandos nos dará la posibilidad de automatizar procesos , haciendo mas cómoda y amena  la administración de nuestros sistemas .

## Bibliografía

- [Comando watch ](https://ubunlog.com/comando-watch-algunas-formas-de-uso/)[Comando crontab](https://geekytheory.com/programar-tareas-en-linux-usando-crontab/)

