from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
import numpy as np
from SoundPlayer import *
from ScoreKeeper import *

camera = PiCamera()
camera.resolution = (800, 480)
camera.framerate = 32
camera.hflip = True
rawCapture = PiRGBArray(camera, size=camera.resolution)

backSub = cv.createBackgroundSubtractorMOG2(history=500, varThreshold=32, detectShadows=False)

time.sleep(0.1)

push_up_low = 270
push_up_high = 90
has_lowered = False

""" Displays
0 - Raw video
1 - Processed video
2 - Score keeper
"""
display = 2
num_displays = 3

smoothed_height = 0
smoothing_value = .5

daily_goal = 30
daily_total = 0
lifetime_total = 0

sk = ScoreKeeper(goal=daily_goal, fullscreen=True)
sp = SoundPlayer()

def on_successful_push_up():
    global daily_total, lifetime_total
    daily_total += 1
    lifetime_total += 1
    if display == 2:
        sk.update_scores(daily_total, lifetime_total)
    sp.play(mario_coin)
    if daily_total == lifetime_total:
        sp.play(mario_level_complete)
    print('push up!')
    
def next_display():
    global display
    display += 1
    display = display % num_displays
    if display == 2:
        sk.update_scores(daily_total, lifetime_total)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    
    if display == 0:
        sk.show_cv_image(image)
    
    fgMask = backSub.apply(image)
    
    row_sums = np.sum(fgMask, axis=1)
    height = np.argmax(row_sums>10000)
    if height > 0:
        smoothed_height = int(height * smoothing_value + smoothed_height * (1 - smoothing_value))
        height = smoothed_height
    
    if display == 1:
        masked_image = np.copy(image)
        masked_image[fgMask == 0] = 0
        color = (155, 0, 0) if not has_lowered else (0, 155, 0)
        if height > 0:
            cv.line(masked_image, (0, height), (camera.resolution[0], height), color, 3)
        cv.line(masked_image, (0, push_up_low), (camera.resolution[0], push_up_low), (66, 135, 245), 1)
        cv.line(masked_image, (0, push_up_high), (camera.resolution[0], push_up_high), (245, 66, 230), 1)
        sk.show_cv_image(masked_image)
        
    if any([e.type == pygame.MOUSEBUTTONUP for e in list(pygame.event.get())]):
        x, y = pygame.mouse.get_pos()
        if y < 40 and x > 760:
            break
        else:
            next_display()

    if not has_lowered:
        if height > push_up_low:
            has_lowered = True
    else:
        if height < push_up_high and height != 0:
            has_lowered = False
            on_successful_push_up()
            
    rawCapture.truncate(0)
    
safe_quit()
