---
title: "Sharing Network Resources on Windows Server"
date: 2023-09-08T10:00:00+00:00
Description: Learn how to share network resources on Windows Server
tags: [Windows,Sistemas,ISO,ASO]
hero: images/sistemas/compartir_directorios_win/portada.jpg
---


In the business environment, the capacity to share resources in network is essential for collaboration and operational efficiency. In this article, we will explore how to share directories in a Windows Server environment, addressing the methods through both the graphical interface and cmd and PowerShell.

### From the graphic interface

We can share a directory of our server, accessing its properties. Once here we click on the share menu:

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.001.png)

We will now give permission to users who wish to have access to this:

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.002.jpeg)

Once shared it will show us the route we will have to put to access this resource, which we can modify to our taste in advanced shared use:

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.003.png)

From a client we can see the resources that our server is sharing using net view:

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.004.png)

We can map the network drive from the command line using net use:

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.005.png)

Let's create a directory and check that it has been created:

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.006.png)

We see that the server has been created:

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.007.png)

We can also do this from the management of users and groups of active directory:

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.008.png)

### Share resources from cmd

Now let's use net share to share a network resource through the command line:

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.009.png)

If from another client we see the resources that the core server shares, we will see:

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.010.png)

If we want to change the permissions of a shared resource we can use the cacls and icacls commands. We also have the possibility to do so using the graphical interface with RSAT.

### Commands powershell

We will create the shared resource

```ps
New-SmbShare -Name JCD\_comp -Path "C:\compartir\" -FullAccess "Administrador"
```

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.011.png)

If we want to add specific permissions to a group when creating the shared resource would be:

```ps
New-SmbShare -Name <Nombre-de-la-carpeta> -Path <Ruta-de-la-carpeta> -ReadAccess "<Grupo-o-usuario-que-tiene-acceso-de-lectura>" -FullAccess "<Grupo-o-usuario-que-tiene- acceso-total>"
```

If after this we want to add or remove permissions to any user or group to the shared samba directory:

```ps
Set-SmbPathAcl -Path "C:\compartir" -AceType Allow -AccessType Write -AccountName UsuariosCompartidos
```

If on the contrary we want to remove permissions to the user or group:

```ps
Remove-SmbPathAcl -Path "C:\compartir" -AceType Allow -AccessType Write -AccountName UsuariosCompartidos
```

To mount this shared directory on another Windows host:

```ps
New-PSDrive -Name J -PSProvider FileSystem -Root [\\172.22.9.143\JCD_comp](file://172.22.9.143/JCD_comp)
```

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.012.png)

We can also list to see if it has been mounted correctly:

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.013.jpeg)

We will list the content of it to see if we have access to the:

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.014.png)

