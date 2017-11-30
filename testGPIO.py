#!/usr/bin/env python
# History:
#   2017.11.29  Besler  Created
#
# Description:
#   Perform a test run of the GPIO pins on the board
#
# Notes:
#   - Be certain to set pi.conf to correspond to your board.
#   - The two LEDs should alternate (HL -> LH -> HH)

# Imports
from __future__ import print_function
import os
import RPi.GPIO as GPIO
from time import sleep

# Load configuration files
if len(os.sys.argv) == 2:
    exec(open(os.sys.argv[1]).read(), globals())
else:
    exec(open('pi.conf').read(), globals())

# Configure GPIO pints
GPIO.setmode(GPIO.BCM)
GPIO.setup(cf['PinA'], GPIO.OUT)
GPIO.setup(cf['PinB'], GPIO.OUT)


# Toggle lights
testTime = 0.5 # in ms
for _ in range(5):
  GPIO.output(cf['PinA'], GPIO.HIGH)
  GPIO.output(cf['PinB'], GPIO.LOW)
  sleep(testTime)

  GPIO.output(cf['PinA'], GPIO.LOW)
  GPIO.output(cf['PinB'], GPIO.HIGH)
  sleep(testTime)

  GPIO.output(cf['PinA'], GPIO.HIGH)
  GPIO.output(cf['PinB'], GPIO.HIGH)
  sleep(testTime)

GPIO.output(cf['PinA'], GPIO.LOW)
GPIO.output(cf['PinB'], GPIO.LOW)

GPIO.cleanup()
