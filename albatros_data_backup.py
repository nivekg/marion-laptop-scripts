#!/usr/bin/env /usr/bin/python

# A dummy script to automatically execute the correct rsync command for backing up data.
# Looks for existence of 5TB data drives and 8TB backup drives
# List all 5TB drives as a source
# Treats all 8TB drives as a targer


import os
from time import sleep

# There a EIGHT 5TB Hard Drives
srcNum = 8 
# There a EIGHTEEN 8TB Hard Drives
destNum = 18 


def locateSourceDrive():
    # Start by looking for existence of external 5TB data drive
    source = []
    for sourcedrive in range(1, srcNum+1):
        # Look for drive in this directory assuming the drive is labelled as ALBATROS_5TB_DISK#
        drive = '/media/prizm/ALBATROS_5TB_DISK'+str(sourcedrive)
        if os.path.exists(drive):
            # If drive exists, add it to the list of sources
            print('Detected external 5TB data drive ', drive)
            sleep(2)
            source.append(drive)
    return source

def locateTargetDrive():
    for targetdrive in range(1, destNum+1): 
        # Look for drive in this directory assuming the drive is labelled as ALBATROS_DISK#
        target = '/media/prizm/ALBATROS_DISK'+str(targetdrive)
        if os.path.exists(target):
            # If drive exists, return the directory
            return target
    return None

if __name__ == '__main__':
    source = locateSourceDrive()
    if len(source) == 0:
        # No 5TB drives were found
        print('5TB hard drive was not found. Exiting....')
        exit()
    else:
        while True:
            target = locateTargetDrive()
            ret_code = -1

            # Check if a target drive was found
            if target is not None:
                # A 8TB drive was found
                print('Detected external backup drive ', target)
                sleep(2)
                # Copy from all the data sources to the target
                print('=======================================================')
                print('Copying data from '+' '.join(source)+' to '+target)
                print('=======================================================')
                sleep(5)
                # Execute rsync command to copy from 5TB to 8TB
                ret_code = os.system('rsync -auv --ignore-existing --progress '+' '.join(source)+'  '+target)
            else:
                # No external drive found
                print('=======================================================')
                ret = raw_input('No 8TB drive found. Please plug in a drive then press \'c\' to continue: ')
                if ret.lower() == 'c':
                    continue
                else:
                    print('\'c\' was not pressed. Exiting.....')
                    exit()

            # Check return code to determine is the 'rsync' command was successful
            if ret_code == 0:
                # Copying complete
                print('Done copying!')
                exit()
            elif ret_code == 2816:
                # Error code (2816): No more space in target
                # Try another drive
                print('=======================================================')
                ret = raw_input('Ran out of space. Remove current 8TB drive and enter another one then press \'c\' to continue: ')
                if ret.lower() == 'c':
                    continue
                else:
                    print('\'c\' was not pressed. Exiting.....')
                    exit()
            else:
                print('Backup failed with the rsync error code: '+str(ret_code)+ '. See \'man rsync\' for more')
                exit()
