#!/usr/bin/env python3

import sshinfo
import ipv4check
import connectivity
import bgp
import json
import concurrent.futures as cf
import sshinfo
import subprocess
from netmiko import ConnectHandler
import sys

def main():
    deviceinformation = sshinfo.devicedict("sshinfo.csv")
    print(deviceinformation)


    ip_address = []
    print("IP address check.....")
    for i in deviceinformation.values():
        ip_address.append(i['ip'])
    
    print(ip_address)

    for j in ip_address:
       checkop = ipv4check.ipv4check(j)
      # print(f'checkop is {checkop}')
       checkop
       if isinstance(checkop, str) and "Invalid" in checkop:  
        print("Invalid IP address.....Exiting process")
        sys.exit()
       
    print("")
    print("Connectivity check.....")

    for k in ip_address:
        connectivity.pingtest(k)


    print("")
    print("BGP configuration....")

    devices = []
    for i in deviceinformation.values():
       devices.append(i)
    #print(devices)



##MULTIPROCESSING
    #First read the bgp.conf file 
    #Write a parallel loop with bgp.bgp 
    with open("bgp.conf", "r") as file:
        file_json = json.load(file)

    bgp_config_details = file_json['Routers']

    max_workers = 2 

    with cf.ThreadPoolExecutor(max_workers=max_workers) as executor:
       futures = []
       for device_conn_details, device_bgp_config in zip(devices, bgp_config_details.values()):
            executor.submit(bgp.bgp(device_conn_details, device_bgp_config))


    #bgp.bgp(device,"bgp.conf")

    

    bgp.neighborcheck(devices)
    bgp.routecheck(devices)
    bgp.runconfig(devices, "running_config.txt")
    bgp.updateconf(devices, "bgp.conf")
       
    
    ##pingtest
    print("\nPing test to all loopback IP address")

    loopback = ["10.10.10.1","11.11.11.1","20.20.20.1","22.22.22.1"]
    
    for i in deviceinformation.values():
        net_connect = ConnectHandler(**i)
        net_connect.enable()
        for j in loopback:
            output = net_connect.send_command(f"ping {j}")
            print(output)
    

    
        

    

            

    
    

        
        
    
    



if __name__=="__main__":
    main()

