#!/usr/bin/env python
#https://gist.github.com/gxfxyz/48072a72be3a169bc43549e676713201#file-dahua_rpc-py
from dahua_rpc import DahuaRpc

host = "192.168.100.208"
username = "admin"
password = "admin"

dahua = DahuaRpc(host, username, password)
print(f"Attempting to log into {host} with {username}:{password}")
dahua.login()
print(f"Correctly logged in at {dahua.current_time()}")
selection = input("Do you really want to reboot the device? (y/n) \n").lower()
if selection == 'y':
    print("Rebooting...")
    dahua.reboot()
    exit()

print("Goodbye")
exit()