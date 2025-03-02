---
title: "Installation and Configuration of MariaDB in Debian 12"
date: 2024-09-01T10:00:00+00:00
Description: Install MariaDB in Debian
tags: [MariaDB,Debian]
hero: images/base_de_datos/instalar_mariadb/instalar_mariadb.png
---

## MariaDB installation and configuration in Debian 12

To install MariaDB in Debian 12, follow these steps:

1.**Update the repositories and install the MariaDB package**:

 First, update your system repositories and install MariaDB:

   ```bash
    javiercruces@jcruces:~$ sudo apt update
    javiercruces@jcruces:~$ sudo apt install mariadb-server
   ```

2.**Enable and start the MariaDB service**:

 Once installed, set MariaDB to automatically start the start and then start the service:

   ```bash
    javiercruces@jcruces:~$ sudo systemctl start mariadb
    javiercruces@jcruces:~$ sudo systemctl enable mariadb
   ```

3.**Configure MariaDB**:

 Run the security script to make initial settings:

   ```bash
    javiercruces@jcruces:~$ sudo mysql_secure_installation
   ```

 He then answers the following questions from the assistant:

   ```bash
# Enter the current password for root (press Enter if there is no password):
Enter current password for root (enter for none):  
`Enter`

# Set a new password for root? [Y/n]:
Set root password? [Y/n]:  
`Y`

# Remove anonymous users? [Y/n]:
Remove anonymous users? [Y/n]:  
`Y`

# Disallow root login remotely? [Y/n]:
Disallow root login remotely? [Y/n]:  
`Y`

# Remove the test database and access to it? [Y/n]:
Remove test database and access to it? [Y/n]:  
`Y`

# Reload privilege tables now? [Y/n]:
Reload privilege tables now? [Y/n]:  
`Y`

   ```

4. **Create a new user and assign permissions** :

 Connect to MariaDB as root:

   ```bash
    javiercruces@jcruces:~$ sudo mysql -u root
   ```

 Then create a new user and give him complete permissions on the database:

   ```sql
    CREATE USER 'javiercruces'@'localhost' IDENTIFIED BY 'tu_contraseña';
    GRANT ALL PRIVILEGES ON *.* TO 'javiercruces'@'localhost' WITH GRANT OPTION;
    FLUSH PRIVILEGES;
    EXIT;
   ```

5. **Connect using the new user**:

 You can now connect to MariaDB with the newly created user:

   ```bash
    javiercruces@jcruces:~$ mysql -u javiercruces -p
   ```

6. **Create a new database, insert data and consult the table**:

 Create a database, a table and add some data:

   ```sql
    CREATE DATABASE futbol;
    USE futbol;

    CREATE TABLE titulos_champions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        equipo VARCHAR(100) NOT NULL,
        campeonatos INT NOT NULL
    );

    INSERT INTO titulos_champions (equipo, campeonatos) VALUES
    ('Real Madrid', 15),
    ('Barcelona', 5);
   ```

 He then makes a consultation to verify the data:

   ```sql
   SELECT * FROM titulos_champions;
   ```

 The expected exit should be:

   ```sql
   +----+--------------+--------------+
   | id | equipo       | campeonatos  |
   +----+--------------+--------------+
   |  1 | Real Madrid |           15 |
   |  2 | Barcelona    |            5 |
   +----+--------------+--------------+
   ```
