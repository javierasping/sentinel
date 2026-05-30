---
title: "Network Monitoring Commands"
date: 2023-09-08T10:00:00+00:00
description: "A detailed guide to the main commands used for detecting and resolving network incidents."
tags: [Network, commands]
hero: /images/redes/comando_de_supervision_de_redes/comando_de_supervision_de_redes.png
---

This document details the main commands and tools used to detect and solve connectivity incidents in networks.

## Diagnostic Tools in Windows

### TCP/IP Properties Configuration

Network configuration in Windows is managed independently for each network adapter. To access these parameters, follow this path:

**Control Panel** $\rightarrow$ **Network and Internet** $\rightarrow$ **Network and Sharing Center** $\rightarrow$ **Change adapter settings**.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.001.png)

Once at the corresponding adapter, right-click on it, select **Properties**, and then choose **Internet Protocol Version 4 (TCP/IPv4)**.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.002.png)

In the **General** tab, you will find the following key sections:

#### IP Address Configuration

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.003.png)

- **Obtain an IP address automatically**: Enables the use of the DHCP service to dynamically assign the IP address, subnet mask, and default gateway.
- **Use the following IP address**: Allows manual configuration of network parameters:
    - **IP address**: Unique numerical identifier of the computer on the local network.
    - **Subnet mask**: Defines which part of the IP address corresponds to the network (including the subnet) and which part to the host.
    - **Default gateway**: IP address of the device that allows communication with other networks (usually the router).

#### DNS Server Configuration

DNS servers translate domain names into IP addresses to enable web browsing.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.004.png)

- **Obtain DNS server address automatically**: The address is obtained through the network's DHCP server.
- **Use the following DNS server addresses**: Allows manual assignment of DNS servers:
    - **Preferred DNS server**: The first server consulted for name resolution.
    - **Alternate DNS server**: Backup server in case the primary is unavailable.

#### Alternate Configuration

Designed for computers that operate on multiple networks, common in professional environments:

- **Automatic Private IP Addressing (APIPA)**: Uses self-configuration if the DHCP server does not respond.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.005.png)
- **User configured**: Allows manual entry of the configuration.
- **Preferred/Alternate WINS**: Microsoft name servers for NetBIOS that maintain the correspondence between IP addresses and computer names.

### Utility of the `ping` Command

The `ping` command is a fundamental diagnostic tool that verifies connectivity between a local host and a remote computer on a TCP/IP network.

Its most common uses include:

- Checking basic network connectivity.
- Measuring latency (response time) between two points.
- Resolving a domain name to find its IP address.
- Implementing server availability monitoring scripts.

To run it, open a command prompt (`cmd`) by pressing `Win + R` and typing `cmd`.

#### General Use of `ping`

The basic syntax is: `ping [Parameters] [IP/Name]`

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.006.png)

The command output provides the following information:

- **IP Address**: The IP associated with the remote machine's name.
- **ICMP Sequence Number**: Response code (e.g., 0 indicates success).
- **TTL (Time to Live)**: Packet lifetime. It decrements at each hop (router). If it reaches zero, the packet is discarded to avoid infinite loops in the network.
- **Latency**: Time in milliseconds for the packet to travel to the destination and back. As a general rule, a delay over 200 ms may indicate network problems.
- **Statistics**: Summary of packets sent, received, and lost, along with minimum, maximum, and average times.

#### Advanced `ping` Parameters

- **`-t` (Infinite Ping)**: Sends requests continuously until the process is stopped manually with `Ctrl + C`.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.007.png)

- **`-a` (Name Resolution)**: Attempts to resolve the IP address into a hostname, making it easier to identify equipment.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.008.png)

- **`-n [number]` (Number of requests)**: Specifies the number of packets to send (default is 4). Example: `ping -n 10 8.8.8.8`.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.009.png)

- **`-l [size]` (Packet size)**: Modifies the size in bytes of the sent data (between 0 and 65,500 bytes).

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.010.png)

- **`-f` (Do not fragment)**: Prevents packets from being fragmented. The maximum unfragmented size is generally 1472 bytes.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.011.png)

- **`-i [TTL]` (Set TTL)**: Sets the initial TTL value. If the packet reaches the destination after exactly this number of hops, or if it reaches zero before, the corresponding status will be reported.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.012.png)

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.013.png)

- **`-4` and `-6`**: Forces the use of IPv4 or IPv6 respectively.

#### Connectivity Check Protocol

To verify network operation and detect errors, it is recommended to follow this sequence of tests:

1. **Ping own computer (Loopback)**: Verifies that the TCP/IP stack and the network adapter are functioning correctly.
   ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.014.png)

2. **Ping a computer on the local network**: Confirms that physical connectivity and local addressing are correct.
   ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.015.png)

3. **Ping the default gateway**: Demonstrates that communication exists with the router providing access to other networks.
   ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.016.png)

4. **Ping an external IP (Internet)**: Confirms internet access without depending on name resolution.
   ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.017.png)

5. **Ping an external domain**: Verifies that the internet connection is correct and that DNS servers are resolving names properly.
   ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.018.png)

### General Use of the `ipconfig` Command

The `ipconfig` command allows viewing and managing the current configuration of the computer's network adapters.

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.019.png)

**Information provided:**

- **Adapter Description**: Name of the network card used.
- **IPv4 Address**: IP assigned to the computer on the local network.
- **Default Gateway**: IP of the device providing internet access.
- **DNS Servers**: Addresses of the servers responsible for resolving domain names to IP addresses.
- **DHCP State**: Indicates if the configuration is dynamic (enabled) or static.

#### Advanced `ipconfig` Parameters

- **`/all`**: Shows detailed output including MAC addresses and DNS servers.
  ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.020.png)

- **`/release`**: Releases the current IP address assigned by the DHCP server.
  ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.021.png)
  *Example: `ipconfig /release Ethernet0` to release a specific adapter.*

- **`/renew`**: Requests a new IP address lease from the DHCP server.
  ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.022.png)

- **`/flushdns`**: Clears the local computer's DNS resolution cache, useful for forcing the update of DNS record changes.
  ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.023.png)

- **`/registerdns`**: Updates DHCP leases and re-registers DNS names on the server. This command is intended for domain environments.
  ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.024.png)

- **`/displaydns`**: Shows all entries currently stored in the DNS cache.
  ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.025.png)

- **`/showclassid`**: Shows the user classes configured on the DHCP server.
  ![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.026.png)

### General Use of the `arp` Command

The `arp` command is used to view and modify the mapping table between IP addresses and MAC addresses (link layer).

#### Parameter `arp -a`

Shows current ARP cache entries for the host, including the IPv4 address, physical address (MAC), and addressing type (static or dynamic).

![](/redes/comandos_de_supervision_de_redes/images/Aspose.Words.fb3cd5be-2e97-40e8-b21b-cbe3724f86ed.027.png)

*Note: The `-g` parameter performs the same function as `-a`.*
