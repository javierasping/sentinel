---
title: "Instalación y Configuración de MariaDB en Debian 12"
date: 2024-09-01T10:00:00+00:00
description: Instalar MariaDB en Debian
tags: [MariaDB,Debian]
hero: images/base_de_datos/instalar_mariadb/instalar_mariadb.png

---


## Instalación y Configuración de MariaDB en Debian 12

Para instalar MariaDB en Debian 12, sigue estos pasos:

1. **Actualiza los repositorios e instala el paquete de MariaDB**:

    Primero, actualiza los repositorios de tu sistema e instala MariaDB:

    ```bash
    javiercruces@jcruces:~$ sudo apt update
    javiercruces@jcruces:~$ sudo apt install mariadb-server
    ```

2. **Habilita y arranca el servicio de MariaDB**:

    Una vez instalada, configura MariaDB para que se inicie automáticamente al arranque y luego arranca el servicio:

    ```bash
    javiercruces@jcruces:~$ sudo systemctl start mariadb
    javiercruces@jcruces:~$ sudo systemctl enable mariadb
    ```

3. **Configura MariaDB**:

    Ejecuta el script de seguridad para realizar configuraciones iniciales:

    ```bash
    javiercruces@jcruces:~$ sudo mysql_secure_installation
    ```

    A continuación, responde a las siguientes preguntas del asistente:

    ```bash
    # Ingresa la contraseña actual para root (presiona Enter si no hay contraseña):
    Enter current password for root (enter for none):  
    `Enter`

    # ¿Establecer una nueva contraseña para root? [S/n]:
    Set root password? [Y/n]:  
    `Y`

    # ¿Eliminar usuarios anónimos? [S/n]:
    Remove anonymous users? [Y/n]:  
    `Y`

    # ¿Deshabilitar el inicio de sesión remoto para root? [S/n]:
    Disallow root login remotely? [Y/n]:  
    `Y`

    # ¿Eliminar la base de datos de prueba y el acceso a ella? [S/n]:
    Remove test database and access to it? [Y/n]:  
    `Y`

    # ¿Recargar las tablas de privilegios ahora? [S/n]:
    Reload privilege tables now? [Y/n]:  
    `Y`
    ```

4. **Crea un nuevo usuario y asigna permisos**:

    Conéctate a MariaDB como root:

    ```bash
    javiercruces@jcruces:~$ sudo mysql -u root
    ```

    Luego, crea un nuevo usuario y dale permisos completos sobre la base de datos:

    ```sql
    CREATE USER 'javiercruces'@'localhost' IDENTIFIED BY 'tu_contraseña';
    GRANT ALL PRIVILEGES ON *.* TO 'javiercruces'@'localhost' WITH GRANT OPTION;
    FLUSH PRIVILEGES;
    EXIT;
    ```

5. **Conéctate usando el nuevo usuario**:

    Ahora puedes conectarte a MariaDB con el usuario recién creado:

    ```bash
    javiercruces@jcruces:~$ mysql -u javiercruces -p
    ```

6. **Crea una nueva base de datos, inserta datos y consulta la tabla**:

    Crea una base de datos, una tabla y añade algunos datos:

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

    Luego, realiza una consulta para verificar los datos:

    ```sql
    SELECT * FROM titulos_champions;
    ```

    La salida esperada debería ser:

    ```plaintext
    +----+--------------+--------------+
    | id | equipo       | campeonatos  |
    +----+--------------+--------------+
    |  1 | Real Madrid |           15 |
    |  2 | Barcelona    |            5 |
    +----+--------------+--------------+
    ```
