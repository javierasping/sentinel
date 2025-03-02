---
title: "Compilation of a C-program using a Makefile"
date: 2023-11-29T10:00:00+00:00
Description: Compilation of a C-program using a Makefile
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/compilacion_de_un_programa_en_c/compilacion_de_un_programa_en_c.jpg
---



## Introduction

The compilation of programs in programming language C is a fundamental process in software development. It allows the source code written by the programmers to be translated into computer-friendly instructions. One of the challenges associated with the compilation is the efficient management of the project files and units, which becomes even more crucial when working on large and complex projects.

This work aims to explore one of the most used mechanisms to compile projects in C: the use of a Makefile file. A Makefile is a configuration file that describes how to compile the source files of a project and how to manage the units between them. In addition, it allows to automate the compilation process and facilitates the task of maintaining and updating the code.

Throughout this work, we will examine in detail the process of compiling a program in C using a Makefile. We will start by understanding the structure of a Makefile and how the compilation flow is defined. Then we will explore the advantages of its use, such as automatic detection of changes in the source files and selective collection. We will also address best practices to create effective and easy-to-maintain Makefilds.

In addition, we will analyze a practical example of a C program compilation, detailing the steps needed to create a Makefile and compile the project. We will also discuss the installation of the resulting program in a personal directory, avoiding interference with the package system.

Ultimately, we will learn how to clean up the program and understand the importance of proper software management in Unix / Linux systems.

As we progress in this work, we will gain a deeper understanding of the C-compilation and the usefulness of a Makefile as an essential tool in software development.

### Compilation of a C-program using a Makefile

The first thing we're going to install is fundamental for the compilation of C packages in Debian.

The building-essential package provides the necessary compilation tools, and dpkg-dev facilitates package management and source code delivery. You can install other specific development packages according to your needs, but these two are the most essential to start compiling C software in Debian.

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.001.png)

Now let's download the source files from the package that we want to compile in my case I will make it samba:

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.002.png)

Once this is done we will see in our directory that a series of files and directories have been created:

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.003.png)

* * samba-4.17.12 + dfsg: * * This is the directory that contains the Samba source code, which was downloaded from Debian repositories. It is the source that will be used to compile and install Samba in your system.

* * samba\ _ 4.17.12 + dfsg-0 + deb12u1.debian.tar.xz: * * This compressed file contains the specific Debian modifications for the Samba package. You can include patches, construction scripts and other files related to package construction.

* * samba\ _ 4.17.12 + dfsg-0 + deb12u1.dsc: * * This file is the Debian Source Control. It contains information about the source and the versions of the package, as well as links to other files related to the source.

* * samba\ _ 4.17.12 + dfsg.orig.tar.xz: * * This compressed file is the original source of Samba as published on the official Samba website. It is used as a basis for building the Debian package.

Let's get in the main directory and we can see the source code of the package:

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.004.png)

The first thing we will do is install the units of the package that we want to compile in my case samba:

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.005.png)

Now let's launch the script configure. This script is used to configure samba compilation according to your needs and system characteristics:

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.006.png)

Now let's compile the source code using the make command. This will be in charge of compiling the code and creating the executables and libraries that the script has created configure:

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.007.png)

This will take a while depending on the size of the package in my case, it took me 8 minutes:

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.008.png)

Once the code is compiled to install it we will use make install:

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.009.png)

Once this is done we will have our package installed on the route / usr / local:

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.010.png)

Now to start the samba service we will run the nmbd file and make sure it is working:

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.011.png)

We see that the installed version is the one we have compiled:

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.012.png)

### Uninstall the compiled package

To remove the package we have compiled:

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.013.png)

We see that it only leaves us the service configuration files:

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.014.png)

They may remain in our samba trace system as the makefile file is not configured in this case to completely remove it, run whereis and remove the content of the routes:

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.015.png)

Once this has been done, we will have removed the samba trail:

![](../img/Aspose.Words.8ff888af-0a68-4078-abc5-23793c63b7ef.016.png)

