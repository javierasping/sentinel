---
title: "Underworld evolution"
date: 2023-09-08T10:00:00+00:00
description: A scenario in which we will configure routing, SNAT, DNAT, and firewalls with Linux and Windows devices.
tags: [Networking, SNAT, DNAT, Cisco, Linux]
hero: images/redes/underworld_evolution/portada.jpeg
---

The world of UNDERWORLD has evolved greatly in recent months, so you must perform network management tasks to face the new situation.

On one hand, the Internet has been discovered in the Underworld, allowing each of the sub-worlds (remember: vampires, werewolves, lycanthropes, and humans) to connect to a router that, in turn, connects them to one of the two large routers that form Underworld's Internet, called Marcus (for humans and vampires) and Alexander (for werewolves and lycanthropes). Marcus and Alexander are connected to each other.

The scheme would be as follows:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.001.jpeg)

On the other hand, the beings of the underworld have discovered a vulnerability in CISCO routers that allows them to bypass the access control lists, returning to the chaos you previously prevented with the ACLs.

Your tasks will consist of:

1. Replacing the CISCO routers in the network infrastructure with Linux machines following the scheme shown.
2. Properly configure the Linux machines to function as routers.
3. Create the necessary routing tables for all machines to communicate with each other, considering that internal networks will have private addresses and we will have public addresses on the Internet.
4. Configure the necessary firewalls on the routers so that:
   - VAMPIRES cannot communicate with the other species.
   - WEREWOLVES and LYCANTHROPES, since they are not so repulsive when they meet, can communicate with each other. They will not have communication with the other species.
   - HUMANS will also not be able to communicate with the other species.
5. Configure the DHCP service that the werewolves and lycanthropes had under the same conditions they had when using CISCO routers.
6. Configure the firewalls with the necessary rules so that, from HUMANLAND, IT KNIGHT can continue communicating with his two favorite vampires (SONJA and SELENE).
7. Perform the necessary configurations to set up a web server in HUMANLAND accessible from anywhere in UNDERWORLD.

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.002.jpeg)

## Preparation of the scenario in Linux

### Configuration of the network interfaces

The first thing we will do is add the necessary network interfaces to each router. To do this, with the machine turned off, we right-click > settings > network and add the slots that are needed for each machine:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.003.png)

We will need the following number of network interfaces for each device:

- Router 1, 2, 3, and 4: will need 2 network interfaces
- MARCUS and ALEXANDER: will need 3 network interfaces
- PCs: will need 1 network interface

Once this is done, we will edit the file /etc/network/interfaces to perform our network configuration.

Subsequently, we will restart the networking service with systemctl restart networking.service so that the network configuration we indicated is applied.

Configuration of the network interface Router 1:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.004.png)

Configuration of the network interface Router 2:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.005.png)

Configuration of the network interface Router 3:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.006.png)

Configuration of the network interface Router 4:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.007.png)

Configuration of the network interface Router MARCUS:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.008.png)

Configuration of the network interface Router ALEXANDER:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.009.png)

#### Enabling the forwarding bit

If we want to make a Linux machine act as a router, which means it routes packets that are not destined for it, we must enable the forwarding bit.

Additionally, we will take this opportunity to permanently enable the forwarding bit on the routers of the scenario by editing the file /etc/sysctl.conf and uncommenting this line:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.010.png)

We will repeat this for the six routers we have in the scenario:

**Router 1:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.011.png)

**Router 2:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.012.png)

**Router 3:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.013.png)

**Router 4:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.014.png)

**Router MARCUS:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.015.png)

**Router ALEXANDER:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.016.png)

Now all our machines are configured to act as routers and will route any packets that are sent to them that are not for them.

#### Route configuration

Here I will show if I have added any routes manually and the routing tables of the devices.

**Router MARCUS:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.017.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.018.png)

**Router ALEXANDER:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.019.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.020.png)

**Router 1:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.021.png)

**Router 2:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.022.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.023.png)

**Router 4:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.024.png)

With the network configuration I have on the interfaces, I have only added 2 manual routes on the routers of MARCUS and ALEXANDER; in the rest it was not necessary since it is generated automatically with the gateway we placed when configuring the network interfaces.

I could have saved writing them if I had placed the IP of the other as the gateway on the interface configured in the network 100.X.X.X.

#### Connectivity test

We are going to check if we have routed correctly, so I will ping from each router to each one of the edges of the scenario.

**Router 1:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.025.png)

**Router 2:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.026.png)

**Router 3:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.027.png)

**Router 4:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.028.png)

It is confirmed that we have connectivity between all routers; the PCs will not have “connectivity” until we configure the SNAT.

### DHCP Configuration

#### Lycanthropes

The lycanthropes, on their part, hire you to assign their IPs via DHCP as well, but they indicate that they cannot receive the first 10 addresses of their range (not counting the network one or the gateway), as these are reserved for the leaders of their clan who are traveling and will return in a few days.

With the machine connected to the NAT cloud and the interface that is connected configured via DHCP, we will download the DHCP server; to do this, we must first run an apt update because the machine does not have the repositories loaded in memory:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.029.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.030.png)

When it finishes installing, it will give us an error; this is because the service is not configured and does not know which interface the server should assign addresses to:

![ref1]

To do this, we will edit the file /etc/default/isc-dhcp-server and add the name of the interface in the IPV4 section:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.032.png)

Now we will configure the scope with the requirements requested by the lycanthropes by editing the file /etc/dhcp/dhcpd.conf:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.033.png)

We must keep in mind that the configuration we put here is consistent with the network configuration we have; we need to consider that we have a /28, so in this case, we can only have 14 assignable addresses.

But if we follow the statement, they do not want the first 10, so we can only assign 3 to our clients.

Once this is done, we will restart the service:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.034.png)

And we will see if it is working, checking the status:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.035.jpeg)

We will assign an IP to a PC to check that it works:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.036.png)

#### Werewolves

The werewolves, who are quite clumsy at entering IP addresses into their machines, ask you to configure the DHCP service for all their machines to receive an IP automatically.

With the machine connected to the NAT cloud and the interface that is connected configured via DHCP, we will download the DHCP server; to do this, we must first run an apt update because the machine does not have the repositories loaded in memory:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.037.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.038.png)

When it finishes installing, it will give us an error; this is because the service is not configured and does not know which interface the server should assign addresses to:

![ref1]

To do this, we will edit the file /etc/default/isc-dhcp-server and add the name of the interface in the IPV4 section:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.039.png)

Fortunately, the werewolves are less demanding, and they want the entire range of addresses distributed, so for this, we will edit the file /etc/dhcp/dhcpd.conf:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.040.png)

Now we will restart the service:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.041.png)

We will check the status to ensure that it is working correctly:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.042.jpeg)

We will assign an address to a client to make sure everything works correctly:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.043.png)

### SNAT Configuration

To complete the preparation phase, we will need to configure SNAT so that the different races can communicate with each other.

**Router 1:**

I created a file called iptables to save all the rules from the practice:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.044.png)

To demonstrate that the rule works, here is a capture between Router 1 and PC1:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.045.png)

We see that once outside the network between R1 and MARCUS, SNAT has been applied:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.046.png)


**Router 2:**

I created a file called iptables to save all the rules from the practice:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.047.png)

To demonstrate that the rule works, here is a capture between Router 2 and PC3. We see that the source is a private IP address:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.048.png)

We see that once outside the network between R2 and MARCUS, SNAT has been applied, since the source is now a public IP address:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.049.png)

**Router 3:**

I created a file called iptables to save all the rules from the practice:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.050.png)

To demonstrate that the rule works, here is a capture between Router 3 and PC5. We see that the source is a private IP address:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.051.png)

We see that once outside the network between R3 and ALEXANDER, SNAT has been applied, since the source is now a public IP address:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.052.png)

**Router 4:**

I created a file called iptables to save all the rules from the practice:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.053.png)

To demonstrate that the rule works, here is a capture between Router 4 and PC7. We see that the source is a private IP address:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.054.png)

We see that once outside the network between R4 and ALEXANDER, SNAT has been applied since the source is now a public IP address:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.055.png)

With the current scenario, any PC is capable of reaching all public addresses in our network:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.056.png)

### DNAT Configuration

For the machines to be able to communicate with each other, ssh has been installed on them, so we will need to configure DNAT.

**R1**

For this network, since we have two clients, I changed the port that ssh uses:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.057.png)

We check that I can connect to both hosts from another network, thus confirming that DNAT works.

Sonja:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.058.png)

Selene:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.059.png)

**R2**

In this network, we only have one client that we want to be accessible from the outside, so we will only have one DNAT rule:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.060.png)

To check the rule, I will connect from the vampires to the humans:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.061.png)

**R3**

In this network, since there is a DHCP service running, for the DNAT rule to function correctly, we must reserve our host or configure the interface statically.

I will do the former for convenience, for this we go to the file /etc/dhcp/dhcpd.conf and write the following:

```BASH
host ReservationName { hardware ethernet HOST_MAC_ADDR; fixed-address RESERVED_IP;}
```

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.062.png)

Once this is done, we restart the service:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.063.png)

And I will set the following rule:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.064.png)

Now let's check that I can connect to this host:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.065.jpeg)

**R4**

In this network, we will also configure a reservation on the server to keep our rules active; in this case, I will assign the address 192.168.4.5.

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.066.png)

We will restart the service and check that our host has been assigned the reserved IP; if not, we will request another with dhclient:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.067.png)

Now we will add the DNAT rule so that the ssh server can be reached:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.068.png)

We check that the rule is functioning, and we can connect from another network:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.069.jpeg)

### Firewall Configuration

#### Vampires cannot communicate with the other species

I will set a default DROP policy in the FORWARD table to block all traffic coming from the vampire network:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.070.png)

We will verify that the vampires are unable to reach the other networks:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.071.png)

We can see the hits it has made to confirm that the rule is working:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.072.png)

#### Allow communication between Werewolves and Lycanthropes

WEREWOLVES and LYCANTHROPES, since they are not so repulsive when they cross paths, will be able to communicate with each other. They will not have communication with the other species.

I will set a default DROP policy in the FORWARD table, then allow traffic that comes in through interface ens4 and goes out through ens5, and vice versa to permit traffic between these two networks:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.073.png)

We see that they can communicate with each other; however, they cannot access Humans or Vampires:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.074.jpeg)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.075.jpeg)

We will check that the rules have hits:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.076.png)

#### HUMANS will also not be able to communicate with the other species

With the rules we currently have, communication between Humans and other species is not possible; we can see that in R2 without any additional rules, we cannot connect:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.077.png)

We see that we cannot communicate:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.078.png)

If we want to prohibit human traffic on our router and not rely on external rules in case they change, we will add a default DROP policy:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.079.png)

We will see the hits in the default policy:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.080.png)

#### Configure the necessary rules in the firewalls so that, from HUMANLAND, IT KNIGHT can continue communicating with his two favorite vampires (SONJA and SELENE).

The IPs of these machines are:

- IT KNIGHT (SSH) –> 192.168.2.3:22
- SONJA (SSH) –> 192.168.1.4:22    
- SELENE (SSH) –> 192.168.1.5:2222 

In router 1, the necessary rules to allow this communication are:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.081.jpeg)

In router 2, the necessary rules to allow this communication are:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.082.jpeg)

We will check action by action to ensure that these rules fulfill their purpose.

**SELENE –> ITKNIGHT**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.083.png)

In router 1:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.084.jpeg)

In router 2:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.085.jpeg)

**SONJA –> ITKNIGHT**

We ssh:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.086.png)

We see the hits from router 1:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.087.jpeg)

We see the hits from router 2 (same rule as the previous section):

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.088.jpeg)

**ITKNIGHT –> SONJA**

We ssh:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.089.png)

We see the hits from router 1:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.090.jpeg)

We see the hits from router 2:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.091.jpeg)

**ITKNIGHT –> SELENE**

We launch the ssh:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.092.png)

We see the hits from router 1:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.093.jpeg)

We see the hits from router 2:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.094.jpeg)

### HUMANLAND Web Server

Perform the necessary configurations to set up a web server in HUMANLAND accessible from anywhere in UNDERWORLD.

I have assigned it the IP 192.168.2.10.

The first thing we must configure is the DNAT on router R2 (HUMANLAND):

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.095.png)

Now in router 2, we will allow requests to the server and their responses:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.096.png)

In router 1, we allow requests and their responses:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.097.png)

Finally, in ALEXANDER, we allow web requests to pass through:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.098.png)

Let's check that it can be accessed from all networks.

**VAMPIRES:**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.099.png)

We check the hits in router 1:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.100.png)

**WEREWOLVES AND LYCANTHROPES**

We make the web request from both networks:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.101.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.102.png)

We check the hits in router ALEXANDER:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.103.jpeg)

Finally, we see the hits in Router 2 (HUMANS) for the DNAT rule:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.104.png)

## Scenario with Cisco routers

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.105.jpeg)

### Configuration of the interfaces

**R1**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.106.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.107.png)

**R2**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.108.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.109.png)

**R3**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.110.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.111.png)

**R4**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.112.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.113.png)

**MARCUS**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.114.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.115.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.116.png)

**ALEXANDER**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.117.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.118.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.119.png)

#### Routing Tables

**R1**

We add the default route:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.120.png)

Thus, R1's routing table will look like:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.121.png)

**R2**

We add the default route:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.122.png)

Thus, R2's routing table will look like:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.123.png)

**R3**

We add the default route:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.124.png)

Thus, R3's routing table will look like:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.125.png)

**R4**

We add the default route:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.126.png)

Thus, R4's routing table will look like:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.127.png)

**MARCUS**

We add the default route:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.128.png)

Thus, MARCUS's routing table will look like:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.129.png)

**ALEXANDER**

We add the default route:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.130.png)

Thus, ALEXANDER's routing table will look like:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.131.png)

#### Connectivity Test 

We will check that we have routed correctly, so I will ping from each router to each of the edges of the scenario.

R1 → to the edges:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.132.png)

R2 → to the edges:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.133.png)

R3 → to the edges:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.134.jpeg)

R4 → to the edges:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.135.png)


### DHCP Configuration Lycanthropes

The lycanthropes, on their part, hire you to assign their IPs via DHCP as well, but they indicate that they cannot receive the first 10 addresses of their range (not counting the network one or the gateway), as these are reserved for the leaders of their clan who are traveling and will return in a few days.

The first thing we will do is establish the range of excluded IPs from the set (pool) of addresses that the service will assign by indicating the initial and final IP of the range, both included:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.136.png)

We name the DHCP service range:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.137.png)

We define the network to which it will provide DHCP service:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.138.png)

We include the gateway that will offer the service:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.139.png)

With this, we would have set up the DHCP server. With the following command, we can view the service statistics to see if it is running:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.140.png)

We will also confirm that the lease has been granted to our host:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.141.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.142.jpeg)

### DHCP Werewolves

The werewolves, who are quite clumsy at entering IP addresses into their machines, ask you to configure the DHCP service for all their machines to receive an available IP automatically.

In the previous section, I detailed each part of the configuration of a DHCP server in Cisco; here I show you the configuration for the Werewolf network:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.143.png)

We will check that it is working:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.144.png)

### SNAT Configuration

**Router 1:**

The first step is to create an ACL to allow the traffic we want to perform SNAT on:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.145.png)

We will assign this rule to the internal interface of our network:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.146.png)

Now we will create a pool with the public IPs; the command would be this, but it does not show completely in the terminal:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.147.png)

We enable NAT:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.148.png)

We indicate which interface is for “inside”:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.149.png)

We specify the “outside” interface:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.150.png)

The SNAT should be working, so let's verify it:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.151.png)

We see that the rule has HITS:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.152.png)


**Router 2:**

The first step is to create an ACL to allow the traffic we want to perform SNAT on:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.153.png)

We will assign this rule to the internal interface of our network:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.154.png)

Now we will create a pool with the public IPs; the command would be this, but it does not show completely in the terminal:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.155.png)

We enable NAT:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.156.png)

We indicate which interface is for “inside”:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.157.png)

We specify the “outside” interface:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.158.png)

The SNAT should be working, so let's verify it by checking if the rule has HITS:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.159.png)


**Router 3:**

The first step is to create an ACL to allow the traffic we want to perform SNAT on:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.160.png)

We will assign this rule to the internal interface of our network:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.161.png)

Now we will create a pool with the public IPs; the command would be this, but it does not show completely in the terminal:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.162.png)

We enable NAT:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.163.png)

We indicate which interface is for “inside”:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.164.png)

We specify the “outside” interface:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.165.png)

The SNAT should be working, so let's verify it by checking if the rule has HITS:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.166.png)


**Router 4:**

The first step is to create an ACL to allow the traffic we want to perform SNAT on:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.167.png)

We will assign this rule to the internal interface of our network:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.168.png)

Now we will create a pool with the public IPs; the command would be this, but it does not show completely in the terminal:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.169.png)

We enable NAT:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.170.png)

We indicate which interface is for “inside”:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.171.png)

We specify the "outside" interface:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.172.png)

The SNAT should be working, so let's verify it by checking if the rule has HITS:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.173.png)

### DNAT Configuration

**R1**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.174.png)

Checking:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.175.png)

**R2**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.176.png)

Checking:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.177.png)

**R3**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.178.png)

Checking:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.179.png)

**R4**

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.180.png)

Checking:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.181.png)

### Firewall Configuration

#### Vampires cannot communicate with the other species

For this, we will delete the existing rule in the list:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.182.png)

Now we will deny outgoing traffic from the vampire network:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.183.png)

We confirm they cannot communicate:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.184.png)

We look at the hits from the rules:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.185.png)

#### Allow communication between Werewolves and Lycanthropes

WEREWOLVES and LYCANTHROPES, since they are not so repulsive when they cross paths, will be able to communicate with each other. They will not have communication with the other species.

With these two rules, we allow any host from our local networks to exit when the destination is werewolves or lycanthropes:

- R3 → 180.0.0.1   
- R4 → 190.0.0.1

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.186.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.187.png)

We see that it blocks the packets that are not from HL to LC or from LC to HL:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.188.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.189.png)

#### HUMANS will also not be able to communicate with the other species

With the rules we currently have, communication with other species by humans is not possible; we can see that in R2 without any additional rules, we cannot connect since our packets will reach the networks.

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.190.png)

To truly prevent humans from communicating without depending on the rules of the other kingdoms, we will prevent them from exiting the kingdom:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.191.png)

If we check now, they will not be able to exit the kingdom:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.192.png)

We look at the hits:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.193.png)

#### Configure the necessary rules in the firewalls so that, from HUMANLAND, IT KNIGHT can continue communicating with his two favorite vampires (SONJA and SELENE).

The IPs of these machines are:

- IT KNIGHT (SSH) –> 192.168.2.3:22
- SONJA (SSH) –> 192.168.1.4:22    
- SELENE (SSH) –> 192.168.1.5:2222 

To allow the vampires to communicate with humans:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.194.png)

We allow outgoing messages to the public of the vampires when the port is 22 and 2222:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.195.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.196.png)

Now we will allow the vampires to connect to the humans using port 22:

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.197.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.198.png)

![](/redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.199.jpeg)

I don’t know why it’s not working... it only goes through if I don’t place any rules; even allowing ALL SSH traffic doesn’t help... I have also allowed all ICMP, but it still occurs. 

The nat and SNAT are working fine, but when it comes to making the ssh rules, the following happens in the local network. Since the router drops them back despite the traffic being allowed.

[ref1]: /redes/underworld_evolution/img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.031.jpeg