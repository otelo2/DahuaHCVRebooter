#!/usr/bin/env python
#https://gist.github.com/gxfxyz/48072a72be3a169bc43549e676713201#file-dahua_rpc-py
import itertools
import threading
import time
import sys
from dahua_rpc import DahuaRpc, RebootDone
from Ping import ping

host = "192.168.100.208"
username = "admin"
password = "admin"
done = False

def firstReboot():
    dahua = DahuaRpc(host, username, password)
    print(f"Attempting to log into {host} with {username}:{password}")
    dahua.login()
    print(f"Correctly logged in at {dahua.current_time()}")
    selection = input("Do you really want to reboot the device? (y/n) ").lower()
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
            #Note: This has an error margin of about 9 to 2 seconds.
            waiting = 85
            print(f"Waiting {waiting} seconds for the DVR to reboot...")
            #Start the waiting animation
            done = False
            t = threading.Thread(target=waitAnimation)
            t.daemon = True
            t.start()
            time.sleep(waiting)
            done = True
            timeEnd = time.time()
            print(f"DVR is (probably) back online after {timeEnd-timeStart} seconds")
            #Login again and try to reboot
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
        #Note: This has an error margin of about 9 to 2 seconds.
        waiting = 85
        print(f"Waiting {waiting} seconds for the DVR to reboot...")
        #Start the waiting animation
        done = False
        t = threading.Thread(target=waitAnimation)
        t.daemon = True
        t.start()
        time.sleep(waiting)
        done = True
        timeEnd = time.time()
        print(f"DVR is back online after {timeEnd-timeStart} seconds")
        print("Remember to ctrl + C to stop rebooting :)")
        DOS_reboot()

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
    firstReboot()
    print("Goodbye")

if __name__ == "__main__":
    main()