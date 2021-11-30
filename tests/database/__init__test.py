from database import DataSource, diff_data_feed_csv, get_feed_file_path
from tests.test_common import *
import test_common


def test_diff_data_feed_csv():
    pass


class TestDataFeeds:
    
    @pytest.mark.parametrize('symbol', ('AAL', 'GME', 'GLD'))
    def test_diff_in_data_feeds_from_different_sources(self, symbol):
        print(get_feed_file_path(symbol, DataSource.TRADING_VIEW))