#!/usr/bin/python3
"""
--------------------------------------
Script for network automation of
backup configuration
version 1.1 create by Laurent CHAMBERT 
***Modification***
1.0: original edition
1.1: split script for cisco and hp devices
1.2: 
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
import time
import datetime
import json
import getpass #Passwork mask

#Repository for files backup
root_dir = 'C:/Users/chambert_l/Documents/network-automation'
devices_file = root_dir +'/switch_cisco.json'
backuproot_dir = 'C:/Users/chambert_l/Documents/backup-dir'

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
                'session_log': 'cisco_log.txt', #log file to resolved issue
                'global_delay_factor': 1, #delay to avoid issue timing
        }
        #Repository backup
        backup_dir = backuproot_dir + '/' + device['hostname']
        backup_file = 'backup-conf_'+device['hostname'] + \
                      '_{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.cfg'

        #Connection
        try:
            net_connect = ConnectHandler(**device_connected)
        except:
            #Check connection
            print(' /!\ connection failed to ' + device['hostname'] + ' ' + device['ip'] + ' /!\ ')
            continue
        
        #Check connection
        print('# connection successful to ' + device['hostname'] + ' ' + device['ip'] + ' #')

	#Configuration output
        output = net_connect.save_config()
        output_runningconfig = net_connect.send_command("show running-config")
	
	#Test du type de device
        if device['type'] == 'switch':
              vlan_file = 'backup-vlan_' + device['hostname'] + \
             '_{0:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()) + '.txt'
              output_vlan = net_connect.send_command("show vlan")

	#Folder creation for each device
        if not os.path.exists(backup_dir):
           os.makedirs(backup_dir)

	#Record running-config
        file1 = open(backup_dir + '/' + backup_file,'w')
        file1.write(output_runningconfig)
        file1.close()

        #Check the running-config record
        if os.path.isfile(backup_dir+'/'+backup_file):
                print(backup_file+' was recorded')
        else:
                print('backup file recording problem !')

        #Record vlan
        if device['type'] == 'switch':
            file2 = open(backup_dir+'/'+vlan_file,'w')
            file2.write(output_vlan)
            file2.close()
        
        #Check the vlan record
        if device['type'] == 'switch':
                if os.path.isfile(backup_dir+'/'+vlan_file):
                        print(vlan_file+' was recorded')
                else:
                        print('vlan file recording problem !')

	# Close the connection
        net_connect.disconnect()
