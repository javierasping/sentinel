---
title: "Network monitoring commands"
date: 2023-09-08T10:00:00+00:00
Description: A document in which the main commands are detailed when it comes to detecting and solving network incidents.
tags: [Network, comands]
hero: images/redes/comando_de_supervision_de_redes/comando_de_supervision_de_redes.png
---

A document in which the main commands are detailed when it comes to detecting and solving network incidents.

### Windows Commands

### Explanation of the different parameters to be configured in the TCP/IP Properties in Windows

We must keep in mind that each configuration we make is independent for each of our network adapters.

To access these parameters, follow this path in our system:

Control Panel > Network and Internet > Network and Sharing Center > Change adapter settings:


![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.001.png)

Once here, right-click on the adapter, select **Properties**, and then choose **Internet Protocol Version 4 (TCP/IPv4)**:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.002.png)

Once here, we will see two tabs that can be used to configure our card; in the General tab, we can see the following sections:

The first subsection (General) relates to our IP address:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.003.png)

- **Obtain an IP address automatically**: This option uses the DHCP service to dynamically assign the IP address, subnet mask, and default gateway.
- **Use the following IP address**: Allows manual entry of the desired network configuration:
- **IP address**: A numerical label that uniquely identifies our machine on the network; it cannot be repeated.
- **Subnet mask**: A numerical set whose function is to indicate which part of the IP address is the network (including the subnet) and which part is the host.
- **Default gateway**: The default IP address assigned to a device to send packets to other networks.

In the second section of this tab, we will configure the DNS servers, which allow us to translate domain names into IP addresses to enable web browsing.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.004.png)

- **Obtain the DNS server address automatically**: The address is obtained from the DHCP server configured on our network.
- **Use the following DNS server addresses**: Allows manual selection of the IP addresses of our DNS servers:
- **Preferred DNS server**: The first server consulted for name resolution.
- **Alternate DNS server**: A backup server used if the primary server is unavailable.

The alternative configuration tab is designed for equipment that needs to be used in more than one network, which is common in professional environments:

- **Automatic Private IP Addressing (APIPA)**: Uses the DHCP server for configuration.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.005.png)
- **User-configured**: Allows manual entry of the configuration (omitting the fields explained above):
- **Preferred/Alternate WINS**: Microsoft name servers for NetBIOS, which maintain a table correlating IP addresses and NetBIOS computer names.


## Utility of the `ping` Command

`ping` is a fundamental diagnostic tool that verifies connectivity between a local host and a remote computer on a TCP/IP network; it is the most well-known network diagnostic tool.

The most common uses of this tool include:

- Checking network connectivity.
- Measuring the latency between two points.
- Finding the IP address associated with a domain name.
- Implementing scripts to monitor server availability.
- Implementing scripts to detect connectivity to a computer.

To use it, open a command prompt (`cmd`) by pressing `Win + R` and typing `cmd`.

### General use of Ping

The simplest ping syntax is as follows: ping [Parameters] [IP / Name]

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.006.png)

If we look at the command output we see that it allows us to know:

- * * IP address * * corresponding to the name of the remote machine.
- * * The ICMP sequence number * * ("Code that returns us, ej: 0 = inaccessible network").
- * * TTL * *: Life time in seconds; as this value is decreed in each machine in which it is processed, it must be at least equal to or greater than the number of jumps it will give. If ever this number is zero, the router will interpret that the package is traveling in circles, therefore, it ends the process.
- * * Latency: * * corresponds to the time period in milliseconds that is needed to take a turn between the source and destination machines. As a general rule, the delay of a package should not exceed 200 ms.
- * * ping statistics: * * Collects all the information showing us the lost, sent and received packages. It also shows us the package with lower latency and greater as well as an arithmetic mean.

### PING -T

This parameter allows for an infinite ping that does not end until the process is manually stopped; by default, only 4 packets are sent. To stop the execution of this command, press `Ctrl + C`.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.007.png)

Once the execution is stopped, the collected statistics are shown: packets sent, received, lost, and the average round-trip times.

### PING -A

This parameter is used to resolve an IP to a hostname, printing a line indicating the hostname to which the packets are being directed, making it easier to identify the machines:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.008.png)


### PING -N

This parameter specifies the number of requests to send, using a value between 1 and 4,294,967,295.

For example, if we want to send 10 packets, the command would be:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.009.png)

We can verify at the bottom that the requested number of packets was sent.

### PING -L

This allows us to change the byte size of the sent packets; a value between 0 and 65,000 must be specified.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.010.png)


### PING -F

This parameter prevents packets from fragmenting; the maximum unfragmented packet size is 1472 bytes.

If this limit is exceeded, an error will be returned indicating that the packet must be fragmented:

### PING-I
![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.011.png)

This parameter allows us to specify the maximum number that can be given to reach the destination, the maximum value that we can enter 255.

When we specify a TTL this sets the maximum number of jumps, by passing through a new device (a router) this discount 1 to the TTL specifying until it reaches 0, in this case the destination will be shown as unattainable, thus preventing a package from travelling through the network indefinitely looking for a destination that may not exist.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.012.png)

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.013.png)



### PING -4 and -6

Ping -4: Forces a response from a host specified with an IPv4 address. Both the source and destination must have a correct IPv4 configuration.

Ping -6: Forces a response from a host specified with an IPv6 address. Both the source and destination must have a correct IPv6 configuration.

## Connectivity Check in a Network

We will perform a series of tests to verify operation and detect errors. First, we will ping the local machine:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.014.png)

If the output is correct, it shows that the network adapter is functioning properly.

Next, we will ping a machine on our local network to confirm that physical connections are correct:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.015.png)

Then, we will ping the gateway to confirm there is connectivity to the device providing Internet access:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.016.png)

Next, we will ping an external IP (Internet) to check for internet connectivity without relying on name resolution:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.017.png)



Finally, pinging an external domain verifies that the internet connection is correct and that the DNS servers are resolving names properly:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.018.png)


### General Use of the `ipconfig` Command

The `ipconfig` command is used to view and manage the current configuration of the computer's network adapters. An example of general command use is as follows:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.019.png)

**Information provided:**

- **Adapter Description**: Name of the network card used in the connection.
- **IPv4 Address**: The IP address assigned to the computer on the local network.
- **Default Gateway**: The IP address of the device providing internet access.
- **DNS Servers**: IP addresses of the servers responsible for resolving domain names to IP addresses. Usually, there are two: primary and secondary.
- **DHCP State**: Indicates if the configuration is dynamic (enabled) or static.

From these parameters, we can consult adapter information or identify configuration inconsistencies.

#### Advanced `ipconfig` Parameters

- **`/all`**: Displays detailed output, including MAC addresses and DNS servers.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.020.png)

- **`/release`**: Releases the current IP address assigned by the DHCP server.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.021.png)

We can specify the adapter from which we want to release the ip by writing it then, if we omit the name apply them to all.

*Example: `ipconfig /release Ethernet0` to release a specific adapter.*

- **`/renew`**: Requests a new IP address lease from the DHCP server.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.022.png)

We can specify the adapter from which we want the DHCP offer to be renewed by writing it below.

*Example: `ipconfig /renew Ethernet0` to renew only the Ethernet0 adapter. To renew an IPv6 address, use `/renew6`.*

- **`/flushdns`**: Clears the local computer's DNS resolution cache, which is useful for forcing the update of DNS record changes.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.023.png)

- **`/registerdns`**: Updates DHCP leases and re-registers DNS names on the server. This command is intended for domain environments.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.024.png)

- **`/displaydns`**: Shows all entries currently stored in the DNS cache, including IPv4 and IPv6 protocol records.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.025.png)

- **`/showclassid`**: Displays the user classes configured on the DHCP server and available to different customers.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.026.png)

*Use the `/showclass6` parameter to check for IPv6.*


### General Use of the `arp` Command

The `arp` command is used to view and modify the mapping table between IP addresses and MAC addresses (link layer).

#### Parameter `arp -a`

Displays current protocol data and ARP entries. If `inet_addr` is specified, only the IP and physical addresses of the specified equipment are shown. If there is more than one network interface using ARP, the entries of each ARP table are shown.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.027.png)

*Note: The `-g` option performs the same function as `-a`.*

As shown in the screen capture, the `arp -a` command lists all devices currently in the host's ARP cache, including the IPv4 address, physical address (MAC), and addressing type (static/dynamic) for each device.

To delete the ARP cache, use the `-d` option followed by a wildcard (`*`) to delete all entries, or specify an IP address to remove a specific entry.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.028.png)

You can request the MAC of an address using `arp [IP]` and then verify it in the table with `arp -a`.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.029.png)


### General Use of the `netstat` Command

The `netstat` command generates visualizations that show the state of the network and protocol statistics. The status of TCP, SCTP, and UDP endpoints can be viewed in table format. Information about the routing table and interface information can also be viewed.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.030.png)

#### NETSTAT -A

Shows all connections and listening ports on the computer, as well as the port state and the remote address currently using it:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.031.png)


#### NETSTAT -B

Shows the executable file involved in creating each connection or listening port.

#### NETSTAT -E

It shows statistics for the network interfaces, allowing you to see the activity of each one:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.034.png)

#### NETSTAT -R

Shows the routing table, allowing us to see which sites our computer can reach through the network:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.035.png)


#### NETSTAT -N

Shows active connections in a table format, similar to the previous parameter, but it indicates the port number instead of the name.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.036.png)

#### NETSTAT -O

Similar to the above, but it also adds the process PID:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.037.png)

#### NETSTAT -P

Allows filtering connections according to the protocol (TCP, UDP, tcpv6, tcpv4, etc.):

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.038.png)


#### NETSTAT -T

Shows the current connection's download status:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.039.png)

Netstat is very useful for viewing statistical data on a connection and for analyzing open ports to identify problems. It is essential for certain applications and for achieving optimal performance.

### General use nslookup

It is an application included in all Windows systems, to consult, obtain information, test and solve problems with DNS servers.

By invoking it without specifying any parameter, it will return the name of the default DNS server and its IP address:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.040.png)

The command has two modes of use, the traditional through command line and the interactive. We can use it to solve address names from the terminal by putting nslookup followed by the name we want to solve:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.041.png)



We can also do reverse consultations, that is, through the ip tell us the name:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.042.png)

For example we can select the type of DNS records to make requests which are:

- * * A: * * to search for A records that are related to the IPv4 address..
- * * AAAA: * * to search for AAAA records that are related to the IPv6 address. If a web uses IPv6 and so do we, then we will have to indicate this DNS record.
- * * PTR: * * to look for reverse records.
- * * MX * *: to search for Mail Exchange records of the mail.
- * * TXT: * *, to search for text records such as SPF or DKIM.
- * * CNAME: * * to search for domain aliases, this is also known as subdomains, for example, the "www" is always a main subdomain "or the typical" ftp. "which is also a subdomain.

To change the registration type we use the set type = Registry name, for example:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.043.png)

We can also choose the server from which we consult as follows:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.044.png)



### General use tracert

It serves to map the route that makes an incoming package that comes from a host or network point to your computer, so we know where our trip is.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.045.png)

Saying one by one all the nodes and routers through which you pass the test message you sent, their IP addresses and the latency of each of them until they reach their destination.

There are some nodes that are not able to answer for that the spent waiting time entries.

We have some interesting parameters such as:

- -d: does not convert addresses to host names

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.046.png)

- -h: allows us to select the maximum number of jumps

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.047.png)

- -4 or -6: Force using IPV4 or IPV6:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.048.png)

- -w: allows us to specify the waiting time in milliseconds:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.049.png)


### General use route print

The Route command is used to visualize and modify the routing table. Route print shows a list of current IP routes for the host. Route add is used to add routes to the table, and route delete is used to delete routes from the table.

So we can specify the way to reach a network or device.

The syntax is as follows: route [-f] [-p] [command [destination]] [MASK network mask]

Rute print command without parameters to show all the contents of the routing table:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.050.png)

If we want to delete the routing table we must use the -f parameter:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.051.png)

In addition, we can add manual routes as follows:

→ route add IP\ _ Destination Mascara\ _ Destination Door\ _ of\ _ interface metric link

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.052.png)

If we want to change a route, the syntax is the same as the previous command by changing the add-by-change command:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.053.png)

When we just want to remove a route, we will use the delete order followed by the destination:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.054.png)


### How can you find out your router's public IP?

There is a lot of way to know this from Windows, we can use the curl command to order the following web and return the ip:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.055.png)

Another way from the command line is to do a dns consultation with nslookup to the opendns service:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.056.png)

If we have a browser we can use one of the many websites that tell us the public ip address of the router, I use the following <https: ipchicken.com=""></https:> :

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.057.jpeg)


## Linux

### Configure a network interface

To set up a Linux network card we can do it from the graphical interface or from the command line.

From the graphic interface we go to Settings > Wireless or Network. Once here we turn on the card and give the gear.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.058.jpeg)

Once here we can manually configure the network settings of our card.

The same can be done from the command line by editing the / etc / network / interfaces file with superuser permissions.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.059.png)

Within this we can indicate the configuration of our network adapters, here I tell you with commented lines the basic parameters that we can indicate in this file.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.060.png)

Once we have configured our interfaces the changes will not be applied automatically, to do this we have several forms, the most comfortable is to restart the service:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.061.png)

Another way to change the DNS servers used is through the / etc / resolf.conf file

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.062.png)

Here followed by nameserver we will put the address ip or name of our DNS server

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.063.png)

### General use ifconfig

<a name="_page26_x56.70_y84.70"></a>* * Explains the usefulness of the ifconfig command from a real capture. Is there any information from which ipconfig / all is obtained that does not appear? Try to get it another way. * *

It is similar to ifconfig and is focused on the same functions, this command is also used to view, change and manage all current computer network configurations.

This is installed with the net-tools package, to install it:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.064.png)

To use this tool we will need to do it as a superuser, with its simplest use it will show us the basic TCP / IP configuration of our network card as well as statistics of it:

For example with ipconfig / all we can see the configured DNS servers which with ifconfig we can't see.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.065.png)

So we'll have to see the / etc / resolf.conf file

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.066.png)

A common use of this command is to quickly set up a network interface, for example:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.067.png)

We can put this in one line.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.068.png)

We can also lift and download the network card

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.069.png)

### General use dhclient

This uses the dynamic host configuration protocol to dynamically configure the network parameters of the network interface.

The following command will tell dhclient to release the current concession it has from the DHCP server, i.e. we want to release the current ip. We will use the -r and -v parameters

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.070.png)

If we want to reorder a network configuration to the dhcp command we will use only the -v parameter.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.071.png)

Mainly this command is used for this, to solve problems with DHCP service configuration.

Some parameters that I have not mentioned and may be useful are:

- -6: Serve to indicate you want IPV6
- -p: Serves to indicate another port to do the consultation
- -s: Serves to indicate the DHCP server address

### Differences in netstat and ping commands with respect to Windows employees

netstat shows information about the network subsystem on our computer as well as Windows. If you look at the manual, it tells us that this application is partially obsolete. The replacement of netstat is ss, for netstat -r has ip route, for netstat -i can use ip -s link and for netstat -g has ip maddr.

If we launch the parameter we can see to the naked view that shows us more information without indicating any parameter, otherwise these are the same as on Windows.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.072.png)

While the ping command the difference is that it is by infinite default, unlike Windows this will not end until we stop it.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.073.png)

In this the parameters with respect to Windows change their "letter," here would be:

- -i: Indicate the interval to send the next package in seconds (default is 1)
- -s: Change package size to bytes
- -f: flood, to test the network performance under a heavy load (send a lot of packages as quickly as possible)
- -c: indicate the number of traces sent
- -w: Stop printing the results after the indicated seconds
- -q: Remove the command output, quiet option
- -a: makes a sound when there's an answer
- -V indicates the command version

The utility of this is still the same, solving problems of accessibility of hosts in a network. This helps us understand why a website is not loaded.

### General use command dig

Dig is a command that allows you to consult DNS servers for information related to this service. To install it in our system, we will make an apt install dnsutils.

We can do a dns consultation, for example to the institute to check if we are able to get your address ip:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.074.jpeg)

Using the + trace option, it does iterative consultations to solve the search for names. It will consult the server names from the root and then cross the name space tree through iterative consultations following the references on the way:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.075.png)



We can also conduct reverse consultations with the -x option:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.076.png)

### Linux traceroute command differences with Windows tracert command

The traceroute tool is exactly the same as the tracert, but it is called otherwise, although it can internally make use of different protocols, as in some operating systems the ICMP Echo Request / reply protocol is used, and in others it makes use of UDP messages directly to check how many jumps there are from one host to another.

These are used to detect where the error is when accessing a particular computer and to know where the "error" occurs.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.077.jpeg)


Some parameters that may interest us are:

- -f,: Set the distance between the first jump and the next jump.
- -g,: allows us to indicate the link door.
- I: Use ICMP ECHO
- -m,: Set the number of jumps; the default value is 64.
- -M,: the follow-up routes are carried out with ICMP or UDP; the default method is UDP.
- -p: Define the network port; the default value is 33434.
- -q: Define the number of packages per jump.
- -resolve-hostnames: you can use this syntax to correct the host names.
- -w,: Define the waiting time in seconds.

### General use

Wget is a computer tool created by the GNU Project. You can use it to recover content and files from several web servers. The name is a combination of World Wide Web and the word get. It supports downloads through FTP, SFTP, HTTP and HTTPS.

To install it we use the apt install wget command.

An example is to download files, for example an iso. We would put the command followed by the url:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.078.png)

This will download the file to us in the current work directory.

We can use the command -or to indicate a different name when downloading the file:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.079.png)

Some interesting parameters are:

- -P: Indicate the directory where we want to save the file
- --limit-rate: serves to limit the download speed
- -tries: allows us to indicate the number of reattempts of the download
- -b: Make the download in the background
- -c to indicate that a discharge is resumed

If we wanted to download files from a ftp server we would use the following syntax: wget -ftp-user = usario--ftp-password = password

### General use of tcpdump

Tcpdump is a command line tool whose main utility is to analyze the traffic that flows through the network. Allows the user to capture and show in real time the packages transmitted and received by the network to which the computer is connected

The most common parameters are:

- -i allows to specify the network interface in which we are going to serve traffic.
- -c <numero> It allows to limit the number of packages captured in a given number.
</numero>- n Avoid resolution of ports and addresses ip to names.
- - e Show ethernet headers in addition to the ip package.
- - t Do not print the capture time frame for each package.
- -x shows the hexadecimal content of the captured plot.
- -xx Idem to -x, but also shows the content of the Ethernet header.
- -X shows the hexadecimal and ASCII content of the captured plot.
- It just shows the ASCII content of the captured package.
- s <numero> Show only the first <numero> bytes from the beginning of the package.
</numero></numero>- -vv Displays additional information, including parameters of protocol headers.
- -w file Allows to save output in a file with pcap format.
- -r file allows you to read the packages previously captured and stored in a pcap file.

For example we can make a capture of our network of up to 50 packages:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.080.png)

As you see the output is indecipherable, to read it we will use the ngrep command to search for coincidences without taking into account capital and lower case.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.081.png)


### General use of the arp command

The arp command will allow us to interact with the arp resolution cache, modifying it for example.

We can also find out the MAC address of a device, looking for it in the table:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.082.png)

The parameters are the same as we can find on Windows:

- -a: Find a particular address in the table
- -v: Shows all entries
- -n: Displays all entries in numerical form
- -d: removes a particular resolution

We can also do this with the ip command:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.083.png)

For this the basic syntax is as follows:

- add: Add resolution
- of: Delete resolution
- change: Change a resolution
- replace: replace a resolution

For example to add a table:

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.084.png)

### ip command

We can view and configure IP addresses, view and configure routing tables, view and configure IP tunnels, and also view and configure the physical interface.

This is added a "second command" to indicate your function, are as follows:

- link: it serves us to configure physical or logical network interfaces, for example, to see the status of all network interfaces.
- address: allows to view and configure the IPv4 and IPv6 addresses associated with the different network interfaces. Each interface must have at least one configured IP address.
- addrlabel: allows to add a label
- nearby: allows to see the neighborhood links, that is, you can see the ARP table of the operating system.
- rule: allows to view and configure routing policies and change them, this is used especially when you are going to set up several routing tables.
- route: allows to see and configure the routing tables, both of the main routing table and of the "secondary" that you configure.
- tunnel: allows to view IP tunnels and also to configure them.
- maddr: allows to view and configure the multilayer addresses.
- mroute: allows to view and configure the multicast routing table.
- mrule: allows to view and set up multi-direction routing policies.
- monitor: allows to monitor the status of network cards on a continuous basis, also IP addresses and routes.
- ntable: manages the neighbour cache (ARP)
- tuntap: manages TUN / TAP interfaces, oriented to VPN such as OpenVPN or WireGuard.
- maddress: configuration of the multicast addresses
- xfrm: manages IPsec policies.
- netgs: manage network name spaces
- l2tp: L2TP configuration
- tcp\ _ metrics: manages TCP metrics.
- token: manages the identifiers with token of the interfaces.

## Bibliography

[Change TCP / IP configuration] (https: / / support.microsoft.com / es-en / windows / change-la-configuration% C3% B3n-de-tcp-ip-bd0a07af-15f5-cd6a-363f-ca2b6f391ace # WindowsVersion = Windows _ 10) [General information on commands] (https: / / openwebinars.net / blog / 20-mandios-de-red-mass-importantes-code%)

[PING Command] (https: / / apontesjulio.com / como-usar-el-comando-ping /)

[NSLOOKUP command] (https: / / axarnet.es / blog / que-es-nslookup)

[Description of command parameters] (http: / / trajano.us.es / ~ fornes / ARSSP / CommandosRedWindows.pdf) [Debian network configuration] (https: / / wiki.debian.org / es / NetworkConfiguration)

[ifconfig command] (http: / / somebooks.es / comando-ifconfig-ubuntu /)

[ip command] (https: / / www.redeszone.net / tutorials / servers / configure -linux-comand-ip-iproute2-suite /)

