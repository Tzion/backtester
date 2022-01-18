import backtrader as bt
from __init__test import TEST_DATA_DIR
from test_common import *
from shutil import copy
from database.data_writer import store
from database import diff_data_feed_csv
from backtrader import num2date
from database import FeedMergeException
    
data_path = TEST_DATA_DIR+'/writer_test.csv'

#TODO files in tmpdir are not cleaned!

class TestStore:
    def test_store_and_add_new_datapoint(self, write_safe_data):
        data, tmpfile = write_safe_data
        store(data, tmpfile)
        diffs = diff_data_feed_csv(data_path, tmpfile)
        assert diffs.empty, f'There are differences between the files:\n{diffs.to_string(index=True)}\n'
        # add new data point and rewrite
        new_datapoint = extend_last_datapoint_by1(data)
        store(data, tmpfile)
        diffs = diff_data_feed_csv(data_path, tmpfile)
        assert len(diffs) == 1, f'Expecting one additional datapoint'
        assert contains_datapoint(new_datapoint, tmpfile), f'Datapoint is not found in the file'


    def test_store_merge_conflict(self, write_safe_data_copy):
        data, tmpfile = write_safe_data_copy
        data.open[0] = 0
        store(data, tmpfile)
        diffs = diff_data_feed_csv(data_path, tmpfile)
        assert diffs.empty, f'Manipulated data should not be written \n{diffs.to_string(index=True)}\n'


    def test_store_weekend_datapoint(self, write_safe_data_copy):
        return
        data_fixture, tmpfile = write_safe_data_copy


@pytest.mark.parametrize('data', [([bt.feeds.GenericCSVData(dataname=data_path, dtformat='%Y-%m-%d', 
                                                            fromdate=datetime(2020, 11, 2), todate=datetime(2020,11,14))])])
@pytest.fixture
def write_safe_data(data_fixture, tmpdir):
    '''Provies initialized data and writable filepath'''
    tmp_path = tmpdir.join("StoreTest_tempfile.csv")
    return data_fixture, tmp_path

@pytest.mark.parametrize('data', [([bt.feeds.GenericCSVData(dataname=data_path, dtformat='%Y-%m-%d', 
                                                            fromdate=datetime(2020, 11, 2), todate=datetime(2020,11,14))])])
@pytest.fixture
def write_safe_data_copy(data_fixture, tmpdir):
    '''Provies initialized data and writable filepath with copy of the data'''
    tmp_path = tmpdir.join("StoreTest_tempfile_copy.csv")
    copy(data_path, str(tmp_path))
    return data_fixture, tmp_path

def extend_last_datapoint_by1(data_fixture):
    data_fixture.forward()
    data_point = {} 
    for alias in data_fixture.lines.getlinealiases():
        line = getattr(data_fixture.lines, alias)
        line[0] = line[-1] + 1
        data_point[alias] = line[-1] + 1
    return data_point

def contains_datapoint(datapoint, file):
    index_label = 'datetime'
    dataframe = pd.read_csv(file, index_col=index_label,)
    datapoint_date = str(num2date(datapoint.pop(index_label)).date())
    file_datapoint = dataframe.loc[datapoint_date]
    return pd.Series(datapoint).eq(file_datapoint).all()
    