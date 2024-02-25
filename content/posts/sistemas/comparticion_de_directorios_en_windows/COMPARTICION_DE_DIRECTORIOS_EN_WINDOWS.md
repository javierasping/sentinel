---
title: "Compartir recursos en red en Windows Server"
date: 2023-09-08T10:00:00+00:00
description: Aprende cómo compartir recursos en red en Windows Server
tags: [Windows,Sistemas,ISO,ASO]
hero: images/sistemas/compartir_directorios_win/portada.jpg
---

En el entorno empresarial, la capacidad de compartir recursos en red es esencial para la colaboración y la eficiencia operativa. En este artículo, exploraremos cómo compartir directorios en un entorno Windows Server, abordando los métodos tanto a través de la interfaz gráfica como mediante cmd y PowerShell.

## Desde la interfaz gráfica

Podemos compartir un directorio de nuestro servidor , accediendo a las propiedades del mismo . Una vez aquí pulsamos sobre el menú compartir :

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.001.png)

Ahora le daremos permisos a los usuarios que deseemos que tengan acceso a este :

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.002.jpeg)

Una vez compartido nos mostrara la ruta que tendremos que poner para acceder a este recurso , que podemos modificarla a nuestro gusto en uso compartido avanzado :

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.003.png)

Desde un cliente podemos ver los recursos que esta compartiendo nuestro servidor usando net view :

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.004.png)

Podemos mapear la unidad de red desde la linea de comandos usando net use  :

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.005.png)

Vamos a crear un directorio y comprobar que se ha creado :

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.006.png)

Vemos que en el servidor se ha creado :

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.007.png)

También podemos hacer esto desde la administración de usuarios y grupos de active directory :

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.008.png)

## Compartir recursos desde cmd

Ahora vamos a usar net share para compartir un recurso en red a traves de la linea de comandos :

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.009.png)

Si desde otro cliente vemos los recursos que comparte el server core , lo veremos :

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.010.png)

Si queremos cambiar los permisos de un recurso compartido podemos usar los comandos cacls y icacls . También tenemos la posibilidad de hacerlo usando la interfaz gráfica con las RSAT.

## Comandos powershell

Crearemos el recurso compartido 

```ps
New-SmbShare -Name JCD\_comp -Path "C:\compartir\" -FullAccess "Administrador"
```

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.011.png)

Si queremos añadir permisos específicos a un grupo a la hora de crear el recurso compartido seria : 

```ps
New-SmbShare -Name <Nombre-de-la-carpeta> -Path <Ruta-de-la-carpeta> -ReadAccess "<Grupo-o-usuario-que-tiene-acceso-de-lectura>" -FullAccess "<Grupo-o-usuario-que-tiene- acceso-total>"
```

Si después de esto queremos añadirle o quitarle permisos a algún usuario o grupo al directorio samba compartido :

```ps
Set-SmbPathAcl -Path "C:\compartir" -AceType Allow -AccessType Write -AccountName UsuariosCompartidos
```

Si por el contrario queremos eliminar permisos al usuario o grupo :

```ps
Remove-SmbPathAcl -Path "C:\compartir" -AceType Allow -AccessType Write -AccountName UsuariosCompartidos
```

Para montar este directorio compartido en otro host Windows :

```ps
New-PSDrive -Name J -PSProvider FileSystem -Root [\\172.22.9.143\JCD_comp](file://172.22.9.143/JCD_comp)
```

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.012.png)

Además podemos listar para ver si se ha montado correctamente :

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.013.jpeg)

Listaremos el contenido del mismo para ver si tenemos acceso a el :

![](../img/Aspose.Words.2ac587b0-02fe-41e0-b2ab-82492960a464.014.png)

