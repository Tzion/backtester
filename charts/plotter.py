from charts import charts
from charts.charts import ChartData, LabeledData
from utils.backtrader_helpers import extract_buynsell_observers, get_indicator_label, extract_line_data as eld, extract_line_data_datetime as eldd
from globals import *
import collections

class PlotlyPlotter():
    """
    This is an implementation of the plotter interface defined by backtrader (cerebro.plot(plotter, ...))
    It is based on inner charting implementation that uses Plotly to plot the data feed graphes.
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def plot(self, strategy: bt.Strategy, figid=0, numfigs=0, iplot=None, start=None, end=None, use=None):
        self.plot_strategy(strategy, **self.kwargs)
    
    def show(self):
        """ Do nothing - needed as part of the interface """
        pass

    def plot_strategy(self, strategy: bt.Strategy, **kwargs):
        self.charts = collections.defaultdict()
        self.load_price_data(strategy)
        self.load_indicators(strategy)
        self.load_buysell_markers(strategy)
        for chart in self.charts.values():
            fig = charts.plot_feed(chart, **kwargs)

    def load_price_data(self, strategy):
        for data in strategy.datas:
            chart = ChartData(data._name, eldd(data.datetime), open=eld(data.open), high=eld(data.high), low=eld(data.low), close=eld(data.close), volume=eld(data.volume), overlays_data=[], subplots_data=[])
            self.charts[data] = chart
    
    def load_indicators(self, strategy):
        for ind in strategy.getindicators():
            if not hasattr(ind, 'plotinfo') or not ind.plotinfo.plot or ind.plotinfo.plotskip:
                continue

            ind._plotinit()  # some indicators require preperation
            master = ind.plotinfo.plotmaster
            key = master if master is not ind and master is not None else ind._clock
            if key not in self.charts:
                key = key.owner  # maybe we need to iterate key over and over for indicators that are based on other indicators...?
            # key = key if not key is strategy else key.data  # special case for LinesCoupler
            if ind.plotinfo.subplot:
                self.charts[key].subplots_data.append(LabeledData(get_indicator_label(ind), eld(ind.line)))
            else:
                self.charts[key].overlays_data.append(LabeledData(get_indicator_label(ind), eld(ind.line)))
        
    def load_buysell_markers(self, strategy):
        for buysell in extract_buynsell_observers(strategy):
            self.charts[buysell.data].buy_markers = eld(buysell.buy)
            self.charts[buysell.data].sell_markers = eld(buysell.sell)




    