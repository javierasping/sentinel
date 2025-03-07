---
title: "Windows Ssh Service Settings"
date: 2023-09-08T10:00:00+00:00
Description: Learn how to set ssh service on Windows
tags: [Windows,Sistemas,ISO,ASO]
hero: images/sistemas/ssh_win/windows-ssh.jpg
---


## 1.Installation of the feature

The first thing we'll check is to check if the ssh server is installed in the machine we want to connect to.

```ps
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH\*'
```

![](/sistemas/ssh_windows/img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.001.jpeg)

In case we have the feature we will install it:

```ps
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

![](/sistemas/ssh_windows/img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.002.png)

By default the service will be stopped so we take it off:

![](/sistemas/ssh_windows/img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.003.png)

We can set it to automatically boot when you restart the computer:

![](/sistemas/ssh_windows/img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.004.png)

#2. Connect us using key pair

The first thing we will do is generate a couple of keys in the client, with ssh-keygen:

![](/sistemas/ssh_windows/img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.005.jpeg)

Using SCP we can either take our published key or manually add it to the automated _ keys file:

![](/sistemas/ssh_windows/img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.006.png)

![](/sistemas/ssh_windows/img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.007.png)

And we try to connect using the key:

![](/sistemas/ssh_windows/img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.008.jpeg)

If we want the service to only work with public and private keys, we edit the C:\ ProgramData\ ssh\ sshd\ _ config file.

![](/sistemas/ssh_windows/img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.009.png)

If we want to connect with a Linux client, we will have to do the same process. If the server was Linux we could use the ssh-copy-id utility however it is not compatible with Windows servers so we will use scp:

![](/sistemas/ssh_windows/img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.010.png)

Once added, we can connect:

![](/sistemas/ssh_windows/img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.011.png)

