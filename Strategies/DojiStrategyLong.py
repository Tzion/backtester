from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
from backtrader import indicators

# Create a Stratey
# signal - doji candle, buy - next day opens higher than doji close
# stop - under the doji's low
# profit - half portion at stop distance, second half 3 times than doji size
class DojiLongStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.close= self.datas[0].close
        self.open = self.datas[0].open
        self.high= self.datas[0].high
        self.low= self.datas[0].low
        self.atr = indicators.ATR(self.datas[0])
        self.tr = indicators.TR(self.datas[0])

    def is_doji(self, index=0):
        return True if (abs(self.open - self.close) <= 0.02) and self.tr[index] > 3 * self.atr[index] else False 

    def next(self):
        if self.position:
            self.manage_position()
            return
        elif self.open_signal():
            self.open_position()


    def open_signal(self):
        if self.is_doji(-1) and self.open[0] > self.open[-1]:
            self.log('open signal')
            return True

    def open_position(self):
        mainside = self.buy(exectype=bt.Order.Market, transmit=False)
        lowside  = self.sell(price=self.low[-1], size=mainside.size, exectype=bt.Order.Stop, transmit=False, parent=mainside)
        highside = self.sell(price=self.high[-1], size=mainside.size, exectype=bt.Order.Limit, transmit=True, parent=mainside)

    def manage_position(self):
        None # todo improve take profit-1 and 2


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(DojiLongStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../data_feeds/AEP.csv')

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2000, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2018, 3, 10),
        reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()
    cerebro.plot()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
