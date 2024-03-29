from datetime import datetime
import backtrader as bt
from backtrader.analyzers.tradeanalyzer import TradeAnalyzer
from backtrader.utils.dateintern import num2date
from charts import charts, translate
import pandas
from backtrader import num2date

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

def extract_indicator_lines(indicator) -> dict:
    lines = dict()
    for line_i in range(indicator.size()):
        line_alias = indicator.lines._getlinealias(line_i)
        lines[line_alias] = dict()
        lineplotdata = getattr(indicator, line_alias)
        lines[line_alias]['data'] = extract_line_data(lineplotdata)
        lineplotinfo = getattr(indicator.plotlines, line_alias)
        lines[line_alias]['metadata'] = lineplotinfo
    return lines

def indicator_to_lines_data(indicator) -> dict[str,charts.Line]:
    lines = dict()
    for line_i in range(indicator.size()):
        line_alias = indicator.lines._getlinealias(line_i)
        lineplotdata = getattr(indicator.lines, line_alias)
        lineplotinfo = getattr(indicator.plotlines, line_alias)
        lines[line_alias] = charts.Line(extract_line_data(lineplotdata), plotinfo_to_plotly_metadata(lineplotinfo))
    return lines

def plotinfo_to_plotly_metadata(plotinfo) -> dict:
    plot_attributes = plotinfo.__dict__.copy()
    plot_attributes.update(plotinfo._getitems())
    for key in list(plot_attributes):
        val = plot_attributes[key]
        new_key, new_val = translate(key, val)
        plot_attributes.pop(key)
        if new_key:
            plot_attributes[new_key] = new_val
    return plot_attributes

def get_alias(line: bt.LineSeries):
    if len(line.alias) > 0:
        return line.alias[0]
    return line.aliased or line.__class__.__name__