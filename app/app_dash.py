
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import camera
import io
from flask import Flask, Response
from time import sleep
import base64

server = Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets, server=server)


@server.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def gen():
    return stream(camera.camera)


def stream(camera):
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg', use_video_port=True)
    stream.seek(0)
    frame = stream.read()
    return (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def image(camera):
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg', use_video_port=True)
    stream.seek(0)
    frame = stream.read()
    return frame


app.layout = html.Div([
    html.H1('Dash Camera'),
    html.Button('Send',id='btn-send', n_clicks=0),
    html.Img(id='img', src='')
])


@app.callback(
    Output('img', 'src'),
    Input('btn-send','n_clicks')
)
def send(n_clicks):
    print(n_clicks)
    img = image(camera.camera)
    # print(img)
    encode = base64.b64encode(img).decode('utf-8')
    # print(encode)
    return 'data:image/jpeg;base64,{}'.format(encode)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)
