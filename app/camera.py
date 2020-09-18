import io
import random
import picamera
from io import BytesIO
import datetime as dt

def save_movie(buffer:BytesIO, i):
    with open(f'motion_{i}.h264', "wb") as f:
        f.write(buffer.getbuffer())

def motion_detected():
    # Randomly return True (like a fake motion detection routine)
    
    
    return random.randint(0, 10) == 0

with picamera.PiCamera() as camera:
    camera.annotate_text = 'Hello world!'
    stream = picamera.PiCameraCircularIO(camera, seconds=20)
    camera.start_recording(stream, format='h264')
    camera.wait_recording(1)
    for i in range(2):
        while True:
            
            if motion_detected():
                print("motion detected!")
                
                # Keep recording for 5 seconds and only then write the
                # stream to disk
                start = dt.datetime.now()
                while (dt.datetime.now() - start).seconds < 5:
                    camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    camera.wait_recording(0.2)
                print("Saving movie ....")
                # stream.copy_to('motion.h264')
                buffer= BytesIO()
                stream.copy_to(buffer)
                stream.clear()
                save_movie(buffer, i)

                print("movie saved.")
                break

    camera.stop_recording()