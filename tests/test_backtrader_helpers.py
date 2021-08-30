from tests.test_common import *
from backtrader import cerebro
from utils import backtrader_helpers as bh
import unittest
import pytest


@pytest.fixture
def strategy():
    cerebro = bt.Cerebro()
    cerebro.adddata(DUMMY_DATA)
    cerebro.addstrategy(DummyStrategy)
    strategy = cerebro.run()[0]
    yield strategy

class TestBacktraderHelpers():
    def test_extract_buynsell_observer(self, strategy):
        assert bh.extract_buynsell_observer(strategy) is not None


def test_extract_buynsell_observer__non_default_name():
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.adddata(DUMMY_DATA)
    cerebro.addobserver(bt.observers.BuySell, obsname='non_default_name')
    cerebro.addstrategy(DummyStrategy)
    strategy = cerebro.run()[0]
    assert bh.extract_buynsell_observer(strategy) is not None


