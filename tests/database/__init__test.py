from database import DataSource, diff_data_feed_csv, get_feed_file_path
from tests.test_common import *
import test_common
from database import merge_data_feeds
import os
from functools import wraps


class TestDataFeeds:
    
    @pytest.mark.parametrize('symbol', ('AAL', 'GME', 'GLD'))
    def test_diff_in_data_feeds_from_different_sources(self, symbol):
        print(get_feed_file_path(symbol, DataSource.TRADING_VIEW))
    
    @pytest.mark.parametrize('file1, file2', [('tests/database/merge_test_datapoints_0-22.csv', 'tests/database/merge_test_datapoints_0-20.csv'),
                                              ('tests/database/merge_test_datapoints_0-22.csv', 'tests/database/merge_test_datapoints_2-20.csv'),
                                              ('tests/database/merge_test_datapoints_0-20.csv', 'tests/database/merge_test_datapoints_20-22.csv'),
                                            ]
                             )
    def test_merge_data_feeds(self, file1, file2):
        merged = merge_data_feeds(file1, file2)
        assert len(merged) == 23, 'Length of merged result is shorted than expected'
        entire_data = pd.read_csv('tests/database/merge_test_datapoints_0-22.csv')
        entire_data.eq(merged), 'Data of merged result is different than the completed data'
        merged_opposite = merge_data_feeds(file2, file1)
        assert merged.eq(merged_opposite), 'Merge result is not symetric'

    def test_merge_data_feeds__data_mismatch(self, file1, file2):
        pass



# A try to manipulate the test arguments
@pytest.fixture(params=['file1', 'file2'])
def copy_files(request):
    print(request)

@pytest.mark.usefixtures('copy_files')
# @pytest.mark.parametrize('file1, file2', [('tests/database/merge_test_datapoints0-22.csv', 'merge_test_datapoints0-20')])
def test_files(file1='s', file2='auw'):
    # print(file1)
    print('inside the test='+file2)
    pass

