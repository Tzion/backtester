import dash
from dash import dcc
from dash import html
import os

from dash.dependencies import Input, Output
from charts import CHARTS_DIR, TRADES_DIR, OBSERVERS_DIR

ASSETS_PATH = CHARTS_DIR
app = dash.Dash(__name__, assets_folder='../' + ASSETS_PATH)


app.layout = html.Div(children=[
    html.H1(children='Strategy Dashboard'),
    html.Div(children=[
        html.H2('Trades'),
        html.Div(id='trade-list', children=[]),
        dcc.Interval(id='trade-list-interval', interval=4000, n_intervals=0)
        ]
    ),
    html.Div(children=[
        html.H2('Observers'),
        html.Div(id='observers-frames', children=
            [html.Iframe(id=file, src=app.get_asset_url(os.path.join(OBSERVERS_DIR.removeprefix(ASSETS_PATH),file)) ,width='1200vm', height='800vh') for file in os.listdir(OBSERVERS_DIR)]),
    ]),
])

# TODO the callback should be triggered by invocation rather than time span (listener on the file system)
@app.callback(Output('trade-list', 'children'), Input('trade-list-interval', 'n_intervals'))
def update_trade_list(n):
    return [html.A(children=[file_name, html.Br()], href=app.get_asset_url(os.path.join(TRADES_DIR.removeprefix(ASSETS_PATH), file_name))) for file_name in os.listdir(TRADES_DIR)]

if __name__ == '__main__':
    app.run_server(debug=True)