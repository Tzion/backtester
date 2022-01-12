import backtrader as bt
from __init__test import TEST_DATA_DIR
from test_common import *
from shutil import copy
from database.data_writer import store
from database import diff_data_feed_csv
    
data_path = TEST_DATA_DIR+'/writer_test.csv'

#TODO files in tmpdir are not cleaned!

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
    extend_last_data_point_by1(data_fixture)
    store(data_fixture, tmpfile)
    diffs = diff_data_feed_csv(data_path, tmpfile)
    assert len(diffs) == 1, f'Expecting one additional datapoint'

def test_store_merge_conflict():
    pass

def test_store_weekend_datapoint():
    pass

def extend_last_data_point_by1(data_fixture):
    data_fixture.forward()
    for line in data_fixture.lines:
        line[0] = line[-1] + 1

    