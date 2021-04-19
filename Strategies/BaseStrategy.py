import backtrader as bt
from backtrader import indicators

""" 
Base class for strategy of multiple feeds
"""
class BaseStrategy(bt.Strategy):


    def __init__(self):
        for data in self.datas:
            data.atr = indicators.ATR(data)
            data.tr = indicators.TR(data)

    def next(self):
        for stock in self.datas:
            if not self.getposition(data=stock):
                 self.check_signals(stock)
            else:
                self.manage_position(stock)

    #TODO define as abstract. also for manage_position
    def check_signals(self, i):
        pass

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))