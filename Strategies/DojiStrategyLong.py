import backtrader as bt
from .BaseStrategy import BaseStrategy

# Create a Stratey
# signal - doji candle, buy - next day opens higher than doji close
# stop - under the doji's low
# profit - half portion at stop distance, second half 3 times than doji size
class DojiLongStrategy(BaseStrategy):
    
    def check_signals(self, stock):
        if self.open_signal(stock):
            self.open_position(stock)

    def manage_position(self, stock):
        None # todo improve take profit-1 and 2

    def open_signal(self, stock):
        if is_doji(stock) and stock.open[0] > stock.open[-1]:
            self.log(stock, 'open signal')
            return True

    def open_position(self, stock):
        mainside = self.buy(exectype=bt.Order.Market, transmit=False)
        lowside  = self.sell(price=stock.low[-1], 
            size=mainside.size, exectype=bt.Order.Stop, transmit=False, parent=mainside)
        highside = self.sell(price=stock.high[-1], 
            size=mainside.size, exectype=bt.Order.Limit, transmit=True, parent=mainside)

    global is_doji  # move to external file, or find candles utils
    def is_doji(stock, bar_i=0):
        return abs(stock.open[bar_i] - stock.close[bar_i]) <= 0.2 and stock.tr[bar_i] > 1 * stock.atr[bar_i]
