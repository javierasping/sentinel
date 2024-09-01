---
title: "Instalación de PostgreSQL en Debian 12"
date: 2024-09-01T10:00:00+00:00
description: Instalación de PostgreSQL
tags: [PostgreSQL,Debian]
hero: images/base_de_datos/instalar_postgre/instalar_postgre.jpg

---
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GVDYVWJLRH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GVDYVWJLRH');
</script>


En este post, te guiaré a través del proceso de instalación de PostgreSQL en Debian 12, la creación de un usuario con permisos básicos, y cómo crear y consultar una base de datos.

## 1. Instalación de PostgreSQL

Para instalar PostgreSQL en Debian 12, sigue estos pasos:

1. **Actualiza los repositorios e instala PostgreSQL**:

    Primero, asegúrate de que tu sistema esté actualizado e instala PostgreSQL:

    ```bash
    sudo apt update
    sudo apt install postgresql 
    ```

2. **Verifica que el servicio esté en funcionamiento**:

    Después de la instalación, asegúrate de que el servicio de PostgreSQL esté en funcionamiento:

    ```bash
    sudo systemctl status postgresql
    ```

    Deberías ver un mensaje que indique que el servicio está activo (running).

## 2. Creación de un Usuario y Asignación de Permisos

1. **Accede al usuario `postgres`**:

    PostgreSQL crea un usuario llamado `postgres` durante la instalación. Accede a este usuario para realizar las tareas de configuración:

    ```bash
    sudo -u postgres psql
    ```

    Si quieres puedes cambiar la contraseña del usuario postgres de la base de datos con el siguiente comando:
    
    ```sql
    ALTER USER postgres WITH PASSWORD 'tu_nueva_contraseña';
    ```

2. **Crea un nuevo usuario**:

    Dentro del prompt de `postgres`,para crear un nuevo usuario utiliza el siguiente comando. 

    ```sql
    CREATE USER javiercruces WITH PASSWORD 'tu_contraseña';
    ```

3. **Crea una nueva base de datos**:

    A continuación, crea una base de datos que estará asociada a tu nuevo usuario.

    ```sql
     CREATE DATABASE mypgdatabase OWNER mypguser;
    ```

4. **Crear un usuario administrador**

    Si quieres crear un usuario con todos los privilegios en una base de datos introduce el siguiente comando:

    ```sql
    GRANT ALL PRIVILEGES ON DATABASE nombre_base_de_datos TO nombre_usuario;
    ```

    Sal de la consola con `\q`:

    ```sql
    \q
    ```

## 3. Prueba de Conexión

1. **Conéctate a PostgreSQL con el nuevo usuario**:

    Desde el usuario `postgres`, o directamente desde tu terminal, intenta conectarte a PostgreSQL utilizando el nuevo usuario:

    ```bash
    psql -U nombre_usuario -d nombre_base_de_datos
    ```

    Se te pedirá la contraseña del usuario. Si puedes acceder a la base de datos, la configuración fue exitosa.

## 4. Creación y Consulta de una Tabla

1. **Crea una nueva tabla**:

    Una vez dentro de la consola de PostgreSQL con el nuevo usuario, crea una nueva tabla. Por ejemplo, para una tabla de equipos de fútbol:

    ```sql
    CREATE TABLE equipos (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        titulos INT NOT NULL
    );
    ```

2. **Inserta datos en la tabla**:

    Inserta algunos datos de prueba en la tabla creada:

    ```sql
    INSERT INTO equipos (nombre, titulos) VALUES
    ('Real Madrid', 15),
    ('Barcelona', 5);
    ```

3. **Consulta los datos de la tabla**:

    Realiza una consulta para verificar que los datos se han insertado correctamente:

    ```sql
    SELECT * FROM equipos;
    ```

    La salida esperada debería ser:

    ```plaintext
     id |    nombre    | titulos
    ----+--------------+---------
      1 | Real Madrid |      15
      2 | Barcelona    |       5
    ```

Con estos pasos, has instalado PostgreSQL, creado un usuario y base de datos, y realizado pruebas básicas para asegurar que todo funciona correctamente. ¡Ahora tienes tu entorno de PostgreSQL listo para usar!
