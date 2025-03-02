---
title: "Creation of an automated installation system"
date: 2023-11-29T10:00:00+00:00
Description: Creation of an automated installation system
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/creacion_de_un_sistema_automatizado_de_instalacion/creacion_de_un_sistema_automatizado_de_instalacion.jpg
---



### Automatic installation of an iso

On the official debian page we will download a debian image, in my case I have selected a netinstall:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.001.png)

Once you download the debian image, we will copy its content into a folder to then make some modifications. To do this we will mount the iso as a loop device:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.002.png)

Once mounted we can see its content:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.003.jpeg)

We're going to make a copy of the files we're going to use to a directory of ours to make changes to them, once we do this we can dismount the image:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.004.png)

Once the files are copied we will move to the directory to create the file preseed:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.005.png)

Within the same we will copy the bookwork template file provided by debian, you can find it on its official page → https: / / www.debian.org / releases / bookwork / example-presed.txt. I will put this file into the fjcd\ _ car folder.

We will edit the template and select the different options:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.006.jpeg)

Once the presede.cfg file is configured, we give permission to the install.amd directory and uncompress the initrd.gz:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.007.png)

We add the lines of our preseed file to the initrd:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.008.png)

We recompress the initrd file and remove the permissions given to the parent directory previously:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.009.png)

Now we will add an input to this file so that when we start the iso we would have an input that will automatically perform the installation with our presed.cfg file:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.010.jpeg)

Finally, the hash is removed from the different iso files and added to the md5sum.txt file:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.011.png)

With this we have only to generate the iso:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.012.png)

If we start with the iso, we will see the entry we have created:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.013.png)

Outcome:

! [ref1]

## PXE server

Now we're going to prepare the PXE server to make a network installation, to set up SNAT on it so that customers have the Internet:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.015.png)

For the change to be permanent I have installed and configured iptables-persistent, also remember to activate the bit of the forweding

Now we install we will install dnsmasq:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.016.png)

And we'll set up the service:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.017.png)

We restart the service to apply the configuration:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.018.png)

Now in the root directory of our tftp we will download the netboot of our debian version:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.019.png)

Now let's decompress the following content:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.020.png)

Once the file is uncompressed, we will create symbolic links to the following files:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.021.png)

Now we have to set up the web server to pass the file presed.cfg, I have put it in the document root of the virtual host by default:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.022.png)

Finally we have left to configure the entry of the iso menu that we have downloaded, we indicate that the file presed.cfg is in the following url:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.023.jpeg)

Now we can start the machine by pxe:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.024.jpeg)

And if we click on the custom input we just created, it will automatically be installed from the presed.cfg file:

![](../img/Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.025.jpeg)


Outcome:

! [ref1]


[ref1]:.. / img / Aspose.Words.87912b93-5caf-4cac-995f-066fba11b8b6.014.jpeg
