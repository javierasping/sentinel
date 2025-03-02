---
title: "SSH bajo debian"
date: 2023-09-08T10:00:00+00:00
Description: Ssh service configuration
tags: [Servicios,NAT,SMR,IPTABLES,SNAT,SSH,FORWARDING]
hero: images/servicios/ssh/portada-ssh.png
---


#SSH server under debian
## Remote management using SSH
The first thing we should do is install the package on the server and the client:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.079.png)

For safety it is usually not allowed to connect the root to the server; for this, the / etc / ssh / sshd\ _ config file should be modified, and the following option is put:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.080.png)


And we restart the service to apply the changes:

### Connect to ssh server

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.081.png)

We're going to install the ssh client, for that:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.082.png)

To access the server from the client we type:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.083.png)

We'd open up remotely.


### Remote execution of graphic applications
By ssh there is the possibility of running graphic applications on the server and handling and visualizing them on the client. The ssh server must have the redirection of the X protocol activated, i.e. the following parameter in the / etc / ssh / sshd\ _ config configuration file:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.084.png)

In my case it was already enabled, if we didn't have it we changed it and restarted the service to apply the changes. We must now connect to the -X parameter:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.085.png)

and then we can run any graphic application, for example, gedit:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.086.png)

The program will be opened to us graphically:


![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.087.png)

Now we see on the server that has been created:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.088.png)


### Transfer files with ssh
To copy a file from the client to the server we enter the following command:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.089.png)

Now let's check if it's been copied to the server:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.090.png)


### Remote access by asymmetrical encryption

### Key access configuration

We will generate our keys from our client:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.091.png)


Now let's add it to our server:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.092.png)

Once I do this we disable password access on the server by editing the / etc / ssh / sshd\ _ config file:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.093.png)

Then we just need to restart the service and when we re-register, we'll be using public key:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.094.png)

''If we try to register with a user which we don't have the public key will tell us the following:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.095.png)

### Port change

Now let's edit the configuration file to indicate the port:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.096.png)

And we will restart the service:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.097.png)



Now if we try to connect as we have done before, it will give us the following mistake:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.098.png)

To connect we must specify the port by which we connect with -p:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.099.png)

### Connect with a remote access client using tunnels
We will use kitty, when we open it on the first screen we enter the server ip and the port you have configured on the server for the ssh in my case 2222

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.100.png)







Now we add the port by which we will connect using the tunnel and then the ip followed by two points and the same port.

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.101.png)



Now we enter our user and password and we will have connected:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.102.png)

If we want to do the same but using a public key from windows, we press windows + r and write the following:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.103.png)

And we generate the public keys:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.104.png)

Now we go to the route we've saved it we copy the public key and we put it on the server, for comfort I have copied it from the client using ssh.

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.105.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.106.png)

Once added we save the file:

We're going to disable the password authentication and restart the service

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.107.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.097.png)

Now from the kitty we have to go to the ssh > auth, we give it to browse and select our private key, which must have the .ppk extension. I copied it into another directory for comfort for the tests.

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.108.png)

And we connect:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.109.png)

Here we have combined to connect with kitty using a tunnel + another port + public key.

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.110.png)


## VNCserver
We install it with the following command:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.111.png)

Below we set the configuration credentials for access users and administrators with the following command:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.112.png)

Now we go to the client and we enter the ip followed by the port by two points, if we don't know we can look at it with:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.113.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.114.png)

We will be given a warning as the communication is not encrypted, we give you to continue and we enter the access password, which we have previously put:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.115.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.116.png)

Since we do not have a graphic entry on the server, it will not show us an image, but we can see that we have established a connection in both windows and Linux:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.117.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.118.png)

### Web page management using ssh

1. Once the two virtual sites have been created, we want to establish a secure connection to each of our sites, for this we must establish a ssh tunnel in the same way we have established it to establish a remote connection per vnc.

2.Create a tunnel from the ssh client so that access to the private section of the department website is established by port 9999

3. With both established tunnels check that access to the iesgn.org web can be done smoothly by port 80

I only managed to do my page by default, for that we do a tunnel with kitty for example:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.119.png)

We now add the ports of origin and destination of the port:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.120.png)

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.121.png)

We now register with our user:

Once the tunnel is established we enter the localhost browser: 8888:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.122.png)

And so we have established a secure web connection.

If we close the tunnel we'll lose the connection:

![](../img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.123.png)
