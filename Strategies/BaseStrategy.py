import backtrader as bt

""" 
Base class for strategy of multiple feeds
"""
class BaseStrategy(bt.Strategy):


    def __init__(self):
        pass

    def next(self):
        for i,data in enumerate(self.datas):
            if self.getposition(data=self.datas[i]):
                self.manage_position(i)
            else:
                 self.check_signals(i)

    #TODO define as abstract. also for manage_position
    def check_signals(self, i):
        pass

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))