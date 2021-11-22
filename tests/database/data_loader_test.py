import backtrader as bt
from tests.test_common import *
import test_common
from database.data_loader import HistoricalLoader
from datetime import datetime
import pytest

@pytest.fixture
def cerebro():
    return bt.cerebro.Cerebro()


def assert_prices(feed, datetime, open, high, low, close, ago=0):
    assert feed.datetime.date(ago) == datetime.date()
    assert feed.open[ago] == open
    assert feed.high[ago] == high
    assert feed.low[ago] == low
    assert feed.close[ago] == close

class TestLiveLoader:
        
    @pytest.fixture
    def loader(self, cerebro):
        return HistoricalLoader(cerebro)

    def test_request_feed_data(self, cerebro, loader):
        """Request data of specific stock in known dates and verify the prices received """
        loader.load_feeds(['ZION'], datetime(2020,7,31), datetime(2020,8,1))
        cerebro.addstrategy(test_common.DummyStrategy)
        cerebro.run()
        assert_prices(cerebro.datas[0], datetime(2020,7,31), 32.6, 32.69, 31.94, 32.47)
        pass

    def test_load_feed_from_disk_backfill_one_bar(self, cerebro, loader):
        """Load data feed from file, fill missing bar from live data server"""
        # cerebro = bt.cerebro.Cerebro()
        # loader = LiveLoader(cerebro)
        loader.load_feeds(['NVDA'], start_date=datetime(2019, 4, 10), end_date=datetime(2019, 4, 30))
        class Strategy(bt.Strategy):
            def next(self):
                # TODO test assertions
                print(self.data0.datetime.datetime())
        cerebro.addstrategy(Strategy)
        cerebro.run()