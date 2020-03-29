import backtrader as bt
import datetime  # For datetime objects
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
