#!/usr/bin/python3
from time import sleep
import sys
import os
sys.path.append(os.path.relpath('common/'))
from conserial import SerialThread
import print_result
import config
import restart_board
commands = (
    "iccom-test -c 0 -n 2048 -s 2048 & "
    "iccom-test -c 1 -n 2048 -s 2048 & "
    "iccom-test -c 2 -n 2048 -s 2048 & "
    "iccom-test -c 3 -n 2048 -s 2048 & "
    "iccom-test -c 4 -n 2048 -s 2048 & "
    "iccom-test -c 5 -n 2048 -s 2048 & "
    "iccom-test -c 6 -n 2048 -s 2048 & "
    "iccom-test -c 7 -n 2048 -s 2048 & "
)

if __name__ == '__main__':
    a=SerialThread(config.SERIAL_PORT,1, config.MODULE_TEST)
    a.start()
    print_result.print_item(a,6,"Normal")
    restart_board.execute(a)
    a.send("modprobe iccom")
    a.send(commands, 0.001, False)
    sleep(120)
    a.send("\x03")
    sleep(0.01)
    a.send("rmmod iccom.ko")
    print_result.func_pass(a)
