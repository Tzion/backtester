import backtrader as bt

import database
from logger import *
from backtrader.feeds import IBData
import io

class DataWriter():
    
    @staticmethod
    def add_writer(data : bt.feed.AbstractDataBase, at_the_end=False):
        ''' Adds the data object the ability to save itself to a file.
            This happens as part of the lifecycle of the object by decorating its inner methods '''
        if at_the_end:
            data.stop = DataWriter._store_and_stop_decorator(data.stop, data) 
        else:
            data.load = DataWriter._load_and_store_decorator(data.load, data)
            data.file = io.open('test_file.csv', mode='a+')
            data.stop = DataWriter._stop_and_close_file_decorator(data.stop, data.file)
        return data


    @staticmethod
    def _store_and_stop_decorator(stop_func, data):
        def store_and_stop():
            store(data)
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


def store(data):
    print('storing the data to file')
    pass

def write_latest_line(data, file):
    loginfo('storing line')
    line = data.getwritervalues()
    csv_line = str(line)[1:-1] + '\n'
    file.write(csv_line)
        