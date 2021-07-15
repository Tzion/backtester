from backtrader import indicators
from backtrader.indicator import LinePlotterIndicator
from money_mgmt.sizers import LongOnlyPortionSizer, PortionSizer
from strategies.base_strategy import BaseStrategy
from backtrader import talib
import backtrader as bt
from backtrader.order import Order
from enum import Enum

class Direction(Enum):
    SHORT = -1
    LONG = 1

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

    Inspired by https://youtu.be/QKCDt2QnmeM
    AmyBrokers code: https://drive.google.com/file/d/1kou9AiNnq1MKUhfUIw71PADeKOliWka2/view

    Latest backtesting status: the trades are centerilzed around few months around the end of 2018 till
    the begining of 2019. win rate is about 50%.
    Improvements required:
    1. take profits 1 and 2
    2. decide Long/Short direction
    3. stop logic - trades go the right direction cannot loose money
    4. adjust the submitted orders during the entry period - update prices according to changes in the ATR
    5. adjust ask prices according to candle signals (for example possitive candle occurs around the asked price - support of opening position even for higher price)
    6. trade in the trend of the market only
    7. use VIX to filter trades
    '''

    params = (
        ('atr_period', 20),
        ('highs_period', 63),
        ('lows_period', 63),
        ('entry_period', 10),
        ('ma_period', 63)
    )
    
    allowed_directions = [Direction.SHORT, Direction.LONG]

    def prepare_stock(self, stock):
        stock.atr = talib.ATR(stock.high, stock.low, stock.close, timeperiod=self.p.atr_period)
        stock.highs= talib.MAX(stock, timeperiod=self.p.highs_period)
        stock.lows = talib.MIN(stock, timeperiod=self.p.lows_period)
        stock.highs_trend= talib.MAX(stock, timeperiod=self.p.atr_period)
        stock.lows_trend = talib.MIN(stock, timeperiod=self.p.atr_period)
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
            if stock.direction not in self.allowed_directions:
                return
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
        self.log(stock, "orders sent, %s trade. asked price: %.2f, take-profit: %.2f, stop-loss: %.2f"%(stock.direction, stock.entry.price, stock.takeprofit.price, stock.stoploss.price))
        stock.bars_since_order = 0

    def breakout(self, stock):
        # TODO try to use close price instead of high/low
        if stock.direction is Direction.LONG:
            return stock.high[0] > stock.highs[-1]
        if stock.direction is Direction.SHORT:
            return stock.low[0] < stock.lows[-1]

    def opposite_breakout(self, stock):
        if stock.direction is Direction.LONG:
            return stock.low[0] < stock.lows[-1]
        if stock.direction is Direction.SHORT:
            return stock.high[0] > stock.highs[-1]

    def update_direction(self, stock):
        # TODO improve this!
        if stock.long_ma[0] > stock.long_ma[-self.p.ma_period]:
            stock.direction = Direction.LONG
        elif stock.long_ma[0] < stock.long_ma[-self.p.ma_period]:
            stock.direction = Direction.SHORT
        else:
            stock.direction = None

    def manage_position(self, stock):
        pass
        
    def notify_order(self, order, verbose=0):
        super().notify_order(order, verbose)



class HighLowsStructureImproved(BaseStrategy):

    params = (
        ('atr_period', 20),
        ('highs_period', 63),
        ('entry_period', 10),
    )

    def prepare_stock(self, stock):
        stock.atr = talib.ATR(stock.high, stock.low, stock.close, timeperiod=self.p.atr_period)
        stock.highs= talib.MAX(stock.high, timeperiod=self.p.highs_period)
        stock.highs_breakout = HighestHighBreakoutSignal(period=self.p.highs_period)
        stock.entry, stock.stoploss, stock.takeprofit = None, None, None
        stock.bars_since_signal = None

    def check_signals(self, stock):
        return False
        if self.buy_signal(stock):
            stock.entry = self.buy(stock, exectype=Order.Limit, price=stock.buy_level[0], transmit=False)
            stock.stoploss = self.sell(stock, exectype=Order.Stop, price=stock.low[0] - 4*stock.atr[0], parent=stock.entry, transmit=False)
            stock.takeprofit = self.sell(stock, exectype=Order.Limit, price=stock.high[0], parent=stock.entry, transmit=True)
            stock.bars_since_signal = 0
    
    def update_orders(self, stock):
        if stock.entry: 
            if stock.entry.alive():
                # stock.entry.cancel()
                # stock.entry = self.buy(stock, exectype=Order.Limit, price=stock.buy_level[0], transmit=False)
                stock.bars_since_signal += 1
            else:
                stock.entry, stock.stoploss, stock.takeprofit = None, None, None
                stock.bars_since_signal = None
        

    def buy_signal(self, stock):
        return stock.high[0] > stock.highs[-1]
        

    def manage_position(self, stock):
        pass

    def notify_order(self, order, verbose=0):
        super().notify_order(order, verbose)


class HighestHighBreakoutSignal(bt.Indicator):
    lines = ('breakout',)
    params = (('period', 63),)
    plotinfo = dict(plot=True, subplot=False, plotlinelabels=True)
    plotlines = dict(breakout=dict(
        marker='d', markersize=8.0, color='springgreen')
        )

    def __init__(self):
        self.highest = indicators.Highest(self.data.high, period=self.p.period, plot=False)

    def next(self):
        self.lines.breakout[0] =  self.data.high[0] if self.data.high[0] > self.highest[-1] else float('nan')
