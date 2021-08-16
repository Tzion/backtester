from collections import OrderedDict
import backtrader as bt

class Exposer(bt.Analyzer):

    def create_analysis(self):
        self.rets = OrderedDict()  # dict with . notation

        self.rets.len = 0
        self.rets.accumulative_exposer = 0.0
        self.rets.exposer = 0.0

    def next(self):
        self.rets.len += 1
        current_exposer = self.strategy.broker.getcash() / self.strategy.broker.getvalue()
        self.rets.accumulative_exposer += current_exposer
        self.rets.exposer = self.rets.accumulative_exposer / self.rets.len
        assert self.ret.len == len(self.strategy) == len(self)