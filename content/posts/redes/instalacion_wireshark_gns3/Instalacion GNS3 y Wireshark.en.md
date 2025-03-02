---
title: "Installation GNS3 and Wireshark in Debian"
date: 2023-09-08T10:00:00+00:00
Description: Installation of GNSS 3 network simulator and Wireshark protocol analyzer
tags: [Redes, Wireshark, GNS3]
hero: images/redes/instalacion_wireshark_gns3/portada_instalacion_wireshark_gns3.png
---

> * * This post was developed for Debian 11. If you have a more recent version, you can review the Debian 12 post you will find in the network section of the same page. The only part you should not follow if you meet this condition is the installation of GNS3. The rest of the content is still valid.


<! --! [2] (/ images / networks / installation _ wireshark _ gns3 / cover _ installation _ wireshark _ gns3.jpeg)

![](/images/redes/instalacion_wireshark_gns3/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.003.jpeg) -->

## 1. * * Introduction * *

Wireshark is a protocol analyzer used to analyse and solve problems in communications networks, for data and protocol analysis, and as a didactic tool.

Add a graphic interface and many organization and filtering options. So, it allows you to see all the traffic that passes through a network by setting the configuration in promiscuous mode of our network card. It also includes a text-based version called tshark.

It allows you to examine data or a saved capture file on disk. The information captured can be analysed through the details and summaries for each package. Wireshark includes a complete language to filter what we want to see and the ability to show the reconstructed flow of a TCP session.

Wireshark is free software, and runs on most Unix and compatible operating systems.

The minimum requirements for using this software are:

- Any modern AMD64 / x86-64 64 bit or 32 bit x86 processor.
- 500 MB RAM available. The larger capture files require more RAM.
- 500 MB of available disk space. Capture files require additional disk space.
- Any modern screen. A resolution of 1280 × 1024 or more is recommended. Wireshark will use HiDPI or Retina resolutions if available. Advanced users will find several monitors useful.
- A compatible network card to capture

## 1.1 * * Download the package in due * *

To download the package on our computer we will need to look at the [official page] (https: / / www.wireshark.org / download) downloads if it includes support for our operating system.

We see that no GNU / Linux operating system appears on the list, this is because Wireshark is available through the default packaging system on most of these platforms. That is to say this present in the repositories of our distribution, in the event that it is not there we have the source code as a free software and we could compile it.

We can check if it is available in our operating system by visiting the [official page] (https: / / www.wireshark.org / download .html):

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.003.jpeg)
 ! [2] (/ images / networks / installation _ wireshark _ gns3 / cover _ installation _ wireshark _ gns3.jpeg) 
We see that Debian appears on the list this means that the package is in the official repository of due.

In Debian we have the apt package manager, so we can check the version of the package available for installation and check from when repositories are downloaded with the following command:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.004.png)

To perform the wireshark installation we will enter the following command:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.005.jpeg)

Then to make network catches on the equipment we will need permissions for our user to do so, we will use the following command:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.006.png)

## 1.2 * * Operating check * *

We will now open the program to check that everything works properly:

Now we will start a package capture for it if we want to do it on a specific interface we press on it, in my case I will use the wlo1 wireless network card and I will make a web request to the jagger.es page.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.007.jpeg)

Here I show you the DNS request that has traveled from my laptop to the router.


![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.008.jpeg)




## # 1.3 * * General wireshark components * * Wireshark makes use of certain packages:
- * * Wireshark: * * the network protocol analyzer we all know.
- * * TShark: * * a command line network protocol analyzer.
- * * Supplements and extensions: * * extras for Wireshark and TShark dissection engines
- * * Dissector supplements: * * supplements with some extended dissections.
- * * Complements of tree statistics * * -: Extended statistics.
- * * Mate: * * monitoring engine and meta analysis: user-configurable extensions of the screen filter engine; see Chapter 12, MATE for more details.
- * * MIB * * of * * SNMP * *: SNMP MIB for a more detailed SNMP dissection.
- * * Tools: * * additional command line tools to work with capture files
- * * Editcap: * * reads a capture file and writes some or all of the packages in another capture file.
- * * Text2Pcap: * * reads an ASCII hexadecimal overflow and writes the data in a pcap capture file.
- * * Reordercap: * * reorders a capture file by time mark.
- * * Mergecap: * * combines several captured files saved in a single output file.
- * * Capingos: * * provides information about the capture files.
- * * Rawshark * *: unprocessed package filter.
- * * User guide: * * local user guide installation. The Help buttons in most dialog boxes will require an Internet connection to show the help pages if the User Guide is not installed locally.

## 2 * * Installation of GNS3 in Debian 11 * *

### 2.1 ♪ Introduction ♪

GNS3 is a graphical network simulator launched in 2008, which allows you to design complex network topologies and launch simulations on them, allowing the combination of both real and virtual devices.

To complete simulations, GNS3 is closely linked to:

- * * Dynamipes: * * an IOS emulator that allows users to run IOS images.
- * * Dynagen: * * a text-based front-end for Dynamips.
- * * Qemu * * and * * VirtualBox: * * to allow the use of virtual machines such as a PIX firewall or workstations.
- * * VPCS: * * a PC emulator with basic networking functions.
- * * IOU: * * (IOS in Unix), special IOS compilations provided by Cisco to run directly on UNIX systems and derivatives.

The minimum requirements for making use of this tool are:

- * * Processor: * * 2 or more logical cores
- * * Virtualization: * * Virtualization extensions are required. You may need to enable this through your computer's BIOS.
- * * RAM memory: * * 4 GB RAM
- * * Storage: * * 1 GB of available space (Windows installation is < 200 MB).
- * * Additional notes: * * You may need additional storage for your operating system and device images.

## 2.2 * * Installation * *

The first thing we will do before we install will be to check that our system is up-to-date, so we will make an apt update and if we have outdated packages we will make an apt upgrade.


Below we will install all the units you need GNS3:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.010.png)

I will now describe the function of the packages that we will install:



- - - - - - - - - -
- 124; - 124; - 124;
The pipe module is the Python package installer. - 124;
The PyQt5 module exposes the Qt5 API to Python 3.
The PyQt5 SVG module provides classes to show the content of the SVG files. - 124;
The PyQt5 WebSockets module provides Python 3 links for the WebSockets specification (both client and server). - 124;
- 124; qemu - 124; Virtualization software is currently divided into several packages.
- 124; qemu-kvm - 124;
- 124; qemu-utils - 124;
- 124; libvirt-clients - 124; Libvirt is a set of tools in C to interact with the virtualization capabilities of recent Linux versions.
- 124; libvirt-daemon-system - 124; This package contains the configuration files to run the libvirt demon as a system service. - 124;
This package contains some command line utilities to create and edit virtual machines.
It is a network analyzer that captures packages for further analysis.
- 124; xtightvncviewer - 124; '' Remote display system that allows you to see a 'desktop' environment not only on the machine where it is running, but from anywhere on the Internet. - 124;
This is a fictional transition package: compatibility with https.
- 124; ca-certifications - 124; Contains the certificates of the certification authorities that are included in the Mozilla browser to allow SSL-based applications.
- 124; curl - 124; curl is a command line tool to transfer data with URL syntax.
- 124; gnupg2 - 124; It can be used to cipher data and create digital signatures. It includes an advanced key management function and meets the proposed OpenPGP Internet standard. - 124;
- 124; software-properties -common - 124; allows you to easily manage your distribution and software sources from independent software providers. - 124;

Once these packages are installed, we will download GNS3 using pip3:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.011.png)

We will also look at the command output to check for any errors:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.012.png)

The following will be to install docker, which will allow us to create containers. For this we will import your GPG key so that our system trusted the:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.013.png)

The following will be to add the repository to our system for this we will use the following command:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.014.png)

We will update the repositories you use apt by making an apt update:


And we can finally install docker:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.015.png)

Add the following lines to your / etc / apt / sources.list, so that we can install dynamps and ubridge:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.016.png)

In order to install the necessary packages of these repositories, we will add the gpg keys of it:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.017.png)

We will update the repositories you use apt by making an apt update:


We will install the Dynamips and ubridge packages:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.018.png)

A box like this will come out to indicate if users who are not superusers can capture packages, we will tell you that if in our case:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.019.jpeg)

To avoid accidental installation of anything else in that repository (for now), delete or comment those two lines in your / etc / apt / sources.list file and make an apt update:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.020.png)


We can also remove the GPG key from these repositories if we want to:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.021.png)

We will add users who will use the tool to the following groups:

Reset your user session by closing and relaunching it, or by relaunching the system to apply these changes.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.022.png)

## 2.3 * * Our first topology in GNS3 * *

Once the system is restarted, we will start the application, and we will get a box like this:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.023.png)

Here we will indicate that I will run the applications locally in my machine. Below we will select the server route, host name and associated port:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.024.png)

If everything has been right, he will tell us that it has been done correctly:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.025.png)

When we open the program, it will give us a choice to create a project or we can create a new one, in my case I will create one:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.026.jpeg)Si nos fijamos en la parte izquierda del programa veremos los siguientes símbolos que sirven para lo siguiente :

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.027.png)

We will add by dragging 2 VPCS:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.028.png)

We'll add an Ethernet swicht:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.029.png)

We will click on the Add a link button to stop adding links, so we would have the scenario:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.030.png)

We can make visible the interface to which we have connected them by clicking on the following button:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.031.png)El botón verde "Reproducir" en la barra de herramientas GNS3 encenderá todos los dispositivos en la topología, mientras que el botón amarillo "Pausa" los suspenderá y el botón rojo "Detener" apagará todo en la topología:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.032.png)

We'll get a warning, so we can confirm if we want to add all the devices, we'll give you if:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.033.png)

We will see that both left in the device summary and in the outgoing connections of the devices their state "light" to changed from red to green, since these are now on:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.034.png)

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.035.png)

We will now open a terminal on all of our VPCS with the following button:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.036.png)

Through these terminals we will assign ips addresses to our devices with the following command:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.037.png) 

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.038.png)

Once the network cards are configured, we will check for connectivity between them by doing a ping:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.039.png)

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.040.png)

We will add a third VPCS to our scheme:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.041.png)

We will turn it on and open a terminal to configure it as we have done with the above:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.042.png)

And I'll check that this new machine has connectivity to the above:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.043.png)

If we want to save our equipment settings we will enter the save command:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.044.png)

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.045.png)

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.046.png)

## 2.4 * * Internet access via NAT on GNS3 * *

The easiest way to get access to the Internet is through the NAT cloud.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.047.png)

This has Internet access as well as a DHCP service running with IPV4. To make use of it, we will put it on our stage and connect it on a swicht.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.048.png)

Then if we want to get out on the Internet, we will have to set up our customers to get them the right network configuration. We'll take advantage we have a DHCP server.

For customers to configure through this service we will enter the dhcp command:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.049.png)

We'll try to do a ping to google.es to check the connectivity:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.050.png)

## 3 * * Common problems in installation * *

## 3.1 * * VPCS error exectable version must be > = 0.6.1 but not 0.8 * *

This error comes when installing the VPCS, a version that does not currently support the program is downloaded from the repositories.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.051.png)

Luckily it is very easy to solve, we will access the [repository] (https: / / github.com / GNS3 / vpcs / releases) of the developer in github and we will download the following package:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.052.jpeg)

Once downloaded we will uncompress it using the following command:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.053.png)

Where we do this command will create a directory in which we will access to compile the program:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.054.png)

We will run the following script:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.055.png)

The vpcs directory will create us on this route, this one will have to be added in gns3:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.056.png)

We will access gns3, press * CTRL + SHIFT + P * to access the preference panel. Once here we move to the vpcs section and select the directory route we just generated:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.057.jpeg)

We applied the changes and we could already use the vpcs.

## 3.2 * * Xterm not installed * *

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.058.png)

This error appears when we want to access a console of a device of our network typology. To solve this problem the first thing is to close GNS3 and then direct to a terminal to download it, we will use the following command:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.059.png)

We'll reopen the program and we can access the consoles of our machines.

## 4 * * Install IOS images * *

If we want to add to our real hardware system as can be a swan router for example we must access the official GNS3 page and download specifically the one we want to add in my case I will add a swan 3725.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.060.jpeg)

If we click on the download button we will download an extension file, which is a template.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.061.png)

If you look at this case we do not have the possibility to download the image from this repository, it tells us that there is no link available. For these cases there is a cisco repository which has all the images of its products - > tfr.org / cisco-ios

To find out which one to get from here, we will open gns3 and through the top left menu we will click on the file > import applilance section, select the template that we will import. We will give you to install on our local computer:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.062.jpeg)

Once here we are, we will see the name of the file and search it in the external repository, as we can see that the file is not found

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.063.png)

In this case I will download, this version that matches the template I have downloaded:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.064.png)

When we have done this we will have the following problem, the image signatures will not match to mitigate that step we will mark the option allow custom files at the bottom and import the binary we have just downloaded:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.065.png)

Please inform us that for the selected template, the file we downloaded from the repository does not match the hashes. In our case it is normal since the image is not the same as it would have to come with the template, so we will accept the risks.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.066.png)

We'll see you change the state to ready to install, so we'll give you the next on the bottom.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.067.png)

You will ask us for confirmation to add our device, we will confirm the action:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.068.png)

Please inform us that our device has been added to the router templates for this case.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.069.png)

Also inform us of the name given to you.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.070.png)

As I tell us, we'll find it in the routers section:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.071.png)

Now we'll do a little running test, add it to our stage and check that we can start it and connect to the console:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.072.png)

'We'll see the connection to the console is correct:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.073.png)

## 5 * * Installation on GNSS Windows * *

## 5.1 * * Packages needed for Windows * *

Even if we have installed the GNS3 software it will make use of additional packages to perform some functions or even add new features such as emulating routers of certain manufacturers.



- 124; * * Article * * - 124; * * Required * * - 124; * * Description * * - 124;
- - - - - - -
- 124; WinPCAP - 124; Required - 124; Required to connect GNSS 3 to your computer network. Used by the Cloud and NAT nodes to allow their projects to communicate with the outside world. - 124;
- 124; Npcap - 124; Optional - 124; WinPCAP's modern replacement can solve problems but is less proven than WinPCAP.Instale - Npcap with the selected "WinPcap API-compatible mode" option, if used without WinPcap.Npcap can coexist with WinPcap, if that * no * option is selected. - 124;
- 124; Wireshark - 124; Recommended - 124; allows you to capture and see the network traffic sent between nodes. - 124;
- 124; Dynamipes - 124; Required - 124; Required to run a local installation of GNS3 with Cisco routers. - 124;
- 124; QEMU 3.1.0 and 0.11.0 - 124; Optional - 124;<p>A virtualization software. The previous version of Qemu </p><p>0\ .11.0 is installed to support old ASA devices. It is recommended to use the vm GNS3 instead.</p>- 124;
- 124; VPCS - 124; Recommended - 124; A very light PC emulator that supports basic commands such as ping and traceroute - 124;
- 124; Cpolit - 124; Optional - 124; It is used to prevent QEMU from using 100% of its CPU (when it is running) in some cases, as with the old ASA devices - 124;
This is always mandatory. - 124;
- 124; Tiger VNC Visor - 124; Recommended - 124; A VNC client used to connect to the device's graphical user interfaces. - 124;
- 124; Solar-Putty - 124; Recommended - 124; The new default console application. - 124;
- 124; Virt-viewer - 124; Recommended - 124; Alternative Visualizer of Qemu virtual desktop machines that have qemu-spice pre-installed. - 124;
- 124; Intel Hardware Acceleration Manager (HAXM) - 124; Optional - 124; Only available in systems with Intel CPU (and VT-X enabled), which * no * use Hyper-V. It is used for the acceleration of Android emulation hardware as well as for QEMU. - 124;

## 5.2. * * Minimum requirements * *

For small environments on Windows developers require to have at least the following features:

- 124; * * Characteristics * * - 124; * * Requirements * * - 124;
- 124; - 124; - 124;
- 124; operating system - 124; Windows 7 (64 bits) or later - 124;
- 124; Processor - 124; 2 or more logical nuclei - 124;
- 124; Virtualization - 124; Virtualization extensions are required. You may need to enable this through your computer's BIOS.
- 124; memory - 124; 4 GB RAM - 124;
- 124; Storage - 124; 1 GB of available space (Windows installation is < 200 MB). - 124;

## 5.3 * * GNSS 3 installation * *

The first thing that we will have to download the official executable of your website, for this we will have to be registered in advance.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.074.jpeg)

We will launch the executable and ask for the permission of the administration, we will grant them:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.075.png)

A screen will come out informing us about the product, we give it to next.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.076.png)

We will then have to accept the terms and licences for use:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.077.png)

You will ask us where we want to create the shortcuts of the program, I will leave it by default as this will add them to the desktop:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.078.png)A continuación debemos de prestar atención ya que debemos de seleccionar instalación local y todos los paquetes que vayamos a hacer uso , si hubiésemos instalado antes  alguno de ellos los desmarcamos (Los mencionados en el punto 5.1) :

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.079.png)

We will select the route where the program is installed, I will leave the default. It also informs us of the space required by the installation:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.080.png)

We will wait for the installation:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.081.png)

* * WinCap installation * *

Required to connect GNS3 to your computer network. Used by the Cloud and NAT nodes to allow their projects to communicate with the outside world.

As the installation of GNS3 is carried out, the installation of all the programs we have previously marked will begin.

It will show us information about the program this first window so we give you the following:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.082.png)

We accept the license of terms and use:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.083.png)

We mark the option for you to automatically boot the driver and we give you to install

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.084.png)

It informs us that the installation was correct and we close the window:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.085.png)

* * Ncap installation * *

The modern WinPCAP replacement can solve problems but is less proven than WinPCAP.Instale Npcap with the selected "WinPcap API-compatible mode" option, if used without WinPcap.Npcap can coexist with WinPcap, if that option is not selected.

Again the same process, we accept the terms and licenses of use.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.086.png)

We leave the default marked option and give it to install

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.087.png)

When the installation is finished we give you the following:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.088.png)

And we close the installer:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.089.png)Volvemos a GNS3 ya que el proceso de instalación ha quedado detenido mientras hemos instalado los componentes que va a hacer uso , esta se reanuda automáticamente  :

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.090.png)

Once the installation is finished, we give you the next

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.091.png)

GNS3 offers us a free Solarwinds license, we will give you if:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.092.png)

We will have successfully completed the installation of GNS3

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.093.png)

We will open the program and select to run the devices in our local machine:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.094.png)

Here we will configure our local GNSS server 3

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.095.png)

Previously leave it by default, if our configuration is correct, it will tell us that the connection has been performed successfully:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.096.png)

It will show us a summary of the configuration given above:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.097.png)

## 5.4 * * Operating test * *

We will set up the same scenario as in debian to check its operation, the process is the same.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.098.jpeg)

We will set up the ips addresses of the machines and check that they have connectivity through solarputty.

PC1:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.099.png)

PC2:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.100.png)

We can see that both teams have connectivity across the stage.

## 6 * * Wireshark installation on Windows * *

### 6.1 ♪ Installation ♪

The installation of this product is very simple, if we have installed GNS3 previously and marked the box of this, we will have been installed automatically.

On the contrary, if we start from scratch we can do your installation, let's get it off your official website:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.101.jpeg)

When we open the installer you will ask us for administrator's permissions, we will grant it to you:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.102.png)

If, like I installed it with GNS3, we were to find that there is already one installed, so I will cancel it.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.103.png)

If we didn't have it the installation is identical to any program we have installed in practice. Here I show you, the first thing you'll see is an executable information screen:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.104.png)

Like all programs you will be asked to accept the terms and conditions of use:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.105.png)

We will select the products we want to install in my case all:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.106.png)

It will also ask us to access them directly and where we want to create them.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.107.png)

We will select the route where we want it to be installed:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.108.png)

We will select if we are interested in the Ncap package. (We have installed it with GNS3)

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.109.png)

Next you will ask us to install the extension that allows us to analyze USB traffic, in my case the desmarcare as I am not interested.

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.110.png)

We will wait for the installation to complete and give you the following:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.111.png)

Please inform us that the installation has been properly performed:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.112.png)

## 6.2 * * Operating test * *

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.113.jpeg)

I have made a DNS request to [www.sevillafc.es] (http: / / www.sevillafc.es /) and here we can see the DNS consultation:

## 7 * * GNSS VM * *

If we want to deploy virtual machines in a virtual instance we will deploy the virtual machine that gives us GNS3 to carry the Virtualization charge.

We will download the OVA from the official website

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.114.png)

Once downloaded we will import it into Vmware and give you the hardware features we consider appropriate:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.115.png)

Once I do this we will open GNS3 and edit the preferences of GNSS VM and select the virtual machine that we just imported:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.116.jpeg)

We will start the virtual machine and we can see the data from it in the info tab:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.117.png)

We will launch the set-up wizard from the GNS3 help tab and select the option to run the stacks in a virtual machine:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.118.png)

We will select the configuration of our virtual machine:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.119.png)

We will again select our virtual machine and the hardware features we want:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.120.jpeg)

We would only have to import the devices into the virtual machine, this does just like we did before changing the place where we imported it:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.121.jpeg)

If we want to see where a device will run we can see it through preferences:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.122.jpeg)

We can also see in section servers sumarry the resource consumption of our machines:

![](../images/Aspose.Words.7be2264a-b643-4cb1-9a61-896b263a0d52.123.png)

## 8 * * Conclusion * *

We can see that the installation is infinitely more comfortable on Windows as it automatically installs your dependencies, being the typical "next to next" installation.

Also on Windows when the installation was finished the product was ready to use and I have not suffered any errors when starting the program or using its features as if it happened to me in Debian.

#9 * * Bibliography * *

[Official documentation wireshark] (https: / / www.wireshark.org / docs / wsug _ html _ chunked / ChBuildInstallWinInstall.html)

(https: / / packages.qa.debian.org / w / wireshark.html)

[Minimum wireshark requirements] (https: / / www.wireshark.org / docs / wsug _ html _ chunked / ChIntroPlatforms.html)

[Error "VPCS exectable version must be > = 0.6.1 but not 0.8"] (https: / / gns3.com / vpcs-executable-version-must-be-greater-than-0-6-1-but-not-0-8)

[VPCS download] (https: / / github.com / GNS3 / vpcs / releases)


