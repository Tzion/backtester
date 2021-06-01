
import backtrader as bt
from .BaseStrategy import BaseStrategy
from backtrader.utils.autodict import AutoDictList
import itertools
from iknowfirst.IkfIndicator import IkfIndicator

class IkfStrategy(BaseStrategy):
    """
    buy the top data in the 7days forecast.
    sell after 7 days or until it's not in the 7days table anymore - according to the latest
    """

    def __init__(self, forecasts):
        self.forecasts = forecasts.stack().unstack(level=2, ).unstack().fillna(0)
        self.add_forecast_indicator()
        for data in self.datas:
            data.forecast = self.forecasts[data._name]
            data.indicator = IkfIndicator(data, forecast='7days')
            data.indicator.plotinfo.plot = False
            data.indicator.plotinfo.plotname = 'ikf indicator (' + data._name + ')'
        

    """"
    TODO create unit test
    r = forecasts['BEZQ.TA'].loc[:,'7days',:]
    n = 0
    def validate_data(self):
        try:
            assert not self.forecasts.loc[str(self.data0.datetime.date())].empty
        except AssertionError as e:
            print('Error for date %s' % self.data0.datetime.date())

        try:
            assert not r.loc[str(r.index[n])[:-9]].empty
        except AssertionError as e:
            print('Indicator Error for date %s' % str(self.r.index[self.n])[:-9])
        n = n+1
    """


    def check_signals(self, data):
        if self.open_signal(data):
            self.open_position(data)
    
    def open_signal(self, data):
        try:
            if data._name in list(self.forecasts.loc[str(data.datetime.date()),'7days'].index):
                return True
        except KeyError as e:
            pass # todo avoid the KeyError by quring the df differently. something like self.forecasts.loc[('2020-12-03','7days'),:].index

    def open_position(self, data):
        self.buy(data=data, exectype=bt.Order.Limit, price=data.open[0])


    def manage_position(self, data):
        trades : AutoDictList = self._trades[self.data]  # self._trades[data] is {data: {order_id: [trades]}}
        open_trades = [t for t in itertools.chain(*self._trades[self.data].values()) if t.isopen]
        for t in open_trades:
            if (data.datetime.date() - t.open_datetime().date()).days >= 7 and not self.open_position(data):
                self.sell(data=data, exectype=bt.Order.Limit, price=data.open[0])  # todo consider closing directly on the trade -  t.update()
        if len(open_trades) > 1:
            self.log(data, 'Warning - more than one open position!')

    def add_forecast_indicator(self):
        pass
