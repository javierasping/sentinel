---
title: "Installation and Configuration of BIND9 on Linux"
date: 2025-05-04T10:00:00+00:00
description: Learn how to install, configure, and verify a BIND9 DNS server step by step on Debian
tags: [DNS,BIND9,SMR,ASIR]
hero: images/servicios/dns/bind9_install.jpg
------------------------------------------

In this guide, you will learn how to install and configure a DNS server on Linux using BIND9. You will set up forward and reverse lookup zones for your domain, allow DNS queries from other machines on the network, and perform tests using tools like `dig`. You will also learn how to configure forwarders to efficiently resolve external domain names.

---

## 1. Initial Preparation

### Create the DNS Machine

Create a machine and set its name to `dns1.yourname.org`. 

Edit the `/etc/hostname` file:

```bash
javiercruces@dns1:~$ sudo cat /etc/hostname 
dns1
```

Then add a static resolution for this name and the DNS server's FQDN to the `/etc/hosts` file.

```bash
javiercruces@dns1:~$ sudo nano /etc/hosts
```

In my case, I will name the machine `dns1.javiercruces.org`

```bash
127.0.1.1       dns1.javiercruces.org dns1
```

Verify the FQDN with:

```bash
javiercruces@dns1:~$ hostname -f
```

It should return something like this:

```bash
javiercruces@dns1:~$ hostname -f
dns1.javiercruces.org
```

---

## 2. Installing BIND9

Install the BIND9 DNS server:

```bash
debian@dns1:~$ sudo apt update && sudo apt install bind9 bind9utils bind9-doc -y
```

## 3. Basic Configuration

### Disable IPv6 (optional)

Edit `/etc/default/named` to prevent BIND9 from using IPv6:

```bash
OPTIONS="-4 -f -u bind"
```

### Allow queries from specific networks

Edit `/etc/bind/named.conf.options`:

```bash
options {
    directory "/var/cache/bind";

    allow-query { 127.0.0.1; 192.168.10.0/24; 192.168.20.0/24; };
    recursion yes;

    dnssec-validation no;

    forwarders {
        1.1.1.1;
        8.8.8.8;
    };
};
```

Restart BIND9:

```bash
sudo systemctl restart bind9
```

---

## 4. Configure Forward Lookup Zone

Edit `/etc/bind/named.conf.local`:

```bash
zone "javiercruces.org" {
    type master;
    file "/var/cache/bind/db.javiercruces.org";
};
```

Create the zone file:

```bash
sudo cp /etc/bind/db.empty /var/cache/bind/db.javiercruces.org
sudo nano /var/cache/bind/db.javiercruces.org
```

Example content:

```
$TTL    86400
@       IN      SOA     dns1.javiercruces.org. root.javiercruces.org. (
                          1         ; Serial
                     604800         ; Refresh
                      86400         ; Retry
                    2419200         ; Expire
                      86400 )       ; Negative Cache TTL
;
@       IN      NS      dns1.javiercruces.org.
@       IN      MX  10  correo.javiercruces.org.

$ORIGIN javiercruces.org.

dns1            IN      A       192.168.10.1
correo          IN      A       192.168.10.2
thor            IN      A       192.168.10.3
hela            IN      A       192.168.10.4
www             IN      CNAME   thor
informatica     IN      CNAME   thor
ftp             IN      CNAME   hela
```

---

## 5. Configure Reverse Lookup Zone

Edit `/etc/bind/named.conf.local`:

```bash
zone "10.168.192.in-addr.arpa" {
    type master;
    file "/var/cache/bind/db.192.168.10";
};
```

Ensure the corresponding line in `/etc/bind/zones.rfc1918` is commented out:

```bash
//zone "10.168.192.in-addr.arpa" { type master; file "/etc/bind/db.empty"; };
```

Create the zone file:

```bash
sudo cp /etc/bind/db.empty /var/cache/bind/db.192.168.10
sudo nano /var/cache/bind/db.192.168.10
```

Example content:

```
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
```

---

## 6. Testing

With the configuration from the previous sections, your DNS server should now be operational.

### Basic queries with `dig`

If you don’t specify the DNS server using the `@` parameter, it will use the one configured in `/etc/resolv.conf`. Remember to update your DHCP settings to assign your local DNS server to your clients.

```bash
# A record query for hela.javiercruces.org
dig @192.168.10.1 hela.javiercruces.org

# Reverse lookup (PTR) for 192.168.10.4 (corresponding to hela)
dig @192.168.10.1 -x 192.168.10.4

# MX record query for javiercruces.org
dig @192.168.10.1 javiercruces.org MX

# NS record query for javiercruces.org
dig @192.168.10.1 javiercruces.org NS
```

Observe the query times and which records were used for name resolution. The second query should be faster due to cache use.

If you want to flush the DNS cache on your server, use the following command:

```bash
sudo rndc flush
```

---