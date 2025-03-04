---
title: "Implementación de un cortafuegos perimetral con Fortinet I"
date: 2024-03-28T10:00:00+00:00
description: Implementación de un cortafuegos perimetral con Fortinet I
tags: [FIREWALL,LINUX,DEBIAN,FORTINET]
hero: /images/cortafuegos/fortinet1.png
---




Antes de comenzar la practica , el escenario que ves en la practica es lo mas parecido que puedo montar a la practica original . He utilizado la versión 7.0.9-1 de FortiGate , ya que las versiones superiores traen algunas restricciones .  Puedes descargarte la imagen desde este [link](https://drive.google.com/drive/folders/1VGmeLN5inkWoNNUsIvq9ewGUzJLTLkiM) .

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320223139.png)


## Puesta en marcha del cortafuegos

Los dispositivos FortiGate vienen configurados de fabrica con la IP 192.168.1.99/24 , como estoy desde GNS3 no es necesario que me conecte a esta interfaz con un dispositivo y cambie la configuración . Ya que puedo hacerlo desde la consola .

Por defecto a través de ese puerto esta habilitada la administración por http , https , ssh y telnet .

En mi caso me conectare desde la consola , le cambiare el hostname y configurare el puerto 1 para que coja IP por DHCP . 

El usuario por defecto es admin y la contraseña en blanco . Cuando iniciemos sesión por primera vez nos obligara a cambiarla :

```bash
FortiGate-VM64-KVM login: admin
Password: 
You are forced to change your password. Please input a new password.
New Password: 
Confirm Password: 
Welcome!
```

Lo primero que haré sera cambiarle el hostname , como ves es similar a cisco ya que tenemos un modo de configuración  :

```bash
FortiGate-VM64-KVM # conf sys global
FortiGate-VM64-KVM (global) # set hostname FGT
FortiGate-VM64-KVM (global) # end
```

Ahora vamos a configurar el puerto 1 por DHCP para que así desde el cliente 2 lo pueda configurar sin tener que manualmente cambiar la IP del mismo . Ademas voy a configurar el acceso por http y https para poder configurarlo desde un navegador :

```bash
FGT # show system interface port1
config system interface
    edit "port1"
        set vdom "root"
        set mode dhcp
        set allowaccess ping https ssh http fgfm
        set type physical
        set snmp-index 1
    next
end
```

Ahora vamos a ver la IP que el DHCP le ha asignado con el siguiente comando :

```bash
FGT # get system interface 
== [ port1 ]
name: port1   mode: dhcp    ip: 192.168.122.77 255.255.255.0   status: up    netbios-forward: disable    type: physical   ring-rx: 0   ring-tx: 0   netflow-sampler: disable    sflow-sampler: disable    src-check: enable    explicit-web-proxy: disable    explicit-ftp-proxy: disable    proxy-captive-portal: disable    mtu-override: disable    wccp: disable    drop-overlapped-fragment: disable    drop-fragment: disable  
```

Ahora desde cualquier maquina que tenga acceso a la red 'externa' podremos conectarnos al FW :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320225245.png)

Cuando te inicies sesión veras un panel con información general sobre el estado dispositivo :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320225435.png)

### Configuración de la red LAN

Como has visto en la imagen de la topología, la red LAN está conectada al puerto 2. Por lo tanto, procederemos a configurarlo.

Vamos a dirigirnos a Network > Interfaces , selecciona el puerto 2 y pulsa en editar en la barra superior :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320230138.png)

Una vez dentro de la pantalla de configuración de la interfaz, puedes personalizar el puerto asignándole un alias. Además, para facilitar la gestión futura, le he asignado el rol LAN al puerto2, indicando que será utilizado para una red local. Posteriormente, he configurado la dirección IP del mismo, asignándole la 192.168.100.1/24. Además, he creado un objeto con esa IP, lo que facilitará la referencia a esta dirección IP en futuras configuraciones, eliminando la necesidad de recordar la IP .

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320230527.png)

Sigamos con la configuración de la interfaz. Desde la red LAN, donde estaremos la mayor parte del tiempo, permitiré el acceso vía HTTPS y SSH para configurar el FortiGate. También dejaré que respondan a los pings para asegurarme la conectividad con el mismo. Además, cada interfaz puede ser un servidor DHCP, así que le configurare uno para la LAN. Por último, activaré la opción para detectar dispositivos, así tendré control sobre quién se conecta a la red.

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320231025.png)

Una vez configurado el acceso administrativo desde la LAN , voy a quitar el acceso administrativo desde la interfaz puerto 1 ya que esta seria Internet (WAN).

Así que le cambiare el ROL a WAN y le quitare el acceso administrativo :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320231953.png)

Si recuerdas anteriormente marcamos en la interfaz LAN la casilla Device connection , si queremos ver los dispositivos conectados a esta red accedemos a Security Fabric > Asset Identify Center :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320232223.png)

Para apartados posteriores , como voy a realizar la practica de cortafuegos de nodo , es interesante crear un objeto con ese host . Así no sera necesario que recuerde su IP :

![](/cortafuegos/fortinet_uno/img/add_object_cliente1.png)

Aunque no he mencionado nada anteriormente , la política por defecto de estos dispositivos es DROP en todas las direcciones :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320232353.png)

Ahora vamos a crear una nueva política que permita el tráfico desde la LAN hacia Internet (WAN) en cualquier dirección. Esta política sería similar a las que tenemos en casa, donde podemos acceder a cualquier sitio web. Además, desde aquí podemos decir que haga SNAT, lo que nos permitirá navegar acceder a Internet. También podremos configurar hacia qué interfaz se realizará este SNAT.

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320232648.png)

Para acabar con la configuración inicial , crearemos la ruta por defecto para salir a Internet . Para ello nos iremos a Network > Static Routes  :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320233928.png)

Una vez aplicada esta política ya podremos comenzar a realizar la practica , ademas podemos acceder a Internet desde el cliente 1 :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320233557.png)

## Reglas del cortafuegos

Para comenzar desactivare la política anterior , la editare y al final de esta le quitare el tic que la activa :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320234721.png)

Quedando así inactiva :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320234740.png)


#### Los equipos de la red local deben poder tener conexión al exterior.

Para configurar el SNAT en dispositivos FortiGate , es un poco distinto ya que en cada regla que vayamos a permitir tendremos que marcar la casilla si queremos hacer NAT .

Ademas podemos especificar todas las opciones posibles que se nos ocurra , en mi caso dejare este apartado sin activar y lo iré haciendo en las reglas siguientes . La imagen que ves a continuación es para indicarte donde se activaría . Ademas podemos indicar porque interfaz queremos que salga el trafico . Esto es útil si tenemos dos o mas salidas de Internet para hacer un balanceador de carga .

Una vez aquí dentro de la configuración de la interfaz le decimos que la interfaz es de tipo NAT , ademas podemos indicarle que no haga PAT .

![](/cortafuegos/fortinet_uno/img/fw_1_a.png)

#### Permitimos hacer ping desde la LAN a la máquina cortafuegos.

En estos dispositivos no seria una regla como tal , si no que esta opción en concreto se indica desde la opción de acceso administrativo de la interfaz :

![](/cortafuegos/fortinet_uno/img/fw_2_a.png)

Una vez aplicado , si nos vamos al cliente 1 podremos hacerle ping al cortafuegos :

![](/cortafuegos/fortinet_uno/img/cliente1_ping_fw.png)

#### Permite realizar conexiones ssh desde los equipos de la LAN

Crearemos la regla que permite el trafico SSH , aqui en el origen podemos poner o el cliente1 (creamos el objeto en la preparación del escenario) o directamente poner all en el origen :


![](/cortafuegos/fortinet_uno/img/fw_3_a.png)

Aunque actualmente en mi esquema solo tenga un cliente , ceñiendome al enunciado si quiero que TODOS los cliente de la red LAN puedan hacer ssh en origen tengo que permitir todos :

![](/cortafuegos/fortinet_uno/img/fw_3_a_2.png)

Como te explique en el apartado a de la practica , en este tipos de dispositivo tenemos que indicarle si queremos que la regla sea de tipo NAT para que haga SNAT o no .

Una vez aplicada la regla podremos conectarnos por ssh desde el cliente1:

![](/cortafuegos/fortinet_uno/img/cliente1_ssh_atlas.png)

Vamos a asegurarnos de que la regla tiene hits :

![](/cortafuegos/fortinet_uno/img/fw_3_a_hits.png)


####  Permite la navegación en la red LAN

Para ello vamos a crear 2 reglas para la red LAN . Una que permita hacer consultas DNS y otra para permitir el trafico HTTPS y HTTP , ademas en ambas reglas sera necesario indicar que se haga NAT .

![](/cortafuegos/fortinet_uno/img/fw_4_a_dns.png)

![](/cortafuegos/fortinet_uno/img/fw_4_a_https.png)

Como te has fijado no he indicado el numero de puerto , si no que estos dispositivos tienen unos objetos llamados servicios en los cuales se almacenan los números de puerto de los mismos . Podemos crear los objetos que queramos y personalizar los existentes según nuestras necesidades .

Vamos a comprobar que podemos navegar en el cliente 1 :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322192235.png)

Ni que decir tiene que por supuesto que podemos hacer un dig , con la regla actual lo podemos hacer a cualquier servidor DNS :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322192456.png)

Vamos a comprobar que tenemos hits en las reglas :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322192318.png)


#### Instala un servidor de correos en la máquina de la LAN. Permite el acceso desde el exterior y desde el cortafuegos al servidor de correos. Para probarlo puedes ejecutar un telnet al puerto 25 tcp.

Como actualmente tenemos permitido la navegación solo por https es fundamental que los repositorios de la maquina estén configurados  podremos instalar paquetes en nuestro cliente , asi que vamos a instalar postfix :

```bash
sudo apt update && sudo apt install postfix -y
```

Ahora vamos a configurar la primera regla de DNAT que vamos a tener en el escenario . Para ello tendremos que crear una IP virtual y decirle cual es la IP externa (WAN) y la IP donde vamos a hacer el DNAT (LAN) .

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322202326.png)

Ahora vamos a añadir la regla en nuestra política , en el destino de la regla indicaremos la IP virtual que acabamos de crear y indicamos el servicio SMTP que tiene configurado el puerto 25 TCP :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322203152.png)

Y vamos a comprobar que desde un cliente externo , como es Cliente 2 podemos acceder a Cliente 1 :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322202558.png)

Vamos a comprobar que la regla que acabamos de crear tiene hits :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322203530.png)


#### Permite hacer conexiones ssh desde exterior a la LAN

Para realizar esto volveremos a hacer un DNAT , tendremos que volver a crear una nueva IP virtual ya que anteriormente especifique que esa IP solo se utilizaba para el protocolo SMTP . Así que voy a crear una nueva :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322204310.png)

Una vez creada la nueva IP virtual para el ssh , crearemos la regla de DNAT :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322204626.png)

Vamos a probar nuestra nueva regla desde el cliente 2 :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322204918.png)

Vamos a comprobar los hits de nuestra nueva regla :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322205046.png)

#### Modifica la regla anterior, para que al acceder desde el exterior por ssh tengamos que conectar al puerto 2222, aunque el servidor ssh este configurado para acceder por el puerto 22.

Para realizar esto tendremos que generar un nuevo servicio que este en el puerto 2222 :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322205327.png)

Ahora vamos a modificar nuestra IP virtual modificando el servicio por el nuevo que hemos creado con el puerto 2222 y haremos un port forwarding al puerto 22 :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322205425.png)


Una vez hecho esto podremos acceder por ssh utilizando el puerto 2222 y que nos redirija al 22 . No es necesario que modifiquemos las reglas , solo con esto ya podremos acceder :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322205611.png)

Vamos a comprobar los hits de las reglas , ademas en el apartado de Virtual IP también tenemos un contador de hits :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322205747.png)

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322205954.png)

#### Permite hacer consultas DNS desde la LAN sólo al servidor 8.8.8.8. Comprueba que no puedes hacer un dig @1.1.1.1.

Para esto vamos a modificar la regla que permite las consultas DNS y vamos a indicar que el destino solo sea 8.8.8.8 .

Primero necesitaremos crear un nuevo objeto con la IP del servidor DNS de Google :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322210309.png)

Ahora modificamos la regla y pondremos este objeto como destino :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322210344.png)

Vamos a comprobar la modificación de la regla , para que solo podamos hacer consultas dns a 8.8.8.8 :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322210423.png)

Podemos comprobar que los hits han subido :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322210549.png)



#### Permite que los equipos de la LAN puedan navegar por internet, excepto a la página www.realbetisbalompie.es

Estos cortafuegos de nueva generación traen una serie de servicios que nos filtran en el nivel de aplicación que nos permite detectar palabras clave para filtrar el contenido (drogas , pornografía , armas ... ) , en este cortafuegos el filtrar por palabras clave es un servicio de pago , hay que pagar una licencia . Ademas nos permite crear filtros para bloquear ciertas paginas web , que en este caso es gratuito. 

Lo primero sera crear nuestra política de filtro_web :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322211146.png)

Y añadimos en la misma un nuevo filtro por URL :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322211118.png)

Ahora nos dirigimos a la regla que nos permite el trafico https y en seguridad le añadimos el filtro web que acabamos de crear :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322211227.png)

A la izquierda accederé desde el navegador de mi maquina física y puedo acceder a la pagina del maligno , sin embargo si  accedo desde el cliente 1 el firewall no nos deja acceder :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322211357.png)

Si accedemos a FortiView Destinations podremos ver las paginas que ha bloqueado nuestro filtro :

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322211950.png)
