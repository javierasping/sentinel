---
title: "Comparativa entre OpenVPN y Wireguard"
date: 2024-03-28T10:00:00+00:00
description: Comparativa entre OpenVPN y Wireguard
tags: [VPN,LINUX,DEBIAN,WIREGUARD,OPENVPN]
hero: /images/vpn/wire_ovpn.png
---



![](/vpn/comparativa_ovpn_wire/img/Pastedimage20240114150833.png)

El objetivo de este post es comparar los distintos software de VPNs mas utilizados viendo cual es mas rápido , para ello nos apoyaremos en test de velocidad utilizando iperf3 .

> [!NOTE]  
> La comparativa parte de los post de esta sección en los que montamos cada tipo de VPN .


## Velocidad sin VPN

Voy a comenzar comparando las velocidades de estos 2 sistemas , utilizando iperf3 . Para ello he quitado el router cisco ya que lo tenia configurado con interfaces FastEthernet y lo he cambiado por un router Linux con interfaces GigabitEthernet .

Voy a lanzar un iperf3 utilizando las direcciones publicas para que el trafico no utilice ninguna VPN :

```bash
javiercruces@servidor2:~$ iperf3 -c 90.0.0.2 -i 1 -t 30
Connecting to host 90.0.0.2, port 5201
[  5] local 100.0.0.2 port 32858 connected to 90.0.0.2 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec   110 MBytes   919 Mbits/sec  897    188 KBytes       
[  5]   1.00-2.00   sec   102 MBytes   859 Mbits/sec  712    120 KBytes       
[  5]   2.00-3.00   sec   111 MBytes   931 Mbits/sec  735   83.4 KBytes       
[  5]   3.00-4.00   sec   112 MBytes   944 Mbits/sec  600    173 KBytes       
[  5]   4.00-5.00   sec   109 MBytes   913 Mbits/sec  1018    126 KBytes       
[  5]   5.00-6.00   sec   115 MBytes   961 Mbits/sec  889    113 KBytes       
[  5]   6.00-7.00   sec   113 MBytes   947 Mbits/sec  549   90.5 KBytes       
[  5]   7.00-8.00   sec   116 MBytes   976 Mbits/sec  964    198 KBytes       
[  5]   8.00-9.00   sec   114 MBytes   956 Mbits/sec  591   76.4 KBytes       
[  5]   9.00-10.00  sec   108 MBytes   908 Mbits/sec  736    120 KBytes       
[  5]  10.00-11.00  sec   105 MBytes   881 Mbits/sec  689    126 KBytes       
[  5]  11.00-12.00  sec   106 MBytes   893 Mbits/sec  745    124 KBytes       
[  5]  12.00-13.00  sec   118 MBytes   990 Mbits/sec  847   93.3 KBytes       
[  5]  13.00-14.00  sec   122 MBytes  1.03 Gbits/sec  899   94.7 KBytes       
[  5]  14.00-15.00  sec   125 MBytes  1.05 Gbits/sec  1014   73.5 KBytes       
[  5]  15.00-16.00  sec   125 MBytes  1.05 Gbits/sec  973    113 KBytes       
[  5]  16.00-17.00  sec   109 MBytes   915 Mbits/sec  934   86.3 KBytes       
[  5]  17.00-18.00  sec   101 MBytes   844 Mbits/sec  629    115 KBytes       
[  5]  18.00-19.00  sec   105 MBytes   881 Mbits/sec  652    122 KBytes       
[  5]  19.00-20.00  sec   116 MBytes   971 Mbits/sec  826   96.2 KBytes       
[  5]  20.00-21.00  sec   115 MBytes   962 Mbits/sec  820   99.0 KBytes       
[  5]  21.00-22.00  sec   128 MBytes  1.08 Gbits/sec  1193   99.0 KBytes       
[  5]  22.00-23.00  sec   130 MBytes  1.09 Gbits/sec  1027    110 KBytes       
[  5]  23.00-24.00  sec   123 MBytes  1.03 Gbits/sec  855    116 KBytes       
[  5]  24.00-25.00  sec   122 MBytes  1.03 Gbits/sec  714    126 KBytes       
[  5]  25.00-26.00  sec   120 MBytes  1.01 Gbits/sec  861    119 KBytes       
[  5]  26.00-27.00  sec   129 MBytes  1.08 Gbits/sec  768    112 KBytes       
[  5]  27.00-28.00  sec   125 MBytes  1.05 Gbits/sec  976    140 KBytes       
[  5]  28.00-29.00  sec   116 MBytes   972 Mbits/sec  943    140 KBytes       
[  5]  29.00-30.00  sec   119 MBytes   996 Mbits/sec  755    116 KBytes  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-30.00  sec  3.39 GBytes   970 Mbits/sec  24811             sender
[  5]   0.00-30.00  sec  3.39 GBytes   970 Mbits/sec                  receiver
```

La velocidad media de la red ha sido de 970 Mbits/sec , sin usar ninguna VPN .

## Velocidad de Wireguard

Vemos a medir la velocidad de Wireguard : 

```bash
javiercruces@cliente3:~$ iperf3 -c 192.168.0.2 -i 1 -t 30
Connecting to host 192.168.0.2, port 5201
[  5] local 192.168.1.2 port 39096 connected to 192.168.0.2 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  57.5 MBytes   483 Mbits/sec   63    196 KBytes       
[  5]   1.00-2.00   sec  56.4 MBytes   473 Mbits/sec   37    190 KBytes       
[  5]   2.00-3.00   sec  58.2 MBytes   488 Mbits/sec   85    188 KBytes       
[  5]   3.00-4.00   sec  57.1 MBytes   479 Mbits/sec   65    140 KBytes       
[  5]   4.00-5.00   sec  57.8 MBytes   485 Mbits/sec    6    199 KBytes       
[  5]   5.00-6.00   sec  59.7 MBytes   500 Mbits/sec   62    200 KBytes       
[  5]   6.00-7.00   sec  59.0 MBytes   495 Mbits/sec   26    234 KBytes       
[  5]   7.00-8.00   sec  57.8 MBytes   485 Mbits/sec   13    216 KBytes       
[  5]   8.00-9.00   sec  58.6 MBytes   492 Mbits/sec   88    151 KBytes       
[  5]   9.00-10.00  sec  58.1 MBytes   487 Mbits/sec   13    174 KBytes       
[  5]  10.00-11.00  sec  57.9 MBytes   486 Mbits/sec   22    135 KBytes       
[  5]  11.00-12.00  sec  57.1 MBytes   479 Mbits/sec   30    188 KBytes       
[  5]  12.00-13.00  sec  57.3 MBytes   481 Mbits/sec   19    178 KBytes       
[  5]  13.00-14.00  sec  57.1 MBytes   479 Mbits/sec   15    230 KBytes       
[  5]  14.00-15.00  sec  56.5 MBytes   474 Mbits/sec   20    218 KBytes       
[  5]  15.00-16.00  sec  57.4 MBytes   481 Mbits/sec   38    172 KBytes       
[  5]  16.00-17.00  sec  55.9 MBytes   469 Mbits/sec  137    143 KBytes       
[  5]  17.00-18.00  sec  57.0 MBytes   478 Mbits/sec   26    246 KBytes       
[  5]  18.00-19.00  sec  56.6 MBytes   475 Mbits/sec   42    183 KBytes       
[  5]  19.00-20.00  sec  56.2 MBytes   471 Mbits/sec   43    222 KBytes       
[  5]  20.00-21.00  sec  56.5 MBytes   474 Mbits/sec   11    203 KBytes       
[  5]  21.00-22.00  sec  56.4 MBytes   473 Mbits/sec   69    147 KBytes       
[  5]  22.00-23.00  sec  54.1 MBytes   454 Mbits/sec   25    163 KBytes       
[  5]  23.00-24.00  sec  55.9 MBytes   469 Mbits/sec   54    207 KBytes       
[  5]  24.00-25.00  sec  57.5 MBytes   482 Mbits/sec   99    164 KBytes       
[  5]  25.00-26.00  sec  56.5 MBytes   474 Mbits/sec   39    182 KBytes       
[  5]  26.00-27.00  sec  56.7 MBytes   476 Mbits/sec   24    150 KBytes       
[  5]  27.00-28.00  sec  56.3 MBytes   472 Mbits/sec    6    219 KBytes       
[  5]  28.00-29.00  sec  57.0 MBytes   478 Mbits/sec   15    146 KBytes       
[  5]  29.00-30.00  sec  56.0 MBytes   470 Mbits/sec   48    151 KBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-30.00  sec  1.67 GBytes   479 Mbits/sec  1240             sender
[  5]   0.00-30.00  sec  1.67 GBytes   479 Mbits/sec                  receiver
```

La velocidad media de wireguard ha sido de 479 Mbits/sec .

## Velocidad de OpenVPN

Vamos a medir la velocidad de OpenVPN

```bash
javiercruces@cliente3:~$ iperf3 -c 192.168.0.2 -i 1 -t 30
Connecting to host 192.168.0.2, port 5201
[  5] local 192.168.1.2 port 43522 connected to 192.168.0.2 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  25.1 MBytes   211 Mbits/sec   24    139 KBytes       
[  5]   1.00-2.00   sec  24.8 MBytes   208 Mbits/sec   15    163 KBytes       
[  5]   2.00-3.00   sec  23.7 MBytes   199 Mbits/sec   40    103 KBytes       
[  5]   3.00-4.00   sec  24.6 MBytes   207 Mbits/sec   19    114 KBytes       
[  5]   4.00-5.00   sec  24.2 MBytes   203 Mbits/sec    8    119 KBytes       
[  5]   5.00-6.00   sec  24.3 MBytes   204 Mbits/sec   14    155 KBytes       
[  5]   6.00-7.00   sec  24.2 MBytes   203 Mbits/sec   13    139 KBytes       
[  5]   7.00-8.00   sec  24.5 MBytes   206 Mbits/sec   18    115 KBytes       
[  5]   8.00-9.00   sec  24.0 MBytes   201 Mbits/sec   34    132 KBytes       
[  5]   9.00-10.00  sec  24.3 MBytes   204 Mbits/sec   32    120 KBytes       
[  5]  10.00-11.00  sec  24.5 MBytes   206 Mbits/sec   12    100 KBytes       
[  5]  11.00-12.00  sec  24.4 MBytes   205 Mbits/sec    8    139 KBytes       
[  5]  12.00-13.00  sec  23.9 MBytes   201 Mbits/sec    6    171 KBytes       
[  5]  13.00-14.00  sec  24.1 MBytes   202 Mbits/sec   20    156 KBytes       
[  5]  14.00-15.00  sec  24.0 MBytes   202 Mbits/sec    8    135 KBytes       
[  5]  15.00-16.00  sec  23.5 MBytes   197 Mbits/sec   21    143 KBytes       
[  5]  16.00-17.00  sec  24.0 MBytes   202 Mbits/sec    8    168 KBytes       
[  5]  17.00-18.00  sec  24.6 MBytes   206 Mbits/sec   24    154 KBytes       
[  5]  18.00-19.00  sec  23.8 MBytes   200 Mbits/sec   21    132 KBytes       
[  5]  19.00-20.00  sec  24.3 MBytes   204 Mbits/sec   20    139 KBytes       
[  5]  20.00-21.00  sec  24.6 MBytes   206 Mbits/sec   11    142 KBytes       
[  5]  21.00-22.00  sec  23.0 MBytes   193 Mbits/sec   26    115 KBytes       
[  5]  22.00-23.00  sec  24.6 MBytes   207 Mbits/sec    3    128 KBytes       
[  5]  23.00-24.00  sec  24.0 MBytes   202 Mbits/sec   26    104 KBytes       
[  5]  24.00-25.00  sec  24.3 MBytes   204 Mbits/sec   21    106 KBytes       
[  5]  25.00-26.00  sec  24.3 MBytes   204 Mbits/sec   15    108 KBytes       
[  5]  26.00-27.00  sec  23.8 MBytes   200 Mbits/sec   36    132 KBytes       
[  5]  27.00-28.00  sec  22.9 MBytes   192 Mbits/sec   13    118 KBytes       
[  5]  28.00-29.00  sec  23.7 MBytes   199 Mbits/sec   19    163 KBytes       
[  5]  29.00-30.00  sec  24.2 MBytes   203 Mbits/sec   11    126 KBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-30.00  sec   725 MBytes   203 Mbits/sec  546             sender
[  5]   0.00-30.00  sec   724 MBytes   202 Mbits/sec                  receiver
```

La velocidad media ha sido 203 Mbits/sec . 


## Conclusiones

Si comparamos los resultados, queda claro que en términos de velocidad, WireGuard ha demostrado ser la opción más eficiente, superando significativamente a OpenVPN , doblándolo en velocidad . 

WireGuard está diseñado para una velocidad rápida. Establece una conexión en 100 milisegundos, mientras que OpenVPN tarda 8 milisegundos. En algunas pruebas, WireGuard demostró ser un 58% más rápido que OpenVPN. En circunstancias ideales, su velocidad superó los 500 mbps.

WireGuard es el protocolo más rápido debido a muchos factores. Estos incluyen:

- Su código ligero lo convierte intrínsecamente en el protocolo más rápido.
- WireGuard también admite el multithreading -procesar datos utilizando muchos núcleos de la CPU simultáneamente- y utiliza un método de cifrado más rápido.
- Además, WireGuard es bueno en el uso del ancho de banda disponible y opera completamente en el espacio del kernel.

Para evitar la censura, OpenVPN es mejor que WireGuard. ¿Por qué? Porque el protocolo OpenVPN puede funcionar sobre las capas del Protocolo UPD y TCP.

UDP es más rápido, mientras que TCP es fiable.TCP puede evitar la censura utilizando el puerto 443, el mismo puerto que utiliza HTTPS. Gracias a TCP, OpenVPN evita la censura de países estrictos como China y Rusia. En algunos casos, una inspección profunda avanzada puede detectar OpenVPN. Pero para estos casos, los expertos en seguridad recomiendan utilizar el Scramble dentro de la configuración avanzada del protocolo para añadir otra capa de protección al tráfico VPN.

Por otro lado, WireGuard sólo utiliza la capa UDP para transportar datos. Y el propósito principal de UDP es transportar datos a gran velocidad, no eludir la censura. Esto hace que sea fácil de detectar. Además, es susceptible de inspección profunda de paquetes.

OpenVPN es seguro si se configura adecuadamente. Este protocolo no tiene vulnerabilidades de seguridad conocidas, y su código ha sido auditado muchas veces. Además, tiene muchos cifrados y algoritmos de autenticación. Cuando se produce alguna vulnerabilidad de seguridad en el algoritmo, entonces OpenVPN puede configurar inmediatamente otra cosa.

En términos de casos de seguridad, WireGuard también se ha ganado una buena reputación. Es seguro y utiliza la última criptografía. Su código es corto y fácil de auditar. Además, WireGuard tiene un conjunto fijo de algoritmos y cifrados. Cuando se encuentra alguna vulnerabilidad, todos los puntos finales se actualizan a una nueva versión, lo que garantiza que nadie vuelva a utilizar código inseguro.