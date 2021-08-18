import plotly.express as px
import backtrader as bt


def pnl_to_trade_length(trades: list[bt.Trade]):
    pnls = [t.pnl for t in trades]
    bars = [t.barlen for t in trades]
    fig = px.scatter(x=bars, y=pnls)
    fig.show()
