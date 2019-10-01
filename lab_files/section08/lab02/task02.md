# Lab 2: Using Python to enchance CLI commands

## Task 2: Enchance CLI output with Python
Run a python script that monitors and reformats CLI counters/CPU/memory usage to provide real-time resource 
information. Run the following command in the guest shell:

`[admin@guestshell ~]$ vi systemstatus.py`

```
#!/usr/bin/python
import os
import time
import datetime

print "Polling every 2 seconds. Press 'Ctrl + C' to quit"
cnt = 0
while True:
    cnt += 1
    time.sleep(2)
    mem = os.popen("free -h | grep 'Mem:' | awk '/[0-9]+/ {print $2, $7}'").read()
    mem = mem.split()
    mem = {'total': mem[0], 'free': mem[1]}
    os.popen("uptime").read()
    load_average = os.popen("uptime").read().split("load average:")[-1].strip()
    one_minute_load_average = load_average.split(',')[0]
    print ("{3} - Current memory usuage is {0}/{1} and the cpu load average over 1 minute is {2}").format(
        mem['free'], mem['total'],
        one_minute_load_average,
        cnt)
```

**Once the script is running, press 'Ctrl + C' to quit:**

```
[admin@guestshell ~]$ chmod +x systemstatus.py
[admin@guestshell ~]$ ./systemstatus.py
[admin@guestshell ~]$ ./systemstatus.py
Polling every 2 seconds. Press 'Ctrl + C' to quit
1 - Current memory usuage is 885M/7.8G and the cpu load average over 1 minute is 0.98
2 - Current memory usuage is 885M/7.8G and the cpu load average over 1 minute is 0.98
3 - Current memory usuage is 884M/7.8G and the cpu load average over 1 minute is 0.98
4 - Current memory usuage is 884M/7.8G and the cpu load average over 1 minute is 0.98
5 - Current memory usuage is 885M/7.8G and the cpu load average over 1 minute is 0.98

```