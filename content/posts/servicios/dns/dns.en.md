---
title: "DNS server configuration in Debian"
date: 2023-09-08T10:00:00+00:00
Description: DNS server configuration in our basic scenario under debian 10
tags: [Servicios,NAT,SMR,DHCP,SNAT,DNS,BIND9,DNSMASQ]
hero: images/servicios/dns/portada-dns.jpg
---


♪ DNS server settings in Debian
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




### DNS BIND 9
### Installation

The first thing we will do is uninstall dnsmasq since both are not compatible:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.065.png)

We can also see that it tells us that the / etc / dnsmasq.d / directory when not empty has not been deleted it would be good to delete it manually to remove all traces of previous configurations:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.066.png)


Now let's install them bind:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.067.png)

Configuration

Now we will edit the / etc / bind / named.conf.local file where we will create the areas (direct and reverse). In the case of practice we are asked a direct (isgn.com) and a reverse (network 192.168.1).

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.068.png)

We will add the following lines to that file:

In the / etc / bind directory are the db.empty and db.127 files (direct and reverse area configuration files respectively). We copy them to the / var / cache / bind directory to start adding the records

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.069.png)

We modify the / var / cache / bind / db.isgn file and include the following lines for direct resolution:

* javiercrosses is the name of my machine I have changed it to make things easier

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.070.png)

We will now do the same for the reverse resolution:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.071.png)

We will now restart the service to apply the changes:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.072.png)

In addition to make sure we have done the configuration well we will look at the state of the service to see if our areas are working:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.073.png)

This step is optional, but thanks to reviewing this I have discovered because I did not do the reverse resolution and thanks to seeing the areas that were loaded I realized that the error was in the / etc / bind / named.conf.local configuration file and I was able to fix it.

## # Reporter
So far, it would only solve the names and ip of our local network. If we want to set up a remander to ask in case the local DNS cannot give us the answer, we must edit the nano / etc / bind / named.conf.options file and add the following:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.074.png)

Before making this paragraph clear that as in the section of dnsmasq we already comment on the host file and modify the configuration of the dhcp to assign the dns automatically, I will omit it from this part.


### Commands to check service performance
Check the operation using the dig / nslookup command from the customers asking for the different names. Check that the DNS server makes forwarder asking with dig / nslookup the address ip of www.josedomingo.org.

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.075.png)

We see here that the answers are correct, those on our server are authorized while the page of Jose Domingo has given us a forwarder.

I will now make the same requests but inverse:

![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.076.png)
![](/servicios/dns/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.077.png)

With this we have checked that the dns server works properly.



