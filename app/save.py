import datetime as dt
from io import BytesIO
import logging
from logging import log
from threading import Thread
from time import sleep

logger = logging.getLogger()

_MOVIE_FILES = list()
_MAX_QUEE_SIZE = 100
_THREAD = None
_EXIT = False

def save_movie(buffer:BytesIO):
    if len(_MOVIE_FILES) > _MAX_QUEE_SIZE:
        logger.error("MAX QUEE size exceed")
    _MOVIE_FILES.append(buffer)


def _save_movie(buffer:BytesIO):
    now = dt.datetime.now()
    last_minute = now.minute - 1
    if last_minute < 0:
        last_minute = 59
    logger.info(f"Saving movie {last_minute} ....")
    with open(f'motion_{last_minute}.h264', "wb") as f:
        f.write(buffer.getbuffer())
    logger.info(f"movie {last_minute} saved.")

def _loop():
    while not _EXIT:
        if len(_MOVIE_FILES)>0:
            buffer = _MOVIE_FILES.pop(0)
            _save_movie(buffer)
        sleep(0.1)

_THREAD = Thread(target=_loop, args=())
_THREAD.start()

def exit():
    _EXIT = True
    _THREAD.join()

