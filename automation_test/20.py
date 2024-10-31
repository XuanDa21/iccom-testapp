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
    print_result.print_item(a,4,"SystemEvaluation")
    a.send("modprobe iccom")
    a.send("./OGLES3Navigation3D &")
    a.send("./OGLES3Navigation3D &")
    a.send("./OGLES3Navigation3D &")
    a.send("modprobe -a mmngr mmngrbuf vspm_if vsp2 vspm uvcs_drv")
    a.send("gst-launch-1.0 filesrc location=RENESAS_COCKPIT_ImageVideo_1920x1080_60fps.mp4 ! qtdemux ! queue ! h264parse  ! omxh264dec ! waylandsink &")
    a.send("gst-launch-1.0 filesrc location=RENESAS_COCKPIT_ImageVideo_1920x1080_60fps.mp4 ! qtdemux ! queue ! h264parse  ! omxh264dec ! waylandsink &")
    for i in range(8):
        a.send(f"iccom-test -s 2048 -n 1000 -c {i}")
    a.send("rmmod iccom.ko")
    print_result.func_pass(a)
