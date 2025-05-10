---
title: "Instalación y configuración de BIND9 en Linux"
date: 2025-05-04T10:00:00+00:00
description: Aprende a instalar, configurar y verificar un servidor DNS BIND9 paso a paso en Debian
tags: [DNS,BIND9,SMR,ASIR]
hero: images/servicios/dns/bind9_install.jpg
------------------------------------------

En esta guía aprenderás a instalar y configurar un servidor DNS en Linux utilizando BIND9. Configurarás zonas de resolución directa e inversa para tu dominio, permitirás consultas desde otras máquinas en la red y realizarás pruebas utilizando herramientas como dig. Además, verás cómo configurar forwarders para resolver nombres externos eficientemente.

---

## 1. Preparación inicial

### Crear la máquina DNS

Crea una máquina y configúrala con el nombre `dns1.tunombre.org`. 

Para ello edita el fichero `/etc/hostname`:

```bash
javiercruces@dns1:~$ sudo cat /etc/hostname 
dns1
```

Luego añade al fichero `/etc/hosts` la resolución estática de este nombre y el FQDN del servidor DNS.

```bash
javiercruces@dns1:~$ sudo nano /etc/hosts
```

En mi caso llamare a la maquina `dns1.javiercruces.org`

```bash
127.0.1.1       dns1.javiercruces.org dns1
```

Verifica el FQDN con:

```bash
javiercruces@dns1:~$ hostname -f
```

Tendrá que devolverte algo similar a esto :

```bash
javiercruces@dns1:~$ hostname -f
dns1.javiercruces.org
```

---

## 2. Instalación de BIND9

Instalamos el servidor DNS BIND9:

```bash
debian@dns1:~$ sudo apt update && sudo apt install bind9 bind9utils bind9-doc -y
```

## 3. Configuración básica

### Evitar uso de IPv6 (opcional)

Editamos `/etc/default/named` para que BIND9 no use IPv6:

```bash
OPTIONS="-4 -f -u bind"
```

### Permitir consultas desde redes específicas

Editamos `/etc/bind/named.conf.options`:

```bash
options {
    directory "/var/cache/bind";

    allow-query { 127.0.0.1; 192.168.10.0/24; 192.168.20.0/24; };
    recursion yes;

    dnssec-validation no;

    forwarders {
        1.1.1.1;
        8.8.8.8;
    };
};
```

Reiniciamos BIND9:

```bash
sudo systemctl restart bind9
```

---

## 4. Configurar zona de resolución directa

Editamos `/etc/bind/named.conf.local`:

```bash
zone "javiercruces.org" {
    type master;
    file "/var/cache/bind/db.javiercruces.org";
};
```

Creamos el archivo de zona:

```bash
sudo cp /etc/bind/db.empty /var/cache/bind/db.javiercruces.org
sudo nano /var/cache/bind/db.javiercruces.org
```

Ejemplo de contenido:

```
$TTL    86400
@       IN      SOA     dns1.javiercruces.org. root.javiercruces.org. (
                          1         ; Serial
                     604800         ; Refresh
                      86400         ; Retry
                    2419200         ; Expire
                      86400 )       ; Negative Cache TTL
;
@       IN      NS      dns1.javiercruces.org.
@       IN      MX  10  correo.javiercruces.org.

$ORIGIN javiercruces.org.

dns1            IN      A       192.168.10.1
correo          IN      A       192.168.10.2
thor            IN      A       192.168.10.3
hela            IN      A       192.168.10.4
www             IN      CNAME   thor
informatica     IN      CNAME   thor
ftp             IN      CNAME   hela
```

---

## 5. Configurar zona de resolución inversa

Editamos `/etc/bind/named.conf.local`:

```bash
zone "10.168.192.in-addr.arpa" {
    type master;
    file "/var/cache/bind/db.192.168.10";
};
```

Aseguramos que la línea correspondiente en `/etc/bind/zones.rfc1918` esté comentada:

```bash
//zone "10.168.192.in-addr.arpa" { type master; file "/etc/bind/db.empty"; };
```

Creamos el archivo de zona:

```bash
sudo cp /etc/bind/db.empty /var/cache/bind/db.192.168.10
sudo nano /var/cache/bind/db.192.168.10
```

Contenido de ejemplo:

```
$TTL    86400
@       IN      SOA     dns1.javiercruces.org. root.javiercruces.org. (
                          1         ; Serial
                     604800         ; Refresh
                      86400         ; Retry
                    2419200         ; Expire
                      86400 )       ; Negative Cache TTL
;
@       IN      NS      dns1.javiercruces.org.

$ORIGIN 10.168.192.in-addr.arpa.

1       IN      PTR     dns1.javiercruces.org.
2       IN      PTR     correo.javiercruces.org.
3       IN      PTR     thor.javiercruces.org.
4       IN      PTR     hela.javiercruces.org.
```

---

## 6. Comprobaciones

Con la configuracion realizada en los otros apartados tendremos funcionado nuestro servidor DNS.

### Consultas básicas con `dig`

Si no indicamos el servidor DNS al usar la consulta con el parámetro `@` utilizara el configurado en el fichero `etc/resolv.conf` . Recuerda modificar la configuración de tu DHCP para que este le asigne la dirección de tu servidor DNS local a tus clientes .

```bash
# Consulta del registro A para hela.javiercruces.org
dig @192.168.10.1 hela.javiercruces.org

# Consulta inversa (PTR) de la IP 192.168.10.4 (correspondiente a hela)
dig @192.168.10.1 -x 192.168.10.4

# Consulta de registros MX para javiercruces.org
dig @192.168.10.1 javiercruces.org MX

# Consulta de registros NS para javiercruces.org
dig @192.168.10.1 javiercruces.org NS
```

Observa los tiempos y los registros utilizados para resolver nombres. La segunda consulta debería ser más rápida por el uso de caché.

En el caso de que quieras limpiar la cache de la resolución de tu servidor dns utiliza el siguiente comando :

```bash
sudo rndc flush
```


---
