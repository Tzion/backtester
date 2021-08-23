from backtrader.utils.dateintern import num2date
from backtrader_plotting.bokeh.bokeh import Bokeh
from backtrader_plotting.schemes.tradimo import Tradimo
from test_common import *
import backtrader as bt
from datetime import date, datetime
from charts.charts import plot_feed
from utils.backtrader_helpers import extract_line_data as eld, extract_date_line_data as edld
from backtrader import indicators
import backtest

class Strategy(bt.Strategy):
    def __init__(self):
        for data in self.datas:
            data.moving_average = indicators.SMA(data.close, period=14, subplot=False)
            data.atr= indicators.ATR(data, period=4, subplot=True)
            data.atr2= indicators.ATR(data, period=10, subplot=True)

def setup_and_run_strategy(data):
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(Strategy)
    strategy = cerebro.run()
    return strategy[0].data

def single_data_test():
    data = setup_and_run_strategy(data = bt.feeds.GenericCSVData(dataname='tests/test_data.csv', fromdate=datetime(2016, 7, 1), todate=datetime(2017,6,30), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5))
    dates = edld(data.datetime)
    overlay = eld(data.moving_average.line)
    subplot = eld(data.atr.line)
    plot_feed(dates, eld(data.open), eld(data.high), eld(data.low), eld(data.close), eld(data.volume), overlays_data=[overlay], subplots_data=[subplot])
    # cerebro.plot(style='candle')

def date_gap_test():
    data = setup_and_run_strategy(data = bt.feeds.GenericCSVData(dataname='tests/test_data.csv', fromdate=datetime(2016, 12, 1), todate=datetime(2016,12,31), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5))
    overlay = eld(data.moving_average.line)
    subplot = eld(data.atr.line)
    plot_feed(edld(data.datetime), eld(data.open), eld(data.high), eld(data.low), eld(data.close), eld(data.volume), overlays_data=[overlay], subplots_data=[subplot])

def two_subplots_test():
    data = setup_and_run_strategy(bt.feeds.GenericCSVData(dataname='tests/test_data.csv', fromdate=datetime(2016, 7, 1), todate=datetime(2017,6,30), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5))
    overlay = eld(data.moving_average.line)
    subplots = [eld(data.atr.line), eld(data.atr2.line)]
    plot_feed(edld(data.datetime), eld(data.open), eld(data.high), eld(data.low), eld(data.close), eld(data.volume), overlays_data=[overlay], subplots_data=subplots)

def two_charts_test():
    pass

def performance_test():
    cerebro = backtest.gb.cerebro
    backtest.add_data(limit=10, random=False, start_date=datetime(2016,11,30), end_date=datetime(2021, 4, 26), dirpath='../data_feeds')
    cerebro.addstrategy(Strategy)
    strategy = cerebro.run()
    for data in strategy[0].datas:
        overlay = eld(data.moving_average.line)
        subplots = [eld(data.atr.line), eld(data.atr2.line)]
        plot_feed(edld(data.datetime), eld(data.open), eld(data.high), eld(data.low), eld(data.close), eld(data.volume), overlays_data=[overlay], subplots_data=subplots)


def bokeh_test():
    cerebro = backtest.gb.cerebro
    backtest.add_data(limit=1, random=False, start_date=datetime(2016,11,30), end_date=datetime(2021, 4, 26), dirpath='../data_feeds')
    cerebro.addstrategy(Strategy)
    strategy = cerebro.run()
    strategy[0].data.plotinfo.plot=True
    plotter = Bokeh(style='bar', scheme=Tradimo())
    cerebro.plot(plotter=plotter, style='candlestick', barup='green', numfigs=1)

def sample_test():
    open_data = [33.0, 33.3, 33.5, 33.0, 34.1]
    high_data = [33.1, 33.3, 33.6, 33.2, 34.8]
    low_data = [32.7, 32.7, 32.8, 32.6, 32.8]
    close_data = [33.0, 32.9, 33.3, 33.1, 33.1]
    volume_data = [10, 2, 12, 42, 1, 43]
    dates = [datetime(year=2013, month=10, day=10), datetime(year=2013, month=11, day=10), datetime(year=2013, month=12, day=10), datetime(year=2014, month=1, day=10), datetime(year=2014, month=2, day=10)]

    plot_feed(dates, open_data, high_data, low_data, close_data, volume_data)

if __name__ == '__main__':
    single_data_test()
    sample_test()
    two_subplots_test()
    date_gap_test()