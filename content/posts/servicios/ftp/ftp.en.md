---
title: "FTP bajo debian"
date: 2023-09-08T10:00:00+00:00
Description: FTP server configuration
tags: [Servicios,NAT,SMR,IPTABLES,SNAT,SSH,FORWARDING,APACHE,FTP]
hero: images/servicios/ftp/portada-ftp.png
---


♪ FTP server under debian
### Installation and configuration of the authenticated proFTPd server
1. First we will create a group called ftpgroup:
![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.160.png)

2. Create two local users from the ftp group we have created: Jose and Maria

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.161.png)

3. We install the ftp service:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.162.png)

4.Basic configuration of the proftpd.conf file:

All users access your directory only:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.163.png)

We can now access from the browser with users Jose and Maria:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.164.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.165.png)

Each of these I have created a folder with your name within your personal directories in order to identify them.

In order for each user to really connect to the FTP server in Debian and you can upload and download the data into your own directory, you must enter your input directory into proftpd.conf:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.166.png)

We can transfer files correctly:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.167.png)

## ProFTPd configuration to create anonymous ftp

The first thing we have to do is create the directory and give it the right owner:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.168.png)

Now we will change this rule and allow everyone to join:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.169.png)

We also add the following lines and will indicate the route to which the anonymous will access:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.170.png)

So when we reboot, anonymous users can connect:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.171.png)

But not with the users we've created before:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.172.png)

To allow our users to connect in addition to the anonymous:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.173.png)

Now we apply these changes and try to connect. We see that with anonymous we can't copy anything to the server but if we can download.

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.174.png)

Now with a group user, we can copy files:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.175.png)