---

title: "Cómo validar la instalación del host KVM"
date: 2025-10-13T10:00:00+00:00
description: Aprende a validar que tu host Ubuntu/Debian cumple con los requisitos para ejecutar KVM y gestionar máquinas virtuales de manera eficiente.
tags: [Virtualizacion,Linux,KVM,VM,Hypervisor,Ubuntu,Debian]
hero: images/virtualizacion-kvm-linux/instalacion/validacion.png
weight: 2
--------------------------------------------------------------------------

# Validación del host para KVM en Ubuntu/Debian

Antes de crear y ejecutar máquinas virtuales con **KVM**, es fundamental validar que el host cumpla con los **requisitos de hardware y software** necesarios para garantizar un rendimiento óptimo. Esta guía describe cómo verificar las capacidades del sistema utilizando herramientas como `virt-host-validate` y `virsh`.

## 1. Validando soporte de virtualización en la CPU

KVM requiere procesadores con **extensiones de virtualización**:

* Intel: VT-x
* AMD: AMD-V

Para verificar si tu CPU es compatible, ejecuta:

```bash
grep --color -Ew 'svm|vmx|lm' /proc/cpuinfo
```

* `vmx` → CPU Intel con VT-x
* `svm` → CPU AMD con AMD-V
* `lm` → soporte de 64 bits

Si tu CPU no cuenta con estas extensiones, solo será posible ejecutar emulación de CPU, lo que reduce significativamente el rendimiento.

## 2. Comprobando módulos del kernel

Los módulos de kernel necesarios para virtualización deben estar cargados:

```bash
lsmod | grep kvm
```

* Sistemas Intel: `kvm_intel`
* Sistemas AMD: `kvm_amd`

Si no aparecen, cárgalos manualmente:

```bash
sudo modprobe kvm
sudo modprobe kvm_intel  # Para Intel
sudo modprobe kvm_amd    # Para AMD
```

## 3. Validando el host con virt-host-validate

La herramienta `virt-host-validate` ejecuta una serie de pruebas para asegurar que el sistema está preparado para KVM:

```bash
sudo virt-host-validate
```

Un resultado exitoso mostrará `PASS` en todas las pruebas, incluyendo:

* Virtualización de hardware
* Existencia de dispositivos `/dev/kvm`, `/dev/vhost-net` y `/dev/net/tun`
* Soporte de controladores de CPU y memoria

Si alguna prueba falla, se indicará con `FAIL`, lo que puede afectar el rendimiento de las VMs.

### Ejemplo de salida exitosa

```
QEMU: Checking for hardware virtualization              : PASS
QEMU: Checking if device /dev/vhost-net exists          : PASS
QEMU: Checking if device /dev/net/tun exists            : PASS
QEMU: Checking for cgroup 'memory' controller support   : PASS
QEMU: Checking for cgroup 'cpu' controller support      : PASS
```

### Ejemplo de fallo por CPU sin VT-x/AMD-V

```
QEMU: Checking for hardware virtualization              : FAIL (Only emulated CPUs are available, performance will be significantly limited)
```

## 4. Validando información del host con virsh

`virsh` permite consultar detalles del host y capacidades del hypervisor:

```bash
virsh nodeinfo
```

Salida de ejemplo:

```yaml
CPU model:           x86_64
CPU(s):              24
CPU frequency:       4252 MHz
CPU socket(s):       1
Core(s) per socket:  12
Thread(s) per core:  2
NUMA cell(s):        1
Memory size:         62324512 KiB
```

Para ver las capacidades máximas de las VMs:

```bash
virsh domcapabilities | grep -i max
```

Salida de ejemplo:

```xml
  <vcpu max='255'/>
    <mode name='maximum' supported='yes'>
      <enum name='maximumMigratable'>
      <maxphysaddr mode='passthrough' limit='48'/>
```

También se pueden listar los tipos de dispositivos soportados por el hypervisor:

```bash
virsh domcapabilities | grep diskDevice -A 5
```

```xml
      <enum name='diskDevice'>
        <value>disk</value>
        <value>cdrom</value>
        <value>floppy</value>
        <value>lun</value>
      </enum>
```

`virsh` es una herramienta de línea de comandos para la gestión de máquinas virtuales y del hypervisor. Permite administrar VMs, monitorear recursos, gestionar almacenamiento, snapshots y redes virtuales.

## Referencias

- [curso_virtualizacion_linux — GitHub](https://github.com/josedom24/curso_virtualizacion_linux)
* [KVM-virsh - Ubuntu Help](https://help.ubuntu.com/community/KVM/Virsh)
* [Managing guests using virsh - RedHat Virtualization Guide](https://access.redhat.com/documentation/en-us/red_hat_virtualization)
* [virsh - libvirt guide](https://libvirt.org/virshcmdref.html)
