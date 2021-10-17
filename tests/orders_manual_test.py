from test_common import *
import backtrader as bt
import pandas as pd
from backtrader.feeds.pandafeed import PandasData
import numpy as np

# This class is to observe the behaviour of trailing stop orders
class StopTrailTest(bt.Strategy):
    def next(self):
        if not self.getposition():
            entry = self.buy(price=11, exectype=bt.Order.Limit)
            self.sell(exectype=bt.Order.StopTrail,price=10, trailamount=2)

if __name__ == '__main__':
    prices = np.tile([10,11,10,10.2,9.2,9.0,9.1,10,13,14],(7,1)).transpose()
    DATA = PandasData(dataname=pd.DataFrame(data=prices, columns=PandasData.datafields, index=pd.date_range('20210818', periods=10)))
    cerebro = bt.Cerebro()
    cerebro.adddata(DATA)
    cerebro.addstrategy(StopTrailTest)
    strategy = cerebro.run()
    cerebro.plot()