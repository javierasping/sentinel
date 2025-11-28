---
title: "01 - ¿Qué es OpenStack?"
date: 2025-11-23T12:00:00+00:00
description: "Explicación sencilla de qué es OpenStack, sus componentes y cuándo se utiliza."
tags: [openstack,introduccion]
hero: ""
weight: 1
---

OpenStack es un proyecto de software libre que permite crear y gestionar nubes privadas, públicas o híbridas, ofreciendo control total sobre la infraestructura a través de APIs abiertas. No es un producto de una sola empresa, sino un ecosistema abierto mantenido por una comunidad global bajo la licencia Apache. Fundado en 2010 por la NASA y Rackspace, ha recibido contribuciones de organizaciones como AT&T, Red Hat, Canonical, Intel, IBM y Huawei.

La computación en la nube consiste en acceder a programas y datos de manera descentralizada, sin depender de un único servidor físico. La información se distribuye en distintos lugares, a menudo geográficamente separados, y se accede a ella mediante la red. Este modelo exige infraestructuras que garanticen disponibilidad, rendimiento y seguridad. Los datos deben estar protegidos frente a accesos no autorizados y frente a pérdidas accidentales, mientras los recursos se utilizan de manera eficiente.

OpenStack proporciona APIs homogéneas para controlar cómputo, red y almacenamiento, abstrae la complejidad del hardware subyacente y permite que usuarios y aplicaciones gestionen recursos de forma autónoma, sin depender de aprobaciones humanas. Aunque se ejecuta sobre Linux y utiliza hipervisores como KVM o XEN, su verdadera fortaleza está en la interoperabilidad, la escalabilidad y la capacidad de integrarse con otras capas de la nube, como contenedores, plataformas serverless o sistemas PaaS.

## ¿Por qué usar la nube y OpenStack?

La nube permite acceder a potencia de cómputo, almacenamiento y servicios sin depender del hardware de los dispositivos locales. Esto significa que no hace falta invertir grandes sumas en servidores propios, y que los recursos se pueden ajustar según las necesidades reales, pagando únicamente por lo que se utiliza. Esta escalabilidad flexible convierte a la nube en una opción eficiente tanto para pequeñas startups como para grandes organizaciones.

OpenStack aporta valor en este contexto al ofrecer una plataforma libre y extensible para construir nubes privadas, públicas o híbridas. A diferencia de soluciones comerciales cerradas, OpenStack permite a las organizaciones mantener el control total de su infraestructura, desde la gestión de servidores y almacenamiento hasta la red y la seguridad. Su arquitectura abierta facilita la integración con otras capas de la nube, como contenedores, plataformas serverless o entornos PaaS, haciendo posible que aplicaciones modernas aprovechen al máximo los recursos disponibles.

Además, OpenStack incorpora mecanismos que aumentan la seguridad y la resiliencia. Los datos se pueden replicar y los recursos se aíslan entre distintos usuarios o aplicaciones, reduciendo riesgos de accesos no autorizados o pérdidas accidentales. Todo esto convierte a OpenStack en una opción atractiva para quienes buscan autonomía, flexibilidad y fiabilidad a la hora de desplegar y gestionar su propia nube.

## Componentes principales de OpenStack

OpenStack es un conjunto de servicios que, combinados, permiten construir y gestionar una nube completa y flexible. En el núcleo de la plataforma se encuentra Nova, el servicio de cómputo, que gestiona la ejecución de máquinas virtuales y se encarga de la abstracción del hardware mediante virtualización. Nova es compatible con hipervisores populares como KVM, XEN y VMware ESXi, lo que permite a las organizaciones elegir la tecnología que mejor se adapte a sus necesidades.

La gestión de usuarios, proyectos y permisos recae sobre Keystone, que actúa como el servicio de identidad, autenticación y autorización de la nube. Glance se encarga de las imágenes de disco, funcionando como un repositorio donde almacenar, versionar y recuperar plantillas de máquinas virtuales para su despliegue.

La red en OpenStack es proporcionada por Neutron, que permite crear redes virtuales, subredes, asignar IPs, configurar VLANs y VPNs, y aplicar servicios de seguridad como firewalls y NAT. Para el almacenamiento en bloque, Cinder ofrece volúmenes virtuales que se pueden conectar a las instancias, con soporte para snapshots y la integración con distintos backends físicos como Ceph o GlusterFS. Complementando esto, Swift proporciona almacenamiento de objetos distribuido, pensado para replicación masiva y alta durabilidad de los datos.

Para la interacción y administración, Horizon ofrece un panel web desde el cual los operadores y usuarios pueden gestionar recursos, supervisar la infraestructura y lanzar instancias sin necesidad de recurrir a la línea de comandos.

Todos estos servicios están diseñados para trabajar de forma coordinada. Nova utiliza imágenes de Glance para crear instancias, Cinder suministra volúmenes que pueden montarse en esas máquinas, Neutron conecta los nodos entre sí y con el exterior, Keystone controla los accesos y Swift permite servir datos de manera distribuida y confiable. Horizon proporciona una visión completa de todo esto, facilitando la administración de la nube desde un navegador.

Además de estos servicios principales, OpenStack incluye muchos otros componentes especializados para ampliar funcionalidades, como:

- **Zun:** gestión de contenedores.
- **Ironic:** aprovisionamiento de hardware bare-metal.
- **Cyborg:** gestión de aceleradores y dispositivos especializados.
- **Manila:** sistemas de archivos compartidos.
- **Octavia:** balanceadores de carga.
- **Designate:** servicio de DNS.
- **Heat y Mistral:** orquestación y workflows.
- **Trove:** bases de datos como servicio.
- **Magnum:** gestión de clusters de contenedores.
- **Barbican:** gestión de claves y secretos.
- **Masakari:** alta disponibilidad de instancias.

Estos servicios trabajan coordinadamente con los principales, formando un ecosistema modular y extensible que se adapta a necesidades muy diversas.

En su documentation oficial puedes encontrar una lista completa de todos los [componentes de openstack](https://www.openstack.org/software/project-navigator/openstack-components#openstack-services).

## La visión de OpenStack

OpenStack no es solo un conjunto de servicios de nube, sino una visión estratégica de cómo deben funcionar las nubes modernas. Se basa en principios de:

- **Autoservicio:** usuarios y aplicaciones gestionan recursos directamente a través de APIs.
- **Interoperabilidad:** aplicaciones se despliegan entre distintas nubes sin cambios significativos.
- **Abstracción de hardware:** gestión de VMs, GPUs, FPGAs, balanceadores de carga y almacenamiento avanzado.
- **Escalabilidad y resiliencia:** recursos compartidos eficientemente con alta disponibilidad y durabilidad.
- **Integración con otras capas de la nube:** soporte nativo para contenedores, PaaS y serverless.

Esta visión hace de OpenStack un ecosistema modular, flexible y totalmente abierto, donde cada servicio contribuye a construir nubes autónomas, fiables y adaptables.