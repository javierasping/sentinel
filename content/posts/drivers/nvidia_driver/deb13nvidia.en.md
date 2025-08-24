---
title: "Installing NVIDIA Drivers on Debian 13"
date: 2025-08-24T10:00:00+00:00
description: Learn how to install NVIDIA drivers on Debian 13 to optimize your system's graphics performance.
tags: [NVIDIA Drivers,Linux]
hero: images/drivers/instalar_drivers_nvidia_trixie.png
slug: instalacion-controladores-nvidia-debian-13
---

The installation of NVIDIA drivers in the Linux universe has traditionally been a challenge, especially in distributions like Debian, where free software policies often complicate the process.

In this post, I will explain a simple way to install NVIDIA drivers using the official Debian 13 (Trixie) repositories. In addition, at the end of the article, you will learn how to install a key tool called Nvidia Optimus, which gives you the ability to choose which graphics card your system will use.

This tool is especially useful on laptops, since it is common for these devices to have issues outputting video through ports, a situation that can be easily solved with this tool.

## Identifying Our GPU

Before diving into installation and configuration, it is essential to know our system’s hardware. To find out which graphics cards are available in our system, we use the following command:

```bash
javiercruces@HPOMEN15:~$ lspci -nn | egrep -i "3d|display|vga"
01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106M [GeForce RTX 3060 Mobile / Max-Q] [10de:2520] (rev a1)
06:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Cezanne [Radeon Vega Series / Radeon Vega Mobile Series] [1002:1638] (rev c5)
```

Once the hardware has been identified, we can check which driver is currently being used by the system:

```bash
javiercruces@HPOMEN15:~$ lspci -knn 

01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106M [GeForce RTX 3060 Mobile / Max-Q] [10de:2520] (rev a1)
    DeviceName: NVIDIA Graphics Device
    Subsystem: Hewlett-Packard Company Device [103c:88d1]
    Kernel driver in use: nouveau
    Kernel modules: nouveau
```

As you can see, Debian uses the free **nouveau** driver by default, which, while functional, does not provide the same performance or compatibility as NVIDIA’s official drivers.

## Configuring the Repositories

To install proprietary drivers, we need to make sure that the repositories have the **contrib** and **non-free** sections enabled. Edit the `/etc/apt/sources.list` file with your favorite editor and make sure it looks like this:

```bash
javiercruces@HPOMEN15:~$ sudo nano /etc/apt/sources.list

deb http://deb.debian.org/debian/ trixie main contrib non-free non-free-firmware
deb-src http://deb.debian.org/debian/ trixie main contrib non-free non-free-firmware

deb http://security.debian.org/debian-security trixie-security main contrib non-free non-free-firmware
deb-src http://security.debian.org/debian-security trixie-security main contrib non-free non-free-firmware

deb http://deb.debian.org/debian/ trixie-updates main contrib non-free non-free-firmware
deb-src http://deb.debian.org/debian/ trixie-updates main contrib non-free non-free-firmware
```

Remember to update the package indexes after any changes:

```bash
javiercruces@HPOMEN15:~$ sudo apt update -y
```

## Automatic Detection of the Recommended Driver

Debian provides us with a tool that detects which driver version we should install. Install it with:

```bash
javiercruces@HPOMEN15:~$ sudo apt install nvidia-detect -y
```

Run the utility:

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

## Installing the Recommended Driver

Before installing the drivers, it is necessary to have the kernel headers:

```bash
javiercruces@HPOMEN15:~$ sudo apt install linux-headers-amd64 -y
```

Now, we can install the recommended NVIDIA driver:

```bash
javiercruces@HPOMEN15:~$ sudo apt install nvidia-driver -y
```

During installation, you may see a warning about the **nouveau** driver, since it will be loaded and will conflict with the NVIDIA driver. This is just a warning; after rebooting the system, the NVIDIA driver will load and the issue will be resolved. Select "OK" and continue.

After rebooting the system, we can check that the NVIDIA module is loaded:

```bash
javiercruces@HPOMEN15:~$ lspci -knn 

01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106M [GeForce RTX 3060 Mobile / Max-Q] [10de:2520] (rev a1)
    DeviceName: NVIDIA Graphics Device
    Subsystem: Hewlett-Packard Company Device [103c:88d1]
    Kernel driver in use: nvidia
    Kernel modules: nvidia
```

## Verification with NVIDIA-SMI

Once installation is complete, we can use the `nvidia-smi` tool to verify the GPU status:

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

If everything works correctly, you now have your NVIDIA GPU running with the official drivers on Debian 13.

## What if HDMI or DisplayPort Ports Don’t Work?

On some laptops, even though the NVIDIA graphics card is installed and detected correctly, external ports may not output video. If this is your case, the solution is to use the **NVIDIA Optimus** tool.

I have prepared a specific article explaining this process. You can read it here:  
👉 [Configuring NVIDIA Optimus on Debian](https://www.javiercd.es/en/posts/drivers/nvidia_optimus/nvidia_optimus/)  

---

Congratulations, Master of NVIDIA Drivers on Debian 13! You have overcome another challenge in the vast realm of computing. 🚀