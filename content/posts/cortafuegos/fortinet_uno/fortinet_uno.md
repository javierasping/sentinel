---
title: "Implementación de un cortafuegos perimetral con Fortinet I"
date: 2024-03-28T10:00:00+00:00
description: Implementación de un cortafuegos perimetral con Fortinet I
tags: [FIREWALL,LINUX,DEBIAN,FORTINET]
hero: /images/cortafuegos/fortinet1.png
---




Antes de comenzar la práctica, el escenario que ves es lo más parecido que he podido montar a la práctica original. He utilizado la versión 7.0.9-1 de FortiGate, ya que las versiones superiores traen algunas restricciones. Puedes descargarte la imagen desde este [link](https://drive.google.com/drive/folders/1VGmeLN5inkWoNNUsIvq9ewGUzJLTLkiM).

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320223139.png)


## Puesta en marcha del cortafuegos

Los dispositivos FortiGate vienen configurados de fábrica con la IP 192.168.1.99/24. Como estoy utilizando GNS3, no es necesario que me conecte a esta interfaz con un dispositivo para cambiar la configuración, ya que puedo hacerlo directamente desde la consola.

Por defecto, a través de ese puerto está habilitada la administración por HTTP, HTTPS, SSH y Telnet.

En mi caso me conectaré desde la consola, le cambiaré el hostname y configuraré el puerto 1 para que obtenga una IP por DHCP. 

El usuario por defecto es `admin` y la contraseña está en blanco. Al iniciar sesión por primera vez, el sistema obligará a cambiarla:

```bash
FortiGate-VM64-KVM login: admin
Password: 
You are forced to change your password. Please input a new password.
New Password: 
Confirm Password: 
Welcome!
```

Lo primero que haré será cambiarle el hostname. Como ves, es similar a Cisco, ya que utilizamos un modo de configuración:

```bash
FortiGate-VM64-KVM # conf sys global
FortiGate-VM64-KVM (global) # set hostname FGT
FortiGate-VM64-KVM (global) # end
```

Ahora vamos a configurar el puerto 1 por DHCP para que el Cliente 2 pueda configurarlo sin tener que cambiar la IP manualmente. Además, voy a habilitar el acceso por HTTP y HTTPS para poder gestionarlo desde un navegador:

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

Ahora veremos la IP que el DHCP le ha asignado con el siguiente comando:

```bash
FGT # get system interface 
== [ port1 ]
name: port1   mode: dhcp    ip: 192.168.122.77 255.255.255.0   status: up    netbios-forward: disable    type: physical   ring-rx: 0   ring-tx: 0   netflow-sampler: disable    sflow-sampler: disable    src-check: enable    explicit-web-proxy: disable    explicit-ftp-proxy: disable    proxy-captive-portal: disable    mtu-override: disable    wccp: disable    drop-overlapped-fragment: disable    drop-fragment: disable  
```

Ahora, desde cualquier máquina que tenga acceso a la red 'externa', podremos conectarnos al firewall:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320225245.png)

Al iniciar sesión, verás un panel con información general sobre el estado del dispositivo:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320225435.png)

### Configuración de la red LAN

Como has visto en la imagen de la topología, la red LAN está conectada al puerto 2. Por lo tanto, procederemos a configurarlo.

Nos dirigiremos a Network > Interfaces, seleccionaremos el puerto 2 y pulsaremos en editar en la barra superior:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320230138.png)

Una vez dentro de la pantalla de configuración de la interfaz, puedes personalizar el puerto asignándole un alias. Además, para facilitar la gestión futura, le he asignado el rol LAN al puerto 2, indicando que será utilizado para una red local. Posteriormente, he configurado la dirección IP, asignándole la 192.168.100.1/24. Además, he creado un objeto con esa IP, lo que facilitará la referencia a esta dirección en futuras configuraciones, evitando la necesidad de recordar la IP.

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320230527.png)

Sigamos con la configuración de la interfaz. Desde la red LAN, donde estaremos la mayor parte del tiempo, permitiré el acceso vía HTTPS y SSH para configurar el FortiGate. También habilitaré la respuesta a pings para asegurar la conectividad. Además, cada interfaz puede actuar como servidor DHCP, por lo que configuraré uno para la LAN. Por último, activaré la opción para detectar dispositivos, así tendré control sobre quién se conecta a la red.

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320231025.png)

Una vez configurado el acceso administrativo desde la LAN, voy a quitar el acceso administrativo desde la interfaz del puerto 1, ya que esta representaría la salida a Internet (WAN).

Por lo tanto, le cambiaré el rol a WAN y eliminaré el acceso administrativo:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320231953.png)

Si recuerdas, anteriormente marcamos en la interfaz LAN la casilla "Device connection". Si queremos ver los dispositivos conectados a esta red, accedemos a Security Fabric > Asset Identify Center:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320232223.png)

Para apartados posteriores, ya que realizaré la práctica de cortafuegos de nodo, es conveniente crear un objeto con ese host para no tener que recordar su IP:

![](/cortafuegos/fortinet_uno/img/add_object_cliente1.png)

Aunque no lo he mencionado anteriormente, la política por defecto de estos dispositivos es DROP en todas las direcciones:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320232353.png)

Ahora vamos a crear una nueva política que permita el tráfico desde la LAN hacia Internet (WAN) en cualquier dirección. Esta política sería similar a la de un router doméstico, permitiendo acceder a cualquier sitio web. Además, configuraremos el SNAT para permitir la navegación por Internet y definiremos la interfaz de salida.

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320232648.png)

Para finalizar la configuración inicial, crearemos la ruta por defecto para salir a Internet. Para ello, nos dirigiremos a Network > Static Routes:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320233928.png)

Una vez aplicada esta política, ya podremos comenzar la práctica y acceder a Internet desde el Cliente 1:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320233557.png)

## Reglas del cortafuegos

Para comenzar, desactivaré la política anterior editándola y desmarcando la casilla de activación:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320234721.png)

Quedando así inactiva:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240320234740.png)


#### Los equipos de la red local deben poder tener conexión al exterior.

Para configurar el SNAT en dispositivos FortiGate, el proceso es distinto, ya que en cada regla que permitamos debemos marcar la casilla si deseamos aplicar NAT.

Además, podemos especificar diversas opciones. En mi caso, dejaré este apartado desactivado y lo iré configurando en las reglas siguientes. La imagen a continuación indica dónde se activaría. También podemos indicar la interfaz por la que debe salir el tráfico, lo cual es útil si tenemos varias salidas a Internet para realizar un balanceo de carga.

Una vez dentro de la configuración de la interfaz, definimos que la interfaz es de tipo NAT y podemos indicar que no realice PAT.

![](/cortafuegos/fortinet_uno/img/fw_1_a.png)

#### Permitimos hacer ping desde la LAN a la máquina cortafuegos.

En estos dispositivos, esto no se configura como una regla propiamente dicha, sino que se indica en las opciones de acceso administrativo de la interfaz:

![](/cortafuegos/fortinet_uno/img/fw_2_a.png)

Una vez aplicado, si nos situamos en el Cliente 1, podremos hacer ping al cortafuegos:

![](/cortafuegos/fortinet_uno/img/cliente1_ping_fw.png)

#### Permitir conexiones SSH desde los equipos de la LAN

Crearemos la regla que permite el tráfico SSH. En el origen, podemos especificar el Cliente 1 (creando el objeto en la preparación del escenario) o permitir todos los orígenes:


![](/cortafuegos/fortinet_uno/img/fw_3_a.png)

Aunque actualmente solo tenga un cliente en mi esquema, siguiendo el enunciado, para que TODOS los clientes de la red LAN puedan hacer SSH, debo permitir todos los orígenes:

![](/cortafuegos/fortinet_uno/img/fw_3_a_2.png)

Como expliqué en el primer apartado, en este tipo de dispositivos debemos indicar si queremos que la regla sea de tipo NAT para aplicar SNAT.

Una vez aplicada la regla, podremos conectarnos por SSH desde el Cliente 1:

![](/cortafuegos/fortinet_uno/img/cliente1_ssh_atlas.png)

Verifiquemos que la regla tiene hits:

![](/cortafuegos/fortinet_uno/img/fw_3_a_hits.png)


#### Permitir la navegación en la red LAN

Para ello, crearemos dos reglas para la red LAN: una que permita las consultas DNS y otra para el tráfico HTTPS y HTTP. En ambas reglas será necesario activar el NAT.

![](/cortafuegos/fortinet_uno/img/fw_4_a_dns.png)

![](/cortafuegos/fortinet_uno/img/fw_4_a_https.png)

Como habéis notado, no he indicado el número de puerto; esto es porque estos dispositivos utilizan objetos llamados "servicios", donde se almacenan los puertos. Podemos crear nuestros propios objetos o personalizar los existentes.

Comprobemos que podemos navegar desde el Cliente 1:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322192235.png)

No hace falta decir que también podemos realizar un `dig`. Con la regla actual, podemos consultar cualquier servidor DNS:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322192456.png)

Verifiquemos que las reglas tienen hits:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322192318.png)


#### Instalar un servidor de correo en la máquina de la LAN. Permitir el acceso desde el exterior y desde el cortafuegos al servidor de correos. Para probarlo, se puede ejecutar un telnet al puerto 25 TCP.

Como actualmente solo permitimos la navegación por HTTPS, es fundamental configurar los repositorios de la máquina para poder instalar paquetes en nuestro cliente; así que instalaremos Postfix:

```bash
sudo apt update && sudo apt install postfix -y
```

Ahora configuraremos la primera regla de DNAT del escenario. Para ello, crearemos una IP virtual, definiendo la IP externa (WAN) y la IP de destino donde haremos el DNAT (LAN).

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322202326.png)

Ahora añadiremos la regla en nuestra política. En el destino indicaremos la IP virtual recién creada y el servicio SMTP, que utiliza el puerto 25 TCP:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322203152.png)

Comprobaremos que desde un cliente externo (Cliente 2) podemos acceder al Cliente 1:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322202558.png)

Verifiquemos que la regla tiene hits:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322203530.png)


#### Permitir conexiones SSH desde el exterior a la LAN

Para lograr esto, crearemos otra IP virtual, ya que la anterior se especificó solo para el protocolo SMTP. Crearemos una nueva:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322204310.png)

Una vez creada la nueva IP virtual para SSH, definiremos la regla de DNAT:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322204626.png)

Probamos la nueva regla desde el Cliente 2:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322204918.png)

Verifiquemos los hits de la nueva regla:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322205046.png)

#### Modificar la regla anterior para que, al acceder desde el exterior por SSH, se conecte al puerto 2222, aunque el servidor SSH esté configurado en el puerto 22.

Para ello, generaremos un nuevo servicio configurado en el puerto 2222:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322205327.png)

Ahora modificaremos nuestra IP virtual, cambiando el servicio por el nuevo (puerto 2222) y configurando un redireccionamiento de puertos (port forwarding) al puerto 22:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322205425.png)


Una vez hecho esto, podremos acceder por SSH utilizando el puerto 2222, el cual nos redirigirá al 22. No es necesario modificar las reglas; con este cambio ya es posible acceder:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322205611.png)

Verifiquemos los hits de las reglas; además, en el apartado de Virtual IP también tenemos un contador de hits:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322205747.png)

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322205954.png)

#### Permitir que los equipos de la LAN puedan realizar consultas DNS solo al servidor 8.8.8.8. Comprobar que no es posible hacer un `dig @1.1.1.1`.

Para ello, modificaremos la regla que permite las consultas DNS, indicando que el único destino permitido es 8.8.8.8.

Primero, crearemos un nuevo objeto con la IP del servidor DNS de Google:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322210309.png)

Ahora modificamos la regla y asignamos este objeto como destino:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322210344.png)

Comprobemos que solo podemos realizar consultas DNS a 8.8.8.8:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322210423.png)

Verifiquemos que los hits han aumentado:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322210549.png)



#### Permitir que los equipos de la LAN naveguen por Internet, excepto a la página www.realbetisbalompie.es

Estos cortafuegos de nueva generación incluyen servicios que filtran en la capa de aplicación, permitiendo detectar palabras clave para filtrar el contenido (drogas, pornografía, armas, etc.). En este equipo, el filtrado por palabras clave es un servicio de pago; sin embargo, la creación de filtros para bloquear páginas web específicas es gratuita.

Primero, crearemos nuestra política de filtro web:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322211146.png)

Añadimos en la política un nuevo filtro por URL:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322211118.png)

Ahora nos dirigimos a la regla que permite el tráfico HTTPS y, en la sección de seguridad, añadimos el filtro web recién creado:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322211227.png)

Si accedemos desde el navegador de mi máquina física, puedo entrar en la página. Sin embargo, si accedo desde el Cliente 1, el firewall bloquea el acceso:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322211357.png)

Si accedemos a FortiView Destinations, podremos ver las páginas que ha bloqueado nuestro filtro:

![](/cortafuegos/fortinet_uno/img/Pastedimage20240322211950.png)
