import picamera
import config


RESOLUTION = (1280, 720)
FRAME_RATE = 30

camera = None


def load_config():
    global RESOLUTION, FRAME_RATE, camera
    configuration = config.load()
    if configuration:
        RESOLUTION = tuple([int(i) for i in configuration["resolution"].split("x")])
        FRAME_RATE = configuration["framerate"]

    camera = picamera.PiCamera(resolution=RESOLUTION, framerate=FRAME_RATE)
    camera.rotation = configuration.get("rotation") or 0
    camera.annotate_background = picamera.Color('grey')

def save_config():
    configuration = dict()
    configuration["resolution"] = "x".join([str(x) for x in RESOLUTION])
    configuration["framerate"] = FRAME_RATE
    configuration["rotation"] = camera.rotation
    config.save(configuration)


load_config()