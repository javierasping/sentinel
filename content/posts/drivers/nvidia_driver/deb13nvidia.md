---
title: "Instalación de Controladores NVIDIA en Debian 13"
date: 2025-08-24T10:00:00+00:00
description: Aprende cómo instalar los controladores NVIDIA en Debian 13 para optimizar el rendimiento gráfico de tu sistema.
tags: [Controladores NVIDIA,Linux]
hero: images/drivers/instalar_drivers_nvidia_trixie.png
slug: instalacion-controladores-nvidia-debian-13
---

La instalación de los controladores de NVIDIA en el universo de Linux ha sido tradicionalmente un desafío, especialmente en distribuciones como Debian, donde las políticas del software libre a menudo complican el proceso.

En este post voy a explicarte una forma sencilla de instalar los drivers de NVIDIA usando los repositorios oficiales de Debian 13 (Trixie). Además, al final del artículo, aprenderás a instalar una herramienta clave llamada Nvidia Optimus, que te brindará la capacidad de seleccionar qué tarjeta gráfica utilizará tu equipo.

Esta herramienta es especialmente útil en portátiles, ya que es común que estos dispositivos presenten problemas al emitir video a través de los puertos, una situación que puede ser fácilmente solucionada con esta herramienta.

## Identificación de Nuestra GPU

Antes de embarcarnos en la instalación y configuración, es fundamental conocer el hardware de nuestro equipo. Para averiguar qué tarjetas gráficas están disponibles en nuestro sistema, utilizaremos el siguiente comando:

```bash
javiercruces@HPOMEN15:~$ lspci -nn | egrep -i "3d|display|vga"
01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106M [GeForce RTX 3060 Mobile / Max-Q] [10de:2520] (rev a1)
06:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Cezanne [Radeon Vega Series / Radeon Vega Mobile Series] [1002:1638] (rev c5)
```

Una vez identificado el hardware, podemos comprobar qué controlador está usando actualmente el sistema:

```bash
javiercruces@HPOMEN15:~$ lspci -knn 

01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106M [GeForce RTX 3060 Mobile / Max-Q] [10de:2520] (rev a1)
    DeviceName: NVIDIA Graphics Device
    Subsystem: Hewlett-Packard Company Device [103c:88d1]
    Kernel driver in use: nouveau
    Kernel modules: nouveau
```

Como se observa, por defecto Debian utiliza el driver libre **nouveau**, que aunque funcional, no ofrece el mismo rendimiento ni compatibilidad que los controladores oficiales de NVIDIA.

## Configuración de los repositorios

Para instalar los controladores propietarios, necesitamos asegurarnos de que los repositorios tengan habilitadas las secciones **contrib** y **non-free**. Edita el fichero `/etc/apt/sources.list` con tu editor favorito y asegúrate de que quede así:

```bash
javiercruces@HPOMEN15:~$ sudo nano /etc/apt/sources.list

deb http://deb.debian.org/debian/ trixie main contrib non-free non-free-firmware
deb-src http://deb.debian.org/debian/ trixie main contrib non-free non-free-firmware

deb http://security.debian.org/debian-security trixie-security main contrib non-free non-free-firmware
deb-src http://security.debian.org/debian-security trixie-security main contrib non-free non-free-firmware

deb http://deb.debian.org/debian/ trixie-updates main contrib non-free non-free-firmware
deb-src http://deb.debian.org/debian/ trixie-updates main contrib non-free non-free-firmware
```

Recuerda actualizar los índices de paquetes después de cualquier cambio:

```bash
javiercruces@HPOMEN15:~$ sudo apt update -y
```

## Detección automática del controlador recomendado

Debian nos proporciona una herramienta que detecta qué versión del driver debemos instalar. Instálala con:

```bash
javiercruces@HPOMEN15:~$ sudo apt install nvidia-detect -y
```

Ejecutamos la utilidad:

```bash
javiercruces@HPOMEN15:~$ nvidia-detect 
Detected NVIDIA GPUs:
01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106M [GeForce RTX 3060 Mobile / Max-Q] [10de:2520] (rev a1)

Checking card:  NVIDIA Corporation GA106M [GeForce RTX 3060 Mobile / Max-Q] (rev a1)
Your card is supported by all driver versions.
Your card is also supported by the Tesla 535 drivers series.
It is recommended to install the
    nvidia-driver
package.
```

## Instalación del driver recomendado

Antes de instalar los controladores, es necesario tener los encabezados del kernel:

```bash
javiercruces@HPOMEN15:~$ sudo apt install linux-headers-amd64 -y
```

Y ahora sí, instalamos el driver NVIDIA recomendado:

```bash
javiercruces@HPOMEN15:~$ sudo apt install nvidia-driver -y
```

Durante la instalación, puede que aparezca un aviso sobre el driver **nouveau**, ya que este estara cargado y tendra conflictos con el de nvidia . Simplemente es un aviso , al reiniciar el equipo se cargara el de nvidia y se solucionara . Selecciona "OK" y continúa.

Tras reiniciar el sistema, podemos comprobar que el módulo de NVIDIA está cargado:

```bash
javiercruces@HPOMEN15:~$ lspci -knn 

01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106M [GeForce RTX 3060 Mobile / Max-Q] [10de:2520] (rev a1)
    DeviceName: NVIDIA Graphics Device
    Subsystem: Hewlett-Packard Company Device [103c:88d1]
    Kernel driver in use: nvidia
    Kernel modules: nvidia
```

## Verificación con NVIDIA-SMI

Una vez completada la instalación, podemos utilizar la herramienta `nvidia-smi` para verificar el estado de la GPU:

```bash
javiercruces@HPOMEN15:~$ nvidia-smi
Sun Aug 24 21:55:26 2025       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 550.163.01             Driver Version: 550.163.01     CUDA Version: 12.4     |
|-----------------------------------------+------------------------+----------------------|
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 3060 ...    Off |   00000000:01:00.0 Off |                  N/A |
| N/A   42C    P5             10W /   25W |       9MiB /   6144MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------|
                                                                                         
+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A      1999      G   /usr/lib/xorg/Xorg                              4MiB |
+-----------------------------------------------------------------------------------------+
```

Si todo funciona correctamente, ya tendrás tu GPU NVIDIA funcionando con los drivers oficiales en Debian 13 .

## ¿Y si los puertos HDMI o DisplayPort no funcionan?

En algunos portátiles, a pesar de que la tarjeta gráfica NVIDIA se instala y detecta correctamente, los puertos externos no emiten video. Si este es tu caso, la solución pasa por utilizar la herramienta **NVIDIA Optimus**.

He preparado un artículo específico explicando este proceso. Puedes leerlo aquí:  
👉 [Configurar NVIDIA Optimus en Debian](https://www.javiercd.es/posts/drivers/nvidia_optimus/nvidia_optimus/)  

---

¡Felicidades, Maestro de los Drivers NVIDIA en Debian 13! Has superado otro reto en el vasto reino de la informática. 🚀