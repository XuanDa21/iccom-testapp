#!/usr/bin/python3
import threading
import serial
import sys
import time
from time import sleep
import config
import print_result
import os
PLATFORM = config.PLATFORM

#---------------------------------------------------------#
_waited_time_out = 120  # if there is no data transferring, waitln() will break after time_out seconds.
#-------------------- global variables -------------------#
CStr_Expect = ''
_input_str = ''
_bytes_to_read = 0
_matched_result = 0
_start_time = time.time()
_serial = ''
# FAILED=1
# PASSED=0
time_out = 360

class SerialThread(threading.Thread):
    def __init__(self, com, has_print=1, module_test=""):
        threading.Thread.__init__(self)
        self.port_name = com
        self.has_print = has_print
        self.daemon = True
        self.port_err = False
        self.pause = False
        self.serial = serial.Serial()
        self.buff = ''
        if self.config(com) == False:
            exit(1)

        self.module_test = module_test

    def config(self, com):
        self.serial.baudrate = 115200
        self.serial.port = com
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.xonxoff = 0
        self.serial.write_timeout = None
        self.serial.timeout = None

        try:
            self.serial.open()
            self.port_err = False
            return True
        except Exception as e:
            print(f'Cannot open port {self.port_name}: {e}')
            self.port_err = True
            # Attempt to change permissions on the port
            try:
                os.system(f"sudo chmod 777 {self.port_name}")  # Set permissions to 777
                print(f'Permissions changed for {self.port_name}. Retrying...')
                
                # Retry opening the port
                self.serial.open()
                self.port_err = False
                return True
            except Exception as chmod_e:
                print(f'Failed to change permissions for {self.port_name}: {chmod_e}')
                return False

    def output_str(self, _input_str):
        if self.has_print == 0:
            return 0
        for i in _input_str:
            sys.stdout.write(str(i))
            sys.stdout.flush()
            if i == '\n':
                sys.stdout.flush()

    def run(self):
        if self.serial.isOpen():
            _bytes_to_read = self.serial.inWaiting()
            self.serial.read(_bytes_to_read)
            if self.port_err:
                return 1

        while self.serial.isOpen():
            _bytes_to_read = self.serial.inWaiting()
            if _bytes_to_read:
                data = self.serial.read(_bytes_to_read)
                self.output_str(data.decode('utf-8'))  # Decode bytes to string
                self.buff += data.decode('utf-8')  # Append the decoded string

            sleep(0.05)

    def wait_in_line(self, board_name):
        for i in range(1, 50):
            tmp = self.buff.splitlines()

            if len(tmp) == 0:
                sleep(0.5)
            else:
                if 'login:' in tmp[-1]:
                    sleep(0.25)
                    self.serial.write(b'root\n')
                    sleep(2)
                    self.buff = ""
                    self.serial.write(b'\n')
                    break
                if board_name in tmp[-1]:
                    break
                if ('nfs: server' in tmp[-1]) and ('not responding, still trying' in tmp[-1]):
                    sleep(4)
                else:
                    sleep(0.2)
        else:
            return False

        return True

    def send(self, command_str, time=0.005, next_command=True, TIMEOUT=1200, board_name="root@{}".format(PLATFORM)):
        sleep(0.1)

        if (command_str != '\x03') and (command_str != '\x1A'):
            self.serial.write(b'\n')
            if not self.wait_in_line(board_name):
                self.serial.write(b'\n')
                if not self.wait_in_line(board_name):
                    print("\nCannot send command to board!")
                    print_result.func_fail(self)

        sleep(0.1)

        for i in command_str:
            self.serial.write(i.encode('utf-8'))  # Encode the string to bytes
            sleep(time)
        self.serial.write(b'\r')

        sleep(0.1)
        tmp = self.buff.splitlines()
        TIME = 0

        if next_command:
            while (command_str in tmp[-1]) or (board_name not in tmp[-1] and 'ftp' not in tmp[-1]):
                sleep(0.2)
                tmp = self.buff.splitlines()

                if any(err in self.buff for err in ['Kernel panic', 'INFO: rcu_preempt self-detected stall on CPU', 'Unable to handle kernel paging request at virtual address']):
                    print_result.func_fail(self)

                if TIME > TIMEOUT * 5:
                    self.serial.write(b'\n')
                    tmp = self.buff.splitlines()
                    if board_name in tmp[-1]:
                        break
                    print_result.func_fail(self)

                TIME += 1

        sleep(0.1)

        return True

    def find_str(self, value, and_not_value=None):
        for line in self.buff.splitlines():
            if value in line:
                if and_not_value is None or and_not_value not in line:
                    return line
        return None

    def wait(self, value, timeout=600):
        TIME_OUT = 0
        while value not in self.buff:
            sleep(0.5)
            TIME_OUT += 1
            if TIME_OUT > timeout:
                return False
        return True


# Wait command

def wait(self, value, timeout=600):
    TIME_OUT = 0
    while value not in self.buff:
        sleep(0.5)
        TIME_OUT += 1
        if TIME_OUT > timeout:
            return False

    return True
