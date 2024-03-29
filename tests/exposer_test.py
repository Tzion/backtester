from test_common import *
import inspect
import backtrader as bt
import pandas as pd
from backtrader.feeds.pandafeed import PandasData
from analyzers.exposer import Exposer



# TODO migrate to some testing framework

class ZeroExposerTest(bt.Strategy):
    def next(self):
        assert self.analyzers.exposer.rets.exposer == 0.0, 'No trades - expecting exposer to be 0%'

class HighExposerTest(bt.Strategy):
    def next(self):
        self.buy(self.data0, size=1000) # All-in since the second bar- 90% exposer
    def stop(self):
        assert self.analyzers.exposer.rets.exposer == .9, f'expecting exposer to be 90%, actual exposer={self.analyzers.exposer.rets.exposer}'
        assert float(self.analyzers.exposer.get_analysis()['Exposer'][:-1]) == 90, f'expecting printable value to be 90%, got instead: {self.analyzers.exposer.get_analysis()["Exposer"]}'
        
class ShortSaleTest(bt.Strategy):
    def next(self):
        self.sell(self.data0, size=1000) # All-in since the second bar- 90% exposer
    def stop(self):
        assert self.analyzers.exposer.rets.exposer == .9, f'expecting exposer to be 90%, actual exposer={self.analyzers.exposer.rets.exposer}'


# before
def test_run(test: bt.Strategy):
    cerebro = bt.Cerebro()
    cerebro.adddata(DUMMY_DATA)
    cerebro.broker.setcash(1000)
    cerebro.broker.set_shortcash(False)
    cerebro.addstrategy(test)
    cerebro.addanalyzer(Exposer)
    strategy = cerebro.run()

def run_tests(test_classes):
    for test in test_classes:
        test_run(test)

tests = [t[1] for t in inspect.getmembers(sys.modules[__name__], lambda member : inspect.isclass(member) and issubclass(member, bt.Strategy))]

if __name__ == '__main__':
    run_tests(tests)
