import backtrader as bt
from .base_strategy import BaseStrategy
from iknowfirst.ikf_indicator import IkfIndicator
from iknowfirst.iknowfirst import retrieve_forecasts_data

class IkfStrategy(BaseStrategy):

    global pos_size # TODO use sizer

    def __init__(self):
        global pos_size
        pos_size = self.broker.cash/15
        forecasts = retrieve_forecasts_data(filter_friday=False)
        self.forecasts = forecasts.stack().unstack(level=2, ).unstack().fillna(0)
        super().__init__()

    def prepare(self, stock):
        stock.forecast = self.forecasts[stock._name]



class OneMonthPredicationIkf(IkfStrategy):

    def prepare(self, stock):
        super().prepare(stock)
        self.add_indicator(stock, IkfIndicator(stock, forecast='1months'), 'pred_1m')
        self.add_indicator(stock, IkfIndicator(stock, forecast='14days'), 'pred_14d')
        self.add_indicator(stock, IkfIndicator(stock, forecast='7days'), 'pred_7d')
        self.add_indicator(stock, IkfIndicator(stock, forecast='3months'), 'pred_3m')

    def check_signals(self, stock):
        if self.open_signal(stock):
            self.buy(data=stock, exectype=bt.Order.Market, size=max(1, int(pos_size/stock.open[0]))) # TODO buy in the openning price of the current day (now it's the open price of the next day)
    
    def open_signal(self, stock):
        try:
            return stock.pred_1m.strong_predictability[0] > 0 and stock.pred_1m.strong_predictability[1] > 0 
        except IndexError:
            return False

    def manage_position(self, stock):
        open_trades = self.get_open_trades(stock)
        for t in open_trades:
            if (stock.datetime.date() - t.open_datetime().date()).days >= 30 and not self.open_signal(stock):
                self.sell(data=stock, exectype=bt.Order.Market, size=t.size)
        if len(open_trades) > 1:
            self.log(stock, 'Warning - more than one open position!')