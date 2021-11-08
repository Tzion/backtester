from backtrader.feed import CSVDataBase
from charts import charts
from charts.charts import ChartData, LabeledData, LinesData
from utils.backtrader_helpers import extract_buynsell_observers, extract_indicator_lines, get_indicator_label, extract_line_data as eld, extract_line_data_datetime as eldd, indicator_to_lines_data
from globals import *
from utils import backtrader_helpers as bh
import logger

class PlotlyPlotter():
    """
    This is an implementation of the plotter interface defined by backtrader (cerebro.plot(plotter, ...))
    It is based on inner charting implementation that uses Plotly to plot the data feed graphes.
    """

    def __init__(self, trades_only=True, observers=True, pnl2duration=True, auto_open=False, save_to_file=True):
        self.trades_only = trades_only
        self.pnl2duration = pnl2duration
        self.observers = observers
        self.auto_open = auto_open
        self.save_to_file = save_to_file

    def plot(self, strategy: bt.Strategy, figid=0, numfigs=0, iplot=None, start=None, end=None, use=None):
        logger.loginfo(f'plotting strategy: {strategy.__class__.__name__}')
        self.plot_strategy(strategy)
    
    def show(self):
        """ Do nothing - needed as part of the interface """
        pass

    def plot_strategy(self, strategy: bt.Strategy):
        if self.observers:
            self.plot_observers(strategy)
        if self.pnl2duration:
            trades = bh.extract_trades_list(strategy)
            charts.plot_duration_to_profit([trade.pnl for trade in trades], [trade.barlen for trade in trades], self.auto_open, self.save_to_file)
        self.charts : dict[CSVDataBase, ChartData]
        self.select_charts(strategy)
        self.load_price_data(strategy)
        self.load_indicators(strategy)
        self.load_buysell_markers(strategy)
        for chart in self.charts.values():
            charts.plot_price_chart(chart, self.auto_open, self.save_to_file)
    
    def select_charts(self, strategy):
        if self.trades_only:
            self.charts = dict((data, None) for data in bh.extract_trades(strategy).keys())
        else:
            self.charts = dict((data, None) for data in strategy.datas)

    def load_price_data(self, strategy):
        for data in self.charts:
            chart = ChartData(data._name, eldd(data.datetime), open=eld(data.open), high=eld(data.high), low=eld(data.low), close=eld(data.close), volume=eld(data.volume), overlays_data=[], subplots_data=[])
            self.charts[data] = chart
    
    def load_indicators(self, strategy):
        data_keys = {key for key in strategy.datas} # required becuase we want to do __eq__ besed on the key and not based on the internal impl of __eq__ of strategy.datas
        for ind in strategy.getindicators():
            if not hasattr(ind, 'plotinfo') or not ind.plotinfo.plot or ind.plotinfo.plotskip:
                continue

            ind._plotinit()  # some indicators require preperation
            master = ind.plotinfo.plotmaster
            key = master if master is not ind and master is not None else ind._clock
            if key not in data_keys:
                key = key.owner  # maybe we need to iterate key over and over for indicators that are based on other indicators...?
            # key = key if not key is strategy else key.data  # special case for LinesCoupler
            if key not in self.charts:
                continue
            if ind.plotinfo.subplot:
                self.charts[key].subplots_data.append(LinesData(get_indicator_label(ind), extract_indicator_lines(ind), indicator_to_lines_data(ind)))
            else:
                self.charts[key].overlays_data.append(LinesData(get_indicator_label(ind), extract_indicator_lines(ind), indicator_to_lines_data(ind)))
        
    def load_buysell_markers(self, strategy):
        for buysell in extract_buynsell_observers(strategy):
            if buysell.data in self.charts:
                self.charts[buysell.data].buy_markers = eld(buysell.buy)
                self.charts[buysell.data].sell_markers = eld(buysell.sell)

    def plot_observers(self, strategy, **kwargs):
        for obs in strategy.observers:
            lines = {line: bh.extract_line_data(getattr(obs.lines,line)) for line in obs.lines.getlinealiases()}
            charts.plot_lines(bh.get_alias(obs), self.auto_open, self.save_to_file, **lines)


    