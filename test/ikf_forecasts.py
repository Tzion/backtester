from iknowfirst.iknowfirst import retrieve_forecasts_data, retrieve_stocks
import backtrader as bt
import pytest


class TestForecastsData:

    cerebro = bt.Cerebro()

    def test_forecasts_data(self):
        forcasts = retrieve_forecasts_data()
        strategy = IkfStrategy(forecasts=forcasts)
        assert 1==2



if __name__ == '__main__':
    TestForecastsData().test_forecasts_data()

# draft code for test cases - was taked from ikf_strategy
    '''
use this in the other strategies 
    def get_top_signals(self, date: datetime):
        forecasts = self.forecasts.loc[str(date), '1months'].unstack()
        forecasts = forecasts[forecasts['strength'] > 0.19]
        forecasts = forecasts.sort_values(by=['strength'], ascending=False)
        return forecasts[:3].index

    def next(self):
        today = self.data0.datetime.date()
        if self.is_buying_period(today):
            stocks_to_buy = self.get_top_signals(today)
            for stock in stocks_to_buy:
                self.open_position(self.find_stock_by_name(stock))
        if self.updating_period(today):
            for stock in self.broker.positions:
                self.manage_position(stock)

    def find_stock_by_name(self, name):
        for stock in self.stocks:
            if stock._name == name:
                return stock
    def is_buying_period(self, date: datetime):
        return date.day < 4

    def updating_period(self, date: datetime):
        return date.weekday() == 6
    '''



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