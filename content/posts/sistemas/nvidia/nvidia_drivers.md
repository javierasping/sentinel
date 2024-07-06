---
title: "Instalación de Controladores NVIDIA en Debian 12"
date: 2023-09-08T10:00:00+00:00
description: Aprende cómo instalar los controladores NVIDIA en Debian 12 para optimizar el rendimiento gráfico de tu sistema.
tags: [Debian 12, Controladores NVIDIA,Sistemas,ISO,ASO]
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


¡Felicidades, Maestro de los Drivers NVIDIA! Has desbloqueado un logro épico en el reino de la informática. No cualquiera es capaz de llegar hasta aquí, no quiero desilusionarte pero ¿has verificado que funcionen los puertos HDMI y DP de tu equipo?

En este punto, se abren dos posibles caminos:

En el primer escenario, tus puertos funcionan a la perfección sin requerir intervención adicional. Si este es tu caso, felicidades se ve que Dios tiene favoritos .

Si por el contrario al igual que yo no eres uno de sus elegidos , como acabas de comprobar los puertos no emiten video , en tu monitor veras que no tienes señal a pesar de que en el debian veas que te detecta el monitor. 

Aquí se habré un mundo de problemas y incompatibilidades . Puedes tener problema con el sistema de ventanas de tu equipo , te falte alguna librería ... 



## Nvidia Optimus

Después de una extensa investigación, he descubierto una herramienta que facilita, a través de la línea de comandos (CLI), la elección de la tarjeta gráfica que utiliza tu equipo.

La herramienta en cuestión es EnvyControl, una utilidad de línea de comandos (CLI) que simplifica el cambio entre modos de GPU en sistemas Nvidia Optimus, como aquellos presentes en portátiles con configuraciones de gráficos híbridos Intel + Nvidia o AMD + Nvidia, en entornos Linux.

EnvyControl es un software gratuito y de código abierto lanzado bajo la licencia MIT.

Ten en cuenta que este software se proporciona "tal cual" sin ninguna garantía expresa o implícita. Además, cualquier configuración personalizada de X.org puede ser eliminada o sobrescrita al cambiar entre modos.

El repositorio de la herramienta es el siguiente --> https://github.com/bayasdev/envycontrol

Para la instalación, se proporciona un mini tutorial específico para cada distribución en el repositorio. A continuación, te guiaré a través de los pasos para instalarlo en Debian.


### Instalación de EnvyControl

Dado que ya no es posible instalar paquetes pip fuera de un entorno virtual tras la adopción de PEP668, en su lugar, utiliza el paquete .deb proporcionado por el repositorio . 

1. Encuentra la versión más reciente en el siguiente enlace: [Releases - EnvyControl](https://github.com/bayasdev/envycontrol/releases/latest).
2. En esa página, selecciona y descarga el paquete .deb correspondiente. También puedes utilizar la herramienta wget para descargarlo desde la terminal.

   ![Descarga del paquete .deb](../img/github_deb.png)

3. Instala el paquete descargado con el siguiente comando:

```bash
    sudo apt -y install ./python3-envycontrol_version.deb
```

----------

Una vez que hayas instalado la herramienta, tendrás la capacidad de seleccionar la tarjeta gráfica que deseas utilizar en tu equipo. Es importante recordar que cualquier configuración aplicada no surtirá efecto hasta que reinicies el sistema.

Supongamos que decides utilizar la gráfica integrada para ahorrar energía, por ejemplo. El comando correspondiente sería :

```bash
sudo envycontrol -s integrated
```

Si por el contrario quieres utilizar el modo hibrido (ambas) 

```bash
sudo envycontrol -s hybrid --rtd3
```

Si prefieres utilizar solo tu gráfica dedicada, ten en cuenta que esta es la única configuración que me ha funcionado para activar los puertos de video. Para dar el salto a este modo te pedira primero que pongas el modo anterior , el hibrido . Una vez estes en ese modo el comando para activar solo tu grafica dedicada: 

```bash
 sudo envycontrol -s nvidia --force-comp --coolbits 24
```

Vuelvo a insistirse pero **RECUERDA REINICIAR PARA QUE SE APLIQUEN LOS CAMBIOS** . 

En este punto, te he proporcionado los comandos que he utilizado, pero el programa cuenta con su propio manual. Además, en el repositorio del autor, puedes encontrar información útil adicional.

Ademas en esté explica que hay una extension de gnome para que puedas realizar estos cambios desde la interfaz gráfica . Aunque personalmente siempre tengo un enchufe donde trabajo con el portátil , es posible que para ahorrar batería quieras cambiar al modo híbrido o al de la gráfica integrada .

-----------------

Hasta este punto, confío en que los controladores de NVIDIA estén funcionando correctamente y que puedas aprovechar los puertos de video de tu equipo.