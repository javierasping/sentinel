#!/bin/bash
# Script de ejemplo para preparar el host KVM/libvirt para el laboratorio
set -euo pipefail

sudo apt update
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients virtinst vagrant
sudo systemctl enable --now libvirtd
# Crear redes (si los XML existen)
if [ -f mgmt-net.xml ]; then
  sudo virsh net-define mgmt-net.xml || true
  sudo virsh net-autostart mgmt-net || true
  sudo virsh net-start mgmt-net || true
fi
if [ -f provider-net.xml ]; then
  sudo virsh net-define provider-net.xml || true
  sudo virsh net-autostart provider-net || true
  sudo virsh net-start provider-net || true
fi

echo "Host preparado para Vagrant + libvirt. Añade tu usuario al grupo libvirt si es necesario."
