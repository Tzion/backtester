from backtrader.dataseries import TimeFrame
from utils.backtrader_helpers import extract_all_trades, print_trades_length
from utils.charting import pnl_to_trade_length
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
from globals import OUTPUT_DIR
from charts.plotter import PlotlyPlotter
import os


def main():
    clean_previous_output()
    global cerebro
    cerebro = gb.cerebro
    add_strategies(CandlePatternLong)
    # add_data(limit=12, random=True, start_date=datetime(2016,11,30), end_date=datetime(2021, 4, 26), dirpath='data_feeds')
    add_data(random=True, start_date=datetime(2016,11,30), end_date=datetime(2019, 6, 26), limit=3, stock_names=['DFS.csv', 'GD.csv','ABC.csv'], dirpath='data_feeds')
    # add_data(random=True, start_date=datetime(2016,11,30), end_date=datetime(2019, 6, 26), limit=90, dirpath='data_feeds')
    # add_data(random=False, start_date=datetime(2016,11,30), end_date=datetime(2021, 4, 26), limit=120, dirpath='data_feeds')
    add_analyzers()
    add_observers()
    global strategies
    strategies = backtest()
    show_statistics(strategies)
    # cerebro.plot(plotter=PlotlyPlotter())
    # plot(strategies[0], limit=1, only_trades=True, plot_observers=True, interactive_plots=False)


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
    logdebug(f'adding {len(stocks)} data feeds: {stocks}')
    for i, stock in enumerate(stocks):
        feed = bt.feeds.GenericCSVData(
            dataname=os.path.join(dirpath, stock2file(stock)), fromdate=start_date,
            todate=end_date, dtformat=dtformat,
            high=high_idx, low=low_idx, open=open_idx, close=close_idx, volume=volume_idx, plot=False)
        gb.cerebro.adddata(feed, name=stock.strip('.csv'))
        
def add_analyzers():
    cerebro.addanalyzer(BasicTradeStats, _name='basic_trade_stats', useStandardPrint=False)
    cerebro.addanalyzer(TradeAnalyzer)
    cerebro.addanalyzer(Exposer)
    cerebro.addanalyzer(bt.analyzers.DrawDown)
    cerebro.addanalyzer(bt.analyzers.SQN)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio_A)

def add_observers():
    cerebro.addobserver(bt.observers.DrawDown)
    cerebro.addobserver(bt.observers.LogReturns, timeframe=TimeFrame.Months, compression=0)


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
    print_trades_length(strategies[0].analyzers.tradeanalyzer)
    strategies[0].analyzers.tradeanalyzer.print()
    strategies[0].analyzers.exposer.print()
    strategies[0].analyzers.drawdown.print()
    strategies[0].analyzers.sqn.print()
    strategies[0].analyzers.sharperatio.print()
    strategies[0].analyzers.sharperatio_a.print()
    pnl_to_trade_length(extract_all_trades(strategies[0]))


# TODO move to utils, mark as dangerous
def clean_previous_output():
    files_to_delete = ["html",]
    def clean_dir(path):
        for blob in [os.path.join(path,f) for f in os.listdir(path)]:
            if os.path.isdir(blob):
                clean_dir(blob)
            else:
                if blob.split('.')[-1] in files_to_delete:
                    os.remove(os.path.abspath(blob))

    if os.path.abspath(OUTPUT_DIR).endswith('backtester/output'):  ## hardcoded validation
        clean_dir(OUTPUT_DIR)
        


if __name__ == '__main__':
    main()


