#!/usr/bin/python3
#
# with nikon lens 24 mm f 2
# set at f8 and focus 0.7 m
# iso 800
#
import os
import sys
import time
import logging
import picamera
from cam_tools import check_start, get_time, check_path
#
#
# Get ready for a config file
path ='/home/pi/stars'
REPORT = '#=%4i HM=%8s SS=%7i FR=%7.3f ISO=%3i'
#
duration = 160         # duration (min) of timelapse
interval = 5          # delay (seconds) between captures
start = (30, 12)       # time (day, h) to start 
#
iso = 800                  # iso
speed = 15_000_000
resolution = (2028, 1520)  # resolution
sensor_mode = 3            # full FOV, no binning, 4:3, max resolution
#
# must be < 0.08 to allow 15 s exposition
framerate = 0.05           # frames per second
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
    cam = picamera.PiCamera()
    cam.resolution = resolution
    cam.sensor_mode = sensor_mode  
    cam.iso = iso
    cam.framerate = framerate   # always before shutter_speed
    cam.shutter_speed = speed
    picamera.PiCamera.CAPTURE_TIMEOUT = 120
    #
    time.sleep(10)
    #
    cam.start_preview(fullscreen=False, window=(895,300,1014,760))    
    #
    brghtnss = 0
    #
    for i in range(numphotos):
        #print('CXM=', cam.exposure_mode)
        logging.info(REPORT % (i, get_time()[1], cam.exposure_speed,
                               cam.framerate, cam.iso))
        current = photo.format(i)
        try:
            cam.capture(current)
        except picamera.exc.PiCameraRuntimeError:
            logging.error('PiCameraError')
        
        time.sleep(interval)
    #
    cam.stop_preview()
    #
    logging.info("Done taking photos.")
