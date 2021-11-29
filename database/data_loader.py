from abc import ABC, abstractmethod
import backtrader as bt
from datetime import datetime, timedelta
import os
import sys
import numpy as np
from logger import *
import globals as gb
from database import get_feed_file_path

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
    
    def load_feeds(self, symbols=[], start_date=None, end_date=datetime.today(), backfill_from_database=True):
        start_date = start_date or end_date - timedelta(days=100)
        store = bt.stores.ibstore.IBStore(port=7497, _debug=True, notifyall=True) # make it singleton
        for symbol in symbols:
            if backfill_from_database:
                file_data = bt.feeds.GenericCSVData(dataname=get_feed_file_path(symbol), fromdate=start_date, todate=end_date, dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)
                #TODO check ib or backtrader.ib interface for the stock ame manipulation or implement on my side
                data = store.getdata(dataname=symbol+'-STK-SMART-USD', **HistoricalLoader.config, fromdate=start_date, todate=end_date, backfill_from=file_data)
                # self.cerebro.adddata(file_data,)# symbol)
            else:
                data = store.getdata(dataname=symbol+'-STK-SMART-USD', **HistoricalLoader.config, fromdate=start_date, todate=end_date)
            self.cerebro.adddata(data, symbol)


    '''
    load_data
        load_from_file
        backfill_from_ib
            validate
            write_to_file ?
    run backtest
    stay_alive- wait for data
    '''


"""
# %%
import backtrader as bt
import datetime
from samples.ibtest.ibtest import TestStrategy

cerebro = bt.Cerebro(stdstats=False)
istore = bt.stores.IBStore(port=7497, notifyall=False, _debug=True)
exchanges =['SMART']
for exc in exchanges:
    data = istore.getdata(dataname=f'ZION-STK-{exc}-USD', fromdate=datetime.datetime(2021,11,16), todate=datetime.datetime(2021,11,23), historical=True)
    cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)
strat = cerebro.run()[0]


# PLAYING WITH BACKTRADER IB API
# %%

import backtrader as bt
from datetime import datetime

config = dict(
    timeframe=bt.TimeFrame.Days,
    historical=True,  # only historical download
    what = 'TRADES',
    useRTH = True,  # request data of Regular Trading Hours
)
store = bt.stores.ibstore.IBStore(port=7497, _debug=True, notifyall=True)
contract = store.makecontract('NVDA', 'STK', 'SMART', 'USD')
# store.reqHistoricalData(contract, enddate='2021-11-12', duration=, barsize=, useRTH=True)

    

    
# PLAYING DIRECTLY WITH IBAPI
# %%
import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

wrapper = EWrapper()
client = EClient(wrapper)
client.connect('127.0.0.1', 7497, 10)

 
# %%
contract = Contract()
contract.currency='USD'; contract.symbol='ZION'; contract.secType='STK'
client.reqContractDetails(0,contract)
# %%
wrapper
"""