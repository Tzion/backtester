import plotly.graph_objects as go
from datetime import datetime
from plotly.subplots import make_subplots


def plot_feed(date, open, high, low, close, volume):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    prices_trace = go.Candlestick(x=date, open=open, high=high, low=low, close=close)
    fig.add_trace(prices_trace, secondary_y=False)
    volume_trace = go.Bar(x=date, y=volume)
    fig.add_trace(volume_trace, secondary_y=True)

    fig.update_layout(xaxis_type='category')  # workaround to handle gaps of dates when stock exchange is closed
    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.show()

def plot_feed2(date, open, high, low, close, volume):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

    prices_trace = go.Candlestick(x=date, open=open, high=high, low=low, close=close)
    fig.add_trace(prices_trace, row=1, col=1)
    volume_trace = go.Bar(x=date, y=volume)
    fig.add_trace(volume_trace, row=2, col=1)

    # fig.update_layout(xaxis_type='category')  # workaround to handle gaps of dates when stock exchange is closed
    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.show()


