---
title: "Crear autoridad certificadora (CA) y certificados autofirmados en Linux"
date: 2024-03-28T10:00:00+00:00
description: Crear autoridad certificadora (CA) y certificados autofirmados en Linux
tags: [LINUX,DEBIAN,HTTPS]
hero: /images/seguridad/https.png
---

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GVDYVWJLRH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GVDYVWJLRH');
</script>

En un primer momento un alumno creará una Autoridad Certficadora y firmará un certificado para la página del otro alumno. Posteriormente lo pondremos a prueba en los servidores web Apache y Nginx

## Crear la Autoridad Certificadora

### Paso 1: Creación de directorios y archivos

El primer paso será generar un directorio en el que ubicarás tu entidad certificadora, con la finalidad de mantener en todo momento una organización. El nombre del directorio será CA/. A su vez, hay que generar varios subdirectorios dentro del mismo:
- certsdb: En dicho directorio se almacenarán los certificados firmados.
- certreqs: En dicho directorio se almacenarán los ficheros de solicitud de firma de certificados (CSR).
- crl: En dicho directorio se almacenará la lista de certificados que han sido revocados (CRL).
-  private: En dicho directorio se almacenará la clave privada de la autoridad certificadora.
```bash
debian@javiercrucesCA:~$ sudo mkdir /CA
debian@javiercrucesCA:~$ cd !$
debian@javiercrucesCA:/CA$ sudo mkdir certsdb certreqs crl private
debian@javiercrucesCA:/CA$ sudo chmod 700 private/
debian@javiercrucesCA:/CA$ sudo touch index.txt
```
Una vez generados los directorios, muévete dentro del directorio padre CA/. Cuando te encuentres dentro del mismo, lista el contenido de forma gráfica para así poder apreciar que todo se ha generado correctamente, haciendo para ello uso de tree.
Verás que los 4 directorios han sido correctamente generados. Antes de continuar es recomendable cambiar los permisos a 700 al directorio private/, ya que contendrá la clave privada de la CA y nos interesa que únicamente el propietario tenga acceso a la misma.
Además, necesitaremos en el directorio actual un fichero que actuará como base de datos para los certificados existentes de nombre index.txt

```bash
debian@javiercrucesCA:/CA$ sudo tree -p
[drwxr-xr-x]  .
├── [drwxr-xr-x]  certreqs
├── [drwxr-xr-x]  certsdb
├── [drwxr-xr-x]  crl
├── [-rw-r--r--]  index.txt
└── [drwx------]  private

5 directories, 1 file
debian@javiercrucesCA:/CA$ 


```

### Paso 2: Fichero de configuración de openssl

Lo más probable es que quieras usar un fichero de configuración de openssl que no sea el de nuestra máquina, para así tratar de que la autoridad certificadora esté en todo momento lo más aislada posible de la misma, así que haz una copia de tu fichero de configuración nativo y adáptalo a tus necesidades. Dicho fichero se encuentra normalmente en /usr/lib/ssl/openssl.cnf, aunque también podría estar en /etc/openssl.cnf o en /usr/share/ssl/openssl.cnf, tendrás que copiarlo al directorio actual y modificarlo con un editor de textos.
```bash
debian@javiercrucesCA:/CA$ sudo cp /usr/lib/ssl/openssl.cnf ./
debian@javiercrucesCA:/CA$ ls -l
total 32
drwxr-xr-x 2 root root  4096 Jan  8 19:22 certreqs
drwxr-xr-x 2 root root  4096 Jan  8 19:22 certsdb
drwxr-xr-x 2 root root  4096 Jan  8 19:22 crl
-rw-r--r-- 1 root root     0 Jan  8 19:23 index.txt
-rw-r--r-- 1 root root 12332 Jan  8 19:26 openssl.cnf
drwx------ 2 root root  4096 Jan  8 19:22 private

```

Dentro del mismo, hay que realizar las oportunas adaptaciones para que haga uso de los directorios anteriormente generados, así como indicar determinada información básica sobre la autoridad certificadora, que vuestro compañero debe conocer, pues le será solicitada a la hora de la generación del fichero de solicitud de firma de certificado. Las modificaciones a realizar son las siguientes:

dir = /root/CA
certs = $dir/certsdb
new_certs_dir = $certs

```bash
[ CA_default ]

dir             = /CA           # Where everything is kept
certs           = $dir/certsdb          # Where the issued certs are kept
crl_dir         = $dir/crl              # Where the issued crl are kept
database        = $dir/index.txt        # database index file.
#unique_subject = no                    # Set to 'no' to allow creation of
                                        # several certs with same subject.
new_certs_dir   = $certs                # default place for new certs.

```

countryName_default = ES
stateOrProvinceName_default = Sevilla
localityName_default = Dos Hermanas
0.organizationName_default = IES Gonzalo Nazareno
organizationalUnitName_default = Informatica

```bash
[ req_distinguished_name ]
countryName                     = Country Name (2 letter code)
countryName_default             = ES
countryName_min                 = 2
countryName_max                 = 2

stateOrProvinceName             = State or Province Name (full name)
stateOrProvinceName_default     = Sevilla   

localityName                    = Dos Hermanas

0.organizationName              = Organization Name (eg, company)
0.organizationName_default      = IES Gonzalo Nazareno

# we can do this but it is not needed normally :-)
#1.organizationName             = Second Organization Name (eg, company)
#1.organizationName_default     = World Wide Web Pty Ltd

organizationalUnitName          = Organizational Unit Name (eg, section)
organizationalUnitName_default  = Informatica

```

#challengePassword = A challenge password
#challengePassword_min = 4
#challengePassword_max = 20
#unstructuredName = An optional company name

```bash
[ req_attributes ]
challengePassword               = A challenge password
challengePassword_min           = 4
challengePassword_max           = 20

unstructuredName                = An optional company name

```

### Paso 3: Creación y firmado de nuestra propio certificado

Tras ello, ya tendrás todo listo para generar tu par de claves y un fichero de solicitud de firma de certificado que posteriormente te autofirmarás, ejecutando para ello el comando:

```bash
debian@javiercrucesCA:/CA$ sudo openssl req -new -newkey rsa:4096 -keyout private/cakey.pem -out careq.pem -config ./openssl.cnf

Enter PEM pass phrase:
Verifying - Enter PEM pass phrase:
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [ES]:ES
State or Province Name (full name) [Sevilla]:Sevilla
Dos Hermanas []:
Organization Name (eg, company) [IES Gonzalo Nazareno]:
Organizational Unit Name (eg, section) [Informatica]:
Common Name (e.g. server FQDN or YOUR name) []:javiercruces.iesgn.org
Email Address []:javierasping@gmail.com

```

Como puedes ver, se solicita una frase de paso para proteger la clave privada que vamos a generar, así como determinada información básica para el fichero de solicitud de firma de certificado, que debe coincidir con la que anteriormente hemos introducido en el fichero de configuración de openssl. Los dos últimos campos no son genéricos, por lo que debemos rellenarlos según el caso. Tras ello, ya podremos proceder a autofirmarnos el certificado, que es el que posteriormente tendremos que facilitar a los clientes para que incluyan en su lista de certificados de CA, para que así no se les muestre la advertencia al utilizar HTTPS. Como he mencionado anteriormente, en una situación real, este proceso lo suelen llevar a cabo empresas con determinada reputación cuyo certificado se encuentra importado por defecto en los navegadores. Para ello, ejecuta el comando:

```bash
debian@javiercrucesCA:/CA$ sudo openssl ca -create_serial -out cacert.pem -days 365 -keyfile private/cakey.pem -selfsign -extensions v3_ca -config ./openssl.cnf -infiles careq.pem
Using configuration from ./openssl.cnf
Enter pass phrase for private/cakey.pem:
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number:
            74:1e:8a:f8:24:45:14:9e:28:f1:83:04:7c:7d:6c:0f:5f:3b:ac:f2
        Validity
            Not Before: Jan  8 19:57:17 2024 GMT
            Not After : Jan  7 19:57:17 2025 GMT
        Subject:
            countryName               = ES
            stateOrProvinceName       = Sevilla
            organizationName          = IES Gonzalo Nazareno
            organizationalUnitName    = Informatica
            commonName                = javiercruces.iesgn.org
            emailAddress              = javierasping@gmail.com
        X509v3 extensions:
            X509v3 Subject Key Identifier: 
                E3:9C:A3:CF:0E:33:EB:83:45:40:00:9B:04:4A:A9:9B:C8:8C:A9:62
            X509v3 Authority Key Identifier: 
                E3:9C:A3:CF:0E:33:EB:83:45:40:00:9B:04:4A:A9:9B:C8:8C:A9:62
            X509v3 Basic Constraints: critical
                CA:TRUE
Certificate is to be certified until Jan  7 19:57:17 2025 GMT (365 days)
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Data Base Updated
debian@javiercrucesCA:/CA$ 

```

Donde:
- create_serial: Indicamos que genere un serial de 128 bits para comenzar. Gracias a dicha aleatoriedad, si tuviésemos que volver a empezar, no sobreescribiríamos los ya existentes. Es muy importante.
- out: Especificamos dónde se va a almacenar el certificado firmado. En este caso, en el directorio actual, con nombre cacert.pem.
- days: Especificamos la validez en días del certificado firmado. En este caso, 365 días.
- keyfile: Indicamos la clave privada a usar para firmar dicho certificado. En este caso, la generada en el paso anterior, private/cakey.pem.
- selfsign: Indicamos a openssl que vamos a autofirmarnos el certificado.
- extensions: Indicamos a openssl la sección del fichero de configuración en el que se encuentran las extensiones a usar. En este caso, v3_ca.
 - config: Especificamos a openssl que utilice el fichero de configuración modificado, no el nativo, con nombre openssl.cnf.
 - infiles: Indicamos qué queremos firmar, en este caso, el CSR para nuestra nueva autoridad certificadora creado en el paso anterior, con nombre careq.pem.

Como se puede apreciar en la salida del comando, se nos ha pedido la frase de paso previamente configurada, para así asegurarnos que aunque la clave privada llegase a malas manos, no puedan realizar firmas fraudulentas. Además, antes de firmar el certificado, se nos ha mostrado toda la información referente al mismo, y se nos ha pedido confirmación. 
Para verificar que el certificado de la autoridad certificadora se encuentra contenido en el directorio actual, lista el contenido del mismo y comprueba que, efectivamente, existe un fichero cacert.pem que es resultado de firmar el fichero de solicitud de firma de certificado careq.pem.

```bash
debian@javiercrucesCA:/CA$ sudo tree
.
├── cacert.pem
├── careq.pem
├── certreqs
├── certsdb
│   └── 741E8AF82445149E28F183047C7D6C0F5F3BACF2.pem
├── crl
├── index.txt
├── index.txt.attr
├── index.txt.old
├── openssl.cnf
├── private
│   └── cakey.pem
└── serial

5 directories, 9 files
debian@javiercrucesCA:/CA$ 


```

### Paso 4: Firma de solicitudes de certificado

Ya está todo listo para proceder a firmar el certificado para el servidor de tu compañero, así que debes situar su fichero de solicitud de firma de certificado dentro de certreqs/, que es donde deben ubicarse.

```bash
debian@javiercrucesCA:~$ sudo ls -l /CA/certreqs/
total 4
-rw-r--r-- 1 root root 1785 Jan 11 10:00 peperc.csr
```

Puedes proceder a firmarlo, haciendo uso del comando:

```bash
debian@javiercrucesCA:/CA$ sudo openssl ca -config openssl.cnf -extensions v3_req -days 3650 -notext -md sha256 -in certreqs/peperc.csr -out certsdb/pepe.csr.pem
Using configuration from openssl.cnf
Enter pass phrase for /CA/private/cakey.pem:
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number:
            74:1e:8a:f8:24:45:14:9e:28:f1:83:04:7c:7d:6c:0f:5f:3b:ac:f3
        Validity
            Not Before: Jan 11 10:01:58 2024 GMT
            Not After : Jan  8 10:01:58 2034 GMT
        Subject:
            countryName               = ES
            stateOrProvinceName       = Sevilla
            organizationName          = IES Gonzalo Nazareno
            commonName                = pfoter15
            emailAddress              = pepepfoter15@gmail.com
        X509v3 extensions:
            X509v3 Basic Constraints: 
                CA:FALSE
            X509v3 Key Usage: 
                Digital Signature, Non Repudiation, Key Encipherment
Certificate is to be certified until Jan  8 10:01:58 2034 GMT (3650 days)
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Database updated
```


Donde:
- config: Especificamos a openssl que utilice el fichero de configuración modificado, no el nativo, con nombre openssl.cnf.
 - out: Especificamos dónde se va a almacenar el certificado firmado. En este caso, dentro del directorio certsdb/, con nombre nombre.crt.
- infiles: Indicamos qué queremos firmar, en este caso, el CSR de nuestro compañero, situado en certreqs/ con nombre nombre.csr.

En un principio, el certificado ya se encuentra firmado dentro de certsdb/, así que para verificarlo, vas a listar el contenido de dicho directorio.

Deben existir un total de 3 ficheros dentro del mismo: uno correspondiente al propio certificado de la autoridad certificadora, y dos correspondientes a tu compañero, que son exactamente lo mismo pero con diferentes nombres, uno de ellos con un identificador y el otro, con un nombre común que nosotros hemos establecido para así identificarlo con una mayor facilidad.

```bash
debian@javiercrucesCA:~$ sudo ls -l /CA/certsdb/
total 16
-rw-r--r-- 1 root root 7429 Jan  8 19:57 741E8AF82445149E28F183047C7D6C0F5F3BACF2.pem
-rw-r--r-- 1 root root 2139 Jan 11 10:02 741E8AF82445149E28F183047C7D6C0F5F3BACF3.pem
-rw-r--r-- 1 root root 2139 Jan 11 10:02 pepe.csr.pem

```

###  Paso 5: Envío de certificados al servidor web.

Hasta aquí ha llegado tu parte, ya que únicamente quedaría hacerle llegar a tu compañero el fichero certsdb/nombre.crt, que es su certificado firmado, junto al propio certificado de la autoridad certificadora, el cuál contiene la clave pública, para así poder verificar dicha firma sobre su certificado, de nombre cacert.pem. Por último, vas a mostrar el contenido del fichero index.txt, que es una especie de base de datos en texto plano con información sobre los certificados firmados por la autoridad certificadora. Dentro del mismo, encontramos información básica correspondiente a los dos certificados firmados: el de la propia autoridad certificadora y el de nuestro compañero, además de su estado de validez actual.

Voy a enviar y a traerme de la instancia de pepe las diferentes ficheros , el ha configurado mi clave publica para que pueda conectarme  :

```bash
debian@javiercrucesCA:~$ scp javiercd.csr 172.22.200.113:/home/debian/ 
javiercd.csr                          100% 1886   839.4KB/s   00:00   

debian@javiercrucesCA:~$ scp 172.22.200.113:/home/debian/peperc.csr ./ 
peperc.csr                            100% 1785   432.6KB/s   00:00   

-- Le envio su certificado firmado
debian@javiercrucesCA:~$ scp 172.22.200.113:/CA/certsdb/pepe.csr.pem
pepe.csr.pem                           100% 1785   432.6KB/s   00:00

debian@javiercrucesCA:~$ scp /CA/cacert.pem  172.22.200.113:/home/debian/pub_javi.pem 
cacert.pem                            100% 7429   582.6KB/s   00:00    

debian@javiercrucesCA:~$ scp 172.22.200.113:/CA/cacert.pem ./pub_pepe.pem 
cacert.pem                            100% 7389     1.2MB/s   00:00   


```




## Tarea 2: Configurar HTTPS

### Paso 1: Creación de clave y solicitud de certificado.

Lo primero que tendrás que hacer es crear una solicitud de firma de certificado (CSR o Certificate Signing Request) y hacérselo llegar a tu compañero. En este caso, vamos a hacerlo con openssl, pero se podría hacer con otras múltiples opciones de software. 

Para crear una solicitud de firma de certificado, primero debemos tener una clave privada que se asociará al mismo, así que generaremos una clave privada RSA de 4096 bits, que será almacenada en /etc/ssl/private/, ejecutando para ello el comando:

```bash
debian@javiercrucesCA:~$ sudo openssl genrsa 4096 > javiercd.key
debian@javiercrucesCA:~$ sudo mv javiercd.key /etc/ssl/private/
```

Una vez generada, cambiaremos los permisos de la misma a 400, de manera que únicamente el propietario pueda leer el contenido, pues se trata de una clave privada. Este paso no es obligatorio pero sí recomendable por seguridad. Escribe el comando necesario para ello.

```bash
debian@javiercrucesCA:~$ sudo chmod 400 /etc/ssl/private/javiercd.key
```

Tras ello, crearemos un fichero .csr de solicitud de firma de certificado para que sea firmado por la autoridad certificadora (CA) creada por nuestro compañero. Dicho fichero no contiene información confidencial, así que no importará la ruta donde lo almacenemos ni los permisos asignados. En mi caso, lo almacenaré en el directorio actual, ejecutando para ello el comando openssl req, con las opciones:

- new: Indicamos que la creación de la solicitud de firma de certificado sea interactiva, pues nos pedirá determinados parámetros.
 - key: Indicamos la clave privada a asociar a dicha solicitud de firma de certificado. En este caso, la generada en el paso anterior, /etc/ssl/private/tunombre.key.
 - out: Especificamos dónde se va a almacenar la solicitud de firma de certificado. En este caso, en el directorio actual, con nombre tunombre.csr.

Durante la ejecución, nos pedirá una serie de valores para identificar al certificado, que tendremos que rellenar conforme a la configuracion que hemos realizado en la unidad certificadora .

Dicha información nos la tendrá que dar la autoridad certificadora, excepto los dos últimos valores, que en el caso del Common Name, pondrás el FQDN de la web en la que queremos configurar HTTPS. Además, tendrás que introducir tu correo electrónico en el apartado Email Address.

```bash
debian@javiercrucesCA:/CA$ sudo openssl ca -config openssl.cnf -extensions v3_req -days 3650 -notext -md sha256 -in certreqs/peperc.csr -out certsdb/pepe.csr.pem
Using configuration from openssl.cnf
Enter pass phrase for /CA/private/cakey.pem:
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number:
            74:1e:8a:f8:24:45:14:9e:28:f1:83:04:7c:7d:6c:0f:5f:3b:ac:f3
        Validity
            Not Before: Jan 11 10:01:58 2024 GMT
            Not After : Jan  8 10:01:58 2034 GMT
        Subject:
            countryName               = ES
            stateOrProvinceName       = Sevilla
            organizationName          = IES Gonzalo Nazareno
            commonName                = pfoter15
            emailAddress              = pepepfoter15@gmail.com
        X509v3 extensions:
            X509v3 Basic Constraints: 
                CA:FALSE
            X509v3 Key Usage: 
                Digital Signature, Non Repudiation, Key Encipherment
Certificate is to be certified until Jan  8 10:01:58 2034 GMT (3650 days)
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Database updated

```

Para verificar que el fichero de solicitud de firma ha sido correctamente generado, lista el contenido del directorio actual. Debe existir un fichero de nombre tunombre.csr que debes enviar a tu compañero, para que así sea firmado por la correspondiente autoridad certificadora que ha creado.

```bash
debian@javiercrucesCA:~$ ls -l 
total 16
-rw-r--r-- 1 root   root   1886 Jan 11 09:40 javiercd.csr

```

En mi caso se lo haré llegar usando SCP :

```bash
debian@javiercrucesCA:~$ scp javiercd.csr 172.22.200.113:/home/debian/ 
javiercd.csr                          100% 1886   839.4KB/s   00:00   
```

Una vez firmado me lo traeré de su servidor 
### Paso 2: Almacenamiento de certificados en el servidor

Además de dicho certificado firmado, nos debe enviar la clave pública de la entidad certificadora, es decir, el certificado de la misma, para así poder verificar su firma sobre nuestro certificado.
Almacena ambos ficheros en /etc/ssl/certs/ y lista el contenido de dicho directorio.

```bash
debian@javiercrucesCA:~$ sudo mv javiercd.csr.pem /etc/ssl/certs/
debian@javiercrucesCA:~$ sudo mv pub_pepe.pem /etc/ssl/certs


```

Debe existir un fichero de nombre tunombre.crt que es el resultado de la firma de la solicitud de firma de certificado que previamente le hemos enviado, y otro de nombre cacert.pem, que es el certificado de la entidad certificadora, con el que posteriormente se comprobará la firma de la autoridad certificadora sobre dicho certificado del servidor.

```bash
debian@javiercrucesCA:/CA$ sudo ls -l /etc/ssl/certs | grep javi
-rw-r--r-- 1 debian debian   2175 Jan 11 10:05 javiercd.csr.pem
debian@javiercrucesCA:/CA$ sudo ls -l /etc/ssl/certs | grep pepe
-rw-r--r-- 1 root   root     7389 Jan 11 11:24 pub_pepe.pem
debian@javiercrucesCA:/CA$ sudo ls -l /etc/ssl/private/ 
total 8
-r-------- 1 debian debian   3272 Jan 11 09:37 javiercd.key

```


### Paso 3: Configuración de Apache

Al igual que apache2 incluía un VirtualHost por defecto para las peticiones entrantes por el puerto 80 (HTTP), contiene otro por defecto para las peticiones entrantes por el puerto 443 (HTTPS), de nombre default-ssl, que por defecto viene deshabilitado, así que procederemos a modificarlo teniendo en cuenta las siguientes directivas:

- ServerName: Al igual que en el VirtualHost anterior, tendremos que indicar el nombre de dominio a través del cuál accederemos al servidor.
- SSLEngine: Activa el motor SSL, necesario para hacer uso de HTTPS, por lo que su valor debe ser on.
- SSLCertificateFile: Indicamos la ruta del certificado del servidor firmado por la CA. En este caso, /etc/ssl/certs/tunombre.crt.
- SSLCertificateKeyFile: Indicamos la ruta de la clave privada asociada al certificado del servidor. En este caso, /etc/ssl/private/tunombre.key.
- SSLCACertificateFile: Indicamos la ruta del certificado de la CA con el que comprobaremos la firma de nuestro certificado. En este caso, /etc/ssl/certs/cacert.pem.

```bash

debian@javiercrucesCA:/CA$ sudo a2enmod ssl 
debian@javiercrucesCA:/CA$ sudo a2ensite default-ssl.conf 

debian@javiercrucesCA:~$ sudo cat /etc/apache2/sites-available/default-ssl.conf 
<VirtualHost *:80> 
  ServerName javiercruces.iesgn.org

  Redirect permanent / https://javiercruces.iesgn.org/
</VirtualHost>
<VirtualHost *:443>
	ServerAdmin webmaster@localhost
	ServerName javiercruces.iesgn.org
	DocumentRoot /var/www/html

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	SSLEngine on

	SSLCertificateFile      /etc/ssl/certs/javiercd.csr.pem
	SSLCertificateKeyFile   /etc/ssl/private/javiercd.key
</VirtualHost>

debian@javiercrucesCA:~$ sudo systemctl reload apache2.service 


```


Demostración :

![](../img/Pastedimage20240111115927.png)

### Paso 4: Configuración de Nginx

Vamos a forzar la configuración de https en Nginx

Aquí te dejo la configuración del virtualhost :

```bash
debian@javiercrucesCA:/var/www/sad$ sudo cat /etc/nginx/sites-available/default 
server {
    listen 80;
    listen [::]:80;
    server_name javiercruces.iesgn.org;

    # Redirección a HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    root /var/www/sad;
    index  index.php index.html index.htm;
    server_name moodle.javiercd.es;

    ssl_certificate /etc/ssl/certs/javiercd.csr.pem;
    ssl_certificate_key /etc/ssl/private/javiercd.key;

}

```


![](../img/Pastedimage20240111191950.png)