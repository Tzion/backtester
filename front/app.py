import dash
from dash import dcc
from dash import html
import os

from dash.dependencies import Input, Output
from charts import CHARTS_DIR

app = dash.Dash(__name__, assets_folder='../' + CHARTS_DIR)


app.layout = html.Div(children=[
    html.H1(children='Strategy Dashboard'),
    html.Div(children=[
        html.H2('Trades'),
        html.Div(id='trade-list', children=[]),
        dcc.Interval(id='trade-list-interval', interval=1000, n_intervals=0)
        ]
    ),
    html.Div(children=[
        html.H2('Observers'),
        html.Iframe(id='graph', src=app.get_asset_url(os.listdir(CHARTS_DIR)[0]), width='100%', height='300px'),
    ]),
])

@app.callback(Output('trade-list', 'children'), Input('trade-list-interval', 'n_intervals'))
def update_trade_list(n):
    return [html.A(children=[file_name, html.Br()], href=app.get_asset_url(file_name)) for file_name in os.listdir(CHARTS_DIR)]

if __name__ == '__main__':
    app.run_server(debug=True)