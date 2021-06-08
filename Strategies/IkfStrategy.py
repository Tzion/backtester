
import backtrader as bt
from .BaseStrategy import BaseStrategy
from backtrader.utils.autodict import AutoDictList
import itertools
from iknowfirst.IkfIndicator import IkfIndicator
from iknowfirst.iknowfirst import retrieve_forecasts_data

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
            data.indicator1 = IkfIndicator(data, forecast='3days')
            data.indicator2 = IkfIndicator(data, forecast='7days')
            data.indicator3 = IkfIndicator(data, forecast='14days')
            data.indicator4 = IkfIndicator(data, forecast='1months')
            data.indicator5 = IkfIndicator(data, forecast='3months')
            data.indicator6 = IkfIndicator(data, forecast='12months')
        self.test_forecasts = retrieve_forecasts_data(filter_friday=False).stack().unstack(level=2,).unstack().fillna(0)

    

        

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

    def next(self):
        pass
        self.validate_date()

    def _addindicator(self,indcls):
        print("running")

    def validate_date(self):
        for d in self.datas:
            date = d.datetime.date()
            try:
                raw_value = self.forecasts.loc[str(date), d.indicator2.p.forecast][d._name].strength
                assert raw_value == d.indicator2[0]
            except AssertionError as e:
                print('Indicator values mistmatch of %s or date %s', d._name, str(date))


import os, sys, datetime
from iknowfirst.iknowfirst import retrieve_forecasts_data, retrieve_stocks

FILENAME_FORMAT = lambda s: 'TASE_DLY_' + s.replace('.TA', '') + ', 1D.csv'

def add_data(*, limit=0, dirpath='ikf_stocks', cerebro):
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    dirpath = os.path.join(modpath, dirpath)
    stocks = retrieve_stocks()
    stocks = stocks[:limit or len(stocks)]
    print('adding {} data feeds'.format((stocks)))
    for i, stock in enumerate(stocks):
        feed = bt.feeds.GenericCSVData(
            dataname=os.path.join(dirpath, FILENAME_FORMAT(stock)), fromdate=datetime.datetime(2020, 12, 3),
            todate=datetime.datetime(2021, 4, 27), dtformat='%Y-%m-%dT%H:%M:%SZ',
            high=2, low=3, open=1, close=4, volume=7)
        feed.plotinfo.plotmaster = None
        feed.plotinfo.plot = False
        cerebro.adddata(feed, name=stock)