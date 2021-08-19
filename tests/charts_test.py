from test_common import *
import backtrader as bt
from datetime import datetime
from charts.charts import plot_feed
from utils.backtrader_helpers import extract_line_data as eld


DATA = bt.feeds.GenericCSVData(dataname='tests/test_data.csv', fromdate=datetime(2016, 7, 1), todate=datetime(2017,6,30), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)
cerebro = bt.Cerebro()
cerebro.adddata(DATA)
cerebro.addstrategy(DummyStrategy)
strategy = cerebro.run()

data = strategy[0].data
plot_feed(eld(data.datetime), eld(data.open), eld(data.high), eld(data.low), eld(data.close), eld(data.volume))

