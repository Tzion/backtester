
from backtrader import talib
from backtrader.indicator import LinePlotterIndicator
from backtrader.order import Order

from strategies.trade_state_strategy import TradeState, TradeStateStrategy
from backtrader import indicators
from globals import *
from logger import *
from custom_indicators import visualizers


class CandlePatternLong(TradeStateStrategy):
    
    params = {
        'atr_period': 13,
        'highs_period': 30
    }

    def prepare_feed(self, feed):
        feed.atr = talib.ATR(feed.high,feed.low,feed.close, timeperiod=self.p.atr_period)
        feed.tr = talib.ATR(feed.high,feed.low,feed.close, timeperiod=1)
        # feed.three_line_strike = talib.CDL3LINESTRIKE(feed.open, feed.high, feed.low, feed.close, plot=False) 
        # feed.three_line_strike_marker = visualizers.SingleMarker(signals=feed.three_line_strike, level=feed.low*.99, color='silver', marker='*', plotmaster=feed) 
        # feed.three_black_crows = talib.CDL3BLACKCROWS(feed.open, feed.high, feed.low, feed.close, plot=False) 
        # feed.three_black_crows_marker = visualizers.SingleMarker(signals=feed.three_black_crows, level=feed.low*.98, color='pink', marker='*', plotmaster=feed) 
        feed.doji_star = talib.CDLDOJISTAR(feed.open, feed.high, feed.low, feed.close, plot=False) 
        feed.doji_star_marker = visualizers.SingleMarker(signals=feed.doji_star, level=feed.low*.985, color='purple', marker='H', plotmaster=feed, markersize=7) 

        feed.ema_very_fast = indicators.EMA(feed.close, period=12)
        feed.ema_fast = indicators.EMA(feed.close, period=50)
        feed.ema_slow = indicators.EMA(feed.close, period=100)
        feed.highest = indicators.Highest(feed.high, period=self.p.highs_period, subplot=False)
        feed.lowest = indicators.Lowest(feed.low, period=self.p.highs_period, subplot=False)
        feed.highest_breakout = feed.high > feed.highest(-1)
        feed.highest._name = 'somename' ## Workaround for bug in Bokeh - cannot print feed.highest(-1) without this attribute
        feed.highest_breakout_marker = visualizers.SingleMarker(signals=feed.highest_breakout, level=feed.high*1.02 ,plotmaster=feed, color='orange', markersize=6, plot=False)
        feed.open.extend(size=1)
        feed.high.extend(size=1)
        feed.low.extend(size=1)
        feed.close.extend(size=1)


    def initial_state_cls(self):
        return self.LookForEntry
    
    def notify_trade(self, trade: bt.Trade):
        super().notify_trade(trade)
        if trade.isclosed:
            self.change_state(trade.data.state, self.LookForEntry(self, trade.data))
    


    class LookForEntry(TradeState):
        def next(self):
            risk = 1.4*self.feed.atr[0]
            if (
                self.feed.doji_star[0] > 0 
                and self.feed.open[1] > self.feed.low[0]
                and self.feed.lowest[-1] + self.feed.atr[0]/2 > self.feed.low[0] > self.feed.lowest[-1]
                # and self.uptrend(self.feed)
                # and self.feed.ema_very_fast[0] < self.feed.ema_very_fast[-1] < self.feed.ema_very_fast[-2]
                and self.feed.tr[0] >= self.feed.atr[-1] * 1
                # and self.gap(self.feed) > 0  and (self.gap(self.feed) > self.feed.atr[0] * .2)
                ):
                self.entry, self.stoploss, self.takeprofit = self.strategy.buy_bracket(self.feed, exectype=bt.Order.Market, stopprice=self.feed.low[0] - risk, limitprice=self.feed.open[1] + 2*risk)
                self.strategy.change_state(self, CandlePatternLong.LongProfit1(self.strategy, self.feed, self.entry, self.stoploss, self.takeprofit))
                return

            if (
                self.feed.doji_star[0] < 0 
                and self.feed.open[1] < self.feed.high[0]
                and self.feed.highest[-1] - self.feed.atr[0]/2 < self.feed.high[0] < self.feed.highest[-1]
                # and self.downtrend(self.feed) 
                # and self.feed.ema_very_fast[0] > self.feed.ema_very_fast[-1] > self.feed.ema_very_fast[-2]
                and self.feed.tr[0] >= self.feed.atr[-1] * 1
                # and self.gap(self.feed) < 0  and (abs(self.gap(self.feed)) > self.feed.atr[0] * .2)
            ):
                self.entry, self.stoploss, self.takeprofit = self.strategy.sell_bracket(self.feed, exectype=bt.Order.Market, stopprice=self.feed.high[0] + risk, limitprice=self.feed.open[1] - 2*risk)
                return
    
        # TODO should be in some utils module
        def uptrend(self, feed):
            return feed.ema_very_fast[0] > feed.ema_fast[0] > feed.ema_slow[0]

        def downtrend(self, feed):
            return feed.ema_very_fast[0] < feed.ema_fast[0] < feed.ema_slow[0]

        def gap(self, feed):
            return feed.open[1] - feed.close[0]


    class LongProfit1(TradeState):

        def next(self):
            self.validate()
            risk = self.entry.executed.price - self.stoploss.created.price
            move = self.feed.high[0] - self.entry.executed.price
            if move > risk:
                self.stoploss = self.strategy.sell(data=self.feed, price=self.entry.executed.price, exectype=Order.Stop, oco=self.takeprofit)


        def validate(self):
            position = self.strategy.getposition(self.feed)
            assertlog(position, f'{self.feed._name} has no open position of size {position.size} while in state {self.__class__.__name__}')



