import picamera
from io import BytesIO
import datetime as dt
import logging
import save
from threading import Thread

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("start")

RESOLUTION = (1280, 720)
FIRST_RUN = True
_EXIT = False
BUFFER_SIZE = 65 # seconds
FRAME_RATE = 30
_MINIMUM_MOVIE_LENGTH = 2 # minimum length of movie

def _first_run():
    global FIRST_RUN
    if FIRST_RUN:
        FIRST_RUN = False
        return True
    else:
        return False


def start_recording():
    # from 59 to 0
    now = dt.datetime.now()
    if now.second == 0:
        return True

def add_timestamp(camera:picamera.PiCamera):
    while not _EXIT:
        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.wait_recording(0.2)

def exit():
    global _EXIT
    _EXIT = False

with picamera.PiCamera(resolution=RESOLUTION, framerate=FRAME_RATE) as camera:
    logger.info("Start of Script")
    stream = picamera.PiCameraCircularIO(camera, seconds=BUFFER_SIZE)
    camera.start_recording(stream, format='h264')

    t = Thread(target=add_timestamp, args=(camera,))
    t.start()

    camera.wait_recording(1)

    while True:

        start = dt.datetime.now()
        logger.info("start recording movie")

        while True:
            
            # minimum length 2 seconds # recording at least 2 seconds
            if (dt.datetime.now() - start).seconds < _MINIMUM_MOVIE_LENGTH:
                continue

            if start_recording():
                # start recording the new movie
                break
            camera.wait_recording(0.1)

        # stream.copy_to('motion.h264')
        buffer = BytesIO()
        stream.copy_to(buffer)
        stream.clear()
        save.save_movie(buffer)

    camera.stop_recording()
    save.exit()
    exit()
    t.join()
