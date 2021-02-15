#!/usr/bin/python3
#
# with nikon lens 24 mm f 2
# set at f8 and focus 0.7 m
# iso 800
#
from picamera import PiCamera
from PIL import Image
import numpy as np
import os
import time
import datetime
import glob
from fractions import Fraction
#
path ='/home/pi/sunrise'
photo = os.path.join(path, 'image{0:06d}.jpg')
REPORT = '#=%4i HM=%8s SS=%7i FR=%7.3f BR=%.1f'
#
tlapse_min = 360       # duration (min) of timelapse
interval_s = 5         # delay (seconds) between captures
start = (13, 6)        # time (day, h) to start 
#
numphotos = int((tlapse_min * 60) / interval_s)     # number of photos to take
print("number of photos to take = ", numphotos)
#
def chek_start(start):
    while True:
        dateraw = datetime.datetime.now()
        hour = dateraw.hour
        print(hour, end=' ')
        if dateraw.day == start[0]:
            if hour >= start[1]:
                print('')
                datetimeformat = dateraw.strftime("%Y-%m-%d_%H:%M")
                return (datetimeformat)
        #
        time.sleep(300)
#
def get_time():
    dateraw = datetime.datetime.now()
    return ('%2i:%2i:%2i' % (dateraw.hour, dateraw.minute, dateraw.second))
#
def check_path(path):
    if os.path.exists(path):
        kieres = input('quieres borrar el archivo (si/no) ?')
        if kieres == 'si':
            path_glob = os.path.join(path, '*.jpg')
            for arch in glob.glob(path_glob):
                os.remove(arch)
    else:
        os.mkdir(path)

#
if __name__ == '__main__':

    date = check_start(start)
    print("Timelapse started at: %s" + date)
    #
    cam = PiCamera()
    cam.resolution = (2028, 1520)
    cam.sensor_mode = 3  
    cam.iso = 800
    cam.framerate = Fraction(1, 10)
    #
    t0 = time.time()
    check_path(path)
    sleep(max(0, 20 - (time.time()-t0)))
    #
    cam.start_preview(fullscreen=False, window=(895,300,1014,760))    
    #
    brghtnss = 0
    auto = True
    ss = 0
    new_ss = 99_999
    for i in range(numphotos):
        print(REPORT % (i, get_time(), cam.exposure_speed,
                        cam.framerate, brghtnss))
        current = photo.format(i)
        cam.capture(current)
        im = Image.open(current)
        brghtnss = np.mean(im)
        #
        if brghtnss < 50:
            new_ss += 50_000
            new_ss = min(1_000_000, new_ss)
        elif brghtnss > 150:
            new_ss -= 50_000
            if new_ss < 100_000:
                new_ss = 0
        #
        if abs(new_ss - ss) > 8_000:
            ss = new_ss
            cam.shutter_speed = ss
    
        sleep(interval_s)
    #
    cam.stop_preview()
    #
    print("Done taking photos.")
