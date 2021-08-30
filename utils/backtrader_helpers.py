from datetime import datetime
import backtrader as bt
from backtrader.analyzers.tradeanalyzer import TradeAnalyzer
from backtrader.utils.dateintern import num2date

def extract_trades(strategy: bt.Strategy) -> list[bt.Trade]:
    trades = strategy._trades
    trades_list = [t[0][0] for t in list(trades.values())]
    assert len(trades) == len(trades_list), 'some trades were missed to be extracted'
    return trades_list

def extract_line_data(line : bt.linebuffer.LineBuffer) -> list[float]:
    values = line.getzero(size=len(line))
    return values if line.useislice else list(values)

def extract_date_line_data(datetime_line: bt.linebuffer.LineBuffer) -> list[datetime]:
    """
       Convert line buffer of dates of Matplotlib dates format to `~datetime.datetime` list.
    """
    formatted_dates = extract_line_data(datetime_line)
    datetime_dates = list(map(lambda fdate : num2date(fdate), formatted_dates))
    return datetime_dates

def print_trades_length(trade_analyzer: TradeAnalyzer):
    trades_len = trade_analyzer.get_analysis()['len']
    print(f'Trades length: Total: {trades_len.total}, Average: {trades_len.average}, Max: {trades_len.max}, Min: {trades_len.min}. Total bars: {len(trade_analyzer.strategy)}')

def extract_buynsell_observers(strategy: bt.Strategy):
    try:
        # TODO add validation of the type of each item in the list
        return strategy.observers.buysell # try the default name 
    except AttributeError:
        buynsell_observers = [obs for obs in strategy.getobservers() if type(obs) is bt.observers.BuySell]
        return buynsell_observers