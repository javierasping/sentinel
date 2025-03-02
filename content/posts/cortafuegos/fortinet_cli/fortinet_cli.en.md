---
title: "Fortinet CLI"
date: 2024-03-28T10:00:00+00:00
description: Fortinet CLI
tags: [FIREWALL,FORTINET]
hero: /images/cortafuegos/fortinet_cli.png
---



Equivalence from GUI to CLI

Initially, I started the practice using the command line (CLI), however, I found it more comfortable to do it from the graphic interface. Therefore, I decided to establish an equivalence between the different actions I have carried out during practice and to compare them with their counterpart in the terminal.


> [NOTE]
> In this post I do a small summary of the equivalencies between the GUI and the CLI of Fortinet that I have used in the 2 Fortinet firewall posts.

### Configure an interface

As we already have the set-up firewall we have 2 options when viewing the configuration of a particular interface.

See the configuration of all interfaces:

```bash
show system interface
```

Or specify a particular one:

```bash
show system interface port1
```

If we look at the configuration of the three interfaces I have established during practice, we can note that the syntax is very simple. Virtually, even without prior knowledge of the subject, it is easy to understand.

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

As you can see in the port 1 interface that corresponds to the WAN, previously disable the access to configure it from this interface, but for comfort I have left it enabled to use my laptop's browser.

A configuration that may interest us is to set up a DHCP interface, in my case I will do it in port 4:

```bash
#Accedemos al modo de configuración
FTG # config system interface
#Seleccionamos la interfaz 4
FTG (interface) # edit "port4"
#La ponemos en modo DHCP
FTG (port4) # set mode dhcp
#Salimos del modo de configuración
FTG (port4) # end
```

Now if we list the interface configuration, the change will have been applied:

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

At this point, we note that the commands we have used match those that the system shows when listing the configuration.

Now, what we're interested in is knowing the IP address of our interface. If we want to list all the assigned IP addresses, we simply do not specify the interface name. In my case, I am interested to know the IP address of the port interface 4:

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


This is the basic thing we need to start setting up the interfaces. I leave you a [link] (https: / / docs.fortinet.com / document / fortigate / 7.0.0 / cli-reference / 10620 / config-system-interface) to the official documentation where it explains all the details.

## # Policies

The next thing we have done in practice is to create rules from the CLI, so I will start by listing the existing rules, remember that in the test version we have a limit of 10 simultaneous rules so I have removed some rules during the performance of it.

To make the output more legible we will see a "normal" rule and a DNAT rule to compare them:

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

We see that the output is quite clear, if we stop to see the common parameters:

- name: Name we want to give to the rule.
- UUID: A unique identifier that automatically assigns the FW to each rule.
- srcintf: Home interface (The way the traffic enters)
- dstantf: Home interface (From where the traffic enters)
- action: What action we want you to make the rule accept - 124; deny.
- srcaddr: address of origin
- dstaddr: Address of destination
- schedule: Regulation programming, in case it is a temporary rule this will only be active for a certain time.
- service: Service name (assigned to a port number)
- nat: If we want the rule to make SNAT.

This would be the basic syntax of each rule as you see between a "normal" rule and one of DNAT the only thing that changes is the traffic address and the target IP that on this device is a virtual IP.

If we want to delete a rule, we will do the following:

```bash
#Accedemos al modo de configuracion de las politicas de seguridad
FTG # config firewall policy
#Borraremos la regla segun el id de la misma
FTG (policy) # delete 2
#Salimos de la configuracion
FTG (policy) # end
```

To add a new rule, the syntax is similar to when we list the rules, but we need to specify an ID number when creating it. You should know the number of the last rule you added. If you don't indicate a number, a new rule will not be created.

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

There are many more options that I ignore that have not been necessary to use in practice, I leave you a [link] (https: / / docs.fortinet.com / document / fortigate / 7.0.0 / cli-reference / 323620 / config-firewall-policy) to the official documentation where details all the different options.

Services

Services are objects that store a number or set of ports that you will later use when creating rules. Although these devices come with the most common manufacturing services, it is often necessary that we create a new one according to our needs.

As with the previous listing commands, we can list all the services or one in particular:

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

To delete a service, we will follow the following steps:

```bash
#Accedemos a la configuración de los servicios
FTG # config firewall service custom
#Borramos el servicio indicando el nombre
FTG (custom) # delete SSH_2222
#Salimos del modo de configuración
FTG (custom) # end
```

If we want to create it, we will follow the following steps:

```bash
#Accedemos a la configuración de los servicios
FTG # config firewall service custom
#Le asignamos un nombre
FTG (custom) # edit SSH_2222
#Opcionalmente lo añadimos a una categoria
FTG (SSH_2222) # set category "Remote Access"
#Indicamos los puertos que hace referencia al mismo
FTG (SSH_2222) # set tcp-portrange 2222
#Guardamos y salimos del modo de confuguración
FTG (SSH_2222) # next
FTG (custom) # end
```

I leave you a [link] (https: / / docs.fortinet.com / document / fortigate / 7.0.0 / ngfw-deployment / 546227 / creating-service-objects) to the official documentation concerning the services where you explain in detail all the options of the services.

Virtual PIs

The VIPs are used to map external IP addresses to internal IP addresses. This is also called DNAT, where the destination of a package is being sent to a different address.

Static VIP are commonly used to map public IP addresses to resources behind the FortiGate that use private IP addresses. A static VIP one by one is when the entire range of ports is mapped. A port forwarding VIP is when the mapping is set up in a specific port or port range.

If we want to list the different virtual PIs we have we will use the following command, if we only want to list one in particular we will indicate its name:

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

In case we want to remove one of these virtual PIs, we will follow the following steps:

```bash
#Accedemos al modo de configuración
FTG # config firewall vip
#Borramos la IP virtual indicando su nombre
FTG (vip) # delete DNAT_HELA_WEB
#Salimos del modo de configuración
FTG (vip) # end
```

On the other hand to create one of these, as we have done from the GUI we will follow the following steps:

```bash
#Accedemos al modo de configuración
FTG # config firewall vip
#Le asignamos el nombre que deseemos
FTG (vip) # edit DNAT_HELA_WEB
#Indicamos opcionalmente sobre el servicio que sera usado esta IP virtual
FTG (DNAT_HELA_WEB) # set service "HTTP"
#Indicamos la Ip externa
FTG (DNAT_HELA_WEB) # set extip 192.168.122.77
#Indicamos la Ip interna
FTG (DNAT_HELA_WEB) # set mappedip "192.168.200.2"
#Indicamos la interfaz externa
FTG (DNAT_HELA_WEB) # set extintf "port1"
#Guardamos y salimos
FTG (DNAT_HELA_WEB) # next
FTG (vip) # end
```

Virtual IP have more configuration parameters that I have not used in practice, I leave you a [link] (https: / / docs.fortinet.com / document / fortigate / 7.0.9 / administration-guide / 510402 / static-virtual-ips) to the official documentation where you detail all the settings that we can access with them.

### Static routes

Our device needs to know where to send the traffic, for this there are static routes.

To list the routes that our firewall has set up, we will use the following command:

```bash
FTG # show router static
config router static
    edit 1
        set gateway 192.168.122.1
        set device "port1"
    next
end
```

As we have done before, if we want to remove this default route we will follow the following steps:

```bash
FTG # config router static
FTG (static) # delete 1
FTG (static) # end
```

If we want to add a route, you can use this example:

```bash
FTG # config router static
FTG (static) # edit 1
#El siguiete salto o puerta de enlace
FTG (1) # set gateway 192.168.122.1
#La interfaz por donde saldra el trafico
FTG (1) # set device "port1"
FTG (1) # next
FTG (static) # end
```
