---
title: "Interconnection of database servers"
date: 2024-09-01T10:00:00+00:00
description: "Interconnection of database servers"
tags: [Oracle, Mysql, PostgreSQL, Debian]
hero: "images/base_de_datos/interconexion_de_servidores/interconexion_de_servidores.png"
---

This post addresses how to configure and manage connections between different databases, both homogeneous and heterogeneous, to facilitate interoperability between various database systems. Throughout the article, different connection scenarios are explored, starting with configurations between databases of the same type, such as Oracle to Oracle or PostgreSQL to PostgreSQL, and then moving towards heterogeneous connections between different technologies, such as Oracle to MySQL, PostgreSQL to Oracle, and vice versa. It also covers the steps needed to configure links, create users, and modify key configuration files, allowing remote consultations.

## Homogeneous Connections

### Oracle to Oracle

We will interconnect two Oracle databases, which we will call **oracle1** and **oracle2** to differentiate them throughout this practice.

---

#### User Creation in Oracle1

First, we will create a user in Oracle1 who has permissions to connect to the database and to create database links:

![User creation in Oracle1](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.001.png)

To verify that the user has been created correctly, disconnect from the current user and reconnect with the new user:

![User verification](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.002.png)

---

#### User Creation in Oracle2

Repeat the steps made in Oracle1 to create a user in Oracle2 with appropriate permissions to remotely connect and create database links:

![User creation in Oracle2](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.003.png)

Verify the connection to the new user created:

![Connection verification in Oracle2](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.004.png)

---

#### Configuration of `listener.ora` and `tnsnames.ora` Files in ORACLE1

To ensure interconnection, we must configure the files `listener.ora` and `tnsnames.ora`. This will allow ORACLE1 to listen to the connections and recognize the location of ORACLE2.

##### Listener.ora Configuration

Edit the `listener.ora` file so that ORACLE1 can listen to connections on the network:

![Listener.ora configuration](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.006.jpeg)

> **Note:** Although it is recommended to allow connections only from specific IPs, in this test environment we have enabled general access. This file also defines the port used by Oracle.

##### Tnsnames.ora Configuration

We will now set the file `tnsnames.ora` so that ORACLE1 knows where ORACLE2 is:

![Configuration of tnsnames.ora](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.007.jpeg)

In this example, ORACLE2 is configured under IP `192.168.122.13` and listens on port `1521`. It is also important to know the name of the remote service. If you don't know it, you can run the following command on ORACLE2:

![Service name consultation](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.008.png)

---

#### Connectivity Verification

To confirm that ORACLE1 can communicate with ORACLE2, we will use the `tnsping` tool with the configured alias:

![Verification with tnsping](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.009.jpeg)

> **Remember!** If you did not set the `listener.ora` on the remote server (ORACLE2), this test will fail.

---

#### Configuration of `listener.ora` and `tnsnames.ora` Files in ORACLE2

We will now repeat the same steps in ORACLE2 so that it can communicate with ORACLE1.

##### Listener.ora Configuration

Edit the `listener.ora` file so that ORACLE2 listens to incoming connections:

![Listener.ora configuration](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.010.jpeg)

In this case, we have configured ORACLE2 to listen on any IP, using port `1521`, as in ORACLE1.

##### Tnsnames.ora Configuration

Edit the `tnsnames.ora` file to define an alias that allows ORACLE2 to communicate with ORACLE1:

![Configuration of tnsnames.ora](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.011.jpeg)

---

#### Connectivity Verification

Use the `tnsping` tool in ORACLE2 with the alias set for ORACLE1:

![Verification with tnsping](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.012.jpeg)

If the output is successful, it means that ORACLE2 can communicate with ORACLE1.

> **Remember!** If you did not set the `listener.ora` on the remote server (ORACLE1), this test will fail.

---

#### Creation of the Link from ORACLE1 to ORACLE2

At this stage, we will establish a link from ORACLE1 to ORACLE2. We will use a user with link creation privileges, such as **javiercruces1**, which was created earlier.

The link will receive a name, in this case, `ORACLE2_LINK`. We will specify that we will use the remote user credentials **javiercruces2** and the connection defined in the file `tnsnames.ora` for ORACLE2.

![Creation of the ORACLE1 link to ORACLE2](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.013.jpeg)

---

#### Link Verification

To verify, we will create the `dept` table in ORACLE2 and consult from ORACLE1:

![Consultation from ORACLE1](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.014.jpeg)

---

#### Creation of the Link from ORACLE2 to ORACLE1

We will now set the link in the opposite direction, from ORACLE2 to ORACLE1. We will follow the same procedure.

With the user **javiercruces2**, we will create a link called `ORACLE1_LINK`. This link will use the remote user credentials **javiercruces1** and the connection defined in the `tnsnames.ora` file for ORACLE1:

![Creation of the ORACLE2 link to ORACLE1](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.015.jpeg)

---

#### Link Verification

We will conduct a simple consultation using the newly created link:

![Consultation from ORACLE2](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.016.jpeg)

---

#### Simultaneous Consultations between ORACLE1 and ORACLE2

Now, we will check that it is possible to consult using both databases simultaneously from ORACLE1:

![Simultaneous consultation from ORACLE1](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.017.jpeg)

This same consultation can also be made from ORACLE2:

![Simultaneous consultation from ORACLE2](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.018.jpeg)

---

## PostgreSQL to PostgreSQL

To allow interconnection, it is essential to configure both machines to listen to requests. This is achieved by defining the IPs and ports in the configuration file located in `/etc/postgresql/15/main/postgresql.conf`:

![Configuration of listening in postgresql.conf](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.019.jpeg)

In addition, it is necessary to set up the networks from which connections will be accepted. This is done in the file `pg_hba.conf`:

![Pg_hba.conf configuration](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.020.png)

After making these changes, we will restart the PostgreSQL service to apply them:

![PostgreSQL service restart](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.021.png)

As in the previous section, we will use the **Scott** table schema, placing a table in each database for "remote" consultations.

---

### Interconnect PostgreSQL1 to PostgreSQL2

To interconnect the databases, we will use **dblink**, a module that allows for consultations and operations distributed between PostgreSQL databases. This is achieved by establishing direct connections between them.

#### User Creation and Database in PostgreSQL1

First, we create the users and database in PostgreSQL1:

![User creation and database](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.022.png)

---

#### Enable dblink Extension

We will activate the dblink extension in PostgreSQL1:

![Enable dblink](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.023.png)

---

#### Creation of the Connection to PostgreSQL2

We will use the dblink module to establish a connection to PostgreSQL2:

![Creation of connection to PostgreSQL2](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.024.png)

---

#### Conduct Consultations Using dblink

Once the connection is created, we can conduct remote consultations from PostgreSQL1:

![Remote consultation using dblink](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.025.png)

> **Note:** It is a bit tedious to define the fields for each remote consultation, which may make it difficult to use in more complex consultations.

---

### Interconnect PostgreSQL2 to PostgreSQL1

#### User Creation and Database in PostgreSQL2

We will create the users and database in PostgreSQL2 following a process similar to that in PostgreSQL1:

![User creation and database](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.026.png)

---

#### Enable dblink Extension and Create Connection to PostgreSQL1

We will activate the dblink extension and configure the connection to PostgreSQL1:

![Enable dblink and create connection to PostgreSQL1](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.027.png)

---

#### Conduct Consultations Towards PostgreSQL1

Now, we can consult from PostgreSQL2 to PostgreSQL1:

![Remote consultation from PostgreSQL2](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.028.jpeg)

---

#### Simultaneous Consultations between PostgreSQL1 and PostgreSQL2

To simplify remote consultations between the two databases, we can create views. This avoids the need to manually define the type of each field in the consultations:

![Simultaneous remote consultation using views](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.029.jpeg)

The same consultation can be made from PostgreSQL1 to PostgreSQL2:

![Simultaneous consultation from PostgreSQL1](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.030.jpeg)

---

## Heterogeneous Connections

### Oracle to MySQL

#### ODBC Driver Installation for MySQL

First, we download the ODBC driver for MySQL along with the necessary dependencies:

![Download of dependencies](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.031.png)

We access the official MySQL page to download the drivers and proceed to their installation:

![ODBC driver installation](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.032.jpeg)

---

#### Configuration of Heterogeneous Services in Oracle

We access the `hs/admin` directory within our Oracle installation:

![Access to the directory hs/admin](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.033.png)

We edit the `initMYSQL.ora` file with the following content to configure Heterogeneous Services:

![InitMYSQL.ora configuration](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.034.png)

---

#### ODBC Configuration for MySQL

We set ODBC for MySQL, making sure we include the right credentials to connect to the MySQL database:

![ODBC configuration](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.035.png)

---

#### Configuration of the Listener in Oracle

We update the listener configuration to include `localhost` and the Oracle listening port:

![Listener configuration](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.036.jpeg)

We restart the Oracle listener service to apply the changes:

![Reboot of the listener](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.037.png)

---

#### ODBC Driver Check

We check that the ODBC driver is working properly by connecting to the MySQL database. We can also use the `isql` driver to check the connection:

![ODBC driver test with MySQL](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.038.jpeg)

---

#### Creation of the Link between Oracle and MySQL

We created the link in Oracle to connect to the MySQL database:

![Link creation](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.039.png)

---

#### Conducting Consultations between Oracle and MySQL

We can make a simple consultation to the MySQL database:

![Simple consultation of MySQL](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.040.jpeg)

It is also possible to consult using both databases simultaneously. It is important to lock in double quotes the names of MySQL fields and tables to be interpreted correctly:

![Combined consultation between Oracle and MySQL](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.041.jpeg)

---

### MySQL to Oracle

![MySQL to Oracle](/base_de_datos/interconexion_de_servidores/img/when-i-think-i_ve-found-all-the-issues-in-our-infrastructure-but-then-find-something-that-shows-me-it-was-all-just-the-tip-of-the-iceberg.webp)

---

### Oracle to PostgreSQL

> **Note:** A machine with Oracle Linux 8 and Oracle Database 23 was used for this section.

#### Previous Configuration in Oracle

As an initial step, we created again a user and database in Oracle, assigning the appropriate permissions:


![UsercreationanddatabaseinOracle](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.042.jpeg)

### Driver Installation for PostgreSQL

We install the PostgreSQL driver using `dnf`. This command will also install the necessary libraries as dependencies:

![PostgreSQL driver installation](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.043.jpeg)

---

### File Configuration `odbcinst.ini`

The `/etc/odbcinst.ini` file is used in Linux systems to configure ODBC drivers. We edit this file to register the PostgreSQL driver:

![odbcinst.ini configuration](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.044.jpeg)

---

### File Configuration `odbc.ini`

The `/etc/odbc.ini` file contains specific settings for each connection to a database. Here are the details of the connection to the PostgreSQL database:

![odbc.ini configuration](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.045.jpeg)

---

### Configuration in Oracle to Use the Driver

We configure Oracle so it can use the ODBC driver. This includes updating the files needed to set up the connection:

![Oracle configuration to use the driver](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.046.jpeg)

---

### Configuration of the Listener in Oracle

We configure the listener file to enable communication with the PostgreSQL database:

![Listener configuration](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.047.jpeg)

---

### File Configuration `tnsnames.ora`

We add an entry to the `tnsnames.ora` file to define the connection to PostgreSQL:

![Configuration of tnsnames.ora](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.048.jpeg)

---

### Reboot of the Listener

We restart the listener service to apply the changes:

![Reboot of the listener](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.049.jpeg)

---

### Connection Test

We check the connectivity using `tnsping`:

![Connection test with tnsping](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.050.jpeg)

In addition, we test the connection using the ODBC driver from the terminal:

![Connection using the ODBC driver](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.051.jpeg)

---

### Creation of the Link in Oracle

We connect to Oracle and create the link to the PostgreSQL database. In the queries, the names of fields and tables should go between double quotes, and the values between single quotes:

![Link creation](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.052.png)

---

### Simultaneous Consultations between Oracle and PostgreSQL

We can conduct combined consultations between the two databases:

![Combined consultation between Oracle and PostgreSQL](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.053.png)

---

## PostgreSQL to Oracle

### Download and Install Necessary Packages

From the official Oracle page, we will download the following required packages:

![Oracle connection packages](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.054.png)

Since the system used is Debian, it is necessary to convert the RPM-format packages to DEB using `alien`. The process will take about 5 minutes, and the packages will be installed automatically when using the `-i` parameter:

![Conversion and installation with alien](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.055.png)

---

### Oracle Connection Test

Once the packages are installed, we check that it is possible to remotely connect to the Oracle database to ensure that the configuration is correct:

![Oracle connection test](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.056.jpeg)

---

### Download and Compile `oracle_fdw`

The next step is to install `oracle_fdw`, an extension for PostgreSQL that allows you to connect to Oracle. We download the latest version from the official repository:

- **Repository:** [oracle_fdw in GitHub](https://github.com/laurenz/oracle_fdw)

We clone the repository and compile the source code:

![Cloning and compilation of the repository](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.057.png)

Within the downloaded directory, we run `make` to compile:

![Make execution](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.058.png)

Finally, we install the extension with the `make install` command:

![Run make install](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.059.png)

---

### PostgreSQL Configuration

1. **Creation of Extension:**
   We connect to the PostgreSQL database where we want to create the link and set the extension `oracle_fdw`:

   ![Creation of the oracle_fdw extension](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.063.png)

2. **Creation of the Schema and Foreign Server:**
   We create a schema called `oracle` and set up a foreign server pointing to the Oracle database:

   ![External server configuration](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.063.png)

3. **User Mapping:**
   We create a mapping between the local PostgreSQL user (`javiercruces1`) and the remote Oracle user (`javiercruces3`). We also grant the necessary permissions on the schema and the foreign server:

   ![User mapping and permissions](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.063.png)

4. **Importation of the Schema:**
   With the local PostgreSQL user, we import the Oracle user's table schema to the local foreign server:

   ![Importation of the schema](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.064.png)

---

### Combined Consultations

Finally, we can conduct consultations involving data from both databases (PostgreSQL and Oracle). This allows us to work with information distributed in an integrated manner:

![Combined consultations](/base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.065.png)

---

[ref1]: /base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.060.jpeg
[ref2]: /base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.061.jpeg
[ref3]: /base_de_datos/interconexion_de_servidores/img/Aspose.Words.d88df54c-5805-4503-951a-502ec2dae267.062.jpeg