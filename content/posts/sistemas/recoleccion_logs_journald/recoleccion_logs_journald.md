---
title: "Recolección centralizada de logs de sistema, mediante journald"
date: 2023-09-20T10:00:00+00:00
description: Recolección centralizada de logs de sistema, mediante journald
tags: [ASO,DEBIAN]
hero: images/sistemas/recoleccion_logs_journald/journal.jpg
---
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GVDYVWJLRH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GVDYVWJLRH');
</script>

## Paso 1 Instalar systemd-journal-remote 

En nuestro entorno, el primer paso consistirá en instalar el paquete systemd-journal-remote, que nos permitirá acceder a estas máquinas de forma remota. Para llevar a cabo la instalación en las máquinas de nuestro escenario, utilizaremos el gestor de paquetes apt en Odin, que ejecuta Debian 12. Asimismo, instalaremos el mismo paquete en Thor y Loki, que son contenedores alojados dentro de Odin. En cuanto a Hela, un sistema operativo Rocky, requerirá el uso de dnf para la instalación.

```bash
javiercruces@odin:~$ sudo apt install systemd-journal-remote -y
javiercruces@thor:~$ sudo apt install systemd-journal-remote -y
javiercruces@loki:~$ sudo apt install systemd-journal-remote -y
[javiercruces@hela ~]$ sudo dnf install systemd-journal-remote -y
```

En el servidor, habilita y activa los dos componentes de systemd necesarios para recibir mensajes de registro con el siguiente comando:

```bash
javiercruces@odin:~$ sudo systemctl enable --now systemd-journal-remote.socket
javiercruces@odin:~$ sudo systemctl enable systemd-journal-remote.service
```

En el cliente, habilita el componente que systemd utiliza para enviar los mensajes de registro al servidor:

```bash
[javiercruces@hela ~]$ sudo systemctl enable systemd-journal-upload.service
```

A continuación, en el servidor, abre los puertos 19532 y 80 en el firewall . Esto permitirá al servidor recibir los mensajes de registro del cliente. El puerto 80 es el puerto que certbot utilizará para generar el certificado TLS.  En nuestro caso no hay ningun cortafuegos asi que no sera necesario . 

## Paso 2: Generación de claves y certificados 

Dado que utilizaremos el servicio con cifrado para garantizar que nadie pueda acceder a nuestros registros, procederé a generar los certificados mediante OpenSSL.

Podemos generar los certificados manualmente, pero existe una herramienta llamada Easy RSA que automatiza este proceso. Yo generare en Odin todos los certificados de las maquinas y posteriormente los llevare a las maquinas correspondientes .

```bash
javiercruces@odin:~$ sudo apt install easy-rsa openssl -y 
```

Esta utilidad trae un fichero de ejemplo para que nos sea mas facil generar los certificados , dentro de este cambiaremos los siguientes valores :

```bash
javiercruces@odin:/usr/share/easy-rsa$ sudo cp vars.example vars
javiercruces@odin:/usr/share/easy-rsa$ sudo nano vars

set_var EASYRSA_REQ_COUNTRY     "ES"
set_var EASYRSA_REQ_PROVINCE    "Sevilla"
set_var EASYRSA_REQ_CITY        "Dos Hermanas"
set_var EASYRSA_REQ_ORG         "iesgn"
set_var EASYRSA_REQ_EMAIL       "contacto@javiercd.es"
set_var EASYRSA_REQ_OU          "Informatica"

```

Vamos a crear la estructura de directorios y archivos necesarios para comenzar a trabajar con EasyRSA :

```bash
javiercruces@odin:/usr/share/easy-rsa$ sudo ./easyrsa init-pki
* Notice:

  init-pki complete; you may now create a CA or requests.

  Your newly created PKI dir is:
  * /usr/share/easy-rsa/pki

```

Vamos a construir nuestra CA :

```bash
javiercruces@odin:/usr/share/easy-rsa$ sudo ./easyrsa build-ca nopass
-----
Common Name (eg: your user, host, or server name) [Easy-RSA CA]:odin.javiercd.gonzalonazareno.org

* Notice:

CA creation complete and you may now import and sign cert requests.
Your new CA certificate file for publishing is at:
/usr/share/easy-rsa/pki/ca.crt

```

Vamos a generar la clave privada de thor y generaremos a la vez una solicitud de firma del certificado :

```bash
javiercruces@odin:/usr/share/easy-rsa$ sudo ./easyrsa gen-req thor nopass
-----
Common Name (eg: your user, host, or server name) [thor]:thor.javiercd.gonzalonazareno.org
* Notice:

Keypair and certificate request completed. Your files are:
req: /usr/share/easy-rsa/pki/reqs/thor.req
key: /usr/share/easy-rsa/pki/private/thor.key

```

Vamos a generar la clave privada de loki y generaremos a la vez una solicitud de firma del certificado :

```bash
javiercruces@odin:/usr/share/easy-rsa$ sudo ./easyrsa gen-req loki nopass
-----
Common Name (eg: your user, host, or server name) [loki]:loki.javiercd.gonzalonazareno.org
* Notice:

Keypair and certificate request completed. Your files are:
req: /usr/share/easy-rsa/pki/reqs/loki.req
key: /usr/share/easy-rsa/pki/private/loki.key

```

Haremos lo mismo con odin :

```bash
javiercruces@odin:/usr/share/easy-rsa$ sudo ./easyrsa gen-req odin nopass
----
Common Name (eg: your user, host, or server name) [odin]:odin.javiercd.gonzalonazareno.org
* Notice:

Keypair and certificate request completed. Your files are:
req: /usr/share/easy-rsa/pki/reqs/odin.req
key: /usr/share/easy-rsa/pki/private/odin.key

```

Haremos lo mismo con hela :

```bash
javiercruces@odin:/usr/share/easy-rsa$ sudo ./easyrsa gen-req hela nopass
----
Common Name (eg: your user, host, or server name) [odin]:hela.javiercd.gonzalonazareno.org
* Notice:

Keypair and certificate request completed. Your files are:
req: /usr/share/easy-rsa/pki/reqs/hela.req
key: /usr/share/easy-rsa/pki/private/hela.key

```

Una vez generado las claves privadas y las peticiones de firma de los certificados toca firmarlos , para no hacerlo repetitivo mostrare la firma de odin , los demás se hacen de la misma forma : 

```bash
javiercruces@odin:/usr/share/easy-rsa$ sudo ./easyrsa sign-req server odin
* Notice:
Using Easy-RSA configuration from: /usr/share/easy-rsa/vars

* WARNING:

  Move your vars file to your PKI folder, where it is safe!

* Notice:
Using SSL: openssl OpenSSL 3.0.11 19 Sep 2023 (Library: OpenSSL 3.0.11 19 Sep 2023)


You are about to sign the following certificate.
Please check over the details shown below for accuracy. Note that this request
has not been cryptographically verified. Please be sure it came from a trusted
source or that you have verified the request checksum with the sender.

Request subject, to be signed as a server certificate for 825 days:

subject=
    commonName                = odin.javiercd.gonzalonazareno.org


Type the word 'yes' to continue, or any other input to abort.
  Confirm request details: yes

Using configuration from /usr/share/easy-rsa/pki/06312595/temp.f57dfbc5
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'odin.javiercd.gonzalonazareno.org'
Certificate is to be certified until May  5 18:34:45 2026 GMT (825 days)

Write out database with 1 new entries
Database updated

* Notice:
Certificate created at: /usr/share/easy-rsa/pki/issued/odin.crt

```

### Llevar los certificados a las maquinas correspondientes 

Ahora tendremos que hacerle llegar a las distintas maquinas haciendo uso de ssh .
Para cada uno de ellos nos llevaremos el certificado firmado que los hemos generado en /usr/share/easy-rsa/pki/issued/ y su clave privada que esta en  /usr/share/easy-rsa/pki/private/ .

Ademas para los clientes tendremos que hacerle llegar el certificado de la CA , que esta  en /usr/share/easy-rsa/pki/ca.crt

Una vez que tengamos los ficheros en las maquinas correspondientes , lo tendremos que almacenar con los siguientes permisos :

```bash
# Cliente hela
[javiercruces@hela ~]$ sudo ls -l /etc/letsencrypt/live/hela.javiercd.es/
total 60
-rw-r-----. 1 systemd-journal-upload systemd-journal-upload  1294 Jan 31 18:59 ca.crt
-rw-r-----. 1 systemd-journal-upload systemd-journal-upload  4841 Jan 25 11:17 hela.crt
-rw-r-----. 1 systemd-journal-upload systemd-journal-upload  1704 Jan 25 11:17 hela.key
# Servidor Odin 
javiercruces@odin:~$ sudo ls -l /etc/letsencrypt/live/javiercd.es/
total 20
-rw-r--r-- 1 root systemd-journal-remote 7840 Jan 31 18:39 combined.pem
-rw-r----- 1 root systemd-journal-remote 4841 Jan 31 18:35 odin.crt
-rw-r----- 1 root systemd-journal-remote 1704 Jan 31 18:35 odin.key
```

Como habrás notado en odin hay un fichero llamado combined.pem , para conseguir este tendrás que concatenar tu certificado con tu clave privada en un solo archivo 

```bash
javiercruces@odin:~$ sudo cat /etc/letsencrypt/live/javiercd.es/odin.crt /etc/letsencrypt/live/javiercd.es/odin.key > /etc/letsencrypt/live/javiercd.es/combined.pem
```

*Aunque he utilizado el directorio donde se guardan los certificados de Let's Encrypt , no he podido usarlo ya que no tenemos el control del dominio gonzalonazareno.org . Por eso los he generado manualmente anteriormente . Puntualizar que el directorio donde guardes estos no importa siempre y cuando tengan los permisos correctos .
## Paso 3 : Configurar el servidor

Ya solo nos quedaría indicar la configuración del servicio , solo tendrías que cambiar las rutas correspondientes a tus ficheros  :

```bash
javiercruces@odin:~$ sudo cat /etc/systemd/journal-remote.conf
[Remote]
Seal=false
SplitMode=host
ServerKeyFile=/etc/letsencrypt/live/javiercd.es/odin.key
ServerCertificateFile=/etc/letsencrypt/live/javiercd.es/odin.crt
TrustedCertificateFile=/etc/letsencrypt/live/javiercd.es/combined.pem
```

Una vez configurado reiniciamos el servicio y comprobamos que este levantado : 

```bash
javiercruces@odin:~$ sudo systemctl restart systemd-journal-remote.service 
javiercruces@odin:~$ sudo systemctl status systemd-journal-remote.service 
● systemd-journal-remote.service - Journal Remote Sink Service
     Loaded: loaded (/lib/systemd/system/systemd-journal-remote.service; indirect; preset: disabled)
     Active: active (running) since Wed 2024-01-31 18:46:25 UTC; 49min ago
TriggeredBy: ● systemd-journal-remote.socket
       Docs: man:systemd-journal-remote(8)
             man:journal-remote.conf(5)
   Main PID: 4623 (systemd-journal)
     Status: "Processing requests..."
      Tasks: 1 (limit: 2313)
     Memory: 7.9M
        CPU: 238ms
     CGroup: /system.slice/systemd-journal-remote.service
             └─4623 /lib/systemd/systemd-journal-remote --listen-https=-3 --output=/var/log/journal/remote/

```

## Paso 4 : Configurar el cliente

Añadiremos los ficheros correspondientes a la configuración , tu clave privada y tu certificado correspondiente así como el certificado de la CA con el que hayas generado estos :

```bash
[javiercruces@hela ~]$ sudo cat /etc/systemd/journal-upload.conf 
[Upload]
URL=https://odin.javiercd.gonzalonazareno.org/
ServerKeyFile=/etc/letsencrypt/live/hela.javiercd.es/odin.key
ServerCertificateFile=/etc/letsencrypt/live/hela.javiercd.es/odin.crt
TrustedCertificateFile=/etc/letsencrypt/live/hela.javiercd.es/ca.crt
```

Reiniciamos el servicio y comprobamos el estado del mismo : 

```bash
[javiercruces@hela ~]$ sudo systemctl restart systemd-journal-upload.service
[javiercruces@hela ~]$ sudo systemctl status systemd-journal-upload.service
● systemd-journal-upload.service - Journal Remote Upload Service
     Loaded: loaded (/usr/lib/systemd/system/systemd-journal-upload.service; enabled; preset: disabled)
     Active: active (running) since Wed 2024-01-31 19:38:53 UTC; 2s ago
       Docs: man:systemd-journal-upload(8)
   Main PID: 4628 (systemd-journal)
     Status: "Processing input..."
      Tasks: 1 (limit: 10840)
     Memory: 4.1M
        CPU: 53ms
     CGroup: /system.slice/systemd-journal-upload.service
             └─4628 /usr/lib/systemd/systemd-journal-upload --save-state

Jan 31 19:38:53 hela.javiercd.gonzalonazareno.org systemd[1]: Started Journal Remote Upload Service.
```

## Paso 5 : Comprobación de funcionamiento 

Una vez estén los dos servicios levantados , se nos guardaran en el servidor un fichero con los logs de nuestro cliente :

```bash
javiercruces@odin:~$ sudo ls -la /var/log/journal/remote/
total 8204
drwxr-xr-x  2 systemd-journal-remote systemd-journal-remote    4096 Jan 31 18:59 .
drwxr-sr-x+ 4 root                   systemd-journal           4096 Jan 24 13:01 ..
-rw-r-----  1 systemd-journal-remote systemd-journal-remote 8388608 Jan 31 19:38 remote-172.16.0.200.journal
```

Podemos ver los logs de los diferentes servicios , por ejemplo filtrare por httpd :

```bash
javiercruces@odin:~$ sudo journalctl -u httpd --file=/var/log/journal/remote/remote-172.16.0.200.journal
Jan 30 08:32:30 hela.javiercd.gonzalonazareno.org systemd[1]: Starting The Apache HTTP Server...
Jan 30 08:32:31 hela.javiercd.gonzalonazareno.org httpd[775]: [Tue Jan 30 08:32:31.395719 2024] [so:warn] [pid 775:tid 775] AH01574: module rewrite_module is already loaded, skipping
Jan 30 08:32:31 hela.javiercd.gonzalonazareno.org httpd[775]: Server configured, listening on: port 80
Jan 30 08:32:31 hela.javiercd.gonzalonazareno.org systemd[1]: Started The Apache HTTP Server.
```

