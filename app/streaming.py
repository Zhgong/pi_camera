from flask import Flask, render_template, Response
import io
from time import sleep
import logging

from flask.json import jsonify
import camera
import continues
from threading import Thread
from api import app


from picamera import exc
logger = logging.getLogger()


@app.route('/')
def index():
    return render_template('index.html')


def run():
    t_continues = Thread(target=continues.main, args=())
    t_continues.start()
    app.run(host='0.0.0.0', debug=False)
    t_continues.join()


if __name__ == '__main__':
    run()
