#!/usr/bin/python3
from time import sleep
import sys
import os
sys.path.append(os.path.relpath('common/'))
from conserial import SerialThread
import print_result
import config
import restart_board

if __name__ == '__main__':
    a=SerialThread(config.SERIAL_PORT,1, config.MODULE_TEST)
    a.start()
    print_result.print_item(a,5,"Normal")
    a.send("modprobe iccom")
    for i in range(8):
        a.send(f"iccom-test -s 2000 -b 1 -c {i} -n 2")
    a.send("rmmod iccom.ko")
    print_result.func_pass(a)
