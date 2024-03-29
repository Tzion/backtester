from abc import ABC, abstractmethod
import backtrader as bt
from datetime import datetime, timedelta, time
import os
import sys
import numpy as np
from database.data_source import DataSource, IBDataSource
from logger import *
from database.data_writer import DataWriter
from backtrader.feeds import GenericCSVData

class DataLoader(ABC):

    def __init__(self, cerebro:bt.Cerebro):
        self.cerebro = cerebro
    
    @abstractmethod
    def load_feeds(self, **kwargs):
        pass


class StaticLoader(DataLoader):
    # TODO rename to yahooLoader
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
            feed = GenericCSVData(
                dataname=os.path.join(dirpath, stock2file(stock)), fromdate=start_date,
                todate=end_date, dtformat=dtformat,
                high=high_idx, low=low_idx, open=open_idx, close=close_idx, volume=volume_idx, plot=False)
            self.cerebro.adddata(feed, name=stock.strip('.csv'))


class IBLoader(DataLoader):

    source : DataSource = IBDataSource()

    end_of_day = time(23,00)
    config = dict(
        timeframe=bt.TimeFrame.Days,
        historical=True,  # only historical download
        what = 'TRADES',
        useRTH = True,  # request data of Regular Trading Hours,
        sessionend = end_of_day  # the default sessionend suffers from precission error which may cause shift to next day - this is workaround to that bug, until pr approved in the infra
    )

    def __init__(self, cerebro:bt.Cerebro):
        super().__init__(cerebro)
        self.data_store = bt.stores.ibstore.IBStore(port=7497, _debug=True, notifyall=True)
        
    def load_feeds(self, symbols=[], start_date=None, end_date=datetime.today(), backfill_from_database=True, store=False):
        start_date = start_date or end_date - timedelta(days=100)
        for symbol in symbols:
            backfill_data = None
            if backfill_from_database:
                backfill_data = GenericCSVData(dataname=IBLoader.source.get_feed_path(symbol), fromdate=start_date, todate=end_date, dtformat='%Y-%m-%d', tz='US/Eastern', sessionend=IBLoader.end_of_day)
            data = self.data_store.getdata(dataname=IBLoader.source.get_feed_fullname(symbol), **IBLoader.config, fromdate=start_date, todate=end_date, backfill_from=backfill_data)
            if store:
                data = DataWriter.decorate_writing(data, IBLoader.source.get_feed_path(symbol))
            self.cerebro.adddata(data, symbol)
    
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