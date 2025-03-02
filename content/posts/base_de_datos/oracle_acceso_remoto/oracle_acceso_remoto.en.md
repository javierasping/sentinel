---
title: "Remote Access Configuration in Oracle"
date: 2024-09-01T10:00:00+00:00
description: "Remote Access Configuration in Oracle"
tags: [Oracle, Debian]
hero: "images/base_de_datos/instalar_oracle/acceso_remoto_oracle.png"
---

To configure remote access in Oracle, it is essential to correctly adjust the network files located in `$ORACLE_HOME/network/admin`. These files, such as `listener.ora` and `tnsnames.ora`, allow us to define how clients will connect to the database and which equipment will have access.

---

### Remote Access Configuration

The Oracle configuration with respect to the network is saved in the directory that we have defined as the Oracle home: `$ORACLE_HOME/network/admin`.

![Oracle network directory](/base_de_datos/oracle_acceso_remoto/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.029.png)

- **`listener.ora`**: This file is used to configure Oracle's listening service. It contains information about the connection points and protocols that the Oracle server will use to accept client connections.
- **`samples`**: Within this directory, there are examples of configuration files for various Oracle components. These sample files are useful as a reference when we need to create configuration files.
- **`shrept.lst`**: This file is part of the Oracle recovery process and is used to track the replication of real-time change records. It is essential when working with data replication.
- **`sqlnet.ora`**: This file sets Oracle's network options. Here, it defines how server names are resolved, sets security measures, and adjusts the security layer.
- **`tnsnames.ora`**: Here, the aliases that Oracle will use are defined.

---

### Configuring `listener.ora`

We will start by configuring the `listener.ora` file and indicate which equipment can connect to the database. In my case, I allow connections from all devices:

![listener.ora configuration](/base_de_datos/oracle_acceso_remoto/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.030.png)

---

### Starting the Oracle Listener Service

Once this is done, we will log in with the Oracle user and start the Oracle listener service to enable network connections:

![Starting the Oracle listener service](/base_de_datos/oracle_acceso_remoto/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.031.jpeg)

> **Note:** You must add the Oracle variables in the Oracle user's `.bashrc` file to start the service. If you haven't done this, you won't find the command.

---

### Configuring `tnsnames.ora` on the Client

On the client machine where we are going to make the connection, we will need to edit the `tnsnames.ora` file and add the address and port where our server is hosted:

![tnsnames.ora configuration on the client](/base_de_datos/oracle_acceso_remoto/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.032.jpeg)

---

### Connecting to the Oracle Database

Once this is done, the command to connect is as follows:

![Connection command](/base_de_datos/oracle_acceso_remoto/img/IMG_20231028_213222.jpg)

The syntax is:


The syntax is user/password@//IP:PORT /SID

We can consult tables, I have added the outline of the previous year's project:

![](/base_de_datos/oracle_acceso_remoto/img/Aspose.Words.55b57132-3c19-4447-864b-0b88f1173a10.034.png)