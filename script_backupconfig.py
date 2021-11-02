#!/usr/bin/python3
"""
--------------------------------------
Script for network automation of
backup configuration
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
import time
import datetime
import json
import getpass #Passwork mask

#Repository for files backup
devices_file = '/home/user-ansible/network-automation/python/devices.json'
backuproot_dir = '/home/user-ansible/network-automation/python/backup-dir/'

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
                'username': username,
                'password': password,
                'secret': enable
        }
        #Repository backup
        backup_dir = backuproot_dir + device['hostname']
        backup_file = 'backup-conf_'+device['hostname'] + \
                      '_{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.cfg'

        #Connection
        try:
            net_connect = ConnectHandler(**device_connect)
        except:
            continue

        #Enable mode
        net_connect.enable()

	#Configuration output
        output_runningconfig = net_connect.send_command("show running-config")
	
	#Test du type de device
        if device['type'] == 'switch':
              vlan_file = 'backup-vlan_' + device['hostname'] + \
             '_{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.txt'
              output_vlan = net_connect.send_command("show vlan brief")

	#Folder creation for each device
        if not os.path.exists(backup_dir):
           os.makedirs(backup_dir)

	#Record running-config
        file1 = open(backup_dir+'/'+backup_file,'w')
        file1.write(output_runningconfig)
        file1.close()

        #Check the running-config record
        if os.path.isfile(backup_dir+'/'+backup_file):
                print(backup_file+' was recorded')
        else:
                print('backup file recording problem !')

        #Record vlan
        if device['hostname'][:2] == 'SW':
            file2 = open(backup_dir+'/'+vlan_file,'w')
            file2.write(output_vlan)
            file2.close()

        #Check the vlan record
        if os.path.isfile(backup_dir+'/'+vlan_file):
                print(vlan_file+' was recorded')
        else:
                print('vlan file recording problem !')

	# Close the connection
        net_connect.exit_enable_mode()
        net_connect.disconnect()

