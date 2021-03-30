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
from inputimeout import inputimeout, TimeoutOccurred

#
def check_start(start):
    """"""
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
#
def get_time():
    """"""
    dateraw = datetime.datetime.now()
    datetimeformat = dateraw.strftime("%Y-%m-%d %H:%M:%S")
    return datetimeformat.split(' ')
#
#
def check_path(path):
    """"""
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
            else:
                dateraw = datetime.datetime.now()
                path = '%s_%i_%i' % (path, dateraw.hour, dateraw.minute)
                os.mkdir(path)   
        except (TimeoutOccurred, termios.error):
            dateraw = datetime.datetime.now()
            path = '%s_%i_%i' % (path, dateraw.hour, dateraw.minute)
            os.mkdir(path)        
    else:
        os.mkdir(path)
    return path
#        