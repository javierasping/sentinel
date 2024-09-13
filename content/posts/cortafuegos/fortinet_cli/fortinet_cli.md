---
title: "Fortinet CLI"
date: 2024-03-28T10:00:00+00:00
description: Fortinet CLI
tags: [FIREWALL,FORTINET]
hero: /images/cortafuegos/fortinet_cli.png
---



## Equivalencia de GUI a CLI 

Inicialmente, empecé la práctica utilizando la línea de comandos (CLI) sin embargo, encontré que resulta más cómodo realizarla desde la interfaz gráfica. Por eso, decidí establecer una equivalencia entre las diferentes acciones que he llevado a cabo durante la práctica y compararlas con su contraparte en la terminal.


> [!NOTE]  
> En este post hago un pequeño resumen de las equivalencias entre la GUI y la CLI de Fortinet que he utilizado en los 2 post de cortafuegos Fortinet.

### Configurar una interfaz

Como ya tenemos el cortafuegos configurado tenemos 2 opciones a la hora de ver la configuración de una determinada interfaz .

Ver la configuración de todas las interfaces :

```bash
show system interface
```

O especificar una en concreto : 

```bash
show system interface port1
```

Si observamos la configuración de las tres interfaces que he establecido durante la práctica, podemos notar que la sintaxis es muy sencilla. Prácticamente, incluso sin tener conocimientos previos sobre el tema, es fácil de comprender.

```bash
FTG # show system interface 
config system interface
    edit "port1"
        set vdom "root"
        set ip 192.168.122.77 255.255.255.0
        set allowaccess https http fgfm
        set type physical
        set alias "WAN"
        set lldp-reception enable
        set role wan
        set snmp-index 1
    next
    edit "port2"
        set vdom "root"
        set ip 192.168.100.1 255.255.255.0
        set allowaccess ping https ssh http fgfm
        set type physical
        set alias "LAN"
        set device-identification enable
        set lldp-transmission enable
        set monitor-bandwidth enable
        set role lan
        set snmp-index 2
    next
    edit "port3"
        set vdom "root"
        set ip 192.168.200.1 255.255.255.0
        set type physical
        set alias "DMZ"
        set device-identification enable
        set lldp-transmission enable
        set role lan
        set snmp-index 3
    next 

```

Como puedes ver en la interfaz puerto 1 que es la que corresponde a la WAN , anteriormente desactive el acceso para configurarlo desde esta interfaz  , pero por comodidad lo he dejado activado para usar el navegador de mi portátil . 

Una configuración que nos puede interesar es configurar una interfaz por DHCP , en mi caso lo haré en el puerto 4 :

```bash
# Accedemos al modo de configuración
FTG # config system interface
# Seleccionamos la interfaz 4
FTG (interface) # edit "port4"
# La ponemos en modo DHCP
FTG (port4) # set mode dhcp
# Salimos del modo de configuración
FTG (port4) # end
```

Ahora si listamos la configurar de la interfaz se habrá aplicado el cambio :

```bash 
FTG # show system interface port4
config system interface
    edit "port4"
        set vdom "root"
        set mode dhcp
        set type physical
        set snmp-index 4
    next
end
```

En este punto, observamos que los comandos que hemos utilizado coinciden con los que el sistema muestra al listar la configuración.

Ahora, lo que nos interesa es conocer la dirección IP de nuestra interfaz. Si deseamos listar todas las direcciones IP asignadas, simplemente no especificamos el nombre de la interfaz. En mi caso, me interesa saber la dirección IP de la interfaz del puerto 4:

```bash
FTG # get system interface physical port4
== [onboard]
	==[port4]
		mode: dhcp
		ip: 192.168.122.121 255.255.255.0
		ipv6: ::/0
		status: up
		speed: 1000Mbps (Duplex: full)
		FEC: none
		FEC_cap: none
```


Esto es lo básico que necesitamos para comenzar a configurar las interfaces . Te dejo un [enlace](https://docs.fortinet.com/document/fortigate/7.0.0/cli-reference/10620/config-system-interface) a la documentación oficial donde explica todos los detalles . 

### Políticas

Lo siguiente que hemos realizado en la practica es crear reglas desde la CLI , así que comenzare listando las reglas existentes , recuerda que en la versión de prueba tenemos un limite de 10 reglas simultaneas así que he eliminado algunas reglas durante la realización de la misma .

Para hacer la salida mas legible vamos a ver una regla "normal" y otra de DNAT para compararlas :

```bash
FTG # show firewall policy
config firewall policy
    edit 1
        set name "LAN_WAN_SSH"
        set uuid 57bba290-e881-51ee-3bbe-3ba5903773ed
        set srcintf "port2"
        set dstintf "port1"
        set action accept
        set srcaddr "all"
        set dstaddr "all"
        set schedule "always"
        set service "SSH"
        set nat enable
    next
    edit 5
        set name "WAN_LAN_DNAT_SSH"
        set uuid bdd84292-e884-51ee-a5d3-20eabb2fd433
        set srcintf "port1"
        set dstintf "port2"
        set action accept
        set srcaddr "all"
        set dstaddr "DNAT_SSH"
        set schedule "always"
        set service "SSH"
        set utm-status enable
        set ssl-ssh-profile "certificate-inspection"
        set ips-sensor "block_xmas"
        set nat enable
    next 
```

Vemos que la salida es bastante clara , si nos paramos a ver los parámetros comunes :

- name: Nombre que le queremos dar a la regla .
- UUID: Un identificador único que le asigna automáticamente el FW a cada regla .
- srcintf: Interfaz de origen (Por donde entra el trafico)
- dstintf: Interfaz de origen (Por donde entra el trafico)
- action: Que acción queremos que haga la regla accept | deny . 
- srcaddr:  Dirección de origen
- dstaddr: Dirección de destino
- schedule: Programación de la regla , por si es una regla temporal esta solo estará activa durante cierto tiempo .
- service: Nombre del servicio (Va asignado a un numero de puerto)
- nat: Si queremos que la regla haga SNAT .

Esto seria la sintaxis básica de cada regla como ves entre una regla "normal" y una de DNAT lo único que cambia es la dirección del trafico y la IP de destino que en este dispositivo es una IP virtual .

Si queremos borrar una regla , haremos lo siguiente :

```bash
# Accedemos al modo de configuracion de las politicas de seguridad
FTG # config firewall policy
# Borraremos la regla segun el id de la misma
FTG (policy) # delete 2
# Salimos de la configuracion
FTG (policy) # end
```

Para añadir una nueva regla, la sintaxis es similar a cuando listamos las reglas, pero necesitamos especificar un número de identificación (ID) al crearla. Es recomendable que sepas el número de la última regla que añadiste. Si no indicas un número, no se creará una nueva regla.

```bash
FTG#config firewall policy
FTG (policy) # edit 12
new entry '12' added

FTG (12) #         set name "LAN_WAN_DNS"
FTG (12) #         set srcintf "port2"
FTG (12) #         set dstintf "port1"
FTG (12) #         set action accept
FTG (12) #         set srcaddr "all"
FTG (12) #         set dstaddr "Google_DNS"
FTG (12) #         set schedule "always"
FTG (12) #         set service "DNS"
FTG (12) #         set nat enable
FTG (12) # next
FTG (policy) # end
```

Hay muchísimas mas opciones que ignoro que no ha sido necesarias utilizarlas en la practica , te dejo un [enlace](https://docs.fortinet.com/document/fortigate/7.0.0/cli-reference/323620/config-firewall-policy) a la documentación oficial donde detalla todas las distintas opciones .

### Servicios

Los servicios son unos objetos los cuales almacenan un numero o conjunto de puertos los cuales posteriormente utilizaras al crear reglas .Aunque estos dispositivos vienen con los servicios mas comunes de fabrica , muchas veces es necesario que creemos uno nuevo acorde a nuestras necesidades .

Al igual que con los comandos anteriores de listar , podemos listar todos los servicios o uno en concreto :

```bash
FTG # show firewall service custom
config firewall service custom
    edit "DNS"
        set category "Network Services"
        set tcp-portrange 53
        set udp-portrange 53
    next
   edit "HTTP"
        set category "Web Access"
        set tcp-portrange 80
    next
    edit "HTTPS"
        set category "Web Access"
        set tcp-portrange 443
    next

FTG # show firewall service custom SSH_2222 
config firewall service custom
    edit "SSH_2222"
        set category "Remote Access"
        set tcp-portrange 2222
    next
end

```

Para borrar un servicio , seguiremos los siguientes pasos :

```bash
# Accedemos a la configuración de los servicios
FTG # config firewall service custom
# Borramos el servicio indicando el nombre
FTG (custom) # delete SSH_2222
# Salimos del modo de configuración
FTG (custom) # end
```

Si queremos crearlo seguiremos los siguientes pasos :

```bash
# Accedemos a la configuración de los servicios
FTG # config firewall service custom
# Le asignamos un nombre
FTG (custom) # edit SSH_2222
# Opcionalmente lo añadimos a una categoria
FTG (SSH_2222) # set category "Remote Access"
# Indicamos los puertos que hace referencia al mismo
FTG (SSH_2222) # set tcp-portrange 2222
# Guardamos y salimos del modo de confuguración
FTG (SSH_2222) # next
FTG (custom) # end
```

Te dejo un [enlace](https://docs.fortinet.com/document/fortigate/7.0.0/ngfw-deployment/546227/creating-service-objects) a la documentación oficial referente a los servicios donde explica con detalle todas las opciones de los mismos .

### IPs Virtuales

Las IP Virtuales Estáticas (VIP) se utilizan para mapear direcciones IP externas a direcciones IP internas. Esto también se llama DNAT, donde el destino de un paquete se está enviando a una dirección diferente.

Las VIP estáticas se utilizan comúnmente para mapear direcciones IP públicas a recursos detrás del FortiGate que utilizan direcciones IP privadas. Una VIP estática uno a uno es cuando se mapea todo el rango de puertos. Una VIP de reenvío de puertos es cuando el mapeo se configura en un puerto específico o rango de puertos.

Si queremos listar las diferentes IPs virtuales que tenemos usaremos el siguiente comando , si solo queremos listar una en concreta indicaremos su nombre :

```bash
FTG # show firewall vip
config firewall vip
    edit "DNAT_POSTFIX"
        set uuid a343ec4a-e881-51ee-0ec1-ad73db3ff299
        set service "SMTP"
        set extip 192.168.100.1
        set mappedip "192.168.200.2"
        set extintf "port2"
    next
    edit "DNAT_SSH"
        set uuid a2b62344-e884-51ee-1a11-8946fda2bd91
        set service "SSH_2222"
        set extip 192.168.122.77
        set mappedip "192.168.100.2"
        set extintf "port1"
        set portforward enable
        set mappedport 22
    next

FTG # show firewall vip DNAT_HELA_WEB
config firewall vip
    edit "DNAT_HELA_WEB"
        set uuid a417a8f8-edf6-51ee-f601-43829c174966
        set service "HTTP"
        set extip 192.168.122.77
        set mappedip "192.168.200.2"
        set extintf "port1"
    next
end
```

En el caso de que queramos eliminar una de estas IPs virtuales , seguiremos los siguientes pasos :

```bash
# Accedemos al modo de configuración
FTG # config firewall vip
# Borramos la IP virtual indicando su nombre
FTG (vip) # delete DNAT_HELA_WEB
# Salimos del modo de configuración
FTG (vip) # end
```

Por otro lado para crear una de estas , como hemos realizado desde la GUI seguiremos los siguientes pasos :

```bash
# Accedemos al modo de configuración
FTG # config firewall vip
# Le asignamos el nombre que deseemos
FTG (vip) # edit DNAT_HELA_WEB
# Indicamos opcionalmente sobre el servicio que sera usado esta IP virtual
FTG (DNAT_HELA_WEB) # set service "HTTP"
# Indicamos la Ip externa
FTG (DNAT_HELA_WEB) # set extip 192.168.122.77
# Indicamos la Ip interna
FTG (DNAT_HELA_WEB) # set mappedip "192.168.200.2"
# Indicamos la interfaz externa
FTG (DNAT_HELA_WEB) # set extintf "port1"
# Guardamos y salimos
FTG (DNAT_HELA_WEB) # next
FTG (vip) # end
```

Las IP virtuales tienen mas parámetros de configuración que no he utilizado en la practica , te dejo un [enlace](https://docs.fortinet.com/document/fortigate/7.0.9/administration-guide/510402/static-virtual-ips) a la documentación oficial donde detalla toda la configuración que podemos acceder con las mismas .

### Rutas estáticas 

Nuestro dispositivo necesita conocer hacia donde enviar el trafico , para esto existen las rutas estáticas .

Para listar las rutas que tiene configurado nuestro cortafuegos , usaremos el siguiente comando :

```bash
FTG # show router static
config router static
    edit 1
        set gateway 192.168.122.1
        set device "port1"
    next
end
```

Al igual que hemos hecho anteriormente , si queremos eliminar esta ruta por defecto seguiremos los siguientes pasos :

```bash
FTG # config router static
FTG (static) # delete 1
FTG (static) # end
```

Si queremos añadir una ruta , puedes utilizar este ejemplo :

```bash
FTG # config router static
FTG (static) # edit 1
# El siguiete salto o puerta de enlace 
FTG (1) # set gateway 192.168.122.1
# La interfaz por donde saldra el trafico
FTG (1) # set device "port1"
FTG (1) # next
FTG (static) # end
```
