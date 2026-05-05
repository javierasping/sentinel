---
title: "Protocolo ARP"
date: 2023-09-08T10:00:00+00:00
description: Documento en el cual se responden a una serie de preguntas sobre el protocolo ARP
tags: [Redes, ARP]
hero: images/redes/arp/portada.png
---



El Protocolo de Resolución de Direcciones (ARP) es fundamental en redes informáticas para mapear direcciones IP a direcciones físicas de capa de enlace (MAC). Su función principal es encontrar la dirección MAC asociada a una dirección IP específica en una red local. Cuando un dispositivo necesita comunicarse con otro en la misma red, utiliza ARP para determinar la dirección MAC del destino antes de enviar datos.

## Naturaleza de las solicitudes ARP

Las solicitudes ARP son mensajes de difusión (broadcast), ya que en la cabecera se puede observar que el destino es una dirección de broadcast. Esta dirección tiene todos sus bits establecidos en 1, lo que en las direcciones MAC se traduce en `FF:FF:FF:FF:FF:FF`.

Cuando el dispositivo con la dirección IP solicitada (por ejemplo, `192.168.1.1`) recibe este mensaje, responde a la petición, permitiendo que el emisor obtenga su dirección MAC correspondiente.

![](/redes/arp/img/Aspose.Words.239ce20f-0f3b-447a-b584-fd1166c210d0.001.jpeg)

## Naturaleza de las respuestas ARP

En la respuesta ARP, se puede observar que la dirección de destino es la del dispositivo que inició la solicitud. Por lo tanto, la respuesta no es un mensaje de difusión, sino una comunicación unicast (punto a punto).

![](/redes/arp/img/Aspose.Words.239ce20f-0f3b-447a-b584-fd1166c210d0.002.jpeg)


## Actualización de la caché ARP

Cuando se realiza una operación de ping, tanto el emisor como el receptor se añaden mutuamente a su respectiva tabla ARP. Al consultar ambas tablas, se puede verificar que las correspondencias han sido registradas.

El tiempo de permanencia de las entradas en la caché es, generalmente, de 120 segundos; una vez transcurrido este plazo, la entrada se elimina automáticamente.

Los dispositivos que no han participado en la comunicación no almacenan ninguna información en su caché ARP sobre dicha transacción.

## Uso del comando `ip neigh`

El comando `ip neigh` permite gestionar la tabla ARP, donde se almacenan las relaciones entre direcciones IP y MAC. Con este comando es posible visualizar la tabla, añadir, eliminar o modificar entradas, así como ajustar el tiempo de vida de las mismas.

**Funciones principales:**

- **Mostrar la tabla ARP completa**: `ip neighbour show`
- **Agregar una entrada a la tabla ARP**: `ip neighbour add {IP} lladdr {MAC} dev {interface}`
- **Eliminar una entrada de la tabla ARP**: `ip neighbour del {IP} dev {interface}`
- **Establecer el tiempo de vida de una entrada**: `ip neighbour change {IP} dev {interface} nud {state}`
- **Buscar una entrada específica**: `ip neighbour | grep {IP}`

Este comando es la alternativa moderna y complementaria al comando tradicional `arp`.

## ARP Gratuito (Gratuitous ARP)

Un ARP gratuito es una solicitud emitida por un dispositivo para informar a los demás equipos de la red sobre su propia dirección IP y MAC, actualizando así sus tablas ARP.

Su propósito principal es garantizar que todos los dispositivos tengan la información más actualizada posible. Una de sus utilidades más comunes es la detección de conflictos de direcciones IP; si otro equipo responde a un paquete ARP gratuito, indica que la dirección IP ya está siendo utilizada.


## Ataque de ARP Spoofing

El ARP Spoofing consiste en modificar el flujo de datos entre un dispositivo víctima y su puerta de enlace (Gateway). El atacante envía respuestas ARP falsas para asociar su propia dirección MAC a la dirección IP del Gateway en la máquina de la víctima, logrando así un ataque de tipo Man-in-the-Middle (MITM).

De este modo, el atacante intercepta todo el tráfico, pudiendo obtener contraseñas e información confidencial.

**Pasos del ataque:**

1. **Escaneo de red**: Obtención de la relación de dispositivos conectados.
2. **Envío de paquetes ARP falsos**: Asociación de la MAC del atacante con la IP de la víctima o del gateway.
3. **Intercepción**: Captura de todo el tráfico que transita entre los objetivos.

Este ataque requiere que el atacante tenga acceso a la red local. Para prevenirlo, se recomienda:

- Utilizar herramientas de detección de ARP Spoofing.
- Implementar firewalls capaces de bloquear paquetes ARP sospechosos.
- Emplear protocolos de cifrado como IPsec y SSL/TLS.
- Configurar entradas estáticas en la tabla ARP.

## MAC Flooding y MAC Spoofing

**MAC Flooding**: Consiste en saturar la tabla de direcciones MAC de un dispositivo de red (como un switch) mediante el envío masivo de direcciones falsas. Cuando la tabla se llena, el switch comienza a reenviar el tráfico por todos sus puertos (actuando como un hub), lo que puede permitir la intercepción de datos o provocar una denegación de servicio (DoS).

Para mitigar este ataque, se recomienda limitar el tamaño de la tabla y activar la detección de tráfico sospechoso.

**MAC Spoofing**: Consiste en falsificar la dirección MAC de un dispositivo para suplantar a otro y así interceptar tráfico específico o acceder a recursos restringidos.

Para mitigar este ataque, se pueden implementar las siguientes estrategias:

- **Entradas estáticas en la tabla ARP**: Asociar manualmente IPs a direcciones MAC para evitar que los mensajes ARP dinámicos modifiquen la tabla. Es ideal para la puerta de enlace.
- **DHCP Snooping**: Mantiene un registro de las MAC conectadas a cada puerto y detecta suplantaciones inmediatamente.
- **Dynamic ARP Inspection (DAI)**: Requiere DHCP Snooping y garantiza que solo se transmitan solicitudes y respuestas ARP válidas, descartando paquetes sospechosos.
- **RARP (Reverse ARP)**: Permite consultar la IP asociada a una dirección MAC. Si retorna más de una IP, indica que la MAC ha sido clonada.



## Bibliografía

- [ip neigh](https://rm-rf.es/control-de-tablas-arp-con-el-comando-ip/)
- [arp spoofing](https://www.incibe-cert.es/blog/arp-spoofing)
- [ARP gratuitos ](http://www.tranquilidadtecnologica.com/2006/05/paquetes-arp-gratuitos.html)
- [medidas de mitigación](http://profesores.elo.utfsm.cl/~agv/elo323/2s14/projects/reports/MoraMorales/mitigacion.html#:~:text=Es%20una%20estrategia%20que%20mantiene,es%20el%20caso%20de%20CISCO.)

