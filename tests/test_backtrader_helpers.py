from .test_common import *
from backtrader import cerebro
from utils import backtrader_helpers as bh
import unittest


class TestBacktraderHelpers(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        global cerebro, strategy
        cerebro = bt.Cerebro()
        cerebro.adddata(DUMMY_DATA)
        cerebro.addobserver(bt.observers.BuySell, obsname='non_default_name')
        cerebro.addstrategy(DummyStrategy)
        strategy = cerebro.run()[0]



    def test_extract_buynsell_observer(self):
        self.assertIsNotNone(bh.extract_buynsell_observer(strategy))
