from strategies.DojiStrategyLong import DojiLongStrategy
from strategies.BaseStrategy import BaseStrategy
import backtrader as bt
from backtrader import indicators

class MultipleStocksStrategy(bt.Strategy):

    # todo add type hint for: strategies: list[BaseStrategy]

    def __init__(self): # todo add type hint for strategy (class)
        self.strategies = list()
        for d in self.datas:
            strat = DojiLongStrategy.__new__(DojiLongStrategy)
            strat.__init__()
            self.strategies.append(strat)

    def next(self):
        for strategy in self.strategies:
            pass
            strategy.next()