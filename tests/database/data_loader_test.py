import backtrader as bt
from database.data_loader import LiveLoader
from datetime import datetime
import pytest

@pytest.fixture
def cerebro():
    return bt.cerebro.Cerebro()

@pytest.fixture
def loader(cerebro):
    return LiveLoader(cerebro)


class TestLiveLoader:

    def test_request_feed_data(self):
        """Request data of specific stock in known dates and verify the prices received """
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