---
title: "Paso de CentOS stream 8 a CentOS stream 9"
date: 2023-11-29T10:00:00+00:00
Description: Step from CentOS stream 8 to CentOS stream 9
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/paso_de_centos_stream_8_a_centos_stream_9/paso_de_centos_stream_8_a_centos_stream_9.png
---



### Update the packages

Before migrating, make sure your CentOS Stream 8 system has all the latest packages and updates.

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.001.jpeg)

Eliminate unnecessary packages that appear to us when using the next command as they are orphaned packages

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.002.png)

## Update to CentOS9

Install CentOS 9 repositories:

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.003.jpeg)

Now let's update the packages to CentOS 9:

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.004.png)

When the installation is finished, some packages may be removed:

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.005.png)

We update the database of the local packages:

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.006.png)

We remove the packages from the cache dnf:

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.007.png)

We update the installed packages:

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.008.png)

We install the packages for the minimum installation of a core server (without graphic environment):

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.009.png)

Now we'll reboot the system and start with CentOS 9:

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.010.jpeg)

When we start we can check that we already officially have CentOS 9:

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.011.jpeg)

## Additional cleaning

If you want you can remove the old kernel:

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.012.png)

Also if you don't have a subscription you can remove the subscription manager:

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.013.png)

### Generate rescue input in the grub

We'll move the old rescue kernel to a temporary folder as a backup:

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.014.png)

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.015.png)

Now we're going to regenerate the kernel entries, the command will not return anything so we can check it by looking at the boot partition:

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.016.png)

Once done, we can restart and check that we have the CentOS 9 recovery input:

![](../img/Aspose.Words.64b29d49-eb3e-49be-9751-9727b0deafb9.017.png)

## Bibliography

Guide to migrating from CentOS 8 stream to CenOS 9 stream

