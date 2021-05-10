import backtrader as bt
import pandas as pd

class IkfIndicator(bt.Indicator):
   
    lines = ('strength',)
    params = (('value', 7),)

    def __init__(self, forecast):
        self.iter = iter(forecast)
    
    def next(self):
        self.lines.strength[0] = next(self.iter)
        # self.lines.strength[0] = next(self.iter)


