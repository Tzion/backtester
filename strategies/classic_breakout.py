from backtrader import talib

from strategies.trade_state_strategy import TradeState, TradeStateStrategy
from backtrader import indicators
from globals import *
from logger import *
from custom_indicators import visualizers


class ClassicBreakout(TradeStateStrategy):

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
        feed.single_marker_test= visualizers.SingleMarker(signals=feed.highest_breakout, level=feed.high, color='purple')
        # feed.highs_breakout_markers = visualizers.SingleMarker(signals=feed.highest_breakout, level=feed.high, plotmaster=feed)
        # feed.buy_level = visualizers.PartialLevel(signal=feed.highs_breakout, level=feed.low-2*feed.atr, plotmaster=feed,length=self.p.entry_period)
        # feed.stop_level = visualizers.PartialLevel(signal=feed.highs_breakout, level=feed.low-3.5*feed.atr, plotmaster=feed,color='salmon', length=self.p.entry_period)

    def initial_state_cls(self):
        return self.NoTrade
    

    class NoTrade(TradeState):
        def next(self):
            pass