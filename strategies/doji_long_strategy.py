import backtrader as bt
from .base_strategy import BaseStrategy
from backtrader import talib
from backtrader import Indicator, indicators

# Create a Stratey
# signal - doji candle, buy - next day opens higher than doji close
# stop - under the doji's low
# profit - half portion at stop distance, second half 3 times than doji size
class DojiLongStrategy(BaseStrategy):

    global pos_size


    def prepare_stock(self, stock):
        global pos_size
        pos_size = self.broker.cash/7
        stock.doji = talib.CDLDOJISTAR(stock.open, stock.high, stock.low, stock.close)
        stock.doji.plotinfo.plot = False
        stock.ma_short = indicators.EMA(stock, period=3)
        stock.ma_long = indicators.EMA(stock, period=8)


    def check_signals(self, stock):
        if self.open_signal(stock):
            self.open_position(stock)

    def manage_position(self, stock):
        None # todo improve take profit-1 and 2

    def open_signal(self, stock):
        if stock.doji[0] and stock.open[1] > stock.close[0] and stock.ma_short[0] < stock.ma_short[-1] and stock.close[1] > stock.ma_long[1]:
            return True

    def open_position(self, stock):
        entry = self.buy(data=stock, exectype=bt.Order.Market, transmit=False, size=max(1, int(pos_size/stock.open[0])))
        stoplost  = self.sell(data=stock, price=stock.low[0], 
            size=entry.size, exectype=bt.Order.Stop, transmit=False, parent=entry)
        takeprofit = self.sell(data=stock, price=stock.open[1] + stock.high[0] - stock.low[0], 
            size=entry.size, exectype=bt.Order.Limit, transmit=True, parent=entry)
