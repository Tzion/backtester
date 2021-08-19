import plotly.graph_objects as go
from datetime import datetime
from plotly.subplots import make_subplots

open_data = [33.0, 33.3, 33.5, 33.0, 34.1]
high_data = [33.1, 33.3, 33.6, 33.2, 34.8]
low_data = [32.7, 32.7, 32.8, 32.6, 32.8]
close_data = [33.0, 32.9, 33.3, 33.1, 33.1]
volume_data = [10, 2, 12, 42, 1, 43]
dates = [datetime(year=2013, month=10, day=10),
         datetime(year=2013, month=11, day=10),
         datetime(year=2013, month=12, day=10),
         datetime(year=2014, month=1, day=10),
         datetime(year=2014, month=2, day=10)]

def plot_feed(date, open, high, low, close, volume):
    fig_data = [go.Candlestick(x=date, open=open, high=high, low=low, close=close)]
    fig = go.Figure(data=fig_data)
    fig.show()


plot_feed(dates, open_data, high_data, low_data, close_data, volume_data)