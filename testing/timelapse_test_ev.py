#!/usr/bin/python3
#
# modified from
# https://github.com/carolinedunn/timelapse/blob/master/timelapse.py
#
# esto solo sirve si no se está ya al máximo de exposicion =>
# o sea no sirve para sobreexponer en oscuro.
#
from picamera import PiCamera
from PIL import Image
import numpy as np
import os
import time
import datetime
import glob
from time import sleep
from fractions import Fraction
#
path ='/home/pi/timelapse_test_ev'
photo = os.path.join(path, 'image{0:06d}.jpg')
report = '#=%3i SS=%7i FR=%7.3f BR=%.1f, EV=%2i'
#
tlapse_min = 320       #time (min) to run your timelapse camera
interval_s = 10        #delay (seconds) between each photo taken
#
cam = PiCamera()
#cam.resolution = (1280, 720)
cam.resolution = (2028, 1520)
cam.sensor_mode = 3  
cam.iso = 800
cam.framerate = Fraction(5, 1000)
#
t0 = time.time()
#
if os.path.exists(path):
    kieres = input('quieres borrar el archivo (si/no) ?')
    if kieres == 'si':
        path_glob = os.path.join(path, '*.jpg')
        for arch in glob.glob(path_glob):
            os.remove(arch)
else:
    os.mkdir(path)
#   
sleep(max(0, 20 - (time.time()-t0)))
#
cam.start_preview(fullscreen=False, window=(895,300,1014,760)) 
#
brghtnss = 0
#
print('XM= ', cam.exposure_mode)
print('SM= ', cam.sensor_mode)
print('CI= ', cam.iso)
for i in range(1, 5):
    print(report % (i, cam.exposure_speed, cam.framerate, brghtnss, cam.exposure_compensation))
    current = photo.format(i)
    cam.capture(current)
    im = Image.open(current)
    brghtnss = np.mean(im) 
    sleep(interval_s)
#
cam.exposure_compensation = 24
sleep(20)
print('XM= ', cam.exposure_mode)
print('SM= ', cam.sensor_mode)
print('CI= ', cam.iso)
for i in range(5, 9):
    print(report % (i, cam.exposure_speed, cam.framerate, brghtnss, cam.exposure_compensation))
    current = photo.format(i)
    cam.capture(current)
    im = Image.open(current)
    brghtnss = np.mean(im) 
    sleep(interval_s)  
# 
print("Done taking photos.")
cam.stop_preview()
