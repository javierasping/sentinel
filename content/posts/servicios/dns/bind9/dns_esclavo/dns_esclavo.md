
---
title: "Configuración de un servidor DNS esclavo con BIND9"
date: 2025-05-10T10:00:00+00:00
description: Aprende a configurar un servidor DNS esclavo con BIND9 en Debian, sincronizado con un servidor maestro.
tags: [DNS,BIND9,SMR,ASIR]
hero: images/servicios/dns/dns_esclavo.png
-------------------------------------------

En esta guía aprenderás a configurar un servidor DNS esclavo usando BIND9 en Debian. Este servidor se sincronizará con el servidor maestro (`dns1.javiercruces.org`) y permitirá distribuir la carga de resolución de nombres en tu red local. Además, se te guiará para verificar que la transferencia de zonas se realiza correctamente.

En este caso, el servidor esclavo se encuentra en la red 192.168.10.0/24, con la IP 192.168.10.200.

---

## 1. Preparación inicial del servidor esclavo

### Nombre de la máquina

Primero, asignamos el nombre correcto al host. Edita el archivo `/etc/hostname`:

```bash
dns2
```

Luego, configura el archivo `/etc/hosts` para asociar el nombre completo con la IP local:

```bash
127.0.1.1       dns2.javiercruces.org dns2
```

Verifica que el FQDN se resuelve correctamente con `hostname -f`. Deberías obtener la siguiente salida:

```bash
debian@dns2:~$ hostname -f
dns2.javiercruces.org
```

---

## 2. Instalación de BIND9

Instala el paquete de BIND9 como lo hicimos en el servidor maestro:

```bash
sudo apt update && sudo apt install bind9 bind9utils bind9-doc rsync -y
```

---

## 3. Configuración básica

### Editar `named.conf.options`

En el servidor esclavo, edita el archivo `/etc/bind/named.conf.options` para permitir consultas desde las redes internas:

```bash
options {
    directory "/var/cache/bind";

    allow-query { 127.0.0.1; 192.168.10.0/24; };
    recursion yes;

    dnssec-validation no;

    forwarders {
        1.1.1.1;
        8.8.8.8;
    };
};
```

---

## 4. Configuración de zonas esclavas

Edita el archivo `/etc/bind/named.conf.local` para definir las zonas esclavas. Estas deben coincidir con las configuradas en el servidor maestro:

```conf
zone "javiercruces.org" {
    type slave;
    masters { 192.168.10.1; };
    file "/var/cache/bind/slaves/db.javiercruces.org";
};

zone "10.168.192.in-addr.arpa" {
    type slave;
    masters { 192.168.10.1; };
    file "/var/cache/bind/slaves/db.192.168.10";
};
```

Crea el directorio para almacenar los archivos esclavos si aún no existe:

```bash
sudo mkdir -p /var/cache/bind/slaves
sudo chown bind:bind /var/cache/bind/slaves
```

---

## 5. Reiniciar el servicio

Una vez que todo esté configurado, reinicia el servicio de BIND9:

```bash
sudo systemctl restart bind9
```

Verifica que no haya errores en el registro de eventos:

```bash
sudo journalctl -xeu bind9
```

También puedes comprobar que las zonas se han transferido correctamente con:

```bash
ls -l /var/cache/bind/slaves
```

---

## 6. Actualización del servidor maestro

Para que el servidor esclavo reciba las zonas correctamente, es necesario autorizarlo desde el servidor maestro (`dns1`).

Edita el archivo `/etc/bind/named.conf.local` en el servidor maestro y añade la opción `allow-transfer` con la IP del esclavo:

```bash
zone "javiercruces.org" {
    type master;
    file "/var/cache/bind/db.javiercruces.org";
    allow-transfer { 192.168.10.200; };
};

zone "10.168.192.in-addr.arpa" {
    type master;
    file "/var/cache/bind/db.192.168.10";
    allow-transfer { 192.168.10.200; };
};
```

Además, actualizaremos los registros DNS para añadir el nuevo servidor. Debes agregar un registro A y un registro NS. Aquí tienes el archivo completo:

```bash
debian@dns1:~$ sudo cat /var/cache/bind/db.javiercruces.org
$TTL    86400
@       IN      SOA     dns1.javiercruces.org. root.javiercruces.org. (
                          1         ; Serial
                     604800         ; Refresh
                      86400         ; Retry
                    2419200         ; Expire
                      86400 )       ; Negative Cache TTL
;
@       IN      NS      dns1.javiercruces.org.
@       IN      NS      dns2.javiercruces.org.
@       IN      MX  10  correo.javiercruces.org.

$ORIGIN javiercruces.org.

dns1            IN      A       192.168.10.1
dns2            IN      A       192.168.10.200
correo          IN      A       192.168.10.2
thor            IN      A       192.168.10.3
hela            IN      A       192.168.10.4
www             IN      CNAME   thor
informatica     IN      CNAME   thor
ftp             IN      CNAME   hela
```

También debemos actualizar la zona inversa:

```bash
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
200     IN      PTR     dns2.javiercruces.org.
```

Después de guardar los cambios, recarga la configuración de BIND:

```bash
sudo rndc reload
```

O reinicia el servicio:

```bash
sudo systemctl restart bind9
```

Con esto, el servidor maestro está autorizado para enviar las zonas al esclavo cuando sea necesario.

---

## 7. Comprobaciones

Cada vez que reinicies el servicio en `dns1`, este enviará los cambios a `dns2`. Para comprobar que la transferencia de zonas está funcionando correctamente, ejecuta el siguiente comando en `dns2` para ver los logs en tiempo real:

```bash
debian@dns2:~$ sudo journalctl -u named -f
```

Luego, añade un registro en el servidor maestro:

```bash
sentinel           IN      A       192.168.10.25
```

Puedes forzar la transferencia de la zona con:

```bash
debian@dns2:~$ sudo rndc sync
```

Y los logs de la transferencia exitosa serán similares a los siguientes:

```bash
debian@dns2:~$ sudo journalctl -u named -f
May 10 23:11:08 dns2 named[936]: received control channel command 'sync'
May 10 23:11:08 dns2 named[936]: dumping all zones: success
```

Finalmente, realiza una consulta a ambos servidores para verificar que ambos devuelven el mismo resultado:

```bash
debian@cliente1:~$ dig @192.168.10.1 sentinel.javiercruces.org

; <<>> DiG 9.18.33-1~deb12u2-Debian <<>> @192.168.10.1 sentinel.javiercruces.org
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 31484
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 067375f875fc084c01000000681fdf328945678dcc84fea2 (good)
;; QUESTION SECTION:
;sentinel.javiercruces.org.	IN	A

;; ANSWER SECTION:
sentinel.javiercruces.org. 86400 IN	A	192.168.10.25

;; Query time: 0 msec
;; SERVER: 192.168.10.1#53(192.168.10.1) (UDP)
;; WHEN: Sat May 10 23:20:18 UTC 2025
;; MSG SIZE  rcvd: 98
```

```bash
debian@cliente1:~$ dig @192.168.10.200 sentinel.javiercruces.org

; <<>> DiG 9.18.33-1~deb12u2-Debian <<>> @192.168.10.200 sentinel.javiercruces.org
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 29032
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 4fd30029eb8c1f3d01000000681fdf34b473e093120ca15c (good)
;; QUESTION SECTION:
;sentinel.javiercruces.org.	IN	A

;; AUTHORITY SECTION:
javiercruces.org.	86400	IN	SOA	dns1.javiercruces.org. root.javiercruces.org. 1 604800 8
6400 2419200 86400

;; Query time: 0 msec
;; SERVER: 192.168.10.200#53(192.168.10.200) (UDP)
;; WHEN: Sat May 10 23:20:20 UTC 2025
;; MSG SIZE  rcvd: 128
```