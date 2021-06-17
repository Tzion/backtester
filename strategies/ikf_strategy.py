from datetime import datetime
import backtrader as bt
from backtrader.feed import CSVDataBase, CSVFeedBase
from backtrader.position import Position
from backtrader.trade import Trade
from .base_strategy import BaseStrategy
from backtrader.utils.autodict import AutoDictList
import itertools
from iknowfirst.ikf_indicator import IkfIndicator
from iknowfirst.iknowfirst import retrieve_forecasts_data

class IkfStrategy(BaseStrategy):

    global pos_size

    def __init__(self):
        global pos_size
        pos_size = self.broker.cash/15
        forecasts = retrieve_forecasts_data(filter_friday=False)
        self.forecasts = forecasts.stack().unstack(level=2, ).unstack().fillna(0)
        super().__init__()

    def prepare(self, stock):
        stock.forecast = self.forecasts[stock._name]
        # self.add_indicator(stock, IkfIndicator(stock, forecast='3days'), 'pre_3d')
        # self.add_indicator(stock, IkfIndicator(stock, forecast='7days'), 'pred_7d')
        # self.add_indicator(stock, IkfIndicator(stock, forecast='14days'), 'pred_14d')
        # self.add_indicator(stock, IkfIndicator(stock, forecast='1months'), 'pred_1m')
        # self.add_indicator(stock, IkfIndicator(stock, forecast='3months'), 'pre_3m')
        # self.add_indicator(stock, IkfIndicator(stock, forecast='12months'), 'pre_12m')


    def manage_position_old(self, stock):
        trades : AutoDictList = self._trades[stock]  # self._trades[stock] is {stock: {order_id: [trades]}}
        open_trades = [t for t in itertools.chain(*self._trades[stock].values()) if t.isopen]
        for t in open_trades:
            if (stock.datetime.date() - t.open_datetime().date()).days >= 30 and not self.open_signal(stock):
                self.sell(data=stock, exectype=bt.Order.Market, size=t.size)
        if len(open_trades) > 1:
            self.log(stock, 'Warning - more than one open position!')
    
    def check_signals(self, stock):
        if self.open_signal(stock):
            self.open_position(stock)
    
    def open_signal(self, stock):
        try:
            if stock._name in list(self.forecasts.loc[str(stock.datetime.date()),'7days'].index):
                return True
        except KeyError as e:
            pass # todo avoid the KeyError by quring the df differently. something like self.forecasts.loc[('2020-12-03','7days'),:].index

    def open_position(self, stock):
        self.buy(data=stock, exectype=bt.Order.Market, size=max(1, int(pos_size/stock.open[0]))) # TODO buy in the openning price of the current day (now it's the open price of the next day)

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


class OneMonthPredicationIkf(IkfStrategy):

    def prepare(self, stock):
        super().prepare(stock)
        self.add_indicator(stock, IkfIndicator(stock, forecast='1months'), 'pred_1m')
        self.add_indicator(stock, IkfIndicator(stock, forecast='14days'), 'pred_14d')
        self.add_indicator(stock, IkfIndicator(stock, forecast='7days'), 'pred_7d')

    def check_signals(self, stock):
        if self.open_signal(stock):
            self.open_position(stock)
    
    def open_signal(self, stock):
        return stock.pred_1m.strong_predictability[0] > 0

    def manage_position(self, stock):
        super().manage_position_old(stock)
        return
        position : Position = self.getposition(stock)
        self.positions
        if position.size > 0 and (stock.datetime.date() - position.datetime.date()).days >= 30:
            self.sell(stock=stock, exectype=bt.Order.Limit, price=stock.open[0])