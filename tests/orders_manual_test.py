import backtrader as bt
import pandas as pd
from backtrader.feeds.pandafeed import PandasData
import numpy as np

# This class is to observe the behaviour of trailing stop orders
class StopTrailTest(bt.Strategy):
    def next(self):
        if not self.getposition():
            entry = self.buy(price=11, exectype=bt.Order.Limit)
            self.sell(exectype=bt.Order.StopTrail, trailamount=.5)

prices = np.tile([10,11,12,11.5,11.2,15,14,13,14,15],(7,1)).transpose()
DATA = PandasData(dataname=pd.DataFrame(data=prices, columns=PandasData.datafields, index=pd.date_range('20210818', periods=10)))
cerebro = bt.Cerebro()
cerebro.adddata(DATA)
cerebro.addstrategy(StopTrailTest)
strategy = cerebro.run()
cerebro.plot()