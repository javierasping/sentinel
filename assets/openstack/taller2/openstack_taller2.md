---
title: "Gestión del almacenamiento en OpenStack"
date: 2023-09-08T10:00:00+00:00
description: Gestión del almacenamiento en OpenStack
tags: [OpenStack, CloudComputing, Instancias, OpenStackCLI, ServiciosEnLaNube, NAT, almacenamiento, LVM, volumenes]
hero: images/openstack/taller1/taller1.png
---

<!-- https://fp.josedomingo.org/sri/5_iaas/taller2.html -->

En este post, exploraremos aspectos fundamentales de la gestión de almacenamiento en OpenStack, centrándonos en la manipulación de volúmenes. A lo largo de este taller, aprenderás a gestionar volúmenes, asociarlos con instancias, redimensionarlos según sea necesario y, por último, crear instancias sobre estos volúmenes .

Puedes encontrar apuntes de este post en la pagina web de mi profesor Jose Domingo https://github.com/josedom24/curso_openstack_ies .


# Taller 2: Gestión del almacenamiento en OpenStack

##  1.Comandos OSC para crear y asociar el volumen.

```bash
(os) javiercruces@HPOMEN15:~$ openstack volume create --size 1 taller2
+---------------------+------------------------------------------------------------------+
| Field               | Value                                                            |
+---------------------+------------------------------------------------------------------+
| attachments         | []                                                               |
| availability_zone   | nova                                                             |
| bootable            | false                                                            |
| consistencygroup_id | None                                                             |
| created_at          | 2023-12-11T09:07:33.565167                                       |
| description         | None                                                             |
| encrypted           | False                                                            |
| id                  | 2d119511-8811-4a45-834c-8bbc0b48b07c                             |
| multiattach         | False                                                            |
| name                | taller2                                                          |
| properties          |                                                                  |
| replication_status  | None                                                             |
| size                | 1                                                                |
| snapshot_id         | None                                                             |
| source_volid        | None                                                             |
| status              | creating                                                         |
| type                | __DEFAULT__                                                      |
| updated_at          | None                                                             |
| user_id             | dfda906ffa44103a62ca25d3b6a90d37da5d36db34fd772a636cccd1d7bc5cea |
+---------------------+------------------------------------------------------------------+
(os) javiercruces@HPOMEN15:~$ 

(os) javiercruces@HPOMEN15:~$ openstack server add volume taller1_op taller2
+-----------------------+--------------------------------------+
| Field                 | Value                                |
+-----------------------+--------------------------------------+
| ID                    | 2d119511-8811-4a45-834c-8bbc0b48b07c |
| Server ID             | 6615d11b-4efd-4b7a-b0a9-a5c2eda31b9b |
| Volume ID             | 2d119511-8811-4a45-834c-8bbc0b48b07c |
| Device                | /dev/vdb                             |
| Tag                   | None                                 |
| Delete On Termination | False                                |
+-----------------------+--------------------------------------+
(os) javiercruces@HPOMEN15:~$ 


```

##  2.Antes de redimensionar el volumen, la salida del comando df -h en la instancia donde hemos asociado el volumen.

```bash
javiercruces@maquina1:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            210M     0  210M   0% /dev
tmpfs            46M  552K   46M   2% /run
/dev/vda1       9.7G  1.8G  7.5G  20% /
tmpfs           229M     0  229M   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
/dev/vda15      124M   12M  113M  10% /boot/efi
tmpfs            46M     0   46M   0% /run/user/1000
/dev/vdb1       988M   24K  921M   1% /mnt
javiercruces@maquina1:~$ 



```

##  3.Comando OSC para redimensionar el volumen. La salida del comando df -h en la instancia donde hemos asociado el volumen, después de redimensionar el sistema de ficheros.

```bash
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack server stop taller1_op 
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack server remove volume taller1_op taller2
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack volume set --size 2 taller2
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack server add volume taller1_op taller2
+-----------------------+--------------------------------------+
| Field                 | Value                                |
+-----------------------+--------------------------------------+
| ID                    | 2d119511-8811-4a45-834c-8bbc0b48b07c |
| Server ID             | a6184d0d-d5f0-4f85-bc01-dee91be24bbb |
| Volume ID             | 2d119511-8811-4a45-834c-8bbc0b48b07c |
| Device                | /dev/vdb                             |
| Tag                   | None                                 |
| Delete On Termination | False                                |
+-----------------------+--------------------------------------+
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack server start taller1_op 

--

javiercruces@maquina1:~$ sudo parted /dev/vdb resizepart 1 100%
Information: You may need to update /etc/fstab.

javiercruces@maquina1:~$ sudo resize2fs /dev/vdb1                         
resize2fs 1.47.0 (5-Feb-2023)
Please run 'e2fsck -f /dev/vdb1' first.

javiercruces@maquina1:~$ sudo e2fsck -f /dev/vdb1
e2fsck 1.47.0 (5-Feb-2023)
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure
Pass 3: Checking directory connectivity
Pass 4: Checking reference counts
Pass 5: Checking group summary information
/dev/vdb1: 11/65408 files (0.0% non-contiguous), 8851/261632 blocks
javiercruces@maquina1:~$ sudo resize2fs /dev/vdb1
resize2fs 1.47.0 (5-Feb-2023)
Resizing the filesystem on /dev/vdb1 to 524027 (4k) blocks.
The filesystem on /dev/vdb1 is now 524027 (4k) blocks long.

javiercruces@maquina1:~$ sudo mount /dev/vdb1 /mnt            
javiercruces@maquina1:~$ lsblk -f 
NAME    FSTYPE FSVER LABEL UUID                                 FSAVAIL FSUSE% MOUNTPOINTS
vda                                                                            
├─vda1  ext4   1.0         662371ca-2a9b-4721-99dc-a351b6772a95    7.5G    18% /
├─vda14                                                                        
└─vda15 vfat   FAT16       490A-A94F                             112.2M     9% /boot/efi
vdb                                                                            
└─vdb1  ext4   1.0         bd712ece-3a04-4436-9e3d-7c04851250bb    1.8G     0% /mnt
javiercruces@maquina1:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            210M     0  210M   0% /dev
tmpfs            46M  588K   46M   2% /run
/dev/vda1       9.7G  1.8G  7.5G  20% /
tmpfs           229M     0  229M   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
/dev/vda15      124M   12M  113M  10% /boot/efi
tmpfs            46M     0   46M   0% /run/user/1000
/dev/vdb1       2.0G   24K  1.9G   1% /mnt
javiercruces@maquina1:~$ 


```

##  4.Comando OSC para crear un volumen arrancable con una imagen.

```bash
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack volume create --image 017ae8f0-114e-4770-9df9-7e8b8f24199d --size 10 --bootable taller2_boot        
+---------------------+------------------------------------------------------------------+
| Field               | Value                                                            |
+---------------------+------------------------------------------------------------------+
| attachments         | []                                                               |
| availability_zone   | nova                                                             |
| bootable            | false                                                            |
| consistencygroup_id | None                                                             |
| created_at          | 2023-12-11T09:46:12.905923                                       |
| description         | None                                                             |
| encrypted           | False                                                            |
| id                  | 8707e596-5dd2-40f7-81b8-f14cd57e5ab9                             |
| multiattach         | False                                                            |
| name                | taller2_boot                                                     |
| properties          |                                                                  |
| replication_status  | None                                                             |
| size                | 10                                                               |
| snapshot_id         | None                                                             |
| source_volid        | None                                                             |
| status              | creating                                                         |
| type                | __DEFAULT__                                                      |
| updated_at          | None                                                             |
| user_id             | dfda906ffa44103a62ca25d3b6a90d37da5d36db34fd772a636cccd1d7bc5cea |
+---------------------+------------------------------------------------------------------+

```

##  5.Comando OSC para crear una instancia cuyo disco es el volumen.

```bash
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack server create --flavor vol.normal  --volume 8707e596-5dd2-40f7-81b8-f14cd57e5ab9 --key-name jcruces  taller2_vol_boot 
+-----------------------------+------------------------------------------------------------------+
| Field                       | Value                                                            |
+-----------------------------+------------------------------------------------------------------+
| OS-DCF:diskConfig           | MANUAL                                                           |
| OS-EXT-AZ:availability_zone |                                                                  |
| OS-EXT-STS:power_state      | NOSTATE                                                          |
| OS-EXT-STS:task_state       | scheduling                                                       |
| OS-EXT-STS:vm_state         | building                                                         |
| OS-SRV-USG:launched_at      | None                                                             |
| OS-SRV-USG:terminated_at    | None                                                             |
| accessIPv4                  |                                                                  |
| accessIPv6                  |                                                                  |
| addresses                   |                                                                  |
| adminPass                   | 4dUPoNF6LYcE                                                     |
| config_drive                |                                                                  |
| created                     | 2023-12-11T09:57:21Z                                             |
| flavor                      | vol.normal (9)                                                   |
| hostId                      |                                                                  |
| id                          | 3720614d-e4a8-45b7-839b-baf20be0898d                             |
| image                       | N/A (booted from volume)                                         |
| key_name                    | jcruces                                                          |
| name                        | taller2_vol_boot                                                 |
| progress                    | 0                                                                |
| project_id                  | 83eb5116df714c9b86735f43b85146e9                                 |
| properties                  |                                                                  |
| security_groups             | name='default'                                                   |
| status                      | BUILD                                                            |
| updated                     | 2023-12-11T09:57:21Z                                             |
| user_id                     | dfda906ffa44103a62ca25d3b6a90d37da5d36db34fd772a636cccd1d7bc5cea |
| volumes_attached            |                                                                  |
+-----------------------------+------------------------------------------------------------------+
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ 

(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack floating ip create ext-net
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack server add floating ip  taller2_vol_boot 172.22.200.60


```

##  6.Comprobación de que el servidor web sigue funcionando después de eliminar la instancia y volver a crear una instancia con el mismo volumen.

```bash
(os) javiercruces@HPOMEN15:~$ openstack server delete taller2_vol_boot
(os) javiercruces@HPOMEN15:~$ openstack server create --flavor vol.normal  --volume 8707e596-5dd2-40f7-81b8-f14cd57e5ab9 --key-name jcruces  taller2_vol_boot 
(os) javiercruces@HPOMEN15:~$ openstack server add floating ip  taller2_vol_boot 172.22.200.60
debian@taller2-vol-boot:~$ systemctl status nginx.service 
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; preset: enabled)
     Active: active (running) since Mon 2023-12-11 10:02:34 UTC; 29s ago
       Docs: man:nginx(8)
    Process: 427 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
    Process: 433 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
   Main PID: 434 (nginx)
      Tasks: 2 (limit: 1107)
     Memory: 2.9M
        CPU: 14ms
     CGroup: /system.slice/nginx.service
             ├─434 "nginx: master process /usr/sbin/nginx -g daemon on; master_process on;"
             └─435 "nginx: worker process"

Dec 11 10:02:34 taller2-vol-boot systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...
Dec 11 10:02:34 taller2-vol-boot systemd[1]: Started nginx.service - A high performance web server and a reverse proxy server.
debian@taller2-vol-boot:~$ 


```