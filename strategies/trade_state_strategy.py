from __future__ import annotations
from abc import abstractmethod
from money_mgmt.sizers import PortionSizer

from backtrader.order import Order
from strategies.base_strategy import BaseStrategy
from globals import *
from logger import *

class TradeState():

    strategy : TradeStateStrategy

    def __init__(self, strategy : TradeStateStrategy, feed, entry : Order = None, stoploss: Order = None, takeprofit: Order = None):
        self.strategy = strategy
        self.feed = feed
        self._entry   = entry
        self._stoploss = stoploss
        self._takeprofit = takeprofit

    def _cancel_and_set_order_property(self, order:Order, name: str):
        attr_name = '_' + name
        cur_order = self.__getattribute__(attr_name)
        if cur_order and isinstance(cur_order, Order):
            self.strategy.cancel(cur_order)
        self.__setattr__(attr_name, order)

    entry = property(lambda self: self._entry, lambda self, order: self._cancel_and_set_order_property(order, 'entry'), None)
    stoploss = property(lambda self: self._stoploss, lambda self, order: self._cancel_and_set_order_property(order, 'stoploss'), None)
    takeprofit = property(lambda self: self._takeprofit, lambda self, order: self._cancel_and_set_order_property(order, 'takeprofit'), None)
    
    def cancel_orders(self):
        self.entry, self.stoploss, self.takeprofit = None, None, None,

    @abstractmethod
    def next(self):
        NotImplementedError
    


class TradeStateStrategy(bt.Strategy):

    feeds = []

    def __init__(self):
        self.setsizer(PortionSizer(percents=10))
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

    notify_trade = BaseStrategy.notify_trade

    notify_order = BaseStrategy.notify_order


