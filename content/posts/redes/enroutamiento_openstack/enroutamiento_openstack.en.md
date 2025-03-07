---
title: "OpenStack routing"
date: 2023-09-08T10:00:00+00:00
description: We routed a scenario deployed using the OpenStack orchestration
tags: [Redes, Enrutamiento]
hero: images/redes/enrutamiento_os/portada.png
---

In this practice, we will explore the creation of a scenario through the OpenStack orchestration and then we will conduct the routing to ensure connectivity between the different virtual machines. This exercise will allow us to understand and apply the use of OpenStack to manage virtual environments, as well as to set up the network efficiently to facilitate communication between different devices on the stage.

### Scenario to ride in OpenStack

In order to mount our OpenStack scenario due to the current situation of the images available, we will need to prepare an instance that has password access enabled. In addition, if you want to set up another one to enable the ssh password access for this user.

This will have to be created with the same flavour that we will generate the stage with to avoid errors.

As long as we get our instance ready, we'll check that you can log in from time to time:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.001.png)

Now we'll create a snapshot:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.002.png)

We will copy the ID of the snapshot:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.003.png)

And we'll add it to the file:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.004.png)

And we'll deploy it:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.005.png)

We see that it has been created correctly:

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

As it is a router we will have to activate the forward bit for it we will enter the following command:
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

So we'd have the routing table:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.011.png)

### PC1

We will delete the default route on the device

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.012.png)

And we'll add the new route.

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.013.png)


Router 2

As it is a router we will have to activate the forward bit for it we will enter the following command:

```bash
echo 1 > /proc/sys/net/ipv4/ip\_forward
```

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.014.png)

We'll create the routing table:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.015.png)

It would be like this:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.016.png)

### P2

As we did before, we will remove the default route that it brings and add the new one: 

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.017.png)

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.018.png)

We will activate the forwarding bit with the following command:

```bash
echo 1 > /proc/sys/net/ipv4/ip\_forward
```

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.019.png)

We will create the routing table for our stage:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.020.png)

The routing table would be as follows:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.021.png)

### P2

As with others we will have to change the default route to the ip of the router to which we are connected:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.022.png)



### Configuration and clarification summary

### For routers

1. Activate the forward bit
2. Create routing tables
3. Modify the default route

### For PCs

1. Modify the default route

The modification of the default route is because I can't modify the configuration of the network cards so I can't modify the link door.

By default when using the script this comes with the X.X.X.1 link door however this does not match the client link door.

For routers we must also modify it to indicate where we will send the traffic "by default."

If we want to make the forwarding bit keep permanently so that when we restart the team it will not return to 0:

- > We write directly in the /etc/sysctl.conf file:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.023.png)

If we want to turn the configuration of the routing tables into a file to have a backup of them we use:

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

To capture a particular interface and save it in a file we will use tcpdump:

```bash
tcpdump -i NOMBRE\_INTERFAZ -w NOMBRE\_ARCHIVO
```

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.032.png)

If we want to have an output to the command instead of saving the file we will use the -n parameter: Here we see how the ICMP REQUEST comes from PC3 to PC1 and the ICMP REPLY from PC1 to PC3

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.033.png)

I have also captured a request and arp response from PC3:

![](/redes/enroutamiento_openstack/img/Aspose.Words.05e5a583-273a-4a61-9aa6-cb58c3b88bac.034.png)

## Bibliography

- [How to make routing tables](https://docs.aws.amazon.com/en/vpc/latest/userguide/VPC_Route_Tables.html)

