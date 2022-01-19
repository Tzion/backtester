from genericpath import exists
import backtrader as bt
from logger import *
import io
from functools import reduce
from . import merge_data_feeds_csv, FeedMergeException
import pandas as pd
import os

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
        
'''
TODO Design Cahgne Required:
All of the merging mechanisms should be uniform and based on dataframes;
Now the merging process is based on writing to file line-by-line, but the validations 
are using dataframes. This is to expenssive since writing complete files is overkill when
usually only few lines are need to be added.
Inaddition this creates mismatch when using function like convert_to_dataframe) and 
merge_data_feeds(df1, df2).
'''
def store(data, filepath):
    if os.path.exists(filepath) and os.path.isfile(filepath):
        temp_filepath = filepath + '.premerged'
        write_to_file(data, temp_filepath)
        try:
            merged = merge_data_feeds_csv(filepath, temp_filepath)
            pd.DataFrame.to_csv(merged, filepath)
            # to append csv use binary file: dataframe.to_csv(io.open(filepath+'1', 'ab'), headers=False)
        except FeedMergeException as exp:
            logerror(f'Storing data feed {data._name} failed, path={filepath}. Reason: {exp}')
            return
        os.remove(temp_filepath) 

    else:
        write_to_file(data, filepath)

'''
def store_2(data, filepath):
        data_as_df = feed_to_dataframe(data)
        file_as_df = file_to_dataframe(filepath)
        merged, new_line = merge_data_feeds(data_as_df, file_as_df)
        append(filepath, merged[:new_line])
'''
    
        
def write_to_file(data, filepath):
    with io.open(filepath, 'w') as file:
        write_header(data, file)
        write_values(data, file)
        file.close()
    
def write_header(data, file):
    file.write(reduce(lambda a,b: a + ',' + b, data.getwriterheaders()[2:]) + '\n')

def write_values(data, file):
    data.home()
    while len(data) < data.buflen():
        data.next()
        line = data.getwritervalues()
        file.write(str(line[2].date()) + ',' + str(line[3:])[1:-1].replace('\'', '').replace(' ','') + '\n')
