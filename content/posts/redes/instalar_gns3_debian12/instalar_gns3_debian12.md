---
title: "Instalación GNS3 en Debian 12 "
date: 2024-09-08T10:00:00+00:00
description: Instalación de simulador de redes GNS3
tags: [Redes, Wireshark, GNS3]
hero: images/redes/instalacion_wireshark_gns3/gns3_deb12.png
---
En este artículo, te presento una actualización del proceso de instalación de GNS3 en Debian 12, basado en el post anterior para Debian 11. Si necesitas detalles más profundos sobre la instalación o la configuración de GNS3, te recomiendo revisar la versión anterior.

## Instalación GNS3
Actualizamos los repositorios e instalamos las actualizaciones disponibles del sistema.

```bash
javiercruces@HPOMEN15:~$ sudo apt update -y && sudo apt upgrade -y 
```

Instalamos las dependencias necesarias para GNS3, incluyendo Python, herramientas de virtualización (KVM,QEMU,libvirt), bibliotecas adicionales (PyQt5,dynamips) y otras utilidades.

```bash
javiercruces@HPOMEN15:~$ sudo apt install python3 python3-pip pipx python3-pyqt5 python3-pyqt5.qtwebsockets python3-pyqt5.qtsvg qemu-kvm qemu-utils libvirt-clients libvirt-daemon-system virtinst dynamips software-properties-common ca-certificates curl gnupg2 bridge-utils virt-manager libvirt-daemon -y
```

Habilitamos y arrancamos el servicio de virtualización libvirtd y nos añadimos al grupo "libvirt" para otorgarle permisos sobre las máquinas virtuales y redes de KVM .

```bash
javiercruces@HPOMEN15:~$ sudo systemctl enable --now libvirtd && sudo usermod -aG libvirt $(whoami)
```

Instalamos las aplicaciones principales de GNS3: el servidor (gns3-server) y la interfaz gráfica (gns3-gui) utilizando pipx para un entorno Python aislado de forma comoda , sin necesidad de crear un entorno virtual a mano.

```bash
javiercruces@HPOMEN15:~$ pipx install gns3-server && pipx install gns3-gui
```

Aseguramos que el directorio de binarios de pipx esté en la variable de entorno PATH para que los comandos de GNS3 sean accesibles globalmente desde cualquier terminal.

```bash
javiercruces@HPOMEN15:~$ pipx ensurepath
```

Inyectamos el paquete PyQt5 en el entorno de gns3-gui, asegurándonos de que tenga todas las dependencias necesarias.

```bash
javiercruces@HPOMEN15:~$ pipx inject gns3-gui gns3-server PyQt5
```

Iniciamos la red por defecto de KVM y la configuraremos para que al reiniciar se incie de forma automatica .
```bash
javiercruces@HPOMEN15:~$  virsh --connect=qemu:///system net-start default
La red default se ha iniciado

javiercruces@HPOMEN15:~$  virsh --connect=qemu:///system net-autostart default
La red default ha sido marcada para iniciarse automáticamente
```

Reiniciamos el sistema para aplicar los cambios, como la configuración de grupos y PATH.

```bash
javiercruces@HPOMEN15:~$ sudo reboot 
```

Ahora podremos iniciar gns3 , pero te recomiendo que configures los siguientes apartados que tienes en el post .

```bash
javiercruces@HPOMEN15:~$ gns3
```

## Instalación ubridge 

Clonamos el repositorio de ubridge desde GitHub. Ubridge es una herramienta necesaria para GNS3, que permite gestionar el tráfico entre las interfaces de red virtualizadas.

```bash
javiercruces@HPOMEN15:~$ git clone https://github.com/GNS3/ubridge.git
```

Nos movemos al directorio del proyecto recién clonado.

```bash
javiercruces@HPOMEN15:~$ cd ubridge/
```

Compilamos el código fuente de ubridge utilizando "make" .

```bash
javiercruces@HPOMEN15:~/ubridge$ make 
```

Instalamos el binario de ubridge en el sistema para que esté disponible globalmente.

```bash
javiercruces@HPOMEN15:~/ubridge$ sudo make install
```

Asignamos permisos de ejecución al archivo binario de ubridge

```bash
javiercruces@HPOMEN15:~/ubridge$ chmod +x ubridge
```
Copiamos el archivo binario a "/usr/local/bin", una ruta estándar para comandos disponibles globalmente en el sistema.

```bash
javiercruces@HPOMEN15:~/ubridge$ cp -p ubridge /usr/local/bin
```
Configuramos permisos especiales para ubridge, permitiéndole acceso a operaciones de red (cap_net_admin) y envío de paquetes en bruto (cap_net_raw), necesarias para su funcionamiento.

```bash
javiercruces@HPOMEN15:~/ubridge$ sudo setcap cap_net_admin,cap_net_raw=ep /usr/local/bin/ubridge
```

## Instalación vpcs

Clonamos el repositorio de VPCS desde GitHub. VPCS (Virtual PC Simulator) es una herramienta ligera que simula PCs básicos para pruebas de red en GNS3.

```bash
javiercruces@HPOMEN15:~$ git clone https://github.com/GNS3/vpcs.git
```

Accedemos al directorio donde hemos clonado el repositorio y ejecutamos el script que nos compilara el codigo fuente del programa.

```bash
javiercruces@HPOMEN15:~$ cd vpcs/src
javiercruces@HPOMEN15:~/vpcs/src$ sudo ./mk.sh
```

Dentro de la carpeta src tendremos el ejecutable de las maquinas vpcs , guarda esta ruta ya que tendras que configurarla en gns3 .

```bash
javiercruces@HPOMEN15:~/vpcs/src$ ls | grep c
vpcs
javiercruces@HPOMEN15:~/vpcs/src$ pwd
/home/javiercruces/vpcs/src
```

En preferencias tienes que añadir la ruta donde has guardado el fichero compilado vpcs , en mi caso la ruta seria /home/javiercruces/vpcs/src/vpcs


![](/redes/instalar_gns3_debian12/img/vpc.png)


<!-- ## GNS3 VM

En mi caso configure VMware Workstation puedes descargarlo desde este [enlace](https://support.broadcom.com/group/ecx/productfiles?subFamily=VMware%20Workstation%20Pro&displayGroup=VMware%20Workstation%20Pro%2017.0%20for%20Linux&release=17.6.1&os=&servicePk=524584&language=EN) . Para ello debes estar registrado en la pagina .

Una vez descaargado los ficheros los comandos para instalarlo son los siguientes .

Le damos permiso de ejecucion al fichero .
```bash 
javiercruces@HPOMEN15:~/Descargas/VMware-Player-17.6.1-24319023.x86_64.bundle$ chmod + VMware-Player-17.6.1-24319023.x86_64.bundle 

```

Ejecutamos con sh el script y esperamos a que se instale .
```bash
javiercruces@HPOMEN15:~/Descargas/VMware-Player-17.6.1-24319023.x86_64.bundle$ sudo sh VMware-Player-17.6.1-24319023.x86_64.bundle
Extracting VMware Installer...done.
Installing VMware Player 17.6.1
    Configuring...
[######################################################################] 100%
Installation was successful.

``` -->


<!-- Errores 

```bash
Could not start Telnet console with command 'xterm -T "PC1" -e "telnet localhost 5001"': [Errno 2] No existe el fichero o el directorio: 'xterm'
javiercruces@HPOMEN15:~$ sudo apt install xterm

``` -->