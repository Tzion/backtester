import backtrader as bt
from datetime import datetime

class DummyStrategy(bt.Strategy):
    pass

DATA = bt.feeds.GenericCSVData(dataname='tests/test_data.csv', fromdate=datetime(2016, 7, 1), todate=datetime(2017,6,30), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)
cerebro = bt.Cerebro()
cerebro.adddata(DATA)
cerebro.addstrategy(DummyStrategy)
strategy = cerebro.run()
cerebro.plot(style='candle')
