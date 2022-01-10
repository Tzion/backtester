import pandas as pd

def diff_data_feed_csv(file1, file2, columns=['open', 'low', 'high', 'close',]):
    # TODO support date range
    df1 = pd.read_csv(file1, parse_dates=[0])
    df2 = pd.read_csv(file2, parse_dates=[0])
    return diff_data_feed(df1, df2, columns)

def diff_data_feed(dataframe1, dataframe2, columns=['open', 'low', 'high', 'close',]):
    df1 = pd.DataFrame(dataframe1, columns=columns)
    df2 = pd.DataFrame(dataframe2, columns=columns)
    diffs_indexes = df1.eq(df2).all(axis=1) == False
    difference = df1[diffs_indexes] - df2[diffs_indexes]
    difference = difference.applymap(lambda v: v or '') # convert 0 to '' just to make it easier to read
    return difference

def merge_data_feeds_csv(file1, file2) -> pd.DataFrame:
    dataframe1 = pd.read_csv(file1, parse_dates=[0])
    dataframe2 = pd.read_csv(file2, parse_dates=[0])
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
    def no_conflicts(dataframe): 
        same_date = merged.eq(dataframe)
        same_date = same_date[same_date['Date'] == True]  # TODO get rid of this hardcoded string
        return same_date.all().all()  # rows of the same date contain similar values as the merge result -> no coflicts
    if not no_conflicts(dataframe2) or not no_conflicts(dataframe1):
        raise FeedMergeException('Merge shows conflicts of values in dataframes')
    return merged


class FeedMergeException(Exception):
    pass