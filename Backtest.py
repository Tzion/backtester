from Strategies.IkfStrategy import IkfStrategy
import backtrader as bt
import datetime
import os.path
import sys
from Strategies.DojiStrategyLong import DojiLongStrategy
from Analyzers.BasicSradeStats import BasicTradeStats
import backtrader.analyzers as btanalyzers
import matplotlib.pylab as pylab
from iknowfirst.iknowfirst import retrieve_forecasts_data, retrieve_stocks


cerebro = bt.Cerebro()

FILENAME_FORMAT = lambda s: 'TASE_DLY_' + s.replace('.TA', '') + ', 1D.csv'

def main():
    add_strategies()
    add_data(limit=1, stocks=retrieve_stocks(), dirpath='ikf_stocks')
    # add_analyzer()
    global strategies
    strategies = backtest()
    # show_statistics(strategies)
    plot(1, only_trades=False)


def add_strategies():
    cerebro.addstrategy(IkfStrategy, forecasts=retrieve_forecasts_data())


def add_data(limit=0, stocks=None, dirpath='data_feeds'):
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    dirpath = os.path.join(modpath, dirpath)
    stocks = stocks or os.listdir(dirpath)
    # stocks=list(filter(lambda x:x=='BEZQ.TA', stocks)) ## todo for debugging
    stocks = stocks[:limit or len(stocks)]
    print('adding {} data feeds'.format((stocks)))
    for i, stock in enumerate(stocks):
        feed = bt.feeds.GenericCSVData(
            dataname=os.path.join(dirpath, FILENAME_FORMAT(stock)), fromdate=datetime.datetime(2020, 12, 10),
            todate=datetime.datetime(2021, 4, 27), dtformat='%Y-%m-%dT%H:%M:%SZ',
            high=2, low=3, open=1, close=4, volume=7)
        feed.plotinfo.plotmaster = None
        feed.plotinfo.plot = False
        cerebro.adddata(feed, name=stock)


def add_analyzer():
    cerebro.addanalyzer(BasicTradeStats, _name='basic_trade_stats')


def backtest():
    cerebro.broker.setcash(10000.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('backtesting strategy')
    strategies = cerebro.run()
    return strategies


def plot(max=1, only_trades=True):
    pylab.rcParams['figure.figsize'] = 26, 13 # that's default image size for this interactive session
    feeds = list(dict(sorted(strategies[0]._trades.items(), key=lambda item: len(
        item[1][0])))) if only_trades else cerebro.datas
    print('ploting top %d feeds' % max)
    for i, feed in enumerate(feeds):
        if i >= max:
            break
        feed.plotinfo.plotmaster = feed
        feed.plotinfo.plot = True
        cerebro.plot(style='candlestick', barup='green', numfigs=1)
        feed.plotinfo.plot = False
        feed.plotinfo.plotmaster = None


def show_statistics(strategies):
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    for each in strategies[0].analyzers:
        each.print()

if __name__ == '__main__':
    main()
