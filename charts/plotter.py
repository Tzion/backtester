from charts.charts import plot_feed
from utils.backtrader_helpers import extract_buynsell_observers, extract_line_data as eld, extract_line_data_datetime as eldd
from globals import *
import collections

class PlotlyPlotter():
    """
    This is an implementation of the plotter interface defined by backtrader (cerebro.plot(plotter, ...))
    It is based on inner charting implementation that uses Plotly to plot the data feed graphes.
    """

    def plot(self, strategy: bt.Strategy, figid=0, numfigs=0, iplot=None, start=None, end=None, use=None):
        self.plot_strategy(strategy)
    
    def show(self):
        """ Do nothing - needed as part of the interface """
        pass

    def plot_strategy(self, strategy: bt.Strategy):
        # TODO compare performace of dict and slots
        # self.charts_data = collections.defaultdict(ChartData)
        self.charts_data = collections.defaultdict(dict)
        for data in strategy.datas:
            chart_data = dict(timeline=eldd(data.datetime), open=eld(data.open), high=eld(data.high), low=eld(data.low), close=eld(data.close), volume=eld(data.volume))
            chart_data['subplots'] = []
            chart_data['overlays'] = []
            self.charts_data[data] = chart_data
        for ind in strategy.getindicators():
            if not hasattr(ind, 'plotinfo') or not ind.plotinfo.plot or ind.plotinfo.plotskip:
                continue

            ind._plotinit()  # some indicators require preperation
            master = ind.plotinfo.plotmaster
            key = master if master is not ind and master is not None else ind._clock
            if key not in self.charts_data:
                key = key.owner  # maybe we need to iterate key over and over for indicators that are based on other indicators...?
            # key = key if not key is strategy else key.data  # special case for LinesCoupler
            if ind.plotinfo.subplot:
                self.charts_data[key]['subplots'].append(eld(ind.line))
            else:
                self.charts_data[key]['overlays'].append(eld(ind.line))
        
        # plot charts
        for data,chart_data in self.charts_data.items():
            plot_feed(chart_data['timeline'], chart_data['open'], chart_data['high'], chart_data['low'], chart_data['close'], chart_data['volume'], chart_data['overlays'], chart_data['subplots'])
            # plot_feed(chart_data['timeline'], chart_data['open'], chart_data['high'], chart_data['low'], chart_data['close'], chart_data['volume'])



        
    @staticmethod
    def obtain_overlay_indicators(data):
        data



class ChartData:
    __slots__ = ('open', 'high', 'low', 'close' 'volume', 'overlays_data', 'subplots_data', 'buy_markers', 'sell_markers')
    