# Lab 2: Using Python to enchance CLI commands

## Task 1: Running Python on NX-OS

**Connect to the student workstation:**  
`ssh student@172.16.66.100`

**Connect to the 9K Nexus switch `N9K-A-Pod6`:**    
`student@student-vm:~$ ssh admin@192.168.16.110` 

**Access the guest shell on the Nexus switch:**  
`N9K-A-Pod6# run guestshell`

**Start the python interpreter:**  
```
Python 2.7.5 (default, Apr  9 2019, 14:30:50) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-36)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

You are now in the python interpreter shell. You can run python code directly and get immediate feedback. At any time you want to quit, use the `exit()` function. 

In the shell, import a few modules provided by Cisco. Additionally, import the `json` module which is a standard library that comes with python. 
```
>>> from cli import cli, clid
>>> import json
```

**Use NXOS CLI commands within python to get operational output:**  
We will use `clid` function to print output in JSON. Not all commands support json output, but many of them do. Using `clid("show version")` is equivalent to the NXOS command `show version | json`

```
>>> show_version = clid("show version")
>>> print show_version
'{"header_str": "Cisco Nexus Operating System (NX-OS) Software\\nTAC support: http://www.cisco.com/tac\\nDocuments: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_series_home.html\\nCopyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved.\\nThe copyrights to certain works contained herein are owned by\\nother third parties and are used and distributed under license.\\nSome parts of this software are covered under the GNU Public\\nLicense. A copy of the license is available at\\nhttp://www.gnu.org/licenses/gpl.html.\\n\\nNexus 9000v is a demo version of the Nexus Operating System", "bios_ver_str": null, "kickstart_ver_str": "9.3(1)", "nxos_ver_str": "9.3(1)", "bios_cmpl_time": null, "kick_file_name": "bootflash:///nxos.9.3.1.bin", "nxos_file_name": "bootflash:///nxos.9.3.1.bin", "kick_cmpl_time": "7/18/2019 15:00:00", "nxos_cmpl_time": "7/18/2019 15:00:00", "kick_tmstmp": "07/19/2019 00:04:48", "nxos_tmstmp": "07/19/2019 00:04:48", "chassis_id": "Nexus9000 9000v Chassis", "cpu_name": "Intel(R) Xeon(R) Silver 4114 CPU @ 2.20GHz", "memory": "8163856", "mem_type": "kB", "proc_board_id": "9ZXEWDW4LSL", "host_name": "N9K-A-Pod6", "bootflash_size": "3509454", "kern_uptm_days": "3", "kern_uptm_hrs": "15", "kern_uptm_mins": "20", "kern_uptm_secs": "8", "rr_reason": "Unknown", "rr_sys_ver": null, "rr_service": null, "plugins": "Core Plugin, Ethernet Plugin", "manufacturer": "Cisco Systems, Inc.", "TABLE_package_list": {"ROW_package_list": {"package_id": null}}}'
```

We are storing the json output of `show version` to a variable that we can use later. Then, we are printing that variable to view the raw json data. 

We will now decode that json data so that we can easily access data within this object
```
>>> print json.loads(show_version)['memory']
8163856
```

`json.loads` decodes json so that we can access the data in a pythonic manner. This will change the json data to a python dictionary and data types that python understands. In this case, we are accessing the `memmory` key using bracket notation. This will display the total memory available to the switch; `8163856`.

**Import the cisco module and import the cisco.vlan module:**  
```
>>> import cisco
>>> from cisco.vlan import Vlan
```

**Print help for the `cisco` package:**  
`>>> help(cisco)`

**You should see the package submodules that are available under `package contents`. For instance, you will see the `vlan` module available. Get further help on this module:**  

```
>>> help(Vlan)

     |  
     |  parse_specific(self)
     |  
     |  rerun(self)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from cisco.nxcli.NXCLI:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class Vlan(__builtin__.object)
     |  Methods defined here:
     |  
     |  __init__(self)
     |  
     |  create_vlan(self, id, **args)
     |      create the vlan
     |      
     |      args:
     |          id        Vlan id
     |      
     |      optional args:
     |          name      Vlan description
     |          state     Vlan state
     |          mode      Vlan mode
     |          type      Vlan type
     |  
     |  delete_vlan(self, id)
     |      delete the vlan
     |      
     |      args:
     |          id        Vlan id
     |  
     |  show_vlan(self)
     |      return: Vlans configured on the switch
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

(END)
```

**This will display the `Vlan` class and it's available class methods. Press `q` to get out of help. Now, let's create a vlan by instantiating the `Vlan()` class, saving it to the `my_vlan` variable, and using the `create_vlan` method :**  

```
>>> my_vlan = Vlan()
>>> my_vlan.create_vlan(40, name="A NEW VLAN")
True
```

Here, we are setting an instance of an object (V) When creating a vlan, the module will return `True` if it was able to create a new vlan with no issues. 

**Try to create vlan `40` again, you should see an error that it already exists:**  
```
>>> my_vlan.create_vlan(40)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/isan/python/scripts/cisco/vlan.py", line 87, in create_vlan
    raise ValueError, 'Vlan %d already exists' % id
ValueError: Vlan 40 already exists
```
**View vlans on switch by using `print` and the `raw_output` method:**  

```
>>> print my_vlan.show_vlan().raw_output

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Po20, Eth1/2, Eth1/5, Eth1/6
                                                Eth1/7, Eth1/8, Eth1/9, Eth1/10
                                                Eth1/11, Eth1/12, Eth1/13
                                                <Omitted for breivety>
40   VLAN0040                         active    Po20, Eth1/2

VLAN Type         Vlan-mode
---- -----        ----------
1    enet         CE
40   enet         CE
```

**Pretty Print existing vlans in json:**  

Use the `json` module with the `dumps` method and `indent=4` argument to print json in a structure manner which is easier for a human to read.

```
>>> show_vlan = json.loads(clid("show vlan"))
>>> print json.dumps(show_vlan, indent=4)

{
    "TABLE_mtuinfo": {
        "ROW_mtuinfo": [
            {
                "vlanshowinfo-vlanid": "1",
                "vlanshowinfo-media-type": "enet",
                "vlanshowinfo-vlanmode": "ce-vlan"
            },
            {
                "vlanshowinfo-vlanid": "40",
                "vlanshowinfo-media-type": "enet",
                "vlanshowinfo-vlanmode": "ce-vlan"
            },
        ]
    },
    "TABLE_vlanbrief": {
        "ROW_vlanbrief": [
            {
                "vlanshowbr-vlanstate": "active",
                "vlanshowplist-ifidx": [
                    "port-channel20,Ethernet1/2,Ethernet1/5,Ethernet1/6,Ethernet1/7,Ethernet1/8,Ethernet1/9,Ethernet1/10,Ethernet1/11,Ethernet1/12
                ],
                "vlanshowbr-vlanid-utf": "1",
                "vlanshowbr-vlanname": "default",
                "vlanshowbr-vlanid": "1",
                "vlanshowbr-shutstate": "noshutdown"
            },
            {
                "vlanshowbr-vlanstate": "active",
                "vlanshowplist-ifidx": "port-channel20,Ethernet1/2",
                "vlanshowbr-vlanid-utf": "40",
                "vlanshowbr-vlanname": "VLAN0040",
                "vlanshowbr-vlanid": "40",
                "vlanshowbr-shutstate": "noshutdown"
            },
        ]
    }
}
```

**Delete a vlan by using the `delete_vlan` method:**  
```
[admin@guestshell ~]$ my_vlan.delete_vlan(40)
True
```

**Change the login banner:**  

We can change the login banner by using the system module and the `set_banner` method

```
>>> from cisco.system import System
```

**Set `system` variable as instance of `System()` class and use the `set_banner` method to set a new banner:**  
```
>>> system = System()
>>> system.set_banner("A NEW BANNER\n")
True
```

This returns a bollean, `True` if it successfully adds to configuration, `False` if otherwise. 

**Get system hostname:**  
```
>>> system.get_hostname()
'N9K-A-Pod6'
```
The `get_hostname()` method will return the current device's hostname as a string. 

**Create an ACL to restrict SSH access:**  
```
>>> from cisco.acl import IPv4ACL
>>> from cli import cli
>>> ssh_acl = IPv4ACL("ssh_acl")
>>> ssh_acl.permit("tcp", "192.168.0.0/16", "any", dport_quailifier="eq", dport=22)
True
```

The `IPv4ACL` class allows us to create/modify/delete access lists. IFirst, we set the variable `ssh_acl` to an instance of the `IPv4ACL` class. When we instantiate this object, we must also provide an ACL name, in this case it will be `ssh_acl`.  We then use the `permit()` method in order to add a new acl. 

**Apply ACL to VTY lines:**  
```
>>> cli("config t ;line vty ;access-class ssh_acl in")
```
