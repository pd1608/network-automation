import time
import matplotlib.pyplot as plt
import json
from easysnmp import Session

DEVICES = {
    "R1": "10.0.2.1",
    "R2": "10.0.1.4",
    "R3": "10.0.1.5",
    "R4": "198.51.100.1",
    "R5": "10.0.1.1"
}

SNMP_COMMUNITY_STRING = "public"
SNMP_PROTOCOL_VERSION = 2

MIB_IF_DESCRIPTION = "IF-MIB::ifDescr"  
MIB_IPV4_ADDRESS = "IP-MIB::ipAdEntAddr"  
MIB_IPV4_IF_INDEX = "IP-MIB::ipAdEntIfIndex"  
# MIB_IPV6_ADDRESS = "IPV6-MIB::ipv6AddrAddress"  
# MIB_IPV6_IF_INDEX = "IPV6-MIB::ipv6AddrIfIndex"  
MIB_IF_OPER_STATUS = "IF-MIB::ifOperStatus"  

def retrieve_snmp_data(device_name, device_ip):
    try:
        session = Session(hostname=device_ip, community=SNMP_COMMUNITY_STRING, version=SNMP_PROTOCOL_VERSION)

        interface_descriptions = {}
        for entry in session.walk(MIB_IF_DESCRIPTION):
            interface_descriptions[entry.oid_index] = entry.value  # ifIndex -> Interface Name

        interface_status = {}
        for entry in session.walk(MIB_IF_OPER_STATUS):
            interface_name = interface_descriptions.get(entry.oid_index, f"Interface-{entry.oid_index}")
            interface_status[interface_name] = "Up" if entry.value == "1" else "Down"

        ipv4_addresses = {}
        ipv4_to_interface_map = {}
        for entry in session.walk(MIB_IPV4_ADDRESS):
            ipv4_addresses[entry.oid_index] = entry.value
        for entry in session.walk(MIB_IPV4_IF_INDEX):
            ipv4_to_interface_map[entry.oid_index] = entry.value

        # Get IPv6 Addresses and Interface Mapping (commented out)
        # ipv6_addresses = {}
        # ipv6_to_interface_map = {}
        # for entry in session.walk(MIB_IPV6_ADDRESS):
        #     ipv6_addresses[entry.oid_index] = entry.value
        # for entry in session.walk(MIB_IPV6_IF_INDEX):
        #     ipv6_to_interface_map[entry.oid_index] = entry.value

        # Create structured data
        device_data = {
            device_name: {
                "ip_addresses": {},
                "interface_status": interface_status
            }
        }

        for interface_index, interface_name in interface_descriptions.items():
            ipv4_address_list = [ip for idx, ip in ipv4_addresses.items() if ipv4_to_interface_map.get(idx) == interface_index]
            # ipv6_address_list = [ip for idx, ip in ipv6_addresses.items() if ipv6_to_interface_map.get(idx) == interface_index]

            if not ipv4_address_list:
                ipv4_address_list.append("N/A")
            # if not ipv6_address_list:
            #     ipv6_address_list.append("N/A")

            device_data[device_name]["ip_addresses"][interface_name] = {
                "ipv4": ipv4_address_list,
                # "ipv6": ipv6_address_list
            }

        return device_data

    except Exception as e:
        print(f"Error retrieving SNMP data from {device_name}: {e}")
        return None

all_device_data = {}
for device_name, device_ip in DEVICES.items():
    data = retrieve_snmp_data(device_name, device_ip)
    if data:
        all_device_data.update(data)

with open("router_data.txt", "w") as f:
    json.dump(all_device_data, f, indent=4)

print("SNMP data successfully saved to router_data.txt")



def monitor_cpu_utilization(router_ip, duration=120, interval=5):
    session = Session(hostname=router_ip, community='public', version=2)

    cpu_usage_data = []
    time_stamps = []
    start_time = time.time()
    OID_CPU_UTILIZATION = "1.3.6.1.4.1.9.2.1.58.0"

    while time.time() - start_time < duration:
        cpu_utilization_value = session.get(OID_CPU_UTILIZATION).value
        current_time = round(time.time() - start_time, 2)

        cpu_usage_data.append(float(cpu_utilization_value))
        time_stamps.append(current_time)

        print(f"Time: {current_time}s - CPU Usage: {cpu_utilization_value}%")
        time.sleep(interval)

#graph plotting
    plt.figure(figsize=(10, 6))
    plt.plot(time_stamps, cpu_usage_data, marker='x', linestyle='--', color='darkorange', label="CPU Usage")
    plt.xlabel("Time (seconds)", fontsize=12)
    plt.ylabel("CPU Use (%)", fontsize=12)
    plt.title(f"CPU Use for {router_ip}", fontsize=14)
    plt.legend(loc="upper right", fontsize=10)
    plt.grid(True, linestyle=':', color='gray')

    plt.savefig("cpu_utilization.jpg")
    print("CPU utilization graph saved as cpu_utilization.jpg")

# Run CPU monitoring for R1
monitor_cpu_utilization(DEVICES["R1"])
