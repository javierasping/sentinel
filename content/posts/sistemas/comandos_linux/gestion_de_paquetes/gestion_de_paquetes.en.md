---
title: "Packaging management"
date: 2023-11-29T10:00:00+00:00
description: Package management
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/gestion_de_paquetes/gestion_de_paquetes.jpg
---



### Indicates the steps to be followed to modify DHCP network configuration to static

To configure the ens1 interface with a static IP address (e.g. 192.168.122.10), you must modify the / etc / sysconfig / network-scripts / ifcfg-ens1 file:

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.001.jpeg)

To apply the configuration we restart the Network Manager:

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.002.jpeg)

### Update the system to the latest versions of the installed packages

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.003.png)

### Install the additional EPEL repository.

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.004.jpeg)

### Install the bash- completion package.

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.005.png)

Install the package provided by the dig program, explaining the steps you have taken to find it

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.006.png)

We install the package:

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.007.png)

### Explain which command you would use to view the kernel package information installed

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.008.jpeg)

### Install the additional "elrepo" repository. We import the public key to the repository:

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.009.png)

We install the repository:

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.010.jpeg)

### Find the available versions to install the Linux kernel and install the latest Listamos kernel:

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.011.jpeg)

We install it:

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.012.jpeg)

### Show the contents of the package of the last installed kernel

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.013.png)

