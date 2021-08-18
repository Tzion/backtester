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
        if order.status in [bt.Order.Completed, bt.Order.Partial, bt.Order.Canceled, bt.Order.Submitted]:
            logdebug(f'order #{order.ref} {order.getstatusname()}, {order.ordtypename()}, {order.getordername()}, price: {order.price or order.executed.price or order.created.price:.2f}, size: {order.size:.2f}', order.data)
        if order.status in [bt.Order.Rejected, bt.Order.Margin]:
            logwarning(f'order #{order.ref} {order.getstatusname()}, {order.ordtypename()}, {order.getordername()}, price: {order.price or order.executed.price or order.created.price:.2f}, size: {order.size:.2f}', order.data)


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


    # TODO the are of plotting need refactoring       
    def plot(self, limit=0, only_trades=True, interactive_plots=True, plot_observers=True):
        pylab.rcParams['figure.figsize'] = 26, 13 # that's default image size for this interactive session
        # limit = limit or len(self.stocks)
        # feeds = list(dict(sorted(self._trades.items(), key=lambda item: len(item[1][0]))))[:limit] if only_trades else self.stocks[:limit] # for sorted trades
        plotter = Bokeh(style='bar', scheme=Tradimo()) if interactive_plots else None
        loginfo('ploting top %d feeds' % ((only_trades and len(self._trades) or limit or len(self.stocks))))
        self.set_plot_for_observers(False)
        printed = 0
        for i, stock in enumerate(self.stocks):
            if limit<0:
                break
            if only_trades and stock not in self._trades:
                continue
            if limit and printed >= limit:
                break
            self.set_plotting(stock, True)
            self.set_plot_for_buysell_observer(True, i, stock) # this hack won't work for sorted trades - because of assumption over
            gb.cerebro.plot(plotter=plotter, style='candlestick', barup='green', numfigs=1)
            printed += 1
            self.set_plot_for_buysell_observer(False, i, stock) # this hack won't work for sorted trades - because of assumption over
            self.set_plotting(stock, False)
        if plot_observers:
            self.plot_observers(plotter, only_trades)


    def set_plotting(self, feed, on):
        feed.plotinfo.plotmaster = feed
        feed.plotinfo.plot = on  # todo create a wrapper for the feed (csvData) object with attributes like indicators
        self.set_plot_for_indicators(feed, on)
    
    def plot_observers(self, plotter, only_trades):
        self.set_plot_for_observers(True, only_trades)
        gb.cerebro.plot(plotter)

    def set_plot_for_observers(self, is_plot, only_trades=False):
        for observer in self.getobservers():
            if only_trades and not observer.data in self._trades and type(observer) and not observer.plotinfo.subplot:
                continue
            observer.plotinfo.plot = is_plot

    # hacky function to turn on the buy-sell observer of the stock that is about to plot
    def set_plot_for_buysell_observer(self, plot_on, index, stock):
        observer = self.getobservers()[index+1]
        if observer.data._name != stock._name:
            raise Exception("trying to plot buy-sell observer of wrong stock")
        observer.plotinfo.plot = plot_on
        
