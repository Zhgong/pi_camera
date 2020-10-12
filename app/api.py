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


app = Flask(__name__)


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
    return jsonify({"status": "success", "previous_rotation": previous_rotation, "current_rotation": camera.camera.rotation})


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/config')
def config():
    return jsonify(camera.get_config())


