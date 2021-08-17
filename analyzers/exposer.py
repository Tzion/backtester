from collections import OrderedDict
import backtrader as bt

class Exposer(bt.Analyzer):

    def __init__(self):
        super().__init__()
        if self.strategy.broker.params.shortcash:
            raise Exception('This Analyzer works properly when broker.params.shortcash is False. use broker.set_shortcash(False)')


    def create_analysis(self):
        self.rets = OrderedDict()  # dict with . notation
        self.rets.accumulative_exposer = 0.0
        self.rets.exposer = 0.0

    def next(self):
        current_exposer = (self.strategy.broker.getvalue() - self.strategy.broker.getcash()) / self.strategy.broker.getvalue()
        self.rets.accumulative_exposer += current_exposer
        self.rets.exposer = self.rets.accumulative_exposer / len(self.strategy)
        self.rets['Exposer'] = str(self.rets.exposer * 100) + '%'