---
title: "Configuración servicio ssh en Windows"
date: 2023-09-08T10:00:00+00:00
description: Aprende cómo configuración servicio ssh en Windows
tags: [Windows,Sistemas,ISO,ASO]
hero: images/sistemas/ssh_win/windows-ssh.jpg
---
## 1.Instalación de la característica

Lo primero que comprobaremos es comprobar si el servidor ssh esta instalado en la maquina a la cual queremos conectarnos .

```ps
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH\*'
```

![](../img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.001.jpeg)

En el caso de que tengamos la característica la instalaremos : 

```ps
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
```

![](../img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.002.png)

Por defecto el servicio estará parado así que lo arrancamos :

![](../img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.003.png)

Podemos configurarlo para que arranque automáticamente al reiniciar el equipo :

![](../img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.004.png)

## 2.Conectarnos usando par de claves

Lo primero que haremos sera generar un par de claves en el cliente , con ssh-keygen :

![](../img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.005.jpeg)

Usando SCP podemos llevarnos nuestra clave publica o añadirla manualmente al fichero de authorized_keys :

![](../img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.006.png)

![](../img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.007.png)

Y probamos a conectarnos usando la clave :

![](../img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.008.jpeg)

Si queremos que solo el servicio funcione con claves publicas y privadas , editamos el fichero C:\ProgramData\ssh\sshd\_config.

![](../img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.009.png)

Si queremos conectarnos con un cliente Linux , deberemos hacer el mismo proceso . Si el servidor fuese Linux podríamos usar la utilidad ssh-copy-id sin embargo no es compatible con servidores Windows así que usaremos scp :

![](../img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.010.png)

Una vez añadida podremos conectarnos :

![](../img/Aspose.Words.abd631a7-a62e-4d27-bef0-1d38f74ce102.011.png)

