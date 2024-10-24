#!/usr/bin/python
from time import sleep
import sys
import config
import conserial
import control_board
import re

def after_boot(a):
    if (a.module_test == "USB2F"):
        if (config.PLATFORM == "salvator-x"):
            a.send("echo e659c000.usb > /sys/bus/platform/drivers/renesas_usbhs/unbind",0.005,True,120)

    if (a.module_test == "SATA"):
        a.buff=""
        MOUNT_POINT = sata.mountpoint(a)

        DEVICE = re.findall(r'[A-Za-z]+|\d+', MOUNT_POINT)[0]

        a.send('(echo o; echo n; echo p; echo 1; echo 2048; echo "+5G"; echo Y; echo t; echo 83; echo w) | fdisk /dev/{}'.format(DEVICE))

        a.buff=""
        a.send('echo y | mkfs.ext4 -L "HD" /dev/{}1'.format(DEVICE))

        a.buff=""
        a.send('(echo n; echo p; echo 2; echo 10487808; echo "+5G"; echo Y; echo t; echo 2; echo 83; echo w) | fdisk /dev/{}'.format(DEVICE))

        a.buff=""
        a.send('echo y | mkfs.ext4 -L "HD" /dev/{}2'.format(DEVICE))

        a.buff=""
        a.send('fdisk -l /dev/{}'.format(DEVICE))

    if (a.module_test == "USB_HOST"):
        a.buff=""
        MOUNT_POINT = None
        MOUNT_POINT = usb.mountpoint(a,'usb2ch1')
        if (MOUNT_POINT != None):
            a.buff=""
            a.send('echo y | mkfs.ext4 -L "USB2-1" /dev/{}'.format(MOUNT_POINT))
        
        a.buff=""
        MOUNT_POINT = None
        MOUNT_POINT = usb.mountpoint(a,'usb2ch2')
        if (MOUNT_POINT != None):
            a.buff=""
            a.send('echo y | mkfs.ext4 -L "USB2-1" /dev/{}'.format(MOUNT_POINT))

        a.buff=""
        MOUNT_POINT = None
        MOUNT_POINT = usb.mountpoint(a,'usb3')
        if (MOUNT_POINT != None):
            a.buff=""
            a.send('echo y | mkfs.ext4 -L "USB2-1" /dev/{}'.format(MOUNT_POINT))

def main(a):

    #print('\n------------ BOARD -------------\n')
    sys.stdout.flush()

    if (config.FEATBOX == True):
        control_board.restart_2()
    else:
        print('\nPlease press switch to restart board \n')
        sys.stdout.flush()    
        
        TIME_OUT = 0
        for i in range (120,-1,-1):
  
            if (a.buff.find('NOTICE:  BL2:')!=-1):
                sleep(0.2)
                break
            print ('\033[F 00:00:{:02}'.format(i))
            sys.stdout.flush()
            sleep(1)
            TIME_OUT = TIME_OUT + 1
        
        if (TIME_OUT > 120):
            print('\n TIME OUT \n')
            sys.stdout.flush()
            a.serial.close()
            exit(0)        

    TIME_OUT=0
    count = 0
    while(a.buff.find('login:')==-1):
        sleep(0.5)
        TIME_OUT += 1
        if (TIME_OUT > 360): #nho la 360
            count += 1
            if (count <= 5): #nho la 5
                TIME_OUT = 0
                if (config.FEATBOX == True):
                    print('\nTry to restart board again {}\n'.format(count))
                    sys.stdout.flush()
                    control_board.restart()
                else:
                    break
            else:
                #a.send('\n',0,False)
                print('\nCannot boot board sucessfully')
                sys.stdout.flush()
                a.serial.close()
                exit(0)         

    a.send('\n',0,True,120)
    sleep(5)
    a.send('\n',0,True,120)
    after_boot(a)
    a.send('\n',0,False)

if __name__ == '__main__':

    MODULE_TEST=""
    if (len(sys.argv)==2):
	MODULE_TEST=sys.argv[1]
    a=conserial.serial_thread(config.SERIAL_PORT,1,MODULE_TEST)
    a.start()
    a.buff=""

    main(a)

    a.serial.close()

