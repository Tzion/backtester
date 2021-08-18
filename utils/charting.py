from bokeh.plotting import show, figure
import backtrader as bt


def pnl_to_trade_length(trades: list[bt.Trade]):
    pnls = [t.pnl for t in trades]
    bars = [t.barlen for t in trades]
    chart = figure(title="PnL to bars", x_axis_label='trade length (bars)', y_axis_label='profit and loss')
    chart.scatter(x=bars, y=pnls)
    show(chart)
