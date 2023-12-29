---
title: "Trabajo con instancias en OpenStack "
date: 2023-09-08T10:00:00+00:00
description: Trabajo con instancias en OpenStack 
tags: [OpenStack, CloudComputing, Instancias, OpenStackCLI, ServiciosEnLaNube, NAT, almacenamiento, LVM, volumenes]
hero: images/openstack/taller1/taller1.png
---

<!-- https://fp.josedomingo.org/sri/5_iaas/taller1.html -->

Este taller se centra en la administración de instancias en OpenStack. Aprenderás a configurar el cliente de OpenStack, gestionar imágenes y crear instancias .

Puedes encontrar apuntes de este post en la pagina web de mi profesor Jose Domingo https://github.com/josedom24/curso_openstack_ies .

# Taller 1: Trabajo con instancias en OpenStack

2.Muestra las claves públicas que tienes en tu proyecto OpenStack.

```bash
(os) javiercruces@HPOMEN15:~$ openstack keypair list
+---------+-------------------------------------------------+------+
| Name    | Fingerprint                                     | Type |
+---------+-------------------------------------------------+------+
| jcruces | e9:6f:9b:4d:72:a4:a3:04:2f:0f:9c:dd:3d:6f:35:7f | ssh  |
+---------+-------------------------------------------------+------+
(os) javiercruces@HPOMEN15:~$ 

```

3.Muestra las reglas del grupo de seguridad Default.

```bash
(os) javiercruces@HPOMEN15:~$ openstack security group show default
| Field           | Value                                                                                            |
+-----------------+--------------------------------------------------------------------------------------------------+
| created_at      | 2023-09-27T10:47:07Z                                                                             |
| description     | Default security group                                                                           |
| id              | d4455846-8c8d-47c1-b66f-94796fc4576b                                                             |
| name            | default                                                                                          |
| project_id      | 83eb5116df714c9b86735f43b85146e9                                                                 |
| revision_number | 7                                                                                                |
| rules           | created_at='2023-10-09T07:20:01Z', direction='egress', ethertype='IPv4',                         |
|                 | id='07bfe77e-1425-442d-a341-8c52f89e5f0a', normalized_cidr='0.0.0.0/0', protocol='udp',          |
|                 | remote_ip_prefix='0.0.0.0/0', standard_attr_id='8193',                                           |
|                 | tenant_id='83eb5116df714c9b86735f43b85146e9', updated_at='2023-10-09T07:20:01Z'                  |
|                 | created_at='2023-09-27T10:47:07Z', direction='ingress', ethertype='IPv6',                        |
|                 | id='0f9a50d5-b14b-4119-ba7d-c13961599fa8',                                                       |
|                 | remote_group_id='d4455846-8c8d-47c1-b66f-94796fc4576b', standard_attr_id='7931',                 |
|                 | tenant_id='83eb5116df714c9b86735f43b85146e9', updated_at='2023-09-27T10:47:07Z'                  |
|                 | created_at='2023-09-27T10:47:07Z', direction='egress', ethertype='IPv4',                         |
|                 | id='241cb45a-f37e-4061-9980-a526cf1860fa', standard_attr_id='7930',                              |
|                 | tenant_id='83eb5116df714c9b86735f43b85146e9', updated_at='2023-09-27T10:47:07Z'                  |
|                 | created_at='2023-10-09T07:20:17Z', direction='ingress', ethertype='IPv4',                        |
|                 | id='259e6cf6-fc4a-47c5-a8a5-68974c5f5709', normalized_cidr='0.0.0.0/0', protocol='icmp',         |
|                 | remote_ip_prefix='0.0.0.0/0', standard_attr_id='8194',                                           |
|                 | tenant_id='83eb5116df714c9b86735f43b85146e9', updated_at='2023-10-09T07:20:17Z'                  |
|                 | created_at='2023-10-09T07:35:44Z', direction='egress', ethertype='IPv4',                         |
|                 | id='2cdcb2d0-0061-484b-8ca1-6d618abaee0f', normalized_cidr='0.0.0.0/0', protocol='tcp',          |
|                 | remote_ip_prefix='0.0.0.0/0', standard_attr_id='8196',                                           |
|                 | tenant_id='83eb5116df714c9b86735f43b85146e9', updated_at='2023-10-09T07:35:44Z'                  |
|                 | created_at='2023-10-09T07:19:52Z', direction='ingress', ethertype='IPv4',                        |
|                 | id='59b4770e-2dde-4b73-924b-1a040ca501d1', normalized_cidr='0.0.0.0/0', protocol='udp',          |
|                 | remote_ip_prefix='0.0.0.0/0', standard_attr_id='8192',                                           |
|                 | tenant_id='83eb5116df714c9b86735f43b85146e9', updated_at='2023-10-09T07:19:52Z'                  |
|                 | created_at='2023-10-09T07:19:42Z', direction='ingress', ethertype='IPv4',                        |
|                 | id='8cf43fcd-6900-45b3-9980-bf75dac82713', normalized_cidr='0.0.0.0/0', protocol='tcp',          |
|                 | remote_ip_prefix='0.0.0.0/0', standard_attr_id='8191',                                           |
|                 | tenant_id='83eb5116df714c9b86735f43b85146e9', updated_at='2023-10-09T07:19:42Z'                  |
|                 | created_at='2023-10-09T07:20:24Z', direction='egress', ethertype='IPv4',                         |
|                 | id='9719ad62-a7b6-48b8-908b-20a0a7e46777', normalized_cidr='0.0.0.0/0', protocol='icmp',         |
|                 | remote_ip_prefix='0.0.0.0/0', standard_attr_id='8195',                                           |
|                 | tenant_id='83eb5116df714c9b86735f43b85146e9', updated_at='2023-10-09T07:20:24Z'                  |
|                 | created_at='2023-09-27T10:47:07Z', direction='egress', ethertype='IPv6',                         |
|                 | id='9acf5066-e3c7-4f80-a38d-88d5a2f061de', standard_attr_id='7932',                              |
|                 | tenant_id='83eb5116df714c9b86735f43b85146e9', updated_at='2023-09-27T10:47:07Z'                  |
|                 | created_at='2023-09-27T10:47:07Z', direction='ingress', ethertype='IPv4',                        |
|                 | id='9e1a0436-0e85-44d8-ba63-a519c6cf5cc0',                                                       |
|                 | remote_group_id='d4455846-8c8d-47c1-b66f-94796fc4576b', standard_attr_id='7929',                 |
|                 | tenant_id='83eb5116df714c9b86735f43b85146e9', updated_at='2023-09-27T10:47:07Z'                  |
| shared          | False                                                                                            |
| stateful        | True                                                                                             |
| tags            | []                                                                                               |
| updated_at      | 2023-10-09T07:35:44Z                                                                             |
+-----------------+--------------------------------------------------------------------------------------------------+

```

4.Abre el puerto 443 en el grupo de seguridad Default.

```bash
(os) javiercruces@HPOMEN15:~$ openstack security group rule create --proto tcp --dst-port 443 default
+-------------------------+--------------------------------------+
| Field                   | Value                                |
+-------------------------+--------------------------------------+
| created_at              | 2023-12-05T11:08:12Z                 |
| description             |                                      |
| direction               | ingress                              |
| ether_type              | IPv4                                 |
| id                      | 12b08b49-8c7c-4361-922e-680a06610667 |
| name                    | None                                 |
| normalized_cidr         | 0.0.0.0/0                            |
| port_range_max          | 443                                  |
| port_range_min          | 443                                  |
| project_id              | 83eb5116df714c9b86735f43b85146e9     |
| protocol                | tcp                                  |
| remote_address_group_id | None                                 |
| remote_group_id         | None                                 |
| remote_ip_prefix        | 0.0.0.0/0                            |
| revision_number         | 0                                    |
| security_group_id       | d4455846-8c8d-47c1-b66f-94796fc4576b |
| tags                    | []                                   |
| tenant_id               | 83eb5116df714c9b86735f43b85146e9     |
| updated_at              | 2023-12-05T11:08:12Z                 |
+-------------------------+--------------------------------------+
(os) javiercruces@HPOMEN15:~$ 

```

5.CirrOS es una distribución mínima de Linux que fue diseñada para su uso como imagen de prueba en nubes como OpenStack. Sube a tu proyecto la imagen de CirrOS que puedes encontrar aquí. Lista las imágenes a las que tienes acceso.

```bash
(os) javiercruces@HPOMEN15:~$ openstack image create --container-format bare --disk-format qcow2 --file Descargas/cirros-0.5.1-x86_64-disk.img "Cirros_fjcd"
+------------------+-------------------------------------------------------------------------------------------------+
| Field            | Value                                                                                           |
+------------------+-------------------------------------------------------------------------------------------------+
| container_format | bare                                                                                            |
| created_at       | 2023-12-05T11:12:42Z                                                                            |
| disk_format      | qcow2                                                                                           |
| file             | /v2/images/95523522-0747-40b8-b1ba-bd989b164f18/file                                            |
| id               | 95523522-0747-40b8-b1ba-bd989b164f18                                                            |
| min_disk         | 0                                                                                               |
| min_ram          | 0                                                                                               |
| name             | Cirros_fjcd                                                                                     |
| owner            | 83eb5116df714c9b86735f43b85146e9                                                                |
| properties       | os_hidden='False', owner_specified.openstack.md5='',                                            |
|                  | owner_specified.openstack.object='images/Cirros_fjcd', owner_specified.openstack.sha256=''      |
| protected        | False                                                                                           |
| schema           | /v2/schemas/image                                                                               |
| status           | queued                                                                                          |
| tags             |                                                                                                 |
| updated_at       | 2023-12-05T11:12:42Z                                                                            |
| visibility       | shared                                                                                          |
+------------------+-------------------------------------------------------------------------------------------------+
(os) javiercruces@HPOMEN15:~$ openstack image list
+--------------------------------------+--------------------------+--------+
| ID                                   | Name                     | Status |
+--------------------------------------+--------------------------+--------+
| cd347dce-b664-4965-b56e-415507ceafe2 | CentOS Stream 8          | active |
| 2be93f63-b473-4053-b0e8-600216a73e90 | Cirros 0.5.1             | active |
| ff94c268-b5b2-4b83-8f4f-a7368eef70aa | Cirros 0.5.1             | active |
| 95523522-0747-40b8-b1ba-bd989b164f18 | Cirros_fjcd              | active |
| c65ff8de-e77c-445a-923d-8387570df921 | Debian 11 Bullseye       | active |
| 017ae8f0-114e-4770-9df9-7e8b8f24199d | Debian 12 Bookworm       | active |
| 042065bf-6c32-4b9d-bc76-0c1bc9763a1e | FJCD-OpenVasKali         | active |
| 693f9c02-bbe9-49b1-8769-70b37a71b6ab | FJCD_Masashi             | active |
| 257f8df7-f080-4bb8-8cb4-52e73538999f | Fedora 36                | active |
| 0bdce56c-63e0-4783-b4fa-6ba0b0e7b70b | OpenSuse 15.2            | active |
| 7882dd19-9ac4-4a51-ac20-689e9c8a5d2f | Rocky Linux 9            | active |
| 3e814151-1fc8-4f88-838c-d07479665f8d | Ubuntu 20.04 Focal       | active |
| 597c887b-e1a5-4ba8-9c70-663bcce294f3 | Ubuntu 22.04 Jammy       | active |
| 01bca358-08f1-4b87-aa18-3bef9e816c5f | Windows 2019 Server      | active |
| 95f14708-b55d-4d6d-8f77-30ff25b06d07 | Windows 2019 Server Core | active |
| fb588b58-522d-46a7-82bb-c1753655ebde | exaiso                   | active |
| 0acd31ab-0aaa-4857-88c1-da913b471d59 | imagen-practicas-redes   | active |
| 69c01b9e-7dea-41e2-b899-8ff0903d5b96 | lvm-SISTEMAS             | active |
| 3281ddd8-1534-4488-ae35-cea352d8e4ac | metaexploit              | active |
+--------------------------------------+--------------------------+--------+
(os) javiercruces@HPOMEN15:~$ 


```

6.Lista los sabores que podemos usar para crear una instancia.

```bash
(os) javiercruces@HPOMEN15:~$ openstack flavor list
+----+------------+------+------+-----------+-------+-----------+
| ID | Name       |  RAM | Disk | Ephemeral | VCPUs | Is Public |
+----+------------+------+------+-----------+-------+-----------+
| 1  | m1.nano    |  128 |   10 |         0 |     1 | True      |
| 10 | vol.medium | 2048 |    0 |         0 |     2 | True      |
| 11 | vol.large  | 4096 |    0 |         0 |     2 | True      |
| 12 | vol.xlarge | 8192 |    0 |         0 |     4 | True      |
| 13 | win.normal | 1024 |   20 |        10 |     1 | True      |
| 14 | win.medium | 2048 |   20 |        10 |     1 | True      |
| 15 | win.large  | 4096 |   20 |        10 |     2 | True      |
| 2  | m1.micro   |  256 |   10 |         0 |     1 | True      |
| 3  | m1.mini    |  512 |   10 |         0 |     1 | True      |
| 4  | m1.normal  | 1024 |   10 |         0 |     2 | True      |
| 5  | m1.medium  | 2048 |   20 |         0 |     2 | True      |
| 6  | m1.large   | 4096 |   20 |         0 |     2 | True      |
| 7  | m1.xlarge  | 8192 |   20 |         0 |     4 | True      |
| 8  | vol.mini   |  512 |    0 |         0 |     1 | True      |
| 9  | vol.normal | 1024 |    0 |         0 |     1 | True      |
+----+------------+------+------+-----------+-------+-----------+
(os) javiercruces@HPOMEN15:~$ 

```

7.Crea una instancias Linux, con las siguientes características configuradas con cloud-init:
Al iniciarse se deben actualizar los paquetes.
Se debe instalar Apache2.
Se debe crear un usuario (con tu nombre) y contraseña.
Se debe configurar el fqdn a maquina1.example.org.

```bash
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack server create --flavor 3 --image 017ae8f0-114e-4770-9df9-7e8b8f24199d --key-name jcruces --user-data cloud-init-config.yaml --security-group default taller1_op
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
| adminPass                   | BdL5oS7BLfqD                                                     |
| config_drive                |                                                                  |
| created                     | 2023-12-05T11:33:55Z                                             |
| flavor                      | m1.mini (3)                                                      |
| hostId                      |                                                                  |
| id                          | fee7ec1f-632e-452d-8e90-3faab99ddb2c                             |
| image                       | Debian 12 Bookworm (017ae8f0-114e-4770-9df9-7e8b8f24199d)        |
| key_name                    | jcruces                                                          |
| name                        | taller1_op                                                       |
| progress                    | 0                                                                |
| project_id                  | 83eb5116df714c9b86735f43b85146e9                                 |
| properties                  |                                                                  |
| security_groups             | name='d4455846-8c8d-47c1-b66f-94796fc4576b'                      |
| status                      | BUILD                                                            |
| updated                     | 2023-12-05T11:33:55Z                                             |
| user_id                     | dfda906ffa44103a62ca25d3b6a90d37da5d36db34fd772a636cccd1d7bc5cea |
| volumes_attached            |                                                                  |
+-----------------------------+------------------------------------------------------------------+
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack server add floating ip taller1_op 172.22.201.224



```

8.Muestra tus ips flotantes. Solicita una nueva y asígnala a la instancia.

```bash
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack floating ip create ext-net
+---------------------+--------------------------------------+
| Field               | Value                                |
+---------------------+--------------------------------------+
| created_at          | 2023-12-05T11:22:17Z                 |
| description         |                                      |
| dns_domain          | None                                 |
| dns_name            | None                                 |
| fixed_ip_address    | None                                 |
| floating_ip_address | 172.22.201.224                       |
| floating_network_id | 2ebd4d15-00e3-44c6-a9a7-aeebef5f6540 |
| id                  | 0d9f9510-bc4b-41ab-bf2a-88136715dc67 |
| name                | 172.22.201.224                       |
| port_details        | None                                 |
| port_id             | None                                 |
| project_id          | 83eb5116df714c9b86735f43b85146e9     |
| qos_policy_id       | None                                 |
| revision_number     | 0                                    |
| router_id           | None                                 |
| status              | DOWN                                 |
| subnet_id           | None                                 |
| tags                | []                                   |
| tenant_id           | 83eb5116df714c9b86735f43b85146e9     |
| updated_at          | 2023-12-05T11:22:17Z                 |
+---------------------+--------------------------------------+
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack server add floating ip taller1_op 172.22.201.224

(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ cat cloud-init-config.yaml 
#cloud-config

package_upgrade: true

packages:
  - apache2

users:
  - name: javiercruces
    lock_passwd: false
    passwd: $6$OmzQBNDo.VzQ6d3B$Q0c.FeToLuBo/TRYFhpx.wjM9CsMA392ntCFCCU6Acx5pFR7DCrlxIJhqMUeUsvfFZhCzgT1/fGeOwtgoNo3e1
    ssh-authorized-keys:
      - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC7D77owxzTExSK+jymXOYGUn5GrjB1SPvOh8lJHM29W0KViIFJzumfHFvwfGPcDgVR8DyrZYHTWAmyH2E19Sw5XPV0nMORF8pfakkTOXUkTtYfsajFgehHP7W8NoZAs/4zwyCJuhQwZBRhDSBzNbZrbuMHaBVfnM4dHOgAhJOkvZOejLtmQIGILjNMN7glFEmzY7qswb94/O6R9AOOaThO+2JB+C3ouzSc41rD8xqhEsszjCjjzZXuU5UsMV2XrayQuS8M5A0NwQiIY6VMvzLDuIzIGF+mw8zASy0AOvlm22TJogMr7dA5c/2NSXn3FMKr6YbEeiRgl/iFx/egDymotgML7T6VltivthsHz9HznVFF/mklip8y0EBbbPhygrWrLp3/dJHtNA6eVBkQnwOXzHE/y+3wcX6SuHd63AVtcstdGNn6OZp5eJdIGE5e39YsSwCcc0qTG1bjWLp8ZHr3/z40/ejPCpqtVyeKgLHpi05yveMmYPELXyVvsNdq1ZhaiwqJSDcIHUJ0B60SQPqsMNWH1X/TvpeCgcWriCETTw4WVv5SJMoochUJS1siLbPr1S1vu1uH1a9B63rT+zfIAMdoEPr2IUG9JWbKmrQAvTs3rJkkT9VAh6mzoUoILwSK77F8I5Riainm5XhZnx/8PKtvVyuAlmTV6uuw5jZqAw== javierasping@gmail.com
fqdn: maquina1.javiercd.org
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ 


```

9.Accede por ssh a la instancia que has creado.

```bash
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ ssh 172.22.201.224
The authenticity of host '172.22.201.224 (172.22.201.224)' can't be established.
ED25519 key fingerprint is SHA256:dhOi9PufNBxRWAjYYXM8zd/o6fx37wTmMWXXyV/vqg0.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '172.22.201.224' (ED25519) to the list of known hosts.
Linux maquina1 6.1.0-12-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.52-1 (2023-09-07) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
javiercruces@maquina1:~$ 

```

10.Lista todas las instancias que tienes creada, y elimina la que has creado en el punto 7.

```bash
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ openstack server list
+----------------------+----------------------+--------+----------------------+-------------------------+-----------+
| ID                   | Name                 | Status | Networks             | Image                   | Flavor    |
+----------------------+----------------------+--------+----------------------+-------------------------+-----------+
| 7348b137-b7de-4b99-  | taller1_op           | ACTIVE | red de javier.cruces | Debian 12 Bookworm      | m1.mini   |
| a3f3-c22d9df543de    |                      |        | =10.0.0.122,         |                         |           |
|                      |                      |        | 172.22.201.224       |                         |           |
| 8fdf45f6-df38-4a3c-  | Examen_SRI_HTTP_FJCD | ACTIVE | red de javier.cruces | N/A (booted from        | m1.medium |
| 922e-42c9e709cafb    |                      |        | =10.0.0.57,          | volume)                 |           |
|                      |                      |        | 172.22.201.238       |                         |           |
| 93bebd01-6726-4c22-  | CentOS8-fjcd         | ACTIVE | red de javier.cruces | CentOS Stream 8         | m1.normal |
| a509-a29b98dd9847    |                      |        | =10.0.0.105,         |                         |           |
|                      |                      |        | 172.22.201.164       |                         |           |
| f4f2c1a0-ee82-458a-  | taller-ansible-fjcd- | ACTIVE | red de javier.cruces | N/A (booted from        | m1.normal |
| 98b2-b2db7c30b17c    | bbdd                 |        | =10.0.0.53,          | volume)                 |           |
|                      |                      |        | 172.22.200.27        |                         |           |
| 5b3bba36-47fd-4308-  | taller-ansible-fjcd  | ACTIVE | red de javier.cruces | Debian 12 Bookworm      | m1.normal |
| 8af5-57f9bcb9103d    |                      |        | =10.0.0.47,          |                         |           |
|                      |                      |        | 172.22.200.152       |                         |           |
| 0f928664-3766-4a12-  | transformacion-fjcd  | ACTIVE | red de javier.cruces | N/A (booted from        | m1.normal |
| 81f2-842ae3619ae8    |                      |        | =10.0.0.22,          | volume)                 |           |
|                      |                      |        | 172.22.200.164       |                         |           |
+----------------------+----------------------+--------+----------------------+-------------------------+-----------+
(os) javiercruces@HPOMEN15:~/Documentos/2ºASIR/SRI/openstack$ 

```