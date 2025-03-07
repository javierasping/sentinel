---
title: "Module management exercises"
date: 2023-11-29T10:00:00+00:00
Description: Modular management exercises
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/ejercicios_de_manejo_de_modulos/ejercicios_de_manejo_de_modulos.jpg
---

## 1.Check the loaded modules on your computer.

![](/sistemas/comandos_linux/ejercicios_de_manejo_de_modulos/img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.001.png)

## 2.Count the number of modules available in the kernel you are using.

![](/sistemas/comandos_linux/ejercicios_de_manejo_de_modulos/img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.002.png)

## 3 Connect a USB pencil and watch the output of the dmesg sudo instruction.

We see how the kernel detects the usb device and the necessary modules are loaded for it:

![](/sistemas/comandos_linux/ejercicios_de_manejo_de_modulos/img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.003.jpeg)

We see how the number of modules loaded has increased:

![](/sistemas/comandos_linux/ejercicios_de_manejo_de_modulos/img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.004.png)

## 4.Eliminate the module for some non-essential dispotive and check what happens. Put it back on.

If we download it we will not be able to make use of exfat file systems:

![](/sistemas/comandos_linux/ejercicios_de_manejo_de_modulos/img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.005.png)

To reload it:

![](/sistemas/comandos_linux/ejercicios_de_manejo_de_modulos/img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.006.png)

## 5.Select a module that is in use on your computer and configure the boot so that it is not automatically loaded.

For this we add it to the "black list," then update the initframes:

![](/sistemas/comandos_linux/ejercicios_de_manejo_de_modulos/img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.007.png)

When we restart this will not be loaded:

![](/sistemas/comandos_linux/ejercicios_de_manejo_de_modulos/img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.008.png)

## 6.Load the loop module, get information about what it is and what it's for. List the content of / sys / modules / loop / parameters and set up the equipment so that up to 12 loop devices can be loaded next time it starts.

We load it and check that it's loaded:

![](/sistemas/comandos_linux/ejercicios_de_manejo_de_modulos/img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.009.png)

We see the information from it:

![](/sistemas/comandos_linux/ejercicios_de_manejo_de_modulos/img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.010.jpeg)

Ready the contents of the / sys / module / loop / parameters directory. This will show the parameters available for the loop module

![](/sistemas/comandos_linux/ejercicios_de_manejo_de_modulos/img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.011.png)

If we want to limit there are 12 loop devices, we create the following file and add the following configuration:

![](/sistemas/comandos_linux/ejercicios_de_manejo_de_modulos/img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.012.png)

We will have to update the sudo-initrfs-u initframes to apply the changes, and we will have to restart.

Once we reboot, if we see the content of the max _ loops parameter. We will see that this one has been applied:

![](/sistemas/comandos_linux/ejercicios_de_manejo_de_modulos/img/Aspose.Words.46ea1f3d-268a-4705-a64e-142fcc81092a.013.png)

