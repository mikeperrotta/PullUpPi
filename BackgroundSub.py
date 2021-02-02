from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
import numpy as np
from SoundPlayer import *

camera = PiCamera()
camera.resolution = (800, 480)
camera.framerate = 32
camera.hflip = True
rawCapture = PiRGBArray(camera, size=camera.resolution)

backSub = cv.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    cv.imshow("Frame", image)
    
    fgMask = backSub.apply(image)
    
    row_sums = np.sum(fgMask, axis=1)
    height = np.argmax(row_sums>10000)
    
    cv.line(fgMask, (0, height), (camera.resolution[0], height), 155, 3)
    cv.imshow('FG Mask', fgMask)
    
    key = cv.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break
    """
    if any([e.type == pygame.MOUSEBUTTONUP for e in list(pygame.event.get())]):
        x, y = pygame.mouse.get_pos()
        if y < 40:
            quit()
    """
cv.destroyAllWindows()
