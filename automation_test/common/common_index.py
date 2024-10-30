#!/usr/bin/python
import sys
import re
from datetime import datetime
import os
import testcase
import subprocess
import config
summary_result = []

def num_TC(i):
    return str(i)

def execute_test(TC):
   
    global summary_result

    os.system('mkdir -p logs')
  
    print ('\n{})'.format(TC)) 
    sys.stdout.flush()

    start_time = datetime.now()
    print('Start test: {}\n'.format(start_time))
    print ('==[ {} ]============================'.format(testcase.list_TC[TC]))
    sys.stdout.flush()

    log_name = testcase.list_TC[TC].replace(' ','-')
    count=0

    try:    
        #H2P: Using subprocess.call instead of os.system to exit immediately when executing Ctrl+C
        subprocess.call('python3 {}.py  2>&1 | tee logs/tmp_{}.log'.format(num_TC(TC),num_TC(TC)),shell=True)
 
        with open('logs/tmp_{}.log'.format(num_TC(TC)),'r') as f:
            lines = f.readlines()
   
        for line in lines:
            result = re.search(r"#### Result: (.\S) ####$",line)

        if (result != None):
            result = line.split()[2]
        else:
            if (config.RESTART_IF_FAILED == True):
                while count < 2: #Retest 2 times when result is NG
                  subprocess.call('python3 {}.py  2>&1 | tee logs/tmp_{}.log'.format(num_TC(TC),num_TC(TC)),shell=True)
                  with open('logs/tmp_{}.log'.format(num_TC(TC)),'r') as f:
                      lines = f.readlines()
                  for line in lines:
                      result = re.search(r"#### Result: (.\S) ####$",line)
                  if (result != None):
                      result = line.split()[2]
                      break
                  else:
                      result = 'NG'
                  count += 1
                  if (count == 2):
                      print ("\n \n" +  config.FAIL_MEG)

        end_time = datetime.now()
        print('\nEnd test: {}'.format(end_time))
        print('\nTotal test time: {}'.format(end_time - start_time))
        sys.stdout.flush()

        if (result == 'NG'):
             summary_result.append("\033[31mTC {}: NG\033[0m".format(TC))
        else:
             summary_result.append("TC {}: {}".format(TC,result)) 
    ######################################
        subprocess.call('mv logs/tmp_{}.log logs/{}.log'.format(num_TC(TC),log_name),shell=True)

    except KeyboardInterrupt:
        print("\n----- Summary result ------\n")
        for result in summary_result:
            print(result)
        print('')
        sys.exit() 
    
def boot_board(option):
    os.system('mkdir -p logs')
    
    name = "boot"
    try:
        if (sys.argv[option+1] == '-n') or (sys.argv[option+1] == '-name'): 
            try:
                name = sys.argv[option+2]
            except:
                name = "boot"
    except:
        name = "boot" 
    os.system('python3 ../common/restart_board.py  2>&1 | tee logs/{}.log'.format(name)) 

    # Type 1: _index.py
    
def main():    
    if (len(sys.argv)==1):
        for i in testcase.list_TC:
            execute_test(i)
 
    # Type 2: index.py 1:2
   
    elif (len(sys.argv)==2) and (sys.argv[1].find(':')!=-1):

        BEGIN = int(sys.argv[1].split(':')[0])
        END = int(sys.argv[1].split(':')[1])
       
        for i in testcase.list_TC:
            if (i >= BEGIN) and (i <= END):
                execute_test(i)
 
    # Type 3: index.py 1 2 3

    else:
        for i in range(1,len(sys.argv)):
            if (sys.argv[i] == 'boot'):
                boot_board(i)
                exit(1)

            elif (sys.argv[i].find(':')!=-1):
                BEGIN = int(sys.argv[i].split(':')[0])
                END = int(sys.argv[i].split(':')[1])
                for j in testcase.list_TC:
                    if (j >= BEGIN) and (j <= END):
                        execute_test(j)

            elif int(sys.argv[i]) in testcase.list_TC:
                execute_test(int(sys.argv[i]))
    
    print("\n----- Summary result ------\n")
    for result in summary_result:
        print(result)
    print('')