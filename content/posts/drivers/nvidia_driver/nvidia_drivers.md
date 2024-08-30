---
title: "Instalación de Controladores NVIDIA en Linux"
date: 2023-09-08T10:00:00+00:00
description: Aprende cómo instalar los controladores NVIDIA en Debian 12 para optimizar el rendimiento gráfico de tu sistema.
tags: [Controladores NVIDIA,Linux]
hero: images/sistemas/nvidia/nvidia.png

---
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GVDYVWJLRH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GVDYVWJLRH');
</script>

La instalación de los controladores de NVIDIA en el universo de Linux ha sido tradicionalmente un desafío, especialmente en distribuciones como Debian, donde las políticas del software libre a menudo complican el proceso.

En este post voy a explicarte una forma sencilla de instalar los drivers de NVIDIA usando los repositorios oficiales de Debian . Además, al final del artículo, aprenderás a instalar una herramienta clave llamada Nvidia Optimus, que te brindará la capacidad de seleccionar qué tarjeta gráfica utilizará tu equipo.

Esta herramienta es especialmente útil en portátiles, ya que es común que estos dispositivos presenten problemas al emitir video a través de los puertos, una situación que puede ser fácilmente con esta herramienta.

## Identificación de Nuestra GPU

Antes de embarcarnos en la instalación y configuración, es fundamental conocer el hardware de nuestro equipo. Para averiguar qué tarjetas gráficas están disponibles en nuestro sistema, utilizaremos el siguiente comando:

```bash
javiercruces@HPOMEN15:~$ lspci -nn | egrep -i "3d|display|vga"
01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106M [GeForce RTX 3060 Mobile / Max-Q] [10de:2520] (rev a1)
06:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Cezanne [Radeon Vega Series / Radeon Vega Mobile Series] [1002:1638] (rev c5)
```

Como se puede apreciar en la salida del comando anterior, mi equipo portátil cuenta con dos tarjetas gráficas. Identificar el modelo es crucial, ya que si optamos por una instalación manual del controlador, necesitaremos el específico para nuestra GPU.

No obstante, en Debian contamos con una utilidad que simplifica este proceso, indicándonos qué controlador debemos instalar. Sin embargo, para acceder a esta utilidad, es necesario modificar nuestros repositorios de Debian.

Para llevar a cabo esta modificación, añadiremos la sección "non-free" a nuestros repositorios utilizando un editor de texto de nuestra preferencia:
```bash
javiercruces@HPOMEN15:~$ sudo nano /etc/apt/sources.list

deb http://deb.debian.org/debian/ bookworm main contrib non-free non-free-firmware

```

Recuerda que cada vez que modifiques este fichero tienes que hacer un update para que se actualice.

```bash
javiercruces@HPOMEN15:~$ sudo apt update -y 
```

Con nuestros repositorios debidamente actualizados, procederemos a instalar el script de detección de NVIDIA con el siguiente comando:

```bash
javiercruces@HPOMEN15:~$ sudo apt install  nvidia-detect
```

Ahora ejecutaremos el script de NVIDIA; como podrás observar, nos proporcionará información detallada sobre nuestra tarjeta gráfica NVIDIA, así como los diversos controladores compatibles y el paquete de Debian recomendado para la instalación:

```bash
javiercruces@HPOMEN15:~$ nvidia-detect 
Detected NVIDIA GPUs:
01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106M [GeForce RTX 3060 Mobile / Max-Q] [10de:2520] (rev a1)

Checking card:  NVIDIA Corporation GA106M [GeForce RTX 3060 Mobile / Max-Q] (rev a1)
Your card is supported by all driver versions.
Your card is also supported by the Tesla drivers series.
Your card is also supported by the Tesla 470 drivers series.
It is recommended to install the
    nvidia-driver
package.

```

## Instalación del driver recomendado

Antes de instalar los controladores, debes obtener los encabezados del kernel adecuados para que el controlador de NVIDIA pueda compilar correctamente.

En un sistema típico de 64 bits que utiliza el kernel predeterminado, simplemente ejecutas:

```bash
javiercruces@HPOMEN15:~$ sudo apt install linux-headers-amd64
```

Para sistemas de 32 bits con el kernel no-PAE, en su lugar, realizarías la siguiente instalación:

```bash
javiercruces@HPOMEN15:~$ sudo apt install linux-headers-686
```


Una vez instalada las dependencias del driver , instalaremos el mismo :

```bash
javiercruces@HPOMEN15:~$ sudo apt install nvidia-driver -y
```

Durante la instalación, es probable que encuentres una pantalla típicamente azul que te informa sobre un conflicto con el controlador "nouveau", el cual es el driver instalado automáticamente por Debian debido a sus características de software libre. Simplemente haz clic en "OK" en esta pantalla y continúa con el proceso de instalación.

Al concluir la instalación, será necesario reiniciar tu equipo para cargar el módulo de NVIDIA. Después de reiniciar, puedes verificar si se ha cargado correctamente utilizando el siguiente comando. Utilizando la barra inclinada (/), puedes filtrar la salida escribiendo la palabra "nvidia", lo que te llevará directamente a la información relevante de tu tarjeta gráfica, permitiéndote confirmar que el módulo de NVIDIA está cargado.

Tienes que comprobar que en la linea "Kernel driver in use" , tenga el modulo nvidia . 

```bash
javiercruces@HPOMEN15:~$ lspci -knn | less

01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106M [GeForce RTX 3060 Mobile / Max-Q] [10de:2520] (rev a1)
        DeviceName: NVIDIA Graphics Device
        Subsystem: Hewlett-Packard Company GA106M [GeForce RTX 3060 Mobile / Max-Q] [103c:88d1]
        Kernel driver in use: nvidia
        Kernel modules: nouveau, nvidia_current_drm, nvidia_current


```

Puede que no te hayas dado cuenta pero ahora en tu escritorio tendrás una app llamada nvidia-settings con la cual podrás configurar tu gráfica .

Ademas si quieres ver desde la linea de comandos información de tu GPU NVIDIA tienes a tu disposición el siguiente comando :

```bash
javiercruces@HPOMEN15:~$ nvidia-smi
Fri Dec 29 02:04:58 2023       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.125.06   Driver Version: 525.125.06   CUDA Version: 12.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  On   | 00000000:01:00.0 Off |                  N/A |
| N/A   42C    P5    10W /  80W |    296MiB /  6144MiB |     12%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|    0   N/A  N/A      3246      G   /usr/lib/xorg/Xorg                117MiB |
|    0   N/A  N/A      3442      G   /usr/bin/gnome-shell               32MiB |
|    0   N/A  N/A      4807      G   ...on=20231218-080113.411000      104MiB |
|    0   N/A  N/A      5802      G   ...RendererForSitePerProcess       38MiB |
+-----------------------------------------------------------------------------+
javiercruces@HPOMEN15:~$ 

```


¡Felicidades, Maestro de los Drivers NVIDIA! Has desbloqueado un logro épico en el reino de la informática. No cualquiera es capaz de llegar hasta aquí, no quiero desilusionarte pero ¿has verificado que funcionen los puertos HDMI y DisplayPort de tu equipo?

En este punto, se abren dos posibles caminos:

En el primer escenario, tus puertos funcionan a la perfección sin requerir intervención adicional. Si este es tu caso, felicidades se ve que Dios tiene favoritos .

Si por el contrario al igual que yo no eres uno de ellos , como acabas de comprobar los puertos no emiten video , en tu monitor veras que no tienes señal a pesar de que en el debian veas que te detecta el monitor. 

Si te ocurre este problema puedes encontrar un post en esta misma pagina explicando una posible solución , para ello haremos uso de la herramienta nvidia optimus . Te dejo el enlace a continuación 


