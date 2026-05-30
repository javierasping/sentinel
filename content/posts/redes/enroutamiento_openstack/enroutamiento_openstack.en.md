---
title: "OpenStack routing"
date: 2023-09-08T10:00:00+00:00
description: We routed a scenario deployed using the OpenStack orchestration
tags: [Redes, Enrutamiento]
hero: images/redes/enrutamiento_os/portada.png
---

In this practice, we will explore the creation of a scenario through OpenStack orchestration and then conduct the routing to ensure connectivity between the different virtual machines. This exercise will allow us to understand and apply the use of OpenStack to manage virtual environments, as well as to set up the network efficiently to facilitate communication between different devices in the scenario.

### Scenario to deploy in OpenStack

To mount our OpenStack scenario, given the current state of the available images, we will need to prepare an instance with password access enabled. Additionally, if we want to configure another instance based on this one, we must enable SSH password access for this user.

This must be created using the same flavour as the others in the scenario to avoid errors.

Once the instance is ready, we will verify that we can log in via Horizon:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.001.png)

Now we will create a snapshot:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.002.png)

We will copy the snapshot ID:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.003.png)

And we will add it to the file:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.004.png)

And we will deploy it:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.005.png)

We can see that it has been created correctly:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.006.jpeg)

### Chart of the configuration

The scheme would be as follows:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.007.png)

Having the following relation of IPS:

### IP Relations:

| Machine | IP             | Interface |
| ------- | -------------- | -------- |
| PC1     | 10.0.100.144   | &nbsp; ens3     |
| R1-PC1  | 10.0.100.68    | &nbsp; ens3     |
| R1-R2   | 10.0.110.78    | &nbsp; ens4     |
| R2-R1   | 10.0.110.30    | &nbsp; ens3     |
| R2-PC2  | 10.0.120.191   | &nbsp; ens4     |
| PC2     | 10.0.120.203   | &nbsp; ens3     |
| R2-R3   | 10.0.130.146   | &nbsp; ens5     |
| R3-R2   | 10.0.130.36    | &nbsp; ens3     |
| R3-PC3  | 10.0.140.127   | &nbsp; ens4     |
| PC3     | 10.0.140.158   | &nbsp; ens3     |



---

### Routing Tables

#### Router R1:

| R1          |          |          |
| ----------- | :------: | :------: |
| 10.0.100.0/24 &nbsp; | 0.0.0.0 | &nbsp;  ens3    &nbsp;|
| 10.0.110.0/24 &nbsp; | 0.0.0.0 |  &nbsp; ens4    &nbsp;|
| 10.0.120.0/24 &nbsp; | 10.0.110.30 | &nbsp; ens4 &nbsp;|
| 10.0.130.0/24 &nbsp; | 10.0.110.30 | &nbsp; ens4 &nbsp;|
| 10.0.140.0/24 &nbsp; | 10.0.110.30 | &nbsp; ens4 &nbsp;|
| 0.0.0.0/0   &nbsp; | 10.0.110.30 | &nbsp; ens4   &nbsp;|

**Note:** Networks to which we are directly connected will automatically create the routes.

---

#### Router R2:

| R2          |          |           |
| ----------- | :------: | :-------: |
| 10.0.100.0/24 &nbsp; | 10.0.110.178 | &nbsp; ens3 &nbsp;|
| 10.0.110.0/24 &nbsp; | 0.0.0.0 |  &nbsp;     ens3 &nbsp;|
| 10.0.120.0/24 &nbsp; | 0.0.0.0 |    &nbsp;   ens4 &nbsp;|
| 10.0.130.0/24 &nbsp; | 0.0.0.0 |    &nbsp;   ens5 &nbsp;|
| 10.0.140.0/24 &nbsp; | 10.0.130.36 |&nbsp; ens5   &nbsp;|
| 0.0.0.0/0  &nbsp;  | 10.0.130.36 | &nbsp; ens5    &nbsp;|

**Note:** Networks to which we are directly connected will automatically create the routes.

---

#### Router R3:

|R3|||
| - | :- | :- |
|10\.0.100.0/24 &nbsp;|10\.0.130.146|&nbsp; ens3 &nbsp;|
|10\.0.110.0/24 &nbsp;|10\.0.130.146|&nbsp; ens3 &nbsp;|
|10\.0.120.0/24 &nbsp;|10\.0.130.146|&nbsp; ens3 &nbsp;|
|10\.0.130.0/24 &nbsp;|0\.0.0.0|&nbsp; ens3 &nbsp;|
|10\.0.140.0/24 &nbsp;|0\.0.0.0|&nbsp; ens4 &nbsp;|
|0\.0.0.0/0 &nbsp; |10\.0.130.146|&nbsp; ens4 &nbsp;|

**Note:** Networks to which we are directly connected will automatically create the routes.

### Configuration commands for each node

Router 1

As it is a router, we will have to activate the forwarding bit. To do so, we will enter the following command:
```bash
echo 1 > /proc/sys/net/ipv4/ip\_forward
```

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.008.png)

We'll create the routing table:

Static routes:

```bash
ip route add 10.0.100.0/24 via 0.0.0.0 dev ens3
```

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.009.png)

The default route:

```bash
ip route add default via 10.0.110.30 dev ens4
```

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.010.png)

As a result, we would have the routing table:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.011.png)

### PC1

We will delete the default route on the device.

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.012.png)

Then, we'll add the new route.

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.013.png)


Router 2

As it is a router, we will have to activate the forwarding bit. To do so, we will enter the following command:

```bash
echo 1 > /proc/sys/net/ipv4/ip\_forward
```

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.014.png)

We'll create the routing table:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.015.png)

It would be like this:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.016.png)

### P2

As we did before, we will remove the default route and add the new one: 

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.017.png)

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.018.png)

We will activate the forwarding bit with the following command:

```bash
echo 1 > /proc/sys/net/ipv4/ip\_forward
```

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.019.png)

We will create the routing table for our scenario:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.020.png)

The routing table would be as follows:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.021.png)

### P2

As with the others, we will have to change the default route to the IP of the router to which we are connected:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.022.png)



### Configuration and clarification summary

### For routers

1. Activate the forward bit
2. Create routing tables
3. Modify the default route

### For PCs

1. Modify the default route

The modification of the default route is necessary because I cannot modify the configuration of the network cards, and thus cannot modify the default gateway.

By default, when using the script, this comes with the X.X.X.1 gateway. However, this does not match the client gateway.

For routers, we must also modify it to indicate where we will send the traffic "by default."

If we want the forwarding bit to persist permanently so that it does not return to 0 when we restart the system:

- > We write directly in the /etc/sysctl.conf file:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.023.png)

If we want to save the configuration of the routing tables to a file for backup purposes, we use:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.024.png)

If we want to restore the copy:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.025.png)



## Verification of connectivity (ping) between nodes


### PC1

PC1 - PC2

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.026.png)

PC1-PC3

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.027.png)

### P2
 
PC2-PC1

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.028.png)

PC2-PC3

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.029.png)

### P2

PC3-PC1

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.030.png)

PC3-PC2

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.031.png)

### Traffic capture on the r2 or r3 router showing traffic between h1 and h3.

To capture a particular interface and save it to a file, we will use tcpdump:

```bash
tcpdump -i NOMBRE\_INTERFAZ -w NOMBRE\_ARCHIVO
```

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.032.png)

If we want the output to be displayed in the command instead of saving the file, we will use the -n parameter. Here we see how the ICMP REQUEST comes from PC3 to PC1, and the ICMP REPLY from PC1 to PC3

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.033.png)

I have also captured a request and arp response from PC3:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.034.png)

## Bibliography

- [How to make routing tables](https://docs.aws.amazon.com/en/vpc/latest/userguide/VPC_Route_Tables.html)

