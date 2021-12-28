import backtrader as bt
from tests.test_common import *
import test_common
from database.data_loader import HistoricalLoader
from datetime import datetime
import pytest
from __init__test import TEST_DATA_DIR
from backtrader import date2num, num2date
from utils.backtrader_helpers import convert_to_dataframe
from database import diff_data_feed


def assert_prices(feed, datetime, open, high, low, close, ago=0):
    assert feed.datetime.date(ago) == datetime.date()
    assert feed.open[ago] == open
    assert feed.high[ago] == high
    assert feed.low[ago] == low
    assert feed.close[ago] == close

def get_feed_file_path_mock(symbol):
    return TEST_DATA_DIR + symbol + '.csv'

# redundant TODO remove
def compare_feed(feed, dataframe):
    report = []
    for i in range(len(feed), -1, -1):
        date = str(feed.datetime.date(-i))
        data = dataframe.loc[date]
        if feed.open[-i] != data.open:
            report.append(f'Mismatch at {date}: open price, feed={feed.open[-i]}, data={data.open}\n')
    if report:
        print(''.join(report))
        return False
    return True
    
class TestHistoricalLoader:
    """IB Gateway or TWS must be connected prior to these tests"""
        
    @pytest.fixture
    def loader(self, cerebro):
        return HistoricalLoader(cerebro)

    def test_request_feed_data(self, cerebro, loader):
        """Request data of specific stock and date and verify the prices received """
        loader.load_feeds(['ZION'], datetime(2020,7,31), datetime(2020,8,1), backfill_from_database=False)
        cerebro.addstrategy(test_common.DummyStrategy)
        cerebro.run()
        # d = cerebro.datas[0]
        # print([(str(d.datetime.datetime(ago=-i)), d.open[-i]) for i in range(len(d)-1, -1,-1)])
        assert_prices(cerebro.datas[0], datetime(2020,7,31), 32.6, 32.69, 31.94, 32.47), 'Data mismatch'
    

    def test_request_feed_data_for_period(self, cerebro, loader, start=datetime(2020,7,1), end=datetime(2020,8,1)):
        loader.load_feeds(['ZION'], start_date=start, end_date=end, backfill_from_database=False, store=False)
        cerebro.addstrategy(test_common.DummyStrategy)
        cerebro.run()
        requested_data = cerebro.datas[0]
        df = pd.read_csv(TEST_DATA_DIR+'ZION_BATS_TRADINGVIEW_1D.csv', index_col=0, converters={0:lambda long_date:long_date[:10]}, parse_dates=[0])
        requested_df = convert_to_dataframe(requested_data)
        requested_df.index = requested_df.index.map(lambda dt: dt.date)
        diffs = diff_data_feed(requested_df, df.loc[requested_df.index[0]:requested_df.index[-1]])
        assert diffs.all().all(), f'There are differences between the requested data and the static data:\n {diffs.to_string(index=True)}'
        # assert compare_feed(requested_data, df), 'Data mismatch'

    # TODO test to compare volumes of requested feed and static
        
    def test_request_feed_data_on_weekend(self, cerebro, loader):
        """Request data over the weekend when there is no trading of the contract"""
        weekend_start = datetime(2021,11,13)
        assert weekend_start.isoweekday() == 6  # making sure it's Saturday
        weekend_end = datetime(2021, 11,15)
        assert weekend_end.isoweekday() == 1
        loader.load_feeds(['ZION'], weekend_start, weekend_end, backfill_from_database=False)
        loader.load_feeds(['NVDA'], datetime(2021,11,15), datetime(2021,11,22), backfill_from_database=False)
        cerebro.addstrategy(test_common.DummyStrategy)
        cerebro.run()
        assert len(cerebro.datas[0]) == 0, 'data should be empty - since it\'s weekend'
        assert len(cerebro.datas[1]) == 5, 'data should have full business week - 5 days'
        
    def test_backfill_one_bar(self, cerebro, loader, mocker):
        """Load data feed from file, fill missing bar from live data server"""
        mocker.patch('database.get_feed_file_path', return_value=TEST_DATA_DIR + 'backfill_test.csv')
        loader.load_feeds(['NVDA'], start_date=datetime(2021, 10, 28), end_date=datetime(2021, 11, 10), backfill_from_database=False, store=False)
        cerebro.addstrategy(DummyStrategy)
        cerebro.run()
        d = cerebro.datas[0]
        print([(str(d.datetime.datetime(ago=-i)), d.open[-i]) for i in range(len(d)-1, -1,-1)])
        assert len(cerebro.datas[0]) == 3
        assert_prices(cerebro.datas[0], datetime(2021, 11, 19), 44.44, 66.66, 33.33, 55.55, ago=1), 'Mismatch with data from file'
        assert_prices(cerebro.datas[0], datetime(2021, 11, 22), 335.17, 346.47, 319.0, 319.56, ago=0), 'Mismatch with data from server'



#TODO delete below section
class St(bt.Strategy):
    def next(self):
        pass


def query_data():
    from samples.ibtest.ibtest import TestStrategy
    cerebro = bt.Cerebro()
    istore = bt.stores.IBStore(port=7497, notifyall=False, _debug=True)
    # exchanges =['SMART','AMEX','NYSE','CBOE','PHLX','ISE','CHX','ARCA','ISLAND','DRCTEDGE',
    #             'BEX','BATS','EDGEA','CSFBALGO','JEFFALGO','BYX','IEX','EDGX','FOXRIVER','PEARL','NYSENAT','LTSE','MEMX','PSX']
    exchanges =['SMART']
    for exc in exchanges:
        data = istore.getdata(dataname=f'NVDA-STK-{exc}-USD', fromdate=datetime(2021,11,16), what='TRADES', historical=True, useRTH=True)
        cerebro.adddata(data)
    cerebro.addstrategy(St)
    strat = cerebro.run()[0]
    pass
    
    
if __name__ == '__main__':
    query_data()