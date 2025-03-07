---
title: "Paid management exercises"
date: 2023-11-29T10:00:00+00:00
Description: Paid management exercises
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/ejercicios_de_manejo_de_modulos/ejercicios_de_manejo_de_modulos.jpg
---

### Work with apt, aptitude, dpkg

## Exercise 1 What actions I get when performing apt update and apt upgrade. Explain in detail.

The apt update command is the first fundamental step in the package update. It takes the following actions:

-**Recovers Remote Metadata:**apt update communicates with online software repositories and recovers metadata related to available packages. These metadata include information on the latest versions of the packages, their dependencies and other essential information.
-**Update the Local Metadata Copy:** Then apt reconstructs and updates the local copy of these metadata. This allows the system to quickly access information about the packages without having to download it repeatedly.

Once apt update has updated the information on the available packages, the next step is to use the apt upgrade command. This command makes a number of important steps:

-**Selection of Candidate Versions**: apt selects the candidate versions of the available packages. These versions are often the most recent, although there are exceptions.
-**Unit Resolution:** apt verifies and resolves the units between the packages to ensure that the update is carried out in a coherent manner and that all units are satisfied.
-**Packaging download:** If you find new versions of packages, apt download these versions from the online repositories to the local cache of the system.
-**Packaging:** apt unpack the recovered binary packages.
-**Execution of Orders Against:** During the update, pre-installation command files are run, which may contain necessary settings and settings prior to installation.
-**Installation of binary files:** The binary files of the new versions of the packages are installed in the system.
-**Execution of PostInst Orders:** Finally, post-installation command files are run, which can perform additional settings after installation.


## Exercise 2 List the list of packages that can be updated. What information can you draw according to what was shown in the list?

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.001.png)

You can check the list of packages that can be updated using the following apt list --upgradable command. This command will show a list of packages available for the update and provide information on each of them. Here is a brief description of the information you can get from this list:

- Package Name: The package name is the first column of the list. It shows you the name of the package that can be updated, for example, the name of the package.
- Current version: The currently installed version of the package is on the right of the package name, in the second column. For example, 1.2.3.
- Available version: The third column shows the latest available version of the package in the repositories. For example, 1.2.4.
- Update Status: In the last column, the status of the update is indicated. If there is an asterisk (\ *) next to the package name, it means that that package is marked to be updated.
- Description of the Package: In addition to this basic information, the list also provides a brief description of the package, which gives you an overview of the function of the package and its purpose.


Exercise 3 Indicates the installed version, candidate as well as the priority of the openssh-client package

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.002.png)

## Exercise 4 How can you get information out of an official package installed or not installed?**We can use the apt show command for packages installed as for non-installed.

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.003.jpeg)

We can also do it with dpkg but the package has to be installed → dpkg -s:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.004.jpeg)


## Exercise 5 Take all the information you can from the openssh-client package you have currently installed on your machine

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.005.jpeg)

## Exercise 6 Take all the information you can from the openssh-client package candidate to update on your machine

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.006.jpeg)


## Exercise 7 lists all the content regarding the current openssh-client package of your machine. It uses both dpkg and apt for this.

Using dpkg:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.007.jpeg)

Using apt:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.008.png)


Exercise 8 List the contents of a package without the need to install or download it.

We can use apt file:

- apt-file list [package]

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.009.jpeg)

Exercise 9 Simulates the installation of the openssh-client package

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.010.jpeg)

## Exercise 10 What command informs you of the possible bugs that a certain package presents?

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.011.png)

## Exercise 11 After an apt update & & apt upgrade. If you wanted to update only the packages that have openssh chain. What procedure would you follow? Take this action, with the repetitive structures offered by bash, as well as with the xargs command.

Using the repetitive structure of bash, using one line:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.012.png)

Using xargs:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.013.png)

## Exercise 12 How would you find which packages depend on a specific package?

With this we see the dependencies of the direct package:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.014.png)

While with this the indirect dependencies:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.015.png)

## Exercise 13 How would you proceed to find the package to which a particular file belongs?

We can use dpkg:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.016.png)

We can use apt-file:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.017.png)

## Exercise 14 What procedures would you use to release the cache in terms of parcel downloads?

To clean the download cache:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.018.png)

To remove downloaded packages that are no longer in use:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.019.png)

Or we can do both at once with apt clean:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.020.png)

## Exercise 15 Realizes the installation of the keyboard-configuration package by previously passing the values of the configuration parameters as environment variables.

We make sure we have the package installed:

For this we install debconfs-utils:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.021.png)

In a file we declare the variables we want to set on the keyboard:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.022.png)

And we provide them to the debconf:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.023.png)

And we will see that the changes have been implemented:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.024.jpeg)

## Exercise 16 Reconfigure the local package of your team, adding a location that does not exist previously. Check to modify the corresponding environment variables so that the user session uses another location.

If we want to store our settings for each user we will export our variables and put them in the bashrc:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.025.png)

Then we will run dpkg-reconfigure and observe that we will have selected the value of the variable:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.026.jpeg)

## Exercise 17 Interrupts the configuration of a package and explains the steps to be taken to continue the installation

Once we break into the installation of a package, to continue the installation of the package we can use the dpkg command:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.027.png)

We can use the -a parameter for all packages or specify the name to continue your installation:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.028.png)

## Exercise 18 Explains the instruction you would use to make a complete update of all the packages in your system in a completely non-interactive way

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.029.png)

## Exercise 19 Blocks the update of certain packages

We marked it to avoid updates and listed the marks to check that it was not updated:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.030.png)



### Work with .deb files

## Exercise 1 Download a package without installing it, i.e. download the corresponding .deb file. It indicates different ways of doing it.

We can use the apt command:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.031.png)

We can use wget and download it from the repositories of should:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.032.jpeg)

## Exercise 2 How can you see the content, not extract it, from what will be installed in the system of a deb package?

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.033.png)


## Exercise 3 On the .deb file downloaded, use the ar. ar command to extract the content of a deb package. It indicates the procedure for viewing the contents of the package. With the package you downloaded and using the ar command, decompress the package. What information do you have after the extraction? It indicates the purpose of the extracted.

To view the content:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.034.png)

To decompress the directory:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.035.png)
We have extracted 3 files from the package:

1. control.tar.xz: Contains scripts that dpkg uses to install the package
2. data.tar.xz: contains the package files
3. debian-binary: indicates the version of the package

It indicates the procedure to decompress the extracted by ar from the previous point. What information does it contain?

To decompress files we will use tar -xJf:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.036.png)

We will find the following directories and files:

-**control * *: This file contains metadata on the package, such as its name, version, description, dependencies and other important details.
-**confiles * *: This file lists the configuration files that are part of the package and that should be treated in a special way during updates to preserve the user's custom settings.
-**pre * *: This is a pre-installation script that runs before the package is installed in the system. It may contain necessary preconfiguration actions.
-**postinst * *: This is a post-installation script that runs after the package has been installed on the system. It may contain necessary post-configuration actions.
-**prerm * *: This is a pre-emotion script that runs before the package is disinstalled from the system. It may contain necessary pre-elimination actions.
-**dzm * *: This is a postremoval script that runs after the package has been disinstalled from the system. It may contain necessary post-elimination actions.
-**md5sums * *: This file contains the MD5 control sums of the files that are installed with the package. It is used to verify file integrity during installation.

The data.tar.xz file contains the files and directories that will be installed in the system when the package is installed.



### Work with repositories

## Exercise 1 Add to your source file.

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.037.png)

## Exercise 2 Configure the APT system so that the debian bullseye packages are given the highest priority and therefore the ones that are installed by default.

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.038.png)

## Exercise 3 Configure the APT system so that the bullseye-backports packages have a higher priority than those of unstable.

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.039.jpeg)

## Exercise 4 How do you add the possibility of downloading i386 architecture parcel into your system. What command did you use? List of non-native architectures. How would you proceed to discard the possibility of downloading parcel from i386 architecture?

To add:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.040.png)

To eliminate it:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.041.png)

## Exercise 5 If you wanted to download a package, how can you know all available versions of that package?

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.042.png)

Exercise 6 Indicates the procedure for downloading a package from the stable repository.

As we have it configured the packages per priority will be downloaded from the stable repository. But we can tell him:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.043.png)

## Exercise 7 Indicates the procedure to download a package from the buster-backports repository

You have to have the repository indicated in the sources.list then you can indicate it with the -t parameter.

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.044.png)

## Exercise 8 Indicates the procedure to download a package from the Sid repository

Just like the previous exercise we only indicated here Sid as we have indicated the repository in the sources.list:

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.045.png)

Exercise 9 Indicates the procedure to download an i386 architecture package.**We indicate the name of the package followed by: i386

![](/sistemas/comandos_linux/ejercicios_gestion_de_paqueteria/img/Aspose.Words.92111ab6-0138-481e-ad62-570c3a0b923e.046.jpeg)



### Work with directories

What do they do?

* * / var / lib / apt / lists /:**This directory contains lists of packages available in the configured repositories in my system. These lists are .list extension files that contain information about the available packages, their versions and the sources from which they can be downloaded. When I run apt update, I update these lists.

* * / var / lib / dpkg / available:**This file contains information about the installed packages and their versions. It is used by my dpkg package management system to keep a record of the packages I have installed and their states. It provides information on available packages and their dependencies.

* * / var / lib / dpkg / status:**This file also contains information about the packages installed in my system, but provides a more detailed view than / var / lib / dpkg / available. It contains information on the status of the packages, as if they are installed, uninstalled or if there are problems with their configuration.

* * / var / cache / apt / files /:**This directory stores the package files that I download before they are installed in my system. When I run commands like apt-get install or apt-get upgrade, the packages are downloaded first in this directory and then installed. Keeping a copy of the packages downloaded in this directory can be useful if you want to reinstall or uninstall a package without redownloading it from the repositories, which helps save time and bandwidth.


