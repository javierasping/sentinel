---
title: "Underworld"
date: 2023-09-08T10:00:00+00:00
description: Scenario de routación y acls en cisco
tags: [Redes, Wireshark, GNS3,Cisco,Enrutamiento,ACLS]
hero: /images/redes/underworld/portada_underwolrd.webp
---



## Introduction
You live in UNDERWORLD. In your world, different types of species are presented for a single purpose, "crossing" each other. These creatures are:

- VAMPIROS
- LICANTROPOS: werewolves with the ability to return to their human state.
- LOBO MEN: werewolves who, after their first conversion to wolf, could not return to their human state.

- Human: some shit.
- YOU: a computer warrior with superpowers like turning around a game that has not yet gone out on the market or having the power to become invisible when he comes out of the party and tries to court a female by telling her some kind of phrases: do you want me to compile the baby kernel?

The aspect of UNDERWORLD is as follows:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.001.jpeg)

### 1. Engage the stage

### "paper" routing tables



- 124; HUMAN ROUTER - 124; - 124; - 124;
- - - - - - -
- 124; 192\ .168.1.0 / 24 - 124; 0\ .0.0.0 - 124; F0 / 0 - 124;
- 124; 192\ .168.2.0 / 24 - 124; 0\ .0.0.0 - 124; F1 / 0 - 124;
- 124; 192\ .168.3.0 / 24 - 124; 192\ .168.2.2 - 124; F1 / 0 - 124;
- 124; 192\ .168.4.0 / 24 - 124; 192\ .168.2.2 - 124; F1 / 0 - 124;
- 124; 192\ .168.5.0 / 24 - 124; 192\ .168.2.2 - 124; F1 / 0 - 124;
- 124; 192\ .168.6.0 / 24 - 124; 192\ .168.2.2 - 124; F1 / 0 - 124;
- 124; 192\ .168.7.0 / 24 - 124; 192\ .168.2.2 - 124; F1 / 0 - 124;
- 124; 0\ .0.0.0 / 0 - 124; 192\ .168.2.2 - 124; F1 / 0 - 124;

----------------------------------------------------


- 124; ROUTER VAMPIROS - 124; - 124; - 124;
- - - - - - -
- 124; 192\ .168.1.0 / 24 - 124; 192\ .168.2.1 - 124; F1 / 0 - 124;
- 124; 192\ .168.2.0 / 24 - 124; 0\ .0.0.0 - 124; F1 / 0 - 124;
- 124; 192\ .168.3.0 / 24 - 124; 0\ .0.0.0 - 124; F0 / 0 - 124;
- 124; 192\ .168.4.0 / 24 - 124; 0\ .0.0.0 - 124; F2 / 0 - 124;
- 124; 192\ .168.5.0 / 24 - 124; 192\ .168.4.2 - 124; F2 / 0 - 124;
- 124; 192\ .168.6.0 / 24 - 124; 192\ .168.4.2 - 124; F2 / 0 - 124;
- 124; 192\ .168.7.0 / 24 - 124; 192\ .168.4.2 - 124; F2 / 0 - 124;
- 124; 0\ .0.0.0 / 0 - 124; 192\ .168.4.2 - 124; F2 / 0 - 124;

----------------------------------------------------

- 124; - 124; - 124;
- - - - - - -
- 124; 192\ .168.1.0 / 24 - 124; 192\ .168.4.1 - 124; F2 / 0 - 124;
- 124; 192\ .168.2.0 / 24 - 124; 192\ .168.4.1 - 124; F2 / 0 - 124;
- 124; 192\ .168.3.0 / 24 - 124; 192\ .168.4.1 - 124; F2 / 0 - 124;
- 124; 192\ .168.4.0 / 24 - 124; 0\ .0.0.0 - 124; F2 / 0 - 124;
- 124; 192\ .168.5.0 / 24 - 124; 0\ .0.0.0 - 124; F0 / 0 - 124;
- 124; 192\ .168.6.0 / 24 - 124; 0\ .0.0.0 - 124; F1 / 0 - 124;
- 124; 192\ .168.7.0 / 24 - 124; 192\ .168.6.2 - 124; F1 / 0 - 124;
- 124; 0\ .0.0.0 / 0 - 124; 192\ .168.4.1 - 124; F1 / 0 - 124;

----------------------------------------------------

- 124;
- - - - - - -
- 124; 192\ .168.1.0 / 24 - 124; 192\ .168.6.1 - 124; F1 / 0 - 124;
- 124; 192\ .168.2.0 / 24 - 124; 192\ .168.6.1 - 124; F1 / 0 - 124;
- 124; 192\ .168.3.0 / 24 - 124; 192\ .168.6.1 - 124; F1 / 0 - 124;
- 124; 192\ .168.4.0 / 24 - 124; 192\ .168.6.1 - 124; F1 / 0 - 124;
- 124; 192\ .168.5.0 / 24 - 124; 192\ .168.6.1 - 124; F1 / 0 - 124;
- 124; 192\ .168.6.0 / 24 - 124; 0\ .0.0.0 - 124; F1 / 0 - 124;
- 124; 192\ .168.7.0 / 24 - 124; 0\ .0.0.0 - 124; F0 / 0 - 124;
- 124; 0\ .0.0.0 / 0 - 124; 192\ .168.6.1 - 124; F1 / 0 - 124;



#2 Configuring Ips interfaces addresses

### Human router

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.002.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.003.png)

We save the configuration:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.004.png)

### Router vampires

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.005.jpeg)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.006.png)

We save the configuration:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.007.png)

### Router licanthrops

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.008.jpeg)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.009.png)

We save the configuration:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.010.png)

### Router vampires

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.011.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.012.png)

We save the configuration:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.013.png)



#3. Adding the routing table to the routers

### Human router

We will create by default the routes to the networks we are connected we will only need to add the default route:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.014.png)

We'd have the routing table:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.015.png)

We save the configuration:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.016.png)

### Router vampires

We will add the following routes:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.018.png)

So the routing table would be:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.017.png)

We save the configuration:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.019.png)


### Router licanthrops

We add the following routes:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.020.png)

So our routing table would be:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.021.png)

We save the configuration:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.022.png)

### Router werewolves

We add the following routes:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.023.png)

So our routing table would be:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.024.png)

We save the configuration:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.025.png)



## 4.Rash test

In order not to make this section very extensive, check that from PC1 it reaches all PCs:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.026.png)



## 5.ACLs configuration

Everyone uses the network to send out messages and hook up (so you will have to set up the network to make this possible at first, that is, that all the equipment has a connection with each other). You, who are already up to the\ * #%?! of so much freak as a result of the crosses that occur when a vampire intersects for example with a licanthrope and their son with a werewolf and so on, you decide to end the story by doing the following, putting a few ACLs into the routers that communicate them:

1. * * VAMPIROS cannot communicate with other species * *

We create the rule to deny network traffic 192.168.3.0:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.027.png)

We apply it to the FastEthernet 0 / 0 interface (192.168.3.1) and we apply it to the output of this:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.028.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.029.png)

We'll check that the Vampire Network PCs can't communicate with the rest, tells us there's an ACL cutting us off:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.030.jpeg)

If from any other kingdom we communicate with them the messages will be able to reach them however the answer will not come as the ACL prevents it, the answer is cut off as it comes out of the vampire network:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.031.png)

2. * * LOBO MEN and LICANTROPOS, since they are not so repulsive when they cross, can communicate with each other. The other species will have no communication. * *

This section can give you different solutions, I have chosen to put an ACL, in the F2 / 0 interface of the licanthropy router.

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.032.jpeg)

We create the ACL:

And we apply the output of the F2 / 0 output interface:! [ref1]! [ref2]

We'll check that the ACL works, doing pings between the machines.

From PC7 we see that it does not allow us to leave the route of licanthropy, it cuts the communication but however we can reach the other networks:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.035.jpeg)

From PC5 we can see the same result:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.036.jpeg)

From PC1 we see that we do not get an answer as we are only cutting off the output traffic by preventing the "inside" machines from communicating with those outside.

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.037.png)

* * Human will not be able to communicate with the other species * *

With the current ACLs scheme it would not be necessary to implement a new rule as with the current scheme it is not possible to communicate with them. Even if the messages PC1 makes reach its destination, it will receive no response.

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.038.png)

But if we still want to prevent humans from sending messages to others from their network we will implement the following rule in their router:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.039.png)

Now we're cutting the human messages from Router 1:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.040.jpeg)

## 6.DHCP Server

In the end you decide to do business with rare species because they have no idea of computer and you are hired by these evil entities to carry out the following tasks:

♪ Werewolves ♪

The werewolves who are quite donkeys by putting IP addresses into their machines, ask you to set them up the DHCP service so that all their machines automatically receive a free IP:

We will have to take the following steps:

1. The exclusive ip dhcp command - address 192.168.7.1 - > We point out the addresses that we do not want to be distributed by DHCP, that is the exclusions.
1. The command ip dhcp pool HOMBRES\ _ LOBO we name the range of addresses that we are distributing
1. It will get us into the range configuration, now we tell you the network that we want you to share the network addresses 192.168.7.0 255.255.255.0
1. Now we'll tell you which gateway we want you to assign default-router 192.168.7.1
1. If we wanted to set up a DNS server, for example the google server would be so dns-server 8.8.8.8

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.041.png)

We can see that the DHCP server is working properly with the parameters we have indicated above:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.042.png)

* * Licanthropy * *

The licanthrops, on their part, hire you to assign them also for DHCP their IPs, but they tell you that they cannot receive the first 10 addresses of their rank (not counting the network or the link door), as these are reserved for the heads of their clan who are on their way and will return in a few days.

We declare the ips we're going to exclude:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.043.png)

We name the range of addresses that we are distributing in order to configure it:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.044.png)

We tell you the network that we want you to share the addresses:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.045.png)

Now we'll tell you which gateway we want you to assign:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.046.png)

We'll check that the dhcp server is working:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.047.png)

## 7.ACLs modification

♪ Let the vampires hook up ♪

From so much doing business with vampires, you look at a couple of vampires that are very good to see and you'd like to be able to send them little messages from the villa you just bought in HUMANLAND with the pasture you're taking out of the poor "criaturics." Your IP is 192.168.1.4 and that of SELENE and SONJA is 192.168.3.4 and 192.168.3.5 respectively. Add a machine to HUMANLAND for your equipment called IT KNIGHT and 2 machines called SELENE and SONJA with the above-mentioned PIs in TRANSILVANIA.

If we want to do this we must set up advanced ACLs to control the origin and destination of the packages.

The syntax is quite simple in this case:

allow ip IP\ _ ORIGEN WILDCARD IP\ _ We will create the ACL for humans:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.048.png)

We will also create the ACL for vampires:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.049.png)

We will apply it to the input interface in each network, both are the FastEthernet 0 / 0:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.050.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.051.png)

* *\ * * * We must have previously removed the list assigned to the interface if it will not give an error, to remove it is the same command as to put it in a no in front.

We will now check the effectiveness of these rules that we have implemented:

* * IT KNIGHT - > SELENE and SONJA * *

We see that it only allows us to traffic to these two specific host as we have indicated in our ACLs

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.052.jpeg)

♪ * SELENE - > IT KNIGHT * *

We see that it only allows us to traffic to these two specific host as we have indicated in our ACLs, if we try to communicate with another host will cut the traffic the ACL:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.053.png)

* * SONJA- > IT KNIGHT * *

We see that it only allows us to traffic to these two specific host as we have indicated in our ACLs, if we try to communicate with another host will cut the traffic the ACL:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.054.png)

We can also see the ACL statistics on the router by looking at the rule hits to see if they are working:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.055.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.056.png)

Although in none of the lists we have specified in deny any, it would not be necessary as it is implied, that is by default by not complying with any rule to discard the traffic.

#8. Web server

Since you can't hook up on UNDERWORLD, they're all more boring than a garlic, so you decide to put an internal WEB server on UNDERWORLD. Add to the PUENTE 1 router, a server called FICHEROS that will have IP 192.168.8.2 / 24, creating the necessary ACLs for the entire UNDERWORLD community to be entertained by seeing some cool websites.

The first will be to set up the new interface of the human router:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.057.png)

The following will be to configure for our current scheme in the VAMPIROS router the route to the new network so that the scenario is routed correctly:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.058.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.059.png)

Finally we will set up the ip of our debian in a static way with the address 192.168.8.2:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.060.png)

We will also install apache (we will have to do it previously connected to the NAT cloud):

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.061.png)

Once we already have the web server prepared and routed in our stage, we will modify the different ACLs so that they can only reach the web server by port 80.

In the router of humans we add the following rule, which allows all traffic to host 192.168.8.2 that goes to port 80:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.062.png)

In order to refresh the list and to have the changes applied, we must reassign it to the router:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.063.png)

We will now do the same with the vampire router as it has extended ACLs as well as humans:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.064.png)

Now we're going to set up an advanced ACL for the licanthrops and werewolves:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.065.png)

Let's check that we can NOT ping the server from the VPCs:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.066.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.067.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.068.png)

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.069.png)

In short we have maintained the above rules but we have allowed the traffic to the web server as long as it comes through port 80, so we cannot do it ping.

Let's check that we can access the web server from the networks: - > HUMAN:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.070.jpeg)

- > VAMPIROS:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.071.jpeg)


- > LICANTROPOS:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.072.jpeg)

- > LOBO MEN:

![](../images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.073.jpeg)


[ref1]:.. / images / Asposer.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.033.png
[ref2]:.. / images / Asposer.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.034.png
