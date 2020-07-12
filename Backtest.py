import backtrader as bt
import datetime
import os.path
import sys
from Strategies.DojiStrategyLong import DojiLongStrategy
import matplotlib.pylab as pylab
pylab.rcParams['figure.figsize'] = 30, 20  # that's default image size for this interactive session
if __name__ == '__main__':
    cerebro = bt.Cerebro()

    toplot=0
    plotmaster = None
    # Add a strategy
    cerebro.addstrategy(DojiLongStrategy)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    dirpath = os.path.join(modpath, 'data_feeds')
    files = os.listdir(dirpath)
    print('adding {} data feeds'.format(len(files)))
    for data in files:
        feed = bt.feeds.GenericCSVData(
            dataname=os.path.join(dirpath,data), fromdate=datetime.datetime(2015, 4, 4),
            todate=datetime.datetime(2020, 3, 10), dtformat='%Y-%m-%d',
            high=1, low=2, open=3, close=4)
        cerebro.adddata(feed)
        if plotmaster is None:
            plotmaster = feed
        else:
            feed.plotinfo.plotmaster = plotmaster
        if toplot>=3:
            feed.plotinfo.plot = False
        toplot+=1

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    print('backtesting strategy')
    cerebro.run()
    print('ploting')
    cerebro.plot(style='candlestick', barup='green')

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
