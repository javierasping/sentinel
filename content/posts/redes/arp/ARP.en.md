---
title: "ARP Protocol"
date: 2023-09-08T10:00:00+00:00
description: Document in which a number of questions about the ARP protocol are answered
tags: [Redes, ARP]
hero: images/redes/arp/portada.png
---



The Address Resolution Protocol (ARP) is fundamental in computer networks to map IP addresses to physical link layer addresses (MAC). Its main function is to find the MAC address associated with a specific IP address on a local network. When one device needs to communicate with another on the same network, it uses ARP to determine the MAC address of the destination before sending data.

### Nature of ARP Requests

ARP requests are broadcast messages, as the destination address in the header is a broadcast address. This address has all its bits set to 1, which in MAC addresses is represented as `FF:FF:FF:FF:FF:FF`.

When the device with the requested IP address (for example, `192.168.1.1`) receives this message, it responds to the request, allowing the sender to obtain the corresponding MAC address.

![](/redes/arp/img/Aspose.Words.239ce20f-0f3b-447a-b584-fd1166c210d0.001.jpeg)

### Nature of ARP Responses

In an ARP response, the destination address is that of the device that initiated the request. Therefore, the response is not a broadcast message, but a unicast (point-to-point) communication.

![](/redes/arp/img/Aspose.Words.239ce20f-0f3b-447a-b584-fd1166c210d0.002.jpeg)


### ARP Cache Update Process

When a ping operation is performed, both the sender and the receiver add each other to their respective ARP tables. By consulting both tables, it can be verified that the correspondences have been registered.

The retention time for entries in the cache is generally 120 seconds; once this period expires, the entry is automatically deleted.

Devices that did not participate in the communication do not store any information in their ARP cache regarding said transaction.

### Using the `ip neigh` Command

The `ip neigh` command allows management of the ARP table, where IP-to-MAC address relationships are stored. This command can be used to view the table, add, delete, or modify entries, as well as adjust the lifetime of entries.

**Main functions:**

- **Show the full ARP table**: `ip neighbour show`
- **Add an entry to the ARP table**: `ip neighbour add {IP} lladdr {MAC} dev {interface}`
- **Remove an entry from the ARP table**: `ip neighbour del {IP} dev {interface}`
- **Set the lifetime of an entry**: `ip neighbour change {IP} dev {interface} nud {state}`
- **Search for a specific entry**: `ip neighbour | grep {IP}`

This command is the modern alternative and complement to the traditional `arp` command.

### Gratuitous ARP

A Gratuitous ARP is a request issued by a device to inform other devices on the network about its own IP and MAC address, thereby updating their ARP tables.

Its primary purpose is to ensure that all devices have the most up-to-date information possible. One of its most common uses is the detection of IP address conflicts; if another device responds to a gratuitous ARP packet, it indicates that the IP address is already in use.


### ARP Spoofing Attack

ARP Spoofing consists of modifying the data flow between a victim device and its default gateway. The attacker sends fake ARP responses to associate their own MAC address with the IP address of the gateway on the victim's machine, thereby achieving a Man-in-the-Middle (MITM) attack.

In this way, the attacker intercepts all traffic, enabling them to obtain passwords and confidential or sensitive information.

**Attack steps:**

1. **Network scanning**: Obtaining a list of connected devices.
2. **Sending fake ARP packets**: Associating the attacker's MAC with the victim's or gateway's IP.
3. **Interception**: Capturing all traffic passing between the targets.

This attack requires the attacker to have access to the local network. To prevent it, the following are recommended:

- Using ARP spoofing detection tools.
- Implementing firewalls capable of blocking suspicious ARP packets.
- Employing encryption protocols such as IPsec and SSL/TLS.
- Configuring static entries in the ARP table.

### MAC Flooding and MAC Spoofing

**MAC Flooding**: Consists of saturating the MAC address table of a network device (such as a switch) by sending a massive amount of fake addresses. When the table is full, the switch begins to forward traffic to all its ports (acting like a hub), which can allow data interception or lead to a denial of service (DoS).

To mitigate this attack, it is recommended to limit the table size and enable the detection of suspicious traffic.

**MAC Spoofing**: Consists of falsifying the MAC address of a device to impersonate another and thus intercept specific traffic or access restricted resources.

To mitigate this attack, the following strategies can be implemented:

- **Static ARP table entries**: Manually associating IPs with MAC addresses to prevent dynamic ARP messages from modifying the table. This is ideal for the default gateway.
- **DHCP Snooping**: Maintains a record of MACs connected to each port and immediately detects impersonations.
- **Dynamic ARP Inspection (DAI)**: Requires DHCP Snooping and ensures that only valid ARP requests and responses are transmitted, discarding suspicious packets.
- **RARP (Reverse ARP)**: Allows querying the IP associated with a MAC address. If more than one IP is returned, it indicates that the MAC has been cloned.



## Bibliography

- [ip neigh](https://rm-rf.es/control-de-tablas-arp-con-el-comando-ip/)
- [arp spoofing](https://www.incibe-cert.es/blog/arp-spoofing)
- [Free ARP](http://www.tranquilidadologica.com/2006/05/pagetes-arp-gratuitos.html)
- [mitigation measures](http://profesores.elo.utfsm.cl/~agv/elo323/2s14/projects/reports/MoraMorales/mitigation.html#:~:text=is%20a%20strategy%20which%20maintains,is%20a%20case%20of%20CISCO.)
