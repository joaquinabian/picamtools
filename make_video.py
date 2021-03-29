#!/usr/bin/python3
#
# makes a video from a sequence of pictures in path
#
import datetime
import os 
#
#path = "/home/pi/sunrise/*.jpg"
path = "/home/pi/luna_raise/*.jpg"
save = "/home/pi/Videos/%s.mp4"
#
#fps = 10                # video frames per second
fps = 7                 # video frames per second
res = '2028x1520'       # video resolution ? 
                        # 1280x720 => 4321 pics, 6.9 GB => 206 MB
                        # 2028x1520 =>                  => 206 MB  (no change)
#
dateraw = datetime.datetime.now() 
datetimeformat = dateraw.strftime("%Y-%m-%d_%H:%M")
save = save % datetimeformat


cmd = (
    'ffmpeg '
    '-r {} '                # Set frame rate
    '-f image2 '            # Force input or output file format
    '-s {} '                # Set frame size
    '-nostats '             # disable default Print encoding progress/stats 
    '-loglevel 0 '          # Set logging level to 'panic' (Only fatal errors)
    '-pattern_type glob '   # makes video from files matching the glob pattern in -i option
    '-i "{}" '              # input file url
    '-vcodec libx264 '      # Set video codec (https://trac.ffmpeg.org/wiki/Encode/H.264)
    '-crf 25  '             # Constant Rate Factor, depends on encoder 
                            # (for x264, 0:lossless, 23:default, 51:worst)
    '-pix_fmt yuv420p '     # Set pixel format
    '{}'                    # output video filename
)

cmd = cmd.format(fps, res, path, save)

print("Wait. Video is created from Pictures.")
os.system(cmd)
print('Timelapse video is complete. Video saved as %s' % save)
