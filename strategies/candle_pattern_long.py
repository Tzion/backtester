
from __future__ import annotations
from money_mgmt.sizers import RiskBasedWithMaxPortionSizer
from backtrader import talib
from backtrader.order import Order

from strategies.trade_state_strategy import TradeState, TradeStateStrategy
from backtrader import indicators
from globals import *
from logger import *
from custom_indicators import visualizers


class CandlePatternLong(TradeStateStrategy):
    
    params = {
        'atr_period': 13,
        'highs_period': 37,
        'ema_fast': 21,
        'ema_meduim': 40,
        'ema_slow': 100,

    }

    def __init__(self):
        super().__init__()
        self.setsizer(RiskBasedWithMaxPortionSizer(risk_per_trade_percents=3.0, max_portion_percents=28))

    def prepare_feed(self, feed):
        feed.atr = talib.ATR(feed.high,feed.low,feed.close, timeperiod=self.p.atr_period, plot=False)
        feed.tr = talib.ATR(feed.high,feed.low,feed.close, timeperiod=1, plot=False)
        feed.doji_star = talib.CDLDOJISTAR(feed.open, feed.high, feed.low, feed.close, plot=False) 
        feed.highest = indicators.Highest(feed.high, period=self.p.highs_period, subplot=False)
        feed.lowest = indicators.Lowest(feed.low, period=self.p.highs_period, subplot=False)
        feed.highest_breakout = feed.high > feed.highest(-1)
        feed.doji_star_marker = visualizers.SingleMarker(signals=feed.doji_star, level=feed.low*.985, color='purple', marker='H', plotmaster=feed, markersize=7) 
        feed.highest_breakout_marker = visualizers.SingleMarker(signals=feed.highest_breakout, level=feed.high*1.02 ,plotmaster=feed, color='orange', markersize=6, plot=False)
        feed.open.extend(size=1)
        feed.high.extend(size=1)
        feed.low.extend(size=1)
        feed.close.extend(size=1)

        # trend analysis
        feed.ema_fast = indicators.EMA(feed.close, period=self.p.ema_fast, plot=True)
        feed.ema_meduim = indicators.EMA(feed.close, period=self.p.ema_meduim, plot=True)
        feed.ema_slow = indicators.EMA(feed.close, period=self.p.ema_slow, plot=True)
        feed.trend_line = bt.And((feed.ema_fast > feed.ema_meduim),(feed.ema_meduim > feed.ema_slow)) - bt.And((feed.ema_fast < feed.ema_meduim),(feed.ema_meduim < feed.ema_slow))
        feed.trend = indicators.MovingAverageSimple(feed.trend_line, period=1, plot=True, plotmaster=feed, subplot=True) # using MA with period=1 as a workaround to be able to plot trend_line


    def initial_state_cls(self):
        return self.LookForEntry
    
    def notify_trade(self, trade: bt.Trade):
        super().notify_trade(trade)
        if trade.isclosed:
            self.change_state(trade.data.state, self.LookForEntry(self, trade.data))
    
    def notify_order(self, order: bt.Order):
        super().notify_order(order)
        order.data.state.next_state(order)
        if isinstance(order.data.state, self.Tp2) and order.status is Order.Completed:
            loginfo(f'take profit 2 done by {order.getordername()} order')

    def market_downtrend(self):
        index = self.getdatabyname('^GSPC')
        return index.trend == -1
    
    def risk_factor(self):
        index = self.getdatabyname('^GSPC')
        if index.trend == -1:
            risk = 3
        elif index.trend == 0:
            risk = 2
        else:
            risk =1
        return risk

    class LookForEntry(TradeState):
        def next(self):
            if self.strategy.getposition(self.feed):
                return
            volatility = 1.4*self.feed.atr[0]
            if (
                self.feed.doji_star[0] > 0 
                and self.feed.open[1] > self.feed.low[0]
                and self.feed.lowest[-1] + self.feed.atr[0]/3 >= self.feed.low[0] >= self.feed.lowest[-1]
                # and self.feed.ema_very_fast[0] > self.feed.ema_fast[0] > self.feed.ema_slow[0]
                # and self.feed.ema_very_fast[0] < self.feed.ema_very_fast[-1] < self.feed.ema_very_fast[-2]
                and self.feed.tr[0] >= self.feed.atr[-1] * 1
                # and self.feed.open[1] - self.feed.close[0] > self.feed.atr[0] * .2
                # and self.feed.trend[0] > -1 
                ):
                stopprice = self.feed.low[0] - volatility
                risk = self.feed.open[1] - stopprice
                self.feed.risk = lambda : (self.feed.open[1] - stopprice) * self.strategy.risk_factor()

                self.entry = self.strategy.buy(self.feed, exectype=Order.Market, transmit=False)
                self.stoploss = self.strategy.sell(self.feed, exectype=Order.StopTrail, price=stopprice, parent=self.entry, transmit=False, trailamount=volatility)
                self.takeprofit = self.strategy.sell(self.feed, exectype=Order.Limit, price=self.feed.open[1] + 1*volatility, parent=self.entry, transmit=True, size=self.strategy.getsizing(self.feed)/2)
                return


        def next_state(self, order: bt.Order):
            if self.entry and order.ref == self.entry.ref and order.status is Order.Completed:
                self.strategy.change_state(self, CandlePatternLong.Tp1(self.strategy, self.feed, self.entry, self.stoploss, self.takeprofit))


    class Tp1(TradeState):

        def next(self):
            self.validate()
            # self.change_to_trail_stop_after_some_progress()
            # self.exit_when_close_under_entry_lows()

        # def exit_if_trade_goes_strong_down_on_the_beginning(self):
        def change_to_trail_stop_after_some_progress(self):
            if self.entry.plen > 2 and self.stoploss.getordername() is Order.StopTrail:
                self.stoploss = self.strategy.sell(self.feed, exectype=Order.StopTrail, parent=self.entry, transmit=False, trailamount=self.feed.atr[0]*1.5)

        def exit_when_close_under_entry_lows(self):
            trigger_idx = self.entry.plen - self.feed.open.idx -1
            if self.feed.close[0] < min(self.feed.low[trigger_idx], self.feed.lowest[trigger_idx]):
                self.strategy.close(self.feed)
                self.strategy.cancel(self.takeprofit)
                self.strategy.cancel(self.stoploss)

        def validate(self):
            position = self.strategy.getposition(self.feed)
            assertlog(position, f'{self.feed._name} has no open position of size {position.size} while in state {self.__class__.__name__}')

        def next_state(self, order):
            if order.ref == self.takeprofit.ref and order.status is Order.Completed:
                risk = self.entry.executed.price - self.stoploss.created.price
                next_profit = min(1.5*risk, 3*self.feed.atr[0])
                self.stoploss = self.strategy.sell(self.feed, exectype=Order.Stop, price=order.data.lowest[0])
                self.takeprofit = self.strategy.sell(self.feed, exectype=Order.Limit, price=self.feed.close[0] + next_profit, oco=self.stoploss)
                self.strategy.change_state(self, CandlePatternLong.Tp2(self.strategy, self.feed, self.entry, self.stoploss, self.takeprofit))

    class Tp2(TradeState):
        def next(self):
            pass

        def next_state(self, order):
            pass


