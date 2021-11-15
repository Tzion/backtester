from globals import *
import datetime
from backtrader.stores import ibstore as store
from samples.ibtest.ibtest import TestStrategy

        
def live_signals():
    cerebro = bt.Cerebro(stdstats=False)
    store = bt.stores.IBStore(host='127.0.0.1', port=7497, clientId=1488)
    cerebro.broker = store.getbroker()
    # also: 'TQQQ-STK-ISLAND-USD'
    data = store.getdata(dataname='AAPL-STK-SMART-USD', timeframe=bt.TimeFrame.Days)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Days, compression=1)

    
    cerebro.addstrategy(St)
    strats = cerebro.run()
    print(f'data len: {len(strats[0].data)}')
    print('')
    # ibstore = store.IBStore(host='127.0.0.1', port=7496, clientId=1896292)
    # data = ibstore.getdata(dataname='EUR.USD-CASH-IDEALPRO')

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
    fromdate=datetime.datetime(2021, 11, 4),  # get data from..
    todate=datetime.datetime(2021, 11, 11),  # get data from..
    latethrough=False,  # let late samples through
    tradename=None  # use a different asset as order target
)

def run(args=None):
    cerebro = bt.Cerebro(stdstats=False)
    global store
    store = bt.stores.IBStore(port=7497, notifyall=False, _debug=True)
    cerebro.addstrategy(TestStrategy)
    # quote('BAX', 'CDE', 'CAD', 'FUT') # got result (contract) but no len
    # quote('TSX', 'CDE', 'CAD', 'FUT') # got result (contract) but no len
    data = store.getdata(dataname='AAPL-STK-SMART-USD', **stockkwargs)
    cerebro.replaydata(data, timeframe=bt.TimeFrame.Days)
    # cerebro.resampledata(data, timeframe=bt.TimeFrame.Days, compression=1)
    # data.start()
    store.start()
    cerebro.run()

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
    run()