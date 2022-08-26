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
#Repository for files backup
root_dir = 'C:/Users/chambert_l/Documents/network-automation'
devices_file = root_dir +'/switch_hp.json'
hp_commands = root_dir +'/config/hp_commands.txt'

#Variables for authentification
password = getpass.getpass('adminradiall password= ')

#Devices file opening
with open (devices_file) as json_file:
    devices_tab = json.load(json_file)
    #Read of each device 
    for device in devices_tab['devices_list']:
        #Dictionnary for ConnectHandler
        device_connect = {
                'device_type': 'hp_comware',
                'host': device['ip'],
                'username': 'adminradiall',
                'password': password,
                'session_log': 'hp_log.txt', #log file to resolved issue
        }

        #Connection
        try:
            connection = ConnectHandler(**device_connect)
        except:
            #Check connection
            print(' /!\ connection failed to ' + device['hostname'] + ' ' + device['ip'] + ' /!\ ')
            continue
        
        #Check connection
        print('# connection successful to ' + device['hostname'] + ' ' + device['ip'] + ' #')

        #Conf mode
        connection.config_mode()
        
        #Command's sending
        output = connection.send_config_from_file(hp_commands)
        print('\nConfiguration of '+device['hostname']+':')
        print(output)

        #Record configuration
        connection.exit_config_mode()
        connection.send_command_expect('save force')
        #If it's a router, confirm 
        if device['hostname'] == 'router':
            connection.send_command('enter')

        #Check configuration
        output_runningconfig = connection.send_command("display current-configuration")
        print(output_runningconfig)

	# Close the connection
        connection.disconnect()