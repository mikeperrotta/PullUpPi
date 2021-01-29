import face_recognition
import picamera
import numpy as np
import time

camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.hflip = True
output = np.empty((camera.resolution[1], camera.resolution[0], 3), dtype=np.uint8)

camera.start_preview(alpha=200)

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

pullUpAreaTop = camera.resolution[1] * 1 // 3
pullUpAreaBottom = camera.resolution[1] * 2 // 3

draw_square((pullUpAreaTop, camera.resolution[0] - 1, pullUpAreaBottom, 0), (120, 120, 120, 255))

overlay = None

last_capture_time = time.time()

while True:
    print("Capturing image. ({}s since last capture)".format(time.time() - last_capture_time))
    last_capture_time = time.time()

    camera.capture(output, format="rgb", use_video_port=True)

    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    
    for o in camera.overlays[1:]:
        camera.remove_overlay(o)
    
    for l in face_locations:
        top = l[0]
        print(top)
        color = (255, 0, 0, 200)
        if top < pullUpAreaBottom:
            color = (0, 13, 255, 200)
        if top < pullUpAreaTop:
            color = (0, 207, 17, 200)
        draw_square(l, color)
        