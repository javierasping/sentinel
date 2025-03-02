---
title: "SELinux activation configuration"
date: 2023-09-20T10:00:00+00:00
Description: SELinux defines access controls for applications, processes and files within a system
tags: [ASO,REDHAT,ROCKY,CENTOS]
hero: images/sistemas/selinux/selinux.jpg
---


Enable SELinux on a Rocky-based server and make sure that the samba and nfs services work properly with a strict and secure SELinux configuration. Conducts the corresponding access tests.

The stage consists of two machines, our server is based on Rocky 9 and our client is a Debian 12.

On our server we will have SELinux enabled in enforcing mode.

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


We will start by updating the packages needed to configure samba and nfs:

```bash
[rocky@rocky-javiercruces ~]$ sudo dnf update -y
[rocky@rocky-javiercruces ~]$ sudo dnf install samba samba-common samba-client nfs-utils -y
```


### Samba

A shared samba resource is essentially a directory that will be shared among the network's client systems. So, we'll create a directory as shown. I'll do it in my user's home directory:

```bash
[rocky@rocky-javiercruces ~]$ mkdir sambashare
```

We will give you the permissions and property corresponding to the directory we have just created to make it accessible through the service:

```bash
[rocky@rocky-javiercruces ~]$ sudo chmod -R 755 /home/rocky/sambashare
[rocky@rocky-javiercruces ~]$ sudo chown -R  nobody:nobody /home/rocky/sambashare
[rocky@rocky-javiercruces ~]$ sudo chcon -t samba_share_t /home/rocky/sambashare
```

Now we will create a shared resource within the samba configuration, I will add it at the end of the file:

```bash
[rocky@rocky-javiercruces ~]$ sudo vim /etc/samba/smb.conf 

[sambashare]
        path = /home/rocky/sambashare
        browsable =yes
        writable = yes
        guest ok = yes
        read only = no
```

To verify the configuration file, run the following command:

```bash
[rocky@rocky-javiercruces ~]$ sudo testparm
```

With the current configuration we can access the resource anonymously, although we can configure samba users:

```bash
[rocky@rocky-javiercruces ~]$ sudo smbpasswd -a rocky     
```

Then add to the configuration file the "valid users = user" line at the end of each resource statement, leaving you an example:

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

Now let's start the service:

```bash
[rocky@rocky-javiercruces ~]$ sudo systemctl start smb
[rocky@rocky-javiercruces ~]$ sudo systemctl enable smb

[rocky@rocky-javiercruces ~]$ sudo systemctl start nmb
[rocky@rocky-javiercruces ~]$ sudo systemctl enable nmb
```

Let's confirm that both services are working:

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

The above results indicate that services are being implemented. Now let's enable the samba protocol on the firewall to allow customers to connect:

```bash
[rocky@rocky-javiercruces ~]$ sudo firewall-cmd --permanent --add-service=samba
success
[rocky@rocky-javiercruces ~]$ sudo firewall-cmd --reload
success
```


Now in our client, we install the client and check to connect remotely:

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

We'll check that at both ends we have the same files:

```bash
[rocky@rocky-javiercruces ~]$ sudo ls -l /home/rocky/sambashare/
total 0
-rwxr-xr-x. 1 nobody nobody 0 Feb 12 09:42 fichero_prueba
```

## NFS

We install the nfs server in Rocky:

```bash
[rocky@rocky-javiercruces ~]$ sudo dnf install nfs-utils
```

In the debian client, in this case we download "the client"

```bash
javiercruces@odin:~$ sudo apt install nfs-common
```

We create the directory we want to share:

```bash
[rocky@rocky-javiercruces ~]$ sudo mkdir /var/nfs/general -p
```

We give you the right permissions to make nfs work properly.

```bash
[rocky@rocky-javiercruces ~]$ sudo chown nobody /var/nfs/general
```

We show the current configuration of the services allowed through the firewall using firewall:

```bash
[rocky@rocky-javiercruces ~]$ sudo firewall-cmd --permanent --list-all | grep services
  services: cockpit dhcpv6-client samba ssh
```

Since we are not allowed nfs, we will allow it by making use of the service:

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

We relist the services allowed and make sure that this nfs, mountd and rcp-bind:

```bash
[rocky@rocky-javiercruces ~]$ sudo firewall-cmd --permanent --list-all | grep services
  services: cockpit dhcpv6-client mountd nfs rpc-bind samba ssh
```

Now in the client we will choose where we will set up the shared directory, I will create a new one:

```bash
javiercruces@odin:~$ sudo mkdir -p /nfs/general
```

And we'll set up the new directory:

```bash
javiercruces@odin:~$ sudo mount 172.22.201.86:/var/nfs/general /nfs/general
```

We check that it has been mounted:

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

And we check that at both ends we have the same files:

```bash
[rocky@rocky-javiercruces ~]$ sudo ls -l /var/nfs/general/
total 0
-rw-r--r--. 1 nobody nobody 0 Feb 12 09:38 fichero_prueba

javiercruces@odin:~$ ls -l /nfs/general
total 0
-rw-r--r-- 1 nobody nogroup 0 Feb 12 09:38 fichero_prueba
```
