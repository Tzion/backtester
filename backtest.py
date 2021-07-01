from iknowfirst.ikf_strategies import EndOfMonthEntry, OneTimeframeForecast, Top3, TwoTimeframesForecast, Sma5And30DaysForecasts
from strategies import rsi_strategy, doji_long_strategy
from iknowfirst.iknowfirst import retrieve_stocks
import backtrader as bt
from datetime import datetime
import os.path
import sys
from analyzers.basic_trade_stats import BasicTradeStats
import backtrader.analyzers as btanalyzers
import matplotlib.pylab as pylab
from backtrader_plotting import Bokeh
import globals as gb
import strategies



def main():
    global cerebro
    cerebro = gb.cerebro
    add_strategies(rsi_strategy.RsiAndMovingAverageStrategy)
    add_data(start_date=datetime(2018,4,4), end_date=datetime(2020, 3, 11), limit=59, dirpath='data_feeds')
    # add_strategies(Top3)
    # add_data(start_date=datetime(2020, 12, 3), end_date=datetime(2021, 6, 28), limit=0,
            #  dtformat='%Y-%m-%dT%H:%M:%SZ', stock_names=retrieve_stocks(), dirpath='iknowfirst/ikf_feeds', high_idx=2, low_idx=3, open_idx=1, close_idx=4, volume_idx=7, stock2file = lambda s: 'TASE_DLY_' + s.replace('.TA', '') + ', 1D.csv')
    add_analyzer()
    global strategies
    strategies = backtest()
    show_statistics(strategies)
    # plot(strategies[0], limit=2, only_trades=True, plot_observers=True, interactive_plots=True)


def add_strategies(strategy: bt.Strategy):
    cerebro.addstrategy(strategy)


def add_data(start_date: datetime, end_date: datetime, limit=0, dtformat='%Y-%m-%d', dirpath='data_feeds', stock_names=None, high_idx=1, low_idx=2, open_idx=3, close_idx=4, volume_idx=5, stock2file= lambda s:s):
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    dirpath = os.path.join(modpath, dirpath)
    stocks = stock_names or os.listdir(dirpath)
    stocks = stocks[:limit or len(stocks)]
    print('adding {} data feeds'.format(len(stocks)))
    for i, stock in enumerate(stocks):
        feed = bt.feeds.GenericCSVData(
            dataname=os.path.join(dirpath, stock2file(stock)), fromdate=start_date,
            todate=end_date, dtformat=dtformat,
            high=high_idx, low=low_idx, open=open_idx, close=close_idx, volume=volume_idx, plot=False)
        cerebro.adddata(feed, name=stock.strip('.csv'))
        
def add_analyzer():
    cerebro.addanalyzer(BasicTradeStats, _name='basic_trade_stats')


def backtest():
    cerebro.broker.setcash(1000000.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('backtesting strategy')
    strategies = cerebro.run()
    return strategies


def plot(strategy: bt.Strategy, *args, **kwargs):
    strategy.plot(*args, **kwargs)


def show_statistics(strategies):
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    for each in strategies[0].analyzers:
        each.print()

if __name__ == '__main__':
    main()
