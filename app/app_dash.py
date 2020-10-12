
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from api import app as server
import requests
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets, server=server)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    html.H1('Dash Camera'),
    html.Div([

        dcc.Input(
            id='ratation',
            type='number',
            placeholder='input rotation',
            value=90,
            debounce=True
        ),


        html.Button('Send', id='btn-send', n_clicks=0),
        html.Pre(id='configuration', style=styles['pre'])
    ], style={'display': 'inline-block'}),

    html.Img(id='img', src='/video_feed',
             style={'width': '50%', 'hight': '50%'}),
    html.Div(id='placeholder')
])


@app.callback(
    Output('configuration', 'children'),
    Input('btn-send', 'n_clicks')
)
def send(n_clicks):
    config = requests.get('http://localhost:8050/config').json()
    print(config)
    return json.dumps(config, indent=2)
    # return config


@app.callback(
    Output('placeholder', 'children'),
    Input('ratation', 'value'))
def rotation(value):
        result = requests.post('http://localhost:8050/config', json={'rotation':value})
        print(result.text)
        return value

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)
