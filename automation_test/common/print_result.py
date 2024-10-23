#!/usr/bin/python
from time import sleep
import sys
import config
import restart_board
import control_board

def func_fail(self):
    if (config.RESTART_IF_FAILED == False):
        print "\n \n" +  config.FAIL_MEG
    else:
        print "\n \n Retest"

    sleep(0.5)
    self.buff=""

    if (config.RESTART_IF_FAILED == True):
        print ("\n \n Restart board")
        sys.stdout.flush()
        
        if (config.FEATBOX == True):
            control_board.restart()
        else:
            self.send('reboot',0,False)

        TIME_OUT=0
        while(self.buff.find('login:')==-1):
            sleep(0.5)
            TIME_OUT=TIME_OUT+1
            if (TIME_OUT > 240):
                break

        self.send('\n',0,False)

    restart_board.after_boot(self)

    self.serial.close()
    exit(0)
    
def func_pass(self):
    print "\n \n" + config.PASS_MEG
    self.serial.close()
    exit(0)

def wrong_env(self):
    print "\nWrong environment!"
    print "\n " + config.SKIP_MEG
    self.serial.close()
    exit(0)

