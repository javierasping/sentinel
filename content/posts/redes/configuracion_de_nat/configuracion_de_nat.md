---
title: "Configuración de NAT Cisco y Linux"
date: 2023-09-08T10:00:00+00:00
description: Enrutamiento de un escenario con direcciones públicas, configuramos SNAT y DNAT en máquinas Linux y Cisco.
tags: [Redes, Enrutamiento, NAT, SNAT, DNAT, Cisco, Linux]
hero: images/redes/configuracion_nat/portada.png
---

En este artículo, exploraremos la configuración de SNAT (*Source Network Address Translation*) y DNAT (*Destination Network Address Translation*) en escenarios con direcciones públicas, haciendo uso de routers en entornos Linux y dispositivos Cisco.

## Escenario con máquinas Debian

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.001.jpeg)

### Preparación del entorno

#### Instalación de paquetes

Una vez desplegadas las máquinas, deberemos descargar Apache para los servidores web. Para realizar esto, conectaremos ambos servidores a un switch y este a la nube NAT para disponer de acceso a internet.

Primero actualizaremos los repositorios ejecutando `apt update`:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.002.png)

A continuación, ya podremos descargar los paquetes. Para los servidores, instalaremos Apache:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.003.png)

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.004.png)

Y para el router de casa, descargaremos el servidor DHCP:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.005.png)

Al finalizar la instalación, aparecerá un código de error similar a este, debido a que aún no hay una configuración válida en el servicio:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.006.jpeg)

Por ahora ignoraremos este mensaje y posteriormente configuraremos el servidor DHCP.

Con esto habríamos instalado todos los paquetes necesarios para la práctica, por lo que podemos proceder a montar el escenario.

#### Configuración de las tarjetas de red

Nos encontraremos con un pequeño obstáculo al montar el escenario, ya que necesitamos que algunos routers tengan más de una tarjeta de red.

Para añadir más de una tarjeta (con el dispositivo apagado y sin conexiones), hacemos clic derecho y seleccionamos **Configure** $\rightarrow$ **Network**, y elegimos el número de adaptadores necesarios. Por ejemplo, para el router de casa necesitamos dos adaptadores:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.007.jpeg)

Una vez configuradas las máquinas que requieren múltiples tarjetas, montaremos el escenario y procederemos a configurar sus interfaces.

Para modificar la configuración de las tarjetas de red, editaremos el fichero `/etc/network/interfaces`. Para aplicar los cambios realizados, tenemos varias opciones:

**Subir y bajar la tarjeta modificada:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.008.png)

También podemos reiniciar el servicio de *networking*, lo cual aplicará los cambios a todas las tarjetas simultáneamente y nos ahorrará tiempo:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.009.png)

**Router CASA:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.010.jpeg)

**Router R1:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.011.jpeg)

**Router ISP:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.012.jpeg)

**Router R2:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.013.jpeg)

Esta es la relación de IPs de las tarjetas de red de los routers. Para aplicar esta configuración, deberemos reiniciar la red, como se indicó anteriormente.

Para que el escenario funcione, debemos activar el *bit de forwarding* en estos cuatro routers. Lo haremos de forma permanente editando el fichero `/etc/sysctl.conf` y descomentando la siguiente línea:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.014.png)

#### Rutas necesarias

Para el esquema actual, las rutas necesarias en los routers son:

**Router R1:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.015.png)

**Router ISP:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.016.png)

**Router R2:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.017.png)

**Router CASA:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.018.png)

#### Comprobación de conectividad

Realizaremos un `ping` desde cada uno de los routers hacia sus extremos más lejanos para asegurar que el enrutamiento es correcto.

**Router R1 $\rightarrow$ R2:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.019.png)

**Router R1 $\rightarrow$ CASA:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.020.png)

**Router R2 $\rightarrow$ R1:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.021.png)

**Router R2 $\rightarrow$ CASA:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.022.png)

**Router CASA $\rightarrow$ R1:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.023.png)

Observamos que todos los dispositivos con direcciones IP públicas tienen conectividad entre sí. Sin embargo, los dispositivos con direccionamiento privado no tendrán conectividad, ya que las direcciones privadas no se enrutan en los routers de internet.

Es decir, si lanzamos un `ping` hacia una dirección privada de otra red (por ejemplo, del servidor 1 al servidor 2), este no llegará, ya que en las tablas de enrutamiento del router ISP no existen rutas para direcciones privadas.

Por lo tanto, será imposible alcanzar una red privada diferente a la propia.

Por ejemplo, desde casa, si hacemos `ping` a Google, lo hacemos a la dirección pública `8.8.8.8`, no a la dirección privada que tenga el servidor (que podría ser, por ejemplo, `172.22.1.15`).

### Configuración del servicio DHCP en el router CASA

Retomando la instalación de paquetes, ya hemos descargado el servidor DHCP para Debian (`isc-dhcp-server`). Ahora procederemos a configurarlo.

Primero debemos indicar al servidor a través de qué tarjeta de red queremos repartir las direcciones IP. En nuestro caso, es la tarjeta `ens5`.

Para ello, editaremos el fichero `/etc/default/isc-dhcp-server` y añadiremos el nombre de la tarjeta en la sección de IPv4:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.025.jpeg)

Ahora indicaremos al servidor DHCP la configuración que debe asignar a los clientes editando el fichero `/etc/dhcp/dhcpd.conf`. Podemos basarnos en uno de los ejemplos comentados:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.026.png)

Este es un ejemplo sencillo de servidor DHCP, suficiente para nuestro escenario. Los campos significan:

- **subnet**: Dirección de red de la cual queremos repartir direcciones IP.
- **netmask**: Máscara de red de la red a configurar.
- **range**: Rango de direcciones IP a distribuir (inicial y final).
- **option routers**: Puerta de enlace de nuestra red.
- **option broadcast-address**: Dirección de *broadcast* de nuestra red.

Una vez configurados los parámetros, reiniciaremos el servicio:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.027.png)

Y comprobaremos que el servicio esté activo:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.028.jpeg)

Para que los clientes reciban una dirección mediante este servicio, configuraremos las tarjetas de red de PC1 y PC2 de la siguiente manera:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.029.png)

Reiniciamos el servicio para aplicar los cambios y el servidor nos asignará automáticamente la configuración de red:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.030.png)

Comprobamos que efectivamente se ha asignado la configuración:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.031.jpeg)

También podemos hacer un seguimiento de las asignaciones de IP consultando el archivo `/var/lib/dhcp/dhcpd.leases`, que guarda las concesiones realizadas.

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.032.png)

Podemos ver la fecha de inicio y a quién se le ha asignado mediante su dirección MAC:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.033.jpeg)

### Configuración de NAT

#### Router CASA

Configuraremos el SNAT en el router de casa. Según el esquema actual, la regla es:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.034.png)

Para que la regla persista tras un reinicio, la añadiremos al fichero `/etc/network/interfaces`:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.035.png)

Podemos verificar que se ha aplicado tras reiniciar el servicio de *networking*:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.036.png)

Comprobaremos que la regla funciona lanzando un `ping` a otra red (R1) y verificando si cambia nuestra dirección IP:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.037.png)

Al realizar la captura, observamos que se ha sustituido la dirección IP privada de la máquina por la pública del router de casa, confirmando que la regla de SNAT funciona correctamente.

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.038.jpeg)

#### Router R2

Configuraremos SNAT y DNAT añadiendo las reglas al fichero `/etc/network/interfaces`:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.039.png)

Reiniciamos el servicio de *networking* y verificamos la aplicación:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.040.png)

Comprobaremos el SNAT haciendo un `ping` desde el servidor hacia una dirección pública:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.041.png)

Confirmamos que el SNAT funciona correctamente:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.042.png)

Ya que se ha sustituido la IP privada por la pública del router. En los siguientes apartados probaremos el DNAT.

#### Router R1

Para este router, crearemos las reglas de forma diferente: mediante un servicio que levante las reglas de DNAT y SNAT al reiniciar la máquina, evitando así añadirlas al fichero de interfaces.

Las reglas de DNAT y SNAT para esta máquina son:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.043.png)

Primero crearemos un script con nuestras reglas. Utilizaremos el comando `iptables-save > /etc/iptables/rules.v4` para volcar las reglas existentes.

Luego, crearemos un script en `/usr/local/bin/` que restaure las reglas volcadas:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.044.png)

Aseguraremos que el script tenga permisos de ejecución:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.045.png)

Crearemos un archivo de servicio de Systemd. Este archivo debe tener permisos de lectura y escritura solo para root, por lo que ejecutaremos el comando como root:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.046.png)

Añadiremos el siguiente contenido, especificando la ruta donde se encuentre el script de `iptables` que restaura las reglas:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.047.png)

Configuraremos el servicio para que se inicie automáticamente al arrancar la máquina:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.048.png)

Y lo iniciaremos:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.049.png)

Para verificar que se ha ejecutado correctamente, consultaremos el estado del servicio:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.050.png)

Observamos que las reglas se han añadido automáticamente:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.051.png)

Comprobaremos el SNAT lanzando un `ping`:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.052.png)

Confirmamos que se ha sustituido la IP privada por la pública:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.053.png)

### Comprobación de navegación y DNAT

Ahora comprobaremos que desde la red de casa podemos acceder a los servidores web.

#### Cliente Debian

Desde el cliente Debian, utilizaremos `curl` para comprobar el funcionamiento del DNAT en el Router R1:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.054.jpeg)

Y haremos lo mismo para comprobar el DNAT en el Router R2:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.055.jpeg)

Ahora comprobaremos qué ocurre si utilizamos la dirección privada de los servidores web:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.056.png)

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.057.png)

Como era de esperar, no podemos acceder, ya que los routers de internet no pueden encaminar el tráfico hacia una red privada, dado que estas direcciones pueden repetirse en infinitas redes.

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.058.png)

Tampoco recibiríamos respuesta en una petición web.

Si interceptamos una petición HTTP, veremos que el SNAT se realiza correctamente, sustituyendo la IP privada del solicitante por la pública de su router:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.059.png)

A continuación, interceptaremos una petición en la que se aplique DNAT para comprobar su correcto funcionamiento:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.060.png)
