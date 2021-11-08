from datetime import datetime
import backtrader as bt
from backtrader.analyzers.tradeanalyzer import TradeAnalyzer
from backtrader.utils.dateintern import num2date

def extract_trades(strategy: bt.Strategy) -> dict[bt.DataBase, list[bt.Trade]]:
    '''
    returns a dictionary of data feed to its trades (by stripping the order_id from strategy._trades)
    '''
    trades = strategy._trades # trades is in the form of dict[feed, dict[order_id, trade]]
    all_trades = dict()
    for feed in trades.keys():
        trades_without_order_id = [trade for trade_group in trades[feed].values() for trade in trade_group]
        all_trades[feed] = trades_without_order_id
    return all_trades

def extract_trades_list(strategy: bt.Strategy) -> list[bt.Trade]:
    return [trade for trades in extract_trades(strategy).values() for trade in trades] 

def extract_line_data(line : bt.linebuffer.LineBuffer) -> list[float]:
    values = line.getzero(size=len(line))
    return values if line.useislice else list(values)

def extract_line_data_datetime(datetime_line: bt.linebuffer.LineBuffer) -> list[datetime]:
    """
       Convert line buffer of dates of Matplotlib dates format to `~datetime.datetime` list.
    """
    formatted_dates = extract_line_data(datetime_line)
    datetime_dates = list(map(lambda fdate : num2date(fdate), formatted_dates))
    return datetime_dates

def print_trades_length(trade_analyzer: TradeAnalyzer):
    trades_len = trade_analyzer.get_analysis().get('len')
    if trades_len:
        print(f'Trades length: Total: {trades_len.total}, Average: {trades_len.average}, Max: {trades_len.max}, Min: {trades_len.min}. Total bars: {len(trade_analyzer.strategy)}')

def extract_buynsell_observers(strategy: bt.Strategy) -> list[bt.observers.BuySell]:
    try:
        return strategy.observers.buysell # try the default name of the observer
        # TODO add validation of the type of each item in the list
    except AttributeError:
        buynsell_observers = [obs for obs in strategy.getobservers() if type(obs) is bt.observers.BuySell]
        return buynsell_observers


def get_indicator_label(indicator) -> str:
    # name = indicator.aliased or str(indicator).split('.')[-1].split(' ')[0]  # TODO this line was replaced by the one below- delete after validate
    name = indicator.aliased or indicator.__class__.__name__
    if hasattr(indicator.params, 'period'):
        name += '(' + str(indicator.params.period) + ')'
    elif hasattr(indicator.params, 'timeperiod'):
        name += '(' + str(indicator.params.timeperiod) + ')'
    return name

def extract_indicator_data(indicator) -> dict:
    metadata = dict()
    for line_i in range(indicator.size()):
        line_alias = indicator.lines._getlinealias(line_i)
        lineplotinfo = getattr(indicator.plotlines, line_alias)
        metadata[line_alias] = lineplotinfo.__dict__ # TODO use adapter from AutoClassInfo to plotly figure required data
        lineplotdata = getattr(indicator, line_alias)
        metadata[line_alias]['y'] = extract_line_data(lineplotdata)
    return metadata

def get_alias(line: bt.LineSeries):
    if len(line.alias) > 0:
        return line.alias[0]
    return line.aliased or line.__class__.__name__