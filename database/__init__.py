from pathlib import Path
import os
import enum
import pandas as pd
from typing import Optional, Union

PREFIX = 'database/data/'

class DataSource(enum.Enum):
    INTERACTIVE_BROKERS = 1
    TRADING_VIEW = 2
    YAHOO = 3

    def get_name(self):
        return self.name.lower()


def get_feed_file_path(symbol, source: DataSource=DataSource.INTERACTIVE_BROKERS):
    def find_file(symbol, dir):
        matches = list(Path(dir).glob(f'{symbol}.csv')) # TODO bug - ambiguous for symbols A AA
        if len(matches) > 1:
            raise Exception('Ambiguous search results: more than 1 files matches the symbol')
        if not matches:
            raise FileNotFoundError(f'No csv file {symbol}.csv in {dir}')
        return str(matches[0])
        
    dir = f'{PREFIX}{source.get_name()}/'
    path = find_file(symbol, dir)
    if os.path.isfile(path):
        return path
    return None

    
def diff_data_feed_csv(file1, file2, columns=['open', 'low', 'high', 'close',]):
    # TODO support date range
    df1 = pd.read_csv(file1, parse_dates=[0])
    df2 = pd.read_csv(file2, parse_dates=[0])
    columns.insert(0,df1.columns[0])
    df1 = pd.DataFrame(df1, columns=columns)
    df2 = pd.DataFrame(df2, columns=columns)
    equal = df1.eq(df2)
    if equal.all().all():
        return False  # no diffs between dataframes
    else:
        return equal
    # to show details results - next phase
    compare = df11[df11.eq(df22).all(axis=1) == False]
    print(comparison.to_string(index=True))


def merge_data_feeds_csv(file1, file2, export_path=None) -> Optional[pd.DataFrame]:
    dataframe1 = pd.read_csv(file1, parse_dates=[0])
    dataframe2 = pd.read_csv(file2, parse_dates=[0])
    merged = merge_data_feeds(dataframe1, dataframe2)
    if export_path:
        pass # TODO write to file
    return merged

def merge_data_feeds(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame):
    if _pre_merge_validation(dataframe1, dataframe2):
        merged = _merge_data_frames(dataframe1, dataframe2)
        return merged
    else:
        raise FeedMergeException('Feeds contains conflict data and cannot be merged')
    
def _pre_merge_validation(dataframe1, dataframe2):
    '''Verify that there are no conflicts of data of the same dates'''
    return _headers_match(dataframe1 ,dataframe2) and _values_match(dataframe1 ,dataframe2)
    
def _headers_match(dataframe1, dataframe2):
    return (dataframe1.columns == dataframe2.columns).all()

def _values_match(dataframe1, dataframe2):
    return True

def _merge_data_frames(dataframe1, dataframe2):
    merged = pd.merge(dataframe1, dataframe2, how='outer')  # for debugging do merge(..., indicator=True)
    def no_conflicts(dataframe): 
        same_date = merged.eq(dataframe)
        same_date = same_date[same_date['Date'] == True]  # TODO get rid of this hardcoded string
        return same_date.all().all()  # rows of the same date contain similar values as the merge result -> no coflicts
    if not no_conflicts(dataframe2) or not no_conflicts(dataframe1):
        raise FeedMergeException('Feeds value mismatch')
    return merged


class FeedMergeException(Exception):
    pass