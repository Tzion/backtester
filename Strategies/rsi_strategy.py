from strategies.base_strategy import BaseStrategy
from backtrader import indicators
from backtrader.order import Order


class RsiAndMovingAverageStrategy(BaseStrategy):

    def prepare_stock(self, stock):
        stock.rsi = indicators.RSI(stock, period=10)
        stock.sma = indicators.SMA(stock, period=200)
    
    def check_signals(self, stock):
        if stock.rsi[0] < 30 and stock.close[0] > stock.sma[0]:
            self.buy(stock, exectype=Order.Market)
    
    def manage_position(self, stock):
        trade = self.get_opened_trade(stock)
        if stock.rsi[0] > 40 or (len(self.data) - trade.baropen) > stock.rsi.p.period:
            self.close(stock)

    
