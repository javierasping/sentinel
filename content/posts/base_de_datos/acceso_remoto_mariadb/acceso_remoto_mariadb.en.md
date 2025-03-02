---
title: "Remote access configuration in MariaDB"
date: 2024-09-01T10:00:00+00:00
Description: Remote access configuration in MariaDB
tags: [MariaDB,Debian]
hero: images/base_de_datos/instalar_mariadb/acceso_remoto_mariadb.png

---
To allow remote access to your MariaDB server, follow these steps:

1. **Configure the MariaDB configuration file**
 First, edit the MariaDB configuration file to allow connections from specific IP addresses. Open the file `/etc/mysql/mariadb.conf.d/50-server.cnf` with a text editor, for example, `nano`:

    ```bash
    sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
    ```

 Find the line that starts with `bind-address` and change it to accept connections from any IP address. You can have him accept connections from all the PIs with:

    ```bash
    bind-address = 0.0.0.0
    ```

 If you prefer to allow connections only from specific IP addresses, replace `0.0.0.0` with the desired IP addresses, separated by commas. Save the file and close the editor (`Ctrl + X`, then `Y` to confirm the changes and `Enter` to go out in `nano`).

2. **Reboot MariaDB service**
 For the changes to take effect, restart the MariaDB service:

    ```bash
    sudo systemctl restart mariadb
    ```

3. **Install MariaDB`s client on the machine from which you want to connect**
 In the client machine (from which you want to access the MariaDB server), install the MariaDB client. In Debian or Ubuntu, you can do it with:

    ```bash
    sudo apt update
    sudo apt install mariadb-client
    ```

4. **Connect to the MariaDB server from the client machine**
 Finally, use MariaDB's client to connect to the server. Replace `user`, `server _ ip` and `database` with the user name, the IP address of the server and the database you want to access, respectively:

    ```bash
    mysql -u usuario -p -h servidor_ip
    ```

 When requested, enter the user password you have configured on the MariaDB server.

With these steps, you will have set up the remote access to your MariaDB server and you will be able to connect from any machine that the MariaDB client has installed.