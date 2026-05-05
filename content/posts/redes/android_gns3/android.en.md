---
title: "Installation of android in GNS3 with KVM"
date: 2024-03-28T10:00:00+00:00
Description: Installation of android in GNS3 with KVM
tags: [GNS3,ANDORID,LINUX,DEBIAN,KVM]
hero: /images/redes/android_gns3/android.png
---

To download the Android image, you can use the following page: https://www.fosshub.com/Android-x86.html

```bash
wget https://www.fosshub.com/Android-x86.html?dwl=android-x86_64-9.0-r2.iso
```

Create a KVM machine similar to a Debian installation; it is recommended to assign 2 GB of RAM and 2 CPU cores:

![](/redes/android_gns3/img/Pastedimage20240117194542.png)

In this case, an automatic installation can be initiated:

![](/redes/android_gns3/img/Pastedimage20240117194647.png)

Once the machine is installed, power it off to proceed with the import into GNS3. To do this, copy the KVM disk to the GNS3 images directory and change the ownership of the copied disk to your user:

```bash
cp /var/lib/libvirt/images/android-wireguard.qcow2 /home/javiercruces/GNS3/images/QEMU/

javiercruces@HPOMEN15:~$ sudo chown javiercruces:javiercruces /home/javiercruces/GNS3/images/QEMU/android-wireguard.qcow2 
```

Now, access GNS3 and, in Preferences, add a new QEMU VM:

![](/redes/android_gns3/img/Pastedimage20240117195338.png)

Select the x86_64 emulation binary and assign an appropriate amount of memory; 2 GB is sufficient for correct operation:

![](/redes/android_gns3/img/Pastedimage20240117195434.png)

Since the image uses a graphical environment, select VNC as the console type:

![](/redes/android_gns3/img/Pastedimage20240117195509.png)

Finally, select the disk that was previously copied to the images folder:

![](/redes/android_gns3/img/Pastedimage20240117195622.png)
