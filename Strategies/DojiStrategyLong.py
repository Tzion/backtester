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
        self.close, self.open, self.high, self.low = [], [], [], []
        self.atr, self.tr = [], []
        for i,d in enumerate(self.datas):
            self.close.append(d.close)
            self.open.append(d.open)
            self.high.append(d.high)
            self.low.append(d.low)
            self.atr.append(indicators.ATR(d))
            self.tr.append(indicators.TR(d))

    def is_doji(self, i, j=0):
        return True if (abs(self.open[i][j] - self.close[i][j]) <= 0.2) and self.tr[i][j] > 1 * self.atr[i][j] else False 

    def next(self):
        for i,data in enumerate(self.datas):
            if self.position:
                self.manage_position()
                return
            elif self.open_signal(i):
                self.open_position()


    def open_signal(self, data_index):
        if self.is_doji(data_index) and self.open[data_index][0] > self.open[data_index][-1]:
            self.log('open signal')
            return True

    def open_position(self):
        mainside = self.buy(exectype=bt.Order.Market, transmit=False)
        lowside  = self.sell(price=self.low[-1], size=mainside.size, exectype=bt.Order.Stop, transmit=False, parent=mainside)
        highside = self.sell(price=self.high[-1], size=mainside.size, exectype=bt.Order.Limit, transmit=True, parent=mainside)

    def manage_position(self):
        None # todo improve take profit-1 and 2
