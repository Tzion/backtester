import backtrader as bt
from .base_strategy import BaseStrategy
from backtrader.utils.autodict import AutoDictList
import itertools
from iknowfirst.ikf_indicator import IkfIndicator
from iknowfirst.iknowfirst import retrieve_forecasts_data

class IkfStrategy(BaseStrategy):
    """
    buy the top data in the 7days forecast.
    sell after 7 days or until it's not in the 7days table anymore - according to the latest
    """

    def __init__(self):
        forecasts = retrieve_forecasts_data(filter_friday=False)
        self.forecasts = forecasts.stack().unstack(level=2, ).unstack().fillna(0)
        super().__init__()

    
    def prepare(self, stock):
        stock.forecast = self.forecasts[stock._name]
        self.add_indicator(stock, IkfIndicator(stock, forecast='3days'), 'pre_3d')
        self.add_indicator(stock, IkfIndicator(stock, forecast='7days'), 'pre_7d')
        self.add_indicator(stock, IkfIndicator(stock, forecast='14days'), 'pre_14d')
        self.add_indicator(stock, IkfIndicator(stock, forecast='1months'), 'pre_1m')
        self.add_indicator(stock, IkfIndicator(stock, forecast='3months'), 'pre_3m')
        self.add_indicator(stock, IkfIndicator(stock, forecast='12months'), 'pre_12m')



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


    def next(self):
        pass

"""
# TODO create a test out of this code
    def validate_date(self):
        for d in self.datas:
            date = d.datetime.date()
            for ind in d.indicators:
                timeframe = ind.p.forecast
                try:
                    raw_value = self.forecasts.loc[str(date), timeframe][d._name].strength
                    actual_value = ind[0]
                    assert raw_value == actual_value
                except AssertionError as e:
                    print('Indicator values mistmatch of %s %s, at date %s, expected=%s, actual=%s'%(d._name, timeframe, str(date), raw_value, actual_value))

"""
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


