from tests.test_common import *
from database import csv_to_dataframe, feed_to_dataframe, merge_data_feeds_csv, merge_data_feeds, FeedMergeException
from random import randrange
from logger import *

TEST_DATA_DIR = 'tests/database/data/'

class TestDataFeeds:

    @pytest.mark.parametrize('symbol', ('BATS_AAL, 1D', 'GME', 'GLD'))
    def test_diff_in_data_feeds_from_different_sources(self, symbol):
        # print(get_feed_file_path(symbol, DataSource.TRADING_VIEW))
        pass
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
        entire_data = pd.read_csv(TestMergeDataFeeds.FULL_DATA, parse_dates=[0], index_col=0)
        assert entire_data.equals(merged), 'Data of merged result is different than the completed data'
        merged_opposite = merge_data_feeds_csv(file2, file1)
        assert merged.equals(merged_opposite), 'Merge result is not symetric'
    
    def test_merge_intervals(self, file1=TEST_DATA_DIR+'merge_test_datapoints_0-22.csv', file2=TEST_DATA_DIR+'merge_test_datapoints_2-20.csv'):
       intervals = merge_data_feeds_csv(file1, file2, include_intervals=True)[1]
       assert intervals[0] == (0,1)
       assert intervals[1] == (21,22)
       intervals = merge_data_feeds_csv(file2, file1, include_intervals=True)[1]
       assert intervals[0] == (0,1), 'merge_data_feeds is expected to be a Symetric Relation'
       assert intervals[1] == (21,22), 'merge_data_feeds is expected to be a Symetric Relation'

    def test_merge_data_feeds__values_mismatch(self, file1=TEST_DATA_DIR + 'merge_test_datapoints_0-22.csv', file2=TEST_DATA_DIR + 'merge_test_datapoints_0-20.csv'):
        df1 = pd.read_csv(file1, parse_dates=[0], index_col=0)
        df2 = pd.read_csv(file2, parse_dates=[0], index_col=0)
        manipulate_random_value(df2)
        with pytest.raises(FeedMergeException):
            merge = merge_data_feeds(df1, df2)
    
    def test_merge_data_feeds__columns_mismatch(self, file=TEST_DATA_DIR + 'merge_test_datapoints_0-22.csv'):
        df1 = pd.read_csv(file, parse_dates=[0], index_col=0)
        df2 = df1.copy()
        df2 = flip_columns(df2)
        with pytest.raises(FeedMergeException):
            merge = merge_data_feeds(df2, df1)
    
    def test_merge_data_feeds__columns_case_sensetive(self, file=TEST_DATA_DIR + 'merge_test_datapoints_0-22.csv'):
        df1 = pd.read_csv(file, parse_dates=[0], index_col=0)
        df2 = df1.rename(columns=str.lower, copy=True)
        with pytest.raises(FeedMergeException):
            merge = merge_data_feeds(df1, df2)
        
    def test_merge_data_feeds__extra_column(self, file=TEST_DATA_DIR + 'merge_test_datapoints_0-22.csv'):
        df1 = pd.read_csv(file, parse_dates=[0], index_col=0)
        df2 = df1.copy()
        df2 = df1.join(df1[df1.columns[3]].rename('columnX'))
        with pytest.raises(FeedMergeException):
            merge = merge_data_feeds(df1, df2)
        
    def test_merge_data_feeds__duplicate_date_middle(self, file=TEST_DATA_DIR + 'merge_test_datapoints_0-22.csv'):
        df1 = pd.read_csv(file, parse_dates=[0], index_col=0).iloc[:8]
        df2 = df1.copy()
        df2 = pd.concat([df2.iloc[:4], df2.iloc[3:]])
        with pytest.raises(FeedMergeException):
            merge = merge_data_feeds(df1, df2)

    def test_merge_data_feeds__duplicate_date_overlap(self, file=TEST_DATA_DIR + 'merge_test_datapoints_0-22.csv'):
        df1 = pd.read_csv(file, parse_dates=[0], index_col=0).iloc[:10]
        df2 = df1.copy().iloc[6:]
        df1 = df1.iloc[:7]
        with pytest.raises(FeedMergeException):
            merge = merge_data_feeds(df1, df2)


@pytest.mark.parametrize('data', [([bt.feeds.GenericCSVData(dataname=TEST_DATA_DIR+'convert_test.csv', dtformat='%Y-%m-%d', 
                                                            fromdate=datetime(2020, 11, 2), todate=datetime(2020,11,14))])])
def test_convert_to_dataframe(data_fixture):
    df_converted = feed_to_dataframe(data_fixture, lines=['open','high','low','close','volume', 'openinterest'])
    df_source = csv_to_dataframe(TEST_DATA_DIR+'convert_test.csv')
    assert df_converted.equals(df_source), 'Conversions are not equal'
    try:
        merge_data_feeds(df_converted, df_source)
    except Exception as e:
        pytest.fail(f'Conversions are not mergable. Exception: {e}')
    

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
