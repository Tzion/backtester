import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import logger
from charts import TRADES_DIR, OBSERVERS_DIR

"""
This module creates interactive candlestick financial charts of data feeds using Plotly.

TODO:
    1. Block pan navigation in price chart to go below zero. (waiting for feature - https://github.com/plotly/plotly.js/issues/1876 - expected api: layout.yaxis_rangemode='visible')
    2.  1. Color volume bars in red-green
        2. Set range of the volume bar to be ~40% of the prices (see layout.yaxis.range)
    3. Remove gaps of non-trading days in the X axis
    4. Support intra-day charting
    5. Support in super-complex (few plot lines of different type) indicators (macd-histo: lines and bar)
    6. Support in plotting strategy observers (e.g. cash, drawdown)
"""

@dataclass
class Line:
    data: list[float]
    metadata: dict[str,str] = field(default_factory=dict)

    def __init__(self, data, metadata):
        self.data = data
        self.execution_data = dict()
        for key in list(metadata):
            if key.startswith('_'):
                self.execution_data[key] = metadata.pop(key)
        self.metadata = metadata

@dataclass
class LinesData:
    name: str
    lines : dict[str,Line] = field(default_factory=dict)

@dataclass
class ChartData:
    # __slots__ = ('name', 'dates', 'open', 'high', 'low', 'close' 'volume', 'overlays_data', 'subplots_data', 'buy_markers', 'sell_markers')
    name: str
    dates: list[datetime]
    open: list[float]
    high: list[float] 
    low: list[float]
    close: list[float]
    volume: list[float]
    overlays_data: list[LinesData]
    subplots_data: list[LinesData]
    buy_markers: Optional[list[float]] = None
    sell_markers: Optional[list[float]] = None

config = dict({'scrollZoom': True})

def plot_price_chart(chart_data: ChartData, show, save_to_file):
    d = chart_data
    figure = _plot_feed(d.name, d.dates, d.open, d.high, d.low, d.close, d.volume, d.overlays_data, d.subplots_data, d.buy_markers, d.sell_markers, show, save_to_file)
    return figure

def plot_duration_to_profit(trade_duration: list, profit: list, show, save_to_file):
    if len(trade_duration) > 0:
        name = 'TradeDurationToProfit'
        fig = px.scatter(title=name, y=trade_duration, x=profit)
        _show_and_save(fig, name, OBSERVERS_DIR, show, save_to_file)
        return fig

def plot_lines(name, show, save_to_file, **lines):
    # TODO improve visibility of x values (currently array indecies)
    fig = go.Figure()
    for line,data in lines.items():
        fig.add_trace(go.Scatter(name=line, y=data, mode='markers' if any([val != val for val in data]) else 'lines'))
    fig.update_layout(title=name)
    _show_and_save(fig, name, OBSERVERS_DIR, show, save_to_file)
    return fig


def _plot_feed(name, dates, open, high, low, close, volume, overlays_data, subplots_data, buy_markers, sell_markers, show, save_to_file):
    dates = list(map(lambda datetime: datetime.replace(microsecond=0), dates))  # trim microsecond to handle rounding error that cause the data point to have the date of the next day
    fig = _create_ohlcv_figure(name, dates, open, high, low, close, volume, subplots_data=subplots_data)
    fig = _add_overlay_plots(fig, dates, overlays_data)
    fig = _add_subplots(fig, dates, subplots_data)
    fig = _add_buysell_markers(fig, dates, buy_markers, sell_markers)

    # fig.update_layout(xaxis_type='category')  # workaround to handle gaps of dates when stock exchange is closed. movement isn't smooth when few subgraph - commented out for now

    _config_cursor(fig)
    fig.update_layout(xaxis_rangeslider_visible=False, title=name + ' ' + str(datetime.now()))
    fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.01,xanchor="left",x=0.01))
    _show_and_save(fig, name, TRADES_DIR, show, save_to_file)
    return fig

def _show_and_save(fig, name, path, show, save):
    if show:
        logger.logdebug(f'showing chart of {name}')
        fig.show()
    if save:
        file_path = f'{path}/{name}.html'
        logger.logdebug(f'saving chart file {file_path}')
        fig.write_html(file=file_path, config=config)

def _create_ohlcv_figure(name, date, open, high, low, close, volume=None, subplots_data=None):
    subplots = 0 if not subplots_data else len(subplots_data)
    fig = make_subplots(specs=[[{"secondary_y": True}]] + [[{}]] * subplots, rows=1+subplots, cols=1, shared_xaxes='columns', vertical_spacing=0.01,
                        row_width=[1] * subplots + [4])

    prices_trace = go.Candlestick(x=date, open=open, high=high, low=low, close=close, name=name)
    fig.add_trace(prices_trace, secondary_y=False)
    fig.update_layout(yaxis1_side='right')
    if volume:
        volume_trace = go.Bar(x=date, y=volume, opacity=0.35, showlegend=False)
        fig.add_trace(volume_trace, secondary_y=True)
        fig.update_layout(yaxis2_side='left')
    return fig


def _add_overlay_plots(figure: go.Figure, dates, overlays_data:Optional[list[LinesData]]):
    if overlays_data:
        for overlay in overlays_data:
            for _,line in overlay.lines.items():
                figure.add_trace(go.Scatter(x=dates, y=line.data, name=overlay.name, **line.metadata))
    return figure


def _add_subplots(figure: go.Figure, dates, subplots_data:Optional[list[LinesData]]):
    if subplots_data:
        for i,subplot in enumerate(subplots_data):
            for _,line in subplot.lines.items():
                figure.add_trace(go.Scatter(x=dates, y=line.data, name=subplot.name, **line.metadata), row=i+2, col=1)
    return figure


buy_marker_config =dict(color='green', size=10, symbol='arrow-bar-up')
sell_marker_config =dict(color='red', size=10, symbol='arrow-bar-down')

def _add_buysell_markers(figure: go.Figure, dates, buy_prices, sell_prices):
    if buy_prices:
        figure.add_trace(go.Scatter(y=buy_prices, x=dates, mode='markers', marker=buy_marker_config, showlegend=False, name='buy'))
    if sell_prices:
        figure.add_trace(go.Scatter(y=sell_prices, x=dates, mode='markers', marker=sell_marker_config, showlegend=False, name='sell'))
    return figure


def _config_cursor(figure):
    figure.update_xaxes(showspikes=True, spikemode='across', spikesnap='cursor', spikecolor="black",spikethickness=0.4)
    figure.update_yaxes(showspikes=True, spikemode='across', spikesnap='cursor', spikecolor="black",spikethickness=0.4)
    figure.update_layout(dragmode='pan')  # when chart open the cursor uses for navigation

def _plot_feed__volume_as_subplot(date, open, high, low, close, volume=None):
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