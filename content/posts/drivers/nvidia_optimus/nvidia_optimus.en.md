---
title: "How to choose which graph to use on my laptop with Linux"
date: 2024-09-01T10:00:00+00:00
Description: Learn how to install NVIDIA drivers in Debian 12 to optimize your system's graphic performance.
tags: [Controladores NVIDIA, Linux]
hero: images/drivers/elegir_grafica.png

---


If you have a Linux laptop and a Nvidia graph, you may have noticed that the video ports are not working properly after installing the graphics drivers. If it sounds familiar, don't worry, I got you covered.

I've been investigating and I found a tool that can save you several headaches. It's called EnvyControl, and it's a command line (CLI) utility that allows you to easily choose which graphics card you want to use on your computer. This is especially useful if your laptop has a hybrid graphics configuration, such as Intel + Nvidia or AMD + Nvidia.

In my case, I set up the tool to always use the dedicated graph, and voilà! The video ports started running smoothly.

EnvyControl is free, open source, and is distributed under the MIT license. Please note that the software is provided as, without guarantees. In addition, any custom X.org settings could be overwritten by changing modes.

If you want to try it, I'll leave the link to the repository: [EnvyControl in GitHub] (https: / / github.com / bayasdev / envycontrol). There you will find specific tutorials to install in different distributions.

Then I will guide you through the steps to install it in Debian. Let's get to it!

EnvyControl installation

Since it is no longer possible to install pip packages outside a virtual environment after the adoption of PEP668, instead, it uses the .deb package provided by the repository.

1. Find the latest version at the following link: [Releases - EnvyControl] (https: / / github.com / bayasdev / envycontrol / releases / latest).
2. On that page, select and download the corresponding .deb package. You can also use the wget tool to download it from the terminal.

 ! [Download package .deb] (.. / img / github _ deb.png)

3. Install the package downloaded with the following command:

```bash
    sudo apt -y install ./python3-envycontrol_version.deb
```

Uh...

Once you have installed the tool, you will have the ability to select the graphic card you want to use on your computer. It is important to remember that any applied settings will not take effect until you reboot the system.

Suppose you decide to use the integrated graph to save energy, for example. The corresponding command would be:

```bash
sudo envycontrol -s integrated
```

If on the contrary you want to use the hybrid mode (both)

```bash
sudo envycontrol -s hybrid --rtd3
```

If you prefer to use only your dedicated graph, please note that this is the only configuration that has worked for me to activate the video ports. To make the jump in this way you will first be asked to put the above mode, the hybrid. Once you are in that mode the command to activate only your dedicated graph:

```bash
 sudo envycontrol -s nvidia --force-comp --coolbits 24
```

I insist again but * * RECOGNIZE TO BE APPLICED IN CHANGES * *.

At this point, I have provided you with the commands I have used, but the program has its own manual. In addition, in the author's repository, you can find additional useful information.

It also explains that there is an extension of gnome so that you can make these changes from the graphic interface. Although I personally always have a plug where I work with the laptop, you may want to change to the hybrid mode or the integrated graph.

### 
So far, I trust that NVIDIA drivers are working properly and that you can already use your computer's video ports without problems.

As I mentioned before, compatibility may vary according to your hardware. In my case, video ports only work when I use the mode of the dedicated graph. So if you're in a similar situation, don't hesitate to try this configuration.