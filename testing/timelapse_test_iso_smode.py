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
path ='/home/pi/timelapse_test'
#
tlapse_min = 320       #time (min) to run your timelapse camera
interval_s = 10        #delay (seconds) between each photo taken
fps = 30               #frames per second timelapse video
#
numphotos = int((tlapse_min * 60) / interval_s)     #number of photos to take
print("number of photos to take = ", numphotos)
#
dateraw = datetime.datetime.now()
datetimeformat = dateraw.strftime("%Y-%m-%d_%H:%M")
print("RPi started taking photos for your timelapse at: " + datetimeformat)
#
report = '%i SS=%7i FR=%7.3f'
#
cam = PiCamera()
cam.resolution = (1280, 720)
#
cam.start_preview(fullscreen=False, window=(0,0,400,400))
#
if os.path.exists(path):
    path_glob = os.path.join(path, '*.jpg')
    for arch in glob.glob(path_glob):
        os.remove(arch)
else:
    os.mkdir(path)
    
photo = os.path.join(path, 'image{0:06d}.jpg')
#
print('XM= ', cam.exposure_mode)
print('SM= ', cam.sensor_mode)
print('CI= ', cam.iso)
for i in range(1, 5):
    print(report % (i, cam.exposure_speed, cam.framerate))
    cam.capture(photo.format(i))
    sleep(interval_s)
#
cam.sensor_mode = 3
sleep(20)
print('XM= ', cam.exposure_mode)
print('SM= ', cam.sensor_mode)
print('CI= ', cam.iso)
for i in range(5, 9):
    print(report % (i, cam.exposure_speed, cam.framerate))
    cam.capture(photo.format(i))
    sleep(interval_s)
#    
cam.iso = 800
sleep(20)
print('XM= ', cam.exposure_mode)
print('SM= ', cam.sensor_mode)
print('CI= ', cam.iso)
for i in range(9, 13):
    print(report % (i, cam.exposure_speed, cam.framerate))
    cam.capture(photo.format(i))
    sleep(interval_s)    
#
cam.iso = 1600
sleep(20)
print('XM= ', cam.exposure_mode)
print('SM= ', cam.sensor_mode)
print('CI= ', cam.iso)
for i in range(13, 17):
    print(report % (i, cam.exposure_speed, cam.framerate))
    cam.capture(photo.format(i))
    sleep(interval_s)    
#
cam.iso = 1600
cam.framerate = Fraction(5, 1000)
sleep(20)
print('XM= ', cam.exposure_mode)
print('SM= ', cam.sensor_mode)
print('CI= ', cam.iso)
for i in range(17, 21):
    print(report % (i, cam.exposure_speed, cam.framerate))
    cam.capture(photo.format(i))
    sleep(interval_s)
    
cam.iso = 1600
cam.framerate = Fraction(5, 1000)
cam.exposure_mode = 'night'
sleep(20)
print('XM= ', cam.exposure_mode)
print('SM= ', cam.sensor_mode)
print('CI= ', cam.iso)
for i in range(17, 21):
    print(report % (i, cam.exposure_speed, cam.framerate))
    cam.capture(photo.format(i))
    sleep(interval_s)
# 
print("Done taking photos.")
cam.stop_preview()
