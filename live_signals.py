import globals as gb
from globals import *
import datetime
from backtrader.stores import ibstore as store
from samples.ibtest.ibtest import TestStrategy

        
class St(bt.Strategy):
    def start(self):
        print('strategy is running')

    def logdata(self):
        txt = []
        txt.append('{}'.format(len(self)))
           
        txt.append('{}'.format(
            self.data.datetime.datetime(0).isoformat())
        )
        txt.append('{:.2f}'.format(self.data.open[0]))
        txt.append('{:.2f}'.format(self.data.high[0]))
        txt.append('{:.2f}'.format(self.data.low[0]))
        txt.append('{:.2f}'.format(self.data.close[0]))
        txt.append('{:.2f}'.format(self.data.volume[0]))
        print(','.join(txt))

    def next(self):
        self.logdata()

    def notify_data(self, data, status, *args, **kwargs):
        print(f'new data recieved: {data} {status}')
        
stockkwargs = dict(
    timeframe=bt.TimeFrame.Days,
    rtbar=False,  # use RealTime 5 seconds bars
    historical=True,  # only historical download
    qcheck=0.5,  # timeout in seconds (float) to check for events
    fromdate=datetime.datetime(2019, 4, 20),  # get data from..
    todate=datetime.datetime(2019, 4, 30),  # get data from..
    latethrough=False,  # let late samples through
    tradename=None  # use a different asset as order target
)

def backtest():
    global cerebro
    cerebro = gb.cerebro
    cerebro.addstrategy(TestStrategy)
    from backtest import add_data
    add_data(limit=0, random=False, start_date=datetime(2016,11,30), end_date=datetime(2021, 4, 26), dirpath='data_feeds', stock_names=['ABC.csv'])
    backfill(cerebro.datas)
    global strategies
    strategies = backtest()
    merge_data(cerebro.datas)
    pass
    

def backfill(datas):
    global cerebro
    store = bt.stores.IBStore(port=7497, notifyall=False, _debug=True)
    for data in datas:
        from_date = find_end_date(data)
        live_data = store.getdata(dataname=data._name+'-STK-SMART-USD', fromdate=from_date, todate=datetime.datetime.today(), historical=True, timeframe=bt.TimeFrame.Days)
        cerebro.adddata(live_data)

def merge_data(datas):
    for data in datas:
        data.roll
        pass

def run(args=None):
    cerebro = bt.Cerebro(stdstats=False)
    global store
    store = bt.stores.IBStore(port=7497, notifyall=False, _debug=True)
    cerebro.addstrategy(TestStrategy)
    # quote('BAX', 'CDE', 'CAD', 'FUT') # got result (contract) but no len
    # quote('TSX', 'CDE', 'CAD', 'FUT') # got result (contract) but no len

    disk_data = bt.feeds.GenericCSVData(dataname='data_feeds/NVDA.csv', fromdate=datetime.datetime(2019, 4, 20), todate=datetime.datetime(2019,4,26), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)
    data = store.getdata(dataname='NVDA-STK-SMART-USD', **stockkwargs, backfill_from=disk_data,)
    # cerebro.replaydata(data, timeframe=bt.TimeFrame.Days)
    cerebro.adddata(data, name='A')
    # cerebro.adddata(disk_data, name='A')
    # cerebro.resampledata(data, timeframe=bt.TimeFrame.Days, compression=1)
    # store.start()
    cerebro.run()
    print(len(cerebro.datas[0]))
    # print(len(cerebro.datas[1]))
    print(len(cerebro.datas))
    pass

def run_no_backfill():
    cerebro = bt.Cerebro(stdstats=False)
    istore = bt.stores.IBStore(port=7497, notifyall=False, _debug=True)
    exchanges =['SMART','AMEX','NYSE','CBOE','PHLX','ISE','CHX','ARCA','ISLAND','DRCTEDGE',
                'BEX','BATS','EDGEA','CSFBALGO','JEFFALGO','BYX','IEX','EDGX','FOXRIVER','PEARL','NYSENAT','LTSE','MEMX','PSX']
    for exc in exchanges:
        data = istore.getdata(dataname=f'ZION-STK-{exc}-USD', fromdate=datetime.datetime(2021,11,16), todate=datetime.datetime(2021,11,23), historical=True)
        cerebro.adddata(data)
    cerebro.addstrategy(TestStrategy)
    strat = cerebro.run()[0]
    pass
    
    
# %%


def quote(symbol, exchange, currency='USD', type='STK'):
    if cerebro.datas:
        cerebro.datas=[]
    query = f'{symbol}-{type}-{exchange}-{currency}'
    print ('queying '+query)
    data = store.getdata(dataname=query, **stockkwargs)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Days, compression=1)
    cerebro.adddata(data)
    cerebro.run()
    return cerebro.datas[0]

if __name__ == '__main__':
    run_no_backfill()