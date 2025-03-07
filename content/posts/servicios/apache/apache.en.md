---
title: "Apache configuration under debian"
date: 2023-09-08T10:00:00+00:00
Description: Apache service configuration
tags: [Servicios,NAT,SMR,IPTABLES,SNAT,SSH,FORWARDING,APACHE]
hero: images/servicios/apache/portada-apache.jpg
---



### Install an Apache web server for use in an Intranet

To install the server we must run as root the following command:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.125.png)

Create within the / var / www / html directory a file called intrada.html where you put a welcome message

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.126.png)

Now I'll put it inside the route:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.127.png)

Next we will post a more complete page on our server, for it

use your web application website.


We must also give reading permits to others so that we can view it:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.128.png)

Access from customers, putting the following URL in a browser:

From debian client:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.129.png)

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.130.png)

Below we will post a more complete page on our server, for this use your web application website:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.131.png)

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.132.png)

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.133.png)

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.134.png)



Local name resolution: modify the required files in the BIND service and access using the name you have indicated:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.135.png)

As I had the dns before I used this name:

### Configuration of virtual websites using Apache
The first website will have the base directory will be / var / www / iesgn and will contain a page called index.html, where you will only see a welcome to the page of the Gonzalo Nazarene Institute.

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.136.png)

The second website will have the base directory will be / var / www / departments. On this site we will only have a home page index.html, welcoming the page of the departments of the institute.

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.137.png)

We need to have two files to make the configuration of the two virtual sites, for that we will copy the file 000-default.conf

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.138.png)

Once we have created the files we will add within each the following content:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.139.png)

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.140.png)

We will now have to create a symbolic link in the / etc / apache2 / sites-enabled directory.

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.141.png)

For these changes to be implemented, we must restart the service:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.142.png)

Now we should update the dns:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.143.png)

Once the dns are restarted, we can access both sites from the browser:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.144.png)

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.145.png)




### authenticated access to the Apache web server

To enable the basic authentication we must add the following lines to our site configuration file:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.146.png)

Now we create the password file, with the previously created user:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.147.png)

We restart the service and connect:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.148.png)

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.149.png)

Now let's have the department page access only the director and the teacher, and to address only the director, for that we add in departments:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.150.png)

Now let's add the users of the areas for that, we use this command:

- User teacher to departments:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.151.png)

- Director user to departments:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.152.png)

- User to address area:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.153.png)

We will now restart the service and check that we can access:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.154.png)

We will access departments:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.155.png)

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.156.png)

Now to the area management team:

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.157.png)

![](/servicios/apache/img/Aspose.Words.5fca9cc1-3c81-4853-a5ed-a70b0122341b.158.png)

