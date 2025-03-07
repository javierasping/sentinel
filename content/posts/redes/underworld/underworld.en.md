---
title: "Underworld"
date: 2023-09-08T10:00:00+00:00
description: "Routing and ACLs scenario in Cisco."
tags: [Networking, Wireshark, GNS3, Cisco, Routing, ACLs]
hero: /images/redes/underworld/portada_underwolrd.webp
---

## Introduction

You live in UNDERWORLD. In your world, there are different types of species with one goal: to "crossbreed" with each other. These creatures are:

- **VAMPIRES**
- **WEREWOLVES (LICÁNTROPOS):** Werewolves with the ability to return to their human form.
- **WOLFMEN (HOMBRES LOBO):** Werewolves who, after their first transformation, cannot return to their human form.
- **HUMANS:** Some annoying little creatures.
- **YOU:** A tech-savvy warrior with superpowers like turning around a game that hasn't even been released yet or having the ability to become invisible when going out to party and trying to flirt with a girl by saying things like: "Do you want me to compile your kernel, babe?"

The layout of UNDERWORLD is as follows:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.001.jpeg)

---

## 1. Routing the Scenario

### Routing Tables on Paper

| **ROUTER HUMANO**       |               |          |
|-------------------------|---------------|----------|
| 192.168.1.0/24          | 0.0.0.0       | F0/0     |
| 192.168.2.0/24          | 0.0.0.0       | F1/0     |
| 192.168.3.0/24          | 192.168.2.2   | F1/0     |
| 192.168.4.0/24          | 192.168.2.2   | F1/0     |
| 192.168.5.0/24          | 192.168.2.2   | F1/0     |
| 192.168.6.0/24          | 192.168.2.2   | F1/0     |
| 192.168.7.0/24          | 192.168.2.2   | F1/0     |
| 0.0.0.0/0               | 192.168.2.2   | F1/0     |

------------------------------------------------

| **ROUTER VAMPIROS**     |               |          |
|-------------------------|---------------|----------|
| 192.168.1.0/24          | 192.168.2.1   | F1/0     |
| 192.168.2.0/24          | 0.0.0.0       | F1/0     |
| 192.168.3.0/24          | 0.0.0.0       | F0/0     |
| 192.168.4.0/24          | 0.0.0.0       | F2/0     |
| 192.168.5.0/24          | 192.168.4.2   | F2/0     |
| 192.168.6.0/24          | 192.168.4.2   | F2/0     |
| 192.168.7.0/24          | 192.168.4.2   | F2/0     |
| 0.0.0.0/0               | 192.168.4.2   | F2/0     |

------------------------------------------------

| **ROUTER LICÁNTROPOS**  |               |          |
|-------------------------|---------------|----------|
| 192.168.1.0/24          | 192.168.4.1   | F2/0     |
| 192.168.2.0/24          | 192.168.4.1   | F2/0     |
| 192.168.3.0/24          | 192.168.4.1   | F2/0     |
| 192.168.4.0/24          | 0.0.0.0       | F2/0     |
| 192.168.5.0/24          | 0.0.0.0       | F0/0     |
| 192.168.6.0/24          | 0.0.0.0       | F1/0     |
| 192.168.7.0/24          | 192.168.6.2   | F1/0     |
| 0.0.0.0/0               | 192.168.4.1   | F1/0     |

------------------------------------------------

| **ROUTER HOMBRE LOBO**  |               |          |
|-------------------------|---------------|----------|
| 192.168.1.0/24          | 192.168.6.1   | F1/0     |
| 192.168.2.0/24          | 192.168.6.1   | F1/0     |
| 192.168.3.0/24          | 192.168.6.1   | F1/0     |
| 192.168.4.0/24          | 192.168.6.1   | F1/0     |
| 192.168.5.0/24          | 192.168.6.1   | F1/0     |
| 192.168.6.0/24          | 0.0.0.0       | F1/0     |
| 192.168.7.0/24          | 0.0.0.0       | F0/0     |
| 0.0.0.0/0               | 192.168.6.1   | F1/0     |

---

## 2. Configuring IP Addresses on Interfaces

### Human Router

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.002.png)

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.003.png)

Save the configuration:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.004.png)

### Vampire Router

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.005.jpeg)

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.006.png)

Save the configuration:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.007.png)

### Werewolf Router

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.008.jpeg)

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.009.png)

Save the configuration:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.010.png)

### Wolfman Router

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.011.png)

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.012.png)

Save the configuration:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.013.png)

---

## 3. Adding Routing Tables to the Routers

### Human Router

By default, it will create routes to the networks we are connected to. We only need to add the default route:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.014.png)

The routing table will look like this:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.015.png)

Save the configuration:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.016.png)

### Vampire Router

Add the following routes:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.018.png)

The routing table will look like this:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.017.png)

Save the configuration:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.019.png)

### Werewolf Router

Add the following routes:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.020.png)

The routing table will look like this:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.021.png)

Save the configuration:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.022.png)

### Wolfman Router

Add the following routes:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.023.png)

The routing table will look like this:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.024.png)

Save the configuration:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.025.png)

---

## 4. Routing Test

To keep this section concise, I will verify that PC1 can reach all PCs:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.026.png)

---

## 5. Configuring ACLs

Everyone uses the network to send messages and flirt (so you must configure the network to allow this initially, meaning all devices can communicate with each other). However, you are fed up with all the weird creatures resulting from crossbreeding (e.g., when a vampire mates with a werewolf, and their offspring mates with a wolfman, and so on). You decide to put an end to this by implementing ACLs on the routers:

1. **VAMPIRES cannot communicate with the other species.**

Create a rule to deny traffic from the 192.168.3.0 network:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.027.png)

Apply it to the FastEthernet 0/0 interface (192.168.3.1) and apply it to the outgoing traffic:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.028.png)

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.029.png)

Verify that PCs in the Vampire network cannot communicate with the others. The ACL blocks the traffic:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.030.jpeg)

If any other realm tries to communicate with them, the messages will reach them, but the response will not, as the ACL blocks outgoing traffic from the Vampire network:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.031.png)

2. **WEREWOLVES and WOLFMEN, since they are not as repulsive when they crossbreed, can communicate with each other. They cannot communicate with the other species.**

For this section, we can implement different solutions. I opted to add an ACL on the F2/0 interface of the Werewolf router.

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.032.jpeg)

Create the ACL:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.033.png)

Apply it to the outgoing traffic on the F2/0 interface:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.034.png)

Verify that the ACL works by pinging between machines.

From PC7, we see that we cannot leave the Werewolf router, as it blocks the communication, but we can reach other networks:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.035.jpeg)

From PC5, we observe the same result:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.036.jpeg)

From PC1, we see no response, as we are only blocking outgoing traffic, preventing internal machines from communicating with external ones:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.037.png)

3. **HUMANS cannot communicate with the other species.**

With the current ACL setup, it is not necessary to implement a new rule, as communication with them is already impossible. Although messages from PC1 may reach their destination, they will not receive a response.

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.038.png)

However, if we still want to prevent humans from sending messages to others from their network, we will implement the following rule on their router:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.039.png)

Now we are blocking messages from humans on Router 1:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.040.jpeg)

---

## 6. DHCP Server

Finally, you decide to do business with the weird creatures because they have no clue about IT. You are hired by these evil entities to perform the following tasks:

**Wolfmen**

The Wolfmen, who are terrible at assigning IP addresses to their machines, ask you to configure the DHCP service so that all their machines automatically receive a free IP.

We need to follow these steps:

1. Use the command `ip dhcp excluded-address 192.168.7.1` to specify the addresses we do not want to distribute via DHCP (exclusions).
2. Use the command `ip dhcp pool WOLFMEN` to name the range of addresses we are distributing.
3. Enter the configuration for the range and specify the network we want to distribute: `network 192.168.7.0 255.255.255.0`.
4. Specify the default gateway: `default-router 192.168.7.1`.
5. If we want to configure a DNS server, for example, Google's: `dns-server 8.8.8.8`.

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.041.png)

We can verify that the DHCP server is working correctly with the parameters we specified earlier:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.042.png)

**Werewolves**

The Werewolves also hire you to assign their IPs via DHCP, but they inform you that they cannot receive the first 10 addresses of their range (excluding the network and gateway addresses), as these are reserved for their clan leaders who are traveling and will return in a few days.

Declare the IPs to exclude:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.043.png)

Name the range of addresses we are distributing to configure it:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.044.png)

Specify the network we want to distribute:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.045.png)

Specify the default gateway:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.046.png)

Verify that the DHCP server is working:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.047.png)

---


We will create the ACL for humans:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.048.png)

We will also create the ACL for Vampires:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.049.png)

We will apply it to the inbound interface on each network, both are FastEthernet 0/0:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.050.png)

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.051.png)

**\***We must have previously removed the list assigned to the interface; otherwise, it will throw an error. To remove it, use the same command as to assign it, but add a `no` in front.

Now we will verify the effectiveness of these rules we have implemented:

**IT KNIGHT → SELENE and SONJA**

We can see that it only allows traffic to these two specific hosts, as we specified in our ACLs:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.052.jpeg)

**SELENE → IT KNIGHT**

We can see that it only allows traffic to these two specific hosts, as we specified in our ACLs. If we try to communicate with another host, the ACL will block the traffic:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.053.png)

**SONJA → IT KNIGHT**

We can see that it only allows traffic to these two specific hosts, as we specified in our ACLs. If we try to communicate with another host, the ACL will block the traffic:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.054.png)

We can also check the ACL statistics on the router by looking at the rule hits to see if they are working:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.055.png)

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.056.png)

Although we have not explicitly specified `deny any` in any of the lists, it is not necessary because it is implicit. By default, if no rule is matched, the traffic will be discarded.

---

## 8. Web Server

Since flirting is no longer allowed in UNDERWORLD, everyone is bored out of their minds. So, you decide to set up an internal web server in UNDERWORLD. Add a server called FILES to the BRIDGE 1 router with the IP 192.168.8.2/24, creating the necessary ACLs so that the entire UNDERWORLD community can entertain themselves by browsing some cool websites.

First, we will configure the new interface on the Human router:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.057.png)

Next, we will configure the route to the new network on the Vampire router to ensure proper routing in the scenario:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.058.png)

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.059.png)

Finally, we will configure the IP of our Debian server statically with the address 192.168.8.2:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.060.png)

We will also install Apache (you must do this while connected to the NAT cloud):

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.061.png)

Once the web server is ready and routed in our scenario, we will modify the different ACLs so that traffic can only reach the web server on port 80.

On the Human router, we add the following rule, which allows all traffic to the host 192.168.8.2 on port 80:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.062.png)

To refresh the list and apply the changes, we must reassign it to the router:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.063.png)

Now we will do the same on the Vampire router, as it has extended ACLs configured like the Humans:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.064.png)

Now we will configure an advanced ACL for the Werewolves and Wolfmen:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.065.png)

We will verify that we **cannot** ping the server from the VPCs:

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.066.png)

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.067.png)

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.068.png)

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.069.png)

In summary, we have maintained the previous rules but allowed traffic to the web server only if it comes through port 80. That’s why we cannot ping it.

Now we will verify that we can access the web server from the networks:

**→ HUMANS:**

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.070.jpeg)

**→ VAMPIRES:**

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.071.jpeg)

**→ WEREWOLVES:**

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.072.jpeg)

**→ WOLFMEN:**

![](/redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.073.jpeg)

[ref1]: /redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.033.png
[ref2]: /redes/underworld/images/Aspose.Words.0cb93ef6-f4fa-4538-a812-68ecd45de766.034.png