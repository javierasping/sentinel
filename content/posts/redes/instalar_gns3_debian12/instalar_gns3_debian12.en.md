---
title: "Installation GNS3 in Debian 12"
date: 2024-09-08T10:00:00+00:00
Description: GS3 network simulator installation
tags: [Redes, Wireshark, GNS3]
hero: images/redes/instalacion_wireshark_gns3/gns3_deb12.png
---
In this article, I present an update of the process of installing GNS3 in Debian 12, based on the previous post for Debian 11. If you need more detailed details about the installation or configuration of GNS3, I recommend you review the previous version.

## GNS3 installation
We update the repositories and install the available system updates.

```bash
javiercruces@HPOMEN15:~$ sudo apt update -y && sudo apt upgrade -y 
```

We install the necessary dependencies for GNS3, including Python, virtualization tools (KVM, QEMU, libvirt), additional libraries (PyQt5, dynamipes) and other utilities.

```bash
javiercruces@HPOMEN15:~$ sudo apt install python3 python3-pip pipx python3-pyqt5 python3-pyqt5.qtwebsockets python3-pyqt5.qtsvg qemu-kvm qemu-utils libvirt-clients libvirt-daemon-system virtinst dynamips software-properties-common ca-certificates curl gnupg2 bridge-utils virt-manager libvirt-daemon -y
```

We enable and start the libvirtd virtualization service and add to the "libvirt" group to give you permissions on the virtual machines and KVM networks.

```bash
javiercruces@HPOMEN15:~$ sudo systemctl enable --now libvirtd && sudo usermod -aG libvirt $(whoami)
```

We install the main GNS3 applications: the server (gns3-server) and the graphic interface (gns3-gui) using pipx for an isolated Python environment in a comfortable way, without creating a virtual environment by hand.

```bash
javiercruces@HPOMEN15:~$ pipx install gns3-server && pipx install gns3-gui
```

We ensure that the directory of pipx binaries is in the PATH environment variable so that the GNS3 commands are accessible globally from any terminal.

```bash
javiercruces@HPOMEN15:~$ pipx ensurepath
```

We inject the PyQt5 package into the gns3-gui environment, making sure that it has all the necessary dependencies.

```bash
javiercruces@HPOMEN15:~$ pipx inject gns3-gui gns3-server PyQt5
```

We start the default KVM network and set it up so that when restart it will be automatically incited.
```bash
javiercruces@HPOMEN15:~$  virsh --connect=qemu:///system net-start default
La red default se ha iniciado

javiercruces@HPOMEN15:~$  virsh --connect=qemu:///system net-autostart default
La red default ha sido marcada para iniciarse automáticamente
```

We restart the system to apply changes, such as group settings and PATH.

```bash
javiercruces@HPOMEN15:~$ sudo reboot 
```

Now we can start gns3, but I recommend you set up the following sections you have in the post.

```bash
javiercruces@HPOMEN15:~$ gns3
```

### Ubridge installation

We clone the ubridge repository from GitHub. Ubridge is a necessary tool for GNS3, which allows to manage traffic between virtualized network interfaces.

```bash
javiercruces@HPOMEN15:~$ git clone https://github.com/GNS3/ubridge.git
```

We move to the newly cloned project directory.

```bash
javiercruces@HPOMEN15:~$ cd ubridge/
```

We compile the ubridge source code using "make."

```bash
javiercruces@HPOMEN15:~/ubridge$ make 
```

We install the ubridge binary in the system to make it available globally.

```bash
javiercruces@HPOMEN15:~/ubridge$ sudo make install
```

We assign execution permissions to the Ubridge binary file

```bash
javiercruces@HPOMEN15:~/ubridge$ chmod +x ubridge
```

We copy the binary file to "/usr/local/bin," a standard command route available globally in the system.

```bash
javiercruces@HPOMEN15:~/ubridge$ cp -p ubridge /usr/local/bin
```

We set up special permissions for ubridge, allowing you access to network operations (cap _ net _ admin) and the sending of raw packages (cap _ net _ raw) necessary for its operation.

```bash
javiercruces@HPOMEN15:~/ubridge$ sudo setcap cap_net_admin,cap_net_raw=ep /usr/local/bin/ubridge
```

### Vpcs installation

We clone the VPCS repository from GitHub. VPCS (Virtual PC Simulator) is a light tool that simulates basic PCs for network testing in GNS3.

```bash
javiercruces@HPOMEN15:~$ git clone https://github.com/GNS3/vpcs.git
```

We access the directory where we cloned the repository and run the script that compiled the program source code.

```bash
javiercruces@HPOMEN15:~$ cd vpcs/src
javiercruces@HPOMEN15:~/vpcs/src$ sudo ./mk.sh
```

Within the src folder we will have the executable of the vpcs machines, save this route as you will have to set it in gns3.

```bash
javiercruces@HPOMEN15:~/vpcs/src$ ls | grep c
vpcs
javiercruces@HPOMEN15:~/vpcs/src$ pwd
/home/javiercruces/vpcs/src
```

In preferences you have to add the route where you have saved the compiled file vpcs, in my case the serious route /home/javiercruces/vpcs/src/vpcs


![](/redes/instalar_gns3_debian12/img/vpc.png)

