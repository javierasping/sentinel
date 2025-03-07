---
title: "Comparative between OpenVPN and Wireguard"
date: 2024-03-28T10:00:00+00:00
Description: Comparative between OpenVPN and Wireguard
tags: [VPN,LINUX,DEBIAN,WIREGUARD,OPENVPN]
hero: /images/vpn/wire_ovpn.png
---



![](/vpn/comparativa_ovpn_wire/img/Pastedimage20240114150833.png)

The goal of this post is to compare the different VPNs software most used by seeing which is faster, for which we will support in speed test using iperf3.

> [NOTE]
> The comparative part of the posts in this section in which we mount each type of VPN.


## Speed without VPN

I'm gonna start by comparing the speeds of these 2 systems, using iperf3. For this I have removed the cisco router as I had it configured with FastEthernet interfaces and changed it to a Linux router with GigabitEthernet interfaces.

I'm going to launch an iperf3 using public addresses so that the traffic does not use any VPN:

```bash
javiercruces@servidor2:~$ iperf3 -c 90.0.0.2 -i 1 -t 30
Connecting to host 90.0.0.2, port 5201
[  5] local 100.0.0.2 port 32858 connected to 90.0.0.2 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec   110 MBytes   919 Mbits/sec  897    188 KBytes       
[  5]   1.00-2.00   sec   102 MBytes   859 Mbits/sec  712    120 KBytes       
[  5]   2.00-3.00   sec   111 MBytes   931 Mbits/sec  735   83.4 KBytes       
[  5]   3.00-4.00   sec   112 MBytes   944 Mbits/sec  600    173 KBytes       
[  5]   4.00-5.00   sec   109 MBytes   913 Mbits/sec  1018    126 KBytes       
[  5]   5.00-6.00   sec   115 MBytes   961 Mbits/sec  889    113 KBytes       
[  5]   6.00-7.00   sec   113 MBytes   947 Mbits/sec  549   90.5 KBytes       
[  5]   7.00-8.00   sec   116 MBytes   976 Mbits/sec  964    198 KBytes       
[  5]   8.00-9.00   sec   114 MBytes   956 Mbits/sec  591   76.4 KBytes       
[  5]   9.00-10.00  sec   108 MBytes   908 Mbits/sec  736    120 KBytes       
[  5]  10.00-11.00  sec   105 MBytes   881 Mbits/sec  689    126 KBytes       
[  5]  11.00-12.00  sec   106 MBytes   893 Mbits/sec  745    124 KBytes       
[  5]  12.00-13.00  sec   118 MBytes   990 Mbits/sec  847   93.3 KBytes       
[  5]  13.00-14.00  sec   122 MBytes  1.03 Gbits/sec  899   94.7 KBytes       
[  5]  14.00-15.00  sec   125 MBytes  1.05 Gbits/sec  1014   73.5 KBytes       
[  5]  15.00-16.00  sec   125 MBytes  1.05 Gbits/sec  973    113 KBytes       
[  5]  16.00-17.00  sec   109 MBytes   915 Mbits/sec  934   86.3 KBytes       
[  5]  17.00-18.00  sec   101 MBytes   844 Mbits/sec  629    115 KBytes       
[  5]  18.00-19.00  sec   105 MBytes   881 Mbits/sec  652    122 KBytes       
[  5]  19.00-20.00  sec   116 MBytes   971 Mbits/sec  826   96.2 KBytes       
[  5]  20.00-21.00  sec   115 MBytes   962 Mbits/sec  820   99.0 KBytes       
[  5]  21.00-22.00  sec   128 MBytes  1.08 Gbits/sec  1193   99.0 KBytes       
[  5]  22.00-23.00  sec   130 MBytes  1.09 Gbits/sec  1027    110 KBytes       
[  5]  23.00-24.00  sec   123 MBytes  1.03 Gbits/sec  855    116 KBytes       
[  5]  24.00-25.00  sec   122 MBytes  1.03 Gbits/sec  714    126 KBytes       
[  5]  25.00-26.00  sec   120 MBytes  1.01 Gbits/sec  861    119 KBytes       
[  5]  26.00-27.00  sec   129 MBytes  1.08 Gbits/sec  768    112 KBytes       
[  5]  27.00-28.00  sec   125 MBytes  1.05 Gbits/sec  976    140 KBytes       
[  5]  28.00-29.00  sec   116 MBytes   972 Mbits/sec  943    140 KBytes       
[  5]  29.00-30.00  sec   119 MBytes   996 Mbits/sec  755    116 KBytes  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-30.00  sec  3.39 GBytes   970 Mbits/sec  24811             sender
[  5]   0.00-30.00  sec  3.39 GBytes   970 Mbits/sec                  receiver
```

The average speed of the network has been 970 Mbits / sec, without using any VPN.

## Wireguard speed

We'll measure the speed of Wireguard:

```bash
javiercruces@cliente3:~$ iperf3 -c 192.168.0.2 -i 1 -t 30
Connecting to host 192.168.0.2, port 5201
[  5] local 192.168.1.2 port 39096 connected to 192.168.0.2 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  57.5 MBytes   483 Mbits/sec   63    196 KBytes       
[  5]   1.00-2.00   sec  56.4 MBytes   473 Mbits/sec   37    190 KBytes       
[  5]   2.00-3.00   sec  58.2 MBytes   488 Mbits/sec   85    188 KBytes       
[  5]   3.00-4.00   sec  57.1 MBytes   479 Mbits/sec   65    140 KBytes       
[  5]   4.00-5.00   sec  57.8 MBytes   485 Mbits/sec    6    199 KBytes       
[  5]   5.00-6.00   sec  59.7 MBytes   500 Mbits/sec   62    200 KBytes       
[  5]   6.00-7.00   sec  59.0 MBytes   495 Mbits/sec   26    234 KBytes       
[  5]   7.00-8.00   sec  57.8 MBytes   485 Mbits/sec   13    216 KBytes       
[  5]   8.00-9.00   sec  58.6 MBytes   492 Mbits/sec   88    151 KBytes       
[  5]   9.00-10.00  sec  58.1 MBytes   487 Mbits/sec   13    174 KBytes       
[  5]  10.00-11.00  sec  57.9 MBytes   486 Mbits/sec   22    135 KBytes       
[  5]  11.00-12.00  sec  57.1 MBytes   479 Mbits/sec   30    188 KBytes       
[  5]  12.00-13.00  sec  57.3 MBytes   481 Mbits/sec   19    178 KBytes       
[  5]  13.00-14.00  sec  57.1 MBytes   479 Mbits/sec   15    230 KBytes       
[  5]  14.00-15.00  sec  56.5 MBytes   474 Mbits/sec   20    218 KBytes       
[  5]  15.00-16.00  sec  57.4 MBytes   481 Mbits/sec   38    172 KBytes       
[  5]  16.00-17.00  sec  55.9 MBytes   469 Mbits/sec  137    143 KBytes       
[  5]  17.00-18.00  sec  57.0 MBytes   478 Mbits/sec   26    246 KBytes       
[  5]  18.00-19.00  sec  56.6 MBytes   475 Mbits/sec   42    183 KBytes       
[  5]  19.00-20.00  sec  56.2 MBytes   471 Mbits/sec   43    222 KBytes       
[  5]  20.00-21.00  sec  56.5 MBytes   474 Mbits/sec   11    203 KBytes       
[  5]  21.00-22.00  sec  56.4 MBytes   473 Mbits/sec   69    147 KBytes       
[  5]  22.00-23.00  sec  54.1 MBytes   454 Mbits/sec   25    163 KBytes       
[  5]  23.00-24.00  sec  55.9 MBytes   469 Mbits/sec   54    207 KBytes       
[  5]  24.00-25.00  sec  57.5 MBytes   482 Mbits/sec   99    164 KBytes       
[  5]  25.00-26.00  sec  56.5 MBytes   474 Mbits/sec   39    182 KBytes       
[  5]  26.00-27.00  sec  56.7 MBytes   476 Mbits/sec   24    150 KBytes       
[  5]  27.00-28.00  sec  56.3 MBytes   472 Mbits/sec    6    219 KBytes       
[  5]  28.00-29.00  sec  57.0 MBytes   478 Mbits/sec   15    146 KBytes       
[  5]  29.00-30.00  sec  56.0 MBytes   470 Mbits/sec   48    151 KBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-30.00  sec  1.67 GBytes   479 Mbits/sec  1240             sender
[  5]   0.00-30.00  sec  1.67 GBytes   479 Mbits/sec                  receiver
```

The average speed of wireguard has been 479 Mbits / sec.

## OpenVPN speed

Let's measure the speed of OpenVPN

```bash
javiercruces@cliente3:~$ iperf3 -c 192.168.0.2 -i 1 -t 30
Connecting to host 192.168.0.2, port 5201
[  5] local 192.168.1.2 port 43522 connected to 192.168.0.2 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  25.1 MBytes   211 Mbits/sec   24    139 KBytes       
[  5]   1.00-2.00   sec  24.8 MBytes   208 Mbits/sec   15    163 KBytes       
[  5]   2.00-3.00   sec  23.7 MBytes   199 Mbits/sec   40    103 KBytes       
[  5]   3.00-4.00   sec  24.6 MBytes   207 Mbits/sec   19    114 KBytes       
[  5]   4.00-5.00   sec  24.2 MBytes   203 Mbits/sec    8    119 KBytes       
[  5]   5.00-6.00   sec  24.3 MBytes   204 Mbits/sec   14    155 KBytes       
[  5]   6.00-7.00   sec  24.2 MBytes   203 Mbits/sec   13    139 KBytes       
[  5]   7.00-8.00   sec  24.5 MBytes   206 Mbits/sec   18    115 KBytes       
[  5]   8.00-9.00   sec  24.0 MBytes   201 Mbits/sec   34    132 KBytes       
[  5]   9.00-10.00  sec  24.3 MBytes   204 Mbits/sec   32    120 KBytes       
[  5]  10.00-11.00  sec  24.5 MBytes   206 Mbits/sec   12    100 KBytes       
[  5]  11.00-12.00  sec  24.4 MBytes   205 Mbits/sec    8    139 KBytes       
[  5]  12.00-13.00  sec  23.9 MBytes   201 Mbits/sec    6    171 KBytes       
[  5]  13.00-14.00  sec  24.1 MBytes   202 Mbits/sec   20    156 KBytes       
[  5]  14.00-15.00  sec  24.0 MBytes   202 Mbits/sec    8    135 KBytes       
[  5]  15.00-16.00  sec  23.5 MBytes   197 Mbits/sec   21    143 KBytes       
[  5]  16.00-17.00  sec  24.0 MBytes   202 Mbits/sec    8    168 KBytes       
[  5]  17.00-18.00  sec  24.6 MBytes   206 Mbits/sec   24    154 KBytes       
[  5]  18.00-19.00  sec  23.8 MBytes   200 Mbits/sec   21    132 KBytes       
[  5]  19.00-20.00  sec  24.3 MBytes   204 Mbits/sec   20    139 KBytes       
[  5]  20.00-21.00  sec  24.6 MBytes   206 Mbits/sec   11    142 KBytes       
[  5]  21.00-22.00  sec  23.0 MBytes   193 Mbits/sec   26    115 KBytes       
[  5]  22.00-23.00  sec  24.6 MBytes   207 Mbits/sec    3    128 KBytes       
[  5]  23.00-24.00  sec  24.0 MBytes   202 Mbits/sec   26    104 KBytes       
[  5]  24.00-25.00  sec  24.3 MBytes   204 Mbits/sec   21    106 KBytes       
[  5]  25.00-26.00  sec  24.3 MBytes   204 Mbits/sec   15    108 KBytes       
[  5]  26.00-27.00  sec  23.8 MBytes   200 Mbits/sec   36    132 KBytes       
[  5]  27.00-28.00  sec  22.9 MBytes   192 Mbits/sec   13    118 KBytes       
[  5]  28.00-29.00  sec  23.7 MBytes   199 Mbits/sec   19    163 KBytes       
[  5]  29.00-30.00  sec  24.2 MBytes   203 Mbits/sec   11    126 KBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-30.00  sec   725 MBytes   203 Mbits/sec  546             sender
[  5]   0.00-30.00  sec   724 MBytes   202 Mbits/sec                  receiver
```

The average speed has been 203 Mbits / sec.


Conclusions

If we compare the results, it is clear that in terms of speed, WireGuard has proved to be the most efficient option, significantly exceeding OpenVPN, doubling it in speed.

WireGuard is designed for fast speed. It establishes a connection in 100 milliseconds, while OpenVPN takes 8 milliseconds. In some tests, WireGuard proved to be 58% faster than OpenVPN. In ideal circumstances, its speed exceeded 500 mbps.

WireGuard is the fastest protocol due to many factors. These include:

- Its light code makes it intrinsically the fastest protocol.
- WireGuard also supports multithreatening - processing data using many CPU cores simultaneously - and uses a faster encryption method.
- In addition, WireGuard is good at using the available bandwidth and operates completely in the kernel space.

To avoid censorship, OpenVPN is better than WireGuard. Why? Because the OpenVPN protocol can work on the layers of the UPD and TCP Protocol.

UDP is faster, while TCP is reliable. TCP can avoid censorship using port 443, the same port that HTTPS uses. Thanks to TCP, OpenVPN avoids censorship of strict countries such as China and Russia. In some cases, an advanced deep inspection can detect OpenVPN. But for these cases, safety experts recommend using the Scramble within the advanced protocol configuration to add another layer of protection to the VPN traffic.

On the other hand, WireGuard only uses the UDP layer to transport data. And the main purpose of UDP is to transport data at high speed, not to evade censorship. This makes it easy to detect. In addition, it is susceptible to deep inspection of packages.

OpenVPN is safe if properly configured. This protocol has no known security vulnerabilities, and its code has been audited many times. In addition, it has many encryption and authentication algorithms. When there is some security vulnerability in the algorithm, then OpenVPN can immediately configure another thing.

In terms of security cases, WireGuard has also gained a good reputation. It is safe and uses the latest cryptography. Your code is short and easy to audit. In addition, WireGuard has a fixed set of algorithms and encryption. When some vulnerability is found, all end points are updated to a new version, which ensures that no one reuses unsafe code.