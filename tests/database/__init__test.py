from database import DataSource, diff_data_feed_csv, get_feed_file_path
from tests.test_common import *
import test_common
import os


class TestDataFeeds:
    
    @pytest.mark.parametrize('symbol', ('AAL', 'GME', 'GLD'))
    def test_diff_in_data_feeds_from_different_sources(self, symbol):
        print(get_feed_file_path(symbol, DataSource.TRADING_VIEW))
    
    @pytest.mark.parametrize('file1, file2', [('tests', '.')])
    def test_merge_data_feeds(self, file1, file2):
        print(os.listdir(file1))
        print(os.listdir(file2))