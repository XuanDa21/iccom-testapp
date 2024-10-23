#!/usr/bin/python
import threading
import serial
import sys
import time
from time import sleep
import config
import print_result

PLATFORM=config.PLATFORM

#---------------------------------------------------------#
_waited_time_out = 120;  # if there is no data transferring, waitln() will break after time_out seconds.
#-------------------- global variables -------------------#
CStr_Expect = ''
_input_str = ''
_bytes_to_read = 0
_matched_result = 0
_start_time = time.time()
_serial = ''
#FAILED=1
#PASSED=0
time_out=360

class serial_thread(threading.Thread):
    def __init__(self,com,has_print=1,module_test=""):
        threading.Thread.__init__(self)
        self.port_name=''
        self.has_print=has_print
        self.daemon=True
        self.port_err=False
        self.pause=False
        self.serial = serial.Serial()
        self.buff=''
        if self.config(com)==False:
            exit(1)

        self.module_test=module_test

    def config(self,com):
        self.serial.baudrate = 115200
        self.serial.port = com
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.xonxoff = 0
        self.serial.timeout = 358
        #self.serial.rtscts=True
        #self.serial.dsrdtr=True

        try:
            self.serial.open()
            self.port_err = False
            return True
        except:
            print 'cannot open port %s'% self.port_name
            self.port_err=True
            return False

    def output_str(self,_input_str):
        if self.has_print==0:
            return 0
        for i in _input_str:
            sys.stdout.write(i)
            sys.stdout.flush()
            if i == '\n':
                # sys.stdout.write('[' + datetime.datetime.now().strftime("%a %b %d %H:%M:%S.%f %Y") + '] ')
                sys.stdout.flush()

    def run(self):
        if (self.serial.isOpen()):
            _bytes_to_read = self.serial.inWaiting()
            self.serial.read(_bytes_to_read)
            if self.port_err:
                return 1

        while self.serial.isOpen():
            _bytes_to_read = self.serial.inWaiting()
            if _bytes_to_read:
                    data=self.serial.read(_bytes_to_read)
                    self.output_str(data)
                    self.buff =self.buff+data

            sleep(0.05)

    def wait_in_line(self,board_name):
        for i in range(1, 50):
                tmp = self.buff.splitlines()

                if (len(tmp)==0):
                    sleep(0.5)
                else:
                    if (tmp[len(tmp)-1].find('login:')>-1):
                       sleep(0.25)
                       self.serial.write('root\n')
                       sleep(2)
                       self.buff=""
                       self.serial.write('\n')
                       break
                    if (tmp[len(tmp)-1].find(board_name)>-1):
                       break
                    if (tmp[len(tmp)-1].find('nfs: server')>-1) and (tmp[len(tmp)-1].find('not responding, still trying')>-1):
                       sleep(4)
                    else:
                        sleep(0.2)
        else:
            return False

        return True

    def send(self,str,time=0.005,next_command=True,TIMEOUT=1200,board_name="root@{}".format(PLATFORM)):
        sleep(0.1)
        #self.buff=""

        if (str != '\x03') and (str != '\x1A'):

            self.serial.write('\n')
            if (self.wait_in_line(board_name) == False):
                self.serial.write('\n')    
                if (self.wait_in_line(board_name) == False):
                    print("\nCannot send command to board!")
                    print_result.func_fail(self)

        sleep(0.1)

        for i in str:
            self.serial.write(i)
            sleep(time)
        self.serial.write('\r')
     
        sleep(0.1)
        tmp = self.buff.splitlines()
        
        TIME=0

        if (next_command == True):
            while (tmp[len(tmp)-1].find(str)!=-1) \
              or ( (tmp[len(tmp)-1].find(board_name)==-1) and (tmp[len(tmp)-1].find('ftp')==-1)):
                 sleep(0.2)
                 tmp = self.buff.splitlines()
                 
                 if (self.buff.find('Kernel panic')!=-1) \
                   or (self.buff.find('INFO: rcu_preempt self-detected stall on CPU')!=-1) \
                   or (self.buff.find('Unable to handle kernel paging request at virtual address')!=-1):
                     print_result.func_fail(self)

                 if (TIME > TIMEOUT*5):
                     self.serial.write('\n')
                     tmp = self.buff.splitlines()
                     if (tmp[len(tmp)-1].find(board_name)!=-1): 
                         break
                     print_result.func_fail(self)
                 
                 TIME = TIME + 1     
                            
        sleep(0.1)
 
        return True
   
    def find_str(self,value,and_not_value=None):
    
        for i in (self.buff.splitlines()):
            if (i.find(value)!=-1):
                if (and_not_value == None):
                    return i
                else:
                    if (i.find(and_not_value)==-1):
                        return i
        
        return None

    def wait(self,str,timeout=600):
        TIME_OUT = 0
        while (self.buff.find('{}'.format(str))==-1):
           sleep(0.5)
           TIME_OUT = TIME_OUT + 1
           if (TIME_OUT > timeout):
               return False

        return True
        
   # def func_fail(self):
   #     print "\n \n" +  FAIL_MEG
   #     sleep(0.5)
   #     self.buff=""
   #     print ("\n \n Restart board")
        #control_board.restart()
        #while(self.buff.find('login:')==-1):
        #    sleep(0.5)

   #     self.serial.close()
   #     exit(0)
    
   # def func_pass(self):
   #     print "\n \n" + PASS_MEG
   #     self.serial.close()
   #     exit(0)

# Wait command

def wait(self,str,timeout=600):
   
       TIME_OUT = 0
       while (self.buff.find('{}'.format(str))==-1):
           sleep(0.5)
           TIME_OUT = TIME_OUT + 1
           if (TIME_OUT > timeout): 
               return False
       
       return True
