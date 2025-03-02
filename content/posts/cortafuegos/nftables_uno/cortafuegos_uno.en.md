---
title: "Implementation of a perimeter firewall with Nftables I"
date: 2024-03-28T10:00:00+00:00
Description: Implementation of a perimeter firewall with Nftables
tags: [FIREWALL,LINUX,DEBIAN,NFTABLES]
hero: /images/cortafuegos/nftables1.png
---



In this post on a Debian machine scenario, we will apply rules with Nfables to match the traffic that goes into and out of our network, trying to imitate a scenario.



> [NOTE]
> To deploy the stage to perform these exercises you will need to deploy the .yaml file you will find in the link to the next paragraph. This will be in charge of deploying 2 machines one that will make firewall and one that will simulate a client that will be connected to the first machine to simulate a local network.

With NFTABLES it does the exercise of the https: / / fp.josedomingo.org / seguridad / u03 / perimetral _ iptables.html by documenting the operating tests performed.

### Stage preparation

The first thing we'll do is activate the forwarding bit. To do this, we will edit the file '/ etc / sysctl.conf' using the following command:

```bash
javiercruces@router-fw:~$ sudo nano /etc/sysctl.conf 
#Descomentamos la linea
net.ipv4.ip_forward=1
```

Then we will apply the changes using the following command:

```bash
javiercruces@router-fw:~$ sudo sysctl -p
net.ipv4.ip_forward = 1
```

Now we'll add the filter table:

```bash
javiercruces@router-fw:~$ sudo nft add table inet filter
```

We can see the tables created:

```bash
javiercruces@router-fw:~$ sudo nft list tables
table inet filter
```

Create the chains for the input and output:

```bash
#Cadena de "entrada"
javiercruces@router-fw:~$ sudo nft add chain inet filter input { type filter hook input priority 0 \; counter \; policy accept \; }

#Cadena de "salida"
javiercruces@router-fw:~$ sudo nft add chain inet filter output { type filter hook output priority 0 \; counter \; policy accept \; }

#Cadena forward , peticiones que atraviesen :
javiercruces@router-fw:~$ sudo nft add chain inet filter forward { type filter hook forward priority 0 \; counter \; policy drop \; }
```

We will now see that these three chains have been created:

```bash
javiercruces@router-fw:~$ sudo nft list chains
table inet filter {
	chain input {
		type filter hook input priority filter; policy accept;
	}
	chain output {
		type filter hook output priority filter; policy accept;
	}
	chain forward {
		type filter hook forward priority filter; policy accept;
	}
}
```
### Firewall rules

## Allow ssh to the firewall

Now let's allow the ssh to the router-fw machine:

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter input iif ens3 tcp dport 22 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter output oif ens3 tcp sport 22 ct state established counter accept
```

## # Default policy DROP

Now let's put the default DROP policy:

```bash
javiercruces@router-fw:~$ sudo nft chain inet filter input { policy drop \; }
javiercruces@router-fw:~$ sudo nft chain inet filter output { policy drop \; }
javiercruces@router-fw:~$ sudo nft chain inet filter forward { policy drop \; }
```

We will check that with the new policy we can connect by ssh and we have not lost the connection, seeing that we have hits in the rules.

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
table inet filter {
	chain input {
		type filter hook input priority filter; policy drop;
		counter packets 174 bytes 11824
		iif "ens3" tcp dport 22 ct state established,new counter packets 129 bytes 8252 accept
	}

	chain output {
		type filter hook output priority filter; policy drop;
		counter packets 169 bytes 31232
		oif "ens3" tcp sport 22 ct state established counter packets 85 bytes 22632 accept
	}
}
```

### SNAT

We make SNAT so LAN teams can access the outside.

This will require us to create the NAT table and its chains. As we can see, we have indicated less priority in the posttrouting chain (the lower the number, the higher the priority) for the rules of that chain to be executed after the pre-routing rules.

```bash
#Creamos la tabla NAT
javiercruces@router-fw:~$ sudo nft add table nat

#Cadena para el DNAT
javiercruces@router-fw:~$ sudo nft add chain nat prerouting { type nat hook prerouting priority 0 \; }

#Cadena para el SNAT
javiercruces@router-fw:~$ sudo nft add chain nat postrouting { type nat hook postrouting priority 100 \; }
```

Now let's let SNAT do to the LAN network:

```bash
javiercruces@router-fw:~$ sudo nft add rule ip nat postrouting oifname "ens3" ip saddr 192.168.100.0/24 counter masquerade
```
### We allowed the ssh from the firecut to the LAN

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter output oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter input iifname "ens4" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter accept
```

Now that we can connect by ssh to our LAN machine, let's check the two above rules.

```bash
javiercruces@router-fw:~$ ssh debian@192.168.100.10
Linux lan 6.1.0-12-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.52-1 (2023-09-07) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Feb 27 18:31:10 2024 from 192.168.100.2

debian@lan:~$ ping 1.1.1.1
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
^C
--- 1.1.1.1 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1002ms
```

We will see that we can connect by ssh, however the ping is not allowed but I have done so that the SNAT rule has hits.

Let's see that the rules have hits:

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
table inet filter {
	chain input {
		type filter hook input priority filter; policy drop;
		counter packets 621 bytes 63636
		iif "ens3" tcp dport 22 ct state established,new counter packets 493 bytes 41948 accept
		iifname "ens4" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 81 bytes 17628 accept
	}

	chain output {
		type filter hook output priority filter; policy drop;
		counter packets 1231 bytes 141120
		oif "ens3" tcp sport 22 ct state established counter packets 349 bytes 68222 accept
		oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 103 bytes 17420 accept
	}
	chain forward {
		type filter hook forward priority filter; policy drop;
		counter packets 4 bytes 336
	}
}

table ip nat {
	chain prerouting {
		type nat hook prerouting priority filter; policy accept;
	}

	chain postrouting {
		type nat hook postrouting priority srcnat; policy accept;
		oifname "ens3" ip saddr 192.168.100.0/24 counter packets 1 bytes 84 masquerade
	}
}
```

As we can see the SNAT has hits, so the rule is working, but since we don't let it through the firewall these won't go out.
### We allow traffic for the loopback interface

We add the rules, to allow traffic to the loopback interface:

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter input iifname "lo" counter accept    
javiercruces@router-fw:~$ sudo nft add rule inet filter output oifname "lo" counter accept
```

We check that we have connectivity:

```bash
javiercruces@router-fw:~$ ping 127.0.0.1
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.205 ms
```

Let's see the rule hits:

```bash
javiercruces@router-fw:~$ sudo nft list ruleset | grep lo
		iifname "lo" counter packets 2 bytes 168 accept
		oifname "lo" counter packets 2 bytes 168 accept
```

## Petitions and responses protocol ICMP

We will allow the router-fw machine to accept ICMP requests and that I sent the answer:

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter output oifname "ens3" icmp type echo-reply counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter input iifname "ens3" icmp type echo-request counter accept
```

I do ping from my machine:

```bash
javiercruces@HPOMEN15:~/Documentos/2ºASIR/SAD/cortafuegos1$ ping 172.22.201.120 -c 1
PING 172.22.201.120 (172.22.201.120) 56(84) bytes of data.
64 bytes from 172.22.201.120: icmp_seq=1 ttl=61 time=85.4 ms

--- 172.22.201.120 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 85.403/85.403/85.403/0.000 ms
```

## # Allow to do ping from the LAN

Let's let you do ping from the LAN:

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 icmp type echo-request counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 icmp type echo-reply counter accept
```

Let's check it out:

```bash
debian@lan:~$ ping 1.1.1.1
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
64 bytes from 1.1.1.1: icmp_seq=1 ttl=50 time=40.8 ms
64 bytes from 1.1.1.1: icmp_seq=2 ttl=50 time=40.8 ms
^C
--- 1.1.1.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 40.821/40.834/40.848/0.013 ms
```

Let's see the rule hits, plus with this we can check the SNAT rule:

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
table inet filter {
	chain input {
		type filter hook input priority filter; policy drop;
		counter packets 2637 bytes 213636
		iif "ens3" tcp dport 22 ct state established,new counter packets 2346 bytes 172928 accept
		iifname "ens4" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 225 bytes 32812 accept
		iifname "lo" counter packets 2 bytes 168 accept
		iifname "ens3" icmp type echo-request counter packets 1 bytes 84 accept
	}

	chain output {
		type filter hook output priority filter; policy drop;
		counter packets 4656 bytes 697080
		oif "ens3" tcp sport 22 ct state established counter packets 1618 bytes 477018 accept
		oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 291 bytes 30252 accept
		oifname "lo" counter packets 2 bytes 168 accept
		oifname "ens3" icmp type echo-reply counter packets 1 bytes 84 accept
	}

	chain forward {
		type filter hook forward priority filter; policy drop;
		counter packets 31 bytes 2604
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 icmp type echo-request counter packets 12 bytes 1008 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 icmp type echo-reply counter packets 2 bytes 168 accept
	}
}
table ip nat {
	chain prerouting {
		type nat hook prerouting priority filter; policy accept;
	}

	chain postrouting {
		type nat hook postrouting priority srcnat; policy accept;
		oifname "ens3" ip saddr 192.168.100.0/24 counter packets 4 bytes 336 masquerade
	}
}
```
## DNS consultations and responses from the LAN

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 udp dport 53 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 udp sport 53 ct state established counter accept
```

We will do a query using the host command, as I do not have another tool installed to do dns consultations:

```bash
debian@lan:~$ host www.javiercd.es
www.javiercd.es is an alias for javierasping.github.io.
javierasping.github.io has address 185.199.111.153
javierasping.github.io has address 185.199.108.153
javierasping.github.io has address 185.199.109.153
javierasping.github.io has address 185.199.110.153
javierasping.github.io has IPv6 address 2606:50c0:8000::153
javierasping.github.io has IPv6 address 2606:50c0:8001::153
javierasping.github.io has IPv6 address 2606:50c0:8003::153
javierasping.github.io has IPv6 address 2606:50c0:8002::153
```

Let's check the hits of the rules:

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 udp dport 53 ct state established,new counter packets 10 bytes 643 accept
iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 udp sport 53 ct state established counter packets 10 bytes 2644 accept
```
### We allow web navigation from the LAN

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip protocol tcp ip saddr 192.168.100.0/24 tcp dport { 80,443} ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip protocol tcp ip daddr 192.168.100.0/24 tcp sport { 80,443} ct state established counter accept
```

To verify this point, we will need to modify the / etc / nsSwitch.conf file, which determines the priority of DNS resolution. We will make this modification to prioritize DNS consultation to the system DNS service, which is included in Debian and Ubuntu. This will allow the queries to be carried out first on the machine itself and, if necessary, will be sent to the configured DNS server as in this scenario the applications do not solve us if we do not make this modification.

```bash
debian@lan:~$ sudo nano /etc/nsswitch.conf 
hosts:          files dns resolve [!UNAVAIL=return]
```

We'll also change the machine's dns server and instead of us, we'll put the high school server:

```bash
debian@lan:~$ sudo cat /etc/resolv.conf 
nameserver 172.22.0.1
```

Once the changes are applied, we will order a web by the domain name, so we will check the operation of the two above points. I'll just order the headers to make the output more legible, a code 200 would be correct. In the part of http gives us a redirection as the server redirects you to https:

```bash
debian@lan:~$ curl -I https://www.javiercd.es/
HTTP/2 200 
server: GitHub.com
content-type: text/html; charset=utf-8
last-modified: Sun, 25 Feb 2024 23:03:49 GMT
access-control-allow-origin: *
strict-transport-security: max-age=31556952
etag: "65dbc755-675b"
expires: Wed, 28 Feb 2024 10:10:17 GMT
cache-control: max-age=600
x-proxy-cache: MISS
x-github-request-id: 5CD4:0E10:CBDBE5:CFBAEA:65DF0430
accept-ranges: bytes
date: Wed, 28 Feb 2024 10:00:17 GMT
via: 1.1 varnish
age: 0
x-served-by: cache-mad2200123-MAD
x-cache: MISS
x-cache-hits: 0
x-timer: S1709114417.014922,VS0,VE167
vary: Accept-Encoding
x-fastly-request-id: e15d291bbff90bf9de58991f0f6477e4398c415d
content-length: 26459

debian@lan:~$ curl -I http://www.javiercd.es/
HTTP/1.1 301 Moved Permanently
Content-Length: 162
Server: GitHub.com
Content-Type: text/html
Location: https://www.javiercd.es/
X-GitHub-Request-Id: 9870:0E7F:37400AD:3848DF5:65DF0425
Accept-Ranges: bytes
Date: Wed, 28 Feb 2024 10:00:27 GMT
Age: 21
X-Served-By: cache-mad2200100-MAD
X-Cache: HIT
X-Cache-Hits: 1
X-Timer: S1709114427.468002,VS0,VE1
Vary: Accept-Encoding
X-Fastly-Request-ID: e321e34041a049f6f7c99e0693be994990da6da3
X-Cache: MISS from f0
X-Cache-Lookup: HIT from f0:3128
Via: 1.1 varnish, 1.1 f0 (squid/4.6)
Connection: close
```


### We allow access to our LAN web server from the outside

As we already have dns resolution and web navigation, we can update our repositories and install packages:

```bash
debian@lan:~$ sudo apt update -y && sudo apt install apache2 -y 
```

Once apache is installed we will perform the DNAT rule:

```bash
javiercruces@router-fw:~$ sudo nft add rule ip nat prerouting iifname "ens3" tcp dport 80 counter dnat to 192.168.100.10
```

Now we have to allow on the forward chain the traffic to allow the DNAT. Requests to the web server and answers

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 80 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 80 ct state established counter accept
```

Now let's check that we can access the web server:

```bash
javiercruces@HPOMEN15:~/Documentos/2ºASIR/SAD/cortafuegos1$ curl -I 172.22.201.120
HTTP/1.1 200 OK
Date: Wed, 28 Feb 2024 10:24:26 GMT
Server: Apache/2.4.57 (Debian)
Last-Modified: Wed, 28 Feb 2024 10:17:20 GMT
ETag: "29cd-6126e72b03120"
Accept-Ranges: bytes
Content-Length: 10701
Vary: Accept-Encoding
Content-Type: text/html
```

From a browser:

![](../img/Pastedimage20240228112558.png)

Finally let's check that the rules involved have hits and I'll leave you the full list to see the rules up to this point:

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
table inet filter {
	chain input {
		type filter hook input priority filter; policy drop;
		counter packets 20313 bytes 2212299
		iif "ens3" tcp dport 22 ct state established,new counter packets 11896 bytes 827728 accept
		iifname "ens4" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 8093 bytes 1321072 accept
		iifname "lo" counter packets 92 bytes 17660 accept
		iifname "ens3" icmp type echo-request counter packets 1 bytes 84 accept
	}

	chain output {
		type filter hook output priority filter; policy drop;
		counter packets 69191 bytes 6011531
		oif "ens3" tcp sport 22 ct state established counter packets 8461 bytes 1953220 accept
		oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 9482 bytes 623484 accept
		oifname "lo" counter packets 92 bytes 17660 accept
		oifname "ens3" icmp type echo-reply counter packets 1 bytes 84 accept
	}

	chain forward {
		type filter hook forward priority filter; policy drop;
		counter packets 42155 bytes 145465374
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 icmp type echo-request counter packets 32 bytes 2688 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 icmp type echo-reply counter packets 18 bytes 1512 accept
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 udp dport 53 ct state established,new counter packets 273 bytes 17860 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 udp sport 53 ct state established counter packets 273 bytes 52163 accept
		iifname "ens4" oifname "ens3" ip protocol tcp ip saddr 192.168.100.0/24 tcp dport { 80, 443 } ct state established,new counter packets 33973 bytes 1794576 accept
		iifname "ens3" oifname "ens4" ip protocol tcp ip daddr 192.168.100.0/24 tcp sport { 80, 443 } ct state established counter packets 7119 bytes 143533481 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 80 ct state established,new counter packets 47 bytes 3905 accept
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 80 ct state established counter packets 32 bytes 24161 accept
	}
}
table ip nat {
	chain prerouting {
		type nat hook prerouting priority filter; policy accept;
		iifname "ens3" tcp dport 80 counter packets 4 bytes 240 dnat to 192.168.100.10
	}

	chain postrouting {
		type nat hook postrouting priority srcnat; policy accept;
		oifname "ens3" ip saddr 192.168.100.0/24 counter packets 547 bytes 38852 masquerade
	}
}

```
## Additional exercises

You must then add the necessary rules to allow the following operations:

### It allows to make ssh connections to the outside from the firewall machine.

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter output oifname "ens3" tcp dport 22 ct state new,established  counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter input iifname "ens3" tcp sport 22 ct state established  counter accept
```

We're gonna connect by ssh from the firewall machine to another to check this out:

```bash
javiercruces@router-fw:~$ ssh 172.22.200.47
Linux odin.javiercd.gonzalonazareno.org 6.1.0-18-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.76-1 (2024-02-01) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Feb 28 10:35:56 2024 from 172.22.201.120
javiercruces@odin:~$ 
```

Let's check the hits in the rules:

```bash
javiercruces@router-fw:~$ sudo nft list ruleset 
iifname "ens3" tcp sport 22 ct state established counter packets 66 bytes 18624 accept
oifname "ens3" tcp dport 22 ct state established,new counter packets 89 bytes 16572 accept

```

### It allows DNS queries from the firewall machine only to the 8.8.8.8 server. Check that you can't make a dig @ 1.1.1.1.

Let's add this rule:

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter output oifname "ens3" ip daddr 8.8.8.8 udp dport 53 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter input iifname "ens3" ip saddr 8.8.8.8 udp sport 53 ct state established counter accept
```

Now let's check that through 1.1.1.1 we can't solve names but with 8.8.8.8 if:

```bash
javiercruces@router-fw:~$ dig @1.1.1.1 www.javiercd.es
;; communications error to 1.1.1.1#53: timed out
;; communications error to 1.1.1.1#53: timed out
;; communications error to 1.1.1.1#53: timed out

; <<>> DiG 9.18.24-1-Debian <<>> @1.1.1.1 www.javiercd.es
; (1 server found)
;; global options: +cmd
;; no servers could be reached

javiercruces@router-fw:~$ dig @8.8.8.8 www.javiercd.es

; <<>> DiG 9.18.24-1-Debian <<>> @8.8.8.8 www.javiercd.es
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 4046
;; flags: qr rd ra; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;www.javiercd.es.		IN	A

;; ANSWER SECTION:
www.javiercd.es.	3600	IN	CNAME	javierasping.github.io.
javierasping.github.io.	3600	IN	A	185.199.108.153
javierasping.github.io.	3600	IN	A	185.199.109.153
javierasping.github.io.	3600	IN	A	185.199.110.153
javierasping.github.io.	3600	IN	A	185.199.111.153

;; Query time: 68 msec
;; SERVER: 8.8.8.8#53(8.8.8.8) (UDP)
;; WHEN: Wed Feb 28 11:09:05 UTC 2024
;; MSG SIZE  rcvd: 144

```

Let's see the hits of the rules:

```bash
javiercruces@router-fw:~$ sudo nft list ruleset 
iifname "ens3" ip saddr 8.8.8.8 udp sport 53 ct state established counter packets 314 bytes 36448 accept
oifname "ens3" ip daddr 8.8.8.8 udp dport 53 ct state established,new counter packets 314 bytes 21912 accept
```

### It allows the firewall machine to navigate through https.

Let's add the rule:

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter output oifname "ens3" ip protocol tcp tcp dport 443 ct state new,established  counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter input iifname "ens3" ip protocol tcp tcp sport 443  ct state established  counter accept
```

Let's check that by asking the headers, which is similar to browsing we can see a code 200 in https:

```bash
javiercruces@router-fw:~$ curl -I https://www.javiercd.es/
HTTP/2 200 
server: GitHub.com
content-type: text/html; charset=utf-8
last-modified: Sun, 25 Feb 2024 23:03:49 GMT
access-control-allow-origin: *
strict-transport-security: max-age=31556952
etag: "65dbc755-675b"
expires: Wed, 28 Feb 2024 10:10:17 GMT
cache-control: max-age=600
x-proxy-cache: MISS
x-github-request-id: 5CD4:0E10:CBDBE5:CFBAEA:65DF0430
accept-ranges: bytes
date: Wed, 28 Feb 2024 11:10:32 GMT
via: 1.1 varnish
age: 0
x-served-by: cache-mad22033-MAD
x-cache: HIT
x-cache-hits: 1
x-timer: S1709118632.338441,VS0,VE131
vary: Accept-Encoding
x-fastly-request-id: 01056938385ca0e465882fa75fd0b19d0973df62
content-length: 26459
```

### Local network equipment should be able to have an external connection.

previously performed SNAT

### We allowed the ssh from the firewall to the LAN

Permitted by previous rule

### We allowed to do ping from the LAN to the firewall machine.

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter output oifname "ens4" icmp type echo-reply counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter input iifname "ens4" icmp type echo-request counter accept
```

We do the ping from LAN to firewall

```bash
debian@lan:~$ ping 192.168.100.2
PING 192.168.100.2 (192.168.100.2) 56(84) bytes of data.
64 bytes from 192.168.100.2: icmp_seq=1 ttl=64 time=1.09 ms
64 bytes from 192.168.100.2: icmp_seq=2 ttl=64 time=1.75 ms
^C
--- 192.168.100.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 1.091/1.419/1.748/0.328 ms
```

We'll see the hits for this particular rule:

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
iifname "ens4" icmp type echo-request counter packets 2 bytes 168 accept
oifname "ens4" icmp type echo-reply counter packets 2 bytes 168 accept
```

### Allows to make ssh connections from LAN equipment

Let's make the rules:

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip protocol tcp ip saddr 192.168.100.0/24 tcp dport 22 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip protocol tcp ip daddr 192.168.100.0/24 tcp sport 22 ct state established counter accept
```

We're going to connect by ssh to a machine outside the lan:

```bash
debian@lan:~$ ssh javiercruces@172.22.200.47
Linux odin.javiercd.gonzalonazareno.org 6.1.0-18-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.76-1 (2024-02-01) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Feb 28 10:36:26 2024 from 172.22.201.120
javiercruces@odin:~$ 
```

Let's see the hits of these rules:

```bash
javiercruces@router-fw:~$ sudo nft -a list table inet filter
iifname "ens4" oifname "ens3" ip protocol tcp ip saddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 10 bytes 3312 accept # handle 44
iifname "ens3" oifname "ens4" ip protocol tcp ip daddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 7 bytes 3088 accept # handle 45
```

### Install a post server on the LAN machine. It allows access from the outside and from the firewall to the post server. To prove it you can run a telnet to port 25 tcp.

With these rules we allow to connect from outside the network to the post server:

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 25 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 25 ct state established counter accept

#Regla DNAT puerto 25
javiercruces@router-fw:~$ sudo nft add rule ip nat prerouting iifname "ens3" tcp dport 25 counter dnat to 192.168.100.10
```

Let's check it out:

```bash
javiercruces@HPOMEN15:~/Documentos/2ºASIR/SAD/cortafuegos1$ telnet 172.22.201.120 25
Trying 172.22.201.120...
Connected to 172.22.201.120.
Escape character is '^]'.
220 lan.openstacklocal ESMTP Postfix (Debian/GNU)
Connection closed by foreign host.
```

Let's see the hits in the rules:

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
#Reglas para permitir el trafico
iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 25 ct state established,new counter packets 10 bytes 544 accept # handle 46
iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 25 ct state established counter packets 9 bytes 613 accept
#Regla DNAT
iifname "ens3" tcp dport 25 counter packets 1 bytes 60 dnat to 192.168.100.10

```


### Allows to make ssh connections from outside to the LAN

For this I will do a DNAT to port 2222 and allow that traffic

```bash
#Reglas para permitir el trafico del DNAT
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 2222 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 2222 ct state established counter accept

#Regla DNAT puerto 2222 para ssh
sudo nft add rule ip nat prerouting iifname "ens3" tcp dport 2222 counter dnat to 192.168.100.10
```

I have changed the port of the service ssh of lan to 2222, I will connect from outside to the LAN by ssh:

```bash
javiercruces@HPOMEN15:~/Documentos/2ºASIR/SAD/cortafuegos1$ ssh -p 2222 debian@172.22.201.120

Linux lan 6.1.0-12-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.52-1 (2023-09-07) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Feb 28 14:12:18 2024 from 192.168.100.2
debian@lan:~$ 
```

Let's check the hits of the rules:

```bash
#Reglas para permitir el ssh 2222 desde fuera hacia la LAN
iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 2222 ct state established,new counter packets 54 bytes 9784 accept
iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 2222 ct state established counter packets 44 bytes 10494 accept

#Regla DNAT
iifname "ens3" tcp dport 2222 counter packets 5 bytes 300 dnat to 192.168.100.10
```

## # Modifies the above rule, so that when we access from the outside by ssh we have to connect to port 2222, although the ssh server is configured to access by port 22.

For this we will remove the 3 above rules and add the following:

```bash
#Permitimos el trafico que ahora "cambiamos" el puerto con la regla DNAT de 2222 a 22
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state new,established counter accept
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter accept

#Regla DNAT
javiercruces@router-fw:~$ sudo nft add rule ip nat prerouting iifname "ens3" tcp dport 2222 counter dnat to 192.168.100.10
```

Now let's check that we can connect from the outside to the LAN although we have now changed the LAN ssh server to listen in port 22:

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 34 bytes 7868 accept
iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 32 bytes 9066 accept
iifname "ens3" tcp dport 2222 counter packets 7 bytes 420 dnat to 192.168.100.10:22
```


### It allows DNS queries from the LAN only to the 8.8.8.8 server. Check that you can't make a dig @ 1.1.1.1.

We will delete the previous rule that allows DNS queries:

```bash
javiercruces@router-fw:~$ sudo nft -a list table inet filter
iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 udp dport 53 ct state established,new counter packets 285 bytes 17036 accept # handle 35


javiercruces@router-fw:~$ sudo nft delete rule inet filter forward handle 35
```

We add the new rule to allow only consultations to 8.8.8:

```bash
javiercruces@router-fw:~$ sudo nft add rule inet filter forward iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 udp dport 53 ip daddr 8.8.8.8 counter accept
```

Let's check it out:

```bash
debian@lan:~$ dig @1.1.1.1 www.javiercd.es
;; communications error to 1.1.1.1#53: timed out
;; communications error to 1.1.1.1#53: timed out
;; communications error to 1.1.1.1#53: timed out

; <<>> DiG 9.18.24-1-Debian <<>> @1.1.1.1 www.javiercd.es
; (1 server found)
;; global options: +cmd
;; no servers could be reached

debian@lan:~$ dig @8.8.8.8 www.javiercd.es

; <<>> DiG 9.18.24-1-Debian <<>> @8.8.8.8 www.javiercd.es
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 59302
;; flags: qr rd ra; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;www.javiercd.es.		IN	A

;; ANSWER SECTION:
www.javiercd.es.	3600	IN	CNAME	javierasping.github.io.
javierasping.github.io.	3600	IN	A	185.199.108.153
javierasping.github.io.	3600	IN	A	185.199.109.153
javierasping.github.io.	3600	IN	A	185.199.110.153
javierasping.github.io.	3600	IN	A	185.199.111.153

;; Query time: 72 msec
;; SERVER: 8.8.8.8#53(8.8.8.8) (UDP)
;; WHEN: Wed Feb 28 14:44:29 UTC 2024
;; MSG SIZE  rcvd: 144
```

Let's see the hits of the rules:

```bash
javiercruces@router-fw:~$ sudo nft -a list table inet filter

iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 udp dport 53 ip daddr 8.8.8.8 counter packets 3 bytes 218 accept # handle 53
```



### Allows LAN equipment to browse the Internet, except for the www.realbetisbalompie.es page

We have a problem and it is that nfables only filters up to the level of transport, that is by port. So we can't read the domain as it travels in a header of the application level.

To ban it, we will have to block that IP in its entirety for a given port, in my case it will be 80 and 443.

Let's find out the domain IPS we want to block:

```bash
javiercruces@router-fw:~$ dig +short www.realbetisbalompie.es
realbetisbalompie.es.
51.255.76.196
```

We will add it to the beginning of the chain instead of add the word insert:

```bash
javiercruces@router-fw:~$ sudo nft insert rule inet filter forward ip daddr 51.255.76.196 tcp dport {80, 443} iifname "ens4" oifname "ens3" counter drop 
```

And now we won't be able to navigate the evil one's page:

```bash
debian@lan:~$ curl -I https://www.realbetisbalompie.es/
curl: (28) Failed to connect to www.realbetisbalompie.es port 443 after 129885 ms: Couldn't connect to server
```

Let's see the hits of the rule that protects us from evil:

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
ip daddr 51.255.76.196 tcp dport { 80, 443 } iifname "ens4" oifname "ens3" counter packets 7 bytes 420 drop
```


### Make the rules persistent

Let's save the rules with:

```bash
rott@router-fw:/home/javiercruces# nft list ruleset > /etc/nftables.conf
```

If we want to restore them:

```bash
javiercruces@router-fw:~$ sudo nft -f /etc/nftables.conf
```


To make the rules restart alone:

```bash
#Creamos la unidad de systemd
javiercruces@router-fw:~$ sudo cat /etc/systemd/system/nftables-persistent.service
[Unit]
Description=Cargar reglas de nftables al iniciar el sistema

[Service]
Type=oneshot
ExecStart=/usr/sbin/nft -f /etc/nftables/nftables.rules

[Install]
WantedBy=multi-user.target

#Activa el servicio para que al reiniciar se apliquen los cambios
javiercruces@router-fw:~$ sudo systemctl enable nftables-persistent.service
```

### Rules at the end of the year

I'll leave you the list of rules in the state of last exercise:

```bash
javiercruces@router-fw:~$ sudo nft list ruleset
table inet filter {
	chain input {
		type filter hook input priority filter; policy drop;
		counter packets 34414 bytes 6500685
		iif "ens3" tcp dport 22 ct state established,new counter packets 21235 bytes 1526616 accept
		iifname "ens4" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 11648 bytes 1793088 accept
		iifname "lo" counter packets 92 bytes 17660 accept
		iifname "ens3" icmp type echo-request counter packets 1 bytes 84 accept
		iifname "ens3" tcp sport 22 ct state established counter packets 66 bytes 18624 accept
		iifname "ens3" ip protocol tcp tcp sport 443 ct state established counter packets 519 bytes 3016033 accept
		iifname "ens3" ip saddr 8.8.8.8 udp sport 53 ct state established counter packets 557 bytes 68077 accept
		iifname "ens4" icmp type echo-request counter packets 2 bytes 168 accept
	}

	chain output {
		type filter hook output priority filter; policy drop;
		counter packets 86303 bytes 8331992
		oif "ens3" tcp sport 22 ct state established counter packets 15004 bytes 3534878 accept
		oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 14125 bytes 950568 accept
		oifname "lo" counter packets 92 bytes 17660 accept
		oifname "ens3" icmp type echo-reply counter packets 1 bytes 84 accept
		oifname "ens3" tcp dport 22 ct state established,new counter packets 89 bytes 16572 accept
		oifname "ens3" ip daddr 8.8.8.8 udp dport 53 ct state established,new counter packets 557 bytes 36254 accept
		oifname "ens3" ip protocol tcp tcp dport 443 ct state established,new counter packets 367 bytes 25011 accept
		oifname "ens4" icmp type echo-reply counter packets 2 bytes 168 accept
	}

	chain forward {
		type filter hook forward priority filter; policy drop;
		ip daddr 51.255.76.196 tcp dport { 80, 443 } iifname "ens4" oifname "ens3" counter packets 7 bytes 420 drop
		counter packets 45573 bytes 149083811
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 icmp type echo-request counter packets 32 bytes 2688 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 icmp type echo-reply counter packets 18 bytes 1512 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 udp sport 53 ct state established counter packets 664 bytes 101857 accept
		iifname "ens4" oifname "ens3" ip protocol tcp ip saddr 192.168.100.0/24 tcp dport { 80, 443 } ct state established,new counter packets 34813 bytes 1843071 accept
		iifname "ens3" oifname "ens4" ip protocol tcp ip daddr 192.168.100.0/24 tcp sport { 80, 443 } ct state established counter packets 7583 bytes 146852066 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 80 ct state established,new counter packets 47 bytes 3905 accept
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 80 ct state established counter packets 32 bytes 24161 accept
		iifname "ens4" oifname "ens3" ip protocol tcp ip saddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 72 bytes 18540 accept
		iifname "ens3" oifname "ens4" ip protocol tcp ip daddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 56 bytes 17296 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 25 ct state established,new counter packets 10 bytes 544 accept
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 25 ct state established counter packets 9 bytes 613 accept
		iifname "ens3" oifname "ens4" ip daddr 192.168.100.0/24 tcp dport 22 ct state established,new counter packets 90 bytes 17200 accept
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 tcp sport 22 ct state established counter packets 77 bytes 19296 accept
		iifname "ens4" oifname "ens3" ip saddr 192.168.100.0/24 udp dport 53 ip daddr 8.8.8.8 counter packets 81 bytes 5250 accept
	}
}
table ip nat {
	chain prerouting {
		type nat hook prerouting priority filter; policy accept;
		iifname "ens3" tcp dport 80 counter packets 4 bytes 240 dnat to 192.168.100.10
		iifname "ens3" tcp dport 25 counter packets 1 bytes 60 dnat to 192.168.100.10
		iifname "ens3" tcp dport 2222 counter packets 8 bytes 480 dnat to 192.168.100.10:22
	}

	chain postrouting {
		type nat hook postrouting priority srcnat; policy accept;
		oifname "ens3" ip saddr 192.168.100.0/24 counter packets 916 bytes 61536 masquerade
	}
}
```