---
title: "Configuración activación de SELinux"
date: 2023-09-20T10:00:00+00:00
description: SELinux define los controles de acceso para las aplicaciones, los procesos y los archivos dentro de un sistema
tags: [ASO,REDHAT,ROCKY,CENTOS]
hero: images/sistemas/selinux/selinux.jpg
---


Habilita SELinux en un servidor basado en Rocky y asegúrate que los servicios samba y nfs funcionan correctamente con una configuración estricta y segura de SELinux. Realiza las pruebas de acceso correspondientes.

El escenario consta de dos máquinas , nuestro servidor esta basado en Rocky 9 y nuestro cliente es un Debian 12 .

En nuestro servidor tendremos activado SELinux en modo enforcing .

```bash
[rocky@rocky-javiercruces ~]$ sestatus
SELinux status:                 enabled
SELinuxfs mount:                /sys/fs/selinux
SELinux root directory:         /etc/selinux
Loaded policy name:             targeted
Current mode:                   enforcing
Mode from config file:          enforcing
Policy MLS status:              enabled
Policy deny_unknown status:     allowed
Memory protection checking:     actual (secure)
Max kernel policy version:      33
```


Comenzaremos actualizando los paquetes necesarios para configurar samba y nfs :

```bash
[rocky@rocky-javiercruces ~]$ sudo dnf update -y
[rocky@rocky-javiercruces ~]$ sudo dnf install samba samba-common samba-client nfs-utils -y
```


## Samba 

Un recurso compartido de samba es esencialmente un directorio que se compartirá entre los sistemas cliente de la red. Por lo tanto, crearemos un directorio como se muestra. Yo lo hare en el directorio home de mi usuario :

```bash
[rocky@rocky-javiercruces ~]$ mkdir sambashare
```

Le daremos los permisos y la propiedad correspondientes al directorio que acabamos de crear para que sea accesible a través del servicio :

```bash
[rocky@rocky-javiercruces ~]$ sudo chmod -R 755 /home/rocky/sambashare
[rocky@rocky-javiercruces ~]$ sudo chown -R  nobody:nobody /home/rocky/sambashare
[rocky@rocky-javiercruces ~]$ sudo chcon -t samba_share_t /home/rocky/sambashare
```

Ahora vamos a crear un recurso compartido dentro de la configuración de samba , lo añadiré al final del fichero :

```bash
[rocky@rocky-javiercruces ~]$ sudo vim /etc/samba/smb.conf 

[sambashare]
        path = /home/rocky/sambashare
        browsable =yes
        writable = yes
        guest ok = yes
        read only = no
```

Para verificar el archivo de configuración, ejecuta el siguiente comando :

```bash
[rocky@rocky-javiercruces ~]$ sudo testparm
```

Con la configuración actual podremos acceder al recurso de forma anónima , aunque podemos configurar usuarios samba :

```bash
[rocky@rocky-javiercruces ~]$ sudo smbpasswd -a rocky     
```

Luego añade al fichero de configuración la linea "valid users = usuario" al final de cada declaración de recurso , te dejo un ejemplo :

```bash
[sambashare]
	path = /home/rocky/sambashare
        guest only = no
        writable = yes
        force create mode = 0666
        force directory mode = 0777
        browseable = yes
        valid users = rocky
```

Ahora vamos a arrancar el servicio : 

```bash
[rocky@rocky-javiercruces ~]$ sudo systemctl start smb
[rocky@rocky-javiercruces ~]$ sudo systemctl enable smb

[rocky@rocky-javiercruces ~]$ sudo systemctl start nmb
[rocky@rocky-javiercruces ~]$ sudo systemctl enable nmb
```

Vamos a confirmas que ambos servicios están funcionando :

```bash
[rocky@rocky-javiercruces ~]$ sudo systemctl status smb
● smb.service - Samba SMB Daemon
     Loaded: loaded (/usr/lib/systemd/system/smb.service; enabled; preset: disabled)
     Active: active (running) since Mon 2024-02-05 11:21:45 UTC; 1min 50s ago
       Docs: man:smbd(8)
             man:samba(7)
             man:smb.conf(5)
   Main PID: 49025 (smbd)
     Status: "smbd: ready to serve connections..."
      Tasks: 3 (limit: 4340)
     Memory: 8.6M
        CPU: 70ms
     CGroup: /system.slice/smb.service
             ├─49025 /usr/sbin/smbd --foreground --no-process-group
             ├─49027 /usr/sbin/smbd --foreground --no-process-group
             └─49028 /usr/sbin/smbd --foreground --no-process-group

Feb 05 11:21:45 rocky-javiercruces.novalocal systemd[1]: Starting Samba SMB Daemon...
Feb 05 11:21:45 rocky-javiercruces.novalocal smbd[49025]: [2024/02/05 11:21:45.649440,  0] ../../source3/smbd/server.c:1746(main)
Feb 05 11:21:45 rocky-javiercruces.novalocal smbd[49025]:   smbd version 4.18.6 started.
Feb 05 11:21:45 rocky-javiercruces.novalocal smbd[49025]:   Copyright Andrew Tridgell and the Samba Team 1992-2023
Feb 05 11:21:45 rocky-javiercruces.novalocal systemd[1]: Started Samba SMB Daemon.

[rocky@rocky-javiercruces ~]$ sudo systemctl status nmb
● nmb.service - Samba NMB Daemon
     Loaded: loaded (/usr/lib/systemd/system/nmb.service; enabled; preset: disabled)
     Active: active (running) since Mon 2024-02-05 11:22:49 UTC; 1min 7s ago
       Docs: man:nmbd(8)
             man:samba(7)
             man:smb.conf(5)
   Main PID: 49065 (nmbd)
     Status: "nmbd: ready to serve connections..."
      Tasks: 1 (limit: 4340)
     Memory: 2.8M
        CPU: 48ms
     CGroup: /system.slice/nmb.service
             └─49065 /usr/sbin/nmbd --foreground --no-process-group

Feb 05 11:22:49 rocky-javiercruces.novalocal nmbd[49065]: [2024/02/05 11:22:49.116367,  0] ../../source3/nmbd/nmbd.c:901(main)
Feb 05 11:22:49 rocky-javiercruces.novalocal nmbd[49065]:   nmbd version 4.18.6 started.
Feb 05 11:22:49 rocky-javiercruces.novalocal nmbd[49065]:   Copyright Andrew Tridgell and the Samba Team 1992-2023
Feb 05 11:22:49 rocky-javiercruces.novalocal systemd[1]: Started Samba NMB Daemon.
Feb 05 11:23:12 rocky-javiercruces.novalocal nmbd[49065]: [2024/02/05 11:23:12.157234,  0] ../../source3/nmbd/nmbd_become_lmb.c:398(become_local_master_stage2)
Feb 05 11:23:12 rocky-javiercruces.novalocal nmbd[49065]:   *****
Feb 05 11:23:12 rocky-javiercruces.novalocal nmbd[49065]: 
Feb 05 11:23:12 rocky-javiercruces.novalocal nmbd[49065]:   Samba name server ROCKY-JAVIERCRUCES is now a local master browser for workgroup SAMBA on subnet 10.0.0.150
Feb 05 11:23:12 rocky-javiercruces.novalocal nmbd[49065]: 
Feb 05 11:23:12 rocky-javiercruces.novalocal nmbd[49065]:   *****
```

Los resultados anteriores indican que los servicios se están ejecutando. Ahora habilitemos el protocolo samba en el firewall para permitir que los clientes puedan conectarse :

```bash
[rocky@rocky-javiercruces ~]$ sudo firewall-cmd --permanent --add-service=samba
success
[rocky@rocky-javiercruces ~]$ sudo firewall-cmd --reload
success
```


Ahora en nuestro cliente , nos instalamos el cliente y comprobamos a conectarnos remotamente :

```bash
javiercruces@odin:~$ sudo apt install samba-client -y

javiercruces@odin:~$ sudo smbclient //172.22.201.86/sambashare -U rocky
Password for [WORKGROUP\rocky]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Mon Feb 12 09:42:09 2024
  ..                                  D        0  Mon Feb  5 11:50:24 2024
  fichero_prueba                      N        0  Mon Feb 12 09:42:09 2024

		9286656 blocks of size 1024. 7952516 blocks available
smb: \> 
```

Comprobaremos que en ambos extremos tenemos los mismos ficheros :

```bash
[rocky@rocky-javiercruces ~]$ sudo ls -l /home/rocky/sambashare/
total 0
-rwxr-xr-x. 1 nobody nobody 0 Feb 12 09:42 fichero_prueba
```

## NFS

Nos instalamos el servidor nfs en rocky :

```bash
[rocky@rocky-javiercruces ~]$ sudo dnf install nfs-utils
```

En el cliente debian , en este caso odin nos descargamos "el cliente" 

```bash
javiercruces@odin:~$ sudo apt install nfs-common
```

Creamos el directorio que queremos compartir :

```bash
[rocky@rocky-javiercruces ~]$ sudo mkdir /var/nfs/general -p
```

Le damos los permisos adecuados para que nfs funcione correctamente.

```bash
[rocky@rocky-javiercruces ~]$ sudo chown nobody /var/nfs/general
```

Mostramos la configuración actual de los servicios permitidos a través del firewall usando firewalld :

```bash
[rocky@rocky-javiercruces ~]$ sudo firewall-cmd --permanent --list-all | grep services
  services: cockpit dhcpv6-client samba ssh
```

Como no tenemos permitido nfs , lo permitiremos haciendo uso del servicio : 

```bash
[rocky@rocky-javiercruces ~]$ sudo firewall-cmd --permanent --add-service=nfs
success
[rocky@rocky-javiercruces ~]$ sudo firewall-cmd --permanent --add-service=mountd
success
[rocky@rocky-javiercruces ~]$ sudo firewall-cmd --permanent --add-service=rpc-bind
success
[rocky@rocky-javiercruces ~]$ sudo firewall-cmd --reload
success
```

Volvemos a listar los servicios permitidos y nos aseguramos que este nfs , mountd y rcp-bind  :

```bash
[rocky@rocky-javiercruces ~]$ sudo firewall-cmd --permanent --list-all | grep services
  services: cockpit dhcpv6-client mountd nfs rpc-bind samba ssh
```

Ahora en el cliente elegiremos donde montaremos el directorio compartido , yo creare uno nuevo :

```bash
javiercruces@odin:~$ sudo mkdir -p /nfs/general
```

Y montaremos el nuevo directorio :

```bash
javiercruces@odin:~$ sudo mount 172.22.201.86:/var/nfs/general /nfs/general
```

Comprobamos que se ha montado : 

```bash
javiercruces@odin:~$ df -h
Filesystem                      Size  Used Avail Use% Mounted on
udev                            965M     0  965M   0% /dev
tmpfs                           197M  684K  197M   1% /run
/dev/vda1                        15G  7.0G  7.1G  50% /
tmpfs                           984M     0  984M   0% /dev/shm
tmpfs                           5.0M     0  5.0M   0% /run/lock
/dev/vda15                      124M   12M  113M  10% /boot/efi
tmpfs                           197M     0  197M   0% /run/user/1000
172.22.201.86:/var/nfs/general  8.9G  1.3G  7.6G  15% /nfs/general
```

Y comprobamos que en ambos extremos tenemos los mismos ficheros :

```bash
[rocky@rocky-javiercruces ~]$ sudo ls -l /var/nfs/general/
total 0
-rw-r--r--. 1 nobody nobody 0 Feb 12 09:38 fichero_prueba

javiercruces@odin:~$ ls -l /nfs/general
total 0
-rw-r--r-- 1 nobody nogroup 0 Feb 12 09:38 fichero_prueba
```
