from tests.test_common import *
from custom_indicators import visualizers
from charts.plotter import PlotlyPlotter
from backtrader_plotting.bokeh.bokeh import Bokeh
from backtrader_plotting.schemes.tradimo import Tradimo
from test_common import *
import backtrader as bt
from datetime import datetime
from charts.charts import LabeledData, plot_feed, _plot_feed
from utils.backtrader_helpers import extract_line_data as eld, extract_line_data_datetime as edld
from backtrader import indicators
import backtest

class FourIndicators(bt.Strategy):
    def __init__(self):
        for data in self.datas:
            data.moving_average = indicators.SMA(data.close, period=14, subplot=False)
            data.atr= indicators.ATR(data, period=4, subplot=True)
            data.atr2= indicators.ATR(data, period=10, subplot=True)
            data.buy_level = visualizers.PartialLevel(signal=data.high*1.05, level=data.high*1.05,length=1, plotmaster=data)

class BuyAndSellFirstDataOnly(bt.Strategy):
    def next(self):
        if self.datetime.idx % 31 == 0:
            self.buy()
        if self.datetime.idx % 47 == 0:
            self.sell()
        
def setup_and_run_strategy(strategy=FourIndicators, datas=[bt.feeds.GenericCSVData(dataname='tests/test_data.csv', fromdate=datetime(2016, 7, 1), todate=datetime(2017,6,30), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)]):
    cerebro = bt.Cerebro()
    for d in datas:
        cerebro.adddata(d)
    cerebro.addstrategy(strategy)
    strategy = cerebro.run()
    return strategy[0]

class TestChartsApi:

    def test_plot_with_sampled_data(self):
        print('Small chart with few candles')
        open_data = [33.0, 33.3, 33.5, 33.0, 33, 34.1]
        high_data = [33.1, 33.3, 33.6, 33.2, 33.5, 34.8]
        low_data = [32.7, 32.7, 32.8, 32.6, 32.8, 32.8]
        close_data = [33.0, 32.9, 33.3, 33.1, 33.2, 33.1]
        volume_data = [10, 2, 12, 42, 1, 40, 43]
        buy_markers = [33,] * 5
        dates = [datetime(year=2021, month=8, day=16), datetime(year=2021, month=8, day=17), datetime(year=2021, month=8, day=18), datetime(year=2021, month=8, day=19), datetime(year=2021, month=8, day=20), datetime(year=2021, month=8, day=23)]
        _plot_feed('sampled',dates, open_data, high_data, low_data, close_data, volume_data, buy_markers=buy_markers)

    def test_trade_markers_test(self):
        print('Plot chart with volume and buy&sell markers')
        strategy = setup_and_run_strategy(BuyAndSellFirstDataOnly, datas=[bt.feeds.GenericCSVData(dataname='tests/test_data.csv', fromdate=datetime(2016, 7, 1), todate=datetime(2017,6,30), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)])
        data = strategy.data0
        buysell = strategy.observers.buysell[0]
        _plot_feed(data._name, edld(data.datetime), eld(data.open), eld(data.high), eld(data.low), eld(data.close), eld(data.volume), buy_markers=eld(buysell.buy), sell_markers=eld(buysell.sell))

    def test_two_subplots(self):
        print('Chart with 2 subplots indicators')
        data = setup_and_run_strategy(datas=[bt.feeds.GenericCSVData(dataname='tests/test_data.csv', fromdate=datetime(2016, 7, 1), todate=datetime(2017,6,30), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)]).data
        overlay = LabeledData('overlay', eld(data.moving_average.line))
        subplots = [LabeledData('subplot1', eld(data.atr.line)), LabeledData('subplot2',eld(data.atr2.line))]
        _plot_feed(data._name, edld(data.datetime), eld(data.open), eld(data.high), eld(data.low), eld(data.close), eld(data.volume), overlays_data=[overlay], subplots_data=subplots)


    def test_candle_gaps_for_non_trading_days(self):
        print('Demosntrate the gaps on the x axis for days of no trading (weekends). problem solved when there\'s not gap')
        strategy = setup_and_run_strategy(datas = [bt.feeds.GenericCSVData(dataname='tests/test_data.csv', fromdate=datetime(2016, 12, 1), todate=datetime(2016,12,31), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)])
        data = strategy.data
        overlay = LabeledData('overlay', eld(data.moving_average.line))
        subplot = LabeledData('subplot', eld(data.atr.line))
        _plot_feed(data._name, edld(data.datetime), eld(data.open), eld(data.high), eld(data.low), eld(data.close), eld(data.volume), overlays_data=[overlay], subplots_data=[subplot])


class TestIntegrationWithCerebro:
    def test_plotter_integration(self):
        print('Expected output: 2 graphs each with 4 indicators and the first has buy&sell markers')
        cerebro = bt.Cerebro()
        modified_strategy = FourIndicators
        modified_strategy.next = BuyAndSellFirstDataOnly.next
        cerebro.addstrategy(modified_strategy)
        for d in [bt.feeds.GenericCSVData(dataname='tests/test_data.csv', fromdate=datetime(2016, 7, 1), todate=datetime(2017,6,30), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5),
                    bt.feeds.GenericCSVData(dataname='tests/test_data2.csv', fromdate=datetime(2016, 7, 1), todate=datetime(2017,6,30), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5)]:
            cerebro.adddata(d)
        cerebro.run()
        cerebro.plot(plotter=PlotlyPlotter())


    # change plot_number as required
    @pytest.mark.parametrize('plot_number', [(5)])
    def test_performance(self, plot_number):
        print(f'Plot {plot_number} charts - expecting it to be smooth')
        cerebro = bt.Cerebro()
        path = './data_feeds/'
        datas_path = [path + file_name for file_name in os.listdir(path)]
        datas = [bt.feeds.GenericCSVData(dataname=data_path, fromdate=datetime(2016, 11, 30), todate=datetime(2021,4,26), dtformat='%Y-%m-%d', high=1, low=2, open=3, close=4, volume=5) for data_path in datas_path]
        for d in datas[:plot_number]:
            cerebro.adddata(d)
        cerebro.addstrategy(FourIndicators)
        strategy = cerebro.run()
        cerebro.plot(plotter=PlotlyPlotter())




# Here for comparison if needed
def bokeh_test():
    cerebro = bt.Cerebro()
    backtest.add_data(limit=1, random=False, start_date=datetime(2016,11,30), end_date=datetime(2021, 4, 26), dirpath='../data_feeds')
    cerebro.addstrategy(FourIndicators)
    strategy = cerebro.run()
    strategy[0].data.plotinfo.plot=True
    plotter = Bokeh(style='bar', scheme=Tradimo())
    cerebro.plot(plotter=plotter, style='candlestick', barup='green', numfigs=1)

