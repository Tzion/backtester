import backtrader as bt

import database
from logger import *
from backtrader.feeds import IBData
import io
from functools import reduce

class DataWriter():
    
    @staticmethod
    def decorate_writing(live_data : bt.feed.AbstractDataBase, static_data):
        ''' Adds the data object the ability to save itself to a file.
            This happens as part of the lifecycle of the object by decorating its inner methods '''
        export_file = io.open(static_data._dataname + '.unmerged', 'w')
        live_data.stop = DataWriter._store_and_stop_decorator(live_data.stop, live_data, export_file) 
        return live_data

    @staticmethod
    def _store_and_stop_decorator(stop_func, data, export_file):
        def store_and_stop():
            store(data, export_file)
            stop_func()
        return store_and_stop
        
def store(data, file):
    file.write(reduce(lambda a,b: a + ',' + b, data.getwriterheaders()[2:]) + '\n')
    write_values(data, file)
    file.close()

def write_values(data, file):
    data.home()
    while len(data) < data.buflen():
        data.next()
        line = data.getwritervalues()
        file.write(str(line[2].date()) + ',' + str(line[3:])[1:-1].replace('\'', '').replace(' ','') + '\n')
