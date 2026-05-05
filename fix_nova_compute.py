
import os

file_path = "/home/javiercruces/github/sentinel/content/posts/openstack/curso-openstack/instalacion-manual/10-instalacion-nova-nodo-computo/10-instalacion-nova-nodo-computo.md"

with open(file_//home/javiercruces/github/sentinel/content/posts/openstack/curso-openstack/instalacion-manual/10-instalacion-nova-nodo-computo/10-instalacion-nova-nodo-computo.md, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ("En esta página configuro un nodo de cómputo (por ejemplo `compute01`) para que pueda ejecutar instancias con Nova. Uso QEMU/KVM cuando el hardware lo soporta; si no, dejo configurado QEMU puro.", 
     "En esta guía, configuraremos un nodo de cómputo (por ejemplo, `compute01`) para que sea capaz de ejecutar instancias mediante Nova. Utilizaremos QEMU/KVM siempre que el hardware lo permita; en caso contrario, dejaremos configurado QEMU puro."),
    ("Antes de empezar, asegúrate de:", "Antes de comenzar, asegúrate de cumplir los siguientes requisitos:"),
    ("Haber añadido el nombre e IP del controlador en `/etc/hosts` del nodo de cómputo.", "Haber añadido el nombre y la IP del nodo controlador al archivo `/etc/hosts` del nodo de cómputo."),
    ("Disponer de las credenciales del servicio (`admin-openrc`) y de acceso al servidor de bases de datos.", "Disponer de las credenciales administrativas (`admin-openrc`) y acceso al servidor de bases de datos."),
    ("Instalo el paquete principal del servicio de cómputo en el nodo:", "Instalaremos el paquete principal del servicio de cómputo en el nodo:"),
    ("Edito el fichero `/etc/nova/nova.conf` y apunto las cadenas de conexión a las bases de datos del controlador:", "Editaremos el archivo `/etc/nova/nova.conf` para definir las cadenas de conexión a las bases de datos situadas en el controlador:"),
    ("Configuro la conexión con RabbitMQ (reemplaza `RABBIT_PASS`) y otras opciones por defecto:", "Configuraremos la conexión con RabbitMQ (sustituye `RABBIT_PASS` por tu contraseña) y otras opciones predeterminadas:"),
    ("Configuro las credenciales del servicio (usuario `nova`) para que el nodo pueda autenticarse contra Keystone:", "Configuraremos las credenciales del servicio (usuario `nova`) para que el nodo pueda autenticarse contra Keystone:"),
    ("Indico la IP de gestión del nodo en `my_ip` (sustituye `IP_GESTION_NODO_COMPUTO`, en mi ejemplo `10.0.0.3`):", "Definiremos la IP de gestión del nodo en el parámetro `my_ip` (sustituye `IP_GESTION_NODO_COMPUTO` por la IP correspondiente; en mi ejemplo es `10.0.0.3`):"),
    ("Configuro el apartado VNC para que el proxy use la IP del controlador y el servidor escuche en todas las interfaces:", "Configuraremos el apartado VNC para que el proxy utilice la IP del controlador y el servidor escuche en todas las interfaces:"),
    ("Apunto Nova a Glance y configuro el lock_path:", "Conectaremos Nova con Glance y definiremos la ruta de bloqueo (`lock_path`):"),
    ("En la sección de autenticación con Keystone configuro el token middleware (reemplaza `<NOVA_PASSWORD>` si procede):", "En la sección de autenticación con Keystone, configuraremos el token middleware (sustituye `<NOVA_PASSWORD>` si es necesario):"),
    ("Compruebo si el nodo soporta virtualización por hardware y, si no, fuerzo QEMU:", "Verificaremos si el nodo soporta virtualización por hardware y, en caso negativo, forzaremos el uso de QEMU:"),
    ("Si el resultado es 0, establezco `virt_type=qemu` en `/etc/nova/nova-compute.conf`:", "Si el resultado es 0, estableceremos `virt_type=qemu` en el archivo `/etc/nova/nova-compute.conf`:"),
    ("Reinicio el servicio `nova-compute` para aplicar la configuración:", "Reiniciaremos el servicio `nova-compute` para aplicar la nueva configuración:"),
    ("Cargo las credenciales de administrador en el controlador y busco hosts sin mapear:", "Cargaremos las credenciales de administrador en el nodo controlador y buscaremos los hosts que no hayan sido mapeados:"),
    ("Compruebo si nuestro controlador detecta nodos de cómputo pendientes de ser añadidos:", "Verificaremos si el controlador detecta nodos de cómputo pendientes de añadir:"),
    ("Verifico que el nodo aparece como servicio `nova-compute`:", "Verificaremos que el nodo aparezca correctamente como el servicio `nova-compute`:"),
    ("Nota: cada vez que añadas un nuevo nodo debes ejecutar `discover_hosts` en el controlador, o habilitar la detección periódica añadiendo en `/etc/nova/nova.conf`:", "Nota: cada vez que añadas un nuevo nodo, deberás ejecutar `discover_hosts` en el controlador o, alternativamente, habilitar la detección periódica añadiendo lo siguiente en `/etc/nova/nova.conf`:"),
]

for old, new in replacements:
    content = content.replace(old, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
