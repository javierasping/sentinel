
# ¿Qué es OpenStack?

OpenStack es una plataforma de código abierto para construir nubes públicas y privadas. Se le suele llamar "el sistema operativo de la nube" porque proporciona
abstracciones y APIs estandarizadas para gestionar recursos de cómputo, almacenamiento y red, permitiendo aprovisionar y administrar infraestructura como servicio (IaaS)
de forma programática.

## Principales ideas

- OpenStack está formado por múltiples proyectos independientes que, combinados, ofrecen las funcionalidades de una nube: lanzamiento de máquinas virtuales, gestión de
	imágenes y volúmenes, redes virtuales, identidades y paneles de usuario.
- Los usuarios interactúan con OpenStack mediante APIs REST, la interfaz de línea de comandos o el panel Horizon.
- OpenStack abstrae los detalles del hardware y los backends (hipervisores, almacenamiento, soluciones de red) para ofrecer una interfaz uniforme.

## Componentes clave

Aunque OpenStack incluye decenas de proyectos, seis de ellos suelen considerarse el núcleo de la plataforma:

- Keystone: servicio de identidad y autenticación (gestión de usuarios, roles y tokens).
- Nova: servicio de cómputo, responsable del ciclo de vida de las instancias.
- Neutron: servicio de red, para redes virtuales, subredes, routers y servicios de red (firewalls, balanceadores).
- Cinder: servicio de almacenamiento en bloque (volúmenes persistentes).
- Glance: servicio de imágenes (almacena y sirve imágenes de sistema operativo).
- Swift (u otros backends de objetos como Ceph RGW): servicio de almacenamiento de objetos.

Además de estos, existen proyectos opcionales (Heat, Mistral, Trove, Barbican, Sahara, etc.) que añaden capacidades como orquestación, bases de datos como servicio, gestión
de claves y procesamiento de datos.

## Arquitectura y modelos de despliegue

OpenStack no es monolítico: cada servicio puede desplegarse en hosts separados o agrupados, según las necesidades:

- AIO (All-In-One): todos los servicios en un único host. Ideal para pruebas y aprendizaje.
- Multinodo: separación de responsabilidades entre nodos de control (control plane) y nodos de cómputo/almacenamiento (data plane).
- Despliegues a escala: múltiples réplicas de servicios críticos (bases de datos, colas, controladores) detrás de balanceadores para alta disponibilidad.

El diseño de red suele incluir al menos una red de gestión (privada) y una red pública/proveedor para el tráfico de instancias. Cada servicio expone su API en una IP y puerto
concretos (p. ej. Cinder suele usar el puerto 8776).

## APIs y modelo de consumo

OpenStack ofrece APIs REST que aceptan y devuelven JSON. Las operaciones CRUD sobre recursos (instancias, volúmenes, redes) se realizan mediante llamadas HTTP (POST, GET,
PUT/PATCH, DELETE) y están protegidas por Keystone mediante tokens y políticas RBAC.

Existen clientes y SDKs en varios lenguajes (python-openstacksdk, openstacksdk) que facilitan la interacción desde scripts y herramientas de automatización (Terraform,
Ansible, etc.).

Ejemplo simplificado: para crear un volumen, un cliente envía un POST al endpoint de Cinder (p. ej. http://controlador:8776/v3/volumes) con un JSON que describe el tamaño y
los metadatos; la API responde con la representación JSON del volumen creado y su identificador.

## Comunidad vs. soluciones comerciales

OpenStack puede obtenerse directamente de la comunidad o a través de proveedores comerciales:

- Comunidad: lanzamientos regulares, amplia documentación y mayor rapidez para acceder a nuevas versiones. Requiere más trabajo de integración y operación.
- Proveedores: versiones empaquetadas, soporte comercial y herramientas de despliegue integradas; suelen facilitar la adopción en producción a costa de licencia/soporte y
	posibles limitaciones en componentes incluidos.

La elección depende de los requisitos de soporte, control de versiones y recursos del equipo operativo.

## Casos de uso y ventajas

- Flexibilidad: soporte para varios hipervisores (KVM, Xen, VMware) y backends de almacenamiento (Ceph, SANs, LVM).
- Programabilidad: APIs uniformes y compatibilidad con infraestructuras como código.
- Escalabilidad: desde un AIO hasta despliegues repartidos por centros de datos con balanceo y replicación.
- Portabilidad: las abstracciones permiten cambiar backends sin afectar a los usuarios.

OpenStack se utiliza en nubes privadas corporativas, entornos de IaaS para desarrollo y pruebas, y como plataforma para PaaS y cargas de datos masivas.

## Retos y consideraciones

- Complejidad operacional: OpenStack agrupa muchos componentes (20+), cuya instalación y orden de despliegue son críticos.
- Integración de backends: almacenamiento, redes y soluciones de hypervisor requieren diseño y pruebas.
- Requisitos de infraestructura: separación clara de redes (mgmt, storage, public) y planificación de alta disponibilidad.
- Curva de aprendizaje: entender Keystone, Neutron (VLAN, VXLAN), políticas RBAC y dependencias entre servicios.

Operaciones como la configuración de LVM para Cinder pueden ser destructivas si no se realizan con cuidado; siempre documente y haga backups.


## Infraestructura y plano de control

Este artículo aborda aspectos clave de la infraestructura necesaria para desplegar y operar OpenStack, con enfoque en el plano de control, el plano de usuario, la red física y el backend de almacenamiento.

OpenStack no funciona de forma aislada: es una colección de APIs que requieren una infraestructura sólida. Muchos servicios (por ejemplo, Keystone) son aplicaciones Python que se ejecutan detrás de un servidor HTTP en Linux —Apache y Nginx son opciones habituales—.

La mayoría de los servicios persisten datos en bases de datos SQL. Es habitual disponer de uno o varios motores (MySQL/MariaDB o PostgreSQL); pueden centralizarse o distribuirse según requisitos de seguridad, rendimiento o administración. Para la comunicación asíncrona entre componentes se emplean servidores de mensajería (RabbitMQ es el más común, aunque existen alternativas). También es frecuente utilizar caches en memoria (por ejemplo Memcached) para mejorar rendimiento.

### Elementos del plano de control

El plano de control concentra los componentes que gestionan y orquestan la nube: bases de datos, sistema de colas, proxies, balanceadores y los endpoints API. En despliegues con muchos servicios (20+), aparecerá una gran cantidad de endpoints en el plano de control.

Para mejorar la seguridad y la escalabilidad, algunos servicios (como agentes de cómputo o de red) dividen sus funciones entre el plano de usuario y el plano de control; los agentes en los nodos de cómputo no acceden directamente a las bases de datos de servicio, sino que lo hacen a través de los componentes "conductor" ejecutados en el plano de control.

### Alta disponibilidad del plano de control

Garantizar disponibilidad es crítico. Para ello es habitual:

- Ejecutar el motor de base de datos en un clúster (por ejemplo Galera Cluster para MySQL/MariaDB) para replicación síncrona y tolerancia a fallos.
- Colocar un proxy o balanceador delante de las APIs para distribuir carga y detectar fallos. HAProxy es la opción software más extendida; en entornos maduros puede usarse hardware especializado.
- Gestionar la orquestación y la conmutación por error de servicios con soluciones como Pacemaker/Corosync cuando los servicios requieren gestión avanzada de recursos y dependencias.

Muchos servicios se ejecutan como unidades gestionadas por systemd en cada nodo; combinando systemd con HAProxy y, cuando procede, Pacemaker, se consigue un nivel de resistencia adecuado. Antes de desplegar Pacemaker conviene revisar la guía de alta disponibilidad de OpenStack y adaptarla a la versión concreta que vaya a usar.

## Planificación del pool de recursos informáticos (compute)

OpenStack ofrece tres grandes abstracciones de computación: instancias (máquinas virtuales), bare-metal y contenedores. La elección del hipervisor es una decisión clave: KVM es la opción libre más habitual, pero OpenStack soporta también Xen, ESXi, y otros. Si ya dispone de cargas en VMware, puede optar por integrar ESXi para evitar convertir imágenes.

Puede agrupar hosts con diferentes hipervisores en diferentes pools y usar zonas de disponibilidad y agregados de host para controlar la colocación. Esto permite, por ejemplo, ofrecer hosts con SSD, o con GPU, o con un hipervisor concreto.

Los sabores (flavors) definen recursos asignados a cada instancia (vCPU, memoria, discos). El overcommit de CPU/RAM es configurable: valores típicos de CPU overcommit pueden ser 16:1, aunque entornos exigentes usan 1:1 para garantizar QoS.

## Red física y virtualización de red

La red subyacente (underlay) es fundamental. Debe diseñarse para aislar tráfico (gestión, almacenamiento, datos de instancia, proveedor) y garantizar redundancia (NICs enlazadas, switches redundantes). Además hay que valorar soporte para aceleración (SR-IOV), offload o hardware que facilite VxLAN/Geneve.

En el plano virtual (overlay), es común usar túneles VXLAN o VLANs L2 para segmentar tenant networks. Para conmutación virtual, Open vSwitch (OVS) es la opción más extendida; en despliegues con requerimientos especiales se pueden integrar controladores SDN o soluciones comerciales (NSX, Cisco ACI…).

## Backend de almacenamiento

El almacenamiento puede ser hardware (matrices SAN) o software (Ceph, LVM). La elección suele depender de lo que ya exista en el CPD y de requisitos de rendimiento, disponibilidad y coste. Es importante diseñar las rutas de datos entre dispositivos de almacenamiento y nodos de cómputo.


En este artículo se emplean LVM y Ceph como ejemplos de backends para Cinder y otros servicios de almacenamiento. La planificación debe incluir rendimiento esperado, replicación, redes dedicadas y dimensionamiento (capacity planning).

## Telemetría y servicios adicionales

No olvide planificar servicios complementarios como telemetría, logging y alarma. Recolectar métricas y almacenar telemetría aporta visibilidad, pero supone una carga adicional en red y almacenamiento; hay que dimensionar recursos para procesar y almacenar esos datos.

Si planea añadir servicios como Trove (DBaaS), Sahara (procesamiento de datos) o Magnum (contenedores), valore sus dependencias y la carga adicional sobre red y almacenamiento.

---


Se recomienda revisar las guías oficiales de diseño de arquitectura y alta disponibilidad de OpenStack; contienen recomendaciones prácticas y ejemplos que conviene adaptar al contexto de cada despliegue.

## Recursos

- Documentación oficial de OpenStack: https://docs.openstack.org/
- OpenStack-Ansible: https://docs.openstack.org/project-deploy-guide/openstack-ansible/latest/
- SDKs y clientes: python-openstacksdk

---
