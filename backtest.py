from backtrader.dataseries import TimeFrame
from utils.backtrader_helpers import print_trades_length
from analyzers.exposer import Exposer
from strategies.candle_pattern_long import CandlePatternLong
import backtrader as bt
from datetime import datetime
from analyzers.basic_trade_stats import BasicTradeStats
from backtrader.analyzers.tradeanalyzer import TradeAnalyzer
import globals as gb
import strategies
from logger import *
from charts.plotter import PlotlyPlotter
from database.data_loader import DataLoader, StaticLoader
from utils import utils
import os


def main():
    utils.clean_previous_output()
    global cerebro
    cerebro = gb.cerebro
    add_strategies(CandlePatternLong)
    stock_for_testing = ['ABC.csv',   'BAC.csv',   'CDW.csv',   'CVX.csv',   'GD.csv',    'GPN.csv',   'IP.csv',    'JNJ.csv',   'LDOS.csv',  'MNST.csv',  'NKE.csv',   'OKE.csv', 'PNW.csv',   'RE.csv',    'STE.csv',   'UDR.csv',   'WELL.csv',  '^GSPC.csv', 'ADSK.csv',  'BR.csv','CNP.csv','EBAY.csv','GNRC.csv','HPQ.csv','JCI.csv','JNPR.csv', 'LNC.csv','MRO.csv', 'NVDA.csv', 'ORLY.csv', 'PVH.csv','SEE.csv','SWK.csv', 'VLO.csv',   'WHR.csv', 'ANSS.csv',  'CB.csv','CTAS.csv','EXR.csv','GOOG.csv', 'IFF.csv','JKHY.csv', 'JPM.csv','MCHP.csv','NFLX.csv','ODFL.csv', 'PKG.csv','PWR.csv','SNA.csv','TXT.csv', 'VRTX.csv',  'ZTS.csv']
    load_data(StaticLoader(cerebro), limit=0, random=False, start_date=datetime(2016,11,30), end_date=datetime(2021, 4, 26), dirpath='data_feeds', stock_names=stock_for_testing)
    # disk_data = bt.feeds.GenericCSVData(dataname='data_feeds/NVDA.csv', fromdate=datetime(2018, 9, 1), todate=datetime(2019,4,26), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)
    # cerebro.adddata(disk_data, name=disk_data._name)
    # add_analyzers()
    # add_observers()
    global strategies
    strategies = backtest()
    pass
    # show_statistics(strategies)
    # cerebro.plot(plotter=PlotlyPlotter(trades_only=True))


def add_strategies(strategy: bt.Strategy):
    loginfo(f'backtesting strategy {strategy.__class__.__name__}')
    cerebro.addstrategy(strategy)

def load_data(data_loader : DataLoader, **kwargs):
    data_loader.load_feeds(**kwargs)
    

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


#TODO cleanup
def plot(strategy: bt.Strategy, *args, **kwargs):
    strategy.plot(*args, **kwargs)


def show_statistics(strategies):
    loginfo(f'Final portfolio value: {cerebro.broker.getvalue():.2f}')
    strategies[0].analyzers.basic_trade_stats.print()
    print_trades_length(strategies[0].analyzers.tradeanalyzer)
    strategies[0].analyzers.exposer.print()
    '''
    strategies[0].analyzers.tradeanalyzer.print()
    strategies[0].analyzers.drawdown.print()
    strategies[0].analyzers.sqn.print()
    strategies[0].analyzers.sharperatio.print()
    strategies[0].analyzers.sharperatio_a.print()
    '''


if __name__ == '__main__':
    main()


