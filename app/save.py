import datetime as dt
from io import BytesIO
import logging
from logging import log
from shutil import disk_usage
from threading import Thread
from time import sleep
import os
import shutil


logger = logging.getLogger()

_MOVIE_FILES = list()
_MAX_QUEE_SIZE = 100
_THREAD = None
_EXIT = False
_PATH = "movie"

def _check_path():
    """Creating path if not exists"""
    if not os.path.exists(_PATH):
        os.mkdir(_PATH)

def save_movie(buffer: BytesIO):
    """Append movies to buffer"""
    if len(_MOVIE_FILES) > _MAX_QUEE_SIZE:
        logger.error("MAX QUEE size exceed")
    _MOVIE_FILES.append(buffer)


def _save_movie(buffer: BytesIO):
    now = dt.datetime.now()
    last_time = now - dt.timedelta(minutes=1)
    logger.info(f"Saving movie {last_time.minute} ....")

    file_name = f'{_PATH}/{last_time.year}-{last_time.month}-{last_time.day}_{last_time.hour}_{last_time.minute}.h264'
    with open(file_name, "wb") as f:
        f.write(buffer.getbuffer())
    logger.info(f"movie {last_time.minute} saved.")

def _disk_full():
    """if the rest space of disk small as 100 M"""
    dsk_usg = shutil.disk_usage("/")
    return (dsk_usg.free/1024/1024) <100 

def _check_dsk_usage():
    """Remove the oldest files if the disk is out of use"""
    while _disk_full():
        logger.info("Disk is out of space!!")
        list_of_files = os.listdir(_PATH)
        if not list_of_files:
            logger.info("There is no movies to delete to make free space")
            break
        full_path = [f"{_PATH}/{x}" for x in list_of_files]

        oldest_file = min(full_path, key=os.path.getctime)
        os.remove(oldest_file)
        logger.info(f"{oldest_file} was removed.")


def _loop():
    while not _EXIT:
        _check_dsk_usage()
        _check_path()
        while len(_MOVIE_FILES) > 0:
            buffer = _MOVIE_FILES.pop(0)
            _save_movie(buffer)
        sleep(0.2)


_THREAD = Thread(target=_loop, args=())
_THREAD.start()


def exit():
    _EXIT = True
    _THREAD.join()


_check_path()