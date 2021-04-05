import datetime as dt
from io import BytesIO
import logging
from threading import Thread
from time import sleep
import os
import shutil
import subprocess


logger = logging.getLogger()

_MOVIE_FILES = list()
_MAX_QUEE_SIZE = 100
_THREAD = None
_EXIT = False
_PATH = "movie"
_MINIMUM_FREE_SPACE = 500  # MB. minimum free space of disk


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
    return file_name


def _convert_to_mp4(filename: str):
    # MP4Box -add movie/2020-9-27_23_56.h264 movie/2020-9-27_23_56.mp4
    convert = subprocess.run(
        ["MP4Box", "-add", filename, filename.replace("h264", "mp4")])

    logger.info(f"Converting function with return code: {convert.returncode}")
    
    # delete the h264 file
    if convert.returncode == 0:
        os.remove(filename)


def _disk_full():
    """if the rest space of disk small as x M"""
    dsk_usg = shutil.disk_usage("/")
    return (dsk_usg.free/1024/1024) < _MINIMUM_FREE_SPACE


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
            h264_file = _save_movie(buffer)
            _convert_to_mp4(h264_file)
        sleep(0.2)


_THREAD = None # thread object for saving


def stop():
    global _EXIT
    _EXIT = True
    _THREAD.join()


def start():
    global _THREAD
    if _THREAD is None or not _THREAD.is_alive():
        _THREAD = Thread(target=_loop, args=())
        _THREAD.start()
        print(f"thread {_THREAD} has been created")
    else:
        print(f"thread {_THREAD} exists and is alive")


_check_path()
