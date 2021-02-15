#!/usr/bin/python3
#
# modified from
# https://github.com/carolinedunn/timelapse/blob/master/timelapse.py
#
from picamera import PiCamera
import os
import datetime
import glob
from time import sleep
from fractions import Fraction
#
report = '%2i XS=%8i FR=%7.3f'
#
cam = PiCamera()
#cam.resolution = (1280, 720)
cam.resolution = (2028, 1520)
#
cam.sensor_mode = 3  
cam.iso = 800
#cam.exposure_mode = 'night'
cam.framerate = Fraction(1, 5)
cam.shutter_speed = 1_000_000
#
cam.start_preview(fullscreen=False, window=(895,300,1014,760))
#
print('XM= ', cam.exposure_mode)
print('SM= ', cam.sensor_mode)
print('CI= ', cam.iso)
print('CR= ', cam.resolution)
#
i = 0
while True:
    print(report % (i, cam.exposure_speed, cam.framerate))
    sleep(5)
    i += 1
# 
print("Done taking photos.")
cam.stop_preview()