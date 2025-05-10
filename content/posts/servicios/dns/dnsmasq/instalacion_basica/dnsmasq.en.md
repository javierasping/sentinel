---
title: "DNS server configuration in Debian"
date: 2023-09-08T10:00:00+00:00
Description: DNS server configuration in our basic scenario under debian 10
tags: [Servicios,NAT,SMR,DHCP,SNAT,DNS,DNSMASQ]
hero: images/servicios/dns/dnsmasq.png
---

### Dnsmasq

The dnsmasq package allows you to start a DNS server in a very simple way. Simply by installing and starting the dnsmasq service, without any additional configuration, our PC will become a DNS cache server and will also solve the names we have configured in the / etc / hosts file of our server. The resolution will work both directly and inversely, that is, it will solve the IP given a PC name and the PC name given the IP.

### Installation
To install it only the following command will be necessary:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.048.png)

Configuration
Then we edit the / etc / dnsmasq.conf file and modify the following lines:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.049.png)

1. We discomment strict-order for DNS requests to be made to the servers that appear in the / etc / resolv.conf file in the order in it appear.

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.050.png)

2.We include network interfaces that must accept DNS requests, discomment the interface line for example: interface = eth0

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.051.png)

We will now create our configuration file:

3. We create the configuration file of our area:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.052.png)

4. The domain we have chosen is iesgn.org

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.053.png)

5. We assume that the name of the server is miseror.

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.054.png)

6.We will assume that we have a ftp server called ftp.iesgn.org and that it is in 192.168.1.201 (this is fictitious) and that we have two websites: www.iesgn.org and departments.iesgn.org.

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.055.png)

7. We also want to name the client who had a reservation assigned: smooth.

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.056.png)

8. We restart the service

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.057.png)



## modification on DHCP server
Configure the customers and indicate that your DNS is our server. If you have a DHCP server modify it to send the new DNS to the customers.

We edit the file:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.058.png)

And we restart the service:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.059.png)

Now we'll check if the client has changed our dns by looking at the following file:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.060.png)

We have been successfully changed.

### Command to check the operation of dns
Check the operation using the dig / nslookup command from the customers asking for the different names. Check that the DNS server makes forwarder asking with dig / nslookup the address ip of www.josedomingo.org.

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.061.png)

For the Jose Sunday page the answer is unauthorized because our server does not have the resolution in your file and has to use a forwarder

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.062.png)



As you see above I have created my own area and despite having followed the steps of this [page] (https: / / www.josedomingo.org / pledin / 2020 / 12 / servo-dns-dnsmasq /) of Jose Domingo, I have not managed to get the answers authorized.

I created the dns.conf file.

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.063.png)

And I created my area:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.064.png)

I have also tried more things however the only way I have got to give me an authorized response is by having only the resolutions in the host file of the server, without creating my area.