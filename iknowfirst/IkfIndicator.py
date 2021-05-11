import backtrader as bt
import pandas as pd

class IkfIndicator(bt.Indicator):
   
    lines = ('strength', 'predictability')
    params = (('timeframe', '7days'),)

    def __init__(self, forecast):
        self.forecast = forecast
        self.iter_strength = iter(forecast.loc[:,self.p.timeframe,:]['strength'])
        self.iter_pred = iter(forecast.loc[:,self.p.timeframe,:]['predictability'])
    
    def next(self):
        self.lines.strength[0] = next(self.iter_strength)
        self.lines.predictability[0] = next(self.iter_pred)*100


