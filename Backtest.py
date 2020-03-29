import backtrader as bt
import datetime
import os.path
import sys
from Strategies.DojiStrategyLong import DojiLongStrategy
import matplotlib.pylab as pylab
pylab.rcParams['figure.figsize'] = 30, 20  # that's default image size for this interactive session
if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(DojiLongStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    
    datapath = os.path.join(modpath, 'data_feeds/AAPL.csv')
    data = bt.feeds.GenericCSVData(
        dataname=datapath, fromdate=datetime.datetime(2015, 4, 4),
        todate=datetime.datetime(2020, 3, 10), dtformat='%Y-%m-%d',
        high=1, low=2, open=3, close=4)
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()
    cerebro.plot(style='candlestick', barup='green')

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
