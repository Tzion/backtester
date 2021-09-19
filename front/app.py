import dash
# import dash_html_components as html
from dash import html
import os
from globals import CHARTS_DIR

app = dash.Dash(__name__, assets_folder='../'+CHARTS_DIR)


chart_links = [html.A(children=[file_name, html.Br()], href='assets/'+ file_name) for file_name in os.listdir(CHARTS_DIR)]
app.layout = html.Div(children=[
    html.H1(children='Charts'),
    html.Div(children=chart_links),
])

if __name__ == '__main__':
    app.run_server(debug=True)