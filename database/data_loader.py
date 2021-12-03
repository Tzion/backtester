from abc import ABC, abstractmethod
import backtrader as bt
from datetime import datetime, timedelta
import os
import sys
import numpy as np
from logger import *
import database

class DataLoader(ABC):

    def __init__(self, cerebro:bt.Cerebro):
        self.cerebro = cerebro
    
    @abstractmethod
    def load_feeds(self, **kwargs):
        pass


class StaticLoader(DataLoader):
    """Load data feeds from static files solely"""

    def load_feeds(self, start_date: datetime, end_date: datetime, limit=0, dtformat='%Y-%m-%d', dirpath='data_feeds', stock_names=None, high_idx=1, low_idx=2, open_idx=3, close_idx=4, volume_idx=5, stock2file= lambda s:s, random=False):
        modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        dirpath = os.path.join(modpath, dirpath)
        stocks = stock_names or os.listdir(dirpath)
        if random:
            stocks = np.random.permutation(stocks)
        stocks = stocks[:limit or len(stocks)]
        logdebug(f'adding {len(stocks)} data feeds: {stocks}')
        for i, stock in enumerate(stocks):
            feed = bt.feeds.GenericCSVData(
                dataname=os.path.join(dirpath, stock2file(stock)), fromdate=start_date,
                todate=end_date, dtformat=dtformat,
                high=high_idx, low=low_idx, open=open_idx, close=close_idx, volume=volume_idx, plot=False)
            self.cerebro.adddata(feed, name=stock.strip('.csv'))


class HistoricalLoader(DataLoader):

    config = dict(
        timeframe=bt.TimeFrame.Days,
        historical=True,  # only historical download
        what = 'TRADES',
        useRTH = True,  # request data of Regular Trading Hours
    )
    

    def load_feeds(self, symbols=[], start_date=None, end_date=datetime.today(), backfill_from_database=True, store=True):
        start_date = start_date or end_date - timedelta(days=100)
        store = bt.stores.ibstore.IBStore(port=7497, _debug=True, notifyall=True) # make it singleton
        for symbol in symbols:
            if backfill_from_database:
                file_data = bt.feeds.GenericCSVData(dataname=database.get_feed_file_path(symbol), fromdate=start_date, todate=end_date, dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)
                #TODO check ib or backtrader.ib interface for the stock ame manipulation or implement on my side
                data = store.getdata(dataname=symbol+'-STK-SMART-USD', **HistoricalLoader.config, fromdate=start_date, todate=end_date, backfill_from=file_data)
            else:
                data = store.getdata(dataname=symbol+'-STK-SMART-USD', **HistoricalLoader.config, fromdate=start_date, todate=end_date)
            
            if store:
                decorate_data_writter(data)
                # data.stop = stop_and_store_decorator(data.stop)
                # data.load = load_and_store.__get__(data, bt.feeds.ibdata.IBData)
                # data.stop = stop_and_store_decorator(data.stop)
                pass
            self.cerebro.adddata(data, symbol)
            # self.cerebro.addstorecb(notify_data_callback)
        if store:
            pass
            # data.load = load_and_store.__get__(data, bt.feeds.ibdata.IBData)
            self.cerebro.addwriter(bt.WriterFile, csv=True, out='./writer_test')


def decorate_data_writter(data):
    data.stop = stop_and_store_decorator(data.stop, data)
    # return data

def load_and_store(data):
    return bt.feeds.ibdata.IBData.load(data)
    
def stop_and_store_decorator(stop_func, data):
    def stop_and_store():
        d = data
        print('im storing')
        stop_func()
    return stop_and_store
    
# class Data():
#     def stop(self):
#         pass

# class DataDecorator():
#     def __init__(self, data):
#         self.data = data
    
#     def stop(self):
#         self.data.stop()

class DataWriterDecorator():
    
    def __init__(self, data):
        self.data = data

    def __get__(self, instance, owner):
            if instance is None:
                return self
            print (instance, owner)

    def stop(self):
        print('Im writing the data') 
        self.data.stop()

    '''
    load_data
    fetch
    store
    stay_alive- wait for data?

    fetch:
        fetch_from_cache (files)
        if cached file is not completed:
            fetch from server
    
    store:
        validate no conflicts with already stored file
        append the extra lines to the csv


    tests:
    1. no mismatches between data sources
    2. fetch from server data matches the stored
    '''

    '''
    live loader:
            prepare data query with backfill to cached file
        run strategy
            fetch from server with backfill from cache
            override load with my own store functionality


    '''