from charts.charts import ChartData, plot_feed
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
        self.charts_data = collections.defaultdict(ChartData)
        for data in strategy.datas:
            chart_data = ChartData(data._name, eldd(data.datetime), open=eld(data.open), high=eld(data.high), low=eld(data.low), close=eld(data.close), volume=eld(data.volume), overlays_data=[], subplots_data=[], sell_markers=None, buy_markers=None)
            self.charts_data[data] = chart_data
        for ind in strategy.getindicators():
            continue
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
        
        for buysell in extract_buynsell_observers(strategy):
            continue
            self.charts_data[buysell.data]['buy'] = eld(buysell.buy)
            self.charts_data[buysell.data]['sell'] = eld(buysell.sell)

        # plot charts
        for data,chart_data in self.charts_data.items():
            plot_feed(chart_data)




        
    @staticmethod
    def obtain_overlay_indicators(data):
        data



    