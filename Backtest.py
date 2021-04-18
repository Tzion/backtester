import backtrader as bt
import datetime
import os.path
import sys
from Strategies.DojiStrategyLong import DojiLongStrategy
from Analyzers.BasicSradeStats import BasicTradeStats
import backtrader.analyzers as btanalyzers
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
    stocks = os.listdir(dirpath)
    print('adding {} data feeds'.format(len(stocks)))
    for i, stock in enumerate(stocks):
        if i >= 2 : continue
        feed = bt.feeds.GenericCSVData(
            dataname=os.path.join(dirpath, stock), fromdate=datetime.datetime(2015, 4, 4),
            todate=datetime.datetime(2020, 3, 10), dtformat='%Y-%m-%d',
            high=1, low=2, open=3, close=4)
        feed.plotinfo.plotmaster = None
        feed.plotinfo.plot = False
        cerebro.adddata(feed, stock)

    # Add analyzer
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
    cerebro.addanalyzer(BasicTradeStats, _name='basic_trade_stats')

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    print('backtesting strategy')
    strats = cerebro.run()
    print('ploting')
    for i,feed in enumerate(cerebro.datas):
        if i>1: continue
        feed.plotinfo.plotmaster = feed
        feed.plotinfo.plot = True
        # cerebro.plot(style='candlestick', barup='green', numfigs=1)
        feed.plotinfo.plot = False
        feed.plotinfo.plotmaster = None

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    for each in strats[0].analyzers:
        each.print()