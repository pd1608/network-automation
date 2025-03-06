#!/usr/bin/env python3
'''This python code is used to parse a csv file having device SSH configurations and make a nested dictionary(see help resources) for each device IP address(key)
and its corresponding attributes(values) such as username, password, device type. Importing this dictionary to our main python file would make it easier
for us to call the attributes

expected output(nested dictionary):

{'198.51.100.1': {'username': 'pranav', 'password': 'pranav123', 'devicetype': 'cisco_ios'}, '198.51.100.3': {'username': 'pranav', 'password': 'pranav123', 'devicetype': 'cisco_ios'}}


'''

def devicedict(path):

    device = {}    #initialized a blank dictionary
    try:        #using try except block for error handling
        with open(path, "r") as sshfile:        #user will have to define the path for the csv file to be parsed
            for line in sshfile:
                values=line.strip().split(",")          #converting the lines of the csv file into a list of elements with ":" as the separator

                #creating a nested dictionary with the split 
                device[values[0]] = {
                    "username": values[1],
                    "password" : values[2],
                    "device_type" : values[4],
                    "ip" : values[3],
                    "secret" : values[5],
                    "host" : values[0]
                    }
       
       #   for debugging
        #print(device) 
    except:
        print("Error opening file. Check if file path exists and CSV text formatting")

    return(device)

    

#for checking and debugging

#if __name__=="__main__":
   #devicedict("sshinfo.csv")




     