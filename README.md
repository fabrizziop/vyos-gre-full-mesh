# vyos-gre-full-mesh
GRE tunnel generator, for a set of routers to be fully meshed with each other.

Have you ever wanted to create a full mesh of GRE tunnels between a set of routers?. Even though this might be pointless?. No?. Well, then here you have a script to do just that!.

This can be used, for example, if you want the tunnel mesh to route IPv6 traffic over a v4-only core and for some reason you only have GRE tunnels to do the job.

You just have to fill in several values in the script:

`full_v6_address` - this must be a string with an uncompressed IPv6 address, the first five hextets (/80) will be used for the base addressing for the tunnels.
The next two hextets (/32) will indicate the tunnel ID and the last hextet will be reserved for the point to point addressing.

Example: `full_v6_address = "2001:0db8:fade:food:dead:0000:0000:0000"`

Next, you have to fill in `start_interface_number`, it must be an integer. It will indicate where the numbering scheme for the tunnel interfaces is starting.

Example: `start_interface_number = 100`, it means we will start numbering the tunnels from 100, the first tunnel will be `'tun101'`

Now, you have to fill in the router list. It will be a list containing a list for each router you want to be in the mesh.

Example: 
```
router_list = [
[True, "PAR1BR1", "172.17.10.11"],
[True, "NYC1BR1", "172.17.10.12"],
[True, "STL2BR2", "172.17.10.16"],
[True, "MIA1BR3", "172.17.10.17"]
]
```

The first value on each list is a boolean, if it is `True` it means we actually want to build tunnels to that router. 
If it is set to `False` the next two values do not matter, and we will just keep the entry as a placeholder. 

The second value is the router name, must be a string, and the third value is the router loopback/dummy IP which you are going to use to build the tunnels.

The tunnel numbering scheme is based on the order of the devices in router list, so it will be deterministic and remain the same for existing tunnels, if you add more nodes and run the tool again.

The tunnel number for each tunnel will be `start_interface_number + 2**a + 2**b`, where A and B are the positions of each router on the list.
As an example, tunnel between PAR1BR1 and STL2BR1 will be named `tun117` on both ends, as the position of "PAR1BR1" is 0 and "STL2BR1" is 4. `100 + 2**0 + 2**4 = 117`

If you are going to bring a router out of service then just set the value to `False` on it, to avoid removing it from the list and affecting the numbering of your other tunnels.

Last thing to do is to adjust function `generate_tunnel_config` to your requirements. I am just creating simple GRE tunnels with the MTU I need and adding them to OSPFv3.

Now, by running the script with the three mentioned sample values we will obtain the config for each router (indicated between brackets).

For my usecase this was more than enough after setting the IGP cost to what I needed - and this is how it works on AS203528 :) Maybe this will be useful for you.


```
['PAR1BR1']
set interfaces tunnel tun103 address 2001:0db8:fade:food:dead:0000:0067:1001/126
set interfaces tunnel tun103 description 'IPv6 Tunnel to NYC1BR1'
set interfaces tunnel tun103 encapsulation 'gre'
set interfaces tunnel tun103 ipv6 adjust-mss '1336'
set interfaces tunnel tun103 mtu '1396'
set interfaces tunnel tun103 parameters ip key '103'
set interfaces tunnel tun103 remote 172.17.10.12
set interfaces tunnel tun103 source-address 172.17.10.11
set protocols ospfv3 interface tun103 cost XXXXREPLACEMEXXXX
set protocols ospfv3 interface tun103 area 0
set protocols ospfv3 interface tun103 network 'point-to-point'
set interfaces tunnel tun105 address 2001:0db8:fade:food:dead:0000:0069:1001/126
set interfaces tunnel tun105 description 'IPv6 Tunnel to STL2BR2'
set interfaces tunnel tun105 encapsulation 'gre'
set interfaces tunnel tun105 ipv6 adjust-mss '1336'
set interfaces tunnel tun105 mtu '1396'
set interfaces tunnel tun105 parameters ip key '105'
set interfaces tunnel tun105 remote 172.17.10.16
set interfaces tunnel tun105 source-address 172.17.10.11
set protocols ospfv3 interface tun105 cost XXXXREPLACEMEXXXX
set protocols ospfv3 interface tun105 area 0
set protocols ospfv3 interface tun105 network 'point-to-point'
set interfaces tunnel tun109 address 2001:0db8:fade:food:dead:0000:006d:1001/126
set interfaces tunnel tun109 description 'IPv6 Tunnel to MIA1BR3'
set interfaces tunnel tun109 encapsulation 'gre'
set interfaces tunnel tun109 ipv6 adjust-mss '1336'
set interfaces tunnel tun109 mtu '1396'
set interfaces tunnel tun109 parameters ip key '109'
set interfaces tunnel tun109 remote 172.17.10.17
set interfaces tunnel tun109 source-address 172.17.10.11
set protocols ospfv3 interface tun109 cost XXXXREPLACEMEXXXX
set protocols ospfv3 interface tun109 area 0
set protocols ospfv3 interface tun109 network 'point-to-point'
-----
-----
['NYC1BR1']
set interfaces tunnel tun103 address 2001:0db8:fade:food:dead:0000:0067:1002/126
set interfaces tunnel tun103 description 'IPv6 Tunnel to PAR1BR1'
set interfaces tunnel tun103 encapsulation 'gre'
set interfaces tunnel tun103 ipv6 adjust-mss '1336'
set interfaces tunnel tun103 mtu '1396'
set interfaces tunnel tun103 parameters ip key '103'
set interfaces tunnel tun103 remote 172.17.10.11
set interfaces tunnel tun103 source-address 172.17.10.12
set protocols ospfv3 interface tun103 cost XXXXREPLACEMEXXXX
set protocols ospfv3 interface tun103 area 0
set protocols ospfv3 interface tun103 network 'point-to-point'
set interfaces tunnel tun106 address 2001:0db8:fade:food:dead:0000:006a:1001/126
set interfaces tunnel tun106 description 'IPv6 Tunnel to STL2BR2'
set interfaces tunnel tun106 encapsulation 'gre'
set interfaces tunnel tun106 ipv6 adjust-mss '1336'
set interfaces tunnel tun106 mtu '1396'
set interfaces tunnel tun106 parameters ip key '106'
set interfaces tunnel tun106 remote 172.17.10.16
set interfaces tunnel tun106 source-address 172.17.10.12
set protocols ospfv3 interface tun106 cost XXXXREPLACEMEXXXX
set protocols ospfv3 interface tun106 area 0
set protocols ospfv3 interface tun106 network 'point-to-point'
set interfaces tunnel tun110 address 2001:0db8:fade:food:dead:0000:006e:1001/126
set interfaces tunnel tun110 description 'IPv6 Tunnel to MIA1BR3'
set interfaces tunnel tun110 encapsulation 'gre'
set interfaces tunnel tun110 ipv6 adjust-mss '1336'
set interfaces tunnel tun110 mtu '1396'
set interfaces tunnel tun110 parameters ip key '110'
set interfaces tunnel tun110 remote 172.17.10.17
set interfaces tunnel tun110 source-address 172.17.10.12
set protocols ospfv3 interface tun110 cost XXXXREPLACEMEXXXX
set protocols ospfv3 interface tun110 area 0
set protocols ospfv3 interface tun110 network 'point-to-point'
-----
-----
['STL2BR2']
set interfaces tunnel tun105 address 2001:0db8:fade:food:dead:0000:0069:1002/126
set interfaces tunnel tun105 description 'IPv6 Tunnel to PAR1BR1'
set interfaces tunnel tun105 encapsulation 'gre'
set interfaces tunnel tun105 ipv6 adjust-mss '1336'
set interfaces tunnel tun105 mtu '1396'
set interfaces tunnel tun105 parameters ip key '105'
set interfaces tunnel tun105 remote 172.17.10.11
set interfaces tunnel tun105 source-address 172.17.10.16
set protocols ospfv3 interface tun105 cost XXXXREPLACEMEXXXX
set protocols ospfv3 interface tun105 area 0
set protocols ospfv3 interface tun105 network 'point-to-point'
set interfaces tunnel tun106 address 2001:0db8:fade:food:dead:0000:006a:1002/126
set interfaces tunnel tun106 description 'IPv6 Tunnel to NYC1BR1'
set interfaces tunnel tun106 encapsulation 'gre'
set interfaces tunnel tun106 ipv6 adjust-mss '1336'
set interfaces tunnel tun106 mtu '1396'
set interfaces tunnel tun106 parameters ip key '106'
set interfaces tunnel tun106 remote 172.17.10.12
set interfaces tunnel tun106 source-address 172.17.10.16
set protocols ospfv3 interface tun106 cost XXXXREPLACEMEXXXX
set protocols ospfv3 interface tun106 area 0
set protocols ospfv3 interface tun106 network 'point-to-point'
set interfaces tunnel tun112 address 2001:0db8:fade:food:dead:0000:0070:1001/126
set interfaces tunnel tun112 description 'IPv6 Tunnel to MIA1BR3'
set interfaces tunnel tun112 encapsulation 'gre'
set interfaces tunnel tun112 ipv6 adjust-mss '1336'
set interfaces tunnel tun112 mtu '1396'
set interfaces tunnel tun112 parameters ip key '112'
set interfaces tunnel tun112 remote 172.17.10.17
set interfaces tunnel tun112 source-address 172.17.10.16
set protocols ospfv3 interface tun112 cost XXXXREPLACEMEXXXX
set protocols ospfv3 interface tun112 area 0
set protocols ospfv3 interface tun112 network 'point-to-point'
-----
-----
['MIA1BR3']
set interfaces tunnel tun109 address 2001:0db8:fade:food:dead:0000:006d:1002/126
set interfaces tunnel tun109 description 'IPv6 Tunnel to PAR1BR1'
set interfaces tunnel tun109 encapsulation 'gre'
set interfaces tunnel tun109 ipv6 adjust-mss '1336'
set interfaces tunnel tun109 mtu '1396'
set interfaces tunnel tun109 parameters ip key '109'
set interfaces tunnel tun109 remote 172.17.10.11
set interfaces tunnel tun109 source-address 172.17.10.17
set protocols ospfv3 interface tun109 cost XXXXREPLACEMEXXXX
set protocols ospfv3 interface tun109 area 0
set protocols ospfv3 interface tun109 network 'point-to-point'
set interfaces tunnel tun110 address 2001:0db8:fade:food:dead:0000:006e:1002/126
set interfaces tunnel tun110 description 'IPv6 Tunnel to NYC1BR1'
set interfaces tunnel tun110 encapsulation 'gre'
set interfaces tunnel tun110 ipv6 adjust-mss '1336'
set interfaces tunnel tun110 mtu '1396'
set interfaces tunnel tun110 parameters ip key '110'
set interfaces tunnel tun110 remote 172.17.10.12
set interfaces tunnel tun110 source-address 172.17.10.17
set protocols ospfv3 interface tun110 cost XXXXREPLACEMEXXXX
set protocols ospfv3 interface tun110 area 0
set protocols ospfv3 interface tun110 network 'point-to-point'
set interfaces tunnel tun112 address 2001:0db8:fade:food:dead:0000:0070:1002/126
set interfaces tunnel tun112 description 'IPv6 Tunnel to STL2BR2'
set interfaces tunnel tun112 encapsulation 'gre'
set interfaces tunnel tun112 ipv6 adjust-mss '1336'
set interfaces tunnel tun112 mtu '1396'
set interfaces tunnel tun112 parameters ip key '112'
set interfaces tunnel tun112 remote 172.17.10.16
set interfaces tunnel tun112 source-address 172.17.10.17
set protocols ospfv3 interface tun112 cost XXXXREPLACEMEXXXX
set protocols ospfv3 interface tun112 area 0
set protocols ospfv3 interface tun112 network 'point-to-point'

```
