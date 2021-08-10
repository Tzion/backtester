from strategies.candle_pattern_long import CandlePatternLong
from strategies.classic_breakout import ClassicBreakout
from strategies.highs_lows_stracture import HighLowsStructureImproved, HighestHighsBreakoutStrategy, HighsLowsStructure
from test.trade_state_strategy_test import TradePhaseStrategyTest
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
import numpy as np
from logger import *


def main():
    global cerebro
    cerebro = gb.cerebro
    add_strategies(CandlePatternLong)
    # add_data(random=True, start_date=datetime(2016,11,30), end_date=datetime(2021, 4, 26), limit=0, dirpath='data_feeds')
    add_data(random=False, start_date=datetime(2016,11,30), end_date=datetime(2021, 4, 26), stock_names=['PG.csv'], dirpath='data_feeds')
    # add_strategies(Top3)
    # add_data(start_date=datetime(2020, 12, 3), end_date=datetime(2021, 6, 28), limit=0,
            #  dtformat='%Y-%m-%dT%H:%M:%SZ', stock_names=retrieve_stocks(), dirpath='iknowfirst/ikf_feeds', high_idx=2, low_idx=3, open_idx=1, close_idx=4, volume_idx=7, stock2file = lambda s: 'TASE_DLY_' + s.replace('.TA', '') + ', 1D.csv')
    add_analyzer()
    global strategies
    strategies = backtest()
    show_statistics(strategies)
    plot(strategies[0], limit=5, only_trades=True, plot_observers=True, interactive_plots=True)


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
        
def add_analyzer():
    cerebro.addanalyzer(BasicTradeStats, _name='basic_trade_stats')


def backtest():
    cerebro.broker.setcash(10000.0)
    loginfo(f'Strating portfolio value: {cerebro.broker.getvalue():.2f}')
    strategies = cerebro.run()
    return strategies


def plot(strategy: bt.Strategy, *args, **kwargs):
    strategy.plot(*args, **kwargs)


def show_statistics(strategies):
    loginfo(f'Final portfolio value: {cerebro.broker.getvalue():.2f}')
    for each in strategies[0].analyzers:
        each.print() # TODO use logger

if __name__ == '__main__':
    main()
