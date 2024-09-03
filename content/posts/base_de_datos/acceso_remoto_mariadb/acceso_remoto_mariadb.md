---
title: "Configuración de acceso remoto en MariaDB"
date: 2024-09-01T10:00:00+00:00
description: Configuración de acceso remoto en MariaDB
tags: [MariaDB,Debian]
hero: images/base_de_datos/instalar_mariadb/instalar_mariadb.png

---


Para permitir el acceso remoto a tu servidor MariaDB, sigue estos pasos:

1. **Configura el archivo de configuración de MariaDB**

    Primero, edita el archivo de configuración de MariaDB para permitir conexiones desde direcciones IP específicas. Abre el archivo `/etc/mysql/mariadb.conf.d/50-server.cnf` con un editor de texto, por ejemplo, `nano`:

    ```bash
    sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
    ```

    Busca la línea que comienza con `bind-address` y cámbiala para que acepte conexiones desde cualquier dirección IP. Puedes hacer que acepte conexiones desde todas las IPs con:

    ```bash
    bind-address = 0.0.0.0
    ```

    Si prefieres permitir conexiones solo desde direcciones IP específicas, reemplaza `0.0.0.0` con las direcciones IP deseadas, separadas por comas. Guarda el archivo y cierra el editor (`Ctrl+X`, luego `Y` para confirmar los cambios y `Enter` para salir en `nano`).

2. **Reinicia el servicio de MariaDB**

    Para que los cambios surtan efecto, reinicia el servicio de MariaDB:

    ```bash
    sudo systemctl restart mariadb
    ```

3. **Instala el cliente de MariaDB en la máquina desde la que quieres conectarte**

    En la máquina cliente (desde la que deseas acceder al servidor MariaDB), instala el cliente de MariaDB. En Debian o Ubuntu, puedes hacerlo con:

    ```bash
    sudo apt update
    sudo apt install mariadb-client
    ```

4. **Conéctate al servidor MariaDB desde la máquina cliente**

    Finalmente, usa el cliente de MariaDB para conectarte al servidor. Reemplaza `usuario`, `servidor_ip` y `base_de_datos` con el nombre de usuario, la dirección IP del servidor y la base de datos a la que deseas acceder, respectivamente:

    ```bash
    mysql -u usuario -p -h servidor_ip
    ```

    Cuando se te solicite, ingresa la contraseña del usuario que has configurado en el servidor MariaDB.

Con estos pasos, habrás configurado el acceso remoto a tu servidor MariaDB y podrás conectarte desde cualquier máquina que tenga el cliente de MariaDB instalado.
