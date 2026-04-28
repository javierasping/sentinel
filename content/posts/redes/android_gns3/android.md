---
title: "Instalación de android en GNS3 con KVM"
date: 2024-03-28T10:00:00+00:00
description: Instalación de android en GNS3 con KVM
tags: [GNS3,ANDORID,LINUX,DEBIAN,KVM]
hero: /images/redes/android_gns3/android.png
---



Para descargar la imagen de Android, puede utilizar la siguiente página: https://www.fosshub.com/Android-x86.html

```bash
wget https://www.fosshub.com/Android-x86.html?dwl=android-x86_64-9.0-r2.iso
```

Cree una máquina virtual en KVM siguiendo el proceso similar a una instalación de Debian; se recomienda asignar 2 GB de RAM y 2 núcleos de CPU:

![](/redes/android_gns3/Pastedimage20240117194542.png)

En este caso, se puede iniciar una instalación automática:

![](/redes/android_gns3/Pastedimage20240117194647.png)

Una vez instalada la máquina, apáguela para proceder con la importación en GNS3. Para ello, copie el disco de KVM al directorio de imágenes de GNS3 y asigne la propiedad del archivo al usuario actual:

```bash
cp /var/lib/libvirt/images/android-wireguard.qcow2 /home/javiercruces/GNS3/images/QEMU/

javiercruces@HPOMEN15:~$ sudo chown javiercruces:javiercruces /home/javiercruces/GNS3/images/QEMU/android-wireguard.qcow2 
```

Ahora, acceda a GNS3 y, en el menú de Preferencias, añada una nueva máquina virtual QEMU:

![](/redes/android_gns3/Pastedimage20240117195338.png)

Seleccione el binario de emulación x86_64 y asigne la memoria RAM adecuada; 2 GB resultan suficientes para un funcionamiento correcto: 

![](/redes/android_gns3/Pastedimage20240117195434.png)

Dado que la imagen utiliza un entorno gráfico, seleccione VNC como método de consola:

![](/redes/android_gns3/Pastedimage20240117195509.png)

Finalmente, seleccione el disco que fue copiado previamente a la carpeta de imágenes:

![](/redes/android_gns3/Pastedimage20240117195622.png)
