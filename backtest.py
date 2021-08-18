from analyzers.exposer import Exposer
from strategies.candle_pattern_long import CandlePatternLong
import backtrader as bt
from datetime import datetime
import os.path
import sys
from analyzers.basic_trade_stats import BasicTradeStats
from backtrader.analyzers.tradeanalyzer import TradeAnalyzer
import globals as gb
import strategies
import numpy as np
from logger import *


def main():
    global cerebro
    cerebro = gb.cerebro
    add_strategies(CandlePatternLong)
    add_data(random=False, start_date=datetime(2016,11,30), end_date=datetime(2021, 4, 26), dirpath='data_feeds')
    # add_data(random=False, start_date=datetime(2018,3,24), end_date=datetime(2019, 2, 22), stock_names=['WHR.csv', 'UDR.csv', 'CNP.csv', 'NKE.csv', 'NVDA.csv', 'GPN.csv', 'OKE.csv', 'CB.csv', 'ADSK.csv', 'MRO.csv', 'GD.csv', 'JPM.csv', 'ORLY.csv', 'IFF.csv'], dirpath='data_feeds')
    # add_data(random=False, start_date=datetime(2017,11,30), end_date=datetime(2019, 6, 26), limit=120, stock_names=['GNRC.csv'], dirpath='data_feeds')
    # add_data(random=False, start_date=datetime(2016,11,30), end_date=datetime(2021, 4, 26), limit=120, dirpath='data_feeds')
    add_analyzers()
    global strategies
    strategies = backtest()
    show_statistics(strategies)
    # plot(strategies[0], limit=1, only_trades=True, plot_observers=True, interactive_plots=True)


def add_strategies(strategy: bt.Strategy):
    loginfo(f'backtesting strategy {type(strategy).__name__}')
    cerebro.addstrategy(strategy)


def add_data(start_date: datetime, end_date: datetime, limit=0, dtformat='%Y-%m-%d', dirpath='data_feeds', stock_names=None, high_idx=1, low_idx=2, open_idx=3, close_idx=4, volume_idx=5, stock2file= lambda s:s, random=False):
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    dirpath = os.path.join(modpath, dirpath)
    stocks = stock_names or os.listdir(dirpath)
    if random:
        stocks = np.random.permutation(stocks)
    stocks = stocks[:limit or len(stocks)]
    loginfo(f'adding {len(stocks)} data feeds')
    for i, stock in enumerate(stocks):
        feed = bt.feeds.GenericCSVData(
            dataname=os.path.join(dirpath, stock2file(stock)), fromdate=start_date,
            todate=end_date, dtformat=dtformat,
            high=high_idx, low=low_idx, open=open_idx, close=close_idx, volume=volume_idx, plot=False)
        cerebro.adddata(feed, name=stock.strip('.csv'))
        
def add_analyzers():
    cerebro.addanalyzer(BasicTradeStats, _name='basic_trade_stats', useStandardPrint=False)
    cerebro.addanalyzer(TradeAnalyzer)
    cerebro.addanalyzer(Exposer)


def backtest():
    cerebro.broker.setcash(10000.0)
    cerebro.broker.set_shortcash(False)
    loginfo(f'Strating portfolio value: {cerebro.broker.getvalue():.2f}')
    strategies = cerebro.run()
    return strategies


def plot(strategy: bt.Strategy, *args, **kwargs):
    strategy.plot(*args, **kwargs)


def show_statistics(strategies):
    loginfo(f'Final portfolio value: {cerebro.broker.getvalue():.2f}')
    strategies[0].analyzers.basic_trade_stats.print()
    strategies[0].analyzers.exposer.print()
    print_trades_length()

def print_trades_length(): # TODO add the required statistics (len, exposer) to the custom analyzer and remove this
    trades_len = strategies[0].analyzers.tradeanalyzer.get_analysis()['len']
    print(f'Trades length: Total: {trades_len.total}, Average: {trades_len.average}, Max: {trades_len.max}, Min: {trades_len.min}. Total bars: {len(strategies[0].data)}')

if __name__ == '__main__':
    main()
