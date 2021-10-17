from datetime import datetime
import itertools
import backtrader as bt
from backtrader.feeds.csvgeneric import GenericCSVData
from backtrader.trade import Trade
from backtrader.utils.autodict import AutoDictList
import matplotlib.pylab as pylab
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Blackly, Tradimo
from backtrader import observers
import globals as gb
from money_mgmt.sizers import PortionSizer
from logger import *


""" 
Base class for strategy of multiple feeds
"""

class BaseStrategy(bt.Strategy):

    def __init__(self):
        self.stocks = self.datas
        self.setsizer(PortionSizer())
        self.prepare_strategy()
        for stock in self.stocks:
            self.prepare_stock(stock)
 
    def next(self):
        # TODO redesign
        self.on_next_bar()
        for stock in self.stocks:
            if not self.getposition(data=stock):
                self.check_signals(stock)
            else:
                self.manage_position(stock)


    @staticmethod
    def add_indicator(stock, indicator, attr_name=None, subplot=None):
        stock.indicators = stock.indicators if hasattr(stock, 'indicators') else []
        stock.indicators.append(indicator)
        if subplot is not None:
            indicator.plotinfo.subplot = subplot
        indicator.plotinfo.plot = False
        if attr_name:
            setattr(stock, attr_name, indicator)
        return indicator
    
    @staticmethod
    def set_plot_for_indicators(stock, is_plot):
        if hasattr(stock, 'indicators'):
            for ind in stock.indicators:
                ind.plotinfo.plot = is_plot
    
    # TODO no need of this - use the already defined Strategy.start() method by the super class
    def prepare_strategy(self):
        '''
        do setup (if needed) in the strategy level before the backtest starting
        '''
        pass

    def prepare_stock(self, stock):
        '''
        do setup needed per each stock before the backtest starting - called once per stock
        '''
        raise NotImplementedError

    # TODO  rename/ remove / redesign (take in care the use-case as in ikf_stratigies.Top3)
    def on_next_bar(self):
        '''
        called each bar before backtesing that bar
        '''
        pass

    def check_signals(self, stock):
        raise NotImplementedError

    def manage_position(self, stock):
        raise NotImplementedError

    def notify_order(self, order: bt.Order):
        if order.status in [bt.Order.Canceled, bt.Order.Submitted]:
            logdebug(f'order #{order.ref} {order.getstatusname()}, {order.ordtypename()}, {order.getordername()}, price: {order.price or order.created.price:.2f} created price: {order.created.price:.2f}, size: {order.size:.2f}', order.data)
        if order.status in [bt.Order.Completed, bt.Order.Partial]:
            logdebug(f'order #{order.ref} {order.getstatusname()}, {order.ordtypename()}, {order.getordername()}, price: {order.price or order.created.price:.2f} executed price: {order.executed.price:.2f}, size: {order.size:.2f}', order.data)
        if order.status in [bt.Order.Rejected, bt.Order.Margin, bt.Order.Partial]:
            logwarning(f'order #{order.ref} {order.getstatusname()}, {order.ordtypename()}, {order.getordername()}, price: {order.price or order.created.price:.2f} created price: {order.created.price:.2f}, size: {order.size:.2f}', order.data)


    def notify_trade(self, trade: bt.Trade):
        if (trade.status <= 1): # created or open
            loginfo(f'{"long" if trade.size>0 else "short"} trade {trade.status_names[trade.status]}, price: {trade.price:.2f}, size: {trade.size:.2f}, date: {trade.open_datetime().date()}', trade.data)
        else: # closed
            loginfo(f'trade {trade.status_names[trade.status]}, pnl: {trade.pnl:.0f}, date: {trade.close_datetime().date()} bars: {trade.barlen}', trade.data)

    def get_opened_trade(self, stock): #TODO handle trade management by my strategy
        trades : AutoDictList = self._trades[stock]  # self._trades[stock] is {data: {order_id: [trades]}}
        open_trades = [t for t in itertools.chain(*self._trades[stock].values()) if t.isopen]
        if len(open_trades) > 1:
            raise Exception('Warning - more than one open position for %s, trades: %s'%(stock, open_trades))
        return open_trades[0]
