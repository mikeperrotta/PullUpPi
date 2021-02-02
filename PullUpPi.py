import face_recognition
import picamera
import numpy as np
import time
import pygame
from SoundPlayer import *

sound_player = SoundPlayer()
camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.hflip = True
output = np.empty((camera.resolution[1], camera.resolution[0], 3), dtype=np.uint8)

camera.start_preview(alpha=235)

def draw_square(corners, color, layer=3):
    top, right, bottom, left = corners
    
    top = max(top, 0)
    right = min(right, camera.resolution[0] - 1)
    bottom = min(bottom, camera.resolution[1] - 1)
    left = max(left, 0)
    
    frame = np.zeros((camera.resolution[1], camera.resolution[0], 4), dtype=np.uint8)
    frame[top, left:right] = color
    frame[bottom, left:right] = color
    frame[top:bottom, left] = color
    frame[top:bottom, right] = color
    return camera.add_overlay(np.asarray(frame), layer=layer)

pullUpAreaTop = camera.resolution[1] * 2 // 5
pullUpAreaBottom = camera.resolution[1] * 3 // 5

draw_square((pullUpAreaTop, camera.resolution[0] - 1, pullUpAreaBottom, 0), (10, 10, 10, 50))

overlay = None

last_capture_time = time.time()

pull_ups = 0
is_descending = True  # True if face has completed a pull up but hasn't yet lowered fully

validTop, validBottom, validLeft, validRight = (20, 220, 40, 280)
draw_square((validTop, validRight, validBottom, validLeft), (0, 0, 0, 100))

num_permanent_overlays = len(camera.overlays)

while True:
    print("Capturing image. ({:.4}s since last capture)".format(time.time() - last_capture_time))
    last_capture_time = time.time()

    camera.annotate_text = "Pull ups: {}".format(pull_ups)
    
    camera.capture(output, format="rgb", use_video_port=True)
    print("Capture took {}s".format(time.time() - last_capture_time))

    face_locations = face_recognition.face_locations(output[validTop:validBottom, validLeft:validRight, :])
    print("Found {} faces in image.".format(len(face_locations)))
        
    for o in camera.overlays[num_permanent_overlays:]:
        camera.remove_overlay(o)
    
    for l in face_locations:
        # first, adjust locations to be relative to our screen instead of our valid area
        l = list(l)
        l[0] += validTop
        l[1] += validLeft
        l[2] += validTop
        l[3] += validLeft
        
        top = l[0]
        
        if top > pullUpAreaBottom:
            # face is fully lowered
            color = (255, 0, 0, 200)
            is_descending = False
        elif top > pullUpAreaTop:
            # face is between thresholds
            color = (0, 13, 255, 200)
        else:
            # face is fully up
            color = (0, 207, 17, 200)
            if not is_descending:
                pull_ups += 1
                is_descending = True
                sound_player.play(mario_coin)
        
        draw_square(l, color)