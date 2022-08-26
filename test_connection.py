#!/usr/bin/python3

#Modules
from netmiko import ConnectHandler #network devices connection
import os
import sys
import json
import getpass #Passwork mask

#Repository for files backup
root_dir = 'C:/Users/chambert_l/Documents/network-automation'
devices_file = root_dir +'/switch_cisco_all.json'
output_file = root_dir + '/connection.txt'

#Variables for authentification
password = getpass.getpass('adminradiall password= ')

#Devices file opening
with open (devices_file) as json_file:
    devices_tab = json.load(json_file)
    #Read of each device 
    for device in devices_tab['devices_list']:
        #Dictionnary for ConnectHandler
        device_connected = {
                'device_type': 'cisco_s300',
                'host': device['ip'],
                'username': 'adminradiall',
                'password': password,
        }
       
        #Connection
        try:
            connection = ConnectHandler(**device_connected)
        except:
            print('connection failed to ' + device['hostname'] + ' ' + device['ip'])
            continue

	# Close the connection
        connection.disconnect()
