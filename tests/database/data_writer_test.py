import backtrader as bt
from __init__test import TEST_DATA_DIR
from test_common import *
from shutil import copy
from database.data_writer import store
from database import diff_data_feed_csv
from backtrader import num2date
    
data_path = TEST_DATA_DIR+'/writer_test.csv'

#TODO files in tmpdir are not cleaned!

#TODO unfiy 3 tests to one as: write to new file, add new data point and rewrite. 
# The added value is that we're validate that the write and append, keep on the same format
@pytest.mark.parametrize('data', [([bt.feeds.GenericCSVData(dataname=data_path, dtformat='%Y-%m-%d', 
                                                            fromdate=datetime(2020, 11, 2), todate=datetime(2020,11,14))])])
def test_store_to_new_file(data_fixture: bt.feed.FeedBase, tmpdir):
    tmpfile = tmpdir.join("tmpfile.csv")
    store(data_fixture, tmpfile)
    diffs = diff_data_feed_csv(data_path, tmpfile)
    assert diffs.empty, f'There are differences between the files:\n{diffs.to_string(index=True)}\n'


@pytest.mark.parametrize('data', [([bt.feeds.GenericCSVData(dataname=data_path, dtformat='%Y-%m-%d', 
                                                            fromdate=datetime(2020, 11, 2), todate=datetime(2020,11,14))])])
def test_store_to_existing_file(data_fixture: bt.feed.FeedBase, tmpdir):
    tmpfile = tmpdir.join("tmpfile.csv")
    copy(data_path, str(tmpfile))
    store(data_fixture, tmpfile)
    diffs = diff_data_feed_csv(data_path, tmpfile)
    assert diffs.empty, f'There are differences between the files:\n{diffs.to_string(index=True)}\n'

@pytest.mark.parametrize('data', [([bt.feeds.GenericCSVData(dataname=data_path, dtformat='%Y-%m-%d', 
                                                            fromdate=datetime(2020, 11, 2), todate=datetime(2020,11,14))])])
def test_store_new_datapoint(data_fixture: bt.feed.FeedBase, tmpdir):
    tmpfile = tmpdir.join("tmpfile.csv")
    copy(data_path, str(tmpfile))
    new_datapoint = extend_last_datapoint_by1(data_fixture)
    store(data_fixture, tmpfile)
    diffs = diff_data_feed_csv(data_path, tmpfile)
    assert len(diffs) == 1, f'Expecting one additional datapoint'
    assert contains_datapoint(new_datapoint, tmpfile), f'Datapoint is not found in the file'

def test_store_merge_conflict():
    pass

def test_store_weekend_datapoint():
    pass

def extend_last_datapoint_by1(data_fixture):
    data_fixture.forward()
    data_point = {}
    for line in data_fixture.lines:
        line[0] = line[-1] + 1
    for alias in data_fixture.lines.getlinealiases():
        line = getattr(data_fixture.lines, alias)
        data_point[alias] = line[-1] + 1
    return data_point

def contains_datapoint(datapoint, file):
    index_label = 'datetime'
    dataframe = pd.read_csv(file, index_col=index_label,)
    datapoint_date = str(num2date(datapoint.pop(index_label)).date())
    file_datapoint = dataframe.loc[datapoint_date]
    return pd.Series(datapoint).eq(file_datapoint).all()
    