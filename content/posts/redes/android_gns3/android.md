---
title: "Instalación de android en GNS3 con KVM"
date: 2024-03-28T10:00:00+00:00
description: Instalación de android en GNS3 con KVM
tags: [GNS3,ANDORID,LINUX,DEBIAN,KVM]
hero: /images/redes/android_gns3/android.png
---



Para descargarnos la imagen de android puedes hacerlo desde esta pagina -->  https://www.fosshub.com/Android-x86.html :

```bash
wget https://www.fosshub.com/Android-x86.html?dwl=android-x86_64-9.0-r2.iso
```

Crea una maquina en KVM como si fuese un Debian , yo le he dado 2GB de RAM y 2 cores :

![](../img/Pastedimage20240117194542.png)

En nuestro caso podemos lanzar una instalación automática :

![](../img/Pastedimage20240117194647.png)

Cuando tengas la maquina instalada , apaga la maquina y vamos a importarla en gns3 . Para ello vamos a llevarnos el disco de KVM y vamos a importarlo en el directorio donde hayamos instalado las imágenes de GNS3 , luego haz propiedad del disco copiado a tu usuario .

```bash
cp /var/lib/libvirt/images/android-wireguard.qcow2 /home/javiercruces/GNS3/images/QEMU/

javiercruces@HPOMEN15:~$ sudo chown javiercruces:javiercruces /home/javiercruces/GNS3/images/QEMU/android-wireguard.qcow2 
```

Ahora accede a tu GNS3 y en preferencias vamos a añadir una nueva QEMU VMs :

![](../img/Pastedimage20240117195338.png)

Selecciona el binario de emulación x86_64 y asignale la memoria que consideres oportuna , a mi con 2GB me funciona correctamente : 

![](../img/Pastedimage20240117195434.png)

Como la imagen utiliza entorno gráfico vamos a seleccionar VNC :

![](../img/Pastedimage20240117195509.png)

Y selecciona el disco que hemos copiado a la carpeta images anteriormente :

![](../img/Pastedimage20240117195622.png)
