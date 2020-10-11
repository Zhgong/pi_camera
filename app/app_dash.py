
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import camera
import io
from flask import Flask, Response
from time import sleep

server = Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets, server=server)


@server.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


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


app.layout = html.Div([
    html.H1('Dash Camera'),
    html.Img(src='/video_feed')
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)
