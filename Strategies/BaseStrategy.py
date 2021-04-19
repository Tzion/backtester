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

    def check_signals(self, stock):
        pass

    def manage_position(self, stock):
        pass

    def log(self, stock, txt):
        ''' Logging function for this strategy'''
        date = stock.datetime.date(0)
        print('%s @ %s: %s' % (stock._name, date.isoformat(), txt))