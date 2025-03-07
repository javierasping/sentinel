---
title: "Active Directory in Ubuntu"
date: 2023-09-20T10:00:00+00:00
description: Install and configure samba in Debian
tags: [Debian 12,Sistemas,ISO,ASO]
hero: images/sistemas/ad_ubuntu/portada.jpeg
---


In this post, we will explore how to set up an Active Directory environment on an Ubuntu server using tools such as Kerberos and Samba. Active Directory is an integral Microsoft solution for identity management and access control in business networks. Through this guide, we will learn step by step how to implement a Ubuntu server as a domain controller, establish Kerberos-based authentication and configure directory services by using Samba.

## Introduction

You want to set up a Linux server (Ubuntu Server 20.04 LTS) to service a set of client equipment (Windows and Linux).

I will take advantage that the stage is mounted from previous class activities and I will restore the snapshots to have the clean machines.

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.001.png)

### Preparation of the environment

## 1. The Linux server will not have a graphic environment. You will have at least the partitions: root, home and exchange.

Here we can see that I have no graphic environment installed, we can see that the service is active, however, no environment is launched. Also, if we look for any process with the best known desktop names, it doesn't give us any results.

Here I show you the partitions that my Ubuntu server has (root, boot, home and swap):

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.002.png)

#2. The server must be prepared for remote administration (from now on all management will be done remotely from another network equipment).

To manage it remotely I will use ssh, for this we install it on the server:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.003.png)

Once it is installed we will have it running, no configuration is necessary.

If we check the service status we can see that you have taken the default configuration:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.004.png)

To connect remotely we will need to know the IP of the equipment or the name:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.005.jpeg)

In my case I will connect from the external network to our server (enp0s3), we have previously configured the network with netplan:

And we have implemented the changes:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.006.png)

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.007.png)

Once we know this data we will connect by ssh from a machine in our network to follow with the other sections, in my case I will use my host machine, for this I have installed the openssh-client package previously:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.008.jpeg)

#3. Create the following users and groups

- Groups: teachers, students, smr, asir. I believe the groups:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.009.png)

- User to create: profedesiree, profejose, proferaul, erik, manu, olive, sandra, fabio and domi

I believe the users:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.010.png)

I created them with home directory and assigned them the 1234 password:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.011.png)


- Teachers: profedesiree, profejose and proferaul. We add them:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.012.png)

We can check that they have been added with the following command:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.013.png)

- Students: erik, manu, olive, sandra, fabio and domi.

We add them:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.014.png)

We check that they have been added:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.015.jpeg)

- Users of the group smr: profedesiree, profejose, proferaul, erik, manu and olive.

We add them:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.016.png)

We check that they have been added:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.017.png)

- Users of the asir group: sandra, fabio and domi.

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.018.png)

We check that they have been added:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.019.png)

## 4. All users will be Samba users. For this we must have installed samba:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.020.png)

To add a samba user we must enter the following command and assign a password:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.021.png)

We will do this with the 9 users, once added we can use this command to list the samba users we have:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.022.png)

### Samba domain controller

## 5. Create and configure a Samba domain controller on the Server.

Before starting the installation we must take into account a number of data:

* Active Directory * domain controller name: FJCD

- Name of the domain of * Active Directory *: javiercrucies.local
- Name of the Kerberos Kingdom: javiercrucies.local
- NetBIOS name of the domain: javiercrosses
- Fixed IP address of the server: 192.168.0.1
- Server role: Domain Controller (DC)
- DNS Reporter: 192.168.0.1

Once with these clear data we will start with the installation, the first thing is to update the system:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.023.png)

Next we will need to change the name of our server to be in line with the data we have selected before, for this I have selected my initials, for this we edit the file * / etc / hostname *:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.024.png)

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.025.png)

Now we need to reboot the equipment to apply the changes, we will lose the connection by ssh:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.026.png)

Let's take the ssh remote control back in a few minutes when you have restarted:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.027.png)

As you can see we have connected using the old name that our server had, this is because the / etc / hosts file, contains an IP address ratio with its corresponding logical names. This file contained a reference to the old name of the server itself, which we will change to refer to the new name:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.028.png)

Once we have applied these two changes, before we continue we would only have to make sure that our server has the network properly configured. In our stage we have two network cards on our server:

- enp0s3 (External card, gives us internet access)
- enp0s8 (Internal card, is the one that communicates with our local network)

Because of this the first is configured by DHCP, as we do not care about the configuration that is assigned to it, however, the second is configured statically, as we must control the configuration of it so that we have control over it and then join the equipment to the domain.

Once this is clarified, at the beginning of the document I indicate how the interfaces are configured, here I leave a screen to remember the addresses:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.029.jpeg)

We will now need to have some packages that must be installed before starting, these are:

- samba: file server, printing and authentication for SMB / CIFS. smbclient: command line customers for SMB / CIFS.
- krb5-config: Configuration files for Kerberos Version 5.
- winbind: Service to solve information about users and groups of Windows NT servers.

We can install these four packages with a simple command:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.030.png)

Kerberos, will ask us about the kingdom (domain name) during the installation of the packages, in our case it will be javiercrucies.local:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.031.jpeg)

Here we will enter the name of our server team:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.032.png)

Here we will re-enter the name of our server:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.033.png)

After this, the installation will continue a little further, but without need for more information:


![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.034.jpeg) 

We will now configure samba, but before we do so we will change the name to the * smb.conf * configuration file so that you do not use it while we configure it and so we will also have a copy of the original file:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.035.png)

We will use the samba-tool domain provision command, so that it is the command itself that requests the values you need and, where possible, suggests its default values. So, if these match those we expect, it will be very likely that the previous steps have been the right ones:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.036.png)

As you can see, it is very intuitive to do so, since except for the forwarder IP and the administrator password we have chosen the answers that the same command offers us. This must meet minimum complexity requirements:

- at least 8 characters
- 1 capital
- 1 number or symbol

This, in addition to setting up Samba, has generated a configuration file for Kerberos on the route / var / lib / samba / private / krb5.conf. So we'll copy it to / etc:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.037.png)

The following will be to configure the resolution of names, for this we will start by stopping the services involved:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.038.png)

We will also remove them from starting automatically when restart the equipment:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.039.jpeg)

We will then make sure that the samba- and ad- dc service can be started without difficulty, avoiding any masking that may exist:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.040.png)

Then we delete the resolv.conf file which, in fact, will be a link to stub-resolv.conf. So we eliminate it and create a new one to remove it:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.041.png)

We now introduce the right values according to our domain, for my case:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.042.png)

We save the changes and get out of the file.

We will start the samba-ad@-@ dc service and enable it to start when restart the equipment:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.043.png)

## Check the installation

If we have managed to get here, we have all the ballots so that our installation has been correct. But it's never too much to do a few checks.

## Consult the domain level and create a new user

To know our domain level we simply enter this command:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.044.png)

In doing so, we check that the level of the domain, and of the forest where it is located, is equivalent to a Windows Server 2008 R2 installation

We will try to create a new user account in the domain with the command (we will need to take into account password policy):

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.045.png)

## Confirm that the DNS server works properly

The first thing is to check the LDAP service on the TCP protocol, for which we will write the following order:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.046.png)

If we have an answer similar to that, it all works as it should.

We will then check the SRV record for the Kerberos protocol on UDP, for which we use the following order:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.047.png)

The answer must be similar to the previous one, if so SRV record is correct.

Finally, we check the resolution of the name of our server:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.048.jpeg)

## Check the operation of Kerberos

To check the operation we can, for example, use the smbclient command to check the services that a particular user can get. For this we will use the following command:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.049.png)

If authentication is correct, we'll know Kerberos is doing his job. If we want, we can even log into the server using the administrator account. To achieve this, we will use a syntax like this:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.050.png)

We've already checked everything so we can start joining customers to our domain.

### Join the domain

#6. It integrates at least one Windows client into the Samba domain.

Windows client

The first thing we will do is set up our client's network:

- IP: 192.168.0.10
- Subnet mass: / 24
- Liaison door 192.168.0.1
- DNS 192.168.0.1

Both cards (Internal server and Windows client) must be in internal network for communication.

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.051.png)

Once the card is configured, we will do a ping to the server to check the connectivity:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.052.png)

Now we access control panel → system and security → system → advanced system configuration → team name → network id. We select the first option to join the domain

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.053.png)

We will select the first option, as our network has a domain:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.054.png)

We will now need to enter the data of the administrator user and the name of our domain:

The administrator user that is created by default in samba is called the administrator

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.055.png)

Once you enter the data you will ask us if we want to create a domain account on this computer, I will select that no:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.056.png)

And for the changes to be applied, we must restart:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.057.png)

Once restart we can log in with the different users of our domain:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.058.jpeg)

We can see that we can log into the team with the accounts of our domain:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.059.jpeg)

Linux client

The first thing is to set up the network, for which I have assigned the IP address 192.168.0.2

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.060.jpeg)

We will now have to add to our server in the host file, a line in which the IP address of our server will go followed by the name of this server and the full domain name of our server:

To check this change we have made we will do a ping to the server using its name:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.061.jpeg)

We will now update the equipment to download the latest versions from the repositories:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.062.jpeg)

To have the Internet on the client I have previously configured NAT on the server.

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.063.png)

Once the system is updated we will install the following packages:

- sssd (System Security Services Daemon): Manages authentication mechanisms and access to remote directories. It replaces the classic Winbind with more speed and stability.
- heimdal-clients: This is a free implementation of Kerberos 5 created with the intention of being compatible with the Kerberos protocol implemented by the MIT.
- msktutil: The utility of Kerberos' keytabs in a Microsoft Active Directory environment.

We can do it with 1 command:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.064.png)

As we install you will request the name of our active directory server so we enter it:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.065.png)

Now you will ask us the name of the computer that acts as a server in our case is:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.066.png)

Finally, he will ask us about the administrative server that in our case is the same:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.067.png)

Once this is done, the installation will continue without having to enter more data.

Now let's add additional data to Kerberos to make sure it behaves properly. We will start by changing the name of the configuration file, so that we can return to the original parameters if necessary:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.068.png)

We will now use nano to edit the file settings, it will be empty so we will add the following:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.069.jpeg)

Once filled in with our domain data, we save the files and check if we can log into the domain:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.070.png)

If the output does not offer us any error, it is because the authentication process has worked properly.

We will proceed to join the domain, for this we will use the following command:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.071.png)

This command will have to be completed according to the data of our domain, in case we do not get any output, we will have joined the domain.

To complete the task, we will remove the kerberos authorization tickets that we activate when running kinit. To achieve this, just use the kdestroy command.

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.072.png)

## Share folders

#7. Personal folders are needed on the server for each user. There will also be a folder for each group, to which only the members of each group can access and write.

We will create the directories in the root partition for each user and one for each group. These will be created by the name of the group or user:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.073.png)

We have to bear in mind that the samba users we have generated at the beginning of the document have been removed when installing the domain and we will have to produce them again.

We will share these folders through samba, for this we edit the / etc / samba / smb.conf file:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.074.jpeg)

To indicate that you can access a group we will have to put an @ in front of the group name:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.075.jpeg)

We would only be able to correctly assign the appropriate local permissions for our resources and change the folder owners so that users can write on them:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.076.png)

This would be the right thing to do, but if we assign you the 775 permissions we can't write in the folder, so we'll assign you all the permissions:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.077.png)

Now we'll repeat this with all the directories, first I'll give you the permissions:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.078.png)

And finally we will change the folder owners and make each user or group their respective owners:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.079.png)

Let's make sure we have applied these changes correctly:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.080.png)

We will check that we can access the shared resources from the olive user, we will access the Oliver folder and create a directory within:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.082.png)

## 8. From Windows access these folders through network drives.

From the file browser we can see all the shared resources on the network. Now we will create network units, so for example we will add the Oliver folder to the Oliver user as a network drive, for this, we right click on the folder > connect to network drive:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.083.png)

And we will select a letter to assign to the network unit:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.084.jpeg)

Now this unit will appear on this team:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.085.jpeg)

### Mobile profiles

## 9. Define mobile profiles on the Linux server using Samba, so that users can authenticate on different Windows machines, maintaining their configuration. To do this we will install RSAT (Remote Server Administration Tools) that will allow us to manage our samba domain controller identical to windows server.

To add them we will search the search for Windows * * * Add optional features * * once here we will give you to add feature:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.086.png)

Once here we will look for the following features with RSAT and install them:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.087.png)

Once installed we will be created an application similar to that of a Windows server called administrative tools:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.088.png)

We will be opened a folder with the management tools:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.089.jpeg)

And we will search for user management and active directory equipment or write in running dsa.msc, this we will do with the user managing our domain to be able to access this:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.090.png)

Before creating our mobile user we will create a network resource as we have previously done called profiles and we will give the mobile group permission to write on them:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.091.png)

For our user to write in this directory we will add it to the group:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.092.png)

Now we go to the configuration of our user and we change the profile path. We will put the path of our shared folder profiles followed by * *% username% * *:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.093.png)

We kept and we would have made our mobile profile created.

We will demonstrate the operation of the mobile profile, for which I have changed the background and created two folders:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.094.jpeg)

Now let's log in and start it on the Windows on the right:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.095.jpeg)

We see that the mobile profile has been properly performed.

## NFS

## 10. Through NFS, folders: projects, documentation, programs _ and _ drivers will be shared on the server. The first can only be read; the last two can also be written. Linux equipment will automatically mount the folders in the boot.

The first thing we will do is install the following packages:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.096.png)

Now we'll create in the root the directories we're going to share:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.097.png)

And we'll change the owner and the permissions to these directories:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.098.png)

After this, we must edit the / etc / exports file. This is the file where the folders we are going to share are indicated to NFS. The first one will be read only and the last two can be written:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.099.png)

To access these resources on the server we will install the following packages:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.100.png)

Now we will create the directories where we will mount our folders:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.101.png)

To manually mount them in Linux we will do the following command:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.102.png)

Let's check that in projects we can't write:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.103.png)

While in the other two we can write:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.104.png)

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.105.png)

If we want to access these resources in Windows -- >\\ 192.168.0.1\ documentation

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.106.png)

\\ 192.168.0.1\ projects (reading only directory)

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.107.png)

\\ 192.168.0.1\ programs\ _ and\ _ drivers

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.108.png)

To view them you need to have the following features installed in Windows (We can access this program through the Windows search engine by writing Windows features)

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.109.png)

To end with this point we will set that Linux equipment automatically mount when you start the directories. We will edit the / etc / fstab file by adding the following lines:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.110.png)

Once this is done we will reboot and we will see that we will have been automatically mounted:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.111.png)

Quotas

#11. The server / home folder will have a quota system to avoid saturation with user files (100 MB per user).

The first thing we will do is install the packages to implement quotas:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.112.png)

We will now allow the shares in the partition / home by adding this to the fstab of our server:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.113.png)

We take the home partition to apply these changes:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.114.png)

And we apply quotas on the partition / home

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.115.png)

We will check that at the root of the partition we have been created two files (afuca.group and afuca.user):

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.116.png)

We will now apply the 100Mb quota to olive using edcupa:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.117.png)

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.118.png)

We will now use a tool which is * gawk, * which will allow us to focus on this command, apply the quota we have just created for Oliver to all our users:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.119.png)

The order we just launched has drawn a list of all users and has applied Oliver's quota to all users with an ID greater than 499.

We will now review the quotas to see how they are:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.120.jpeg)

To check that it works we will exhaust the proferaul user's share, for this we will create a 30 MB file:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.121.png)

Now we'll move him to the home directory of him and make him the owner of the file:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.122.png)

We see that the space used in the user directory is updated:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.123.png)

## Webmin

#12. Install Webmin on the server to have the possibility to manage it graphically from a client. Show some of your functionalities.

Webmin is a modern web control panel that allows you to manage your Linux server through a browser-based interface.

We will need to install apache to be able to install webmin on our server:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.124.png)

We will now have to add the webmin repository, so we will edit the sources.list and add it:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.125.png)

We save the file and make an apt update to update the repositories, we will be wrong warning us that the repository is not reliable.

So now we will download the PGP key from Webmin and add it to our system:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.127.png)

We go back to making an apt update and see that now the repository is reliable

Below we will download the webmin package:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.129.png)

The latest lines of the installation will give us the data to access this service web:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.130.png)

So in a client we go to the browser and access this url:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.131.jpeg)

It will tell us that the connection is not private, to skip this warning Advanced configuration > access

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.132.png)

We will have a portal where we will need to enter with an administrator user of our server:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.133.png)

The first thing we will see on the web interface will be a resource monitor, as well as data from our team:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.134.jpeg)

We will see a resource monitor history, which will show us the hours and percentage of use of our hardware, as well as system information:


![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.135.jpeg) 

We have more sections such as recent login or network interfaces, which will give us information about who has connected and their settings respectively:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.136.jpeg)

To end with the panel we will have a last window which will tell us the use of the disk and partitions:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.137.png)

Once we have taken a look at the main page we are going to take advantage of a functionality that has to allow us to view the directories shared by nfs, to access here we are going to networking > NFS exports:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.138.jpeg)

Come on, it also allows us to edit the current shared directories as well as add or delete these.

In addition, this tool allows us to set up a Firewall with iptables, which is now of vital importance to have security on our network:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.139.jpeg)

It even has a web terminal so that we can manage the server from a client, to access it we deploy the menu and click on the terminal symbol or we press Alt + K:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.140.png)

We see you using ssh with the user connected in the application, in my case javiercrosses:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.141.png)

Webmin includes many more management functions that help us work with the server in a graphic way to make it more friendly to manage it, from updating packages to setting up a Firewall. In addition, it uses https, so our traffic would travel encrypted, which would allow us to configure nat to be able to access from a device that is outside our network, without a snifer being able to decipher our traffic easily. It is advisable that we change the self-signed certificate that uses webmin to one of our own that we can generate with Let's encrypt, for example.

## CUPS

#13. There will be a CUPS printing server, which will be administered from a Ubuntu client. The first thing we need to do is install on the cup server:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.142.png)

Once this is done we will configure the service to allow to be managed from our Ubuntu client, for this we edit the following file:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.143.png)

We will now add the following parameters:

- Listen 192.168.0.1: 631
- allow 192.168.0.0 / 24

To allow our client Ubuntu to be able to manage the service

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.144.png)

Now we'd only have to restart the service:

We will move to the client and in the browser we will enter the ip of our server followed by two points and 631:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.146.jpeg)

With this we have checked that the client can manage coups.

#14. Set up a network printer for all users, with daily page limits for all users.

To share our network printer, we access the web panel and in the management section we mark sharing printers connected to this system:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.147.jpeg)

Before setting the limits we will enable the service to register the name of the users when sending files, for that in the cups.conf file we change this default value to none:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.148.png)

We will now restart the service:

To set a daily limit for each 20-page user for example, we would apply the following command for our printer.

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.149.png)

Once this command has been applied, users will only be able to print the indicated number of pages, when they exceed the limit the works will be sent to cups, but it will remove them from the tail and will not print them:

![](/sistemas/ad_ubuntu/img/Aspose.Words.2fdbf265-b3ba-4503-a174-3e0534a81c76.150.jpeg)

In other words, work 21 in this example will not be created until 24 hours.

## Bibliography

- [How to know what desktop I have] (https: / / www.sysadmit.com / 2020 / 06 / linux-as-know-that-scriptorio@-@ tengo.html)
- [Mounting samba domain controller] (http: / / somebooks.es / create -a-controller-de-domino-de-active-directory-con-samba-en-ubuntu-18-04-lts /)
- [Configure the network with netplan] (http: / / somebooks.es / establish -a -direction-ip-estatica-ubuntu-server-17-10-posterios /)
- [Unite client linux to domain part 1] (http: / / somebooks.es / unir-a-cliente-ubuntu-20-04-a-a-domine-of-active-directory-over-windows-server-2019-part-1 /)
- [Unite client linux to domain part 2] (http: / / somebooks.es / unir-a-cliente-ubuntu-20-04-a-a-domine-of-active-directory-over-windows-server-2019-part-2 /)
- [Manage domain with RSAT] (http: / / somebooks.es / 12-7-administrar-el-control-de-domino-resara-con-rsat /)
- [Access shared folders w10] (http: / / somebooks.es / nfs-parte-6-acceder-a-la-carpeta-comparta-de-a-cliente-windows-10 /)
- [Contributions] (https: / / www.linuxtotal.com.mx / index.php? cont = info _ admon _ 018)
- [Installation and use of webmin] (https: / / www.digitalocean.com / community / tutorials / how-to-install-webmin-on-ubuntu-20-04-es)
- [CUPS Commands] (https: / / docs.oracle.com / cd / E26921 _ 01 / html / E25809 / gllgm.html)

