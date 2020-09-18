import random
import picamera
from io import BytesIO
import datetime as dt
import logging
import save

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("start")

RESOLUTION = (1280, 720)
FIRST_RUN = True

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


with picamera.PiCamera(resolution=RESOLUTION) as camera:
    logger.info("Start of Script")
    stream = picamera.PiCameraCircularIO(camera, seconds=20)
    camera.start_recording(stream, format='h264')
    camera.wait_recording(1)

    while True:

        if start_recording() or _first_run():
            start = dt.datetime.now()
            logger.info("start recording movie")

            # Keep recording for 5 seconds and only then write the
            # stream to disk
            start = dt.datetime.now()
            while True:
                camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                camera.wait_recording(0.2)

                # minimum length 2 seconds # recording at least 2 seconds
                if (dt.datetime.now() - start).seconds < 2:
                    continue

                if start_recording():
                    # start recording the new movie
                    break

            # stream.copy_to('motion.h264')
            buffer = BytesIO()
            stream.copy_to(buffer)
            stream.clear()
            save.save_movie(buffer)

    camera.stop_recording()
    save.exit()
