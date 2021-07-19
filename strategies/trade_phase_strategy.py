from globals import *
from . import *

class TradePhaseStrategy(bt.Strategy):

    feeds = []

    def __init__(self, initial_state_cls):
        self.feeds = self.datas
        for feed in self.feeds:
            feed.state : TradePhase = initial_state_cls(self, feed)

    def next(self):
        for feed in self.feeds:
            feed.state.next()



class TradePhase():

    strategy : TradePhaseStrategy

    def __init__(self, strategy : TradePhaseStrategy, feed):
        self.strategy = strategy
        self.feed = feed
    
    def next(self):
        NotImplementedError


