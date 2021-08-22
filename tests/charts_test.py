from backtrader.utils.dateintern import num2date
from test_common import *
import backtrader as bt
from datetime import date, datetime
from charts.charts import plot_feed
from utils.backtrader_helpers import extract_line_data as eld
from backtrader import indicators


class Strategy(bt.Strategy):
    def __init__(self):
        self.data.moving_average = indicators.SMA(self.data.close, period=14, subplot=False)
        self.data.atr= indicators.ATR(self.data, period=4, subplot=True)
        self.data.atr2= indicators.ATR(self.data, period=10, subplot=True)

def csv_test():
    data = bt.feeds.GenericCSVData(dataname='tests/test_data.csv', fromdate=datetime(2016, 7, 1), todate=datetime(2017,6,30), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(Strategy)
    strategy = cerebro.run()
    data = strategy[0].data
    dates = list(map(lambda fdate : num2date(fdate).date(), eld(data.datetime)))  # TODO overcome the date timestamp format issue
    overlay = eld(data.moving_average.line)
    subplot = eld(data.atr.line)
    plot_feed(dates, eld(data.open), eld(data.high), eld(data.low), eld(data.close), eld(data.volume), overlays_data=[overlay], subplots_data=[subplot])
    # cerebro.plot(style='candle')

def date_gap_test():
    data = bt.feeds.GenericCSVData(dataname='tests/test_data.csv', fromdate=datetime(2016, 12, 1), todate=datetime(2016,12,31), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(Strategy)
    strategy = cerebro.run()
    data = strategy[0].data
    dates = list(map(lambda fdate : num2date(fdate).date(), eld(data.datetime)))  # TODO overcome the date timestamp format issue
    overlay = eld(data.moving_average.line)
    subplot = eld(data.atr.line)
    plot_feed(dates, eld(data.open), eld(data.high), eld(data.low), eld(data.close), eld(data.volume), overlays_data=[overlay], subplots_data=[subplot])
    # cerebro.plot(style='candle')

def two_subplots_test():
    data = bt.feeds.GenericCSVData(dataname='tests/test_data.csv', fromdate=datetime(2016, 7, 1), todate=datetime(2017,6,30), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(Strategy)
    strategy = cerebro.run()
    data = strategy[0].data
    dates = list(map(lambda fdate : num2date(fdate).date(), eld(data.datetime)))  # TODO overcome the date timestamp format issue
    overlay = eld(data.moving_average.line)
    subplots = [eld(data.atr.line), eld(data.atr2.line)]
    plot_feed(dates, eld(data.open), eld(data.high), eld(data.low), eld(data.close), eld(data.volume), overlays_data=[overlay], subplots_data=subplots)
    # cerebro.plot(style='candle')

def two_charts_test():
    pass

def sample_test():
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

    plot_feed(dates, open_data, high_data, low_data, close_data, volume_data)

if __name__ == '__main__':
    two_subplots_test()
    # csv_test()