import backtrader as bt
import os
import os.path
import sys
import pandas as pd
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))) # TODO no need anymore - remove after align all test classes
from backtrader.feeds.pandafeed import PandasData
import pytest

class DummyStrategy(bt.Strategy):
    def next(self):
        pass

DUMMY_DATA = PandasData(dataname=pd.DataFrame(data=1, columns=PandasData.datafields, index=pd.date_range('20210816', periods=10)))

TEST_DATA0 = bt.feeds.GenericCSVData(dataname='tests/test_data.csv', fromdate=datetime(2016, 7, 1), todate=datetime(2017,6,30), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)
TEST_DATA1 = bt.feeds.GenericCSVData(dataname='tests/test_data2.csv', fromdate=datetime(2016, 7, 1), todate=datetime(2017,6,30), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)

@pytest.fixture
def strategy_fixture(strategy, datas):
    return run_strategy(strategy, datas)

# for debugging reasons it may be more convenient to call this directrly from the test
def run_strategy(strategy, datas=[TEST_DATA0, TEST_DATA1]):
    cerebro = bt.Cerebro()
    for d in datas:
        cerebro.adddata(d)
    cerebro.addstrategy(strategy)
    strategy = cerebro.run()
    return strategy[0]