#!/usr/bin/env python
#https://gist.github.com/gxfxyz/48072a72be3a169bc43549e676713201#file-dahua_rpc-py
import time
from dahua_rpc import DahuaRpc, RebootDone
from Ping import ping

host = "192.168.100.208"
username = "admin"
password = "admin"

def firstReboot():
    dahua = DahuaRpc(host, username, password)
    print(f"Attempting to log into {host} with {username}:{password}")
    dahua.login()
    print(f"Correctly logged in at {dahua.current_time()}")
    selection = input("Do you really want to reboot the device? (y/n) \n").lower()
    if selection == 'y':
        print("Rebooting...")
        timeStart = time.time()
        try:
            dahua.reboot()
        except RebootDone:
            print("DVR likely reboted!")
        
        #Check if the DVR has come online
        DOS = input("Do you want to keep rebooting the device? (y/n) ").lower()
        if DOS == "y":
            while(ping(host)==False):
                pass
            timeEnd = time.time()
            print(f"DVR is back online after {timeEnd-timeStart} seconds")
            DOS_reboot()
        else:
            print("Exiting reboot sequence")

def DOS_reboot():
    dahua = DahuaRpc(host, username, password)
    print(f"Attempting to log into {host} with {username}:{password}")
    dahua.login()
    print(f"Correctly logged in at {dahua.current_time()}")

    print("Rebooting...")
    timeStart = time.time()
    try:
        dahua.reboot()
    except RebootDone:
        print("DVR likely reboted!")
        
        #Check if the DVR has come online
        while(ping(host)==False):
            pass
        timeEnd = time.time()
        print(f"DVR is back online after {timeEnd-timeStart} seconds")
        print("Remember to ctrl + C to stop rebooting")
        DOS_reboot()
        

def main():
    firstReboot()
    print("Goodbye")

if __name__ == "__main__":
    main()