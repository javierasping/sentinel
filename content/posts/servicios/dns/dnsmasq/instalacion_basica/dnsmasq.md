---
title: "Configuración servidor DNS en Debian"
date: 2023-09-08T10:00:00+00:00
description: Configuración del servidor DNS en nuestro escenario básico bajo debian 10
tags: [Servicios,NAT,SMR,DHCP,SNAT,DNS,DNSMASQ]
hero: images/servicios/dns/dnsmasq.png
---

# Configuración servidor DNS en Debian    

## Dnsmasq

El paquete dnsmasq permite poner en marcha un servidor DNS de una forma muy sencilla. Simplemente instalando y arrancando el servicio dnsmasq, sin realizar ningún tipo de configuración adicional, nuestro PC se convertirá en un servidor caché DNS y además, resolverá los nombres que tengamos configurados en el archivo /etc/hosts de nuestro servidor. La resolución funcionará tanto en sentido directo como en sentido inverso, es decir, resolverá la IP dado un nombre de PC y el nombre del PC dada la IP.

### Instalación
Para instalarlo solo sera necesario introducir el siguiente comando :

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.048.png)

### Configuración

A continuación, editamos el fichero /etc/dnsmasq.conf y modificamos las siguientes líneas:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.049.png)

1.Descomentamos strict-order para que se realicen las peticiones DNS a los servidores que aparecen en el fichero /etc/resolv.conf en el orden en él aparecen.

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.050.png)

2.Incluimos las interfaces de red que deben aceptar peticiones DNS, descomentar la línea interface por ejemplo: interface=eth0

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.051.png)

Ahora crearemos nuestro archivo de configuración :

3.Creamos el fichero de configuración de nuestra zona :

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.052.png)

4.El dominio que hemos elegido es iesgn.org

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.053.png)

5.Suponemos que el nombre del servidor es miservidor.

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.054.png)

6.Vamos a suponer que tenemos un servidor ftp que se llame ftp.iesgn.org y que está en 192.168.1.201 (esto es ficticio) y que tenemos dos sitios webs: www.iesgn.org y departamentos.iesgn.org.

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.055.png)

7.Además queremos nombrar al cliente que tenía asignada una reserva: lisa.

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.056.png)

8.Reiniciamos el servicio

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.057.png)



### Modificación en el servidor DHCP

Configura los clientes e indica que su DNS es nuestro servidor. Si tienes un servidor DHCP modificarlo para que envíe el nuevo DNS a los clientes.

Editamos el fichero :

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.058.png)

Y reiniciamos el servicio :

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.059.png)

Ahora comprobaremos si el cliente nos ha cambiado el dns mirando el siguiente archivo :

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.060.png)

Se nos ha cambiado satisfactoriamente .

### Comandos para comprobar funcionamiento dns

Comprueba el funcionamiento usando el comando dig/nslookup desde los clientes preguntando por los distintos nombres. Comprueba que el servidor DNS hace de forwarder preguntando con  dig/nslookup la dirección ip de www.josedomingo.org.

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.061.png)

Para la pagina de Jose domingo la respuesta es no autorizada porque nuestro servidor no tiene la resolución en su fichero y tiene que utilizar un forwarder

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.062.png)

Como ves arriba yo he creado mi propia zona y a pesar de haber seguido los pasos de esta [pagina](https://www.josedomingo.org/pledin/2020/12/servidor-dns-dnsmasq/) de Jose domingo , no he conseguido que las respuestas estén autorizadas .

He creado el archivo dns.conf .

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.063.png)

Y he creado  mi zona :

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.064.png)

También he probado mas cosas sin embargo la única forma que he conseguido que me de respuesta autorizada es teniendo solo las resoluciones en el fichero host del servidor , sin crear mi zona .