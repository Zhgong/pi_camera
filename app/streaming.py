from flask import Flask, render_template, Response
import io
from time import sleep
import logging

from flask.json import jsonify
import camera
import continues
from threading import Thread


from picamera import exc
logger = logging.getLogger()

RESOLUTION = (1280, 720)
FIRST_RUN = True
_EXIT = False
BUFFER_SIZE = 65  # seconds
FRAME_RATE = 30

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen():
    yield from stream(camera.camera)


def stream(camera):
    while True:
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg', use_video_port=True)
        stream.seek(0)
        frame = stream.read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        sleep(1/25)

@app.route("/camera/rotate")
def camera_rotate():
    previous_rotation = camera.camera.rotation 
    camera.camera.rotation += 90
    return jsonify({"status":"success", "previous_rotation":previous_rotation, "current_rotation": camera.camera.rotation})
    

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def run():
    t_continues = Thread(target=continues.main, args=())
    t_continues.start()
    app.run(host='0.0.0.0', debug=False)
    t_continues.join()


if __name__ == '__main__':
    run()
