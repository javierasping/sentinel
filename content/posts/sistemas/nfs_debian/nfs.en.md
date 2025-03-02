---
title: "Share directories with NFS in debian"
date: 2023-09-08T10:00:00+00:00
Description: Learn how to share directories with NFS in debian
tags: [Linux,Sistemas,ISO,ASO]
hero: images/sistemas/nfs/portada.png
---


The NFS (Network File System) technology has been a key part of file sharing in network environments. Developed by Sun Microsystems, NFS allows Unix and Linux operating systems to share file resources transparently, providing access to remote files and directories as if they were stored locally.

## 1.Installation and NFS configuration

We installed the nfs-kernel-server package.

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.001.png)

We will create the directory we are going to share and change the owners and permissions of it:

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.002.png)

In the file etc / exports we will indicate what our directory is and their respective permissions:

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.003.jpeg)

- * * ro * *: directory reading only permission
- * * rw * *: reading and writing permission of the directory
- * * subtree _ check * *: specifies subdirectories verification
- * * no _ subtree _ check: * * prevents subdirectories verification
- * * sync: * * Write all changes to the disk before applying it
- * * Async: * * ignores synchronization verification to improve speed

We apply the changes and restart the service:

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.004.png)

## 2.Visualize it on a debian client

We will install the following package:

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.005.png)

We put it on our client:

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.006.png)

We can also do this permanently in the fstab:

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.007.png)

We can view the content:

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.008.png)

Let's create a file and check that it has been created on the server:

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.009.png)

## 3 Visualization on Windows

We download the NFS client feature:

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.010.jpeg)

We map the network unit:

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.011.jpeg)

We created a file remotely and we checked that it was created.

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.012.jpeg)

We also checked on the server:

![](../img/Aspose.Words.11ce2099-f519-43cd-a00b-9a47a367ade4.013.png)

