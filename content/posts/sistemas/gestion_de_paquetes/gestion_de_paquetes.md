---
title: "Gestion de paquetes"
date: 2023-11-29T10:00:00+00:00
description: Gestion de paquetes
tags: [Sistemas,ISO,ASO,Linux]
hero: images/sistemas/gestion_de_paquetes/gestion_de_paquetes.jpg
---
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GVDYVWJLRH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-GVDYVWJLRH');
</script>


## Indica los pasos a seguir para modificar la configuración de red de DHCP a estática

Para configurar la interfaz ens1 con una dirección IP estática (por ejemplo, 192.168.122.10), debes modificar el archivo /etc/sysconfig/network-scripts/ifcfg-ens1 :

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.001.jpeg)

Para aplicar la configuración reiniciamos el Network Manager :

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.002.jpeg)

## Actualiza el sistema a las versiones más recientes de los paquetes instalados

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.003.png)

## Instala el repositorio adicional EPEL.

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.004.jpeg)

## Instala el paquete bash-completion.

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.005.png)

Instala el paquete que proporciona el programa dig, explicando los pasos que has dado para encontrarlo

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.006.png)

Instalamos el paquete :

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.007.png)

## Explica qué comando utilizarías para ver la información del paquete kernel instalado

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.008.jpeg)

## Instala el repositorio adicional "elrepo". Importamos la clave publica del repositorio :

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.009.png)

Instalamos el repositorio :

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.010.jpeg)

## Busca las versiones disponibles para instalar del núcleo Linux e instala la más nueva Listamos los kernel mas recientes :

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.011.jpeg)

Lo instalamos:

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.012.jpeg)

## Muestra el contenido del paquete del último núcleo instalado

![](../img/Aspose.Words.0f9af8ba-710a-47db-ba6b-edb2ea8012f0.013.png)

