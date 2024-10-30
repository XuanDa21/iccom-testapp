#!/usr/bin/python3
from time import sleep
import sys
import config
import control_board

def execute(a):
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


