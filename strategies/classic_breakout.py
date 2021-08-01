from backtrader import talib

from strategies.trade_state_strategy import TradeState, TradeStateStrategy
from backtrader import indicators
from globals import *
from logger import *
from custom_indicators import visualizers


class ClassicBreakout(TradeStateStrategy):
    '''
    Long strategy of breakout
    breakup candle with high volumes
    breaks 3 month highest (paramertized)
    strong candle - long body opens in gap
    '''

    params = (
        ('atr_period', 20),
        ('highs_period', 63),
        ('entry_period', 10),
    )
    def prepare_feed(self, feed):
        feed.atr = talib.ATR(feed.high,feed.low,feed.close, timeperiod=self.p.atr_period)
        feed.highest = indicators.Highest(feed.high, period=self.p.highs_period, subplot=False)
        feed.highest_breakout = feed.high > feed.highest(-1)
        feed.highest._name = 'somename' ## Workaround for bug in Bokeh - cannot print feed.highest(-1) without this attribute
        feed.highest_breakout_marker = visualizers.SingleMarker(signals=feed.highest_breakout, level=feed.high*1.02 ,plotmaster=feed, color='orange')
        feed.volume_avg = indicators.SMA(feed.volume, period=self.p.highs_period, subplot=True) # feed.buy_level = visualizers.Partia, subplot=TrueFalsTrue, plotmaster=feeds_breakout, level=feed.low-2*feed.atr, plotmaster=feed,length=self.p.entry_period)
        feed.volume_peek = feed.volume > feed.volume_avg * 2
        feed.volume_peek_marker = visualizers.SingleMarker(signals=feed.volume_peek, level=feed.low*.96, color='blueviolet', marker='o', plotmaster=feed)
        feed.bulish_candle = talib.CDLMARUBOZU(feed.open, feed.high, feed.low, feed.close, plot=False) > 0
        feed.bulish_candle_marker = visualizers.SingleMarker(signals=feed.bulish_candle > 0, level=feed.low*.99, color='gold', marker='*', plotmaster=feed) 
        feed.bulish_candle2 = talib.CDLCLOSINGMARUBOZU(feed.open, feed.high, feed.low, feed.close, plot=False) > 0
        feed.bulish_candle_marker2 = visualizers.SingleMarker(signals=feed.bulish_candle2, level=feed.low*.99, color='silver', marker='*', plotmaster=feed) 



    def initial_state_cls(self):
        return self.NoTrade
    

    class NoTrade(TradeState):
        def next(self):
            if self.feed.volume_peek[0] and (self.feed.bulish_candle[0] or self.feed.bulish_candle2[0]) and self.feed.highest_breakout[0]:
                self.strategy.buy_bracket(self.feed, exectype=bt.Order.Market, stopprice=self.feed.low[0], limitprice=self.feed.high[0]+self.feed.atr[0])