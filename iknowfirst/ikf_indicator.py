import backtrader as bt
import pandas as pd

class IkfIndicator(bt.Indicator):
   
    lines = ('strength', 'predictability', 'strong_predictability')
    params = (('forecast', '7days'), ('predictability_threshold', '0.19'))
    global PRED_FACTOR
    PRED_FACTOR = 100

    def __init__(self):
        self.iter_strength = self.data.forecast.loc[:,self.p.forecast,:]['strength'].iteritems()
        self.iter_pred = self.data.forecast.loc[:,self.p.forecast,:]['predictability'].iteritems()
        self.plotinfo.plotname = self.p.forecast + ' forecast (' + self.data._name + ')'
        self.plotinfo.plot = False
    
    def next(self):
        def proceed2date(date, iter):
            cur = next(iter)
            while date > cur[0]: # iter[0] contains the date
                cur = next(iter)
            assert cur[0] == date, "no forecasts data for date %s"%date
            return cur

        date = self.data.datetime.date() 
        todays_strength = proceed2date(date, self.iter_strength)
        self.lines.strength[0] = todays_strength[1]
        todays_pred = proceed2date(date, self.iter_pred)
        self.lines.predictability[0] = todays_pred[1]* PRED_FACTOR
        self.lines.strong_predictability[0] = 100 if todays_pred[1] >= 0.19 else 0


    def forecast_in_days(self):
        return FORECAST_IN_DAYS[self.params.forecast]

    def is_positive(self, ago=0, high_pred=True):
        try:
            return self.l.strength[1-ago] > 0 and (not high_pred or self.l.predictability[1-ago] >= float(self.p.predictability_threshold)*PRED_FACTOR)
        except IndexError:
            return False


FORECAST_IN_DAYS = {'3days': 3, '7days': 7, '14days': 14, '1months': 30, '3months': 90, '12months': 360}

