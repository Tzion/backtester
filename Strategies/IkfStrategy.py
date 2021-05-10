
import backtrader as bt
from .BaseStrategy import BaseStrategy
from backtrader.utils.autodict import AutoDictList
import itertools
from iknowfirst.IkfIndicator import IkfIndicator

class IkfStrategy(BaseStrategy):
    """
    buy the top stock in the 7days forecast.
    sell after 7 days or until it's not in the 7days table anymore - according to the latest
    """

    def __init__(self, forecasts):
        self.forecasts = forecasts.stack().unstack(level=2, ).unstack().fillna(0)
        self.add_forecast_indicator()
        for stock in self.datas:
            stock.strength = IkfIndicator(
                forecast=self.forecasts.loc[:, '7days',:][stock._name]['strength'])


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
        self.buy(data=stock, exectype=bt.Order.Limit, price=stock.open[0])


    def manage_position(self, stock):
        trades : AutoDictList = self._trades[self.data]  # self._trades[data] is {data: {order_id: [trades]}}
        open_trades = [t for t in itertools.chain(*self._trades[self.data].values()) if t.isopen]
        for t in open_trades:
            if (stock.datetime.date() - t.open_datetime().date()).days >= 7 and not self.open_position(stock):
                self.sell(data=stock, exectype=bt.Order.Limit, price=stock.open[0])  # todo consider closing directly on the trade -  t.update()
        if len(open_trades) > 1:
            self.log(stock, 'Warning - more than one open position!')

    def add_forecast_indicator(self):
        pass
