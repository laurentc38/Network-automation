#!/usr/bin/python3
"""
--------------------------------------
Script for network automation for configuration
version 1.1 create by Laurent CHAMBERT 
***Modification***
1.0: original edition
1.1: split script for cisco and hp devices
--------------------------------------
"""
#Required device network configuration:
#User creation
#IP address configuration
#SSH activation

#************ CISCO DEVICES ************

#Modules
from netmiko import ConnectHandler #network devices connection
import os
import json
import getpass #Passwork mask

#Repository
root_dir = 'C:/Users/chambert_l/Documents/network-automation'
devices_file = root_dir+'/switch_cisco.json'
cisco_commands = root_dir+'/config/cisco_commands.txt'

#Variables for authentification
password = getpass.getpass('adminradiall password= ')

#Devices file opening
with open (devices_file) as json_file:
    devices_tab = json.load(json_file)
    #Read of each device 
    for device in devices_tab['devices_list']:
        #Dictionnary for ConnectHandler
        device_connect = {
                'device_type': 'cisco_s300',
                'host': device['ip'],
                'username': 'adminradiall',
                'password': password,
                'session_log': 'cisco_log.txt', #log file to resolved issue
                'global_delay_factor': 1, #delay to avoid issue timing
        }

        #Connection
        try:
            net_connect = ConnectHandler(**device_connect)
        except:
            #Check connection
            print(' /!\ connection failed to ' + device['hostname'] + ' ' + device['ip'] + ' /!\ ')
            continue
        
        #Check connection
        print('# connection successful to ' + device['hostname'] + ' ' + device['ip'] + ' #')
        
        #Command's sending
        #output = net_connect.send_config_from_file(cisco_commands)
        output = net_connect.send_command("show version")

        #Yes answers if needed
        if 'Are you sure you' in output:
            output += net_connect.send_command_timing('Y')
        
        #Record configuration
        output += net_connect.save_config()
        
        #Cleans-up output
        print()
        print('\nConfiguration of '+device['hostname']+':')
        print(output)

	# Close the connection
        net_connect.disconnect()