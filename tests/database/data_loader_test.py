from tests.test_common import *
import test_common
from database.data_loader import IBLoader
from datetime import datetime
import pytest
from __init__test import TEST_DATA_DIR
from database import diff_data_feed, convert_to_dataframe


def assert_prices(feed, datetime, open, high, low, close, ago=0):
    assert feed.datetime.date(-ago) == datetime.date()
    assert feed.open[-ago] == open
    assert feed.high[-ago] == high
    assert feed.low[-ago] == low
    assert feed.close[-ago] == close

class TestIBLoader:
    """TWS or IB Gateway MUST BE CONNECTED prior to these tests"""
        
    @pytest.fixture
    def loader(self, cerebro):
        return IBLoader(cerebro)

    #TODO add exception message to check the connectivity
    
    @pytest.mark.parametrize('start, end', [('2020-11-02', '2021-03-19')])
    def test_request_feed_data_for_period(self, cerebro, loader, start, end, mocker):
        static_data = TEST_DATA_DIR + 'request_test-ZION-IB.csv'
        mocker.patch.object(loader.source, 'get_feed_path', return_value=static_data)
        loader.load_feeds(['ZION'], start_date=datetime.fromisoformat(start), end_date=datetime.fromisoformat(end), backfill_from_database=False, store=False)
        cerebro.addstrategy(test_common.DummyStrategy)
        cerebro.run()
        requested_data = cerebro.datas[0]
        df = pd.read_csv(static_data, index_col=0, parse_dates=[0])
        requested_df = convert_to_dataframe(requested_data)
        diffs = diff_data_feed(requested_df, df.loc[requested_df.index[0]:requested_df.index[-1]], columns=['open', 'low', 'high', 'close','volume'])
        assert diffs.empty, f'There are differences between the requested data and the static data:\n{diffs.to_string(index=True)}\n'

    def test_request_feed_data_on_weekend(self, cerebro, loader):
        """Request data over the weekend when there is no trading of the contract"""
        weekend_start = datetime(2021,11,13)
        assert weekend_start.isoweekday() == 6  # making sure it's Saturday
        weekend_end = datetime(2021, 11,15)
        assert weekend_end.isoweekday() == 1
        loader.load_feeds(['ZION'], weekend_start, weekend_end, backfill_from_database=False, store=False)
        loader.load_feeds(['NVDA'], datetime(2021,11,15), datetime(2021,11,22), backfill_from_database=False)
        cerebro.addstrategy(test_common.DummyStrategy)
        cerebro.run()
        assert len(cerebro.datas[0]) == 0, 'data should be empty - since it\'s weekend'
        assert len(cerebro.datas[1]) == 5, 'data should have full business week - 5 days'
        
    def test_backfill_one_bar(self, cerebro, loader, mocker):
        """Load data feed from file, fill missing bar from live data server"""
        mocker.patch.object(loader.source, 'get_feed_path', return_value=TEST_DATA_DIR + 'backfill_test.csv')
        loader.load_feeds(['NVDA'], start_date=datetime(2021, 11, 19), end_date=datetime(2021, 11, 23), backfill_from_database=True, store=False)
        cerebro.addstrategy(DummyStrategy)
        cerebro.run()
        assert len(cerebro.datas[0]) == 2
        assert_prices(cerebro.datas[0], datetime(2021, 11, 19), 44.44, 66.66, 33.33, 55.55, ago=1), 'Mismatch with data from file'
        assert_prices(cerebro.datas[0], datetime(2021, 11, 22), 335.17, 346.47, 319.0, 319.56, ago=0), 'Mismatch with data from server'
