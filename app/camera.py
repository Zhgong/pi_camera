import picamera


RESOLUTION = (1280, 720)
FRAME_RATE = 30

camera = picamera.PiCamera(resolution=RESOLUTION, framerate=FRAME_RATE)