import backtrader as bt
from backtrader import indicators
from backtrader import indicator
from backtrader.order import Order
from .base_strategy import BaseStrategy
from iknowfirst.ikf_indicator import IkfIndicator
from iknowfirst.iknowfirst import retrieve_forecasts_data
from backtrader import math

class IkfStrategy(BaseStrategy):


    def __init__(self):
        forecasts = retrieve_forecasts_data(filter_friday=False)
        self.forecasts = forecasts.stack().unstack(level=2, ).unstack().fillna(0)
        super().__init__()

    def prepare(self, stock):
        stock.forecast = self.forecasts[stock._name]



class OneTimeframeForecast(IkfStrategy):

    active_stocks = ['HARL.TA', 'DSCT.TA', 'ORA.TA', 'TSEM.TA', 'ARPT.TA', 'MLSR.TA', 'OPK.TA', 'NVMI.TA', 'MTRX.TA',
        'PHOE1.TA', 'ESLT.TA', 'AMOT.TA', 'SPEN.TA', 'BEZQ.TA', 'SAE.TA', 'ICL.TA']

    global pos_size # TODO use sizer

    def prepare(self, stock):
        super().prepare(stock)
        global pos_size
        pos_size = self.broker.cash/15
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
        open_trades = [self.get_open_trade(stock)]
        for t in open_trades:
            if (stock.datetime.date() - t.open_datetime().date()).days >= 30 and not self.open_signal(stock):
                self.sell(data=stock, exectype=bt.Order.Market, size=t.size)
        if len(open_trades) > 1:
            self.log(stock, 'Warning - more than one open position!')


class TwoTimeframesForecast(IkfStrategy):

    global pos_size # TODO use sizer

    def prepare(self, stock):
        super().prepare(stock)
        global pos_size
        pos_size = self.broker.cash/12
        # self.add_indicator(stock, IkfIndicator(stock, forecast='3days'), 'pred_3d')
        # self.add_indicator(stock, IkfIndicator(stock, forecast='14days'), 'pred_14d')
        # self.add_indicator(stock, IkfIndicator(stock, forecast='7days'), 'pred_7d')
        self.add_indicator(stock, IkfIndicator(stock, forecast='1months'), 'pred_1m')
        self.add_indicator(stock, IkfIndicator(stock, forecast='3months'), 'pred_3m')

    def check_signals(self, stock):
        def strong(ind):
            try:
                return ind.strong_predictability[0] > 0 #and ind.strong_predictability[1] > 0
            except IndexError:
                return False
        strongs = list(filter(strong, stock.indicators))
        def weak(ind):
            return ind.strong_predictability[0] > 0
        weaks = list(filter(weak, stock.indicators))
        if len(weaks) < 2 or len(strongs) < 1:
            return False 
        
        stock.long_period = strongs[0].forecast_in_days()
        best_weak = weaks[0] if weaks[0] is not strongs[0] else weaks[1]
        stock.short_period = best_weak.forecast_in_days()
        self.buy(stock, max(1, int(pos_size/stock.open[0])), exectype=Order.Market)
        stock.profit_taken = False


    def manage_position(self, stock):
        trade = self.get_open_trade(stock)
        cur_duration = (self.datetime.date() - trade.open_datetime().date()).days
        if  cur_duration >= stock.long_period: # and not self.is_strong_signal(stock):
            self.sell(stock, trade.size, exectype=Order.Market)
        if cur_duration >= stock.short_period and not stock.profit_taken:
            self.sell(stock, int(trade.size/2), exectype=Order.Market)
            stock.profit_taken = True

    def is_strong_signal(self, stock):
        for ind in stock.indicators:
            if ind.strong_predictability[0]:
                return True


class Sma5And30DaysForecasts(IkfStrategy):
    
    def prepare(self, stock):
        super().prepare(stock)
        self.add_indicator(stock, indicators.SMA(stock, period=5), 'sma5', subplot=True)
        self.add_indicator(stock, IkfIndicator(stock, forecast='1months'), 'pred_1m')
        self.add_indicator(stock, SimpleMovingAverage1(stock, period=5), 'strn_sma5_my')
        self.add_indicator(stock, indicators.SMA(stock.pred_1m, period=5), 'strn_sma5', subplot=True)

    def check_signals(self, stock):
        if self.is_possitive_signal(stock):
            self.buy(stock, max(1, int(pos_size/stock.open[0])), exectype=Order.Market)

    def manage_position(self, stock):
        if not self.is_possitive_signal(stock):
            self.close(stock)

    def is_possitive_signal(self, stock):
        stock.close[0] >= stock.sma5[0] and stock.strn_sma5[0] > stock.strn_sma5[-1]

class SimpleMovingAverage1(indicator.Indicator):
    lines = ('sma',)
    params = (('period', 5),)

    def __init__(self):
        # self.addminperiod(self.params.period)
        self.count = 1 # workaround because the get with fixed size returns the same slice of the array (in next())

    def next(self):
        datasum = math.fsum(self.data.pred_1m.strength.get(size=self.count)[:self.p.period])
        self.count += 1
        self.lines.sma[0] = datasum / self.p.period