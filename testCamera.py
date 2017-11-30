#!/usr/bin/env python
# History:
#   2017.11.29  Besler  Created
#
# Description:
#   Perform a test run of the Pi camera.
#
# Notes:
#   - Be sure to the '-X' flag when sshing into your Pi.
#   - Shamelessly taken from: https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/

# Imports
from __future__ import print_function
import os
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# Load configuration files
if len(os.sys.argv) == 2:
    exec(open(os.sys.argv[1]).read(), globals())
else:
    exec(open('pi.conf').read(), globals())

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
  # grab the raw NumPy array representing the image, then initialize the timestamp
  # and occupied/unoccupied text
  image = frame.array
 
  # show the frame
  cv2.imshow("Frame", image)
  key = cv2.waitKey(1) & 0xFF
 
  # clear the stream in preparation for the next frame
  rawCapture.truncate(0)
 
  # if the `q` key was pressed, break from the loop
  if key == ord("q"):
    break
