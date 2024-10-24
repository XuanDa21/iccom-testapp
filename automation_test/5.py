#!/usr/bin/python
from time import sleep
import sys
import os
sys.path.append(os.path.relpath('common/'))
import conserial
import print_result
import config
import restart_board

if __name__ == '__main__':
    a=conserial.serial_thread(config.SERIAL_PORT,1, config.MODULE_TEST)
    a.start()
    a.send("insmod iccom.ko")
    for i in range(8):
        a.send("iccom-test -s 2000 -b 1 -c {} -n 2".format(i))
    a.send("rmmod iccom.ko")
    print_result.func_pass(a)
