
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from api import app as server
import camera
import continues
# import requests
import json
import dash2recording

cam_config = camera.get_config()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets, server=server)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

available_resolutions = ["640x480", "1024x768", "1280x720"]
app.title = "Cameraeye"
app.layout = html.Div([
    html.H1('Raspberry Pi Camera eye'),
    html.Div([

        dcc.Input(
            id='rotation',
            type='number',
            placeholder='input rotation',
            value=cam_config["rotation"],
            debounce=True
        ),

        dcc.Input(
            id='framerate',
            type='number',
            placeholder='input framerate',
            value=cam_config["framerate"],
            min=1,
            max=30,
            debounce=True
        ),

        dcc.Dropdown(
            id='resolution',
            options=[{'label': i, 'value': i} for i in available_resolutions],
            value=cam_config["resolution"]
        ),

        html.Button('Save', id='btn-save', n_clicks=0),
    ], style={'width': '300px', 'float': 'left'}),



    html.Div([
        html.Img(id='img', src='/video_feed',
                 style={'width': '50%', 'hight': '50%'}),
    ]),

    html.Div(id='placeholder'),
    html.Div(id='placeholder2'),
    html.Div(id='placeholder3'),
    html.Div(id='placeholder4')
])


@app.callback(
    Output('placeholder', 'value'),
    Input('btn-save', 'n_clicks'),
    State('rotation', 'value'),
    State('resolution', 'value'),
    State('framerate', 'value'),
    prevent_initial_call=True
)
def save(n_clicks, rotation, resolution, framerate):
    return dash2recording.save_config({
            "rotation":rotation, 
            "resolution":resolution, 
            "framerate":framerate
            })



if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=80, debug=False)


