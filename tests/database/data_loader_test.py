import backtrader as bt
from tests.test_common import *
import test_common
from database.data_loader import HistoricalLoader
from datetime import datetime
import pytest



def assert_prices(feed, datetime, open, high, low, close, ago=0):
    assert feed.datetime.date(ago) == datetime.date()
    assert feed.open[ago] == open
    assert feed.high[ago] == high
    assert feed.low[ago] == low
    # assert feed.close[ago] == close ## todo fix

class TestLiveLoader:
    """IB Gateway or TWS must be connected prior to these tests"""
        
    @pytest.fixture
    def loader(self, cerebro):
        return HistoricalLoader(cerebro)

    def test_request_feed_data(self, cerebro, loader):
        """Request data of specific stock in known dates and verify the prices received """
        loader.load_feeds(['ZION'], datetime(2020,7,31), datetime(2020,8,1), backfill_from_database=False)
        cerebro.addstrategy(test_common.DummyStrategy)
        cerebro.run()
        assert_prices(cerebro.datas[0], datetime(2020,7,31), 32.6, 32.69, 31.94, 32.47)
    
    def test_request_feed_data_on_weekend(self, cerebro, loader):
        """Request data over the weekend when there is no trading of the contract"""
        weekend_start = datetime(2021,11,13)
        assert weekend_start.isoweekday() == 6  # making sure it's Saturday
        weekend_end = datetime(2021, 11,15)
        assert weekend_end.isoweekday() == 1
        loader.load_feeds(['ZION'], weekend_start, weekend_end, backfill_from_database=False)
        loader.load_feeds(['ZION'], datetime(2021,11,15), datetime(2021,11,22), backfill_from_database=False)
        cerebro.addstrategy(test_common.DummyStrategy)
        cerebro.run()
        assert len(cerebro.datas[0]) == 0
        assert len(cerebro.datas[1]) == 5
        

    def test_backfill_one_bar(self, cerebro, loader):
        """Load data feed from file, fill missing bar from live data server"""
        loader.load_feeds(['NVDA'], start_date=datetime(2021, 11, 19), end_date=datetime(2021, 11, 23), backfill_from_database=True)
        cerebro.addstrategy(DummyStrategy)
        cerebro.run()
        # assert len(cerebro.datas[0]) == 2
        assert_prices(cerebro.datas[0], datetime(2021, 11, 19), 44.44, 66.66, 33.33, 55.55)
        assert_prices(cerebro.datas[0], datetime(2021, 11, 22), 335.17, 346.47, 333.50, 0)