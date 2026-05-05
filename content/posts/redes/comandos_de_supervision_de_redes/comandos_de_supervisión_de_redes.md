---
title: "Comandos de supervisión de redes"
date: 2023-09-08T10:00:00+00:00
description: "Guía detallada de los principales comandos utilizados para la detección y resolución de incidencias en redes."
tags: [Redes, comandos]
hero: images/redes/comando_de_supervision_de_redes/comando_de_supervision_de_redes.png
---

Este documento detalla los principales comandos y herramientas utilizadas para detectar y solucionar incidencias de conectividad en redes.

## Herramientas de diagnóstico en Windows

### Configuración de las propiedades de TCP/IP

La configuración de red en Windows se gestiona de forma independiente para cada adaptador de red. Para acceder a estos parámetros, siga la siguiente ruta:

**Panel de control** $\rightarrow$ **Redes e Internet** $\rightarrow$ **Centro de redes y recursos compartidos** $\rightarrow$ **Cambiar configuración del adaptador**.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.001.png)

Una vez en el adaptador correspondiente, haga clic derecho sobre él, seleccione **Propiedades** y luego elija **Protocolo de Internet versión 4 (TCP/IPv4)**.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.002.png)

En la pestaña **General**, se encuentran los siguientes apartados clave:

#### Configuración de la dirección IP

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.003.png)

- **Obtener una dirección IP automáticamente**: Activa el uso del servicio DHCP para asignar dinámicamente la dirección IP, la máscara de subred y la puerta de enlace predeterminada.
- **Usar la siguiente dirección IP**: Permite la configuración manual de los parámetros de red:
    - **Dirección IP**: Identificador numérico único del equipo en la red local.
    - **Máscara de subred**: Define qué parte de la dirección IP corresponde a la red (incluida la subred) y qué parte al host.
    - **Puerta de enlace predeterminada**: Dirección IP del dispositivo que permite la comunicación con otras redes (generalmente el router).

#### Configuración de servidores DNS

Los servidores DNS traducen nombres de dominio en direcciones IP para permitir la navegación web.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.004.png)

- **Obtener la dirección del servidor DNS automáticamente**: La dirección se obtiene a través del servidor DHCP de la red.
- **Usar las siguientes direcciones del servidor DNS**: Permite asignar manualmente los servidores DNS:
    - **Servidor DNS preferido**: El primer servidor consultado para la resolución de nombres.
    - **Servidor DNS alternativo**: Servidor de respaldo en caso de que el primario no esté disponible.

#### Configuración alternativa

Diseñada para equipos que operan en múltiples redes, común en entornos profesionales:

- **Dirección IP privada automática (APIPA)**: Utiliza la autoconfiguración si el servidor DHCP no responde.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.005.png)
- **Configurada por el usuario**: Permite introducir manualmente la configuración.
- **WINS preferido/alternativo**: Servidores de nombres de Microsoft para NetBIOS que mantienen la correspondencia entre direcciones IP y nombres de equipos.

### Utilidad del comando `ping`

El comando `ping` es una herramienta de diagnóstico fundamental que verifica la conectividad entre un host local y un equipo remoto en una red TCP/IP.

Sus usos más comunes incluyen:

- Comprobar la conectividad básica de la red.
- Medir la latencia (tiempo de respuesta) entre dos puntos.
- Resolver el nombre de un dominio para conocer su dirección IP.
- Implementar scripts de monitoreo de disponibilidad de servidores.

Para ejecutarlo, abra una terminal de comandos (`cmd`) presionando `Win + R` y escribiendo `cmd`.

#### Uso general de `ping`

La sintaxis básica es: `ping [Parámetros] [IP/Nombre]`

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.006.png)

La salida del comando proporciona la siguiente información:

- **Dirección IP**: La IP asociada al nombre de la máquina remota.
- **Número de secuencia ICMP**: Código de respuesta (ej. 0 indica éxito).
- **TTL (Time to Live)**: Tiempo de vida del paquete. Se decrementa en cada salto (router). Si llega a cero, el paquete se descarta para evitar bucles infinitos en la red.
- **Latencia**: Tiempo en milisegundos que tarda el paquete en ir y volver. Como regla general, una demora superior a 200 ms puede indicar problemas de red.
- **Estadísticas**: Resumen de paquetes enviados, recibidos y perdidos, junto con los tiempos mínimo, máximo y promedio.

#### Parámetros avanzados de `ping`

- **`-t` (Ping infinito)**: Envía solicitudes continuamente hasta que el proceso se detenga manualmente con `Ctrl + C`.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.007.png)

- **`-a` (Resolución de nombre)**: Intenta resolver la dirección IP en un nombre de host, facilitando la identificación de los equipos.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.008.png)

- **`-n [número]` (Cantidad de solicitudes)**: Especifica el número de paquetes a enviar (por defecto son 4). Ejemplo: `ping -n 10 8.8.8.8`.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.009.png)

- **`-l [tamaño]` (Tamaño del paquete)**: Modifica el tamaño en bytes de los datos enviados (entre 0 y 65,500 bytes).

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.010.png)

- **`-f` (No fragmentar)**: Evita que los paquetes se fragmenten. El tamaño máximo sin fragmentar es generalmente de 1472 bytes.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.011.png)

- **`-i [TTL]` (Fijar TTL)**: Establece el valor inicial del TTL. Si el paquete alcanza el destino después de exactamente este número de saltos, o si llega a cero antes, se informará el estado correspondiente.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.012.png)

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.013.png)

- **`-4` y `-6`**: Fuerza el uso de IPv4 o IPv6 respectivamente.

#### Protocolo de comprobación de conectividad

Para verificar el funcionamiento de la red y detectar errores, se recomienda seguir esta secuencia de pruebas:

1. **Ping al propio equipo (Loopback)**: Verifica que la pila TCP/IP y el adaptador de red funcionen correctamente.
   ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.014.png)

2. **Ping a un equipo de la red local**: Confirma que la conectividad física y el direccionamiento local son correctos.
   ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.015.png)

3. **Ping a la puerta de enlace (Gateway)**: Demuestra que existe comunicación con el router que proporciona acceso a otras redes.
   ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.016.png)

4. **Ping a una IP externa (Internet)**: Confirma la salida a internet sin depender de la resolución de nombres.
   ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.017.png)

5. **Ping a un dominio externo**: Verifica que la conexión a internet sea correcta y que los servidores DNS estén resolviendo nombres adecuadamente.
   ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.018.png)

### Uso general del comando `ipconfig`

El comando `ipconfig` permite visualizar y gestionar la configuración actual de los adaptadores de red del equipo.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.019.png)

**Información proporcionada:**

- **Descripción del adaptador**: Nombre de la tarjeta de red utilizada.
- **Dirección IPv4**: IP asignada al equipo en la red local.
- **Puerta de enlace predeterminada**: IP del dispositivo que proporciona acceso a internet.
- **Servidores DNS**: Direcciones de los servidores encargados de resolver nombres de dominio.
- **Estado de DHCP**: Indica si la configuración es dinámica (habilitada) o estática.

#### Parámetros avanzados de `ipconfig`

- **`/all`**: Muestra una salida detallada que incluye las direcciones MAC y los servidores DNS.
  ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.020.png)

- **`/release`**: Libera la dirección IP actual asignada por el servidor DHCP.
  ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.021.png)
  *Ejemplo: `ipconfig /release Ethernet0` para liberar un adaptador específico.*

- **`/renew`**: Solicita una nueva concesión de dirección IP al servidor DHCP.
  ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.022.png)

- **`/flushdns`**: Vacía la caché de resolución DNS del equipo local, útil para forzar la actualización de cambios en registros DNS.
  ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.023.png)

- **`/registerdns`**: Actualiza las concesiones DHCP y vuelve a registrar los nombres DNS en el servidor.
  ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.024.png)

- **`/displaydns`**: Muestra todas las entradas almacenadas actualmente en la caché DNS.
  ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.025.png)

- **`/showclassid`**: Muestra las clases de usuario configuradas en el servidor DHCP.
  ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.026.png)

### Uso general del comando `arp`

El comando `arp` se utiliza para visualizar y modificar la tabla de correspondencias entre direcciones IP y direcciones MAC (capa de enlace).

#### Parámetro `arp -a`

Muestra las entradas actuales de la caché ARP del host, incluyendo la dirección IPv4, la dirección física (MAC) y el tipo de direccionamiento (estático o dinámico).

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.027.png)

*Nota: El parámetro `-g` realiza la misma función que `-a`.*
