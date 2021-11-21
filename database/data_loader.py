from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import os
import sys
import numpy as np
from logger import *
import globals as gb
from globals import *

class DataLoader(ABC):

    def __init__(self, cerebro):
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


class LiveLoader(DataLoader):

    config = dict(
        timeframe=bt.TimeFrame.Days,
        historical=True,  # only historical download
        fromdate= datetime(2019, 4, 10),  # get data from..
        todate= datetime(2019, 4, 30),  # get data from..
    )
    
    def load_feeds(self, symbols=[], start_date=None, end_date=datetime.today()):
        start_date = start_date or end_date - timedelta(days=100)
        store = bt.stores.ibstore.IBStore(port=7497, _debug=True)
        ib_symbols = [symbol +'-STK-SMART-USD' for symbol in symbols]
        for symbol in ib_symbols:
            data = store.getdata(dataname=symbol, **LiveLoader.config)
            self.cerebro.adddata(data)


        

        pass

    '''
    load_data
        load_from_file
        backfill_from_ib
            validate
            write_to_file ?
    run backtest
    stay_alive- wait for data
    '''