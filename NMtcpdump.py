#!/usr/bin/env python3

from scapy.all import rdpcap,Ether, IPv6



#def checkmacadd(pcapfile, ip1, ip2):

def ipv6_to_mac(ipv6_add):
    int_id = ipv6_add.split(":")[-4:]
    eui64 = "".join(int_id)

    mac1 = eui64[:6]
    mac2= eui64[10:]
    mac = f"{mac1[:2]}:{mac2[2:4]}:{mac1[4:]}:{mac2[:2]}:{mac2[2:4]}:{mac2[4:]}"

    mac_bytes = bytes.fromhex(mac.replace(":",""))
    modified_mac_bytes=bytearray(mac_bytes)
    modified_mac_bytes[0] ^= 0x02

    modified_mac = ":".join(f"{byte:02x}" for byte in modified_mac_bytes)
    return modified_mac

def checkmacadd(pcapfile):
    capture = rdpcap(pcapfile)

    mac_addr = []
    

    for packet in capture:
        if packet.haslayer('IPv6') and packet.haslayer('ICMPv6EchoRequest'): 
            a = packet[IPv6].src
            

            mac = ipv6_to_mac(a)
            if mac not in mac_addr:
                mac_addr.append(mac)
    print(f'devices detected in capture:')       
    
    for n, i in enumerate(mac_addr):
        print(f'{n+1}] {i}')
    
    return(mac_addr)
            

    
    
           

if __name__ == "__main__":
    # checkmacadd("midtermcapture.pcap", "10.0.1.3", "10.0.1.2")
    checkmacadd("midtermcapturev6.pcap")
