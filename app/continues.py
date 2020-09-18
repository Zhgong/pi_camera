import io
import random
import picamera
from io import BytesIO
import datetime as dt

def save_movie(buffer:BytesIO):
    now = dt.datetime.now()
    last_minute = now.minute - 1
    if last_minute < 0:
        last_minute = 59
    print(f"Saving movie {last_minute} ....")
    with open(f'motion_{last_minute}.h264', "wb") as f:
        f.write(buffer.getbuffer())
    print(f"movie {last_minute} saved.")

def start_recording():
        # from 59 to 0
        now = dt.datetime.now()
        if now.second == 0:
            return True

def motion_detected():
    # Randomly return True (like a fake motion detection routine)
    
    
    return random.randint(0, 10) == 0

with picamera.PiCamera() as camera:
    camera.annotate_text = 'Hello world!'
    stream = picamera.PiCameraCircularIO(camera, seconds=20)
    camera.start_recording(stream, format='h264')
    camera.wait_recording(1)
    
    while True:
        
        if start_recording():
            print("start recording movie")
            camera.wait_recording(2) # recording at least 2 secons
            
            # Keep recording for 5 seconds and only then write the
            # stream to disk
            start = dt.datetime.now()
            while True:
                camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                camera.wait_recording(0.2)
                if start_recording():
                    # start recording the new movie
                    break
            
            # stream.copy_to('motion.h264')
            buffer= BytesIO()
            stream.copy_to(buffer)
            stream.clear()
            save_movie(buffer)

            

    camera.stop_recording()