from strategies.base_strategy import BaseStrategy
from backtrader import talib
from backtrader.order import Order
from enum import Enum

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
        ('lows_period', 63),
        ('entry_period', 10),
        ('ma_period', 63)
    )
    


    def prepare_stock(self, stock):
        stock.atr = talib.ATR(stock.high, stock.low, stock.close, timeperiod=self.p.atr_period)
        stock.highs= talib.MAX(stock, timeperiod=self.p.highs_period)
        stock.lows = talib.MIN(stock, timeperiod=self.p.lows_period)
        stock.long_ma = talib.SMA(stock, timeperiod=self.p.highs_period)
        stock.short_ma = talib.SMA(stock, timeperiod=self.p.entry_period)
        stock.entry = None
        stock.direction = None

    def check_signals(self, stock):
        if self.entry_pending(stock):
            stock.bars_since_order += 1
            if self.entry_period_passed(stock) or self.opposite_breakout(stock):
                stock.entry.cancel()
        else:
            self.update_direction(stock)
            if self.breakout(stock):
                self.send_orders(stock)
    
    def entry_pending(self, stock):
        return stock.entry and stock.entry.active()
    
    def entry_period_passed(self, stock):
        return stock.bars_since_order >= self.p.entry_period

    def send_orders(self, stock):
        if stock.direction is Direction.LONG:
            stock.entry = self.buy(stock, exectype=Order.Limit, price=stock.low[0] - 2*stock.atr[0], transmit=False)
            stock.stoploss = self.sell(stock, exectype=Order.Stop, price=stock.low[0] - 4*stock.atr[0], parent=stock.entry, transmit=False)
            stock.takeprofit = self.sell(stock, exectype=Order.Limit, price=stock.high[0], parent=stock.entry, transmit=True)
        if stock.direction is Direction.SHORT:
            stock.entry = self.sell(stock, exectype=Order.Limit, price=stock.high[0] + 2*stock.atr[0], transmit=False)
            stock.stoploss = self.buy(stock, exectype=Order.Stop, price=stock.high[0] + 4*stock.atr[0], parent=stock.entry, transmit=False)
            stock.takeprofit = self.buy(stock, exectype=Order.Limit, price=stock.low[0], parent=stock.entry, transmit=True)
        stock.bars_since_order = 0

    def breakout(self, stock):
        if stock.direction is Direction.LONG:
            return stock.high[0] > stock.highs[-1]
        if stock.direction is Direction.SHORT:
            return stock.low[0] < stock.lows[-1]

    def opposite_breakout(self, stock):
        if stock.direction is Direction.LONG:
            return stock.low[0] < stock.lows[-1]
        if stock.direction is Direction.SHORT:
            return stock.high[0] > stock.highs[-1]

    def breakout1(self, stock, direction):
        if direction is Direction.LONG:
            return stock.low[0] < stock.lows[-1]
        if direction is Direction.SHORT:
            return stock.high[0] > stock.highs[-1]
    
    def update_direction(self, stock):
        if stock.long_ma[0] > stock.long_ma[-self.p.ma_period]:
            stock.direction = Direction.LONG
        else:
            stock.direction = Direction.SHORT

    def manage_position(self, stock):
        pass
        
    def notify_order(self, order, verbose=0):
        super().notify_order(order, verbose)

class Direction(Enum):
    SHORT = -1
    LONG = 1