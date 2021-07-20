from __future__ import annotations
from abc import abstractmethod
from globals import *


class TradeStateStrategy(bt.Strategy):

    feeds = []

    def __init__(self, initial_state_cls : type[TradeState]):
        self.feeds = self.datas
        for feed in self.feeds:
            feed.state : TradeState = initial_state_cls(self, feed)
            self.prepare_feed(feed)

    def next(self):
        for feed in self.feeds:
            feed.state.next(feed)

    @abstractmethod
    def prepare_feed(self, feed):
        pass




class TradeState():

    strategy : TradeStateStrategy

    def __init__(self, strategy : TradeStateStrategy, feed):
        self.strategy = strategy
        self.feed = feed
    
    @abstractmethod
    def next(self, feed):
        NotImplementedError


