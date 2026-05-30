---
title: "NAT Cisco and Linux Configuration"
date: 2023-09-08T10:00:00+00:00
description: Routing in a scenario with public addresses, configuring SNAT and DNAT on Linux and Cisco machines.
tags: [Networking, Routing, NAT, SNAT, DNAT, Cisco, Linux]
hero: images/redes/configuracion_nat/portada.png
---

In this article, we will explore the configuration of SNAT (Source Network Address Translation) and DNAT (Destination Network Address Translation) in scenarios involving public addresses, using Linux-based routers and Cisco devices.

## Scenario with Debian Machines

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.001.jpeg)

### Environment Setup

#### Package Installation

Once the machines are deployed, we must install Apache on the web servers. To do this, we connect both servers to a switch, which is then connected to the NAT cloud to provide internet access.

First, we update the repositories by running `apt update`:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.002.png)

Next, we download the required packages. For the servers, we install Apache:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.003.png)

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.004.png)

For the home router, we install the DHCP server:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.005.png)

At the end of the installation, an error code similar to this one may appear because there is no valid configuration in the service yet:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.006.jpeg)

We will ignore this for now and configure the DHCP server later.

With the necessary packages installed, we can proceed to set up the scenario.

#### Network Interface Configuration

We encounter a small obstacle when building the scenario, as some routers require more than one network interface.

To add multiple interfaces (while the device is powered off and disconnected), right-click the device, select **Configure** $\rightarrow$ **Network**, and choose the required number of adapters. For example, the home router needs two adapters:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.007.jpeg)

After configuring the machines that need multiple interfaces, we set up the scenario and configure their IP addresses.

To modify the network interface settings, we edit the `/etc/network/interfaces` file. To apply the changes, we have several options:

**Bringing the modified interface down and up:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.008.png)

Alternatively, we can restart the networking service, which applies the changes to all interfaces simultaneously and saves time:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.009.png)

**Home Router:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.010.jpeg)

**Router R1:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.011.jpeg)

**ISP Router:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.012.jpeg)

**Router R2:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.013.jpeg)

This is the mapping of IP addresses for the routers' network interfaces. To apply these settings, the network service must be restarted as mentioned above.

For the scenario to work, we must enable the forwarding bit on these four routers. We will do this permanently by editing the `/etc/sysctl.conf` file and uncommenting the following line:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.014.png)

#### Required Routes

For the current scheme, the required routes on the routers are:

**Router R1:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.015.png)

**ISP Router:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.016.png)

**Router R2:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.017.png)

**Home Router:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.018.png)

#### Connectivity Check

We will perform a `ping` from each router to its furthest endpoint to ensure that the routing is correct.

**Router R1 $\rightarrow$ R2:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.019.png)

**Router R1 $\rightarrow$ Home:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.020.png)

**Router R2 $\rightarrow$ R1:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.021.png)

**Router R2 $\rightarrow$ Home:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.022.png)

**Home Router $\rightarrow$ R1:**

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.023.png)

We observe that all devices with public IP addresses have connectivity between them. However, devices with private addressing will not have connectivity, as private addresses are not routed across internet routers.

In other words, if we ping a private address from another network (for example, from server 1 to server 2), it will not reach its destination because the ISP router's routing tables do not contain routes for private addresses.

Therefore, it is impossible to reach a private network other than your own.

For example, if we ping Google from home, we use the public address `8.8.8.8`, not the private address of the server (which might be, for instance, `172.22.1.15`).

### DHCP Service Configuration on the Home Router

Returning to the package installation section, we have already downloaded the DHCP server for Debian (`isc-dhcp-server`). We will now configure it.

First, we must tell the server which network interface to use for distributing IP addresses. In our case, it is the `ens5` interface.

To do this, we edit the `/etc/default/isc-dhcp-server` file and add the interface name in the IPv4 section:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.025.jpeg)

Next, we configure the settings that the DHCP server should assign to clients by editing the `/etc/dhcp/dhcpd.conf` file. We can use one of the commented examples:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.026.png)

This is a simple DHCP server example, sufficient for our scenario. The fields mean:

- **subnet**: The network address from which the service distributes IP addresses.
- **netmask**: The subnet mask of the network being configured.
- **range**: The range of IP addresses to be distributed (start and end).
- **option routers**: The gateway for our network.
- **option broadcast-address**: The broadcast address of our network.

After configuring these parameters, we restart the service:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.027.png)

And verify that the service is active:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.028.jpeg)

For clients to receive an address from this service, we configure the network interfaces of PC1 and PC2 as follows:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.029.png)

We restart the service to apply the changes, and the server automatically assigns the network configuration:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.030.png)

We verify that the network configuration has been successfully assigned:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.031.jpeg)

We can also track the IP assignments by viewing the `/var/lib/dhcp/dhcpd.leases` file, which stores the active leases.

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.032.png)

We can see the lease start time and the device to which it was assigned by checking its MAC address:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.033.jpeg)

### NAT Configuration

#### Home Router

We will configure SNAT on the home router. Based on the current scheme, the rule is:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.034.png)

To ensure the rule persists after a reboot, we add it to the `/etc/network/interfaces` file:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.035.png)

We can verify the application of the rule after restarting the networking service:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.036.png)

We test the rule by pinging another network (R1) and verifying if our IP address changes:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.037.png)

Using a packet capture, we observe that the private IP of the machine has been replaced by the public IP of the home router, confirming that the SNAT rule is working correctly.

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.038.jpeg)

#### Router R2

We will configure SNAT and DNAT by adding the rules to `/etc/network/interfaces`:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.039.png)

We restart the networking service and verify the results:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.040.png)

We test SNAT by pinging a public address from the server:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.041.png)

The SNAT rule is working correctly:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.042.png)

The private IP address has been replaced by the corresponding public IP of the router. In the following sections, we will test DNAT.

#### Router R1

For this router, we will implement the rules differently. We will create a service to load the DNAT and SNAT rules upon reboot to avoid adding them to the interfaces file.

The DNAT and SNAT rules for this machine are:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.043.png)

First, we create a script with our rules. We use the command `iptables-save > /etc/iptables/rules.v4` to dump the existing rules.

We then create a restoration script in `/usr/local/bin/`:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.044.png)

We ensure the script has execution permissions:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.045.png)

Next, we create a Systemd service file. This file must have read and write permissions only for root, so we execute the following command as root:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.046.png)

We add the following content, specifying the path to the `iptables` restoration script:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.047.png)

We configure the service to start automatically on boot:

![](/redes/configuracion_de_nat/img/Aspose.Words.C5d96acd8-9177-4bad-9621-78ead201ec37.048.png)

And start it:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.049.png)

To verify the execution, we check the service status:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.050.png)

The rules have been added automatically:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.051.png)

We verify the SNAT by performing a `ping`:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.052.png)

The private IP address has been replaced by the public one:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.053.png)

### Navigation and DNAT Check

Now we will verify that web servers are accessible from the home network.

#### Debian Client

From the Debian client, we use `curl` to check the DNAT functionality on Router R1:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.054.jpeg)

And similarly for Router R2:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.055.jpeg)

Next, we check what happens if we use the private IP addresses of the various web servers:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.056.png)

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.057.png)

Obviously, we do not receive a response because we are simulating the Internet, and private IP addresses cannot be routed as they may be repeated across an infinite number of networks.

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.058.png)

A web request would also fail.

If we intercept an HTTP request, we can see that SNAT is working correctly, as the requester's private IP is replaced by the public IP of their router:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.059.png)

Finally, we intercept a request where DNAT is applied to confirm it is working properly:

![](/redes/configuracion_de_nat/img/Aspose.Words.5d96acd8-9177-4bad-9621-78ead201ec37.060.png)
