#!/usr/bin/python
from time import sleep
import sys
import os
sys.path.append(os.path.relpath('common/'))
import conserial
import print_result
import config
import restart_board

def print_item(a, n):
    print("\n\n----------Item {}----------\n".format(n))
    sys.stdout.flush()
    a.buff = ""

if __name__ == '__main__':
    a=conserial.serial_thread(config.SERIAL_PORT,1, config.MODULE_TEST)
    a.start()
    # restart_board.main(a)
    # a.send("dmesg")
    a.send("insmod iccom.ko")
    a.send("iccom-abnormal-test -t 5 -c 0")
    a.send("rmmod iccom.ko")
    print_result.func_pass(a)
