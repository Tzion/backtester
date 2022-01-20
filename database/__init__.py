import pandas as pd
import backtrader as bt
from backtrader import num2date

def diff_data_feed_csv(file1, file2, columns=None):
    df1 = pd.read_csv(file1, parse_dates=[0], index_col=0)
    df2 = pd.read_csv(file2, parse_dates=[0], index_col=0)
    return diff_data_feed(df1, df2, columns)

def diff_data_feed(dataframe1, dataframe2, columns=None):
    df1 = pd.DataFrame(dataframe1, columns=columns)
    df2 = pd.DataFrame(dataframe2, columns=columns)
    diffs_indexes = df1.eq(df2).all(axis=1) == False
    difference = df1[diffs_indexes] - df2[diffs_indexes]
    difference = difference.applymap(lambda v: v or '') # convert 0 to '' just to make it easier to read
    return difference

def merge_data_feeds_csv(file1, file2) -> pd.DataFrame:
    dataframe1 = pd.read_csv(file1, parse_dates=[0], index_col=0)
    dataframe2 = pd.read_csv(file2, parse_dates=[0], index_col=0)
    merged = merge_data_feeds(dataframe1, dataframe2)
    return merged

def merge_data_feeds(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame):
    _validate_headers(dataframe1, dataframe2)
    return _merge_data_frames(dataframe1, dataframe2)
    
def _validate_headers(dataframe1, dataframe2):
    if (dataframe1.columns == dataframe2.columns).all():
        return True
    else:
        raise FeedMergeException('Feeds have different headers and cannot be merged')

def _merge_data_frames(dataframe1, dataframe2):
    merged = pd.merge(dataframe1, dataframe2, how='outer')  # for debugging do pd.merge(..., indicator=True)
    merge_on = [dataframe1.index.name] + list(dataframe1.columns.intersection(dataframe2.columns))
    merged = pd.merge(dataframe1, dataframe2, how='outer', on=merge_on)  # for debugging do pd.merge(..., indicator=True)
    def no_conflicts(dataframe): 
        intersect_dates = dataframe.index.intersection(merged.index)
        compare_same_dates = merged.eq(dataframe).loc[intersect_dates]
        return compare_same_dates.all().all()  # rows of the same date contain similar values as the merge result -> no coflicts
    if not no_conflicts(dataframe2) or not no_conflicts(dataframe1):
        raise FeedMergeException('Merge shows conflicts of values in dataframes')
    return merged


class FeedMergeException(Exception):
    pass


def convert_to_dataframe(feed: bt.DataBase, idx_line='datetime', lines=['open', 'high', 'low', 'close', 'volume'], date_only=True)-> pd.DataFrame:
    if not lines or len(lines) == 0:
        lines = list(feed.lines._getlines())
        lines.remove(idx_line)
    index = getattr(feed.lines, idx_line).getzero(idx=0, size=len(feed))
    values = {line: getattr(feed.lines, line).getzero(idx=-0, size=len(feed)) for line in lines}
    df = pd.DataFrame(index=pd.Series(index, name=idx_line), data=values)
    df.index = df.index.map(lambda timestamp: num2date(timestamp, feed._tz))
    df.index = df.index.map(lambda datetime: datetime.date()) if date_only else df.index
    return df
