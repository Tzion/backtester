import pandas as pd
import numpy
import backtrader as bt
from backtrader import num2date
from typing import Callable

DATETIME_LABEL = 'datetime'

def diff_data_feed_csv(file1, file2, columns=None):
    return diff_data_feed(csv_to_dataframe(file1), csv_to_dataframe(file2), columns)

def diff_data_feed(dataframe1, dataframe2, columns=None):
    df1 = pd.DataFrame(dataframe1, columns=columns)
    df2 = pd.DataFrame(dataframe2, columns=columns)
    diffs_indexes = df1.eq(df2).all(axis=1) == False
    difference = df1[diffs_indexes] - df2[diffs_indexes]
    difference = difference.applymap(lambda v: v or '') # convert 0 to '' just to make it easier to read
    return difference

def merge_data_feeds_csv(file1, file2, include_intervals=False):
    return merge_data_feeds(csv_to_dataframe(file1), csv_to_dataframe(file2), include_intervals)

def merge_data_feeds(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame, include_intervals=False, validator:Callable[[pd.DataFrame],bool]=None):
    '''
    Returns dataframe which is the join merge result of the 2 dataframes.
    If include_interval is True, it returns tuple of (merge_result, intervals),
    intervals contains numberic indexies of the rows, of the merge result's dataframe,
    that exists in dataframe2 but not in dataframe1.
    '''
    _validate_headers(dataframe1, dataframe2)
    merged, intervals = _merge_data_frames(dataframe1, dataframe2, include_intervals)
    if validator and not validator(merged):
        raise FeedMergeException(f'Merge result fails on validation of {validator}')
    return (merged, intervals) if include_intervals else merged
    
def _validate_headers(dataframe1, dataframe2):
    # this validation if for verbose feedback - merge fails anyway due to header conflict
    if set(dataframe1.columns) == set(dataframe2.columns):
        return True
    else:
        raise FeedMergeException('Feeds have different headers and cannot be merged')

def _merge_data_frames(dataframe1, dataframe2, include_intervals):
    merge_on = [dataframe1.index.name] + list(dataframe1.columns.intersection(dataframe2.columns))
    merged_and_intervals = pd.merge(dataframe1, dataframe2, how='outer', on=merge_on, indicator='intervals', sort=True)
    merged = merged_and_intervals.drop('intervals', axis=1)
    def no_conflicts(dataframe): 
        intersect_dates = dataframe.index.intersection(merged.index)
        compare_same_dates = merged.eq(dataframe).loc[intersect_dates]
        return compare_same_dates.all().all()  # rows of the same date contain similar values as the merge result -> no coflicts
    if not no_conflicts(dataframe2) or not no_conflicts(dataframe1):
        raise FeedMergeException('Merge shows conflicts of values in dataframes')
    if include_intervals:
        intervals = _find_new_intervals(merged_and_intervals)
        return merged, intervals
    return merged, None


def _find_new_intervals(dataframe, column='intervals'):
    new_interval_identifier = 'right_only'
    new_rows = numpy.where(dataframe['intervals'] == new_interval_identifier)[0]

    def find_ascending_intervals(numbers):
        intervals = []
        interval = (numbers[0], numbers[0])
        for row in numbers:
            if row == interval[1] + 1:
                interval = (interval[0], row)
            if row > interval[1] + 1:
                intervals.append(interval)
                interval = (row, row)
        if interval:
            intervals.append(interval)
        return intervals
    return find_ascending_intervals(new_rows) if len(new_rows) else []
    

class FeedMergeException(Exception):
    pass

def feed_to_dataframe(feed: bt.DataBase, idx_line=DATETIME_LABEL, lines=['open', 'high', 'low', 'close', 'volume'], date_only=True)-> pd.DataFrame:
    if not lines or len(lines) == 0:
        lines = list(feed.lines._getlines())
        lines.remove(idx_line)
    index = getattr(feed.lines, idx_line).getzero(idx=0, size=len(feed))
    values = {line: getattr(feed.lines, line).getzero(idx=-0, size=len(feed)) for line in lines}
    df = pd.DataFrame(index=pd.Series(index, name=idx_line), data=values)
    df.index = df.index.map(lambda timestamp: num2date(timestamp, feed._tz)) # convert to datetime.datetime
    df.index = df.index.map(lambda datetime: datetime.date()) if date_only else df.index
    df.index = pd.to_datetime(df.index) # since pandas force the index type to be pandas.datetime on read_csv(), I have to align with that here.
    return df

def csv_to_dataframe(file) -> pd.DataFrame:
    return pd.read_csv(file, index_col=[0], parse_dates=True)
