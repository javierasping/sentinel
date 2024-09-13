---
title: "Eliminación de systemd"
date: 2023-09-20T10:00:00+00:00
description: 
tags: [ASO,DEBIAN]
hero: images/sistemas/eliminar_systemd/eliminar_systemd.jpg
---


Systemd y System V (SysV) son dos sistemas de inicio utilizados en distribuciones de Linux para gestionar el arranque del sistema y los servicios. System V (SysV) es un sistema de inicio tradicional que utiliza scripts de shell almacenados en diferentes niveles de ejecución (runlevels) para iniciar y detener servicios de manera secuencial. Fue ampliamente utilizado en muchas distribuciones de Unix y Linux durante décadas. Por otro lado, systemd es un sistema de inicio más moderno y avanzado que reemplaza a SysV. Introducido para mejorar la velocidad y eficiencia del arranque del sistema, systemd utiliza un enfoque basado en unidades y depende de la paralelización para iniciar servicios simultáneamente. Además, incluye características adicionales como la gestión de servicios, sockets, temporizadores, y dependencias, lo que lo convierte en una opción más robusta y flexible en comparación con SysV.

## Migración de systemd a systemV

Modifica /etc/apt/sources.list para que apunte a los repositorios de Daedalus que es el equivalente de Debian 12 en Devuan.

```bash
root@ASOjaviercruces:~# nano /etc/apt/sources.list
```

Modifica sources.list para que se parezca al proporcionado. Comenta todas las demás líneas.

```bash
root@ASOjaviercruces:~# cat  /etc/apt/sources.list
deb http://deb.devuan.org/merged daedalus main
deb http://deb.devuan.org/merged daedalus-updates main
deb http://deb.devuan.org/merged daedalus-security main
deb http://deb.devuan.org/merged daedalus-backports main
```

Actualiza las listas de paquetes desde los repositorios de Daedalus , permitiendo los orígenes inseguros ya que esta firmado los repositorios .

```bash
root@ASOjaviercruces:~# apt-get update --allow-insecure-repositories
```

Instala el anillo de claves de Devuan para autenticar el repositorio y los paquetes.

```bash
root@ASOjaviercruces:~# apt-get install devuan-keyring --allow-unauthenticated
```

Actualiza las listas de paquetes nuevamente para autenticar los repositorios y paquetes.

```bash
root@ASOjaviercruces:~# apt-get update
```

Actualiza los paquetes instalados a las versiones más recientes. Ten en cuenta que esto no completa la migración a system-v.

```bash
root@ASOjaviercruces:~# apt-get upgrade (ten cuidado de NO usar dist-upgrade aquí)
```

Instalamos los paquetes eudev y sysvinit-core para gestionar eficientemente la detección y configuración de dispositivos a través de eudev, mientras que sysvinit-core se encarga del control del sistema de inicio y  procesos .

```bash
root@ASOjaviercruces:~# apt-get install eudev sysvinit-core
```

Es posible que el último comando cause roturas de paquetes, pero se resolverán como parte del proceso de migración.

```bash
root@ASOjaviercruces:~# apt-get -f install
```

Se requiere un reinicio para cambiar aplicar el cambio de systemd a systemV.

```bash
root@ASOjaviercruces:~# reboot
```

Actualizaremos la distribución para que los paquetes pasen de utilizar systemd a systemV.

```bash
root@ASOjaviercruces:~# apt-get dist-upgrade
```

Una vez completada la migración a Devuan, elimina los paquetes relacionados con systemd.

```bash
root@ASOjaviercruces:~# apt-get purge systemd libnss-systemd
```

Elimina cualquier paquete huérfano generado por el proceso de migración y cualquier archivo de caché no utilizable.

```bash
root@ASOjaviercruces:~# apt-get autoremove --purge
root@ASOjaviercruces:~# apt-get autoclean
```

### Comprobación y uso de systemV

Comprueba que el proceso 1 es init , esto significa que el sistema ha arrancado haciendo uso de systemV :

```bash
root@ASOjaviercruces:~# ps -s1
  PID TTY          TIME CMD
    1 ?        00:00:00 init
```


Me instalare un servicio que debería de depender de systemd pero como hemos cambiado a systemv , no lo usara ya que ahora usamos los repositorios de Devuan :

```bash
debian@ASOjaviercruces:~$ sudo apt install apache2 -y
```

Entonces para manejar el servicio lo haremos a partir del directorio /etc/init.d/ y buscando el "servicio" de cada demonio :

```bash
# Para iniciar el servicio
debian@ASOjaviercruces:~$ sudo /etc/init.d/apache2 start
Starting Apache httpd web server: apache2.

# Para parar el servicio
debian@ASOjaviercruces:~$ sudo /etc/init.d/apache2 stop
Stopping Apache httpd web server: apache2.

# Para reiniciar el servicio
debian@ASOjaviercruces:~$ sudo /etc/init.d/apache2 restart
Restarting Apache httpd web server: apache2AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 192.168.122.208. Set the 'ServerName' directive globally to suppress this message
.

# Para ver el estado
debian@ASOjaviercruces:~$ sudo /etc/init.d/apache2 status
apache2 is running.

```

