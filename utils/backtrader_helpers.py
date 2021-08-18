import backtrader as bt
from backtrader.analyzers.tradeanalyzer import TradeAnalyzer

def extract_trades(strategy: bt.Strategy) -> list[bt.Trade]:
    trades = strategy._trades
    trades_list = [t[0][0] for t in list(trades.values())]
    assert len(trades) == len(trades_list), 'some trades were missed to be extracted'
    return trades_list

def print_trades_length(trade_analyzer: TradeAnalyzer):
    trades_len = trade_analyzer.get_analysis()['len']
    print(f'Trades length: Total: {trades_len.total}, Average: {trades_len.average}, Max: {trades_len.max}, Min: {trades_len.min}. Total bars: {len(strategies[0].data)}')