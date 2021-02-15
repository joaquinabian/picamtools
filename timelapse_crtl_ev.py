#!/usr/bin/python3
#
# modified from
# https://github.com/carolinedunn/timelapse/blob/master/timelapse.py
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
path ='/home/pi/timelapse_4'
photo = os.path.join(path, 'image{0:06d}.jpg')
report = '#=%3i SS=%7i FR=%7.3f BR=%.1f, EV=%2i'
#
tlapse_min = 320       #time (min) to run your timelapse camera
interval_s = 5        #delay (seconds) between each photo taken
#
numphotos = int((tlapse_min * 60) / interval_s)     #number of photos to take
print("number of photos to take = ", numphotos)
#
dateraw = datetime.datetime.now()
datetimeformat = dateraw.strftime("%Y-%m-%d_%H:%M")
print("RPi started taking photos for your timelapse at: " + datetimeformat)
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
cam.shutter_speed = 0
auto = True
ev = 0
new_ev = 0
#
for i in range(numphotos):
    print(report % (i, cam.exposure_speed, cam.framerate, brghtnss, cam.exposure_compensation))
    current = photo.format(i)
    cam.capture(current)
    im = Image.open(current)
    brghtnss = np.mean(im) 
    #
    if brghtnss < 100:
        new_ev = int (24.4 - ( 24 * brghtnss / 100))
    else:
        new_ev = 0
    #
    if new_ev != ev:
        ev = new_ev
        cam.exposure_compensation = ev
    
    sleep(interval_s)
#
cam.stop_preview()
#
print("Done taking photos.")
