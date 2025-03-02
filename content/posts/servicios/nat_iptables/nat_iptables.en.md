---
title: "NAT with iptables"
date: 2023-09-08T10:00:00+00:00
Description: Installation of a basic scenario and configuration of SNAT
tags: [Servicios,NAT,SMR,IPTABLES,SNAT]
hero: images/servicios/nat_iptables/portada_iptables.jpeg
---


#NAT with iptables
In this article you will learn to set up a small scenario in which you can set up a series of services. You will create the scenario described below, and you will make it through an internal network, using a Linux server, that you have access to the Internet by configuring SNAT in it by using iptables.
## Installation of the test environment
We will install the following environment:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.001.png)

VirtualBox configuration
Debian server:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.002.png)

Customer windows

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.003.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.004.png)

Debian client

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.005.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.006.png)




### Network configuration
The first thing we will do is set up the network cards of our machines.

## # Debian server
We edit the file with nano / ect / network / interfaces as a superuser and add the following lines.

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.007.png)

The red tables correspond to the configuration of the network cards enp0s3 (external card) and enp0s8 (internal network). The blue table corresponds to the ipable rules to allow requests to be made abroad and to prohibit the interior.

### Debian client
We edit the file with nano / etc / network / interfaces as a superuser and add the following lines. The link door will be the ip address of the internal server card.

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.008.png)


## # Windows 10 client
In windows 10 we set up manually by accessing network connections > configuration of the adapter > ipv4 and we assign you the following. Like the client debian changing the address ip. I have put dns from Google because I use my mobile network.

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.009.png)





### Nat configuration on server
Modify the / etc / sysctl.conf. file The line must be discounted:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.010.png)

We check if it has been applied.

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.011.png)


### Internet check on customers

Windows 10

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.012.png)

### Debian 11

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.013.png)
