---
title: "IPV6 Tunes"
date: 2023-09-08T10:00:00+00:00
Description: In this detailed post, we explore the process of setting up IPv6 to IPv4 tunnels and vice versa in Linux and Cisco environments. As migration to IPv6 becomes important, the ability to establish communications between IPv4 and IPv6 networks becomes essential. We will cover the basic concepts of tunnel configuration, including the most common tunnel types, such as 6to4 and Teredo. In addition, we will provide step-by-step instructions for configuration on both Linux systems and Cisco devices
tags: [Redes,IPV6,IPV4,Cisco,Linux]
hero: images/redes/tuneles_ipv6/portada.png
---



In this detailed post, we explore the process of setting up IPv6 to IPv4 tunnels and vice versa in Linux and Cisco environments. As migration to IPv6 becomes important, the ability to establish communications between IPv4 and IPv6 networks becomes essential. We will cover the basic concepts of tunnel configuration, including the most common tunnel types, such as 6to4 and Teredo. In addition, we will provide step-by-step instructions for configuration on both Linux systems and Cisco devices

 ! [] (.. / img / Aspose.Words.c9cb3e7-b0e3-4eb4-b70b-2432dbadc7d8.001.jpeg) 

### 6to4 Tunes in Swan

1. They set up the Router network interfaces

♪ R1 ♪

R1 - > FastEthernet 0 / 0
- Take the network prefix - > 3333: db7:: / 64
- Link: FE80:: C801: 20FF: FE69: 0 Global: 3333: DB7:: C801: 20FF: FE69: 0

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.002.png)

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.003.png)

R1 - > FastEthernet 1 / 0

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.004.png)

R1 - > FastEthernet 2 / 0

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.005.png)

For router 1 customers will configure SLAAC:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.006.png)


* * R2 * *

R2 - > FastEthernet 0 / 0

- Take the network prefix - > 3333: db7: 1:: / 64
- Link: FE80:: C802: 20FF: FE79: 0 Global: 3333: DB7: 1: 0: C802: 20FF: FE79: 0

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.007.png)


 ! [] (.. / img / Aspose.Words.c9cb3e7-b0e3-4eb4-b70b-2432dbadc7d8.008.png) 
R2- > FastEthernet 1 / 0

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.009.png)

R2- > FastEthernet 2 / 0

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.010.png)

For router 2 customers will configure SLAAC:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.011.png)


* * R3 * *

R3 - > FastEthernet 0 / 0

- Take the network prefix - > 3333: db7: 2:: / 64
- Link: FE80:: C803: 20FF: FE89: 0 Global: 3333: DB7: 2: 0: C803: 20FF: FE89: 0

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.012.png)

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.013.png)

R3- > FastEthernet 1 / 0

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.014.png)

R3- > FastEthernet 2 / 0

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.015.png)

For router 3 customers will configure SLAAC:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.016.png)

* *\ * In this scenario we do not need to manually entrust IPV4 routes as with the configuration given on the network cards the scenario will be rolled on IPV4. * *

2 GRE Tunes

GRE is a non-secure site-to-site VPN tunneling protocol that can encapsulate a wide variety of protocol package types within IP tunnels, allowing an organization to deliver other protocols through an IP-based WAN.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.017.png)

This will allow an IPV4 header to travel through IPV4 networks on our IPV6 package.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.018.jpeg)

* * R1 - > R3 * *

We will create a tunnel interface:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.019.png)

We set the tunnel mode to GRE with IP that encapsulated our IPV6 packages within IPV4:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.020.png)

We give an IPV4 to our tunnel:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.021.png)

We set the WAN address of our router, FastEthernet 1 / 0:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.022.png)

We establish the WAN direction of the tunnel end (R2):

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.023.png)

We enable OSPF that is a dynamic routing protocol:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.024.png)

This command adds to the tunnel network to OSPF:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.025.png)

We will give an IPV6 to our tunnel, with the network prefix 2002 from the IPV4 of the 2002 router: 0A00: 0001:: 1 / 64:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.026.png)

We create the route to get to the network:

! [ref1]

We'll create a tunnel interface.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.028.png)

We set the tunnel mode to GRE with IP that encapsulated our IPV6 packages within IPV4:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.029.png)

We give an IPV4 address to our tunnel:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.030.png)

We set the WAN address of our router, FastEthernet 1 / 0.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.031.png)

We establish the WAN direction of the tunnel end (R2):

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.032.png)

We enable OSPF that is a dynamic routing protocol.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.033.png)

This command adds to the tunnel network to OSPF

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.034.png)

We will give an IPV6 to our tunnel, with the network prefix 2002 from the IPV4 of the 2002 router: 0A00: 0002:: 1 / 64:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.035.png)

We create the route to get to the network:

! [ref1]

We'll create a tunnel interface.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.036.png)

We set the tunnel mode to GRE with IP that encapsulated our IPV6 packages within IPV4:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.037.png)

We give an IPV4 address to our tunnel:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.038.png)

We set the WAN address of our router, FastEthernet 1 / 0.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.039.png)

We establish the WAN direction of the tunnel end (R2):

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.040.png)

We enable OSPF that is a dynamic routing protocol.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.041.png)

This command adds to the tunnel network to OSPF

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.042.png)

We will give an IPV6 to our tunnel, with the network prefix 2002 from the IPV4 of the 2002 router: 1400: 0001:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.043.png)

We create the route to get to the network:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.044.png)


* * R3 - > R1 * *

We'll create a tunnel interface.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.045.png)

We set the tunnel mode to GRE with IP that encapsulated our IPV6 packages within IPV4:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.046.png)

We give an IPV4 address to our tunnel:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.047.png)

We set the WAN address of our router, FastEthernet 1 / 0.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.048.png)

We establish the WAN direction of the tunnel end (R2):

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.049.png)

We enable OSPF that is a dynamic routing protocol.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.050.png)

This command adds to the tunnel network to OSPF

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.051.png)

We will give an IPV6 to our tunnel, with the network prefix 2002 from the IPV4 of the 2002 router: 1400: 0002:: 1 / 64:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.052.png)

We create the route to get to the network:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.053.png)


* * R3 - > R2 * *

We'll create a tunnel interface.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.054.png)

We set the tunnel mode to GRE with IP that encapsulated our IPV6 packages within IPV4:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.055.png)

We give an IPV4 address to our tunnel:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.056.png)

We set the WAN address of our router, FastEthernet 1 / 0.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.057.png)

We establish the WAN direction of the tunnel end (R2):

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.058.png)

We enable OSPF that is a dynamic routing protocol.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.059.png)

This command adds to the tunnel network to OSPF

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.060.png)

We will give an IPV6 to our tunnel, with the network prefix 2002 from the IPV4 of the router:

30.0.0.2 - > 2002: 1e00: 0002:: 1 / 64

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.061.png)

We create the route to get to the network:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.062.png)


♪ R2- > R3 ♪

We'll create a tunnel interface.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.063.png)

We set the tunnel mode to GRE with IP that encapsulated our IPV6 packages within IPV4:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.064.png)

We give an IPV4 address to our tunnel:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.065.png)

We set the WAN address of our router, FastEthernet 1 / 0.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.066.png)

We establish the WAN direction of the tunnel end (R2):

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.067.png)

We enable OSPF that is a dynamic routing protocol.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.068.png)

This command adds to the tunnel network to OSPF

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.069.png)

We will give an IPV6 to our tunnel, with the network prefix 2002 from the IPV4 of the router 30.0.0.1 - > 2002: 1e00: 0001:: 1 / 64:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.070.png)

We create the route to get to the network:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.071.png)



## 3 Operating checks

Let's check that the tunnels have been created for this we will introduce the following command in the three routers of our stage:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.072.png)

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.073.png)

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.074.png)

This will appear once both ends of the tunnel have been created if nothing will appear. In our case we can see that the tunnels have been successfully created.



## # # Ping

We'll check the operation of the tunnels by doing a ping.

- PC1- → 3333: db7:: e60: ddff: fea6: 0
- PC2- → 3333: db7: 1: 0: e2e: 3bff: fe83: 0
- PC3 - > 3333: db7: 2: 0: e62: 5dff: Fedf: 0

PC1 - > PC2

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.075.png)

PC1 - > PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.076.png)

PC2 - > PC1

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.077.png)

PC2- → PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.078.png)

PC3 - > PC1

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.079.png)

PC3 → PC2

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.080.png)

We see that we have connectivity between all of our stage machines with IPV6 even if we have to cross IPV4 networks.

#### Traceroute ♪

Let's check the path of the packages.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.081.png)

Trajectory following a PC1 to PC3 package:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.082.png)

Trajectory following a PC2 to PC1 package:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.083.png)

Trajectory following a PC2 to PC3 package:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.084.png)

Trajectory following a PC3 to PC1 package:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.085.png)

Trajectory following a PC3 package to PC2:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.086.png)

## 4 Study of an encapsulated package

♪ Before you go through the tunnel ♪

Package traveling from PC1 to PC2.

We see that by not having crossed the tunnel, it does not yet have IPV4 headers, it only has IPV6. We can see that the origin is PC1 and the destination is PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.087.jpeg)

We'll see how in the next section once you get through the tunnel the router will put an IPV4 header so that you can get through that section.

♪ After crossing the tunnel ♪

If you look at a package that has passed through a tunnel we can see that it has "2 levels of network":

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.088.png)

If we look at the network level, we see that the PIs of origin and destination are those of the ends of the tunnel. We also see that you use protocol 47 which means you've crossed a GRE tunnel.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.089.jpeg)

Finally we can see at the IPV6 header, which is not distinguished from one that has not crossed a tunnel.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.090.jpeg)

♪ Once you get to the target network ♪

We see that once it reaches the destination that is, once it has already travelled the IPV4 section and re-enter the IPV6 network the router will remove the IPV4 header and leave the IPV6 header for the package to reach its destination.

We see that the IPV6 header is still intact, it is the same throughout the package:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.091.jpeg)

### 6to4 Linux Tunes

 ! [] (.. / img / Aspose.Words.c9cb3e7-b0e3-4eb4-b70b-2432dbadc7d8.092.jpeg) 
### 1.Network interface configuration

I will respect the IPV4 addresses of the stage with swan.

♪ R1 ♪

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.093.jpeg)

To apply the configuration we will make a sudo systemctl restart networking.service

I will configure SLAAC to configure the customers of our IPV6 network, we will previously have to have the radvd package installed with sudo apt install radvd.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.094.png)

A set-up the service will restart radvd and our customers will automatically configure with the prefix indicated.


* * R2 * *

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.095.jpeg)

To apply the configuration we will make a sudo systemctl restart networking.service

I will configure SLAAC to configure the customers of our IPV6 network, we will previously have to have the radvd package installed with sudo apt install radvd.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.096.png)

A set-up the service will restart radvd and our customers will automatically configure with the prefix indicated.


* * R3 * *

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.097.jpeg)

To apply the configuration we will make a sudo systemctl restart networking.service

I will configure SLAAC to configure the customers of our IPV6 network, we will previously have to have the radvd package installed with sudo apt install radvd.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.098.png)

A set-up the service will restart radvd and our customers will automatically configure with the prefix indicated.

* * In this scenario it is not necessary that we confess IPV4 routes manually as with the configuration given on the network cards the scenario will be rolled on IPV4. * *

However it will be necessary for all routers to enable the forwardbit for both IPV4 and IPV6.

For this we edit the sudo nano / etc / sysctl.conf file and discomment the following lines:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.099.jpeg)

This will be repeated for each of our routers and reinitiated for the changes to be applied.

## 2.Configuration of the SIT tunnels

The operation is similar to the GRE tunnels in swan this limp our packages and through a tunnel type interface you will add an IPV4 header to enable you to cross IPV4 networks.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.100.png)

Once the tunnel is up we will tell the router that to reach the prefix of the X network you will have to use it to add the header to our packages.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.101.png)

For more comfort I have created a small script on each router with the commands necessary for the tunnel to work.

It consists of 4 commands:

1. It will create the tunnel interface with the destination and then the origin of this.
2. The network card will be lifted
3. It will assign the IPV6 to the tunnel from the IPV4 address of its origin.
4. We'll create the traffic route that used the tunnel.

We can give the tunnel the name we want in my case I have put tunnel followed by a number in order to identify them.


* * R2 Tunes * *

So would the "script" of the R2 tunnels

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.102.png)

Once the script is created, we will give you permission and execute it:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.103.png)

We will check that the interfaces have been created correctly:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.104.jpeg)

! [ref2]

Once the script is created, we will give you permission and execute it:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.106.png)

We will check that the interfaces have been created correctly:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.107.jpeg)


* * R3 Tunes * *

So would the "script" of the R3 tunnels

! [ref2]

Once the script is created, we will give you permission and execute it:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.108.png)

We will check that the interfaces have been created correctly:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.109.jpeg)



## 3.

PC1 - > 3333: db7:: e47: bfff: fe86: 0 PC2 - > 2222: db7:: ebc: f6ff: fe7d: 0 PC3 - > 4444: db7:: e43: 78ff: fec6: 0

## # # Ping

PC1 - > PC2

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.110.png)

PC1 - > PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.111.png)

PC2 - > PC1

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.112.png)

PC2 - > PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.113.png)


PC3 - > PC1

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.114.png)

PC3 - > PC2

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.115.png)

#### Traceroute ♪

Once we have checked that we have connectivity, let's see if the packages use the tunnels.

PC1 - > PC2

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.116.png)

PC1 - > PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.117.png)


PC2 - > PC1

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.118.png)

PC2 - > PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.119.png)

PC3 - > PC1

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.120.png)

PC3 - > PC2

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.121.png)

## 4 Study of an encapsulated package

♪ Before you go through the tunnel ♪

Package traveling from PC1 to PC2.

We see that by not having crossed the tunnel, it does not yet have IPV4 headers, it only has IPV6. We can see that the origin is PC1 and the destination is PC3

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.122.jpeg)

We'll see how in the next section once you get through the tunnel the router will put an IPV4 header so that you can get through that section.

♪ After crossing the tunnel ♪

If we look at a package that has passed through a tunnel we can see that it has "2 levels of network."

If we look at the network level, we see that the PIs of origin and destination are those of the ends of the tunnel. We also see that you use protocol 47 which means you've crossed a GRE tunnel.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.123.jpeg)


Finally we can see at the IPV6 header, which is not distinguished from one that has not crossed a tunnel.

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.124.jpeg)

♪ Once you get to the target network ♪

We see that once it reaches the destination that is, once it has already travelled the IPV4 section and re-enter the IPV6 network the router will remove the IPV4 header and leave the IPV6 header for the package to reach its destination.

We see that the IPV6 header is still intact, it is the same throughout the package:

![](../img/Aspose.Words.c9ccb3e7-b0e3-4eb4-b70b-2432dbadc7d8.125.jpeg)

## Bibliography

- [6to4 automatic tunnel] (https: / / community.cisco.com / t5 / blogs-general / t% C3% BAneles-autom% C3% A1ticos-6to4 / ba-p / 4822594)
- [Automatic Tunes for Ipv6] (https: / / educationadistancia.juntadeandalucia.es / centers / sevilla / pluginfile.php / 347162 / mod _ resource / content / 1 / 52470-Tunes% 20Automatiques% 20para% 20IPv6\ (1\) .pdf)
- [GRE Tunes] (https: / / ccnadesdecero.es / tuneles-gre-characteristics -and -configuration /)
- [SIT 6to4 Linux Tunes] (https: / / juncotic.com / tunel-ipv6-montando-tunel-ipv6 /)


[ref1]:.. / img / Asposer.Words.c9cb3e7-b0e3-4eb4-b70b-2432dbadc7d8.027.png
[ref2]:.. / img / Asposer.Words.c9cb3e7-b0e3-4eb4-b70b-2432dbadc7d8.105.png
