import picamera
import config


RESOLUTION = (1280, 720)
FRAME_RATE = 30

camera = None
configuration = None


def load_config():
    global RESOLUTION, FRAME_RATE, camera, configuration
    configuration = config.load()
    if configuration:
        RESOLUTION = tuple([int(i) for i in configuration["resolution"].split("x")])
        FRAME_RATE = configuration["framerate"]

    camera = picamera.PiCamera(resolution=RESOLUTION, framerate=FRAME_RATE)
    camera.rotation = configuration.get("rotation") or 0
    camera.annotate_background = picamera.Color('grey')

    
    configuration["resolution"] = "x".join([str(x) for x in RESOLUTION])
    configuration["framerate"] = FRAME_RATE
    configuration["rotation"] = camera.rotation

def save_config():
    global configuration
    config.save(configuration)

def get_config():
    return configuration

def set_config(config):
    print(config)
    camera.rotation = config.get("rotation") or camera.rotation

load_config()