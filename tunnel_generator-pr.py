full_v6_address = "2001:0db8:fade:food:dead:0000:0000:0000"
#                                           XXXX:XXXX: Tunnel ID
#                                                     XXXX: Will be 1001 for first router, 1002 for second router

#first value is if the router exists
#if you decommission a node but want to keep it in the "order" then just set it to False.

#secomd value is the router name

#third value is the loopback IP which will be used for tunnel source
#idea is to keep it IPv4 only - I am building tunnels to carry IPv6 over IPv4 core

router_list = [
[True, "PAR1BR1", "172.17.10.11"],
[True, "NYC1BR1", "172.17.10.12"],
[True, "STL2BR2", "172.17.10.16"],
[True, "MIA1BR3", "172.17.10.17"]
]

start_interface_number = 100
#expanding config list...

config_list = [[[router[1]]] for router in router_list]

#now actually making the configuration

#for each router in the router list (Except the last one)

def generate_two_hextets(tunnel_id):
    hexbase = "0"*(8-len(str(hex(tunnel_id))[2:]))+str(hex(tunnel_id))[2:]
    return hexbase[0:4]+":"+hexbase[4:8]

def generate_tunnel_config(router_parameter_a,router_parameter_b, tunnel_id, ipv6_address_base, is_first_node):
    ipv6_end = "1001" if is_first_node == True else "1002"
    remote_name = router_parameter_b[1] if is_first_node == True else router_parameter_a[1]
    source_address = router_parameter_a[2] if is_first_node == True else router_parameter_b[2]
    destination_address = router_parameter_b[2] if is_first_node == True else router_parameter_a[2]
    tunnel_name = "tun" + str(tunnel_id)
    ipv6_twohextets = generate_two_hextets(tunnel_id)
    config_to_return = []
    config_to_return.append("set interfaces tunnel "+tunnel_name+" address "+ipv6_address_base[:25]+ipv6_twohextets+":"+ipv6_end+"/126")
    config_to_return.append("set interfaces tunnel "+tunnel_name+" description "+"'IPv6 Tunnel to "+remote_name+"'")
    config_to_return.append("set interfaces tunnel "+tunnel_name+" encapsulation 'gre'")
    config_to_return.append("set interfaces tunnel "+tunnel_name+" ipv6 adjust-mss '1336'")
    config_to_return.append("set interfaces tunnel "+tunnel_name+" mtu '1396'")
    config_to_return.append("set interfaces tunnel "+tunnel_name+" parameters ip key '"+str(tunnel_id)+"'")
    config_to_return.append("set interfaces tunnel "+tunnel_name+" remote "+destination_address)
    config_to_return.append("set interfaces tunnel "+tunnel_name+" source-address "+source_address)
    config_to_return.append("set protocols ospfv3 interface "+tunnel_name+" cost XXXXREPLACEMEXXXX")
    config_to_return.append("set protocols ospfv3 interface "+tunnel_name+" area 0")
    config_to_return.append("set protocols ospfv3 interface "+tunnel_name+" network 'point-to-point'")
    return config_to_return


for i in range(len(router_list)-1):
    #print("current router",i)
    #the code will iterate on all the remaining routers starting from that one... 
    #and build the tunnel config for both itself and its pair. 
    #the tunnel identifier will depend on the router numbers itself...
    #so if you keep adding routers here and just rerun the tool, the existing tunnels will remain the same.
    
    
    #if the current router is to be skipped, then do so.
    if router_list[i][0] == False:
        continue
    for j in range(i+1, len(router_list)):
        #if the destination router is to be skipped, then do so.
        if router_list[j][0] == False:
            continue
        tunnel_id = start_interface_number + 2**(i) + 2**(j)
        
        #now we should only be working with valid router pairings: I and J.
        #print(i, j, tunnel_id)
        
        #generating the config of the first router
        tunnel_config_a = generate_tunnel_config(router_list[i],router_list[j], tunnel_id, full_v6_address, True)
        #generating the config of the second router

        tunnel_config_b = generate_tunnel_config(router_list[i],router_list[j], tunnel_id, full_v6_address, False)
        config_list[i].extend(tunnel_config_a)
        config_list[j].extend(tunnel_config_b)
        #[print(line) for line in tunnel_config_b]

for router_config in config_list:
    print("-----")
    [print(line) for line in router_config]
    print("-----")