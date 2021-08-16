import backtrader as bt
from backtrader.feed import CSVDataBase, CSVFeedBase
from backtrader.feeds.pandafeed import PandasData
import pandas as pd


class StrategyTester(bt.Strategy):
    pass


class ExposerAnalyzerTester(StrategyTester):
    def next(self):
        pass

class DfOpen(PandasData):
    params = (
        ('high', None),
        ('open', None),
        ('low', None),
        ('openinterest', None),
    )

def test_run():
    cerebro = bt.Cerebro()
    dataframe = pd.DataFrame({
        'close': [12,12,12],
        'volume': [1,1,1]
    },
    index=pd.date_range('20180310', periods=3))
    data = DfOpen(dataname=dataframe)
    cerebro.adddata(data)
    strategy = cerebro.run()
    # cerebro.plot(style='close', barup='green')
    

    



if __name__ == '__main__':
    test_run()