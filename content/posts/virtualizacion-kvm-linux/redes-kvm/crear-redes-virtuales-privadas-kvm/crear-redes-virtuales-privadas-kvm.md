---
title: "Cómo crear y configurar redes virtuales privadas"
date: 2025-10-18T09:00:00+00:00
description: "Guía práctica para crear redes virtuales en KVM/libvirt: NAT, redes aisladas y redes muy aisladas. Incluye comandos con virsh, ejemplos XML y verificación."
tags: [KVM,Virtualizacion,Libvirt,Redes,Linux]
hero: images/virtualizacion-kvm-linux/redes/redes-pivadas.png
weight: 2
---
En esta guía crearemos tres tipos de redes virtuales gestionadas por libvirt:

- NAT (Network Address Translation)
- Aislada (Isolated)
- Muy aislada (Very isolated)
 weight: 2

---

## Requisitos y notas previas

- Paquetes: `libvirt-daemon` y `libvirt-daemon-system` (o equivalentes en tu distro). Opcional: `virt-manager`.
- Ejecuta los comandos como root o con `sudo`.
- Servicio: `systemctl status libvirtd` debe estar activo.
- Listar redes actuales: `virsh net-list --all`
- Rutas de configuración (persistentes): `/etc/libvirt/qemu/networks/`

Cuidado con conflictos de subred: usa rangos que no choquen con tu red física ni con otras redes libvirt.

---

## Paso 1: Crear una red NAT

La red NAT permite que las VMs tengan IPs privadas y salgan al exterior a través del host.

### 1.1 Definición XML (ejemplo)

```xml
<network>
  <name>red_nat_lab</name>
  <forward mode='nat'/>
  <bridge name='virbr101' stp='on' delay='0'/>
  <ip address='192.168.101.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.101.100' end='192.168.101.254'/>
    </dhcp>
  </ip>
</network>
```

- `<forward mode='nat'/>` habilita NAT.
- El host tendrá `192.168.101.1/24` en el bridge `virbr101`.
- El DHCP de libvirt asignará IPs en el rango indicado.

### 1.2 Crear, arrancar y hacer autostart

```bash
# Guardar el XML en red_nat_lab.xml y luego:
virsh net-define red_nat_lab.xml
virsh net-autostart red_nat_lab
virsh net-start red_nat_lab

# Verificación
virsh net-list --all
virsh net-info red_nat_lab
virsh net-dumpxml red_nat_lab
```

### 1.3 Conecta una VM a la red NAT

- Con `virt-install`:

```bash
virt-install \
  --name vm-nat-ejemplo \
  --memory 2048 \
  --vcpus 2 \
  --disk size=10 \
  --os-variant debian12 \
  --network network=red_nat_lab,model=virtio \
  --cdrom /ruta/a/tu.iso \
  --noautoconsole
```

- Con `virsh` (VM existente):

```bash
virsh attach-interface --domain VM_EXISTENTE \
  --type network --source red_nat_lab \
  --model virtio --config --live
```

### 1.4 Verifica que funciona

```bash
# Comprueba que la red está activa
virsh net-list --all

# Ver que el bridge existe y tiene IP
ip addr show virbr101 | grep inet

# Dentro de una VM conectada a red_nat_lab, prueba conectividad
ping -c 2 1.1.1.1
```

---

## Paso 2: Crear una red aislada

Red privada sin salida al exterior. El host puede tener IP en el bridge para comunicarse con las VMs y opcionalmente ofrecer DHCP/DNS.

### 2.1 Definición XML (con DHCP opcional)

```xml
<network>
  <name>red_aislada_dev</name>
  <bridge name='virbr102' stp='on' delay='0'/>
  <ip address='192.168.102.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.102.100' end='192.168.102.254'/>
    </dhcp>
  </ip>
</network>
```

- Sin `<forward>`: no hay NAT ni enrutamiento hacia fuera.
- Si prefieres todo estático, elimina el bloque `<dhcp>` y configura IPs manualmente en cada VM.

### 2.2 Define, arranca y verifica

```bash
virsh net-define red_aislada_dev.xml
virsh net-autostart red_aislada_dev
virsh net-start red_aislada_dev

virsh net-list --all
virsh net-info red_aislada_dev
```

Conecta VMs igual que en el caso NAT, pero apuntando a `red_aislada_dev`.

---

## Paso 3: Crear una red muy aislada

Segmento L2 compartido entre VMs, sin IP del host en el bridge y sin servicios de libvirt (sin DHCP/DNS). Las VMs deberán configurarse con IP estática o desplegar su propio servicio interno.

### 3.1 Definición XML (sin IP ni DHCP)

```xml
<network>
  <name>red_muy_aislada</name>
  <bridge name='virbr103' stp='on' delay='0'/>
</network>
```

### 3.2 Define, arranca y verifica

```bash
virsh net-define red_muy_aislada.xml
virsh net-autostart red_muy_aislada
virsh net-start red_muy_aislada

virsh net-list --all
virsh net-dumpxml red_muy_aislada
```

Verificación útil:

```bash
# Este bridge no tendrá IP del host (sin L3)
ip addr show virbr103 | grep inet || echo "sin IP (esperado)"

# Dentro de las VMs, asigna IPs estáticas de la misma subred y prueba conectividad entre ellas
```

---

## Gestión y eliminación

- Listar redes: `virsh net-list --all`
- Mostrar XML: `virsh net-dumpxml NOMBRE`
- Parar red: `virsh net-destroy NOMBRE`
- Quitar autostart: `virsh net-autostart NOMBRE --disable`
- Eliminar (no debe estar activa): `virsh net-undefine NOMBRE`

Archivos persistentes en `/etc/libvirt/qemu/networks/` (y `.../autostart/`).

---

## Problemas comunes y consejos

- Conflictos de subred: usa rangos que no colisionen con tu LAN (p.ej., 192.168.101.0/24, 192.168.102.0/24, 192.168.103.0/24).
- Firewall: libvirt gestiona NAT/iptables/nft por defecto, pero si tienes reglas estrictas, revisa cadenas de `libvirt`.
- Permisos: añade tu usuario al grupo `libvirt` si no puedes usar `virsh` sin root.
- Persistencia: usa `net-define` y `net-autostart` para que la red sobreviva reinicios.

---

## Referencias

- [curso_virtualizacion_linux — GitHub](https://github.com/josedom24/curso_virtualizacion_linux)
- [Libvirt: Virtual networking overview](https://libvirt.org/network.html)
- [Libvirt: Network XML format](https://libvirt.org/formatnetwork.html)
- [Libvirt: Domain XML (interfaces, tipos de NIC)](https://libvirt.org/formatdomain.html)
- [Libvirt Wiki: Guest networking (macvtap, bridge)](https://wiki.libvirt.org/page/Guest_Networking)
