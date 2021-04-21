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
            self.cur_stock = stock
            if not self.getposition(data=stock):
                 self.check_signals(stock)
            else:
                self.manage_position(stock)

    def check_signals(self, stock):
        pass

    def manage_position(self, stock):
        pass

    def notify_order(self, order):
        if order.status is bt.Order.Completed or order.status is bt.Order.Partial: 
            self.log(self.cur_stock, "order %s: %s %s, price: %s, size: %s" % (order.getstatusname(), order.ordtypename(), order.getordername(), order.price, order.size))
    
    def notify_trade(self, trade):
        pass  # todo

    def log(self, stock, txt):
        ''' logging function for this strategy'''
        date = stock.datetime.date(0)
        print('%s @ %s: %s' % (stock._name, date.isoformat(), txt))
