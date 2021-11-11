from globals import *
from backtrader.stores import ibstore as store

class St(bt.Strategy):
    def next(self):
        print('hello interative brokers!!!')
        
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

    

if __name__ == '__main__':
    live_signals()