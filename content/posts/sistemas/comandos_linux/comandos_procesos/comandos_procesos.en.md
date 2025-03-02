---
title: "Linux Process Management"
date: 2023-09-08T10:00:00+00:00
Description: In the Linux ecosystem, a process is the execution of a specific program that performs a particular task. Each process has its own unique identifier (PID) and is composed of a set of resources, such as memory and CPU, that allow it to operate independently.
tags: [Debian 12,Sistemas,ISO,ASO]
hero: images/sistemas/comandos_procesos/portata_procesos.jpg
---


In the Linux ecosystem, a process is the execution of a specific program that performs a particular task. Each process has its own unique identifier (PID) and is composed of a set of resources, such as memory and CPU, that allow it to operate independently.

In the Linux universe, effective process management is a crucial ability to optimize performance and ensure system stability. This post will immerse you in the essential foundations of process management

## PS

If we do not add any parameters, ps will show the user processes with which we are logged. On the other hand, the most basic parameters known are:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.001.png)

* * aux * *: List the processes of all users with added information (we highlight below).

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.002.png)

* * -a * * List the processes of all users.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.003.png)

* * -u * * List process information such as the running user, CPU use and memory, etc.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.004.png)

* * -x * * List processes of all terminals and users

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.005.png)

* * -l * * It shows information that includes the UID and the "nice" value.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.006.png)

* * --forest * * It shows the process listing in a tree-type format that allows you to see how processes interact with each other, it could be something similar to the pstree command.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.007.png)

### PSTREE

The pstree program provides information on the completion of a number of related processes, that is, all the descendants of a particular process. The program makes it clear from the beginning that the process is primary and secondary. This avoids looking for the relationships between the various processes manually.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.008.png)

commonly used parameters:

* * -H * *: If we are interested we can see the tree of a specific process:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.009.png)

* * -g * *: Group processes:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.010.png)

* * -n * *: Allows us to order the output by the PID number:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.011.png)

* * -p * *: Shows the PID number

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.012.png)

* * -s * *: Shows parent processes

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.013.png)

### SYSTEMCTL STATUS

This command is used to see the state of a service, specifically, shows information on whether the service or unit is active or inactive, and whether it is in operation or in detention. It also shows any error or warning message related to the service or unit. This command is useful to verify the status of a service or unit in the system and to solve related problems.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.014.png)

## TOP

It is a all-in-one program: simultaneously it performs the functions of ps and kill. It's a console command, so you should start it from a terminal.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.015.png)

Within this we can control it using the following keys:

* * -k * *: This command is used to send a signal to a process. Then top will ask you about the process PID, followed by the number of the signal to be sent (predetermined TERM - or 15);

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.016.png)

* * -M * *: this command is used to order the listing of the processes according to the memory they use (field% MEM);

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.017.png)

* * -P * *: this command is used for

order the list of processes according to the CPU time they consume (field% CPU; this is the default method of ordering);

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.018.png)

* * -u * *: This command is used to show the processes of a particular user, top will ask you which one. You must enter the user name.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.019.png)

* * -i * *: this command acts as a switch; predetermined all processes, even those that are asleep, are displayed; this command ensures that only the processes that are in the course of execution are shown:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.020.png)

## HTOP

Htop is the improved and current version of top which has a more friendly interface and more functionalities which will help us to monitor processes. This is divided into several parts:

The header divides the top of the interface into left and right sections. These show the use of CPU / memory, exchange space, machine activity time, tasks and average load.

The upper left section shows a line for each CPU core. For example, the previous screen capture shows two CPU cores, with the percentage that represents the load in each.

You can also see the color code provided by htop to identify what type of processes the CPU uses:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.021.png)

- Red: percentage occupied by system processes
- Blue: percentage occupied by low priority process
- Green: percentage occupied by user processes

The memory lines also use color codes, this time to represent:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.022.png)

- Yellow: percentage occupied by cache content
- Green: percentage occupied by the memory used
- Blue: percentage occupied by buffer content

The central panel shows all the processes in progress with its associated statistics according to the use of the CPU. It shows the following information for each process:

- Process ID (PID)
- The owner (User)
- Virtual memory consumption percentage of processor physical memory

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.023.png)

To end this program is also interactive, below we have an index where we can check the functions that allow us to use:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.024.png)

We also have several keyboards:

- or Order processes by username
- p Alternate with the program route
- F2 or S Enter Configuration
- F3 or / Search process
- F5 or t
- F6 + / - Select the main process to expand / contract the tree
- F7 or [Increase the priority only for root
- F8 or] Low priority (good +)
- F9 or k Kill process
- H Alterna with user process subprocesses
- K Alterna with kernel process subprocesses

## &

The & symbol is a shell operator in Unix and Linux that allows you to run a background process. When setting & at the end of a command, the process will be run in the background and you will be assigned a task in the background. This means that the process will run in parallel with other tasks and will not block the terminal or command line until it is finished.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.025.png)

## JOBS

This command will list the processes that are in second hand as well as their status, let us know your PID:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.026.png)

## FG

Complementing the previous command, it allows us to resume in the foreground the last work that was suspended.:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.027.png)

Listing with jobs we can send a specific process to the foreground:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.028.png)

## BG

When a command is running you can suspend it using ctrl-Z. The command will stop immediately, and you will return to the terminal shell.

You can resume the execution of the command in the background, so it will continue to run but it will not prevent you from doing another job in the terminal.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.029.png)

### KILL

Linux processes can receive and react to signals. That is one way we can interact with ongoing programmes. The kill program can send a variety of signals to a program. Not only is it used to finish a program, as the name suggests, but it is its main work by default, it sends a TERM signal to the indicated process identifier.

We can list the signals with kill-l:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.030.png)

We send a signal with the -s parameter followed by the number of this and the PID of the process:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.031.png)

### XKILL

This is the simplest and most practical method. The mouse cursor will be transformed into a small skull. All that remains is to click on the window you want to close and voila. Chau proceso.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.032.png)

### KILLALL

Similar to the kill command, killall will send the signal to multiple processes at once instead of sending a signal to a specific process identifier. For example, you can have multiple instances of the top program running, and killall top will end with all of them.

You can specify the signal, as with kill:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.033.png)

For example we can kill all the tops:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.034.png)

### PIDOF

Allows you to find the process ID of a running program:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.035.png)

* * -s * *: Single request - orders the program to return a single process identifier

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.036.png)

### PID BASH

* * echo t $→ id bash * *

It's a quick way to find the current bash identifier:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.037.png)

NICE

Run a command with a given priority, or change the priority to a process (running program). It uses a variable priority that part of the shell priority and sums up or subtract values. The lower the value of the priority the process has.

The value of the priority of the find process increases by 5, decreases its priority.

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.038.png)

### RENICE

It serves to change the priority of a process:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.039.png)

### PKILL

This command allows us to kill a process from which we know your full name or part of it. Let's see an example:

![](../img/Aspose.Words.cdf0ee61-4f6a-42ca-bc2e-28e5236ec493.040.png)

## Bibliography

- [Pstree use guide] (https: / / www.ochobitshacenunbyte.com / 2018 / 06 / 04 / visualize -trees -de-processes -en-linux-con-pstree /)
- (https: / / ergodic.ugr.es / cphysn / LECTIONS / UNIX / Command-Line10.pdf)
- [Htop use guide] (https: / / blog.elhacker.net / 2022 / 01 / top-replace -htop-and -monitor-processes-resources-services-linux@-@ time-real.html)
- [Guide to use nice, renice, kill...] (https: / / www.digitalocean.com / community / tutorials / how-to-use-ps-kill-and-nice-to-manage-process-in-linux@-@ es)

