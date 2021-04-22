import backtrader as bt
import datetime
import os.path
import sys
from Strategies.DojiStrategyLong import DojiLongStrategy
from Analyzers.BasicSradeStats import BasicTradeStats
import backtrader.analyzers as btanalyzers
import matplotlib.pylab as pylab


cerebro = bt.Cerebro()

def main():
    add_strategies()
    add_data()
    add_analyzer()
    global strategies
    strategies = backtest()
    plot()
    show_statistics(strategies)


def add_strategies():
    cerebro.addstrategy(DojiLongStrategy)


def add_data(limit=-1):
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    dirpath = os.path.join(modpath, 'data_feeds')
    stocks = os.listdir(dirpath)
    print('adding {} data feeds'.format(len(stocks)))
    for i, stock in enumerate(stocks):
        feed = bt.feeds.GenericCSVData(
            dataname=os.path.join(dirpath, stock), fromdate=datetime.datetime(2015, 4, 4),
            todate=datetime.datetime(2020, 3, 10), dtformat='%Y-%m-%d',
            high=1, low=2, open=3, close=4)
        feed.plotinfo.plotmaster = None
        feed.plotinfo.plot = False
        cerebro.adddata(feed, name=stock.strip('.csv'))


def add_analyzer():
    cerebro.addanalyzer(BasicTradeStats, _name='basic_trade_stats')


def backtest():
    cerebro.broker.setcash(10000.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('backtesting strategy')
    strategies = cerebro.run()
    return strategies


def plot():
    pylab.rcParams['figure.figsize'] = 26, 14 # that's default image size for this interactive session
    trades = strategies[0]._trades
    top_feeds = list(dict(sorted(trades.items(), key=lambda item : len(item[1][0]))))
    print('ploting')
    for i, feed in enumerate(top_feeds):
        if i >= 1:
            continue
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
