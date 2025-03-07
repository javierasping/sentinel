---
title: "DHCP server configuration under debian"
date: 2023-09-08T10:00:00+00:00
Description: DHCP server configuration in our basic scenario under debian 10
tags: [Servicios,NAT,SMR,DHCP,SNAT]
hero: images/servicios/dhcp_v4/isc-dhcp.webp
---


# DHCP server configuration under debian
In this article you will learn how to configure the DHCP is-dhcp-server. In addition, you will set up a reservation and configure it to work in two areas.
### Isc-dhcp-server installation
To install our dhcp server we run:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.015.png)

It will give us the following error as it is not configured:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.016.png)


### Configuration of is-dhcp-server

The first thing we have to do is set up the network interface that the dhcp server will work for, for this we edit the following file:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.017.png)

And we add our interface that will deliver addresses:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.018.png)

Configure the dhcp server with the following features:

- Range of addresses to be distributed: 192.168.0.100 - 192.168.0.110
- Network mask: 255.255.255.0
- Duration of the concession: 1 hour
- Liaison door: 192.168.0.1
- DNS servers: 8.8.8.8

For this we edit the following file:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.019.png)


We now add the following:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.020.png)

Here we are configuring our scope according to the statement.

We will now have to restart the service with the following command:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.021.png)

### Configuration of customers for dynamic steering

We will edit the network configuration to use the dhcp:

In the debian we edit the network / interfaces:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.022.png)

Now we reboot the network card:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.023.png)

Now we'll check if we're assigned ip with ipconfig:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.024.png)

We see that it has been assigned correctly. We will repeat the same with our client windows.

We set up the network card to use the dhcp protocol, restart the card and check the ip you have assigned us:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.025.png)

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.026.png)







Now let's check the address concessions for it we'll have to see the following file. We'll open it with cat because it's important not to edit it, it can cause trouble.

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.027.png)

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.028.png)







### Book an IP address
For this we will need to edit the configuration file of our dhcp server:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.029.png)

Once here we will add the following lines:

- Name of reservation
- Ethernet hardware: It is the MAC address of the host's network card.
- fix

Our reservation would remain this way (we will put it out of the configuration of our field):

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.030.png)

Now we'll start the service again.

We will check that the concession has been made, for that we will go to windows. We may have to renew the concession or restart the network card.

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.031.png)

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.032.png)



Let's check what happens to the client configuration in certain circumstances, for this we'll put a very low concession time. I'll give you a minute.

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.033.png)

1. Customers take a configuration, and then we turn off the dhcp server. What about the window client? What about the Linux client?

In windows we will be assigned an address of APIPA

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.034.png)

While in Linux it does not assign me any ip address, though then I assign an APIPA address

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.035.png)





### What happens when we modify the configuration?
Customers take a configuration, and then we change the dhcp server settings (e.g. range). What about the window client? What about the Linux client?

We change the range:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.036.png)

And we restart the service

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.037.png)

With windows I keep the booking address:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.038.png)

And with Linux we are assigned the direction of the new range:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.039.png)






### Configure Two Ambit
Make the necessary modifications to the current configuration of our dhcp server to share ip addresses to two different networks, the 192.168.0.0 and the 192.168.2.0.

The first thing we will do is add a fourth network card and set it up manually. If we don't know the name of the interface we can see it with ip to:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.040.png)

We will now set it static, following the statement and add it to / etc / default / isch-dhcp-server.

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.041.png)

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.042.png)

And we set our second range:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.043.png)

We now restart the service:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.044.png)


I will now add several network cards to my client to check the concessions and set up the cards:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.045.png)

And we would have been given ip address in both ranges:

![](/servicios/dhcp/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.046.png)



