#!/usr/bin/env /usr/bin/python

# A dummy script to automatically execute the correct rsync command
# for copying ALBATROS data.  Looks for existence of external backup
# drive by default, but also gives an option to copy to the laptop.

import os
import subprocess

if __name__ == '__main__':

    # We have more than one year now!
    year = '2019'

    # Arbitrary # of external drive numbers to try
    ndrive = 4
    
    # Start by looking for existence of external drive
    dest = None
    for username in ['scihi','prizm']:
        for idrive in range(1, ndrive+1):
            extdrive = '/media/'+username+'/PRIZM_DISK'+str(idrive)
            if os.path.exists(extdrive):
                print('Detected external drive ', extdrive)
                extpath = extdrive+'/marion'+year
                ret = raw_input('Copy to external drive path '+extpath+'? (y/n) ')
                if ret.lower() == 'y':
                    dest = extpath
    # See if the human wants to copy to the laptop instead
    if dest is None:
        print('No external drive detected or selected')
        extpath = '/data/marion'+year
        ret = raw_input('Copy to laptop path '+extpath+'? (y/n) ')
        if ret.lower() == 'y':
            dest = extpath
        else:
            print('I have failed to find a path that makes you happy.')
            dest = raw_input('Enter the data destination path that you want. [e/E to escape] ')
            if dest.lower() == 'e':
                print('Goodbye...')
                exit(0)


    # This is the static IP set for all the enclosures. Change if necessary
    ip = '192.168.1.71'

    # Find out where to copy data from. 
    # PRIZM site, hostname ''
    # HYDROSHACK site, hostname ''
    # BASETEST, hostname 'albatross-2'


    print('Checking for connection to', ip)
    ret = os.system('ping -c 1 -W 2 ' + ip)
    if ret == 0:
        # Get output of remote command
        hostname = subprocess.check_output(['ssh', 'pi@'+ip, 'hostname'])
        # Get rid of \n at the end of the output
        hostname = hostname[0:-1]
        # Copy to subdirectory labelled with hostname
        dest = dest+'/'+hostname

        print('Found live connection to ', hostname, ': initializing data transfer')
        print('Copying data from ' + hostname)
        cmd = 'rsync -auv --ignore-existing --progress pi@'+ip+':/home/pi/data_auto_cross ' + dest
        print(cmd)
        os.system(cmd)
    else:
        print('Failed to detect connection to', ip)
