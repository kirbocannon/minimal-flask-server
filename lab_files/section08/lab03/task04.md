# Lab 3: Using Python to enchance CLI commands

# Task 5: Make changes and view configurations diffs with git
You can view delta's between files managed by git. For instance, if you have made more recent changes file A, and want to compare it to file B that was commited two days ago, you can do that. In our case, NXOS is instructed to commit to git any time the `copy running-config startup-config` is ran and the configuration file has changed in some way. 

**Connect to the student workstation:**  
`ssh student@172.16.66.100`

**Connect to the 9K Nexus switch `N9K-A-Pod6`:**   
`student@student-vm:~$ ssh admin@192.168.16.110`

**Change an interface description in the running config and save again:**  
```
N9K-A-Pod6# config terminal
N9K-A-Pod6(config)# interface ethernet 1/71
N9K-A-Pod6(config)# description THIS IS A NEW DESCRIPTION
N9K-A-Pod6(config)# copy running-config startup-config
```

**Save the running config:**  
`N9K-A-Pod6# copy running-config startup-config`

**Enter guest shell and compare commits:**   
We will use `git log` in order to view past commits. Each commit is saved with a unique hash value which identifies the commited file(s) and saves the state of the file(s) at a particular point in time.  
```
[admin@guestshell ~]$ run guestshell
[admin@guestshell ~]$ cd network_configs
[admin@guestshell network_configs]$ git log

commit 7f030701e5b81cbb8dd19be41665af49ec89f5aa
Author: git <git@gittest.com>
Date:   Sat Sep 28 01:01:22 2019 +0000

    Configuration change

commit e5a8c8c076a8bf8530b10868bd56127e613762e4
Author: git <git@gittest.com>
Date:   Sat Sep 28 01:00:29 2019 +0000

    Configuration change
```

The above shows two commits and the time they were commited. In our case, these are two different versions of the NXOS switche's running configuraiton, each pushed to the remote repository. Now that we have the commit IDs (hashes), we can compare the two using the `git diff` command. Here, we give `git diff` two arguments, commit A and commit B IDs. IDs are unique, so it will not be exactly the same as the example. You will have to run `git log` and note the two commits you want to compare. 

```
[admin@guestshell network_configs]$ git diff 7f030701e5b81cbb8dd19be41665af49ec89f5aa e5a8c8c076a8bf8530b10868bd56127e613762e4
diff --git a/N9K-A-Pod6/running.latest b/N9K-A-Pod6/running.latest
index 76c2aaa..6f5d218 100644
--- a/N9K-A-Pod6/running.latest
+++ b/N9K-A-Pod6/running.latest
@@ -1,7 +1,7 @@

 !Command: show running-config
-!Running configuration last done at: Sat Sep 28 01:05:09 2019
-!Time: Sat Sep 28 01:10:36 2019
+!Running configuration last done at: Sat Sep 28 01:13:47 2019
+!Time: Sat Sep 28 01:13:52 2019

 version 9.3(1) Bios:version
 power redundancy-mode combined force
@@ -192,6 +192,7 @@ interface Ethernet1/69
 interface Ethernet1/70

 interface Ethernet1/71
+  description THIS IS A NEW DESCRIPTION

 interface Ethernet1/72
```

The output shows the changes we made to `Ethernet1/71`'s description. git prepends additions with `+` and deletions with `-`. Since every time you save the running configuration to a file, the switch adds a timestamp, this changed as well. git is also showing that a description was added under `Ethernet1/71`. `@@` indicates the start of a new hunk. `-192,6` indicates the original file starting on line 192, had 6 lines before this diff was applied. And `+192,7` means that starting on line one, this file has 7 lines after diff was appied. Since `+` Preceds `description`, this means that it was added. 
