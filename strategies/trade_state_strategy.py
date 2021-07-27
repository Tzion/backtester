from __future__ import annotations
from abc import abstractmethod

from backtrader.order import Order
from strategies.base_strategy import BaseStrategy
from globals import *
import matplotlib.pylab as pylab
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Blackly, Tradimo
import globals as gb
from logger import *
from typing import Optional

class TradeState():

    strategy : TradeStateStrategy

    def __init__(self, strategy : TradeStateStrategy, feed, entry : Order = None, stoploss: Order = None, takeprofit: Order = None):
        self.strategy = strategy
        self.feed = feed
        self._entry   = entry
        self._stoploss = stoploss
        self._takeprofit = takeprofit

    def set_order_property(self, order:Order, name: str):
        attr_name = '_' + name
        cur_order = self.__getattribute__(attr_name)
        if cur_order and type(cur_order) == Order:
            self.strategy(cur_order)
        self.__setattr__(attr_name, order)

    entry = property(lambda self: self._entry, lambda self, order: self.set_order_property(order, 'entry'), None)
    stoploss = property(lambda self: self._stoploss, lambda self, order: self.set_order_property(order, 'stoploss'), None)
    takeprofit = property(lambda self: self._takeprofit, lambda self, order: self.set_order_property(order, 'takeprofit'), None)
    
    @abstractmethod
    def next(self):
        NotImplementedError
    


class TradeStateStrategy(bt.Strategy):

# TODO once we have asset class - it should hold the state of the trade (and also the feed data - Asset.state, Asset.data/feed
    feeds = []

    def __init__(self):
        self.feeds = self.datas
        for feed in self.feeds:
            feed.state : TradeState = self.initial_state_cls()(self, feed)
            self.prepare_feed(feed)
    
    @abstractmethod
    def initial_state_cls(self): #TODO define the first state as the default
        pass

    def change_state(self, old_state : TradeState, new_state : TradeState):
        assert old_state.feed.state is old_state
        logdebug(f"changing state from {old_state.__class__.__name__} to {new_state.__class__.__name__}", old_state.feed)
        old_state.feed.state = new_state

    def next(self):
        for feed in self.feeds:
            feed.state.next()

    @abstractmethod
    def prepare_feed(self, feed):
        pass






    
    # TODO the are of plotting need refactoring       
    def plot(self, limit=0, only_trades=True, interactive_plots=True, plot_observers=True):
        pylab.rcParams['figure.figsize'] = 26, 13 # that's default image size for this interactive session
        # limit = limit or len(self.stocks)
        # feeds = list(dict(sorted(self._trades.items(), key=lambda item: len(item[1][0]))))[:limit] if only_trades else self.stocks[:limit] # for sorted trades
        plotter = Bokeh(style='bar', scheme=Tradimo()) if interactive_plots else None
        loginfo('ploting top %d feeds' % (limit or (only_trades and len(self._trades) or len(self.feeds))))
        self.set_plot_for_observers(False)
        printed = 0
        for i, stock in enumerate(self.feeds):
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
        BaseStrategy.set_plot_for_indicators(feed, on)
    
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

    notify_trade = BaseStrategy.notify_trade

    notify_order = BaseStrategy.notify_order


