import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import os

# Load configuration files
if len(os.sys.argv) > 1:
  exec(open(os.sys.argv[1]).read(), globals())
else:
  filePath = os.path.dirname(os.path.realpath(__file__))
  exec(open(os.path.join(filePath, 'pi.conf')).read(), globals())

# Configure GPIO pints
GPIO.setmode(GPIO.BCM)
GPIO.setup(cf['PinA'], GPIO.OUT)
GPIO.setup(cf['PinB'], GPIO.OUT)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

cv2.setNumThreads(4)

def FindCircles(frame):
  # Do some adaptive histogram equalization to deal with uneven lighting
  split = cv2.split(frame)
  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(10,10))
  for i in range(len(split)):
      split[i] = clahe.apply(split[i])
  eq = cv2.merge(split)

  # Do some blurring. This smooths out the final segmentation
  blur = cv2.GaussianBlur(eq, (21, 21), 0)

  # Convert to HSV and do some harsh thresholding.
  # We have essentially clipped out camera with the phone light.
  hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
  thresh = cv2.inRange(hsv,
      np.array([0.00*256, 0.00*256, 0.95*256]),
      np.array([0.05*256, 0.05*256, 1.00*256]))

  # Hough transform to grab circles
  circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT,
                  1, np.sqrt(thresh.size)/8,
                  param1=10, param2=10,
                  minRadius=5, maxRadius=int(np.sqrt(thresh.size)/4)
                  )

  return circles

def ProcessCircles(circles):
  # Check if we have a circle
  if circles is None:
    ProcessCircles.LastCenter = None
    return None
  circles = np.uint16(np.around(circles))

  # If we are in state "no object" return the first center
  i = np.array([0,0])
  if ProcessCircles.LastCenter is None:
    # We don't have a previous example. Just take the first circle
    i = circles[0,0]
  else:
    # Determine which point was closest to the most previous.
    bestMatch = np.inf
    for index in circles[0,:]:
      distance = np.linalg.norm(np.array([i[0],i[1]]) - ProcessCircles.LastCenter)
      if distance < bestMatch:
        bestMatch = distance
        i = index
  ProcessCircles.LastCenter = np.array([i[0], i[1]])
  return ProcessCircles.LastCenter
ProcessCircles.LastCenter = None

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
  # Grab this frame
  frame = frame.array

  # Process image
  circles = FindCircles(frame)
  center = ProcessCircles(circles)

  # If we 
  if center is not None:
    # Show on frame
    cv2.circle(frame,(center[0],center[1]), 2, (0,0,255), 3)

    # Check if center is left or right of frame and highlight appropriately.
    # Note the flipped coordinates are correct
    shape = frame.shape
    if center[0] < shape[1]/2:
      GPIO.output(cf['PinA'], GPIO.HIGH)
      GPIO.output(cf['PinB'], GPIO.LOW)
    else:
      GPIO.output(cf['PinA'], GPIO.LOW)
      GPIO.output(cf['PinB'], GPIO.HIGH)

    # Print some helpful info
    if cf['Interactive']:
      print('center: {}'.format(center))
      print('shape: {}'.format(shape))
      print('')
    
  else:
    GPIO.output(cf['PinA'], GPIO.LOW)
    GPIO.output(cf['PinB'], GPIO.LOW)


  # clear the stream in preparation for the next frame
  rawCapture.truncate(0)

  # Show frame if the shell was ran in interactive mode
  if cf['Interactive']:
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
GPIO.cleanup()
cv2.destroyAllWindows()

