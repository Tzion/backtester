
from backtrader import talib

from strategies.trade_state_strategy import TradeState, TradeStateStrategy
from backtrader import indicators
from globals import *
from logger import *
from custom_indicators import visualizers


class CandlePatternLong(TradeStateStrategy):
    
    params = {
        'atr_period': 20
    }

    def prepare_feed(self, feed):
        feed.atr = talib.ATR(feed.high,feed.low,feed.close, timeperiod=self.p.atr_period)
        feed.three_line_strike = talib.CDL3LINESTRIKE(feed.open, feed.high, feed.low, feed.close, plot=False) 
        feed.three_line_strike_marker = visualizers.SingleMarker(signals=feed.three_line_strike, level=feed.low*.99, color='silver', marker='*', plotmaster=feed) 
        feed.three_black_crows = talib.CDL3BLACKCROWS(feed.open, feed.high, feed.low, feed.close, plot=False) 
        feed.three_black_crows_marker = visualizers.SingleMarker(signals=feed.three_black_crows, level=feed.low*.98, color='purple', marker='*', plotmaster=feed) 
        feed.ema_short = indicators.EMA(feed.close, period=10)
        feed.ema_long = indicators.EMA(feed.close, period=50)



    def initial_state_cls(self):
        return self.NoTrade
    

    class NoTrade(TradeState):
        def next(self):
            if self.feed.three_black_crows[0]:
                self.strategy.buy_bracket(self.feed, exectype=bt.Order.Market, stopprice=self.feed.low[0]-self.feed.atr[0], limitprice=self.feed.high[0]+self.feed.atr[0])