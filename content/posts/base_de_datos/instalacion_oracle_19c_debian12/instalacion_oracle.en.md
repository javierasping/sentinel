---
title: "Oracle installation 19c under Debian 12"
date: 2024-09-01T10:00:00+00:00
Description: Oracle installation 19c under Debian 12
tags: [Oracle,Debian]
hero: images/base_de_datos/instalar_oracle/instalacion_oracle.png
---


Installing Oracle 19c on Debian 12 may seem complicated, but don't worry, I'm here to guide you in every step. In this post, I will explain to you in a simple way how to prepare your system and make the installation of Oracle 19c in Debian 12.

### Update the repositories

The first thing is to update the repositories of our virtual machine and in case we don't have any packages we update it:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.001.png)

### Install dependencies

The following will be to install the Oracle units in our system:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.002.png)

- * * libaio1 * *: Provides asynchronous access to E / S.
- * * Unixodbc * *: It is an ODBC controller for database connectivity.
- * * Bc * *: It's an arbitrary precision calculator.
- * * Ksh * *: It's the Korn shell for scripts.
- * * Gawk * *: It's an improved version of Awk for text and data processing.

### Add oracle user

We will create the dba group and create the oracle user:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.003.png)

We check that we can access the oracle user:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.004.png)

### Network configuration

We have to have a static ip set up:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.005.png)

We also have to have an entry in the hosts file of our private address:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.006.png)

### Download the Oracle website installation file

Once we have checked that we can install it in our system or virtual machine we will download it from your official website.

We will quickly realize that Oracle does not support Debian as we will find the package in .rpm format this means that it is prepared to be installed in network-based distributions hat.

For us to use this package we will have to transform it to .deb for it there is a tool called alien that will convert the package to us so that we can use it.

We install the tool:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.007.png)

Now using wget we'll download the Oracle meta-package:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.008.png)

Once downloaded we will use the alien utility to transform us, this will take approximately a step to lighten the process I have transformed it into my physical machine:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.009.png)

We passed it to our virtual machine using scp.

Now that we have our package transformed to .deb we install it using dpkg in our virtual machine

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.010.jpeg)

We'll start the installation, it'll take a while, so you have to be patient:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.011.jpeg)

Once finished in our user's bashrc we will add the oracle environment variables, ORACLE\ _ SID will tell us at the end of the installation, the others will depend on the directory we have put in previous steps:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.012.png)

## Error solution

## Error [FATAL] [DBT-50000] Unable to check available memory

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.013.png)

It returns an error, it tells us that you cannot check the available memory, this error can be solved by deactivating the check of configuration parameters for it in line 164 of the → / etc / init.d / oracledb\ _ ORCLCDB-19c file

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.014.jpeg)

We will change it to the following (complete line 164):

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

\ * I highlight the content you should add, you can also replace the entire line.

Another mistake you can give us is that you can't find netstat:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.015.png)

It is easily solved by installing net- tools.

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.016.png)

## # ORA-65096: unvalid username or common role

If you don't let us create a user:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.017.png)

With this modification let us create users

### First steps with Oracle

We will connect as administrators in the database:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/conn_oracle.png)

The first thing we have to do is create a user, give him permissions we need and check that we can connect with the:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.018.png)

And we give him the permits we consider to him:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.019.png)

Then we try to connect with it:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.020.png)

With this we will have completed the basic installation of Oracle 19c on Debian 12. It is recommended that if you are using the database you be installed by a client like SQLplus or SQLdeveloped.

## SQLplus installation

We download the basic SQLplus package for Linux, it's a .zip:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.021.jpeg)

We download the second SQLplus package:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.022.jpeg)

We create the /opt/oracle directory:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.023.png)

We uncompress the zip files in the directory we just created:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.024.png)

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.025.png)

We get into the directory and list the content:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.026.jpeg)

And then we export the SQLplus bookstore variable and run the changes:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.027.png)

If we want it to be maintained we will add it to the bashrc:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.028.png)


