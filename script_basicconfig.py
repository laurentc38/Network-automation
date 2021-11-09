#!/usr/bin/python3
"""
--------------------------------------
Script for network automation for configuration
version 1.0 create by Laurent CHAMBERT 
--------------------------------------
"""
#Required device network configuration:
#User creation
#IP address configuration
#SSH activation

#Modules
from netmiko import ConnectHandler #network devices connection
import os
import json
import getpass #Passwork mask

#Repository
root_dir = '/home/user-ansible/network-automation/python/'
devices_file = root_dir+'switch.json'
conf_dir = root_dir+'conf-dir/'
config_commands = root_dir+'config_commands.txt'

#Variables for authentification
print('Enter identification connexion: ')
username = input('username connexion= ')
#print('Enter username password=')
password = getpass.getpass('username password= ')
#print('Enter enable password=')
enable = getpass.getpass('enable password=')

#Devices file opening
with open (devices_file) as json_file:
    devices_tab = json.load(json_file)
    #Read of each device 
    for device in devices_tab['devices_list']:
        #Dictionnary for ConnectHandler
        device_connect = {
                'device_type': 'cisco_ios',
                'host': device['ip'],
                'username': 'user-ansible',
                'password': 'ansible',
                'secret': 'enable'
        }

        #Connection
        try:
            net_connect = ConnectHandler(**device_connect)
        except:
            continue

        #Enable mode
        net_connect.enable()

        #Conf mode
        net_connect.config_mode()
        
        #Command's sending
        output = net_connect.send_config_from_file(config_commands)
        print('\nConfiguration of '+device['hostname']+':')
        print(output)

        #Record configuration
        net_connect.exit_config_mode()
        net_connect.send_command_expect('write')
        #If it's a router, confirm 
        if device['hostname'] == 'router':
            net_connect.send_command('enter')

        #Check configuration
        output_runningconfig = net_connect.send_command("show running-config")
        print(output_runningconfig)

	# Close the connection
        net_connect.exit_config_mode()
        net_connect.exit_enable_mode()
        net_connect.disconnect()