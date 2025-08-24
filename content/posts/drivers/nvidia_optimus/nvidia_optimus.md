---
title: "Como elegir que gráfica usar en mi portátil con Linux"
date: 2024-09-01T10:00:00+00:00
description: Aprende cómo instalar los controladores NVIDIA en Debian 12 para optimizar el rendimiento gráfico de tu sistema.
tags: [Controladores NVIDIA, Linux]
hero: images/drivers/elegir_grafica.png

---


Si tienes un portátil con Linux y una gráfica Nvidia, es posible que, después de instalar los drivers de la gráfica, hayas notado que los puertos de video no funcionan correctamente. Si te suena familiar, no te preocupes, te tengo cubierto.

He estado investigando y encontré una herramienta que te puede ahorrar varios dolores de cabeza. Se llama EnvyControl, y es una utilidad de línea de comandos (CLI) que te permite elegir fácilmente qué tarjeta gráfica quieres usar en tu equipo. Esto es especialmente útil si tu portátil tiene una configuración de gráficos híbridos, como Intel + Nvidia o AMD + Nvidia.

En mi caso, configuré la herramienta para que siempre use la gráfica dedicada, y ¡voilà! Los puertos de video empezaron a funcionar sin problemas.

EnvyControl es gratuito, de código abierto, y se distribuye bajo la licencia MIT. Eso sí, ten en cuenta que el software se proporciona tal cual, sin garantías. Además, cualquier configuración personalizada de X.org podría ser sobrescrita al cambiar de modos.

Si quieres probarlo, te dejo el enlace al repositorio: [EnvyControl en GitHub](https://github.com/bayasdev/envycontrol). Ahí encontrarás tutoriales específicos para instalarlo en diferentes distribuciones.

A continuación, te guiaré por los pasos para instalarlo en Debian. ¡Vamos a ello!

### Instalación de EnvyControl

Dado que ya no es posible instalar paquetes pip fuera de un entorno virtual tras la adopción de PEP668, en su lugar, utiliza el paquete .deb proporcionado por el repositorio . 

1. Encuentra la versión más reciente en el siguiente enlace: [Releases - EnvyControl](https://github.com/bayasdev/envycontrol/releases/latest).
2. En esa página, selecciona y descarga el paquete .deb correspondiente. También puedes utilizar la herramienta wget para descargarlo desde la terminal.

   ![Descarga del paquete .deb](/drivers/nvidia_optimus/img/github_deb.png)

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

Si prefieres utilizar solo tu gráfica dedicada, ten en cuenta que esta es la única configuración que me ha funcionado para activar los puertos de video. Para dar el salto a este modo te pedirá primero que pongas el modo anterior , el híbrido . Una vez estés en ese modo el comando para activar solo tu gráfica dedicada: 

```bash
 sudo envycontrol -s nvidia --force-comp --coolbits 24
```

Vuelvo a insistirse pero **RECUERDA REINICIAR PARA QUE SE APLIQUEN LOS CAMBIOS** . 

En este punto, te he proporcionado los comandos que he utilizado, pero el programa cuenta con su propio manual. Además, en el repositorio del autor, puedes encontrar información útil adicional.

Ademas en esté explica que hay una extension de gnome para que puedas realizar estos cambios desde la interfaz gráfica . Aunque personalmente siempre tengo un enchufe donde trabajo con el portátil , es posible que para ahorrar batería quieras cambiar al modo híbrido o al de la gráfica integrada .

-----------------

Hasta aquí, confío en que los controladores de NVIDIA estén funcionando correctamente y que ya puedas usar los puertos de video de tu equipo sin problemas.

Como mencioné antes, la compatibilidad puede variar según tu hardware. En mi caso, los puertos de video solo funcionan cuando uso el modo de la gráfica dedicada. Así que si te encuentras en una situación similar, no dudes en probar esta configuración.