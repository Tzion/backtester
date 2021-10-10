from tests.test_common import *
import test_common
from utils import backtrader_helpers as bh
import pytest


@pytest.fixture
def strategy(default_observers, buynsell_name):
    cerebro = bt.Cerebro(stdstats=default_observers)
    cerebro.adddata(DUMMY_DATA)
    cerebro.adddata(DUMMY_DATA) # 2 datas is part of the test
    if (buynsell_name):
        cerebro.addobservermulti(bt.observers.BuySell, obsname=buynsell_name)
    cerebro.addstrategy(DummyStrategy)
    strategy = cerebro.run()[0]
    yield strategy


class TestExtractBuyNSellObservers:

    @pytest.mark.parametrize('default_observers, buynsell_name', [(True, '')])
    def test_extract_buynsell_observers(self, strategy):
        assert len(bh.extract_buynsell_observers(strategy)) == 2

    @pytest.mark.parametrize('default_observers, buynsell_name', [(False, 'non_default_name')])
    def test_extract_buynsell_observers__no_default_observers(self, strategy):
        assert len(bh.extract_buynsell_observers(strategy)) == 2

    @pytest.mark.parametrize('default_observers, buynsell_name', [(False, '')])
    def test_extract_buynsell_observers__no_buynsell_observers(self, strategy, default_observers):
        assert len(bh.extract_buynsell_observers(strategy)) == 0


class ExtractTradesStrategy(bt.Strategy):
    def next(self):
        if self.datetime.idx == 0:
            self.buy(data=self.data0, tradeid=0)
        if self.datetime.idx == 3:
            self.sell(data=self.data0, tradeid=0)
        if self.datetime.idx == 10:
            self.buy(data=self.data0, tradeid=0)
        if self.datetime.idx == 13:
            self.sell(data=self.data0, tradeid=0)
        if self.datetime.idx == 20:
            self.buy(data=self.data0, tradeid=2)
        if self.datetime.idx == 23:
            self.sell(data=self.data0, tradeid=2)
        if self.datetime.idx == 20:
            self.buy(data=self.data1, tradeid=2)
        if self.datetime.idx == 23:
            self.sell(data=self.data1, tradeid=2)
        

@pytest.mark.parametrize('strategy, datas', [(ExtractTradesStrategy,[test_common.TEST_DATA0, test_common.TEST_DATA1])])
def test_extract_all_trades(strategy_fixture):
    trades = bh.extract_trades_list(strategy_fixture)
    assert len(trades) == 4