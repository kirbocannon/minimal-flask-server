# Lab 4: Linux containers on NX-OS

**Ensure bash shell feature is enabled on the nexus switch:**  
```
N9K-A-Pod6# config terminal
N9K-A-Pod6(config) feature bash-shell
```

**Start Docker services:**  
Ensure the docker services are started. We will run a bash command from NXOS by using the `run bash` command. `sudo su` is used to log in as root user.
```
switch# run bash sudo su
root@switch# service docker start
root@switch# service docker status
```

**Add docker to appropriate run levels for persistence:**   
```
root@switch# chkconfig --add docker
chkconfig --list | grep docker
```

**Create the docker container:**    
```
bash-4.3# docker run --name=alpinerun -v /var/run/netns:/var/run/netns:ro,rslave --rm --network host --cap-add SYS_ADMIN -it alpine
```

`run` - run a command in a new container   
`--name` - name of the container  
`-v` - volumn to mount to   
`--rm` - automatically remove container when it exits  
`--network` - network name for the host to be added to. The default network is `default`  
`--cap-add` - add linux system capabilities. For example `SYS_ADMIN` - will allow certain rights such as mounting/unmounting drives. Here for more information: http://man7.org/linux/man-pages/man7/capabilities.7.html  
`i` - interactive (keep STDIN open)  
`t` - Allocate a pseudo-TTY  

**Docker will attempt to find the container image locally, if it cannot, it will download the latest image:**  
```
Unable to find image 'alpine:latest' locally
latest: Pulling from library/alpine
9d48c3bd43c5: Pull complete
Digest: sha256:72c42ed48c3a2db31b7dafe17d275b634664a708d901ec9fd57b1529280f01fb
Status: Downloaded newer image for alpine:latest
```

**You should now be in the docker container, run `ip addr` and see the docker interface:**  
```
/ # ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: tunl0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN
    link/ipip 0.0.0.0 brd 0.0.0.0
3: gre0@NONE: <NOARP> mtu 1476 qdisc noop state DOWN
    link/gre 0.0.0.0 brd 0.0.0.0
4: gretap0@NONE: <BROADCAST,MULTICAST> mtu 1462 qdisc noop state DOWN qlen 1000
    link/ether 00:00:00:00:00:00 brd ff:ff:ff:ff:ff:ff
5: ip6tnl0@NONE: <NOARP> mtu 1452 qdisc noop state DOWN
    link/tunnel6 00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00 brd 00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00
6: ip6gre0@NONE: <NOARP> mtu 1448 qdisc noop state DOWN
    link/[823] 00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00 brd 00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00
7: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP100> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 00:50:56:84:d7:b0 brd ff:ff:ff:ff:ff:ff
    inet 192.168.16.110/24 brd 192.168.16.255 scope global eth1
       valid_lft forever preferred_lft forever
8: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
    link/ether 02:42:dd:6c:b0:09 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 scope global docker0
       valid_lft forever preferred_lft forever
```

**Anything in this docker container is `contained` and will be destroyed immediately upon exit:**  
```
touch myTest
exit
```

**Create the docker container again:**  
`bash-4.3# docker run --name=alpinerun -v /var/run/netns:/var/run/netns:ro,rslave --rm --network host --cap-add SYS_ADMIN -it alpine`

`run` - run a command in a new container  
`--name` - name of the container  
`-v` - volumn to mount to  
`--rm` - automatically remove container when it exits  
`--network` - network name for the host to be added to. The default network is `default`  
`--cap-add` - add linux system capabilities. For example `SYS_ADMIN` will allow certain rights such as     mounting/unmounting drives. Here for more information: http://man7.org/linux/man-pages/man7/capabilities.7.html
`i` - interactive (keep STDIN open)  
`t` - Allocate a pseudo-TTY  

**Look for the `myTest` file you created previously:**  
`/ # ls -la`

**You should not see the `myTest` file, as it was destroyed with the container:**  
```
.           .dockerenv  dev         home        media       opt         root        sbin        sys         usr
..          bin         etc         lib         mnt         proc        run         srv         tmp         var
```

**Exit the docker container:**  
`/ # exit`

**View docker images**:  
`bash-4.3# docker images` 

**You should see the `alpine` image you've downloaded:**  
```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
alpine              latest              961769676411        5 weeks ago         5.58 MB
```