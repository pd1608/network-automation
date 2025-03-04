#!/usr/bin/env python3
import sshinfo
from netmiko import ConnectHandler
import re
import NMtcpdump

def connect():
    # Load device information from the csv
    device = sshinfo.devicedict("sshinfo.csv")

    # Connect to R4
    r4 = device['R4']
    print(r4)

    # Connect to R5 (later populated with extracted r5ip)
    r5 = device['R5']
    print(r5)

    regex = r"ca05\.2623\.0000"  # Match specific IPv6 address
    noregex = r"FE80"  # Exclude lines with 'FE80'

    net_connect = ConnectHandler(**r4)
    net_connect.enable()

    # Get the output of 'show ipv6 neighbor'
    output = net_connect.send_command("sh ipv6 neighbor")
    print(output)

    # Extract R5's IP address
    r5ip = None
    for line in output.splitlines():
        if re.search(regex, line) and not re.search(noregex, line):
            r5ip = line.split(" ")[0]
            print(r5ip)
            break

    if not r5ip:
        print("Error: No matching IP found.")
        net_connect.disconnect()
        return

    print(f"R5 IP address: {r5ip}")
    net_connect.disconnect()

    # Prepare R5 connection dictionary
    r5 = {
        'username': 'pranav',
        'password': 'pranav123',
        'device_type': 'cisco_ios',
        'ip': r5ip,
        'secret': 'pranav123',
    }

    # Get MAC addresses from the pcap file
    mac_add = NMtcpdump.checkmacadd("midtermcapturev6.pcap")
    if len(mac_add) < 2:
        print("Error: Not enough MAC addresses found.")
        return

    # Convert MACs to client-identifier format (Cisco expects 0100.XXXX.XXXX)
    mac1 = f"01{mac_add[0].replace(':', '')}"
    mac2 = f"01{mac_add[1].replace(':', '')}"

    # Establish SSH connection to R5
    net_connect = ConnectHandler(**r5)
    net_connect.enable()

    # Define DHCP configuration commands
    commandstat1 = [
        "ip dhcp excluded-address 10.0.1.2",
        "ip dhcp pool NetmanStatic1",
        f"host 10.0.1.2 255.255.255.0",  # Corrected format
        f"client-identifier {mac1}", 
        "default-router 10.0.1.1"
    ]

    commandstat2 = [
        "ip dhcp pool NetmanStatic2",
        f"host 10.0.1.3 255.255.255.0",  # Corrected format
        f"client-identifier {mac2}", 
        "default-router 10.0.1.1"
    ]

    # Send commands properly using send_config_set()
    output1 = net_connect.send_config_set(commandstat1)
    print(output1)

    output2 = net_connect.send_config_set(commandstat2)
    print(output2)

    commandyn = [
        "ip dhcp pool NetmanDyn",
        "network 10.0.1.0 255.255.255.0"
    ]
    output = net_connect.send_config_set(commandyn)
    print(output)

    output = net_connect.send_command("sh ip dhcp binding")

    print("DHCPv4 IP addresses assigned: ")
    
    for line in output.splitlines()[2:]:
        a = line.split(" ")[0]
        print(a)

      #  print(f'{n+1}: {b}')

        
    #print(output)
    

    # Exit config mode and disconnect
    net_connect.exit_config_mode()
    net_connect.disconnect()

if __name__ == "__main__":
    connect()