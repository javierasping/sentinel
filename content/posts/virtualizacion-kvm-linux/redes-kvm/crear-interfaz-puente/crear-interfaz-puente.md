---
title: "Cómo crear una interfaz puente (bridge) en el host KVM"
date: 2025-10-18T09:00:00+00:00
description: "Guía paso a paso para crear un bridge (br0) en Linux y conectarlo a libvirt, con ejemplos para Netplan y ifupdown (interfaces)."
tags: [KVM,Virtualizacion,Libvirt,Redes,Linux,Bridge]
hero: images/virtualizacion-kvm-linux/redes/redes-puente.png
weight: 3
---

# Crear una interfaz puente (bridge) en el host para KVM/libvirt

Un bridge (puente) en el host permite que tus máquinas virtuales se conecten directamente a la red física, como si fueran otro equipo más de la LAN. Es la base de las “redes puente” que vimos en los tipos de redes.

Importante: si haces esto por SSH remoto, podrías quedarte sin conexión al aplicar los cambios. Siempre que puedas, hazlo con acceso local/console o ten un plan de recuperación (KVM/IPMI, segunda interfaz, ventana de mantenimiento, etc.).

---

## 0. Preparación: identifica tu interfaz y haz copia de seguridad

1) Identifica la interfaz física con salida a tu LAN/Internet (ej.: `enp1s0`, `enp3s0`, `eth0`):

```bash
ip -br link
ip -br addr
```

2) Haz copia de tus ficheros de red antes de cambiar nada , usa el comando que aplique para tu caso:

```bash
sudo cp -a /etc/netplan /etc/netplan.bak.$(date +%F) 2>/dev/null 
sudo cp -a /etc/network/interfaces /etc/network/interfaces.bak.$(date +%F) 2>/dev/null 
```

3) Nota importante: la IP debe vivir en el bridge (br0), no en la interfaz física. La física quedará sin IP y “esclavada” al bridge.

---

## Opción A: Netplan (Ubuntu/Debian modernos)

Aplica a sistemas que usen Netplan (Ubuntu Server ≥ 18.04, Debian recientes si has migrado). El renderer más habitual es `networkd`, pero también puede ser `NetworkManager`. Aquí configuramos un `br0` y “esclavamos” la interfaz física al bridge.

Ejemplo DHCP (renderer networkd):

```yaml
# /etc/netplan/01-br0.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp1s0:
      dhcp4: no
      dhcp6: no
  bridges:
    br0:
      interfaces: [enp1s0]
      dhcp4: yes
      dhcp6: no
      parameters:
        stp: true
        forward-delay: 0
```

Ejemplo IP estática:

```yaml
# /etc/netplan/01-br0.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp1s0:
      dhcp4: no
      dhcp6: no
  bridges:
    br0:
      interfaces: [enp1s0]
      addresses: [192.168.1.50/24]
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses: [1.1.1.1,8.8.8.8]
      parameters:
        stp: true
        forward-delay: 0
```

Aplicar y verificar:

```bash
sudo netplan apply
ip -br addr show br0
```

---

## Opción B: interfaces (/etc/network/interfaces)

Para servidores Debian/Ubuntu que usan ifupdown clásico (sin NetworkManager/Netplan). Asegúrate de tener instalado el soporte de bridge (p. ej., paquete `bridge-utils` para las opciones `bridge_*` y la herramienta `brctl`).

Ejemplo 1 (DHCP en `br0`, la física sin IP):

```ini
auto lo
iface lo inet loopback

auto enp1s0
iface enp1s0 inet manual

auto br0
iface br0 inet dhcp
    bridge_ports enp1s0
    bridge_stp on
    bridge_fd 0
```

Ejemplo 2 (IP estática en `br0`):

```ini
auto lo
iface lo inet loopback

auto enp1s0
iface enp1s0 inet manual

auto br0
iface br0 inet static
    address 192.168.1.50/24
    gateway 192.168.1.1
    dns-nameservers 1.1.1.1 8.8.8.8
    bridge_ports enp1s0
    bridge_stp on
    bridge_fd 0
```

Notas ifupdown:
- La interfaz física (`enp1s0`) queda en modo `manual` (sin IP). La IP pasa a `br0`.
- `bridge_stp on` habilita STP en el bridge; `bridge_fd 0` minimiza el retardo de reenvío (ajústalo a tus necesidades de red).
- Si usas VLANs, puedes usar `bridge_vlan_aware yes` en distros que lo soporten o gestionar VLANs en las VMs.

Aplicar cambios con cuidado (puedes perder SSH). Opciones:

```bash
# Reinicio del servicio (más simple, puede cortar conexión SSH):
sudo systemctl restart networking.service

# O de forma granular (si tienes acceso local/TTY):
sudo ifdown enp1s0 
sudo ifdown br0 
sudo ifup br0
```

---

## Conectar las VMs al bridge (libvirt)

Una vez tengas `br0` operativo:

- Con `virt-install`:

```bash
virt-install \
  --name vm-bridge-ejemplo \
  --memory 2048 \
  --vcpus 2 \
  --disk size=10 \
  --os-variant debian12 \
  --network bridge=br0,model=virtio \
  --cdrom /ruta/a/tu.iso \
  --noautoconsole
```

- Con `virsh` en una VM existente (adjuntar interfaz puente):

```bash
virsh attach-interface --domain VM_EXISTENTE \
  --type bridge --source br0 \
  --model virtio --config --live
```

- En XML de dominio (fragmento):

```xml
<interface type='bridge'>
  <source bridge='br0'/>
  <model type='virtio'/>
</interface>
```

Tras arrancar la VM, debería obtener IP de tu red física (vía DHCP del router) o la que le asignes si usas estática dentro del invitado.

---

## Comprobación de funcionamiento

- En el host:

```bash
ip link show br0
bridge link
ip route
```

Con `ip a` deberías ver algo similar (ejemplo):

```bash
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br0 state UP group default qlen 1000
  link/ether 52:54:00:22:d7:3f brd ff:ff:ff:ff:ff:ff
3: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
  link/ether 92:d8:69:79:60:69 brd ff:ff:ff:ff:ff:ff
  inet 192.168.121.169/24 brd 192.168.121.255 scope global dynamic br0
     valid_lft 3595sec preferred_lft 3595sec
```

Si usas la herramienta clásica `brctl` (paquete bridge-utils), puedes listar puentes e interfaces:

```bash
sudo brctl show
# Salida esperada:
# bridge name	bridge id		STP enabled	interfaces
# br0		8000.7eb448933f70	no		enp1s0
```

- En la VM conectada al bridge:

```bash
ip -br addr
ping -c 2 8.8.8.8
ping -c 2 <IP_DEL_ROUTER>
```

- Desde otro equipo de la LAN, haz ping a la IP de la VM bridged.

---

## Gestión de redes puente públicas con libvirt (bridge y macvtap)

Además de conectar directamente las VMs al `br0`, puedes definir redes en libvirt:

### 1) Red puente conectada a `br0` (mode="bridge")

Fichero `red-bridge.xml`:

```xml
<network>
  <name>red_bridge</name>
  <forward mode="bridge"/>
  <bridge name="br0"/>
  <!-- Sin DHCP/DNS: los dará tu red física -->
</network>
```

Crear e iniciar:

```bash
virsh net-define red-bridge.xml
virsh net-start red_bridge
virsh net-list --all
```

Conecta la VM a esta red puente:

```bash
virsh detach-interface debian12 network --mac XX:XX:XX:XX:XX:XX --persistent
virsh attach-interface debian12 network red_bridge --model virtio --persistent
```

También puedes adjuntar directamente al puente del host:

```bash
virsh attach-interface debian12 bridge br0 --model virtio --persistent
```

### 2) Red macvtap (comparte interfaz física del host, sin puente)

Fichero `red-macvtap.xml`:

```xml
<network>
  <name>red_macvtap</name>
  <forward mode="bridge">
    <interface dev="enp1s0"/>
  </forward>
</network>
```

Crear e iniciar:

```bash
virsh net-define red-macvtap.xml
virsh net-start red_macvtap
```

Conectar VM a macvtap y limitación importante:

```bash
virsh detach-interface debian12 network --mac XX:XX:XX:XX:XX:XX --persistent
virsh attach-interface debian12 network red_macvtap --model virtio --persistent

# Nota: macvtap suele impedir comunicación directa host↔VM.
```

Ejemplo de fallo esperado desde la VM al host (por la limitación macvtap):

```bash
ping 192.168.100.127
# From 192.168.100.250 icmp_seq=1 Destination Host Unreachable
```

---

## Problemas comunes y consejos

- Te quedas sin red al aplicar cambios: puede pasar si migras IP/gateway al bridge estando por SSH. Usa consola local o programa una ventana de mantenimiento.
- Doble gestor de red: evita que NetworkManager y netplan/networkd gestionen la misma interfaz.
- STP y switches: el STP puede introducir pequeña latencia al levantar puertos; usa `forward-delay 0` si sabes lo que haces.
- VLANs: si tu puerto físico es trunk, necesitarás configurar VLANs en el bridge o en las VMs (virtio con VLAN tag, etc.).
- Firewall: revisa reglas si aplicas políticas estrictas; el tráfico bridged pasa a L2.
- Persistencia: asegúrate de que tu método (Netplan/NM/networkd) aplica al arranque.

---

## Referencias

- [curso_virtualizacion_linux — GitHub](https://github.com/josedom24/curso_virtualizacion_linux)
- [Netplan](https://netplan.io/examples)
- [Libvirt: Networking overview](https://libvirt.org/network.html)
- [Debian Wiki: BridgeNetworkConnections](https://wiki.debian.org/BridgeNetworkConnections)
- [iproute2 — ip-link, ip-address, ip-route](https://man7.org/linux/man-pages/man8/ip.8.html)
- [TUN/TAP (kernel docs)](https://www.kernel.org/doc/Documentation/networking/tuntap.txt)
- [ip-netns (network namespaces)](https://man7.org/linux/man-pages/man8/ip-netns.8.html)
- [veth (ip-link)](https://man7.org/linux/man-pages/man8/ip-link.8.html)
- [Bonding (kernel docs)](https://www.kernel.org/doc/Documentation/networking/bonding.txt)
- [brctl (bridge-utils) manpage](https://manpages.debian.org/bridge-utils)

---