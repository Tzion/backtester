from database import DataSource, diff_data_feed_csv, get_feed_file_path
from tests.test_common import *
from database import merge_data_feeds_csv, merge_data_feeds, FeedMergeException
from random import random, randrange
from logger import *

TEST_DATA_DIR = 'tests/database/data/'

class TestDataFeeds:

    @pytest.mark.parametrize('symbol', ('BATS_AAL, 1D', 'GME', 'GLD'))
    def test_diff_in_data_feeds_from_different_sources(self, symbol):
        print(get_feed_file_path(symbol, DataSource.TRADING_VIEW))
        #TODO

class TestMergeDataFeeds:
    FULL_DATA = TEST_DATA_DIR + 'merge_test_datapoints_0-22.csv'
    @pytest.mark.parametrize('file1, file2', [(TEST_DATA_DIR + 'merge_test_datapoints_0-22.csv', 
                                               TEST_DATA_DIR + 'merge_test_datapoints_0-20.csv'),
                                              (TEST_DATA_DIR + 'merge_test_datapoints_0-22.csv',
                                              TEST_DATA_DIR +  'merge_test_datapoints_2-20.csv'),
                                              (TEST_DATA_DIR + 'merge_test_datapoints_0-20.csv',
                                               TEST_DATA_DIR + 'merge_test_datapoints_20-22.csv'), ])
    def test_merge_data_feeds(self, file1, file2):
        merged = merge_data_feeds_csv(file1, file2)
        assert len(merged) == 23, 'Length of merged result is shorted than expected'
        entire_data = pd.read_csv(TestMergeDataFeeds.FULL_DATA)
        assert all(entire_data.eq(merged)), 'Data of merged result is different than the completed data'
        merged_opposite = merge_data_feeds_csv(file2, file1)
        assert all(merged.eq(merged_opposite)), 'Merge result is not symetric'

    def test_merge_data_feeds__values_mismatch(self, file1=TEST_DATA_DIR + 'merge_test_datapoints_0-22.csv', file2=TEST_DATA_DIR + 'merge_test_datapoints_0-20.csv'):
        df1 = pd.read_csv(file1, parse_dates=[0])
        df2 = pd.read_csv(file2, parse_dates=[0])
        manipulate_random_value(df2)
        with pytest.raises(FeedMergeException):
            merge = merge_data_feeds(df1, df2)
    
    def test_merge_data_feeds__columns_mismatch(self, file=TEST_DATA_DIR + 'merge_test_datapoints_0-22.csv'):
        df1 = pd.read_csv(file, parse_dates=[0])
        df2 = df1.copy()
        df2 = flip_columns(df2)
        with pytest.raises(FeedMergeException):
            merge = merge_data_feeds(df2, df1)
    
    def test_merge_data_feeds__columns_case_sensetive(self, file=TEST_DATA_DIR + 'merge_test_datapoints_0-22.csv'):
        df1 = pd.read_csv(file, parse_dates=[0])
        df2 = df1.rename(columns=str.lower, copy=True)
        with pytest.raises(Exception):
            merge = merge_data_feeds(df1, df2)
        
    def test_merge_data_feeds__extra_column(self, file=TEST_DATA_DIR + 'merge_test_datapoints_0-22.csv'):
        df1 = pd.read_csv(file, parse_dates=[0])
        df2 = df1.copy()
        df2 = df1.join(df1[df1.columns[3]].rename('columnX'))
        with pytest.raises(Exception):
            merge = merge_data_feeds(df1, df2)


def flip_columns(dataframe: pd.DataFrame):
    col2 = dataframe[dataframe.columns[2]]
    dataframe = dataframe.drop(columns=dataframe.columns[2])
    dataframe = dataframe.join(col2)
    return dataframe

def manipulate_random_value(dataframe: pd.DataFrame):
    x = randrange(1, dataframe.shape[0])
    y = randrange(1, dataframe.shape[1])
    logdebug(f'changing value at location ({x},{y})')
    dataframe.iloc[x,y] = dataframe.iloc[x,y] + 0.01

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
