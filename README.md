Network automation v1.0 (2021/11/02)

License: GNU v3.0
Script to improve configuration and backup on network devices

New:
Initial release

###Requires:###
Python3:3.8.2
Netmiko=2.4.2

###Testing lab###
GNS3 2.2.17
Switch: Cisco IOS software vios_l2 version 15.2
Router: Cisco IOS software 7200 version 15.2

###Script use###
---before script used---
Your device must be configured with:
-user with admin privileged
-ip address which must be reachable
-ssh connexion
-modify the repository for files and recording
---backup script---
Create you device.json file with you network devices
---basicconfig script---
Create your device.json for each device type
Write your commands in config_commands.txt
