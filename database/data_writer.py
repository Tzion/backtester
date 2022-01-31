import os
import io
import backtrader as bt
from logger import *
from . import merge_data_feeds, FeedMergeException, feed_to_dataframe, csv_to_dataframe
import pandas as pd

class DataWriter():
    
    @staticmethod
    def decorate_writing(live_data: bt.feed.AbstractDataBase, output_filepath: str):
        ''' Adds the data object the ability to save itself to a file.
            This happens as part of the lifecycle of the object by decorating its inner methods '''
        live_data.stop = DataWriter._store_and_stop_decorator(live_data.stop, live_data, output_filepath) 
        return live_data

    @staticmethod
    def _store_and_stop_decorator(stop_func, data, export_file):
        def store_and_stop():
            store(data, export_file)
            stop_func()
        return store_and_stop

        
def store(data, filepath):
    live_data = feed_to_dataframe(data)
    if os.path.exists(filepath) and os.path.isfile(filepath):
        static_data = csv_to_dataframe(filepath)
        try:
            merged, intervals = merge_data_feeds(static_data, live_data, include_intervals=True)
        except FeedMergeException as exp:
            logerror(f'Storing data feed {data._name} failed, path={filepath}. Reason: {exp}')
            live_data.to_csv(filepath+'.premerged')
            return
        write_to_file(merged, intervals, filepath)
    else:
        pd.DataFrame.to_csv(live_data, filepath, index=True)


def write_to_file(merged: pd.DataFrame, intervals, filepath):
    if len(intervals) == 0:
        return
    if len(intervals) == 1 and intervals[0][1] == len(merged)-1:  # the new section is at the end - able to append
        merged[intervals[0][0]:intervals[0][1]+1].to_csv(io.open(filepath, mode='a'), header=False)
    else:
        pd.DataFrame.to_csv(merged, filepath, index=True)
