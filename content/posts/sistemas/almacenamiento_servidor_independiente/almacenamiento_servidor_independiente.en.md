---
title: "Storage Spaces on Windows Server"
date: 2023-09-08T10:00:00+00:00
Description: Learn how to use Storage Spaces on Windows Server
tags: [Linux,Sistemas,ISO,ASO]
hero: images/sistemas/storage_spaces/portada.png
---


Storage Spaces is a software-defined storage feature in the Windows Server operating system that allows system administrators to combine several physical disks in a single logical storage space called "storage pool." This storage pool can be used to create virtual storage spaces called "storage spaces" that offer various redundancy functions and advanced storage management capabilities.

### Storage groups

The following Windows PowerShell cmdlets perform the same function as the previous procedure. Write each cmdlet in a single line, although here you can appear with line jumps between several lines here due to format restrictions.

The following example shows which physical disks are available in the primary group.

```ps
Get-StoragePool -IsPrimordial $true | Get-PhysicalDisk -CanPool $True
```

![](../img/Aspose.Words.2ccae554-4864-4939-8439-3bfaf64ead92.001.png)

The following example creates a new storage group called StoragePool1 that uses all available disks:

```ps
New-StoragePool –FriendlyName StoragePool1 –StorageSubsystemFriendlyName "Windows Storage\*" –PhysicalDisks (Get-PhysicalDisk –CanPool $True) 
```

![](../img/Aspose.Words.2ccae554-4864-4939-8439-3bfaf64ead92.002.png)

By default the type of supply is mirror.

If we need to add more disks:

```ps
Add-PhysicalDisk -StoragePoolFriendlyName StoragePool1 -PhysicalDisks (Get-PhysicalDisk  - CanPool $True)
```

### Create a virtual disk

Let's create a virtual disk:

```ps
New-VirtualDisk –StoragePoolFriendlyName StoragePool1 –FriendlyName VirtualDisk1 –Size (8GB)
```

![](../img/Aspose.Words.2ccae554-4864-4939-8439-3bfaf64ead92.003.jpeg)

It will automatically create a volume for us and mount it into a available letter:

![](../img/Aspose.Words.2ccae554-4864-4939-8439-3bfaf64ead92.004.jpeg)

We can interact with and save information:

![](../img/Aspose.Words.2ccae554-4864-4939-8439-3bfaf64ead92.005.png)

We see that this is the "equivalent" to LVM on Windows. We see that there are similarities not only in the structure when creating it, but also that they refer in the official documentation to RAID 5 and RAID 6:

![](../img/Aspose.Words.2ccae554-4864-4939-8439-3bfaf64ead92.006.png)

The way to store the data in either stripes or by saving the full space, as in Linux:

![](../img/Aspose.Words.2ccae554-4864-4939-8439-3bfaf64ead92.007.jpeg)

## Bibliography

- [Official documentation] (https: / / learn.microsoft.com / es-en / windows-server / storage / storage-spaces / deploy-standalone-storage-spaces)

