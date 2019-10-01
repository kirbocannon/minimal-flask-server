# Lab 3: Using Python to enchance CLI commands

**Task 1: Ensure git client is installed:**  
Use `yum list git` in order to check if the `git` package is installed.

```
[admin@guestshell ~]$ yum list git
Loaded plugins: fastestmirror
Determining fastest mirrors
 * base: centos.mirror.ndchost.com
 * extras: centos.mirror.ndchost.com
 * updates: centos.sonn.com
Installed Packages
git.x86_64                                             1.8.3.1-20.el7                                             @base
```


**If git client is not installed, run the following command to install it:**  

```
[admin@guestshell ~]$ sudo chvrf management yum  -y install git
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirror.keystealth.org
 * extras: mirror.fileplanet.com
 * updates: mirror.keystealth.org
base                                                                                            | 3.6 kB  00:00:00
extras                                                                                          | 2.9 kB  00:00:00
updates                                                                                         | 2.9 kB  00:00:00
Resolving Dependencies
--> Running transaction check
---> Package git.x86_64 0:1.8.3.1-20.el7 will be installed
--> Processing Dependency: perl-Git = 1.8.3.1-20.el7 for package: git-1.8.3.1-20.el7.x86_64
--> Processing Dependency: perl(Git) for package: git-1.8.3.1-20.el7.x86_64
--> Running transaction check
---> Package perl-Git.noarch 0:1.8.3.1-20.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

=======================================================================================================================
 Package                     Arch                      Version                           Repository               Size
=======================================================================================================================
Installing:
 git                         x86_64                    1.8.3.1-20.el7                    base                    4.4 M
Installing for dependencies:
 perl-Git                    noarch                    1.8.3.1-20.el7                    base                     55 k

Transaction Summary
=======================================================================================================================
Install  1 Package (+1 Dependent package)

Total download size: 4.4 M
Installed size: 22 M
Downloading packages:
(1/2): perl-Git-1.8.3.1-20.el7.noarch.rpm                                                       |  55 kB  00:00:00
(2/2): git-1.8.3.1-20.el7.x86_64.rpm                                                            | 4.4 MB  00:00:00
-----------------------------------------------------------------------------------------------------------------------
Total                                                                                   14 MB/s | 4.4 MB  00:00:00
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : git-1.8.3.1-20.el7.x86_64                                                                           1/2
  Installing : perl-Git-1.8.3.1-20.el7.noarch                                                                      2/2
  Verifying  : perl-Git-1.8.3.1-20.el7.noarch                                                                      1/2
  Verifying  : git-1.8.3.1-20.el7.x86_64                                                                           2/2

Installed:
  git.x86_64 0:1.8.3.1-20.el7

Dependency Installed:
  perl-Git.noarch 0:1.8.3.1-20.el7

Complete!
```