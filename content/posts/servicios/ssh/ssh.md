---
title: "SSH bajo debian 10"
date: 2023-09-08T10:00:00+00:00
description: Configuracion del servicio ssh 
tags: [Servicios,NAT,SMR,IPTABLES,SNAT,SSH,FORWARDING]
hero: images/servicios/ssh/portada-ssh.png
---
# SSH
## Gestión remota usando SSH
Lo primeros que deberemos de hacer sera instalarnos el paquete  en el servidor y el cliente :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.079.png)

Por seguridad se suele no permitir la conexión del root al servidor; para ello, se debe modificar el archivo /etc/ssh/sshd\_config, y se pone la siguiente opción:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.080.png)


Y reiniciamos el servicio para que se apliquen los cambios :

### Conectarse al servidor ssh

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.081.png)

Vamos a  instalarnos el cliente ssh, para ello:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.082.png)

Para acceder desde el cliente al servidor tecleamos:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.083.png)

Nos abríamos conectado remotamente


## Ejecución remota de aplicaciones gráficas
Mediante ssh existe la posibilidad de ejecutar aplicaciones gráficas en el servidor y manejarlas y visualizarlas en el cliente. El servidor ssh deberá tener activada la redirección del protocolo X, es decir, deberá tener el siguiente parámetro en el archivo de configuración /etc/ssh/sshd\_config:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.084.png)

En mi caso ya estaba habilitado , si no lo tuviésemos lo cambiamos y reiniciamos el servicio para que se apliquen los cambios . Ahora deberemos de conectarnos con el parámetro -X :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.085.png)

y posteriormente podemos ejecutar cualquier aplicación gráfica, por ejemplo, gedit:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.086.png)

Se nos abrirá el programa gráficamente :


![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.087.png)

Ahora vemos en el servidor que se ha creado :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.088.png)


### Transferir ficheros con ssh
Para copiar un fichero desde el cliente al servidor introducimos el siguiente comando :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.089.png)

Ahora vamos a comprobar si se ha copiado al servidor :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.090.png)


## Acceso remoto por cifrado asimetricó

### Configuracion del acceso por claves

Vamos a generar nuestras  claves desde nuestro cliente :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.091.png)


Ahora vamos a añadirla a nuestro servidor :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.092.png)

Una vez echo esto deshabilitamos el acceso con contraseña en el servidor editando el archivo /etc/ssh/sshd\_config :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.093.png)

A continuación solo debemos reiniciar el servicio y al volver a registrarnos,  ya estaremos utilizando clave publica :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.094.png)

` `Si nos intentamos registrar con usuario el cual no tenemos la clave publica nos dirá lo siguiente :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.095.png)

### Cambio de puerto

Ahora vamos a editar el fichero de configuración para indicar el puerto :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.096.png)

Y reiniciaremos el servicio :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.097.png)



Ahora si nos intentamos conectar como lo hemos hecho anterior mente , nos dara el siguiente error :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.098.png)

Para conectarnos deberemos de especificar el puerto por el cual nos conectamos con -p :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.099.png)

### Conectarnos con un cliente de acceso remoto usando túneles
Usaremos kitty  , cuando lo abramos en la primera pantalla introducimos la ip del servidor  y el puerto  que haya configurado en el servidor para el ssh en mi caso 2222

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.100.png)







Ahora añadimos el puerto por el cual nos conectaremos usando el túnel y después la ip seguida de dos puntos y el mismo puerto .

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.101.png)



Ahora introducimos nuestro usuario y contraseña y nos habremos conectado :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.102.png)

Si queremos hacer lo mismo pero usando una clave publica desde windows , pulsamos windows +r y escribimos lo siguiente :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.103.png)

Y generamos las claves publicas :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.104.png)

Ahora vamos a la ruta que lo hemos guardado copiamos la clave publica y la introducimos en el servidor , por comodidad la he copiado desde el cliente usando ssh.

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.105.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.106.png)

Una vez añadida guardamos el archivo :

Vamos a desactivar la autenticación por contraseña y reiniciamos el servicio

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.107.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.097.png)

Ahora desde el kitty deberemos de irnos al apartado ssh>auth , le damos a browse y seleccionamos nuestra clave privada , que deberá tener la extension .ppk . Yo la copie en otro   directorio por comodidad para las pruebas .

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.108.png)

Y nos conectamos :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.109.png)

Aquí hemos combinado conectarnos con kitty usando un túnel + otro puerto + clave publica .

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.110.png)


## VNCserver
Lo instalamos con el siguiente comando :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.111.png)

A continuación configuramos las credenciales de configuración para administradores y  usuarios de acceso con el siguiente comando :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.112.png)

Ahora vamos al cliente y introducimos la ip seguida del puerto por  dos puntos, si no lo sabemos lo podemos mirar con  :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.113.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.114.png)

Nos saldrá una advertencia al  no estar cifrada la comunicación , le damos a continuar y  introducimos la contraseña de acceso , que hayamos puesto anteriormente :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.115.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.116.png)

Como no tenemos entrono grafico en el servidor no nos mostrara imagen pero podemos ver que hemos establecido conexión tanto en windows como en Linux  :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.117.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.118.png)

## Gestión de páginas web mediante ssh

1.Una vez creado los dos sitio virtuales deseamos establecer una conexión segura a cada uno de nuestros sitios, para ello debemos establecer un túnel ssh de la misma manera que lo hemos establecido para establecer una conexión remota por vnc .

2.Crear un túnel desde el cliente ssh para que el acceso a la sección privada de la web de departamentos se establezca por el puerto 9999

3.Con ambos túneles establecidos comprobar que el acceso a la web iesgn.org se puede realizar sin problemas por el puerto 80

Solo he conseguido hacer a mi pagina por defecto , para eso hacemos un túnel con kitty por ejemplo:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.119.png)

Ahora añadimos los puertos origen y destino  del puerto :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.120.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.121.png)

Ahora nos registramos con nuestro usuario :

Una vez establecido el túnel introducimos en el navegador localhost:8888 :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.122.png)

Y así hemos establecido una conexión segura web .

Si cerramos el túnel perderemos la conexión :

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.123.png)
