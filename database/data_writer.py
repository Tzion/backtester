import backtrader as bt

import database
from logger import *
from backtrader.feeds import IBData
import io

class DataWriter():
    
    @staticmethod
    def decorate_writing(live_data : bt.feed.AbstractDataBase, static_data, at_the_end=True):
        ''' Adds the data object the ability to save itself to a file.
            This happens as part of the lifecycle of the object by decorating its inner methods '''
        if at_the_end:
            export_file = io.open(static_data._dataname + '.unmerged', 'w')
            live_data.stop = DataWriter._store_and_stop_decorator(live_data.stop, live_data, export_file) 
        else:
             # TODO
            live_data.load = DataWriter._load_and_store_decorator(live_data.load, live_data)
            live_data.file = io.open('test_file.csv', mode='a+')
            live_data.stop = DataWriter._stop_and_close_file_decorator(live_data.stop, live_data.file)
        return live_data


    @staticmethod
    def _store_and_stop_decorator(stop_func, data, export_file):
        def store_and_stop():
            store(data, export_file)
            stop_func()
        return store_and_stop
        
    @staticmethod
    def _load_and_store_decorator(load_func, data):
        def load_and_store():
            loaded = load_func()
            if loaded:
                write_latest_line(data, data.file)
            return loaded
        return load_and_store
            
    @staticmethod
    def _stop_and_close_file_decorator(stop_func, file):
        def stop_and_close():
            file.close()
            stop_func()
        return stop_and_close


def store(data, file):
    file.write(str(data.getwriterheaders()))
    file.write(str(data.buflen()))
    file.close()


def write_latest_line(data, file):
    loginfo('storing line')
    line = data.getwritervalues()
    csv_line = str(line)[1:-1] + '\n'
    file.write(csv_line)
        