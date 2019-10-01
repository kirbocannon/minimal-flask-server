# Lab 3: Using Python to enchance CLI commands

## Task 4: Add the EEM applet to monitor configuration
Cisco's EEM (Embedded Event Manager) runs in the background and can trigger scripts based on an action. In this case, we want a python script to trigger every time a network administrator issues the `copy running-config startup-config` command. 

**Connect to the student workstation:**  
`ssh student@172.16.66.100`

**Connect to the 9K Nexus switch `N9K-A-Pod6`:**     
`student@student-vm:~$ ssh admin@192.168.16.110`
 
 **Add EEM script to the switch's configuration**:  
 We will add an EEM script applet named `gitpush` that will invoke upon a network engineer saving the running configuration to startup. This will invoke a script called `update_git.py` that will push the new configuration to a git server (remote repository). This remote repository is the student jumphost.  

```
N9K-A-Pod6# configure terminal
N9K-A-Pod6(config)# event manager applet gitpush 
N9K-A-Pod6(config)# event cli match "copy running-config startup-config" 
N9K-A-Pod6(config)#  action 2 cli copy running bootflash:running.latest 
N9K-A-Pod6(config)#  action 3 cli guestshell run /home/admin/update_git.py 
N9K-A-Pod6(config)#  action 4 event-default 
N9K-A-Pod6(config)# end
```

**Save the running config to the startup configand save again:**
```
N9K-A-Pod6# copy running-config startup-config
[########################################] 100%
Copy complete, now saving to disk (please wait)...
Copy complete.
```

**Get into the guest shell and view the contents of the update_git.py script:**   
When the network administrator saves the running configuration to the startup configuration, EEM will kick off the `update_git.py` script which will automatically upload the configuration to the remote git repository. This is useful for tracking which changes were pushed and serves as a backup store for all configuration. 

```
N9K-A-Pod6# run guestshell
[admin@guestshell ~]$ cat update_git.py
#!/usr/bin/python

import os
import subprocess
from subprocess import call
from cisco import system

BASEDIR = os.path.dirname(os.path.realpath(__file__))
CFGDIR = os.path.join(BASEDIR, 'network_configs')
HOSTNAME = system.System().get_hostname()

if not os.path.isdir(CFGDIR):
    os.mkdir(CFG_DIR)

if not os.path.isdir(os.path.join(CFGDIR, HOSTNAME)):
    os.mkdir(os.path.join(CFGDIR, HOSTNAME))

os.chdir(CFGDIR)

call(["cp", "/bootflash/running.latest", "{}/{}/running.latest".format(CFGDIR, HOSTNAME)])
call(["git", "add", "{}/{}/running.latest".format(CFGDIR, HOSTNAME)])
call(["git", "commit", "-m", "Configuration change"])
p = subprocess.Popen(['chvrf', 'management', 'git', 'push'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()

with open(os.path.join(CFGDIR, 'output.log'), "a+") as f:
    f.write(out)
    f.write(err)
```

**Use `git log` to view past commits:**    
We will use `git log` in order to view past commits. Each commit is saved with a unique hash value which identifies the commited file(s) and saves the state of the file(s) at a particular point in time. There should be one or more commits at this point since you've saved the running configuration. 

```
[admin@guestshell ~]$ cd network_configs
[admin@guestshell network_configs]$ git log

commit e5a8c8c076a8bf8530b10868bd56127e613762e4
Author: git <git@gittest.com>
Date:   Sat Sep 28 01:00:29 2019 +0000

    Configuration change
```

`commit` - precedes the hash or commit ID. This makes the commit unique to any other commits. 
`Author` - the author who pushed this commit
`Date` - the date this commit was committed 
`Configuration change` is the commit message that was used during the commit push.  The commit message is hard coded within the python script so this will always be the same.
