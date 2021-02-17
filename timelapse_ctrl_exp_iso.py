#!/usr/bin/python3
#
# with nikon lens 24 mm f 2
# set at f8 and focus 0.7 m
# iso 800
#
import os
import sys
import time
import datetime
import glob
import logging
import termios
import numpy as np
from picamera import PiCamera
from PIL import Image
from inputimeout import inputimeout, TimeoutOccurred
#
#
# Get ready for a config file
path ='/home/pi/sunrise'
REPORT = '#=%4i HM=%8s SS=%7i FR=%7.3f ISO=%3i BR=%.1f'
#
duration = 360         # duration (min) of timelapse
interval = 5           # delay (seconds) between captures
start = (17, 12)       # time (day, h) to start 
#
iso = 800                  # iso  
resolution = (2028, 1520)  # resolution
sensor_mode = 3            # full FOV, no binning, 4:3, max resolution
#
framerate = 0.1            # frames per second
#
#
def log(path):
    ""
    logfile = os.path.join(path, 'timelapse.log')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(message)s',
                        handlers=[logging.FileHandler(logfile, mode='w', 
                                                  encoding='utf-8'),
                                  logging.StreamHandler(sys.stdout)
                                 ]
                        )
#
def check_start(start):
    while True:
        dateraw = datetime.datetime.now()
        hour = dateraw.hour
        print(hour, end=' ')
        if dateraw.day == start[0]:
            if hour >= start[1]:
                print('')
                datetimeformat = dateraw.strftime("%Y-%m-%d %H:%M:%S")
                return (datetimeformat)
        #
        time.sleep(300)
#
def get_time():
    dateraw = datetime.datetime.now()
    datetimeformat = dateraw.strftime("%Y-%m-%d %H:%M:%S")
    return datetimeformat.split(' ')
#
def check_path(path):
    ""
    if os.path.exists(path):
        
        warning= ('Picture directory already exists\n'
                  'Erase old pictures (yes/no) ?'
                  )
        try:  
            kieres = inputimeout(prompt=warning, timeout=30)
            if kieres == 'yes':
                path_glob = os.path.join(path, '*.jpg')
                for arch in glob.glob(path_glob):
                    os.remove(arch)
        except (TimeoutOccurred, termios.error):
            dateraw = datetime.datetime.now()
            path = '%s_%i_%i' % (path, dateraw.hour, dateraw.minute)
            os.mkdir(path)        
    else:
        os.mkdir(path)
    return path
#        
def check_iso(cam, brghtnss):
    ""
    if cam.iso > 100:
        if (cam.exposure_speed < 5000) or (brghtnss > 200):
            cam.iso -= 50
    if cam.iso < 800:
        if (cam.exposure_speed > 80_000) or (brghtnss < 10):
            cam.iso += 50
#
#
if __name__ == '__main__':
    
    path = check_path(path)
    log(path)
    logging.info("Program started at %s %s" % tuple(get_time()))
    #
    photo = os.path.join(path, 'image{0:06d}.jpg')
    numphotos = int((duration * 60) / interval)     # number of photos to take
    #
    logging.info("photos to take = %i" % numphotos)
    logging.info('resolution = %ix%i' % resolution)
    logging.info('sensor mode = %i\nISO = %i\nframe rate = %f' % (sensor_mode, iso, framerate))
    #
    date = check_start(start)
    logging.info("Timelapse started at %s" % date)
    #
    cam = PiCamera()
    cam.resolution = resolution
    cam.sensor_mode = sensor_mode  
    cam.iso = iso
    cam.framerate = framerate
    #
    time.sleep(20)
    #
    cam.start_preview(fullscreen=False, window=(895,300,1014,760))    
    #
    brghtnss = 0
    auto = True
    ss = 0
    new_ss = 99_999
    #
    for i in range(numphotos):
        #print('CXM=', cam.exposure_mode)
        logging.info(REPORT % (i, get_time()[1], cam.exposure_speed,
                               cam.framerate, cam.iso, brghtnss))
        current = photo.format(i)
        cam.capture(current)
        im = Image.open(current)
        brghtnss = np.mean(im)
        #
        if brghtnss < 50:
            if new_ss == 0:
                new_ss = 10_000
            new_ss = new_ss * (2 - (0.01 * brghtnss))
            new_ss = int(new_ss)
            new_ss = min(1_000_000, new_ss)
        elif brghtnss > 180:
            if new_ss < 120_000:
                new_ss = 0
            else:
                new_ss = new_ss * (0.1 + (0.002 * brghtnss))
                new_ss = int(new_ss) 
        #
        check_iso(cam, brghtnss)
        #
        if new_ss != ss:
            ss = new_ss
            cam.shutter_speed = ss
    
        time.sleep(interval)
    #
    cam.stop_preview()
    #
    logging.info("Done taking photos.")
