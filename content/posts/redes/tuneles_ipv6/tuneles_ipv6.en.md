---
title: "IPv6 Tunnels"
date: 2023-09-08T10:00:00+00:00
description: "In this detailed post, we explore the process of configuring IPv6 to IPv4 tunnels and vice versa in Linux and Cisco environments. As the migration to IPv6 gains importance, the ability to establish communication between IPv4 and IPv6 networks becomes essential. We will cover the basics of tunnel configuration, including the most common types of tunnels, such as 6to4 and Teredo. Additionally, we will provide step-by-step instructions for configuration on both Linux systems and Cisco devices."
tags: [Networking, IPv6, IPv4, Cisco, Linux]
hero: images/redes/tuneles_ipv6/portada.png
---

## Introduction

In this detailed post, we explore the process of configuring IPv6 to IPv4 tunnels and vice versa in Linux and Cisco environments. As the migration to IPv6 gains importance, the ability to establish communication between IPv4 and IPv6 networks becomes essential. We will cover the basics of tunnel configuration, including the most common types of tunnels, such as 6to4 and Teredo. Additionally, we will provide step-by-step instructions for configuration on both Linux systems and Cisco devices.

## 6to4 Tunnels in Cisco

### 1. Configuration of Router Network Interfaces

#### R1

- **FastEthernet 0/0**  
  - Network Prefix: `3333:db7::/64`  
  - Link: `FE80::C801:20FF:FE69:0`  
  - Global: `3333:DB7::C801:20FF:FE69:0`

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.002.png)

- **FastEthernet 1/0**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.004.png)

- **FastEthernet 2/0**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.005.png)

For R1 router clients, we will configure SLAAC:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.006.png)

#### R2

- **FastEthernet 0/0**  
  - Network Prefix: `3333:db7:1::/64`  
  - Link: `FE80::C802:20FF:FE79:0`  
  - Global: `3333:DB7:1:0:C802:20FF:FE79:0`

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.007.png)

- **FastEthernet 1/0**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.009.png)

- **FastEthernet 2/0**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.010.png)

For R2 router clients, we will configure SLAAC:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.011.png)

#### R3

- **FastEthernet 0/0**  
  - Network Prefix: `3333:db7:2::/64`  
  - Link: `FE80::C803:20FF:FE89:0`  
  - Global: `3333:DB7:2:0:C803:20FF:FE89:0`

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.012.png)

- **FastEthernet 1/0**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.014.png)

- **FastEthernet 2/0**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.015.png)

For R3 router clients, we will configure SLAAC:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.016.png)

> **Note:** In this scenario, it is not necessary to manually configure IPv4 routes, as the network interface configuration will make IPv4 traffic routable.

## 2. GRE Tunnels

GRE is an unsecured site-to-site VPN tunneling protocol that can encapsulate a wide variety of protocol packets within IP tunnels. This allows an organization to transmit other protocols over an IP-based WAN.

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.017.png)

This allows adding an IPv4 header to an IPv6 packet so it can travel over IPv4 networks.

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.018.jpeg)

#### R1 → R3

We will create a tunnel interface:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.019.png)

# GRE Tunnel Configuration with IPv6 over IPv4

We set the tunnel mode to GRE with IP, which will encapsulate our IPv6 packets within IPv4:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.020.png)

We assign an IPv4 address to our tunnel:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.021.png)

We set the WAN address of our router, FastEthernet 1/0:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.022.png)

We set the WAN address of the tunnel endpoint (R2):

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.023.png)

We enable OSPF, which is a dynamic routing protocol:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.024.png)

This command adds the tunnel network to OSPF:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.025.png)

We assign an IPv6 address to our tunnel, with the network prefix `2002` based on the router's IPv4 address `2002:0A00:0001::1/64`:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.026.png)

We create the route to reach the network:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.044.png)

We create a tunnel interface:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.028.png)

We set the tunnel mode to GRE with IP, which will encapsulate our IPv6 packets within IPv4:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.029.png)

We assign an IPv4 address to our tunnel:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.030.png)

We set the WAN address of our router, FastEthernet 1/0:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.031.png)

We set the WAN address of the tunnel endpoint (R2):

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.032.png)

We enable OSPF, which is a dynamic routing protocol:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.033.png)

This command adds the tunnel network to OSPF:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.034.png)

We assign an IPv6 address to our tunnel, with the network prefix `2002` based on the router's IPv4 address `2002:0A00:0002::1/64`:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.035.png)

We create the route to reach the network:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.044.png)

We create a tunnel interface:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.036.png)

We set the tunnel mode to GRE with IP, which will encapsulate our IPv6 packets within IPv4:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.037.png)

We assign an IPv4 address to our tunnel:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.038.png)

We set the WAN address of our router, FastEthernet 1/0:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.039.png)

We set the WAN address of the tunnel endpoint (R2):

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.040.png)

We enable OSPF, which is a dynamic routing protocol:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.041.png)

This command adds the tunnel network to OSPF:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.042.png)

We assign an IPv6 address to our tunnel, with the network prefix `2002` based on the router's IPv4 address `2002:1400:0001`:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.043.png)

We create the route to reach the network:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.044.png)

## **R3 → R1**

We create a tunnel interface:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.045.png)

We set the tunnel mode to GRE with IP, which will encapsulate our IPv6 packets within IPv4:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.046.png)

We assign an IPv4 address to our tunnel:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.047.png)

We set the WAN address of our router, FastEthernet 1/0:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.048.png)

We set the WAN address of the tunnel endpoint (R2):

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.049.png)

We enable OSPF, which is a dynamic routing protocol:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.050.png)

This command adds the tunnel network to OSPF:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.051.png)

We assign an IPv6 address to our tunnel, with the network prefix `2002` based on the router's IPv4 address `2002:1400:0002::1/64`:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.052.png)

We create the route to reach the network:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.053.png)

---

## **R3 → R2**

We create a tunnel interface:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.054.png)

We set the tunnel mode to GRE with IP, which will encapsulate our IPv6 packets within IPv4:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.055.png)

We assign an IPv4 address to our tunnel:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.056.png)

We set the WAN address of our router, FastEthernet 1/0:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.057.png)

We set the WAN address of the tunnel endpoint (R2):

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.058.png)

We enable OSPF, which is a dynamic routing protocol:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.059.png)

This command adds the tunnel network to OSPF:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.060.png)

We assign an IPv6 address to our tunnel, with the network prefix `2002` based on the router's IPv4 address `30.0.0.2 → 2002:1e00:0002::1/64`:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.061.png)

We create the route to reach the network:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.062.png)

---

## **R2 → R3**

We create a tunnel interface:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.063.png)

We set the tunnel mode to GRE with IP, which will encapsulate our IPv6 packets within IPv4:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.064.png)

We assign an IPv4 address to our tunnel:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.065.png)

We set the WAN address of our router, FastEthernet 1/0:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.066.png)

We set the WAN address of the tunnel endpoint (R2):

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.067.png)

We enable OSPF, which is a dynamic routing protocol:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.068.png)

This command adds the tunnel network to OSPF:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.069.png)

We assign an IPv6 address to our tunnel, with the network prefix `2002` based on the router's IPv4 address `30.0.0.1 → 2002:1e00:0001::1/64`:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.070.png)

We create the route to reach the network:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.071.png)

---

### 3. Functionality Verification

We will verify that the tunnels have been created. To do this, we will enter the following command on the three routers in our scenario:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.072.png)

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.073.png)

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.074.png)

This will appear once both ends of the tunnel have been created. If not, nothing will appear. In our case, we can see that the tunnels have been successfully created.

---

#### Ping

We will verify the functionality of the tunnels by performing a ping.

- **PC1 → 3333:db7::e60:ddff:fea6:0**
- **PC2 → 3333:db7:1:0:e2e:3bff:fe83:0**
- **PC3 → 3333:db7:2:0:e62:5dff:fedf:0**

**PC1 → PC2**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.075.png)

**PC1 → PC3**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.076.png)

**PC2 → PC1**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.077.png)

**PC2 → PC3**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.078.png)

**PC3 → PC1**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.079.png)

**PC3 → PC2**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.080.png)

We can see that we have connectivity between all the machines in our scenario using IPv6, even though we have to traverse IPv4 networks.

---

#### Traceroute

We will verify the path that the packets follow.

**Path of a packet from PC1 to PC2:**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.081.png)

**Path of a packet from PC1 to PC3:**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.082.png)

**Path of a packet from PC2 to PC1:**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.083.png)

**Path of a packet from PC2 to PC3:**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.084.png)

**Path of a packet from PC3 to PC1:**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.085.png)

**Path of a packet from PC3 to PC2:**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.086.png)

---

### 4. Study of an Encapsulated Packet

**Before Passing Through the Tunnel**

A packet traveling from PC1 to PC2.

We can see that, since it has not yet passed through the tunnel, it does not have IPv4 headers, only IPv6. We can see that the source is PC1 and the destination is PC3:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.087.jpeg)

We will see how, in the next segment, once it passes through the tunnel, the router will add an IPv4 header so it can traverse that segment.

---

## **After Passing Through the Tunnel**

If we look at a packet that has passed through a tunnel, we can see that it has "2 network layers":

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.088.png)

If we look at the network layer, we see that the source and destination IPs are those of the tunnel endpoints. Additionally, we see that it uses protocol 47, which means it has passed through a GRE tunnel.

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.089.jpeg)

Finally, we can see in the IPv6 header that it is indistinguishable from one that has not passed through a tunnel.

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.090.jpeg)

---

## **Once It Reaches the Destination Network**

We see that, once it reaches the destination (i.e., after traversing the IPv4 segment and re-entering the IPv6 network), the router will remove the IPv4 header and leave the IPv6 header so the packet can reach its destination.

We see that the IPv6 header remains intact; it is the same throughout the packet's journey:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.091.jpeg)

---

## 6to4 Tunnels in Linux

### 1. Network Interface Configuration

I will respect the IPv4 addresses from the Cisco scenario.

#### **R1**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.093.jpeg)

To apply the configuration, we will run `sudo systemctl restart networking.service`.

I will configure SLAAC to set up the clients on our IPv6 network. First, we need to install the `radvd` package with `sudo apt install radvd`.

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.094.png)

Once the service is configured, we will restart `radvd`, and our clients will automatically configure themselves with the specified prefix.

#### **R2**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.095.jpeg)

To apply the configuration, we will run `sudo systemctl restart networking.service`.

I will configure SLAAC to set up the clients on our IPv6 network. First, we need to install the `radvd` package with `sudo apt install radvd`.

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.096.png)

Once the service is configured, we will restart `radvd`, and our clients will automatically configure themselves with the specified prefix.

#### **R3**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.097.jpeg)

To apply the configuration, we will run `sudo systemctl restart networking.service`.

I will configure SLAAC to set up the clients on our IPv6 network. First, we need to install the `radvd` package with `sudo apt install radvd`.

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.098.png)

Once the service is configured, we will restart `radvd`, and our clients will automatically configure themselves with the specified prefix.

---

**Note:** In this scenario, it is not necessary to manually configure IPv4 routes, as the network interface configuration will make IPv4 traffic routable.

However, it will be necessary to enable the forwarding bit for both IPv4 and IPv6 on all routers.

To do this, we edit the file `sudo nano /etc/sysctl.conf` and uncomment the following lines:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.099.jpeg)

We will repeat this for each of our routers and reboot to apply the changes.

---

### 2. SIT Tunnel Configuration

The operation is similar to GRE tunnels in Cisco. This will take our packets and, through a tunnel interface, add an IPv4 header so they can traverse IPv4 networks.

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.100.png)

Once the tunnel is up, we will tell the router that to reach the prefix of network X, it must use this tunnel to add the header to our packets.

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.101.png)

For convenience, I have created a small script on each router with the necessary commands to make the tunnel work.

It consists of 4 commands:

1. It will create the tunnel interface with the destination and then the source.
2. It will bring up the network interface.
3. It will assign the IPv6 address to the tunnel based on the source IPv4 address.
4. We will create the route for the traffic that will use the tunnel.

We can name the tunnel as we wish. In my case, I have named it `tunnel` followed by a number to identify them.

---

## **R2 Tunnels**

This is what the "script" for R2 tunnels would look like:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.102.png)

Once the script is created, we will give it permissions and execute it:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.103.png)

We will verify that the interfaces have been created correctly:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.104.jpeg)

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.105.jpeg)

---

## **R3 Tunnels**

This is what the "script" for R3 tunnels would look like:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.106.png)

Once the script is created, we will give it permissions and execute it:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.107.png)

We will verify that the interfaces have been created correctly:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.108.jpeg)

---

### 3. Functionality Verification

- **PC1 → 3333:db7::e47:bfff:fe86:0**
- **PC2 → 2222:db7::ebc:f6ff:fe7d:0**
- **PC3 → 4444:db7::e43:78ff:fec6:0**

#### Ping

**PC1 → PC2**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.109.png)

**PC1 → PC3**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.110.png)

**PC2 → PC1**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.111.png)

**PC2 → PC3**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.112.png)

**PC3 → PC1**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.113.png)

**PC3 → PC2**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.114.png)

---

#### Traceroute

Once we have verified connectivity, we will check if the packets use the tunnels.

**PC1 → PC2**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.115.png)

**PC1 → PC3**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.116.png)

**PC2 → PC1**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.117.png)

**PC2 → PC3**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.118.png)

**PC3 → PC1**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.119.png)

**PC3 → PC2**

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.120.png)

---

### 4. Study of an Encapsulated Packet

#### **Before Passing Through the Tunnel**

A packet traveling from PC1 to PC2.

We can see that, since it has not yet passed through the tunnel, it does not have IPv4 headers, only IPv6. We can see that the source is PC1 and the destination is PC3:

<!-- ![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.121.jpeg) -->

We will see how, in the next segment, once it passes through the tunnel, the router will add an IPv4 header so it can traverse that segment.

---

#### **After Passing Through the Tunnel**

If we look at a packet that has passed through a tunnel, we can see that it has "2 network layers".

If we look at the network layer, we see that the source and destination IPs are those of the tunnel endpoints. Additionally, we see that it uses protocol 47, which means it has passed through a GRE tunnel.

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.122.jpeg)

Finally, we can see in the IPv6 header that it is indistinguishable from one that has not passed through a tunnel.

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.123.jpeg)

---

#### **Once It Reaches the Destination Network**

We see that, once it reaches the destination (i.e., after traversing the IPv4 segment and re-entering the IPv6 network), the router will remove the IPv4 header and leave the IPv6 header so the packet can reach its destination.

We see that the IPv6 header remains intact; it is the same throughout the packet's journey:

![](/redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.124.jpeg)

---

## Bibliography

- [6to4 Automatic Tunnels](https://community.cisco.com/t5/blogs-general/t%C3%BAneles-autom%C3%A1ticos-6to4/ba-p/4822594)
- [Automatic Tunnels for IPv6](https://educacionadistancia.juntadeandalucia.es/centros/sevilla/pluginfile.php/347162/mod_resource/content/1/52470-Tuneles%20Automaticos%20para%20IPv6\(1\).pdf)
- [GRE Tunnels](https://ccnadesdecero.es/tuneles-gre-caracteristicas-y-configuracion/)
- [SIT 6to4 Tunnels in Linux](https://juncotic.com/tunel-ipv6-montando-tunel-ipv6/)

[ref1]: /redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.027.png
[ref2]: /redes/tuneles_ipv6/img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.105.png