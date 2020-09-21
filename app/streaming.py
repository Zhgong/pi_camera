from flask import Flask, render_template, Response
import io
import asyncio
from time import sleep


import picamera
RESOLUTION = (1280, 720)
FIRST_RUN = True
_EXIT = False
BUFFER_SIZE = 65 # seconds
FRAME_RATE = 30

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    with picamera.PiCamera(resolution=RESOLUTION, framerate=FRAME_RATE) as camera:
        while True:
            stream = io.BytesIO()
            
            camera.capture(stream, format='jpeg', use_video_port=True)
            stream.seek(0)
            frame = stream.read()
            yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            sleep(1/25)



@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)