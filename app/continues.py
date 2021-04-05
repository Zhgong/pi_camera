import picamera
from io import BytesIO
import datetime as dt
import logging
from threading import Thread
import time



from picamera.camera import PiCamera
import save
from threading import Thread

FORMAT = '[%(asctime)-15s] %(levelname)-4s %(filename)s:%(funcName)s:%(lineno)d: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

print = logging.info


FIRST_RUN = True
_EXIT = False
BUFFER_SIZE = 65 # seconds
_MINIMUM_MOVIE_LENGTH = 2 # minimum length of movie

stream = None

local_threads = []

_THREAD = None # Main thread

def _first_run():
    global FIRST_RUN
    if FIRST_RUN:
        FIRST_RUN = False
        return True
    else:
        return False


def is_start_of_new_minute():
    # from 59 to 0
    now = dt.datetime.now()
    if now.second == 0:
        return True

def add_timestamp(camera:picamera.PiCamera):
    while not _EXIT:
        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.wait_recording(0.2)

def local_exit():
    global _EXIT
    _EXIT = True
    for t in local_threads:
        t.join()

def loop(camera:picamera.PiCamera):
    global local_threads, state
    logger.info("Start of Script")
    stream = picamera.PiCameraCircularIO(camera, seconds=BUFFER_SIZE)
    camera.start_recording(stream, format='h264')

    t = Thread(target=add_timestamp, args=(camera,))
    t.start()
    local_threads.append(t)


    camera.wait_recording(1)

    while not _EXIT:

        start = dt.datetime.now()
        logger.info(f"start recording movie {start.minute}")

        while not _EXIT:
            
            # minimum length 2 seconds # recording at least 2 seconds
            if (dt.datetime.now() - start).seconds < _MINIMUM_MOVIE_LENGTH:
                continue

            if is_start_of_new_minute():
                # start recording the new movie
                break
            camera.wait_recording(0.1)

        # stream.copy_to('motion.h264')
        buffer = BytesIO()
        stream.copy_to(buffer)
        stream.clear()
        save.save_movie(buffer)

    print("stopping camera")
    camera.stop_recording()



def main():
    logger.info("start")
    import camera
    save.start()
    loop(camera.camera)


def start_thread():
    global _THREAD, _EXIT, local_threads
    local_threads = []
    _EXIT = False
    if _THREAD is None or not _THREAD.is_alive():
        _THREAD = Thread(target=main, args=())
        _THREAD.start()
        print(f"thread {_THREAD} has been created")
    else:
        print(f"thread {_THREAD} exists and is alive")
    local_threads.append(_THREAD)
    return _THREAD

def stop_recording():
    local_exit()
    save.stop()

        

if __name__ == "__main__":
    main()