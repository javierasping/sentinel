---
title: "Installation of android in GNS3 with KVM"
date: 2024-03-28T10:00:00+00:00
Description: Installation of android in GNS3 with KVM
tags: [GNS3,ANDORID,LINUX,DEBIAN,KVM]
hero: /images/redes/android_gns3/android.png
---



To download the android image you can do it from this page -- > https: / / www.fosshub.com / Android-x86.html:

```bash
wget https://www.fosshub.com/Android-x86.html?dwl=android-x86_64-9.0-r2.iso
```

Create a KVM machine as if it were a Debian, I've given it 2GB of RAM and 2 Cor:

![](../img/Pastedimage20240117194542.png)

In our case we can launch an automatic installation:

![](../img/Pastedimage20240117194647.png)

When you have the machine installed, turn off the machine and we'll import it in gns3. To do this we will take the KVM disk and import it into the directory where we have installed the GNS3 images, then property the copied disk to your user.

```bash
cp /var/lib/libvirt/images/android-wireguard.qcow2 /home/javiercruces/GNS3/images/QEMU/

javiercruces@HPOMEN15:~$ sudo chown javiercruces:javiercruces /home/javiercruces/GNS3/images/QEMU/android-wireguard.qcow2 
```

Now access your GNS3 and in preferences we will add a new QEMU VMs:

![](../img/Pastedimage20240117195338.png)

Select the emulation binary x86 _ 64 and assign the memory you consider appropriate, to me with 2GB works correctly:

![](../img/Pastedimage20240117195434.png)

As the image uses graphic environment we will select VNC:

![](../img/Pastedimage20240117195509.png)

And select the disk that we have copied to the folder images above:

![](../img/Pastedimage20240117195622.png)
