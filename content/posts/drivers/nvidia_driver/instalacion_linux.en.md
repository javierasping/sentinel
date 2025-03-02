---
title: "Installation of NVIDIA Controllers in Debian 12"
date: 2024-09-01T10:00:00+00:00
Description: Learn how to install NVIDIA drivers in Debian 12 to optimize your system's graphic performance.
tags: [Controladores NVIDIA,Linux]
hero: images/drivers/instalar_drivers_nvidia.png
slug: instalacion-controladores-nvidia-debian-12
---


The installation of NVIDIA drivers in the Linux universe has traditionally been a challenge, especially in distributions such as Debian, where free software policies often complicate the process.

In this post I will explain a simple way to install NVIDIA drivers using the official Debian repositories. In addition, at the end of the article, you will learn to install a key tool called Nvidia Optimus, which will provide you with the ability to select which graphics card you will use.

This tool is especially useful in laptops, as it is common for these devices to present problems when emitting video through ports, a situation that can be easily with this tool.

## Identification of Our GPU

Before we embark on installation and configuration, it is essential to know the hardware of our computer. To find out which graphics cards are available in our system, we will use the following command:

```bash
javiercruces@HPOMEN15:~$ lspci -nn | egrep -i "3d|display|vga"
01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106M [GeForce RTX 3060 Mobile / Max-Q] [10de:2520] (rev a1)
06:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Cezanne [Radeon Vega Series / Radeon Vega Mobile Series] [1002:1638] (rev c5)
```

As you can see in the output of the previous command, my laptop has two graphics cards. Identifying the model is crucial, as if we choose a manual driver installation, we will need the specific for our GPU.

However, in Debian we have a utility that simplifies this process, indicating which controller we should install. However, to access this utility, we need to modify our Debian repositories.

To make this modification, we will add the "non-free" section to our repositories using a text editor of our preference:
```bash
javiercruces@HPOMEN15:~$ sudo nano /etc/apt/sources.list

deb http://deb.debian.org/debian/ bookworm main contrib non-free non-free-firmware

```

Remember that every time you modify this file you have to make an update for it to be updated.

```bash
javiercruces@HPOMEN15:~$ sudo apt update -y 
```

With our properly updated repositories, we will proceed to install the NVIDIA detection script with the following command:

```bash
javiercruces@HPOMEN15:~$ sudo apt install  nvidia-detect
```

We will now run the NVIDIA script; as you can see, it will provide us with detailed information about our NVIDIA graphics card, as well as the various compatible drivers and the recommended Debian package for installation:

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

### Recommended driver installation

Before installing the drivers, you must get the right kernel headers so that the NVIDIA controller can compile correctly.

In a typical 64-bit system that uses the default kernel, you just run:

```bash
javiercruces@HPOMEN15:~$ sudo apt install linux-headers-amd64
```

For 32-bit systems with the no-PAE kernel, instead, you would make the following installation:

```bash
javiercruces@HPOMEN15:~$ sudo apt install linux-headers-686
```


Once the driver's dependencies are installed, we will install the same:

```bash
javiercruces@HPOMEN15:~$ sudo apt install nvidia-driver -y
```

During installation, you are likely to find a typically blue screen that informs you about a conflict with the "nouveau" driver, which is the driver installed automatically by Debian due to its free software features. Simply click "OK" on this screen and continue the installation process.

At the end of the installation, you will need to restart your equipment to load the NVIDIA module. After reboot, you can check if it has been properly loaded using the following command. Using the tilted bar (/), you can filter the output by writing the word "nvidia," which will take you directly to the relevant information on your graphic card, allowing you to confirm that the NVIDIA module is loaded.

You have to check that on the line "Kernel driver in use," have the nvidia module.

```bash
javiercruces@HPOMEN15:~$ lspci -knn | less

01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106M [GeForce RTX 3060 Mobile / Max-Q] [10de:2520] (rev a1)
        DeviceName: NVIDIA Graphics Device
        Subsystem: Hewlett-Packard Company GA106M [GeForce RTX 3060 Mobile / Max-Q] [103c:88d1]
        Kernel driver in use: nvidia
        Kernel modules: nouveau, nvidia_current_drm, nvidia_current


```

You may not have noticed but now on your desktop you will have an app called nvidia-settings with which you can set your graph.

In addition if you want to see from the command line information of your GPU NVIDIA you have at your disposal the following command:

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


Congratulations, Master of NVIDIA Drivers! You have unlocked an epic achievement in the realm of computer science. Not anyone is able to get here, I don't want to disappoint you but have you checked that the HDMI and DisplayPort ports of your team work?

At this point, two possible paths are opened:

In the first stage, your ports work perfectly without requiring additional intervention. If this is your case, congratulations you see God has favorites.

If, on the contrary, like I'm not one of them, as the ports have just checked, they don't emit video, on your monitor you'll see that you have no signal even though on the debian you see the monitor detects you.

If this problem occurs you can find a post on this same page explaining a possible solution, for this we will make use of the nvidia optimus tool. I leave the link below https: / / www.javiercd.es / posts / drivers / nvidia _ optimus / nvidia _ optimus /


