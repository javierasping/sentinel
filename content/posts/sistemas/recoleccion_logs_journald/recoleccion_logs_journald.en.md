---
title: "Centralized collection of system log, using journald"
date: 2023-09-20T10:00:00+00:00
description: Centralized collection of system log, using journald
tags: [ASO,DEBIAN]
hero: images/sistemas/recoleccion_logs_journald/journal.jpg
---


### Step 1 Install system -journal-remote

In our environment, the first step will be to install the system-journal- remote package, which will allow us to access these machines remotely. To carry out the installation on our stage machines, we will use the apt package manager in Odin, which runs Debian 12. We will also install the same package in Thor and Loki, which are containers housed within Odin. As for Hela, a Rocky operating system, it will require the use of dnf for installation.

```bash
javiercruces@odin:~$ sudo apt install systemd-journal-remote -y
javiercruces@thor:~$ sudo apt install systemd-journal-remote -y
javiercruces@loki:~$ sudo apt install systemd-journal-remote -y
[javiercruces@hela ~]$ sudo dnf install systemd-journal-remote -y
```

On the server, enable and activate the two systems components needed to receive log messages with the following command:

```bash
javiercruces@odin:~$ sudo systemctl enable --now systemd-journal-remote.socket
javiercruces@odin:~$ sudo systemctl enable systemd-journal-remote.service
```

In the client, enable the component that you use to send the registration messages to the server:

```bash
[javiercruces@hela ~]$ sudo systemctl enable systemd-journal-upload.service
```

Then on the server, open ports 19532 and 80 on the firewall. This will allow the server to receive the customer's registration messages. The port 80 is the port that certbot will use to generate the TLS certificate. In our case there's no firewall so it won't be necessary.

Step 2: Generation of keys and certificates

Since we will use the encrypted service to ensure that no one can access our records, I will proceed to generate the certificates using OpenSSL.

We can generate the certificates manually, but there is a tool called Easy RSA that automates this process. I will generate in Odin all the certificates of the machines and then take them to the corresponding machines.

```bash
javiercruces@odin:~$ sudo apt install easy-rsa openssl -y 
```

This utility brings an example file to make it easier for us to generate the certificates, within this we will change the following values:

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

We will create the directory and file structure needed to start working with EasyRSA:

```bash
javiercruces@odin:/usr/share/easy-rsa$ sudo ./easyrsa init-pki
* Notice:

  init-pki complete; you may now create a CA or requests.

  Your newly created PKI dir is:
  * /usr/share/easy-rsa/pki

```

Let's build our CA:

```bash
javiercruces@odin:/usr/share/easy-rsa$ sudo ./easyrsa build-ca nopass
-----
Common Name (eg: your user, host, or server name) [Easy-RSA CA]:odin.javiercd.gonzalonazareno.org

* Notice:

CA creation complete and you may now import and sign cert requests.
Your new CA certificate file for publishing is at:
/usr/share/easy-rsa/pki/ca.crt

```

We will generate the private thor key and we will generate at the same time an application for signature of the certificate:

```bash
javiercruces@odin:/usr/share/easy-rsa$ sudo ./easyrsa gen-req thor nopass
-----
Common Name (eg: your user, host, or server name) [thor]:thor.javiercd.gonzalonazareno.org
* Notice:

Keypair and certificate request completed. Your files are:
req: /usr/share/easy-rsa/pki/reqs/thor.req
key: /usr/share/easy-rsa/pki/private/thor.key

```

We will generate the private loki key and we will generate at the same time an application for signature of the certificate:

```bash
javiercruces@odin:/usr/share/easy-rsa$ sudo ./easyrsa gen-req loki nopass
-----
Common Name (eg: your user, host, or server name) [loki]:loki.javiercd.gonzalonazareno.org
* Notice:

Keypair and certificate request completed. Your files are:
req: /usr/share/easy-rsa/pki/reqs/loki.req
key: /usr/share/easy-rsa/pki/private/loki.key

```

We'll do the same with din:

```bash
javiercruces@odin:/usr/share/easy-rsa$ sudo ./easyrsa gen-req odin nopass
----
Common Name (eg: your user, host, or server name) [odin]:odin.javiercd.gonzalonazareno.org
* Notice:

Keypair and certificate request completed. Your files are:
req: /usr/share/easy-rsa/pki/reqs/odin.req
key: /usr/share/easy-rsa/pki/private/odin.key

```

We'll do the same with hela:

```bash
javiercruces@odin:/usr/share/easy-rsa$ sudo ./easyrsa gen-req hela nopass
----
Common Name (eg: your user, host, or server name) [odin]:hela.javiercd.gonzalonazareno.org
* Notice:

Keypair and certificate request completed. Your files are:
req: /usr/share/easy-rsa/pki/reqs/hela.req
key: /usr/share/easy-rsa/pki/private/hela.key

```

Once the private keys and the requests for signature of the certificates are generated, it is necessary to sign them, in order not to repetitive it will show the signature of odin, the others are done in the same way:

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

### Take the certificates to the corresponding machines

Now we'll have to get him to the different machines using ssh.
For each of them we will take the signed certificate that we have generated in / usr / share / easy-rsa / pki / issued / and its private key that is in / usr / share / easy-rsa / pki / private /.

In addition for customers we will have to send the CA certificate, which is in / usr / share / easy-rsa / pki / ca.crt

Once we have the files in the corresponding machines, we will have to store it with the following permissions:

```bash
#Cliente hela
[javiercruces@hela ~]$ sudo ls -l /etc/letsencrypt/live/hela.javiercd.es/
total 60
-rw-r-----. 1 systemd-journal-upload systemd-journal-upload  1294 Jan 31 18:59 ca.crt
-rw-r-----. 1 systemd-journal-upload systemd-journal-upload  4841 Jan 25 11:17 hela.crt
-rw-r-----. 1 systemd-journal-upload systemd-journal-upload  1704 Jan 25 11:17 hela.key
#Servidor Odin
javiercruces@odin:~$ sudo ls -l /etc/letsencrypt/live/javiercd.es/
total 20
-rw-r--r-- 1 root systemd-journal-remote 7840 Jan 31 18:39 combined.pem
-rw-r----- 1 root systemd-journal-remote 4841 Jan 31 18:35 odin.crt
-rw-r----- 1 root systemd-journal-remote 1704 Jan 31 18:35 odin.key
```

As you will have noticed in din there is a file called combined.pem, to get this you will have to concatenate your certificate with your private key in a single file

```bash
javiercruces@odin:~$ sudo cat /etc/letsencrypt/live/javiercd.es/odin.crt /etc/letsencrypt/live/javiercd.es/odin.key > /etc/letsencrypt/live/javiercd.es/combined.pem
```

* Although I have used the directory where Let's Encrypt certificates are kept, I have not been able to use it as we do not have control of the gonzalonazareno.org domain. That's why I've generated them manually before. Puntualize that the directory where you keep these does not matter as long as you have the right permissions.
Step 3: Configure the server

We would only have to indicate the service configuration, you would only have to change the routes corresponding to your files:

```bash
javiercruces@odin:~$ sudo cat /etc/systemd/journal-remote.conf
[Remote]
Seal=false
SplitMode=host
ServerKeyFile=/etc/letsencrypt/live/javiercd.es/odin.key
ServerCertificateFile=/etc/letsencrypt/live/javiercd.es/odin.crt
TrustedCertificateFile=/etc/letsencrypt/live/javiercd.es/combined.pem
```

Once configured, we restart the service and check that it is up:

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

Step 4: Configure the client

We will add the files corresponding to the configuration, your private key and your corresponding certificate as well as the CA certificate with which you have generated these:

```bash
[javiercruces@hela ~]$ sudo cat /etc/systemd/journal-upload.conf 
[Upload]
URL=https://odin.javiercd.gonzalonazareno.org/
ServerKeyFile=/etc/letsencrypt/live/hela.javiercd.es/odin.key
ServerCertificateFile=/etc/letsencrypt/live/hela.javiercd.es/odin.crt
TrustedCertificateFile=/etc/letsencrypt/live/hela.javiercd.es/ca.crt
```

We restart the service and check the state of the service:

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

Step 5: Operating check

Once the two services are up, we will be saved on the server a file with our client's login:

```bash
javiercruces@odin:~$ sudo ls -la /var/log/journal/remote/
total 8204
drwxr-xr-x  2 systemd-journal-remote systemd-journal-remote    4096 Jan 31 18:59 .
drwxr-sr-x+ 4 root                   systemd-journal           4096 Jan 24 13:01 ..
-rw-r-----  1 systemd-journal-remote systemd-journal-remote 8388608 Jan 31 19:38 remote-172.16.0.200.journal
```

We can see the logs of the different services, for example will filter by httpd:

```bash
javiercruces@odin:~$ sudo journalctl -u httpd --file=/var/log/journal/remote/remote-172.16.0.200.journal
Jan 30 08:32:30 hela.javiercd.gonzalonazareno.org systemd[1]: Starting The Apache HTTP Server...
Jan 30 08:32:31 hela.javiercd.gonzalonazareno.org httpd[775]: [Tue Jan 30 08:32:31.395719 2024] [so:warn] [pid 775:tid 775] AH01574: module rewrite_module is already loaded, skipping
Jan 30 08:32:31 hela.javiercd.gonzalonazareno.org httpd[775]: Server configured, listening on: port 80
Jan 30 08:32:31 hela.javiercd.gonzalonazareno.org systemd[1]: Started The Apache HTTP Server.
```

