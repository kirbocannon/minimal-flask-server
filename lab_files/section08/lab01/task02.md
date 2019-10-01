## Task 2: Running custom Linux applications
The guest shell allows us to install third-party packages just like any other Linux system. These packages can be used to automate and gather metrics about your switch. 

Note: Since we will be installing a few packages to the guest shell, the guest shell has been allocated more disk space prior to this lab. The default is `200MB` and has been increased to `800MB`.

**Connect to the student workstation**  
`ssh student@172.16.66.100`

**Connect to the 9K Nexus switch `N9K-A-Pod6`:**      
`student@student-vm:~$ ssh admin@192.168.16.110` 

**Access the guest shell on the Nexus switch**    
`N9K-A-Pod6# run guestshell`

**To Install some third-party linux packages:**    
DNS is used to resolve the Linux repos locations that host our third-party packages. Linux keeps DNS information in the `/etc/resolve.conf` file. Add the following line to the `resolve.conf` with a text editor:  

`[admin@guestshell ~]$ nameserver 192.168.10.40`

**Install NMAP:**  
Use `yum` package manager to install NMAP (Network Mapper). Yum can be used to install and uninstall third-party packages. NMAP is a tool for discovering hosts and services on a computer network. It is used often in the cyber security security industry. 
`[admin@guestshell ~]$ sudo chvrf management yum -y install nmap`

`sudo` - Elevate priviledges to superuser so that we can install this application  
`chvrf` - A guest shell bash script that allows us to change the context (VRF) to run that command in. Since the management inerface has internet access, we will change the VRF to `management`  
`-y` - Used for convinence so we do not have to type `y` and automatically accept the install prompt. 

**Scan the jumphost with nmap and save results to .txt file:**  
Use `nmap` in the `management` vrf to scan the jumphost and save the results to a text file:  
`[admin@guestshell ~]$ sudo chvrf management nmap -v -p 1-65535 -sV -O -sS -T4 192.168.16.122 > nmapresults.txt`

**View the results from the NMAP Scan:**  
Use the Linux `cat` command to print the contents of a file to the console:  
```
[admin@guestshell ~]$ cat nmapresults.txt 

Starting Nmap 6.40 ( http://nmap.org ) at 2019-09-30 17:13 UTC
NSE: Loaded 23 scripts for scanning.
Initiating ARP Ping Scan at 17:13
Scanning 192.168.16.122 [1 port]
Completed ARP Ping Scan at 17:13, 0.04s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 17:13
Completed Parallel DNS resolution of 1 host. at 17:13, 0.00s elapsed
Initiating SYN Stealth Scan at 17:13
Scanning 192.168.16.122 [65535 ports]
Discovered open port 22/tcp on 192.168.16.122
Completed SYN Stealth Scan at 17:13, 1.55s elapsed (65535 total ports)
Initiating Service scan at 17:13
Scanning 1 service on 192.168.16.122
Completed Service scan at 17:13, 6.00s elapsed (1 service on 1 host)
Initiating OS detection (try #1) against 192.168.16.122
Retrying OS detection (try #2) against 192.168.16.122
Retrying OS detection (try #3) against 192.168.16.122
Retrying OS detection (try #4) against 192.168.16.122
Retrying OS detection (try #5) against 192.168.16.122
NSE: Script scanning 192.168.16.122.
Nmap scan report for 192.168.16.122
Host is up (0.00023s latency).
Not shown: 65534 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     (protocol 2.0)
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at http://www.insecure.org/cgi-bin/servicefp-submit.cgi :
SF-Port22-TCP:V=6.40%I=7%D=9/30%Time=5D9237B8%P=x86_64-redhat-linux-gnu%r(
SF:NULL,29,"SSH-2\.0-OpenSSH_7\.6p1\x20Ubuntu-4ubuntu0\.3\r\n");
MAC Address: 00:50:56:8D:F1:0B (VMware)
No exact OS matches for host (If you know what OS is running on it, see http://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=6.40%E=4%D=9/30%OT=22%CT=1%CU=37040%PV=Y%DS=1%DC=D%G=Y%M=005056%T
OS:M=5D9237C4%P=x86_64-redhat-linux-gnu)SEQ(SP=103%GCD=1%ISR=10A%TI=Z%CI=I%
OS:II=I%TS=A)OPS(O1=M5B4ST11NW7%O2=M5B4ST11NW7%O3=M5B4NNT11NW7%O4=M5B4ST11N
OS:W7%O5=M5B4ST11NW7%O6=M5B4ST11)WIN(W1=7120%W2=7120%W3=7120%W4=7120%W5=712
OS:0%W6=7120)ECN(R=Y%DF=Y%T=40%W=7210%O=M5B4NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=40
OS:%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=
OS:%RD=0%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%
OS:W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=
OS:)U1(R=Y%DF=N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%
OS:DFI=N%T=40%CD=S)

Uptime guess: 23.789 days (since Fri Sep  6 22:16:49 2019)
Network Distance: 1 hop
TCP Sequence Prediction: Difficulty=259 (Good luck!)
IP ID Sequence Generation: All zeros

Read data files from: /usr/bin/../share/nmap
OS and Service detection performed. Please report any incorrect results at http://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.85 seconds
           Raw packets sent: 65646 (2.892MB) | Rcvd: 65621 (2.631MB)
```