
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from api import app as server

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets, server=server)


app.layout = html.Div([
    html.H1('Dash Camera'),
    html.Button('Send', id='btn-send', n_clicks=0),
    html.Img(id='img', src='/video_feed', style={'width':'53%', 'hight':'30%'}),
    html.Div(id='placeholder')
])


@app.callback(
    Output('placeholder', 'children'),
    Input('btn-send', 'n_clicks')
)
def send(n_clicks):
    print(n_clicks)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)
