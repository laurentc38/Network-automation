#Script for device autodection

from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_dispatcher import ConnectHandler
import getpass #Passwork mask

#Variables for authentification
print('Enter identification connexion: ')
username = input('username connexion= ')
#print('Enter username password=')
password = getpass.getpass('username password= ')
#print('Enter enable password=')
#enable = getpass.getpass('enable password=')

#Parameter setting device_type is set to autodetect here
remote_device = {'device_type': 'autodetect',
                 'host': '10.31.50.186',
                 'username': username,
                 'password': password}

#Automatic detection
guesser = SSHDetect(**remote_device)
best_match = guesser.autodetect()

#Debug output of detection results
print("device_type: " + best_match)

#Automatically detected device_Reset type
remote_device['device_type'] = best_match
connection = ConnectHandler(**remote_device)

#Output of command execution result
print(connection.send_command('show version'))

#Disconnect
connection.disconnect()