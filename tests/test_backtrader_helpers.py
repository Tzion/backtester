from tests.test_common import *
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