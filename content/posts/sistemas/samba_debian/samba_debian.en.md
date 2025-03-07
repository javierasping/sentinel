---
title: "Install and configure samba in Debian"
date: 2023-09-20T10:00:00+00:00
description: Install and configure samba in Debian
tags: [Debian 12,Sistemas,ISO,ASO]
hero: images/sistemas/samba_debian/portada.png
---


Samba is a free and open source implementation of the Server Message Block (SMB) protocol, which is used to share files and printers on computer networks. The SMB protocol is a network protocol that allows Windows operating systems to communicate with other network devices, such as file servers, printers and other shared resources.

Samba facilitates interoperability between Windows systems and Unix / Linux-based operating systems by allowing Unix systems to share files and resources with Windows systems using the SMB / CIFS protocol. This means that a Samba server can act as a file server for Windows customers, allowing them to access and share files as if they were in a Windows environment.

## 1.Installation

The first thing is to install the samba server:

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.001.png)

In the / etc / samba / smb.conf file we will make the configuration of our folder:

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.002.png)

We will create a samba user to access the resources:

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.003.png)

We will restart the service to apply the configuration:

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.004.png)

## 2.Access from Windows

Now we can access from a Windows client with the user we just created -- >\\ IP\ DIRECTORY\ PARTICIPING

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.005.png)

He will ask us to become self-conscious:

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.006.png)

We can see the content and create:

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.007.png)

## 3.Access from Linux

We install the smbclient package to connect to shared units with samba:

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.008.png)

List shared directories:

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.009.png)

We connect to the shared resource

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.010.png)

I will create a directory and check that it exists:

![](/sistemas/samba_debian/img/Aspose.Words.7699cd74-f258-4715-a7b4-6d378b49c946.011.png)

## Bibliography

- [Enable guest access] (https: / / learn.microsoft.com / es-en / troubleshoot / windows-client / networking / cannot-access-share-folder-file-explorer)

