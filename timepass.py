import json
import time
import matplotlib.pyplot as plt
from easysnmp import Session
import subprocess

# Define SNMP credentials and router IPs
ROUTERS = {
    "R1": "10.0.2.1",
    "R2": "10.0.1.4",
    "R3": "10.0.1.5",
    "R4": "198.51.100.1",
    "R5": "10.0.1.1"
}

SNMP_COMMUNITY = "public"
SNMP_VERSION = 2

# OIDs
OID_IF_NAME = "1.3.6.1.2.1.2.2.1.2"  # Interface Name
OID_IPV4_ADDR = "1.3.6.1.2.1.4.20.1.1"  # IPv4 Address
OID_IPV4_IFINDEX = "1.3.6.1.2.1.4.20.1.2"  # IPv4 to Interface Index Mapping
OID_IPV6_ADDR = "1.3.6.1.2.1.55.1.8.1.2"  # IPv6 Address
OID_IPV6_IFINDEX = "1.3.6.1.2.1.55.1.8.1.1"  # IPv6 to Interface Index Mapping
OID_IF_STATUS = "1.3.6.1.2.1.2.2.1.8"  # Interface Status (1=up, 2=down)
OID_CPU_UTIL = "1.3.6.1.4.1.9.2.1.58.0"  # Cisco CPU Utilization (1-minute avg)

result = subprocess.run(f"snmpget -v2c -c public 10.0.1.1 ifName.1", shell=True, capture_output=True, text=True)
output = result.stdout

print(output)