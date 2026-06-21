---
title: "Oracle installation 19c under Debian 12"
date: 2024-09-01T10:00:00+00:00
Description: Oracle installation 19c under Debian 12
tags: [Oracle,Debian]
hero: images/base_de_datos/instalar_oracle/instalacion_oracle.png
---


Installing Oracle 19c on Debian 12 may seem complicated, but don't worry, I'm here to guide you through every step. In this post, I will explain in a simple way how to prepare your system and install Oracle 19c on Debian 12.

### Update the repositories

The first step is to update the repositories of our virtual machine and update any missing packages:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.001.png)

### Install dependencies

Next, we will install the Oracle dependencies on our system:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.002.png)

- * * libaio1 * *: Provides asynchronous access to I/O.
- * * Unixodbc * *: It is an ODBC driver for database connectivity.
- * * Bc * *: It is an arbitrary precision calculator.
- * * Ksh * *: It is the Korn shell for scripts.
- * * Gawk * *: It is an improved version of Awk for text and data processing.

### Add oracle user

We will create the dba group and the oracle user:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.003.png)

Check that you can access the oracle user:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.004.png)

### Network configuration

A static IP must be set up:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.005.png)

We also need an entry for our private address in the hosts file:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.006.png)

### Download the Oracle website installation file

Once we have verified that we can install it on our system or virtual machine, we will download it from the official website.

We will quickly realize that Oracle does not support Debian, as the package is in .rpm format. This means it is designed for Red Hat-based distributions.

To use this package, we must convert it to .deb. For this, there is a tool called 'alien' that will convert the package for us.

Install the tool:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.007.png)

Now, using wget, we will download the Oracle meta-package:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.008.png)

Once downloaded, we will use the alien utility to transform it. This will take some time, to speed up the process, I have transformed it on my physical machine:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.009.png)

We transferred it to our virtual machine using scp.

Now that the package has been converted to .deb, we install it using dpkg on our virtual machine:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.010.jpeg)

Start the installation, it will take a while, so please be patient:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.011.jpeg)

Once finished, we will add the Oracle environment variables to our user's .bashrc. The ORACLE_SID will be provided at the end of the installation, the others will depend on the directories used in the previous steps:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.012.png)

## Troubleshooting

## Error [FATAL] [DBT-50000] Unable to check available memory

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.013.png)

An error occurs stating that it cannot check the available memory. This error can be solved by disabling the configuration parameter check on line 164 of the /etc/init.d/oracledb_ORCLCDB-19c file:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.014.jpeg)

Change it to the following (complete line 164):

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

\* I have highlighted the content you should add, you can also replace the entire line.

Another error that may occur is that netstat cannot be found:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.015.png)

This is easily solved by installing net-tools.

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.016.png)

## ORA-65096: invalid username or common role

If you are unable to create a user:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.017.png)

This modification allows us to create users:

### First steps with Oracle

Connect as an administrator to the database:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/conn_oracle.png)

The first step is to create a user, grant the necessary permissions, and verify the connection:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.018.png)

Then, grant the necessary permissions:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.019.png)

Then, try to connect with the user:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.020.png)

This completes the basic installation of Oracle 19c on Debian 12. It is recommended to use a client such as SQL*Plus or SQL Developer to interact with the database.

## SQL*Plus Installation

Download the basic SQL*Plus package for Linux (it is a .zip file):

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.021.jpeg)

Download the second SQL*Plus package:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.022.jpeg)

Create the /opt/oracle directory:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.023.png)

Uncompress the zip files into the directory we just created:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.024.png)

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.025.png)

Enter the directory and list its contents:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.026.jpeg)

Then, export the SQL*Plus binary variable and apply the changes:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.027.png)

To make this permanent, add it to the .bashrc file:

![](/base_de_datos/instalacion_oracle_19c_debian12/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.028.png)
