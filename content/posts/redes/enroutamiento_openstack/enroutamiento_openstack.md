---
title: "Enrutamiento en OpenStack"
date: 2023-09-08T10:00:00+00:00
description: Enrutamos un escenario desplegado usando la orquestación de OpenStack
tags: [Redes, Enrutamiento]
hero: images/redes/enrutamiento_os/portada.png
---
En esta práctica, exploraremos la creación de un escenario mediante la orquestación de OpenStack y, posteriormente, llevaremos a cabo el enrutamiento para asegurar la conectividad entre las distintas máquinas virtuales. Este ejercicio nos permitirá comprender y aplicar el uso de OpenStack para gestionar entornos virtuales, además de configurar la red de manera eficiente para facilitar la comunicación entre los diferentes dispositivos en el escenario.

## Escenario a montar en OpenStack

Para poder montar nuestro escenario en OpenStack debido a la situación actual de las imágenes que hay disponibles , necesitaremos preparar una instancia la cual tenga habilitado el acceso por contraseña . Además si posteriormente a partir de una queremos configurar otra habilitar el acceso ssh por contraseña para este usuario . 

Esta tendremos que crearla con el mismo flavour con las que generaremos el escenario para evitar errores .

Cuanto tengamos  a punto nuestra instancia comprobaremos que puedes iniciar sesión desde horizon :

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.001.png)

Ahora crearemos una instantánea :

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.002.png)

Copiaremos el ID de las instantánea :

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.003.png)

Y lo añadiremos al fichero :

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.004.png)

Y lo desplegaremos :

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.005.png)

Vemos que se ha creado correctamente :

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.006.jpeg)

## Esquema gráfico de la configuración

El esquema quedaría de la siguiente manera : 

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.007.png)

Teniendo la siguiente relación de IPS :

| MAQUINA | IP             | INTERFAZ |
| ------- | -------------- | -------- |
| PC1     | 10.0.100.144   | &nbsp; ens3     |
| R1-PC1  | 10.0.100.68    | &nbsp; ens3     |
| R1-R2   | 10.0.110.78    | &nbsp; ens4     |
| R2-R1   | 10.0.110.30    | &nbsp; ens3     |
| R2-PC2  | 10.0.120.191   | &nbsp; ens4     |
| PC2     | 10.0.120.203   | &nbsp; ens3     |
| R2-R3   | 10.0.130.146   | &nbsp; ens5     |
| R3-R2   | 10.0.130.36    | &nbsp; ens3     |
| R3-PC3  | 10.0.140.127   | &nbsp; ens4     |
| PC3     | 10.0.140.158   | &nbsp; ens3     |



<a name="_page5_x56.70_y68.70"></a>**Tablas de enrutamiento**



| R1          |          |          |
| ----------- | :------: | :------: |
| 10.0.100.0/24 &nbsp; | 0.0.0.0 | &nbsp;  ens3    &nbsp;|
| 10.0.110.0/24 &nbsp; | 0.0.0.0 |  &nbsp; ens4    &nbsp;|
| 10.0.120.0/24 &nbsp; | 10.0.110.30 | &nbsp; ens4 &nbsp;|
| 10.0.130.0/24 &nbsp; | 10.0.110.30 | &nbsp; ens4 &nbsp;|
| 10.0.140.0/24 &nbsp; | 10.0.110.30 | &nbsp; ens4 &nbsp;|
| 0.0.0.0/0   &nbsp; | 10.0.110.30 | &nbsp; ens4   &nbsp;|


\*Las redes en las que estamos directamente conectados se crearan automáticamente las rutas.


| R2          |          |           |
| ----------- | :------: | :-------: |
| 10.0.100.0/24 &nbsp; | 10.0.110.178 | &nbsp; ens3 &nbsp;|
| 10.0.110.0/24 &nbsp; | 0.0.0.0 |  &nbsp;     ens3 &nbsp;|
| 10.0.120.0/24 &nbsp; | 0.0.0.0 |    &nbsp;   ens4 &nbsp;|
| 10.0.130.0/24 &nbsp; | 0.0.0.0 |    &nbsp;   ens5 &nbsp;|
| 10.0.140.0/24 &nbsp; | 10.0.130.36 |&nbsp; ens5   &nbsp;|
| 0.0.0.0/0  &nbsp;  | 10.0.130.36 | &nbsp; ens5    &nbsp;|


*Las redes en las que estamos directamente conectados se crearan automáticamente las rutas.

|R3|||
| - | :- | :- |
|10\.0.100.0/24 &nbsp;|10\.0.130.146|&nbsp; ens3 &nbsp;|
|10\.0.110.0/24 &nbsp;|10\.0.130.146|&nbsp; ens3 &nbsp;|
|10\.0.120.0/24 &nbsp;|10\.0.130.146|&nbsp; ens3 &nbsp;|
|10\.0.130.0/24 &nbsp;|0\.0.0.0|&nbsp; ens3 &nbsp;|
|10\.0.140.0/24 &nbsp;|0\.0.0.0|&nbsp; ens4 &nbsp;|
|0\.0.0.0/0 &nbsp; |10\.0.130.146|&nbsp; ens4 &nbsp;|

## Comandos de configuración de cada nodo

### Router 1

Como es un router deberemos de activar el bit de forwarding para ello introduciremos el siguiente comando :
```bash
echo 1 > /proc/sys/net/ipv4/ip\_forward
```

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.008.png)

Crearemos la tabla de enrutamiento :

Las rutas estáticas :

```bash
ip route add 10.0.100.0/24 via 0.0.0.0 dev ens3
```

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.009.png)

La ruta por defecto:

```bash
ip route add default via 10.0.110.30 dev ens4
```

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.010.png)

Nos quedaría así la tabla de enrutamiento :

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.011.png)

### PC1

Borraremos la ruta por defecto que exista en el dispositivo 

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.012.png)

Y añadiremos la nueva ruta 

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.013.png)


### Router 2

Como es un router deberemos de activar el bit de forwarding para ello introduciremos el siguiente comando :

```bash
echo 1 > /proc/sys/net/ipv4/ip\_forward
```

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.014.png)

Crearemos la tabla de enrutamiento :

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.015.png)

Quedaría así :

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.016.png)

### PC2**

Al igual que hicimos anteriormente eliminaremos la ruta por defecto que trae y la añadiremos la nueva :![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.017.png)![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.018.png)

Activaremos el bit de forwarding con el siguiente comando :

```bash
echo 1 > /proc/sys/net/ipv4/ip\_forward
```

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.019.png)

Crearemos la tabla de enrutamiento para nuestro escenario :

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.020.png)

La tabla de enrutamiento quedaría así :

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.021.png)

### PC3

Al igual que con los demás deberemos de cambiar la ruta por defecto por la ip del router a la que estamos conectado :

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.022.png)



## Resumen de configuración y aclaraciones 

### Para los routers 

1. Activar el bit de forwarding 
2. Crear las tablas de enrutamiento
3. Modificar la ruta por defecto

### Para los PCs 

1. Modificar la ruta por defecto

Lo de modificar la ruta por defecto , es debido a que no puedo modificar la configuración de las tarjetas de red por lo  que no puedo modificar la puerta de enlace . 

Por defecto al utilizar el script esta viene con la puerta de enlace X.X.X.1 sin embargo esta no coincide con la puerta de enlace de los clientes .

Para los routers debemos de modificarla también para indicar por donde mandaremos el trafico “por defecto”.

Si queremos hacer que el bit del forwarding se guarde permanentemente para que cuando reiniciemos el equipo este no vuelva a 0 :

–> Escribimos directamente  en el archivo /etc/sysctl.conf:

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.023.png)

Si queremos volcar en un archivo la configuración de las tablas de enrutamiento para tener una copia de seguridad de las mismas usamos :

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.024.png)

Si queremos restaurar la copia :

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.025.png)



## Verificación de conectividad (ping) entre nodos


### PC1

PC1 – PC2

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.026.png)

PC1-PC3

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.027.png)

### PC2
 
PC2-PC1

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.028.png)

PC2-PC3

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.029.png)

### PC3

PC3-PC1

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.030.png)

PC3-PC2

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.031.png)

## Captura de tráfico en el router r2 o r3 mostrando tráfico entre h1 y h3.

Para hacer una captura de una determinada interfaz y guardarla en un archivo utilizaremos tcpdump:

```bash
tcpdump -i NOMBRE\_INTERFAZ -w NOMBRE\_ARCHIVO
```

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.032.png)

Si queremos tener una salida al comando en lugar de guardar el archivo usaremos el parámetro -n: Aquí vemos como llegan los ICMP REQUEST de PC3 a PC1 y los ICMP REPLY DE PC1 a PC3

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.033.png)

Además he capturado una petición y respuesta arp de PC3:

![](../img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.034.png)

## Bibliografía

- [Como hacer tablas de enrutamiento](https://docs.aws.amazon.com/es_es/vpc/latest/userguide/VPC_Route_Tables.html)

