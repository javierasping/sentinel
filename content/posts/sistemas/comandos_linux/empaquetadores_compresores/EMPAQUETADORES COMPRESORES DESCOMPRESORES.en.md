---
title: "Packaging and compressors in Linux"
date: 2023-09-08T10:00:00+00:00
description: Learn how to treat compressed and packaged files
tags: [Linux,Sistemas,ISO,ASO]
hero: images/sistemas/empaquetadores/portada.jpg
---


Packers and compressors are key elements in the management of files and data in the computer field. The packers allow to group several files in a single container, facilitating their handling and transport. On the other hand, compressors apply techniques to reduce file size, contributing to storage space savings and expediting data transfer. These tools play a crucial role in resource optimization and operational efficiency by more effectively organizing, distributing and supporting information.

## TAR

It is a file packer that as its own name indicates uses the .tar format, it is basically used to store files and directories in the same file.

The name of the package is tar.

### Create a .tar file

You can create compressions. An example of this type of file is:

```bash
tar -cvf sampleArchive.tar /home/sampleArchive
```

Here / home / sampleArchive is the directory that needs to be compressed creating ampleArchive.tar. This command uses the -cvf options that mean:

- c - create a new .tar file
- v - shows a detailed description of the progress of the compression
- f - file name

### Create a .tar.gz file

If you want better compression, you can also use .tar.gz. An example of this is:

```bash
tar -cvzf sampleArchive.tar.gz /home/sampleArchive
```

The additional option * * z * * represents gzip compression. Alternatively, you can create a .tgz file that is similar to tar.gz. We show you an example of the latter:

```bash
tar -cvzf sampleArchive.tgz /home/sampleArchive 
```

### Create a .tar.bz2 file

The .bz2 file provides more compression compared to gzip. However, this alternative will take more time to compress and decompress. To use it, you must use the -j option. An example of how the operation would look is as follows:

```bash
tar -cvjf sampleArchive.tar.bz2 /home/sampleArchive
```

This operation is similar to .tar.tbz or .tar.tb2. I'll show you an example below:

```bash
tar -cvjf sampleArchive.tar.tbz /home/sampleArchive tar -cvjf sampleArchive.tar.tb2 /home/sampleArchive
```

### How to decompress .tar files

The Linux Tar command can also be used to extract a file. The following command will remove the files in the current directory:

```bash
tar -xvf sampleArchive.tar
```

If you want to extract your files to a different directory, you can use the -C option. We show you an example of this below:

```bash
tar -xvf sampleArchive.tar -C /home/ExtractedFiles/
```
You can use a similar command to uncompress .tar.gz files, as shown below:

```bash
tar -xvf sampleArchive.tar.gz

tar -xvf sampleArchive.tar.gz -C /home/ExtractedFiles/
```

.tar.bz2 or .tar.tbz or .tar.tb2 files can be decompressed in a similar way. For this you will need to type the following command in the command line:

```bash
tar -xvf sampleArchive.tar.bz2
```
### How to list the content of a .tar file

Once you have created the file, you can list the content by a command similar to the following:

```bash
tar -tvf sampleArchive.tar
```

This will show the complete list of files along with time marks and permissions. Similarly, for .tar.gz, you can use a command like:

```bash
tar -tvf sampleArchive.tar.gz
```

This would also work for .tar.bz2 files as shown below: tar -tvf sampleArchive.tar.bz2

### How to decompress a single .tar file

Once you create a compressed file, you can extract a single file from that tablet. This you can do with the command we show you below:

```bash
tar -xvf sampleArchive.tar example.sh
```

Here example.sh is a unique file that will be removed from the sample tablet Archive.tar. Alternatively, you can also use the following command:

```bash
tar --extract --file= sampleArchive.tar example.sh
```
To extract a single file from a .tar.gz tablet you can use a command similar to that shown below:

```bash
tar -zxvf sampleArchive.tar.gz example.sh
```

Or alternatively:

```bash
tar --extract --file= sampleArchive.tar.gz example.sh
```
To extract a single file from a .tar.bz2 tablet you can use a command like this:

```bash
tar -jxvf sampleArchive.tar.bz2 example.sh
```
Or, alternatively, one like this:

```bash
tar --extract --file= sampleArchive.tar.bz2 example.sh
```

### How to extract multiple files from .tar files

In case you want to extract several files, use the following command format:

```bash
tar -xvf sampleArchive.tar "file1" "file2" 
```

For .tar.gz you can use:

```bash
tar -zxvf sampleArchive.tar.gz "file1" "file2" 
```

For .tar.bz2 you can use:
```bash
tar -jxvf sampleArchive.tar.bz2 "file1" "file2"
```

### Extract multiple files with a pattern

If you want to remove from the tablet specific file patterns like only .jpg, use the wildcards command. A sample of this command is shown below:
```bash
tar -xvf sampleArchive.tar --wildcards '\*.jpg' 
```

For .tar.gz you can use:

```bash
tar -zxvf sampleArchive.tar.gz --wildcards '\*.jpg' 
```

For .tar.bz2 you can use:

```bash
tar -jxvf sampleArchive.tar.bz2 --wildcards '\*.jpg'
```

### How to add files to a .tar file

While you can extract specific files, you can also add new files to an existing compressed file. To do so, you must use the -r option that means adding. The Tar command can add both files and directories.

Below is an example in which we are adding example.jpg to the existing sampleArchive.tar.

```bash
tar -rvf sampleArchive.tar example.jpg
```

We can also add a directory. In the example shown below, the image\ _ dir directory is added to the sampleArchive.tar file

```bash
tar -rvf sampleArchive.tar image\_dir
```

You cannot add files or folders to .tar.gz or .tar.bz2. tablets

### How to verify a .tar file

Using Tar can verify a file. This is one of the ways you can do it:

```bash
tar -tvf sampleArchive.tar
```

This cannot be applied in .tar.gz or .tar.bz2. files

### How to verify the size of the .tar file

Once you create a file, you can check its size. This will be shown in KB (Kilobytes).

Below are several examples of the command to be used to verify the size of different types of compressed files:

```bash
tar -czf - sampleArchive.tar | wc -c
tar -czf - sampleArchive.tar.gz | wc -c tar -czf - sampleArchive.tar.bz2 | wc -c
```

### GZIP

You can compress a file using gzip with the command called gzip. Name of this package is gzip.

This is the simplest use: gzip filename

This will compress the file and add an .gz extension to it. The original file is deleted. To avoid this, you can use the - c and use the output redirection to write the output on the filename.gzfile:

```bash
gzip -c filename > filename.gz
```

the -c The option specifies that the output will go to the standard output flow, leaving the original file intact or you can use the -k option:

```bash
gzip -k filename
```

There are several levels of compression. The longer the compression, the longer it will take to compress (and decompress). The levels range from 1 (faster, worse compression) to 9 (slower, better compression), and the default value is 6.

You can choose a specific level with the -<number> option:
</number>
```bash
gzip -1 filename
```

You can compress several files by listing them:

```bash
gzip filename1 filename2
```

You can compress all files in a directory, recursively, using the -r:

```bash
gzip -r folder
```

gzipcan also be used to decompress a file, using the -d option:

```bash
gzip -d filename.gz
```

## BZIP2

The bzip2 is very similar to the gzip program. The main difference is that it uses a different compression algorithm called Burrows-Wheeler block classification text compression algorithm and Huffman coding. The bzip2 compressed files will end with the .bz2. extension

As I said, the use of bzip2 is almost the same as gzip. We will simply have to replace gzip in the above examples with bzip2, gunzip by bunzip2, zcat with bzcat and so on.

* * To compress a file using bzip2, replacing it with a compressed version, we will run: * *
```bash
bzip2 prueba.txt # Nos creara un archivo prueba.txt.bz2 
```
* * Compress files without removing the original file * *

If we do not want to replace the original file, we will use the -c option and write the result into a new file.

```bash
Bzip2 -c prueba.txt  # prueba.txt.bz2
```

* * Uncompress files * *

To decompress a compressed file we will use one of the following two possibilities:

```bash
bzip2 -d prueba.txt.bz2
bunzip2 prueba.txt.bz2
```

* * See the contents of the compressed files without uncompressing them * *

To see the content of a compressed file without uncompressing it, we will have to use any of the options:

```bash
bunzip2 -c ubunlog.txt.bz2 bzcat ubunlog.txt.bz2
```

## XZ

The packages are xz-utils

♪ Compress ♪

The simplest example of compression of a xz file is the following. File Compression with XZ

```bash
xz  deb.iso
```

The -z option can also be used to perform the compression:

```bash
xz -z  deb.iso
```

These orders will compress the file, but will remove the source file. If we do not seek to delete the source files, we will use the -k option as follows:

```bash
xz -k deb.iso
```

* * Uncompress * *

To decompress a file, we will be able to use the -d option:

```bash
xz -d deb.iso
unxz deb.iso
```

* * Forging compression * *

If an operation fails, for example, if there is a compressed file with the same name, we will use the -f option to force the process:

```bash
xz -kf deb.iso
```

* * Set compression levels * *

This tool supports different pre-established compression levels (0 to 9. With a default value of 6). We will also be able to use aliases like -fast (will be fast, but with less compression) to set as 0 and -best to set as 9 (slow but higher compression). Examples of how to set these levels are:

```bash
xz -k -8 deb.iso
xz -k --best deb.iso 
```

* * Limit memory * *

In case you have a small amount of system memory and want to compress a huge file, we will have the possibility to use the -memory = limit option (the limit value may be in MB or as a percentage of RAM) to set a memory use limit for compression:

```bash
xz -k --best --memlimit-compress=10% deb.iso
```


♪ Enable silent mode ♪

If we are interested in running the compression in silent mode, only the -q option will have to be added. We can also enable the detailed mode with -v, as shown below:

```bash
xz -k -q deb.iso
xz -k -qv deb.iso
```

* * Create a tar.xz file * *

The following is an example of use to get a file with the tar.xz. extension.

```bash
tar -cf *.txt | xz -7 > deb.tar.xz
```

Create a tar.xz file option 2

```bash
tar -cJf deb.tar.xz *.txt
```

* * Check the integrity of the compressed files * *

We can test the integrity of the compressed files using the -t option. Using -l we can see information about a compressed file.

```bash
xz -t deb.tar.xz xz -l deb.tar.xz
```

#7Z

This compressor has two packages:

- p7zip offers support for 7zr (a light version of 7z and 7za). It allows you to compress and decompress packages in these formats by using your system's graphic tool (file-roll in Ubuntu and Debian) but does not have the encryption functionality.
- p7zip-full is, to put it in some way, the most complete version. Supports 7z and 7za formats and incorporates encryption functionality, in addition to compression tools

## ZIP

* * Compress One or Several Files * *

The format is always the same, it consists of placing 7z, followed by the option to (to compress or pack), followed by the name you want to give to the final package (no need to place the extension .7z) and ending with the name of the file to compress. You can see that 7-Zip is able to take advantage of all the cores of your processor during the operation.

```bash
7z a paquete-comprimido archivo-a-comprimir 7z a paquete-comprimido archivo-1 archivo-2
```

If we want to put a password, we use the -p parameter:

```bash
7z  a -p paquete-comprimido archivo-a-comprimir
```

7-Zip supports several compression or packaging formats, other than its own, with this sentence you can choose to explicitly indicate which format you want to use (you can choose between 7z, zip, gzip, bzip2 or tar).

```bash
7z a -tgzip paquete-comprimido archivo-a-comprimir
```

* * List Tablet Folder Content * *

Another interesting option can be to list the content within a file and see the details. To do this, you must also place yourself in the directory where the compressed file or folder is located and type the following sentence.

```bash
7z l paquete-comprimido.7z
```

* * Uncompress Package and Remove Files * *

Once you have known the content within the file, to pull out all the content within the current work directory, you can use the following command:

```bash
7z e paquete-comprimido.7z
```

* * Check Data Integrity * *

As an additional option, you can also check the integrity of the different files inside the compressed file. This is what you use:

```bash
7z t paquete-comprimida.7z
```

### RAR

The package to install it is rar.

* * How to compress RAR in Linux * *

To compress a file or all of a folder:

```bash
rar a nombre_fichero_comprimido.rar nombre_fichero_a_comprimir rar a nombre_fichero_comprimido.rar 
```
* * How to decompress RAR in Linux * *

And to decompress in the same directory or another different one:

```bash
unrar x nombre\_del\_rar.rar

unrar x nombre\_del\_rar.rar /ruta/destino/descomprimido

```

## ZIP

The name of the package is zip.

To compress files:

```bash
zip archivo.zip archivos
```

To decompress files:

```bash
unzip archivo.zip
```

See content:

```bash
unzip -v archivo.zip
```

## Bibliography

- [Tar command guide] (https: / / www.hostinger.es / tutorials / como-usar-comando -tar-linux)
- [Gzip command guide] (https: / / tech-wiki.online / es / linux-command-gzip.html)
- [Bzip2 command guide] (https: / / ubunlog.com / comprymir-decomprymir-gzip-bzip2 / # The _ program _ bzip2)
- [Guide xz] (https: / / ubunlog.com / compression-xz-datos-sin-lost /)
- [Command guide 7z] (https: / / computernewage.com / 2016 / 01 / 10 / 7-zip-linux-guia -para-comprimir-y-decomprimir-files / # install -7-zip)
- [Rar command guide] (https: / / www.linuxaditos.com / tutorial-para-install-rari-en-linux@-@ y-learn-use)

