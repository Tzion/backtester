from strategies.base_strategy import BaseStrategy
from backtrader import talib
from backtrader.order import Order

class HighsLowsStructure(BaseStrategy):
    '''
    This is a pullback strategy based on the stracture created by highest highs
    and lowest lows.
    Positive signal when price breaks the N-highest high (for long) - 
    buy order on price low-2*ATR of the breakout candle.
    The order is valid for L days - to filter out weak movements.
    Take profit - on the breakout level.
    Stop loss - buy price - 2*ATR
    Shut off strategy when volatility is too high (VIX at top 25% values of last 100 candles)

    Based on https://youtu.be/QKCDt2QnmeM
    AmyBrokers code: https://drive.google.com/file/d/1kou9AiNnq1MKUhfUIw71PADeKOliWka2/view

    '''

    params = (
        ('atr_period', 20),
        ('highs_period', 63),
        ('entry_period', 10),
        ('ma_period', 25)
    )

    def prepare_stock(self, stock):
        stock.atr = talib.ATR(stock.high, stock.low, stock.close, timeperiod=self.p.atr_period)
        stock.highest_high = talib.MAX(stock, timeperiod=self.p.highs_period)
        stock.ma = talib.SMA(stock, timeperiod=self.p.ma_period)
        stock.entry_order = None
        

    
    def check_signals(self, stock):
        if stock.entry_order and stock.entry_order.active():
            stock.bars_from_signal += 1
            if stock.bars_from_signal >= self.p.entry_period:
                stock.entry_order.cancel()
        # elif stock.ma[0]-stock.ma[-1] > 0 and stock.close[0] > stock.highest_high[-1]:
        elif stock.high[0] > stock.highest_high[-1]:
            entry = self.buy(stock, exectype=Order.Limit, price=stock.low[0]-2*stock.atr[0], transmit=False)
            stoploss = self.sell(stock, exectype=Order.Stop, price=stock.low[0] - 4*stock.atr[0], parent=entry, transmit=False)
            takeprofit = stoploss = self.sell(stock, exectype=Order.Limit, price=stock.close[0], parent=entry, transmit=True)
            stock.entry_order = entry
            stock.bars_from_signal = 0
    

    def manage_position(self, stock):
        pass
        