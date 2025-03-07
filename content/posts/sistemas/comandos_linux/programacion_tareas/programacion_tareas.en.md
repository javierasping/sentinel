---
title: "Linux task programming commands"
date: 2023-09-20T10:00:00+00:00
Description: In the Linux ecosystem, a process is the execution of a specific program that performs a particular task. Each process has its own unique identifier (PID) and is composed of a set of resources, such as memory and CPU, that allow it to operate independently.
tags: [Debian 12,Sistemas,ISO,ASO]
hero: images/sistemas/programacion_tareas/portada.png
---


The efficient management of programmed tasks is essential for system managers as it facilitates the automatic execution of routine processes. In this context, having a solid set of Linux commands to program and control tasks becomes a fundamental tool.

### Sleep command

The sleep command stops running in the terminal for a specified time interval before returning to the command line. You can indicate the time in seconds, minutes, hours or days. This command is found in the choreutils package.

- s: seconds
- m: minutes
- hours
- d: days

Ej: sleep 10m - > wait 10 min

In case it is not of any use, however it is very useful in Scripts. Here is a small example:

date + "% H:% M:% S '; sleep 5; date +"% H:% M:% S'

![](/sistemas/comandos_linux/programacion_tareas/img/Aspose.Words.cdeb5ac3-4737-4a2f-b87a-694716c02a3b.001.png)

### Watch command

The watch utility is part of the procps (or procps-ng) package that is pre-installed in almost all Gnu / Linux distributions.

When used without arguments, this utility will run the specified command every two seconds:

![](/sistemas/comandos_linux/programacion_tareas/img/Aspose.Words.cdeb5ac3-4737-4a2f-b87a-694716c02a3b.002.png)

![](/sistemas/comandos_linux/programacion_tareas/img/Aspose.Words.cdeb5ac3-4737-4a2f-b87a-694716c02a3b.003.png)

We can specify the repetition time using the -n parameter, specifying the parameter in seconds:

watch -n 5 date - > Every 5 seconds

If we want to remove the header, that is to say to show us every time it is repeated, we use the -t parameter:

![](/sistemas/comandos_linux/programacion_tareas/img/Aspose.Words.cdeb5ac3-4737-4a2f-b87a-694716c02a3b.004.png)

If we want to put an error message in case the command cannot be executed we use the -and parameter followed by the error message:

watch -e 'error'

The -b watch option emits a beep every time the command comes out with a different state code from zero.

watch -b

With the parameter -d it points to the changes that have occurred in the execution of the command: watch -d

![](/sistemas/comandos_linux/programacion_tareas/img/Aspose.Words.cdeb5ac3-4737-4a2f-b87a-694716c02a3b.005.png)

### Command at

This command is used to run commands at a certain time, mainly used to program periodic tasks such as can be, backup.

The main parameters are:

- **V**: print the version number on the standard error and come out successfully.

- **m**: Send mail to the user when the work has been completed even if there has been no output. -M: He never sends mail to the user.

- **f**: Read the work file from a file instead of the standard input.

- **t**: time Executs work on time, given in the format [[CC] YY] MMDDhhmm [.ss]

- **l**: It's an alias for atq.

- **r**: It's an alias for atrm.

- **d**: It's an alias for atrm.

- **b**: It's an alias for batch.

- **v**: It shows the time the work will run before reading it.

- **The** times shown will be in the format "Thu Feb 20 14: 50: 00 1997."

- **c** collects the works listed in the command line on the standard output.

We can program tasks from the command line, with echo:

echo "sh copia-segurity.sh" ¦ 124; at 10: 00 PM

Has this task will be assigned a number automatically, to list the tasks we have we invoke the at command without any parameter

If we want to delete a scheduled task, we use the -c parameter followed by the task number to be removed.

Examples to schedule tasks include:

- Within 30 min: at now + 30 minutes
- 11AM of next 14 April: at 11: 00 AM April 14

### Crontab command

The crontab command is used in UNIX systems to program the execution of other commands, that is, to automate tasks. We can see the chrontabs that are being programmed and also edit them, logically.

To see them, we use this command: sudo crontab -l To edit: sudo crontab -e

The cron tasks follow a certain syntax. They have 5 asterisks followed by the command to run. Now I'll explain what it's all about.

\ *\ *\ *\ **/ bin / run / script.sh

The 5 asterisks, from left to right, the asterisks represent:

- Minutes: from 0 to 59.
- Hours: 0 to 23.
- Day of the month: from 1 to 31.
- Month: 1 to 12.
- Day of the week: from 0 to 6, being 0 on Sunday.

If you leave an asterisk, you mean "every minute, time, day of month, month or day of the week.

If we want a file to run at 5 in the morning every day: 0 5\ *\ *\ * path\ _ absolute\ _ from the\ _ script

To run twice a day at 6 AM and 6 PM: 0 6,18\ *\ **path\ _ absolute\ _ of the\ _ script

We often have words reserved to facilitate the use of programming programs or languages. Cron couldn't be less, so we have some that are usually the most common. Now everyone who sets it up according to their needs. Here they go:

- @ reboot: runs once at the start.
- @ early / @ annual: run every year.
- @ monthly: run once a month.
- @ weekly: once a week.
- @ daily / @ midnight: once a day.
- @ hourly: every hour.

We must also know the uses of the parameters:

crontab archivo.cron (set the file as the user's crontab)

crontab -e (will open the pre-established editor where you can create or edit the crontab file) crontab -l (list the current user crontab, your cron tasks)

crontab -r (removes current user crontab)

When we make some change we must restart the service to make sure that our changes take effect:

service crow restart

These commands will give us the possibility to automate processes, making the management of our systems more comfortable and friendly.

## Bibliography

- [Watch command](https://ubunlog.com/comando-watch-some-formas-de-use/) 
- [Crontab command](https://geekytheory.com/programar-tareas-en-linux-using-crontab/)

