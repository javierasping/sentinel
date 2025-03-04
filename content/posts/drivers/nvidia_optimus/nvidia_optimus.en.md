---
title: "How to Choose Which GPU to Use on My Laptop with Linux"
date: 2024-09-01T10:00:00+00:00
description: Learn how to install NVIDIA drivers in Debian 12 to optimize your system's graphic performance.
tags: [NVIDIA Drivers, Linux]
hero: images/drivers/elegir_grafica.png
---

If you have a Linux laptop with an NVIDIA GPU, you may have noticed that the video ports are not working properly after installing the graphics drivers. If this sounds familiar, don't worry—I’ve got you covered.

I've been investigating and found a tool that can save you several headaches. It's called **EnvyControl**, a command-line utility (CLI) that allows you to easily choose which graphics card you want to use on your computer. This is especially useful if your laptop has a hybrid graphics configuration, such as Intel + NVIDIA or AMD + NVIDIA.

In my case, I set up the tool to always use the dedicated GPU, and voilà! The video ports started working smoothly.

EnvyControl is free, open-source, and distributed under the MIT license. Please note that the software is provided *as is*, without guarantees. Additionally, any custom X.org settings could be overwritten when switching modes.

If you want to try it, here is the repository link: [EnvyControl on GitHub](https://github.com/bayasdev/envycontrol). There, you will find specific installation tutorials for different distributions.

Now, let's go through the steps to install it on Debian.

## EnvyControl Installation

Since it is no longer possible to install pip packages outside a virtual environment after the adoption of PEP 668, you should use the `.deb` package provided in the repository instead.

1. Find the latest version at the following link: [Releases - EnvyControl](https://github.com/bayasdev/envycontrol/releases/latest).
2. On that page, select and download the corresponding `.deb` package. You can also use the `wget` tool to download it from the terminal.

   ![Download package .deb](/drivers/nvidia_optimus/img/github_deb.png)

3. Install the downloaded package with the following command:

   ```bash
   sudo apt -y install ./python3-envycontrol_version.deb
   ```

## Using EnvyControl

Once you have installed the tool, you can select the GPU you want to use on your computer. Keep in mind that any applied settings will not take effect until you reboot the system.

- To use the **integrated GPU** (for power saving):

  ```bash
  sudo envycontrol -s integrated
  ```

- To enable **hybrid mode** (both GPUs):

  ```bash
  sudo envycontrol -s hybrid --rtd3
  ```

- To use **only the dedicated GPU** (recommended if you need external video ports):

  First, switch to hybrid mode:

  ```bash
  sudo envycontrol -s hybrid
  ```

  Then, switch to dedicated GPU mode:

  ```bash
  sudo envycontrol -s nvidia --force-comp --coolbits 24
  ```

⚠️ **REMEMBER TO REBOOT FOR CHANGES TO APPLY.**

## Additional Notes

I've provided the commands that worked for me, but EnvyControl has its own manual. You can also find more information in the [official repository](https://github.com/bayasdev/envycontrol).

Additionally, there is a GNOME extension that allows you to switch GPUs through a graphical interface. While I personally always work with my laptop plugged in, you might want to switch to hybrid or integrated mode when on battery.

### Conclusion

By now, your NVIDIA drivers should be working properly, and you should be able to use your laptop's video ports without issues.

As mentioned earlier, compatibility may vary depending on your hardware. In my case, video ports only work when I use the dedicated GPU mode. If you're facing a similar situation, don’t hesitate to try this setup!
