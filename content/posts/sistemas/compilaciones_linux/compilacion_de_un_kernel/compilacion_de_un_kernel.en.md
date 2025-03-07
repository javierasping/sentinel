---
title: "Compilation of a kernel"
date: 2023-11-29T10:00:00+00:00
description: Compilation of a kernel
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/compilacion_de_un_kernel/compilacion_de_un_kernel.jpg
---



## Introduction

For the practice I will choose the kernel 6.4.4 that I have downloaded from the backports repository:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.001.jpeg)

To download the source code we will use apt source:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.002.png)

It will create us a directory with the source code

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.003.png)


If we list the contents of the directory with the source code, we will see that the structure is the same as to compile a package in C.

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.004.jpeg)

### First compilation

The first thing we're gonna do is use the .config file that has our kernel loaded, mine currently has 10640 lines.

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.005.png)

Next we will launch the make oldconfig command to use the current kernel file we are using.

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.006.png)

If we see we have 2413 modules configured in a static way and 3855 in a dynamic way:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.007.png)

Let's pass the localmodconfig parameter, leave the enter pressed to select the different parameters by default.

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.008.png)

We see that with this parameter we have significantly reduced the number of modules, as with the method used in the previous step only those we have currently loaded in the kernel are used:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.009.png)

We'll build the kernel and try it, in my case it starts:

![ref1]

### Second compilation

I will remove some components manually using the make xconfig tool:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.011.jpeg)

After removing several points from the .config I have been left with:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.012.png)

Now we're going to use a method to compile which will make us .deb packages and use 15 cores for it:

![ref1]

We will generate 4 .deb packages in the top directory:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.013.jpeg)

We're going to install them, for that we'll use a wildcard to install all the .deb:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.014.png)

Finally let's make sure the kernel is installed:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.015.png)



### Sign a kernel

As I have the safe start activated on the laptop, you will need to sign the kernel so you can start it.

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.016.png)

So for this we will follow the steps that debian tells us to do it.

If you want to know which keys are in use in your system, several other mokutile calls will help you, for example, sudo mokutile --list-enlisted to show the current list of MOK keys

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.017.jpeg)

To generate a new keys to sign the kernel we will create the following directory:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.018.png)

Let's generate the private and certified key in DER format

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.019.jpeg)

Now let's convert the DER certificate to PEM format:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.020.png)

Now to register a new MOK key, I first issue the request using the mokutile command. I run the following command:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.021.png)

During this process, I will be asked to enter an "one-time password" to confirm the registration. This password is crucial for validating and authorizing the operation.

After issuing the request and providing the password, the key entry is not completed immediately. Instead, I need to restart the system.

When we reboot, we will have a blue screen, we will head for the second MOK roll option:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.022.jpeg)

He'll tell us if we want to add the keys:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.023.jpeg)

And you will ask us to put the password we have indicated in one use:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.024.jpeg)

Once this has been done, we restart the team:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.025.jpeg)

Once the key is added, we can check it with the following command:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.026.png)

For DKMS (Dynamic Kernel Module Support) to automatically sign the kernel modules, it is necessary to tell you which key to sign the module with. This is done by adding two configuration values to the "/ etc / dkms / framework.conf" file, adjusting the routes as needed.

In addition, we will add the following script:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.027.png)

The script will have the following content:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.028.png)

Now we're going to define the variables needed to proceed to sign the kernel, the version one makes it with a -r in the debian documentation but my modules have the 6.4.4 prefix. You can check it on the s / lib / modules / route.

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.029.png)

Now let's sign the kernel:

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.030.png)

Once the kernel has been signed, we can reboot it and check that it starts. It took me more than usual to get started, but in about 2 minutes it finally starts.

![](/sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.031.png)


[ref1]: /sistemas/compilaciones_linux/compilacion_de_un_kernel/img/Aspose.Words.4794869c-382a-4c20-b046-83b787e9bd0a.010.png
