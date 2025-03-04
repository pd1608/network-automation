#!/usr/bin/env python3
import re #good to use but should prefably use split and strip 
import subprocess  #awesome library for linux OS command integration
def main():
    
    oid = ["1.3.6.1.2.1.1.4.0", "1.3.6.1.2.1.1.5.0", "1.3.6.1.2.1.1.6.0", "1.3.6.1.2.1.2.1.0", "1.3.6.1.2.1.1.3.0"]
    
    print("SNMP version 1")
    print("********")
    

    for i in oid:
        result = subprocess.run(f"snmpget -v 1 -c public 198.51.100.3 {i}", shell=True, capture_output=True, text=True)
        output = result.stdout
        
        split_output = output.split("=")
        parameter = split_output[0].split("::")[-1].strip()
        value=split_output[1].split("STRING:")[-1].strip()
        final_parameter = parameter.split(".")[0].strip()
        print(f"{final_parameter} : {value}") 
        

    
    print("")
    print("SNMP version 2")
    print("********")

    for i in oid:
        result = subprocess.run(f"snmpget -v 2c -c public 198.51.100.4 {i}", shell=True, capture_output=True, text=True)
        output = result.stdout
        
        split_output = output.split("=")
        parameter = split_output[0].split("::")[-1].strip()
        value=split_output[1].split("STRING:")[-1].strip()
        final_parameter = parameter.split(".")[0].strip()
        print(f"{final_parameter} : {value}") 

    print("") 
    print("SNMP version 3")
    print("********") 


    for i in oid:
        result = subprocess.run(f"snmpget -v3 -u pranav -l authPriv -a sha -A pranav123 -x AES -X pranav123 198.51.100.5 {i}", shell=True, capture_output=True, text=True)
        output = result.stdout
        
        split_output = output.split("=")
        parameter = split_output[0].split("::")[-1].strip()
        value=split_output[1].split("STRING:")[-1].strip()
        final_parameter = parameter.split(".")[0].strip()
        print(f"{final_parameter} : {value}")     
  


    

if __name__=="__main__":
    main()

    