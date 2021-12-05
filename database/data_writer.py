import backtrader as bt

import database
from backtrader.feeds import IBData

class DataWriter():
    
    @staticmethod
    def add_writer(data : bt.feed.AbstractDataBase):
        ''' Adds the data object the ability to save itself to a file.
            This happens as part of the lifecycle of the object by decorating its inner methods '''
        data.stop = DataWriter._store_and_stop_decorator(data.stop, data) 
        return data


    @staticmethod
    def _store_and_stop_decorator(stop_func, data):
        def store_and_stop():
            DataWriter._store(data)
            stop_func()
        return store_and_stop
        

    @staticmethod
    def _store(data):
        print('storing the data to file')
        pass
    
    
    
class DataWriterDecorator(IBData):
    
    def __init__(self, wrappee):
        self.ib = wrappee.ib

    def __getattribute__(self, __name: str):
        return getattr(self.wrappee, __name)

    def stop(self):
       print('Store data to disk') 
       self.wrappee.stop()