---
title: "PostgreSQL installation in Debian 12"
date: 2024-09-01T10:00:00+00:00
Description: PostgreSQL installation
tags: [PostgreSQL,Debian]
hero: images/base_de_datos/instalar_postgre/instalacion_postgree.png

---



In this post, I will guide you through the process of installing PostgreSQL on Debian 12, creating a user with basic permissions, and how to create and query a database.

## 1. PostgreSQL Installation

To install PostgreSQL on Debian 12, follow these steps:

1. **Update the repositories and install PostgreSQL**:

 First, make sure your system is updated and install PostgreSQL:

    ```bash
    sudo apt update
    sudo apt install postgresql 
    ```

2. **Verify that the service is running**:

 After installation, make sure that the PostgreSQL service is running:

    ```bash
    sudo systemctl status postgresql
    ```

You should see a message indicating that the service is active (running).

## 2. User Creation and Permission Assignment

1. **Access the `postgres` user**:

 PostgreSQL creates a user called `postgres` during installation. Access this user to perform the configuration tasks:

    ```bash
    sudo -u postgres psql
    ```

If you wish, you can change the password for the `postgres` database user with the following command:
    
    ```sql
    ALTER USER postgres WITH PASSWORD 'tu_nueva_contraseña';
    ```

2. **Create a new user**:

 Within the `postgres` prompt, use the following command to create a new user:

    ```sql
    CREATE USER javiercruces WITH PASSWORD 'tu_contraseña';
    ```

3. **Create a new database**:

 Next, create a database associated with your new user:

    ```sql
     CREATE DATABASE mypgdatabase OWNER mypguser;
    ```

4. **Create an administrator user**:

 If you want to create a user with all privileges on a database, enter the following command:

    ```sql
    GRANT ALL PRIVILEGES ON DATABASE nombre_base_de_datos TO nombre_usuario;
    ```

Exit the console with `\\q`:

    ```sql
    \q
    ```

## 3. Connection Test

1. **Connect to PostgreSQL with the new user**:

 From the `postgres` user, or directly from your terminal, try to connect to PostgreSQL using the new user:

    ```bash
    psql -U nombre_usuario -d nombre_base_de_datos
    ```

You will be asked for the user's password. If you can access the database, the configuration was successful.

## 4. Table Creation and Querying

1. **Create a new table**:

 Once inside the PostgreSQL console with the new user, create a new table. For example, a table for football teams:

    ```sql
    CREATE TABLE equipos (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        titulos INT NOT NULL
    );
    ```

2. **Insert data into the table**:

 Insert some test data into the created table:

    ```sql
    INSERT INTO equipos (nombre, titulos) VALUES
    ('Real Madrid', 15),
    ('Barcelona', 5);
    ```

3. **Query the data in the table**:

 Perform a query to verify that the data has been correctly inserted:

    ```sql
    SELECT * FROM equipos;
    ```

The expected output should be:

    ```plaintext
     id |    nombre    | titulos
    ----+--------------+---------
      1 | Real Madrid |      15
      2 | Barcelona    |       5
    ```

With these steps, you have installed PostgreSQL, created a user and database, and performed basic tests to ensure that everything works properly. Now you have your PostgreSQL environment ready to use!
