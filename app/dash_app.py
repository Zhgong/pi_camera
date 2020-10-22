import dash
import dash_core_components as dcc
import dash_html_components as html
from api import app as server


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.6
    '''),
    html.Img(src="/video_feed")


    
])


if __name__ == '__main__':
    app.run_server(debug=False)