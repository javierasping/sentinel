---
title: "Implementation of a perimeter firewall with Nftables II"
date: 2024-03-28T10:00:00+00:00
Description: Implementation of a perimeter firewall with Nftables II
tags: [FIREWALL,LINUX,DEBIAN,NFTABLES]
hero: /images/cortafuegos/nftables2.png
---




On the stage created in the service module with the Odin (Router), Hela (DMZ), Loki and Thor (LAN) machines and using nftables, it sets up a perimeter firewall on the Odin machine so that the stage continues to function completely taking into account the following points:

 • The creation of different chains for each traffic flow (from LAN to the outside, from LAN to DMZ, etc.) will be valued.
 • Default DROP policy for all chains.
 • You can use the extensions that we create appropriate, but at least you should follow the connection when necessary.
 • We must implement the firewall to work after a machine reboot.
 • You must show proof of operation of all rules.

In order not to make the practice too long, I will show you the hits of the rules at the end, as well as the complete script of the rules. Since I will only put in every exercise the rules that intervene and a check of it.

### Ride the stage with Nftables

I'm gonna remove iptables and we're gonna move on to Nfables so we don't lose any stage functionality.

The first thing is to create the tables and chains:

```bash
javiercruces@odin:~$ sudo nft add table inet filter

javiercruces@odin:~$ sudo nft add chain inet filter input { type filter hook input priority 0 \; counter \; policy accept \; }
javiercruces@odin:~$ sudo nft add chain inet filter output { type filter hook output priority 0 \; counter \; policy accept \; }
javiercruces@odin:~$ sudo nft add chain inet filter WAN_LAN { type filter hook forward priority 0\; counter \; policy accept \;}
javiercruces@odin:~$ sudo nft add chain inet filter WAN_DMZ { type filter hook forward priority 0\; counter \; policy accept \;}
javiercruces@odin:~$ sudo nft add chain inet filter LAN_WAN { type filter hook forward priority 0\; counter \; policy accept \;}
javiercruces@odin:~$ sudo nft add chain inet filter LAN_DMZ { type filter hook forward priority 0\; counter \; policy accept \;}
javiercruces@odin:~$ sudo nft add chain inet filter DMZ_LAN { type filter hook forward priority 0\; counter \; policy accept \;}
javiercruces@odin:~$ sudo nft add chain inet filter DMZ_WAN { type filter hook forward priority 0\; counter \; policy accept \;}
```

So would our chains created:

```bash
javiercruces@odin:~$ sudo nft list chains
table inet filter {
	chain input {
		type filter hook input priority filter; policy accept;
	}
	chain output {
		type filter hook output priority filter; policy accept;
	}
	chain WAN_LAN {
		type filter hook forward priority filter; policy accept;
	}
	chain WAN_DMZ {
		type filter hook forward priority filter; policy accept;
	}
	chain LAN_WAN {
		type filter hook forward priority filter; policy accept;
	}
	chain DMZ_LAN {
		type filter hook forward priority filter; policy accept;
	}
	chain LAN_DMZ {
		type filter hook forward priority filter; policy accept;
	}
	chain DMZ_WAN {
		type filter hook forward priority filter; policy accept;
	}
}
```

The LAN network corresponds to the network of the containers 192.168.0.0 / 24.
The DMZ network corresponds to the helium network 172.16.0.0 / 16.


We continue to create the NAT table to be able to configure the SNAT and the DNAT, since these are usually a small number of rules I will not create different chains:

```bash
#Creamos la tabla NAT
javiercruces@odin:~$ sudo nft add table nat

#Cadena para el DNAT
javiercruces@odin:~$ sudo nft add chain nat prerouting { type nat hook prerouting priority 0 \; }

#Cadena para el SNAT
javiercruces@odin:~$ sudo nft add chain nat postrouting { type nat hook postrouting priority 100 \; }
```

## # SNAT rules

Once this is done I will create the rules of SNAT so that our customers can go online on the LAN and DMZ network:

My network card that's facing the outside is the ens4.

```bash
#Regla SNAT para LAN
sudo nft add rule ip nat postrouting oifname "ens4" ip saddr 192.168.0.0/24 counter masquerade
#Regla SNAT para DMZ
sudo nft add rule ip nat postrouting oifname "ens4" iffname "ens3" ip saddr 172.16.0.0/16 counter masquerade

sudo nft add rule ip nat postrouting oifname "ens4" ip saddr 192.168.0.0/24 counter snat to 172.22.200.47
sudo nft add rule ip nat postrouting oifname "ens4" ip saddr 172.16.0.0/16 counter snat to 172.22.200.47

```

Let's check that customers already have access to the Internet, currently the default policy is ACCEPT.


Check for SNAT in Hela:

```bash
[javiercruces@hela ~]$ ping www.javiercd.es -c 1
PING javierasping.github.io (185.199.109.153) 56(84) bytes of data.
64 bytes from cdn-185-199-109-153.github.com (185.199.109.153): icmp_seq=1 ttl=51 time=39.4 ms

--- javierasping.github.io ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 39.439/39.439/39.439/0.000 ms
```

Verification of SNAT in Thor:

```bash
javiercruces@thor:~$ ping www.javiercd.es -c 1
PING javierasping.github.io (185.199.108.153) 56(84) bytes of data.
64 bytes from cdn-185-199-108-153.github.com (185.199.108.153): icmp_seq=1 ttl=51 time=38.1 ms

--- javierasping.github.io ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 38.138/38.138/38.138/0.000 ms

```

Verification of SNAT in Loki:

```bash
javiercruces@loki:~$ ping www.javiercd.es -c 1
PING javierasping.github.io (185.199.111.153) 56(84) bytes of data.
64 bytes from cdn-185-199-111-153.github.com (185.199.111.153): icmp_seq=1 ttl=51 time=37.7 ms

--- javierasping.github.io ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 37.667/37.667/37.667/0.000 ms
```

Finally we will make sure that the rule receives hits:

```bash
javiercruces@odin:~$ sudo nft list ruleset
#Salida del comando recortada
	chain postrouting {
		type nat hook postrouting priority srcnat; policy accept;
		oifname "ens4" ip saddr 172.16.0.0/16 counter packets 11 bytes 868 masquerade
		oifname "ens4" ip saddr 192.168.0.0/24 counter packets 122 bytes 10594 masquerade
	}
}
```

## # DNAT rules

The previous rules we had were as follows:

```bash
javiercruces@odin:~$ sudo iptables -L -t nat
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination         
DNAT       tcp  --  anywhere             anywhere             tcp dpt:http to:172.16.0.200
DNAT       udp  --  anywhere             anywhere             udp dpt:domain to:192.168.0.2
DNAT       tcp  --  anywhere             anywhere             tcp dpt:smtp to:192.168.0.3
DNAT       tcp  --  anywhere             anywhere             tcp dpt:mysql to:192.168.0.3
```

So let's move them to nftables:

```bash
#Para un wordpress que hay en hela
sudo nft add rule ip nat prerouting tcp dport 80 counter dnat to 172.16.0.200

#Para hacer consultas DNS a thor
sudo nft add rule ip nat prerouting udp dport 53 counter dnat to 192.168.0.2

#Para poder recibir correos en loki
sudo nft add rule ip nat prerouting tcp dport 25 counter dnat to 192.168.0.3

#Para acceder desde fuera a un mysql que hay en loki
sudo nft add rule ip nat prerouting tcp dport 3306 counter dnat to 192.168.0.3
```

Now let's add a series of rules to allow the previous traffic and the rest of the stage preparation:

```bash
#PERMITIR USO DE ODIN

##Permitir consultas DNS de odin a thor (DNSSERVER)
sudo nft add rule inet filter output oifname "br-intra2" udp dport 53 counter accept
sudo nft add rule inet filter input iifname "br-intra2" udp sport 53 counter accept

##Permitir tráfico HTTP y HTTPS en odin
sudo nft add rule inet filter output oifname "ens4" ip protocol tcp tcp dport { 80,443 } ct state new,established counter accept
sudo nft add rule inet filter input iifname "ens4" ip protocol tcp tcp sport { 80,443 } ct state established counter accept

#Permitir conexiones SSH por el puerto 2222
sudo nft add rule ip nat prerouting iifname "ens4" tcp dport 2222 counter dnat to 192.168.0.1:22
sudo nft add rule inet filter output oifname "ens4" tcp sport 22 ct state established counter accept
sudo nft add rule inet filter input iifname "ens4" tcp dport 22 ct state new,established counter accept

#Permitir conexiones SSH de odin a hela
sudo nft add rule inet filter output oifname "ens3" ip daddr 172.16.0.0/16 tcp dport 22 counter accept
sudo nft add rule inet filter input iifname "ens3" ip saddr 172.16.0.0/16 tcp sport 22 ct state established,related counter accept

#Permitir conexiones ssh de odin a thor y loki
sudo nft add rule inet filter output oifname "br-intra2" ip daddr 192.168.0.0/24 tcp dport 22 counter accept
sudo nft add rule inet filter input iifname "br-intra2" ip saddr 192.168.0.0/24 tcp sport 22 ct state established,related counter accept

#Reglas perimetrales

##Permitir consultas DNS desde br-intra hacia ens4 , necesario para el forward del dns (ESTA REGLA SOLO ME FUNCIONA SI ESTA EN LA MISMA CADENA)
#sudo nft add rule inet filter DMZ_WAN iifname "br-intra2" oifname "ens4" udp dport 53 counter accept
#sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "br-intra2" udp sport 53 counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens4" udp dport 53 counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "br-intra2" udp sport 53 counter accept


##Permitir consultas dns desde LAN a DMZ (hela --> thor) (ESTA REGLA SOLO ME FUNCIONA SI ESTA EN LA MISMA CADENA)
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" udp dport 53 counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" udp sport 53 counter accept

sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" udp dport 53 counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" udp sport 53 counter accept


##Reglas para permitir trafico a wordpress en hela
sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { new, established } counter accept
sudo nft add rule inet filter DMZ_WAN iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter accept

#Regla para hacer consultas DNS a thor (Permitir DNAT)
sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "br-intra2" ip daddr 192.168.0.2 udp dport 53 ct state new,established counter accept
sudo nft add rule inet filter DMZ_WAN iifname "br-intra2" oifname "ens4" ip saddr 192.168.0.2 udp sport 53 ct state established,related counter accept

#Regla para recibir e enviar correos en loki
sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state new,established counter accept
sudo nft add rule inet filter DMZ_WAN iifname "br-intra2" oifname "ens4" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter accept

#Permitir a hela usar el servidor LDAP
sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" tcp dport 389 counter accept
sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" tcp sport 389 counter accept


```



## Exercises

The firewall must meet at least these rules:

### The Odin machine has a ssh server listening to port 22, but when you access from the outside you will have to connect to port 2222.

To perform this exercise I will do a DNAT to the DMZ interface of odin which is the 192.168.0.1, so I will connect to that interface by ssh. After that we must allow this traffic that goes from the ens4 to the ens3.

```bash
#Permitimos el trafico que ahora "cambiamos" el puerto con la regla DNAT de 2222 a 22 hacia odin
sudo nft add rule inet filter output oifname "ens4" tcp sport 22 ct state established counter accept
sudo nft add rule inet filter input iifname "ens4" tcp dport 22 ct state new,established counter accept
#Regla DNAT
sudo nft add rule ip nat prerouting iifname "ens4" tcp dport 2222 counter dnat to 192.168.0.1:22
```


I will put the default DROP policy once I reach this point:

```bash
sudo nft chain inet filter input { policy drop \; }
sudo nft chain inet filter output { policy drop \; }
sudo nft chain inet filter WAN_LAN { policy drop \; }
sudo nft chain inet filter WAN_DMZ { policy drop \; }
sudo nft chain inet filter LAN_WAN { policy drop \; }
sudo nft chain inet filter DMZ_LAN { policy drop \; }
sudo nft chain inet filter LAN_DMZ { policy drop \; }
sudo nft chain inet filter DMZ_WAN { policy drop \; }
```

And let's check that the connection works by port 2222:

```bash
javiercruces@HPOMEN15:~$ ssh 172.22.200.47 -p 2222
Linux odin.javiercd.gonzalonazareno.org 6.1.0-18-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.76-1 (2024-02-01) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Mar  9 13:49:09 2024 from 172.29.0.58
javiercruces@odin:~$ 
```

We checked the hits in the rules:

```bash
javiercruces@odin:~$ sudo nft list ruleset
#IMPUT
iifname "ens4" tcp dport 22 ct state established,new counter packets 241918 bytes 13788652 accept
#OUTPUT
oifname "ens4" tcp sport 22 ct state established counter packets 355383 bytes 210012030 accept
#DNAT
iifname "ens4" tcp dport 2222 counter packets 5 bytes 300 dnat to 192.168.0.1:22
```

### From Thor and Hela you should allow the ssh connection by port 22 to the Odin machine.

To be able to check these rules I will allow ssh connections from Odin to both DMZ and LAN networks

```bash
#Permitir conexiones ssh de odin a hela
sudo nft add rule inet filter output oifname "ens3" ip daddr 172.16.0.0/16 tcp dport 22 counter accept
sudo nft add rule inet filter input iifname "ens3" ip saddr 172.16.0.0/16 tcp sport 22 ct state established,related counter accept

#Permitir conexiones ssh de odin a thor y loki
sudo nft add rule inet filter output oifname "br-intra2" ip daddr 192.168.0.0/24 tcp dport 22 counter accept
sudo nft add rule inet filter input iifname "br-intra2" ip saddr 192.168.0.0/24 tcp sport 22 ct state established,related counter accept

#Permitir conexion ssh desde hela a odin
sudo nft add rule inet filter input iifname "ens3" ip saddr 172.16.0.200 tcp dport 22 ct state new,established counter accept
sudo nft add rule inet filter output oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 ct state established counter accept

#Permitir conexion ssh desde thor a odin
sudo nft add rule inet filter input iifname "br-intra2" ip saddr 192.168.0.2 tcp dport 22 ct state new,established counter accept
sudo nft add rule inet filter output oifname "br-intra2" ip daddr 192.168.0.2 tcp sport 22 ct state established counter accept
```

Let's check the two above rules by connecting to Odin by ssh from these two customers:

```bash
#Hela --> Odin
javiercruces@odin:~$ ssh 172.16.0.200 -A
Last login: Sat Mar  9 19:02:49 2024 from 172.16.0.1
[javiercruces@hela ~]$ ssh 172.16.0.1
Linux odin.javiercd.gonzalonazareno.org 6.1.0-18-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.76-1 (2024-02-01) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Mar  9 19:49:28 2024 from 192.168.0.2
javiercruces@odin:~$ 

#Thor --> Odin
javiercruces@thor:~$ ssh 192.168.0.1
Linux odin.javiercd.gonzalonazareno.org 6.1.0-18-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.76-1 (2024-02-01) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Mar  9 19:46:12 2024 from 192.168.0.2
javiercruces@odin:~$ 

```

I'll leave you the rule hits at the end of practice.

### The Odin machine must be allowed traffic for the loopback interface.

```bash
sudo nft add rule inet filter input iifname "lo" counter accept    
sudo nft add rule inet filter output oifname "lo" counter accept
```

Check:

```bash
javiercruces@odin:~$ ping 127.0.0.1 -c 1
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.100 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.100/0.100/0.100/0.000 ms

```

### The Odin machine can be ping from the DMZ, but from the LAN the connection (REJECT) must be rejected and from the outside will be rejected silently.

```bash
#DMZ
sudo nft add rule inet filter input iifname "ens4" ip protocol icmp icmp type echo-request counter accept
sudo nft add rule inet filter output oifname "ens4" ip protocol icmp icmp type echo-reply counter accept
#Las siguientes 2 reglas , no funcionaran como esperamos ya que hacen lo mismo que la politica por defecto , ademas no se permite este trafico .
#LAN
sudo nft add rule inet filter input iifname "br-intra2" ip protocol icmp counter reject
#Exterior
sudo nft add rule inet filter input iifname "ens3" ip protocol icmp counter drop
```

Let's check these rules:

```bash
#LAN Thor a odin
javiercruces@thor:~$ ping 192.168.0.1
PING 192.168.0.1 (192.168.0.1) 56(84) bytes of data.
From 192.168.0.1 icmp_seq=1 Destination Port Unreachable

#DMZ , Hela --> Odin
[javiercruces@hela ~]$ ping 172.16.0.1 -c 1
PING 172.16.0.1 (172.16.0.1) 56(84) bytes of data.
64 bytes from 172.16.0.1: icmp_seq=1 ttl=64 time=0.471 ms

--- 172.16.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.471/0.471/0.471/0.000 ms

#Exterior a odin
javiercruces@HPOMEN15:~$ ping 172.22.200.47
PING 172.22.200.47 (172.22.200.47) 56(84) bytes of data.
^C
--- 172.22.200.47 ping statistics ---
419 packets transmitted, 0 received, 100% packet loss, time 428036ms
```

At the end of the practice I'll leave you all the hits of the rules.

### The Odin machine can do ping to the LAN, the DMZ and the outside.

```bash
#PERMITIR PING A DMZ
sudo nft insert rule inet filter output oifname "ens3" icmp type echo-request counter accept
sudo nft insert rule inet filter input iifname "ens3" icmp type echo-reply counter accept

#PERMITIR PING A EXTERIOR
sudo nft insert rule inet filter output oifname "ens4" icmp type echo-request counter accept
sudo nft insert rule inet filter input iifname "ens4" icmp type echo-reply counter accept

#PERMITIR PING A LAN
sudo nft insert rule inet filter output oifname "br-intra2" icmp type echo-request counter accept
sudo nft insert rule inet filter input iifname "br-intra2" icmp type echo-reply counter accept
```

Check:

```bash
javiercruces@odin:~$ ping 8.8.8.8 -c 1
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=116 time=8.70 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 8.701/8.701/8.701/0.000 ms

javiercruces@odin:~$ ping 192.168.0.2 -c 1
PING 192.168.0.2 (192.168.0.2) 56(84) bytes of data.
64 bytes from 192.168.0.2: icmp_seq=1 ttl=64 time=6.030 ms

--- 192.168.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.030/0.030/0.030/0.000 ms

javiercruces@odin:~$ ping 172.16.0.200 -c 1
PING 172.16.0.200 (172.16.0.200) 56(84) bytes of data.
64 bytes from 172.16.0.200: icmp_seq=1 ttl=63 time=59.1 ms

--- 172.16.0.200 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 59.052/59.052/59.052/0.000 ms
```

### From the Hela machine you can make ping and ssh connection to LAN machines.

```bash
##Si no estan en la cadena forward no funciona
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 ip protocol icmp icmp type echo-request counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 ip protocol icmp icmp type echo-reply counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp dport 22 counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 counter accept

sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 ip protocol icmp icmp type echo-request counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 ip protocol icmp icmp type echo-reply counter accept

sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp dport 22 counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 counter accept

```

Check:

```bash
[javiercruces@hela ~]$ ping 192.168.0.2
PING 192.168.0.2 (192.168.0.2) 56(84) bytes of data.
64 bytes from 192.168.0.2: icmp_seq=1 ttl=63 time=0.596 ms
^C
--- 192.168.0.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.596/0.596/0.596/0.000 ms
[javiercruces@hela ~]$ ssh  192.168.0.2
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 6.1.0-18-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
Last login: Sun Mar 10 14:52:57 2024 from 192.168.0.1
javiercruces@thor:~$ 

```

### From any LAN machine you can connect ssh to the hela machine.

```bash
##Si no esta en la cadena forward no funciona
#sudo nft add rule inet filter LAN_DMZ iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 22 counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 22 counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 22 counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 22 counter accept
```

Check:

```bash
javiercruces@thor:~$ ssh 172.16.0.200
Last login: Sun Mar 10 14:53:12 2024 from 192.168.0.2
[javiercruces@hela ~]$ 
```

### Configure the Odin machine so that LAN and DMZ machines can access the outside.

These rules were already indicated.

```bash
sudo nft add rule ip nat postrouting oifname "ens4" ip saddr 192.168.0.0/24 counter masquerade
sudo nft add rule ip nat postrouting oifname "ens4" ip saddr 172.16.0.0/16 counter masquerade
```

### LAN machines can do ping outside and navigate.

```bash
#Las máquinas de la LAN pueden hacer ping al exterior y navegar.
##Si no estan en la cadena forward no funciona
#sudo nft add rule inet filter LAN_WAN iifname "br-intra2" oifname "ens4" ip protocol icmp icmp type echo-request counter accept
#sudo nft add rule inet filter WAN_LAN iifname "ens4" oifname "br-intra2" ip protocol icmp icmp type echo-reply counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens4" ip protocol icmp icmp type echo-request counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "br-intra2" ip protocol icmp icmp type echo-reply counter accept
```

Check:

```bash
javiercruces@thor:~$ curl -I https://www.javiercd.es
HTTP/2 200 
server: GitHub.com
content-type: text/html; charset=utf-8
last-modified: Sat, 02 Mar 2024 10:17:01 GMT
access-control-allow-origin: *
strict-transport-security: max-age=31556952
etag: "65e2fc9d-675b"
expires: Sun, 10 Mar 2024 15:35:43 GMT
cache-control: max-age=600
x-proxy-cache: MISS
x-github-request-id: E24C:3800B1:1881E48:18E9A93:65EDD0F7
accept-ranges: bytes
date: Sun, 10 Mar 2024 19:14:10 GMT
via: 1.1 varnish
age: 60
x-served-by: cache-mad22083-MAD
x-cache: HIT
x-cache-hits: 1
x-timer: S1710098050.166466,VS0,VE2
vary: Accept-Encoding
x-fastly-request-id: 0c6c80bbef19370976aadfc6988441c5a36beccc
content-length: 26459

javiercruces@thor:~$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=110 time=38.5 ms
^C
--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 38.451/38.451/38.451/0.000 ms
```


### The hela machine can sail. Install a web server, a ftp server and a post server if you don't have them yet.

```bash
#La máquina Hela puede navegar. Instala un servidor web, un servidor ftp y un servidor de correos si no los tienes aún.
#Hela ya tiene permitido hacer consultas dns a thor
sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" tcp dport {80, 443} counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" tcp sport {80, 443} counter accept
```

I check that I can navigate:

```bash
[root@hela javiercruces]# curl -I https://www.javiercd.es/
HTTP/2 200 
server: GitHub.com
content-type: text/html; charset=utf-8
last-modified: Sat, 02 Mar 2024 10:17:01 GMT
access-control-allow-origin: *
strict-transport-security: max-age=31556952
etag: "65e2fc9d-675b"
expires: Sun, 10 Mar 2024 15:35:43 GMT
cache-control: max-age=600
x-proxy-cache: MISS
x-github-request-id: E24C:3800B1:1881E48:18E9A93:65EDD0F7
accept-ranges: bytes
date: Sun, 10 Mar 2024 19:13:17 GMT
via: 1.1 varnish
age: 7
x-served-by: cache-mad22067-MAD
x-cache: HIT
x-cache-hits: 1
x-timer: S1710097997.474757,VS0,VE2
vary: Accept-Encoding
x-fastly-request-id: 2d2811893898abf05bebd96c6bd5a09ed7abfe5b
content-length: 26459
```

I understand you want me to install these 3 hela services. On our stage it is the other machines that house these services.

### Configure the Odin machine to make web and ftp services accessible from the outside.

The web server is already previously configured in the migration of the scenario.

```bash
sudo nft add rule ip nat prerouting tcp dport 21 counter dnat to 172.16.0.200
#No funcionan en cadenas separadas
#sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
#sudo nft add rule inet filter DMZ_WAN iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept

sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept
```

### The web server and the ftp server must be accessible from the LAN and from the outside.

The FTP server is on the LAN so it's already accessible, I'm gonna make it accessible from the DMZ. From the outside, both are already accessible.

```bash
##No funcionan las reglass en cadenas separadas
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { new, established } counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter accept

```

Access from DMZ to LAN:

```bash
javiercruces@thor:~$ curl 172.16.0.200
<!DOCTYPE html>

javiercruces@thor:~$ ftp 172.16.0.200
Connected to 172.16.0.200.
220 (vsFTPd 3.0.5)
```

### The post server should only be accessible from the LAN.

We comment on the lines of stage preparation that allow access to the scenario and add:

```bash
#No funciona en cadenas separadas
#sudo nft add rule inet filter DMZ_LAN iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state { new, established } counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter accept

sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter accept

```

Let's access the:

```bash
[root@hela javiercruces]# telnet 192.168.0.3 25
Trying 192.168.0.3...
Connected to 192.168.0.3.
Escape character is '^]'.
220 loki.javiercd.gonzalonazareno.org ESMTP Postfix (Ubuntu)
```

### In the Loki machine you install a Postgres server if you don't have it yet. This server can be accessed from the DMZ, but not from the outside.


```bash
#no funciona en cadenas distintas
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 5432 ct state { new, established } counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 5432 ct state established,related counter accept


sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 5432 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 5432 ct state established,related counter accept
```

We access the postwree server from hela:

```bash
[root@hela javiercruces]# psql -h 192.168.0.3 -U postgres
Password for user postgres: 
psql (13.14, server 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1))
WARNING: psql major version 13, server major version 14.
         Some psql features might not work.
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
Type "help" for help.

postgres=# 
```

## # Avoid DoS attacks by ICMP Flood, limiting the number of requests per second to 4 from the same IP.


```bash
sudo nft insert rule inet filter input icmp type echo-request limit rate 1/second burst 4 packets counter drop
```

If we make a flood attack, this will cut the traffic:

```bash
[root@hela javiercruces]# hping3 --icmp --flood --rand-source 172.16.0.1 
HPING 172.16.0.1 (eth0 172.16.0.1): icmp mode set, 28 headers + 0 data bytes
hping in flood mode, no replies will be shown

icmp type echo-request limit rate 1/second burst 4 packets counter packets 46 bytes 2128 drop

```

Avoid DoS attacks by SYN Flood.

```bash
#Evita ataques DoS por SYN Flood.
sudo nft add rule inet filter input tcp flags \& '(fin|syn|rst|ack) == syn' counter limit rate over 25/second drop
```

If we test the attack:

```bash
[root@hela javiercruces]# hping3  --flood --rand-source 172.16.0.1 
HPING 172.16.0.1 (eth0 172.16.0.1): NO FLAGS are set, 40 headers + 0 data bytes
hping in flood mode, no replies will be shown
^C
--- 172.16.0.1 hping statistic ---
1267916 packets transmitted, 0 packets received, 100% packet loss
round-trip min/avg/max = 0.0/0.0/0.0 ms

icmp type echo-request limit rate 1/second burst 4 packets counter packets 31 bytes 2492 drop
```


## Script with all the rules

I'll leave you here the script I used during practice.

```bash
#Crear estructura de tablas
sudo nft delete table inet filter
sudo nft delete table ip nat

##Añadir tabla filter y sus cadenas
sudo nft add table inet filter
sudo nft add chain inet filter forward { type filter hook forward priority 10\; counter \; policy drop\; }
sudo nft add chain inet filter input { type filter hook input priority 0 \; counter \; policy drop \; }
sudo nft add chain inet filter output { type filter hook output priority 0 \; counter \; policy drop \; }

sudo nft add chain inet filter WAN_LAN { type filter hook forward priority 1\; counter \; policy accept \;}
sudo nft add chain inet filter WAN_DMZ { type filter hook forward priority 2\; counter \; policy accept \;}
sudo nft add chain inet filter LAN_WAN { type filter hook forward priority 3\; counter \; policy accept \;}
sudo nft add chain inet filter LAN_DMZ { type filter hook forward priority 4\; counter \; policy accept \;}
sudo nft add chain inet filter DMZ_LAN { type filter hook forward priority 5\; counter \; policy accept \;}
sudo nft add chain inet filter DMZ_WAN { type filter hook forward priority 6\; counter \; policy accept \;}


##Añadir Tabla NAT y sus cadenas :
sudo nft add table ip nat
sudo nft add chain ip nat prerouting { type nat hook prerouting priority 0 \; }
sudo nft add chain ip nat postrouting { type nat hook postrouting priority 100 \; }


#Reglas para mantener el escenario de clase anterior con IPTABLES

##Reglas SNAT
###Regla SNAT para LAN
sudo nft add rule ip nat postrouting oifname "ens4" ip saddr 192.168.0.0/24 counter masquerade
###Regla SNAT para DMZ
sudo nft add rule ip nat postrouting oifname "ens4" ip saddr 172.16.0.0/16 counter masquerade

##Reglas DNAT
#Para un wordpress que hay en hela
sudo nft add rule ip nat prerouting tcp dport 80 counter dnat to 172.16.0.200

#Para hacer consultas DNS a thor
#sudo nft add rule ip nat prerouting udp dport 53 counter dnat to 192.168.0.2
sudo nft add rule ip nat prerouting iifname "ens3" ip saddr { 172.22.0.0/16, 172.19.0.0/16 } udp dport 53 counter dnat to 192.168.0.2

#Para poder recibir correos en loki
sudo nft add rule ip nat prerouting tcp dport 25 counter dnat to 192.168.0.3
#Para acceder desde fuera a un mysql que hay en loki
sudo nft add rule ip nat prerouting tcp dport 3306 counter dnat to 192.168.0.3


#PERMITIR USO DE ODIN

##Permitir consultas DNS de odin a thor (DNSSERVER)
sudo nft add rule inet filter output oifname "br-intra2" udp dport 53 counter accept
sudo nft add rule inet filter input iifname "br-intra2" udp sport 53 counter accept

##Permitir tráfico HTTP y HTTPS en odin
sudo nft add rule inet filter output oifname "ens4" ip protocol tcp tcp dport { 80,443 } ct state new,established counter accept
sudo nft add rule inet filter input iifname "ens4" ip protocol tcp tcp sport { 80,443 } ct state established counter accept

#Permitir conexiones SSH por el puerto 2222
sudo nft add rule ip nat prerouting iifname "ens4" tcp dport 2222 counter dnat to 192.168.0.1:22
sudo nft add rule inet filter output oifname "ens4" tcp sport 22 ct state established counter accept
sudo nft add rule inet filter input iifname "ens4" tcp dport 22 ct state new,established counter accept

#Permitir conexiones SSH de odin a hela
sudo nft add rule inet filter output oifname "ens3" ip daddr 172.16.0.0/16 tcp dport 22 counter accept
sudo nft add rule inet filter input iifname "ens3" ip saddr 172.16.0.0/16 tcp sport 22 ct state established,related counter accept

#Permitir conexiones ssh de odin a thor y loki
sudo nft add rule inet filter output oifname "br-intra2" ip daddr 192.168.0.0/24 tcp dport 22 counter accept
sudo nft add rule inet filter input iifname "br-intra2" ip saddr 192.168.0.0/24 tcp sport 22 ct state established,related counter accept

#Reglas perimetrales

##Permitir consultas DNS desde br-intra hacia ens4 , necesario para el forward del dns (ESTA REGLA SOLO ME FUNCIONA SI ESTA EN LA MISMA CADENA)
sudo nft add rule inet filter DMZ_WAN iifname "br-intra2" oifname "ens4" udp dport 53 counter accept
sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "br-intra2" udp sport 53 counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens4" udp dport 53 counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "br-intra2" udp sport 53 counter accept


##Permitir consultas dns desde LAN a DMZ (hela --> thor) (ESTA REGLA SOLO ME FUNCIONA SI ESTA EN LA MISMA CADENA)
sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" udp dport 53 counter accept
sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" udp sport 53 counter accept

sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" udp dport 53 counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" udp sport 53 counter accept


##Reglas para permitir trafico a wordpress en hela
sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { new, established } counter accept
sudo nft add rule inet filter DMZ_WAN iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter accept

#Regla para hacer consultas DNS a thor (Permitir DNAT)
sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "br-intra2" ip daddr 192.168.0.2 udp dport 53 ct state new,established counter accept
sudo nft add rule inet filter DMZ_WAN iifname "br-intra2" oifname "ens4" ip saddr 192.168.0.2 udp sport 53 ct state established,related counter accept

#Regla para recibir e enviar correos en loki
#No funcionan en cadenas separadas
#sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state new,established counter accept
#sudo nft add rule inet filter DMZ_WAN iifname "br-intra2" oifname "ens4" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state new,established counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens4" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter accept


#Permitir a hela usar el servidor LDAP
sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" tcp dport 389 counter accept
sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" tcp sport 389 counter accept

#Ejercicios practica
##Permitir conexiones SSH por el puerto 2222
#sudo nft add rule ip nat prerouting iifname "ens4" tcp dport 2222 counter dnat to 192.168.0.1:22
#sudo nft add rule inet filter output oifname "ens4" tcp sport 22 ct state established counter accept
#sudo nft add rule inet filter input iifname "ens4" tcp dport 22 ct state new,established counter accept

#Desde Thor y Hela se debe permitir la conexión ssh por el puerto 22 a la máquina Odin.
##Permitir conexion ssh desde hela a odin
sudo nft add rule inet filter input iifname "ens3" ip saddr 172.16.0.200 tcp dport 22 ct state new,established counter accept
sudo nft add rule inet filter output oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 ct state established counter accept
##Permitir conexion ssh desde thor a odin
sudo nft add rule inet filter input iifname "br-intra2" ip saddr 192.168.0.2 tcp dport 22 ct state new,established counter accept
sudo nft add rule inet filter output oifname "br-intra2" ip daddr 192.168.0.2 tcp sport 22 ct state established counter accept

#La máquina Odin debe tener permitido el tráfico para la interfaz loopback.
sudo nft add rule inet filter input iifname "lo" counter accept
sudo nft add rule inet filter output oifname "lo" counter accept

#A la máquina Odin se le puede hacer ping desde la DMZ, pero desde la LAN se le debe rechazar la conexión (REJECT) y desde el exterior se rechazará de manera silenciosa.
sudo nft add rule inet filter input iifname "ens3" ip protocol icmp icmp type echo-request counter accept
sudo nft add rule inet filter output oifname "ens3" ip protocol icmp icmp type echo-reply counter accept
##Denegar la conexion desde LAN REJECT
sudo nft add rule inet filter input iifname "br-intra2" ip protocol icmp counter reject
##Denegar de manera silenciosa desde EXTERIOR
sudo nft add rule inet filter input iifname "ens3" ip protocol icmp counter drop

#La máquina Odin puede hacer ping a la LAN, la DMZ y al exterior.
##LAN
sudo nft add rule inet filter output oifname "ens3" icmp type echo-request counter accept
sudo nft add rule inet filter input iifname "ens3" icmp type echo-reply counter accept
##EXTERIOR
sudo nft add rule inet filter output oifname "ens4" icmp type echo-request counter accept
sudo nft add rule inet filter input iifname "ens4" icmp type echo-reply counter accept
##DMZ
sudo nft add rule inet filter output oifname "br-intra2" icmp type echo-request counter accept
sudo nft add rule inet filter input iifname "br-intra2" icmp type echo-reply counter accept


####Desde la máquina Hela se puede hacer ping y conexión ssh a las máquinas de la LAN.
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 ip protocol icmp icmp type echo-request counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 ip protocol icmp icmp type echo-reply counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp dport 22 counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 counter accept

##Si no estan en la cadena forward no funciona
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 ip protocol icmp icmp type echo-request counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 ip protocol icmp icmp type echo-reply counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp dport 22 counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 counter accept

#Desde cualquier máquina de la LAN se puede conectar por ssh a la máquina Hela.

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 22 counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 22 counter accept

##Si no esta en la cadena forward no funciona
#sudo nft add rule inet filter LAN_DMZ iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 22 counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 22 counter accept


#Configura la máquina Odin para que las máquinas de LAN y DMZ puedan acceder al exterior.
##SNAT hecho anteriormente

#Las máquinas de la LAN pueden hacer ping al exterior y navegar.
##Si no estan en la cadena forward no funciona
#sudo nft add rule inet filter LAN_WAN iifname "br-intra2" oifname "ens4" ip protocol icmp icmp type echo-request counter accept
#sudo nft add rule inet filter WAN_LAN iifname "ens4" oifname "br-intra2" ip protocol icmp icmp type echo-reply counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens4" ip protocol icmp icmp type echo-request counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "br-intra2" ip protocol icmp icmp type echo-reply counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens4" tcp dport {80, 443} counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "br-intra2" tcp sport {80, 443} counter accept


#La máquina Hela puede navegar. Instala un servidor web, un servidor ftp y un servidor de correos si no los tienes aún.
#Hela ya tiene permitido hacer consultas dns a thor
sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" tcp dport {80, 443} counter accept
sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" tcp sport {80, 443} counter accept



#### Configura la máquina Odin para que los servicios web y ftp sean accesibles desde el exterior.
sudo nft add rule ip nat prerouting tcp dport 21 counter dnat to 172.16.0.200

#No funcionan en cadenas separadas
#sudo nft add rule inet filter WAN_DMZ iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
#sudo nft add rule inet filter DMZ_WAN iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept

sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept


#### El servidor web y el servidor ftp deben ser accesibles desde la LAN y desde el exterior.
##No funcionan las reglass en cadenas separadas
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { new, established } counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter accept

sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter accept


#### El servidor de correos sólo debe ser accesible desde la LAN.
#no funciona en cadenas separadas
#sudo nft add rule inet filter DMZ_LAN iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state { new, established } counter accept
#sudo nft add rule inet filter LAN_DMZ iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter accept
sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter accept



#### En la máquina Loki instala un servidor Postgres si no lo tiene aún. A este servidor se puede acceder desde la DMZ, pero no desde el exterior.
#no funciona en cadenas distintas
#sudo nft add rule inet filter LAN_DMZ iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 5432 ct state { new, established } counter accept
#sudo nft add rule inet filter DMZ_LAN iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 5432 ct state established,related counter accept


sudo nft add rule inet filter forward iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 5432 ct state { new, established } counter accept
sudo nft add rule inet filter forward iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 5432 ct state established,related counter accept


#### Evita ataques DoS por ICMP Flood, limitando a 4 el número de peticiones por segundo desde una misma IP.
sudo nft insert rule inet filter input icmp type echo-request limit rate 1/second burst 4 packets counter drop

#### Evita ataques DoS por SYN Flood.
#sudo nft insert rule inet filter input tcp flags \& '(fin|syn|rst|ack) == syn' counter limit rate over 25/second drop

####Evita que realicen escaneos de puertos a Odin.
#sudo nft insert rule inet filter input tcp flags & (fin|syn|rst|ack) == (syn) counter drop

#sudo nft add rule inet filter output udp dport 53 counter accept
#sudo nft add rule inet filter input udp sport 53 counter accept

```

### Rules

Every time I have executed the script the rules lose the counters but so would the scheme with all the rules at the end of the practice:

```bash
javiercruces@odin:~$ sudo nft list ruleset  
table inet filter {
	chain forward {
		type filter hook forward priority filter + 10; policy drop;
		counter packets 711 bytes 171730
		iifname "br-intra2" oifname "ens4" udp dport 53 counter packets 107 bytes 8505 accept
		iifname "ens4" oifname "br-intra2" udp sport 53 counter packets 107 bytes 93423 accept
		iifname "ens3" oifname "br-intra2" udp dport 53 counter packets 11 bytes 758 accept
		iifname "br-intra2" oifname "ens3" udp sport 53 counter packets 11 bytes 1818 accept
		iifname "ens4" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state established,new counter packets 0 bytes 0 accept
		iifname "br-intra2" oifname "ens4" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter packets 0 bytes 0 accept
		iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 ip protocol icmp icmp type echo-request counter packets 2 bytes 168 accept
		iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 ip protocol icmp icmp type echo-reply counter packets 2 bytes 168 accept
		iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp dport 22 counter packets 160 bytes 16502 accept
		iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 counter packets 100 bytes 15086 accept
		iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 22 counter packets 30 bytes 6041 accept
		iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 22 counter packets 23 bytes 5213 accept
		iifname "br-intra2" oifname "ens4" ip protocol icmp icmp type echo-request counter packets 1 bytes 84 accept
		iifname "ens4" oifname "br-intra2" ip protocol icmp icmp type echo-reply counter packets 1 bytes 84 accept
		iifname "br-intra2" oifname "ens4" tcp dport { 80, 443 } counter packets 16 bytes 1666 accept
		iifname "ens4" oifname "br-intra2" tcp sport { 80, 443 } counter packets 17 bytes 4947 accept
		iifname "ens3" oifname "ens4" tcp dport { 80, 443 } counter packets 32 bytes 3332 accept
		iifname "ens4" oifname "ens3" tcp sport { 80, 443 } counter packets 34 bytes 9903 accept
		iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { established, new } counter packets 0 bytes 0 accept
		iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter packets 0 bytes 0 accept
		iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 21 ct state { established, new } counter packets 0 bytes 0 accept
		iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 21 ct state established,related counter packets 0 bytes 0 accept
		iifname "br-intra2" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { established, new } counter packets 18 bytes 1064 accept
		iifname "ens3" oifname "br-intra2" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter packets 14 bytes 1348 accept
		iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 25 ct state { established, new } counter packets 0 bytes 0 accept
		iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 25 ct state established,related counter packets 0 bytes 0 accept
		iifname "ens3" oifname "br-intra2" ip daddr 192.168.0.3 tcp dport 5432 ct state { established, new } counter packets 0 bytes 0 accept
		iifname "br-intra2" oifname "ens3" ip saddr 192.168.0.3 tcp sport 5432 ct state established,related counter packets 0 bytes 0 accept
	}

	chain input {
		type filter hook input priority filter; policy drop;
		icmp type echo-request limit rate 1/second burst 4 packets counter packets 13 bytes 1092 drop
		counter packets 1490 bytes 141906
		iifname "br-intra2" udp sport 53 counter packets 18 bytes 2352 accept
		iifname "ens4" ip protocol tcp tcp sport { 80, 443 } ct state established counter packets 17 bytes 13286 accept
		iifname "ens4" tcp dport 22 ct state established,new counter packets 965 bytes 70084 accept
		iifname "ens3" ip saddr 172.16.0.0/16 tcp sport 22 ct state established,related counter packets 356 bytes 39980 accept
		iifname "br-intra2" ip saddr 192.168.0.0/24 tcp sport 22 ct state established,related counter packets 131 bytes 15952 accept
		iifname "ens3" ip saddr 172.16.0.200 tcp dport 22 ct state established,new counter packets 0 bytes 0 accept
		iifname "br-intra2" ip saddr 192.168.0.2 tcp dport 22 ct state established,new counter packets 0 bytes 0 accept
		iifname "lo" counter packets 0 bytes 0 accept
		iifname "ens3" ip protocol icmp icmp type echo-request counter packets 0 bytes 0 accept
		iifname "br-intra2" ip protocol icmp counter packets 1 bytes 84 reject with icmp port-unreachable
		iifname "ens3" ip protocol icmp counter packets 1 bytes 84 drop
		iifname "ens3" icmp type echo-reply counter packets 0 bytes 0 accept
		iifname "ens4" icmp type echo-reply counter packets 1 bytes 84 accept
		iifname "br-intra2" icmp type echo-reply counter packets 0 bytes 0 accept
		iifname "lo" counter packets 0 bytes 0 accept
	}

	chain output {
		type filter hook output priority filter; policy drop;
		counter packets 1404 bytes 207511
		oifname "br-intra2" udp dport 53 counter packets 18 bytes 1304 accept
		oifname "ens4" ip protocol tcp tcp dport { 80, 443 } ct state established,new counter packets 19 bytes 7331 accept
		oifname "ens4" tcp sport 22 ct state established counter packets 577 bytes 142596 accept
		oifname "ens3" ip daddr 172.16.0.0/16 tcp dport 22 counter packets 547 bytes 38208 accept
		oifname "br-intra2" ip daddr 192.168.0.0/24 tcp dport 22 counter packets 194 bytes 14400 accept
		oifname "ens3" ip daddr 172.16.0.200 tcp sport 22 ct state established counter packets 0 bytes 0 accept
		oifname "br-intra2" ip daddr 192.168.0.2 tcp sport 22 ct state established counter packets 0 bytes 0 accept
		oifname "lo" counter packets 12 bytes 1008 accept
		oifname "ens3" ip protocol icmp icmp type echo-reply counter packets 0 bytes 0 accept
		oifname "ens3" icmp type echo-request counter packets 1 bytes 84 accept
		oifname "ens4" icmp type echo-request counter packets 1 bytes 84 accept
		oifname "br-intra2" icmp type echo-request counter packets 1 bytes 84 accept
		oifname "lo" counter packets 0 bytes 0 accept
	}

	chain WAN_LAN {
		type filter hook forward priority filter + 1; policy accept;
		counter packets 711 bytes 171730
	}

	chain WAN_DMZ {
		type filter hook forward priority filter + 2; policy accept;
		counter packets 711 bytes 171730
		iifname "ens4" oifname "br-intra2" udp sport 53 counter packets 107 bytes 93423 accept
		iifname "ens4" oifname "ens3" ip daddr 172.16.0.200 tcp dport 80 ct state { established, new } counter packets 0 bytes 0 accept
		iifname "ens4" oifname "br-intra2" ip daddr 192.168.0.2 udp dport 53 ct state established,new counter packets 0 bytes 0 accept
	}

	chain LAN_WAN {
		type filter hook forward priority filter + 3; policy accept;
		counter packets 711 bytes 171730
	}

	chain LAN_DMZ {
		type filter hook forward priority filter + 4; policy accept;
		counter packets 711 bytes 171730
		iifname "ens3" oifname "br-intra2" udp dport 53 counter packets 11 bytes 758 accept
		iifname "ens3" oifname "br-intra2" tcp dport 389 counter packets 0 bytes 0 accept
	}

	chain DMZ_LAN {
		type filter hook forward priority filter + 5; policy accept;
		counter packets 711 bytes 171730
		iifname "br-intra2" oifname "ens3" udp sport 53 counter packets 11 bytes 1818 accept
		iifname "br-intra2" oifname "ens3" tcp sport 389 counter packets 0 bytes 0 accept
	}

	chain DMZ_WAN {
		type filter hook forward priority filter + 6; policy accept;
		counter packets 711 bytes 171730
		iifname "br-intra2" oifname "ens4" udp dport 53 counter packets 107 bytes 8505 accept
		iifname "ens3" oifname "ens4" ip saddr 172.16.0.200 tcp sport 80 ct state established,related counter packets 0 bytes 0 accept
		iifname "br-intra2" oifname "ens4" ip saddr 192.168.0.2 udp sport 53 ct state established,related counter packets 0 bytes 0 accept
	}
}
table ip nat {
	chain prerouting {
		type nat hook prerouting priority filter; policy accept;
		tcp dport 80 counter packets 8 bytes 480 dnat to 172.16.0.200
		iifname "ens3" ip saddr { 172.19.0.0/16, 172.22.0.0/16 } udp dport 53 counter packets 0 bytes 0 dnat to 192.168.0.2
		tcp dport 25 counter packets 0 bytes 0 dnat to 192.168.0.3
		tcp dport 3306 counter packets 12 bytes 720 dnat to 192.168.0.3
		iifname "ens4" tcp dport 2222 counter packets 0 bytes 0 dnat to 192.168.0.1:22
		tcp dport 21 counter packets 0 bytes 0 dnat to 172.16.0.200
	}

	chain postrouting {
		type nat hook postrouting priority srcnat; policy accept;
		oifname "ens4" ip saddr 192.168.0.0/24 counter packets 109 bytes 8649 masquerade
		oifname "ens4" ip saddr 172.16.0.0/16 counter packets 2 bytes 120 masquerade
	}
}

```

### Make the rules persistent

Let's save the rules with:

```bash
root@odin:/home/javiercruces# nft list ruleset > /etc/nftables.conf
```

If we want to restore them:

```bash
javiercruces@odin:~$ sudo nft -f /etc/nftables.conf
```


To make the rules restart alone:

```bash
#Creamos la unidad de systemd
javiercruces@odin:~$ sudo cat /etc/systemd/system/nftables-persistent.service
[Unit]
Description=Cargar reglas de nftables al iniciar el sistema

[Service]
Type=oneshot
ExecStart=/usr/sbin/nft -f /etc/nftables/nftables.rules

[Install]
WantedBy=multi-user.target

#Activa el servicio para que al reiniciar se apliquen los cambios
javiercruces@odin:~$ sudo systemctl enable nftables-persistent.service
```

