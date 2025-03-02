---
title: "Underworld evolution"
date: 2023-09-08T10:00:00+00:00
Description: Scenario in which we will configure the routing, SNAT, DNAT and firewall with Linux and Windows devices.
tags: [Redes, SNAT ,DNAT , Cisco , Linux]
hero: images/redes/underworld_evolution/portada.jpeg
---



The world of UNDERWORLD has evolved a lot in recent months, so you have to do network management tasks to deal with the new situation.

On the one hand, the Internet has been discovered in the Underworld, so that each of the subworlds (remember: vampires, licanthros, werewolves and humans) is connected to a router that, in turn, connects them to one of the two great routers that form the Underworld Internet, called Marcus (for humans and vampires) and Alexander (for werewolves and licanthrops). Marcus and Alexander are connected to each other.

The scheme would be as follows:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.001.jpeg)

On the other hand, the underworld beings have discovered a vulnerability in the CISCO routers that allows them to skip the access control lists, returning to the chaos you managed to prevent in their day with the ACL.


Your task will then be to:

1. Replace CISCO routers with Linux machines in the network infrastructure following the figure's scheme.
2. Configure Linux machines properly to function as routers.
3. Create the routing tables necessary for all machines to communicate with all in principle, taking into account that the internal networks will have private addresses and on the Internet we will have public addresses.
4. Configure the necessary firewalls in the routers to:
- VAMPIROS cannot communicate with the other species.
- LOBO MEN and LICANTROPOS, since they are not so repulsive when they cross, can communicate with each other. The other species will have no communication.
- Nor can they communicate with other species.
5. Configure the DHCP service that werewolves and licanthrops had under the same conditions as they had when using CISCO routers.
6. Configure in the firewalls the rules necessary for it to continue to communicate with its two favorite vampires (SONJA AND SELENE).
7. It makes the settings necessary to mount a web server on HUMANLAND accessible from anywhere in UNDERWORLD.

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.002.jpeg)


### Stage preparation in Linux

### Network card configuration

The first thing we will do is to add the necessary network cards to each router, so with the machine off we do on the same right click > configuration > network and add the slots that are necessary for each machine:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.003.png)

We will need the following number of network cards for each device:

- Router 1, 2, 3 and 4: You will need 2 network cards
- MARCUS and ALEXANDER: You will need 3 network cards
- PCs: You will need 1 network card

Once this is done we will edit the / etc / network / interfaces file to perform our network configuration.

We will then relaunch the network service with systemctl restart networking.service to apply the network configuration we have indicated.

Router 1 network card configuration:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.004.png)

Router 2 network card configuration:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.005.png)

Router 3 network card configuration:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.006.png)

Router 4 network card configuration:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.007.png)

Router MARCUS network card configuration:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.008.png)

Network card configuration Router ALEXANDER:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.009.png)


### Activate the forward bit

If we want to make a Linux machine act as a router, that is to say to enroute the packages that do not have as their destination this will have to activate the forwarding bit.

We will also take advantage to activate the forwarding bit permanently on the stage routers for this purpose we edit the / etc / sysctl.conf file and discomment this line:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.010.png)

This will be repeated for the 6 routers we have on stage:

* * Router 1: * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.011.png)

* * Router 2: * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.012.png)

* * Router 3: * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.013.png)

♪ Router 4: ♪

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.014.png)

* * Router MARCUS: * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.015.png)

* * Router ALEXANDER: * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.016.png)

Now all of our machines are configured to act as routers and direct the packages that come to you and are not for this.

## # # Route configuration

Here I will show you if I have added any route manually and the routing tables of the devices.

* * Router MARCUS: * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.017.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.018.png)

* * Router ALEXANDER: * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.019.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.020.png)

* * Router 1: * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.021.png)

* * Router 2: * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.022.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.023.png)

♪ Router 4: ♪

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.024.png)

Having the network configuration I have on the cards I have only added 2 manual routes, in the routers of MARCUS and ALEXANDER in the rest it has not been necessary as it is generated automatically with the link door we have placed when setting the network interfaces.

I could have saved myself from writing them if I had placed them on the interface that is configured in the 100.X.X.X network the ip address of the other as a gateway.

## # Connectivity test

Let's check that we've done the routing correctly so I'm going to throw a ping from each router to each of the ends of the stage.

* * Router 1: * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.025.png)

* * Router 2: * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.026.png)

* * Router 3: * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.027.png)

♪ Router 4: ♪

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.028.png)

It is proven that we have connectivity between all routers, PCS cannot have "connectivity" until we entrust the SNAT.

DHCP configuration

### 
The licanthrops, on their part, hire you to assign them also for DHCP their IPs, but they tell you that they cannot receive the first 10 directions of their rank (not counting the network or the link door), as these are reserved for the heads of their clan who are on their way and will return in a few days.

With the NAT cloud-connected machine and the DHCP-configured card we will download the DHCP server, for this we will first have to make an apt update as the machine does not carry the repositories loaded in memory:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.029.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.030.png)

When you have just installed it will give us an error, this is because the service is not configured and does not know why the interface has to distribute the server addresses:

! [ref1]

To do this we will edit the / etc / default / isch-dhcp-server file and add the card name in the IPV4 section:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.032.png)

We will now set the scope with the requirements that the licanthrops ask us to do so we will edit the / etc / dhcp / dhcpd.conf file:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.033.png)

We will have to keep in mind that the configuration we put here is consistent with the network configuration we have, we have to keep in mind that we have a / 28 so in this case we can only have 14 assigned directions.

But if we follow the statement the first 10 do not want them so we can only assign 3 to our customers.

Once this is done, we will restart the service:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.034.png)

And we'll see if it's working, seeing the state:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.035.jpeg)

We will assign ip to a PC to check that it works:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.036.png)

### Werewolves

The werewolves who are quite donkeys putting IP addresses into their machines, ask you to set up the DHCP service for all their machines to automatically receive a free IP.

With the NAT cloud-connected machine and the DHCP-configured card we will download the DHCP server, for this we will first have to make an apt update as the machine does not carry the repositories loaded in memory:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.037.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.038.png)

When you have just installed it will give us an error, this is because the service is not configured and does not know why the interface has to distribute the server addresses:

! [ref1]

To do this we will edit the / etc / default / isch-dhcp-server file and add the card name in the IPV4 section:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.039.png)


Luckily werewolves are less demanding and they want their full range of addresses to be shared so we will edit the / etc / dhcp / dhcpd.conf file:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.040.png)

We will now restart the service:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.041.png)

We'll check the state of it to check that it's working properly:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.042.jpeg)

We will assign an address to a client to make sure that everything works properly:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.043.png)

## # SNAT configuration

To complete the preparation phase we will need to configure SNAT so that different races can communicate with each other.

* * Router 1: * *

I have created a file called iptables to save all the rules of practice:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.044.png)

To prove that the rule works, here is a capture between Router 1 and PC1:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.045.png)

We see that once out of the network between R1 and MARCUS has been applied SNAT:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.046.png)


* * Router 2: * *

I have created a file called iptables to save all the rules of practice:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.047.png)

To prove that the rule works, here we see a capture between Router 2 and PC3. We see that the origin is a private ip address:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.048.png)

We see that once off the network between R2 and MARCUS has been applied SNAT, as the origin is now an ip public address:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.049.png)

* * Router 3: * *

I have created a file called iptables to save all the rules of practice:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.050.png)

To prove that the rule works, here we see a capture between Router 3 and PC5. We see that the origin is a private ip address:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.051.png)

We see that once off the network between R3 and ALEXANDER has been applied SNAT, as the origin is now an ip public address:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.052.png)

♪ Router 4: ♪

I have created a file called iptables to save all the rules of practice:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.053.png)

To prove that the rule works, here we see a capture between Router 4 and PC7. We see that the origin is a private ip address:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.054.png)

We see that once off the network between R4 and ALEXANDER has been applied SNAT, as the origin is now an ip public address:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.055.png)

With the current scenario any PC is able to reach all the public addresses of our network:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.056.png)

## # DNAT configuration

So the machines can communicate with each other if ssh has been installed, so we'll have to set up the DNAT.

♪ R1 ♪

For this network as we have two customers I have changed the port using the ssh:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.057.png)

We check that I can connect to both host from another network, so we see that the DNAT works.

Sonja:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.058.png)

Selene:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.059.png)

* * R2 * *

In this network we only have one client that we want to be able to access from outside so we will only have one DNAT rule:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.060.png)

To check the rule, I'll get in from vampires to humans:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.061.png)

* * R3 * *

In this network there is a DHCP service running for the DNAT rule to work properly we must make a reservation to our host or set up the card in a static way.

I will do the first thing for comfort, for this we address the / etc / dhcp / dhcpd.conf file and write the following:

```BASH
host NombreDeLaReserva { hardware ethernet DIR_MAC_HOST; fixed-address IP_RESERVA;}
```

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.062.png)

Once this has been done, we restart the service:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.063.png)

And I'll put the following rule:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.064.png)


Now let's check that I can connect to this host:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.065.jpeg)

* * R4 * *

In this network we will also set up a reservation on the server to keep our rules active, in this case I will assign you the address 192.168.4.5.

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.066.png)

We will restart the service and check that our host has assigned the booking ip, otherwise we will request another with dhclient:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.067.png)

We will now add the DNAT rule so that you can reach the ssh server:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.068.png)

We check that the rule is working and we can connect from another network:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.069.jpeg)


### Firewall configuration

### Vampires cannot communicate with other species

I'll put a DROP default policy on the FORWARD table to pull all the traffic from the vampire network:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.070.png)

We'll check that vampires are unable to reach the other networks:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.071.png)

We can see the hits you've done to see that the rule is working:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.072.png)


## # Allow communication between Lobo and Licanthropy Men

LOBO MEN and LICANTROPOS, since they are not so repulsive when they cross, can communicate with each other. The other species will have no communication.

I will put a DROP default policy on the FORWARD table and then allow traffic to enter through the ens4 interface and exit through ens5, and the inverse to allow traffic between this two networks:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.073.png)

We see that they can communicate with each other, but they cannot access the Humans or the Vampires:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.074.jpeg)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.075.jpeg)

We'll check that the rules have hits:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.076.png)

## # # Human will also not be able to communicate with the other species

With the rules that we currently have communication with other species by humans is not possible, we can see that in R2 without any additional rule we cannot connect:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.077.png)

We see that we cannot communicate:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.078.png)

If we want to ban traffic in our router and not depend on external rules in case they change we will add a default DROP policy:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.079.png)

We'll see the hits in the default policy:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.080.png)


### Configure in the firewalls the rules necessary for it to continue to communicate with its two favorite vampires (SONJA AND SELENE).

The ips of these machines are:

- IT KNIGHT (SSH) - > 192.168.2.3: 22
- SONJA (SSH) - > 192.168.1.4: 22
- SELENE (SSH) - > 192.168.1.5: 2222

In router 1 the rules necessary to allow this communication are:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.081.jpeg)

In router 2 the rules necessary to allow this communication are:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.082.jpeg)


We're gonna go check action to action to make sure these rules do their job.

♪ * SELENE - > ITKNIGHT * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.083.png)

In router 1:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.084.jpeg)

In router 2:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.085.jpeg)


* * SONJA - > ITKNIGHT * *

We do ssh:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.086.png)

We see the hits of router 1:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.087.jpeg)

We see the hits of router 2 (Same rule as the previous paragraph):

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.088.jpeg)

* * ITKNIGHT - > SONJA * *

We do ssh:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.089.png)

We see the hits of router 1:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.090.jpeg)

We see the hits of router 2:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.091.jpeg)


♪ * ITKNIGHT - > SELENE * *
 
We launch the ssh:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.092.png)

We see the hits of router 1:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.093.jpeg)

We see the hits of router 2:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.094.jpeg)

## Humanand web server

It makes the settings necessary to mount a web server on HUMANLAND accessible from anywhere in UNDERWORLD.

I've given this one the ip 192.168.2.10.

The first thing we have to set up is the DNAT in the R2 router (HUMALAND):

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.095.png)

Now in router 2 we will allow requests to be received to the server and its answers:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.096.png)

In router 1 we allow you to make requests and your answers:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.097.png)

To end on ALEXANDER we allow you to cross web requests:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.098.png)

Let's check that they can be accessed from all networks.

### WOMAN: ♪

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.099.png)

We checked the hits in router 1:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.100.png)

♪ * HOME LOBO AND LICANTROPOS * *

We make the web request from both networks:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.101.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.102.png)

We checked the ALEXANDER router hits:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.103.jpeg)

Finally we see the hits in Router 2 (HUMAN) of the DNAT rule

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.104.png)

### Scenario with Cisco routers

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.105.jpeg)

### Configuration of interfaces

♪ R1 ♪

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.106.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.107.png)

* * R2 * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.108.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.109.png)

* * R3 * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.110.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.111.png)

* * R4 * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.112.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.113.png)

♪ MARCUS ♪

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.114.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.115.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.116.png)

* * ALEXANDER * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.117.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.118.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.119.png)

### Rupture tables

♪ R1 ♪

We add the default route:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.120.png)

So would the R1 routing table:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.121.png)

* * R2 * *

We add the default route:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.122.png)

So would the R2 routing table:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.123.png)

* * R3 * *

We add the default route:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.124.png)

So would the R3 routing table:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.125.png)

* * R4 * *

We add the default route:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.126.png)

So would the R4 routing table:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.127.png)

♪ MARCUS ♪

We add the default route:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.128.png)

So there would be the MARCUS routing table:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.129.png)

* * ALEXANDER * *

We add the default route:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.130.png)

This would include the ALEXANDER routing table:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.131.png)



## # Connectivity test

Let's check that we've done the routing correctly so I'm going to throw a ping from each router to each of the ends of the stage.

R1 → To the ends:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.132.png)

R2 → To the ends:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.133.png)

R3 - > to the ends:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.134.jpeg)

R4 - > to extremes

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.135.png)


## # Licanthropic DHCP configuration

The licanthrops, on their part, hire you to assign them also for DHCP their IPs, but they tell you that they cannot receive the first 10 directions of their rank (not counting the network or the link door), as these are reserved for the heads of their clan who are on their way and will return in a few days.

The first thing we will do is to establish the range of IP's excluded from the set (pool) addresses that the service can assign indicating the initial and final ip of the range, both including:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.136.png)

We name the DHCP service range:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.137.png)

We define the network to which DHCP will serve:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.138.png)

We include the link door that the service will offer:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.139.png)

With this we would already have mounted the DHCP server, with the following command we can see the service statistics to see if it is working:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.140.png)

We will check to others that the concession to our host has been made:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.141.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.142.jpeg)

## # DHCP werewolves

The werewolves who are quite donkeys putting IP addresses into their machines, ask you to set up the DHCP service for all their machines to automatically receive a free IP.

In the above section I detail each section of the configuration of a swan DHCP server, here I show you the configuration for the Lobo Man network:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.143.png)

We'll check that it's working:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.144.png)

## # SNAT configuration

* * Router 1: * *

The first thing we will do is create an acl to allow the traffic we want to do SNAT:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.145.png)

We will assign to the internal interface of our network this rule:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.146.png)

Now we will create a pool with public ips, the command would be this does not come full in the terminal:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.147.png)

We activate the NAT:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.148.png)

We indicate that interface is "inside":

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.149.png)

We indicate the "out" interface:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.150.png)

The SNAT would be working, so let's check it out:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.151.png)

We see that the rule has HITS:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.152.png)


* * Router 2: * *

The first thing we will do is create an acl to allow the traffic we want to do SNAT:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.153.png)

We will assign to the internal interface of our network this rule:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.154.png)

Now we will create a pool with public ips, the command would be this does not come full in the terminal:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.155.png)

We activate the NAT:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.156.png)

We indicate that interface is "inside":

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.157.png)

We indicate the "out" interface:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.158.png)

The SNAT would be working, so let's check it out if the rule has HITS:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.159.png)


* * Router 3: * *

The first thing we will do is create an acl to allow the traffic we want to do SNAT:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.160.png)

We will assign to the internal interface of our network this rule:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.161.png)

Now we will create a pool with public ips, the command would be this does not come full in the terminal:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.162.png)

We activate the NAT:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.163.png)

We indicate that interface is "inside":

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.164.png)

We indicate the "out" interface:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.165.png)

The SNAT would be working, so let's check it out if the rule has HITS:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.166.png)


♪ Router 4: ♪

The first thing we will do is create an acl to allow the traffic we want to do SNAT:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.167.png)

We will assign to the internal interface of our network this rule:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.168.png)

Now we will create a pool with public ips, the command would be this does not come full in the terminal:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.169.png)

We activate the NAT:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.170.png)

We indicate that interface is "inside":

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.171.png)

We indicate the "out" interface:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.172.png)

The SNAT would be working, so let's check it out if the rule has HITS:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.173.png)



## # DNAT configuration

♪ R1 ♪

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.174.png)

Check:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.175.png)

* * R2 * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.176.png)

Check:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.177.png)

* * R3 * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.178.png)

Check:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.179.png)

* * R4 * *

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.180.png)

Check:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.181.png)



### Firewall configuration

### Vampires cannot communicate with other species

For this we will delete the existing rule in the list:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.182.png)

We will now deny the outflow of the vampire network:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.183.png)

We check that they cannot communicate:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.184.png)

We look at the hits of the rules:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.185.png)


## # Allow communication between Lobo and Licanthropy Men

LOBO MEN and LICANTROPOS, since they are not so repulsive when they cross, can communicate with each other. The other species will have no communication.

With these two rules we allow any host of our local networks to leave when the destination is the werewolves or the licanthrops:

- R3- → 180.0.0.1
- R4 - > 190.0.0.1

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.186.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.187.png)

We see that he throws us packages that don't go from HL to LC or from LC to HL:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.188.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.189.png)

## # # Human will also not be able to communicate with the other species

With the rules that we currently have communication with other species by humans is not possible, we can see that in R2 without any additional rule we cannot connect as our packages reached the networks.

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.190.png)

So that humans cannot truly communicate without depending on the rules of the demos kingdoms, we will prevent them from leaving the kingdom:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.191.png)

If we check now they will not be able to leave the kingdom:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.192.png)

We look at the hits:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.193.png)

### Configure in the firewalls the rules necessary for it to continue to communicate with its two favorite vampires (SONJA AND SELENE).

The ips of these machines are:

- IT KNIGHT (SSH) -- > 192.168.2.3: 22
- SONJA (SSH) -- > 192.168.1.4: 22
- SELENE (SSH) -- > 192.168.1.5: 2222

To allow vampires to go out and communicate with humans:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.194.png)

We allow the messages out to the public of vampires when the port is 22 and 2222:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.195.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.196.png)

Now let vampires be able to connect to humans using port 22:

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.197.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.198.png)

![](../img/Aspose.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.199.jpeg)

I don't know why it doesn't work.. it only goes if I don't place any rules even allowing ALL the ssh traffic either... I've also allowed all the ICMP but nothing is happening the same.

The nat and the SNAT are working well but when making the ssh rules the following happens on the local network when they are sent back the router cuts them even though the traffic is allowed

[ref1]:.. / img / Asposer.Words.04ad4cb2-a1f8-43f3-8027-b24afbf6f8f8.01.jpeg
