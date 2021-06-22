import backtrader as bt
from backtrader import indicators
from backtrader import indicator
from backtrader.order import Order
from strategies.base_strategy import BaseStrategy
from iknowfirst.ikf_indicator import IkfIndicator
from iknowfirst.iknowfirst import get_forecast_of, retrieve_forecasts_data

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
        return stock.pred_1m.strong_predictability[1] > 0

    def manage_position(self, stock):
        trade = self.get_opened_trade(stock)
        cur_duration = (self.datetime.date() - trade.open_datetime().date()).days
        if cur_duration >= 30:
            self.close(stock)


class TwoTimeframesForecast(IkfStrategy):

    global pos_size # TODO use sizer

    def prepare(self, stock):
        super().prepare(stock)
        global pos_size
        pos_size = self.broker.cash/12
        # self.add_indicator(stock, IkfIndicator(stock, forecast='3days'), 'pred_3d')
        self.add_indicator(stock, IkfIndicator(stock, forecast='14days'), 'pred_14d')
        # self.add_indicator(stock, IkfIndicator(stock, forecast='7days'), 'pred_7d')
        self.add_indicator(stock, IkfIndicator(stock, forecast='1months'), 'pred_1m')
        # self.add_indicator(stock, IkfIndicator(stock, forecast='3months'), 'pred_3m')

    def check_signals(self, stock):
        def strong(ind):
            try:
                return ind.strong_predictability[1] > 0 and ind.strong_predictability[0] > 0
            except IndexError:
                return False
        strongs = list(filter(strong, stock.indicators))
        def weak(ind):
            try:
                return ind.strong_predictability[1] > 0
            except IndexError:
                return False
        weaks = list(filter(weak, stock.indicators))
        if len(weaks) < 2 or len(strongs) < 1:
            return False 
        
        stock.long_period = strongs[0].forecast_in_days()
        best_weak = weaks[0] if weaks[0] is not strongs[0] else weaks[1]
        stock.short_period = best_weak.forecast_in_days()
        self.buy(stock, max(1, int(pos_size/stock.open[0])), exectype=Order.Market)
        stock.profit_taken = False


    def manage_position(self, stock):
        trade = self.get_opened_trade(stock)
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
    
    global pos_size # TODO use sizer

    def prepare(self, stock):
        super().prepare(stock)
        global pos_size
        pos_size = self.broker.cash/10
        super().prepare(stock)
        self.add_indicator(stock, IkfIndicator(stock, forecast='1months'), 'pred_1m')
        self.add_indicator(stock, indicators.SMA(stock.pred_1m.strength, period=5), 'sma5_1m_strength', subplot=True)
        self.add_indicator(stock, indicators.SMA(stock.pred_1m.strength, period=30), 'sma30_1m_strength', subplot=True)
        self.add_indicator(stock, indicators.SMA(stock, period=5), 'sma5', subplot=True)

    def check_signals(self, stock):
        if self.is_possitive_signal(stock):
            self.buy(stock, max(1, int(pos_size/stock.open[0])), exectype=Order.Market)

    def manage_position(self, stock):
        if not self.is_possitive_signal(stock):
            self.close(stock)

    def is_possitive_signal(self, stock):
            try:
                return (stock.close[0] >= stock.sma5[1] and stock.sma5_1m_strength[1] > stock.sma5_1m_strength[0] 
                    and stock.pred_1m.strong_predictability[1] > 0 and stock.sma5_1m_strength[1] > stock.sma30_1m_strength[1])
            except IndexError:
                return False

class EndOfMonthEntry(IkfStrategy):
    global pos_size

    def prepare(self, stock):
        super().prepare(stock)
        global pos_size
        pos_size = self.broker.cash/7
        super().prepare(stock)
        self.add_indicator(stock, IkfIndicator(stock, forecast='1months'), 'pred_1m')
        # self.add_indicator(stock, IkfIndicator(stock, forecast='7days'), 'pred_7d')
        self.add_indicator(stock, IkfIndicator(stock, forecast='7days'), 'ind2')
        self.add_indicator(stock, indicators.SMA(stock.ind2.strong_predictability, period=7), 'avg_ind2', subplot=True)

    def check_signals(self, stock):
        if self.is_around_end_of_month() and self.check_pred_signal(stock.pred_1m, strong=True):
            self.buy(stock, max(1, int(pos_size/stock.open[0])), exectype=Order.Market)
            stock.hold_for = stock.ind2.forecast_in_days()

    def manage_position(self, stock):
        trade = self.get_opened_trade(stock)
        cur_duration = (self.datetime.date() - trade.open_datetime().date()).days
        if cur_duration >= stock.hold_for:
            if stock.avg_ind2[0] > 50:
                stock.hold_for += stock.ind2.forecast_in_days()
            else:
                self.close(stock)

    def check_pred_signal(self, indicator: IkfIndicator, strong=True):
        try: 
            if strong:
                return indicator.strong_predictability[1] > 0
            else:
                return indicator.predictability[1] > 0
        except IndexError:
            return False

    def is_around_end_of_month(self):
        return 0 <= self.datetime.date().day <= 31


class Top3(IkfStrategy):

    global pos_size

    def prepare(self, stock):
        super().prepare(stock)
        global pos_size
        pos_size = self.broker.cash/7
        super().prepare(stock)
        self.add_indicator(stock, IkfIndicator(stock, forecast='7days'), 'ind1')

    
    def check_signals(self, stock):
        top3 = get_forecast_of(stock.datetime.date(), stock.ind1.p.forecast)
        if stock in top3 and stock.ind1.strong_predictability[1]:
            self.buy(stock, max(1, int(pos_size/stock.open[0])), exectype=Order.Market)
        pass

    def manage_position(self, stock):
        trade = self.get_opened_trade(stock)
        cur_duration = (self.datetime.date() - trade.open_datetime().date()).days