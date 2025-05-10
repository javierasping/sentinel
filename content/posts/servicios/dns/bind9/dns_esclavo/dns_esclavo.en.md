---
title: "Configuring a Slave DNS Server with BIND9"
date: 2025-05-10T10:00:00+00:00
description: Learn how to configure a slave DNS server with BIND9 on Debian, synchronized with a master server.
tags: [DNS,BIND9,SMR,ASIR]
hero: images/servicios/dns/dns_esclavo.png
---

In this guide, you will learn how to configure a slave DNS server using BIND9 on Debian. This server will sync with the master server (`dns1.javiercruces.org`) and distribute the name resolution load in your local network. You will also be guided to verify that the zone transfer works correctly.

In this case, the slave server is located in the 192.168.10.0/24 network, with the IP 192.168.10.200.

---

## 1. Initial Setup of the Slave Server

### Hostname

First, assign the correct hostname. Edit the `/etc/hostname` file:

```bash
dns2
```

Next, configure the `/etc/hosts` file to associate the fully qualified domain name with the local IP:

```bash
127.0.1.1       dns2.javiercruces.org dns2
```

Verify that the FQDN resolves correctly using `hostname -f`. You should get the following output:

```bash
debian@dns2:~$ hostname -f
dns2.javiercruces.org
```

---

## 2. Installing BIND9

Install the BIND9 package as we did on the master server:

```bash
sudo apt update && sudo apt install bind9 bind9utils bind9-doc rsync -y
```

---

## 3. Basic Configuration

### Edit `named.conf.options`

On the slave server, edit the `/etc/bind/named.conf.options` file to allow queries from internal networks:

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

## 4. Configuring Slave Zones

Edit the `/etc/bind/named.conf.local` file to define the slave zones. These should match the zones configured on the master server:

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

Create the directory to store the slave files if it does not exist:

```bash
sudo mkdir -p /var/cache/bind/slaves
sudo chown bind:bind /var/cache/bind/slaves
```

---

## 5. Restarting the Service

Once everything is configured, restart the BIND9 service:

```bash
sudo systemctl restart bind9
```

Check for errors in the event log:

```bash
sudo journalctl -xeu bind9
```

You can also check if the zones were transferred correctly by running:

```bash
ls -l /var/cache/bind/slaves
```

---

## 6. Updating the Master Server

For the slave server to receive the zones correctly, it needs to be authorized by the master server (`dns1`).

Edit the `/etc/bind/named.conf.local` file on the master server and add the `allow-transfer` option with the slave's IP:

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

Additionally, we will update the DNS records to add the new server. You need to add an A record and an NS record. Here's the complete file:

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

We must also update the reverse zone:

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

After saving the changes, reload the BIND configuration:

```bash
sudo rndc reload
```

Or restart the service:

```bash
sudo systemctl restart bind9
```

With this, the master server is authorized to send zones to the slave when necessary.

---

## 7. Verifications

Every time you restart the service on `dns1`, it will send changes to `dns2`. To verify that the zone transfer is working correctly, run the following command on `dns2` to view logs in real-time:

```bash
debian@dns2:~$ sudo journalctl -u named -f
```

Then, add a record on the master server:

```bash
sentinel           IN      A       192.168.10.25
```

You can force the zone transfer with:

```bash
debian@dns2:~$ sudo rndc sync
```

And the logs of a successful transfer will look like this:

```bash
debian@dns2:~$ sudo journalctl -u named -f
May 10 23:11:08 dns2 named[936]: received control channel command 'sync'
May 10 23:11:08 dns2 named[936]: dumping all zones: success
```

Finally, perform a query to both servers to verify that both return the same result:

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