import backtrader as bt
import pandas as pd

class IkfIndicator(bt.Indicator):
   
    lines = ('strength', 'predictability')
    params = (('forecast', '7days'),)

    def __init__(self):
        self.iter_strength = iter(self.data.forecast.loc[:,self.p.forecast,:]['strength'])
        self.iter_pred = iter(self.data.forecast.loc[:,self.p.forecast,:]['predictability'])
    
    def next(self):
        self.lines.strength[0] = next(self.iter_strength)
        self.lines.predictability[0] = next(self.iter_pred)*100


