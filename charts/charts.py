import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_feed(dates, open, high, low, close, volume, overlays_data=None, subplots_data=None, buy_markers=None, sell_markers=None):
    fig = create_ohlcv_figure(dates, open, high, low, close, volume, subplots_data=subplots_data)
    fig = add_overlay_plots(fig, dates, overlays_data)
    fig = add_subplots(fig, dates, subplots_data)
    fig = add_buysell_markers(fig, dates, buy_markers, sell_markers)

    # fig.update_layout(xaxis_type='category')  # workaround to handle gaps of dates when stock exchange is closed. movement isn't smooth when few subgraph - commented out for now
    config = dict({'scrollZoom': True})

    fig.show(config=config)


def create_ohlcv_figure(date, open, high, low, close, volume=None, subplots_data=None):
    subplots = 0 if not subplots_data else len(subplots_data)
    fig = make_subplots(specs=[[{"secondary_y": True}]] + [[{}]] * subplots, rows=1+subplots, cols=1, shared_xaxes='columns', vertical_spacing=0.01)

    prices_trace = go.Candlestick(x=date, open=open, high=high, low=low, close=close)
    fig.add_trace(prices_trace, secondary_y=False)
    fig.update_layout(yaxis1_side='right')
    if volume:
        volume_trace = go.Bar(x=date, y=volume, opacity=0.35)
        fig.add_trace(volume_trace, secondary_y=True)
        fig.update_layout(yaxis2_side='left')

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(dragmode='pan')  # when chart open the cursor uses for navigation
    return fig


def add_overlay_plots(figure: go.Figure, dates, overlays_data):
    if overlays_data:
        for overlay in overlays_data:
            figure.add_trace(go.Scatter(x=dates, y=overlay, mode='lines'))
    return figure


def add_subplots(figure: go.Figure, dates, subplots_data):
    if subplots_data:
        for i,subplot in enumerate(subplots_data):
            figure.add_trace(go.Scatter(x=dates, y=subplot, mode='lines+markers'), row=i+2, col=1)
    return figure


buy_marker_config =dict(color='green', size=10, symbol='arrow-bar-up')
sell_marker_config =dict(color='red', size=10, symbol='arrow-bar-down')

def add_buysell_markers(figure: go.Figure, dates, buy_prices, sell_prices):
    if buy_prices:
        figure.add_trace(go.Scatter(y=buy_prices, x=dates, mode='markers', marker=buy_marker_config))
    if sell_prices:
        figure.add_trace(go.Scatter(y=sell_prices, x=dates, mode='markers', marker=sell_marker_config))
    return figure


def plot_feed_volume_as_subplot(date, open, high, low, close, volume=None):
    fig = make_subplots(rows=1+bool(volume), cols=1, shared_xaxes=True)
    prices_trace = go.Candlestick(x=date, open=open, high=high, low=low, close=close)
    fig.add_trace(prices_trace, row=1, col=1)
    if volume:
        volume_trace = go.Bar(x=date, y=volume)
        fig.add_trace(volume_trace, row=2, col=1)

    fig.update_layout(dragmode='pan')  # when chart open the cursor uses for navigation
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_layout(xaxis_type='category')  # workaround to handle gaps of dates when stock exchange is closed

    fig.show()

